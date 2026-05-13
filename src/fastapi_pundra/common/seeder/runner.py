"""Seeder runner — auto-discovers and orchestrates all seeders."""

import importlib
import inspect
import logging
import os
import pkgutil
import sys
import time
from types import ModuleType
from typing import Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fastapi_pundra.common.seeder.base import BaseSeeder

logger = logging.getLogger("fastapi_pundra.seeder")


def _configure_seeder_logging() -> None:
    """Ensure the seeder logger has a handler so messages are visible in CLI."""
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s.%(msecs)03d | %(levelname)-8s | "
                "%(name)s:%(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)


def _get_base_path() -> str:
    base_path = os.getenv("PROJECT_BASE_PATH", "app").strip()
    return base_path or "app"


def _resolve_seeds_package(seeds_package: ModuleType | None = None) -> ModuleType:
    """Resolve the seeds package from argument or PROJECT_BASE_PATH convention."""
    if seeds_package is not None:
        return seeds_package
    pkg_name = f"{_get_base_path()}.seeders.seeds"
    return importlib.import_module(pkg_name)


def _resolve_session_factory(
    session_factory: Callable[[], Session] | None = None,
) -> Callable[[], Session]:
    """Resolve session factory from argument or PROJECT_BASE_PATH convention."""
    if session_factory is not None:
        return session_factory
    mod_path = f"{_get_base_path()}.lib.database"
    module = importlib.import_module(mod_path)
    return getattr(module, "SessionLocal")


def _discover_seeders(seeds_package: ModuleType) -> list[type[BaseSeeder]]:
    """Auto-discover all BaseSeeder subclasses in the given seeds package."""
    seeders: list[type[BaseSeeder]] = []

    for module_info in pkgutil.iter_modules(
        seeds_package.__path__,
        prefix=seeds_package.__name__ + ".",
    ):
        module = importlib.import_module(module_info.name)
        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseSeeder) and obj is not BaseSeeder:
                seeders.append(obj)

    return sorted(seeders, key=lambda s: s.order)


def run_seeders(
    names: list[str] | None = None,
    *,
    seeds_package: ModuleType | None = None,
    session_factory: Callable[[], Session] | None = None,
) -> None:
    """Run all (or selected) seeders inside a single transaction.

    When called with no ``seeds_package`` / ``session_factory``, the runner
    auto-resolves them via the ``PROJECT_BASE_PATH`` env variable
    (default ``"app"``):

    * seeds package  → ``{PROJECT_BASE_PATH}.seeders.seeds``
    * session factory → ``{PROJECT_BASE_PATH}.lib.database.SessionLocal``

    Args:
        names: Optional list of seeder names to run. If ``None``, all
               discovered seeders are executed.
        seeds_package: Override — the Python package containing seeder modules.
        session_factory: Override — a callable returning a new SQLAlchemy ``Session``.
    """
    _configure_seeder_logging()

    resolved_pkg = _resolve_seeds_package(seeds_package)
    resolved_factory = _resolve_session_factory(session_factory)

    all_seeders = _discover_seeders(resolved_pkg)
    session: Session = resolved_factory()
    start = time.time()

    selected = all_seeders
    if names:
        lookup = {s.__name__.lower(): s for s in all_seeders}
        selected = []
        for n in names:
            key = n.lower().removesuffix("seeder") + "seeder"
            seeder_cls = lookup.get(key)
            if not seeder_cls:
                print(f"Unknown seeder: {n}")  # noqa: T201
                print(f"Available: {', '.join(s.__name__ for s in all_seeders)}")  # noqa: T201
                sys.exit(1)
            selected.append(seeder_cls)

    try:
        for seeder_cls in selected:
            seeder_cls().execute(session)
        session.commit()
        elapsed = time.time() - start
        logger.info("[Seeder] All seeders completed in %.2fs", elapsed)
        print(f"\nSeeding completed successfully ({elapsed:.2f}s)")  # noqa: T201
    except (SQLAlchemyError, ValueError, TypeError) as e:
        session.rollback()
        logger.error("[Seeder] Failed: %s", e)
        print(f"\nSeeding failed: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)
    finally:
        session.close()

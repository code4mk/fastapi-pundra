"""Auto-discovery and registration of FastAPI routers."""

import pkgutil
import importlib
from pathlib import Path
from fastapi import APIRouter


def auto_bind_router(
    router: APIRouter,
    api_package_path: str,
    skip_files: list[str] | None = None,
) -> APIRouter:
    """
    Auto-discover and bind routers from all modules in the specified package.

    This function automatically discovers and includes routers from:
    1. All Python files in the root of the API package (e.g., health.py, root_index.py)
    2. All subdirectories recursively (e.g., v1/, v2/, admin/, etc.)

    Note: Prefixes are NOT automatically added. Users should define prefixes
    in their router definitions if needed.

    Args:
        router: The main APIRouter instance to bind discovered routers to
        api_package_path: The package path (e.g., "app.api")
        skip_files: List of filenames to skip (default: ["__init__.py", "router.py"])

    Returns:
        The router instance with all discovered routers included

    Example:
        ```python
        from fastapi import APIRouter
        from fastapi_pundra.rest.route_register import auto_bind_router

        router = APIRouter()
        auto_bind_router(router, "app.api")
        ```
    """
    if skip_files is None:
        skip_files = ["__init__.py", "router.py"]

    # Get the package directory
    try:
        api_module = importlib.import_module(api_package_path)
        api_dir = Path(api_module.__file__).parent
    except (ImportError, AttributeError) as e:
        msg = f"Failed to import package {api_package_path}: {e}"
        raise ImportError(msg) from e

    # Auto-discover and include routers from all modules in the root package
    for file_path in api_dir.glob("*.py"):
        # Skip specified files
        if file_path.name in skip_files:
            continue

        module_name = file_path.stem
        try:
            module = importlib.import_module(f"{api_package_path}.{module_name}")
            if hasattr(module, "router"):
                router.include_router(module.router)
        except Exception:  # noqa: BLE001, S110
            pass  # Skip modules that fail to load

    # Auto-discover and include routers from all subdirectories recursively
    _discover_subdirectory_routers(router, api_package_path, api_dir, api_dir)

    return router


def _discover_subdirectory_routers(
    router: APIRouter,
    base_package_path: str,
    base_dir: Path,
    current_dir: Path,
) -> None:
    """
    Recursively discover routers in all subdirectories.

    Args:
        router: The main APIRouter instance to bind discovered routers to
        base_package_path: The base package path (e.g., "app.api")
        base_dir: The base directory of the package
        current_dir: The current directory to scan
    """
    for subdir in current_dir.iterdir():
        # Skip non-directories and private/special directories
        if not subdir.is_dir() or subdir.name.startswith("_"):
            continue

        try:
            # Build the package path relative to base
            relative_path = subdir.relative_to(base_dir)
            package_parts = [base_package_path] + list(relative_path.parts)
            package_path = ".".join(package_parts)

            # Import the package
            pkg = importlib.import_module(package_path)

            # Iterate through all modules in the package
            for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
                try:
                    module = importlib.import_module(f"{package_path}.{module_name}")
                    if hasattr(module, "router"):
                        # Include router without automatic prefix
                        router.include_router(module.router)
                except Exception:  # noqa: BLE001, S110
                    pass  # Skip modules that fail to load

            # Recursively scan subdirectories
            _discover_subdirectory_routers(router, base_package_path, base_dir, subdir)

        except Exception:  # noqa: BLE001, S110
            pass  # Skip packages that fail to load


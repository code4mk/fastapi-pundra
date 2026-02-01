"""Auto-discovery and registration of FastAPI routers."""

import pkgutil
import importlib
from pathlib import Path
from fastapi import APIRouter


def auto_bind_router(
    router: APIRouter,
    api_package_path: str,
    skip_files: list[str] | None = None,
    discover_versioned: bool = True,
) -> APIRouter:
    """
    Auto-discover and bind routers from all modules in the specified package.

    This function automatically discovers and includes routers from:
    1. All Python files in the root of the API package (e.g., health.py, root_index.py)
    2. All versioned subdirectories (e.g., v1/, v2/) if discover_versioned is True

    Args:
        router: The main APIRouter instance to bind discovered routers to
        api_package_path: The package path (e.g., "app.api")
        skip_files: List of filenames to skip (default: ["__init__.py", "router.py"])
        discover_versioned: Whether to discover routers in versioned subdirectories (default: True)

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

    # Auto-discover and include routers from versioned API folders (v1, v2, etc.)
    if discover_versioned:
        for subdir in api_dir.iterdir():
            if not subdir.is_dir() or subdir.name.startswith("_"):
                continue

            try:
                # Import the package
                pkg = importlib.import_module(f"{api_package_path}.{subdir.name}")

                # Iterate through all modules in the package
                for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
                    try:
                        module = importlib.import_module(
                            f"{api_package_path}.{subdir.name}.{module_name}"
                        )
                        if hasattr(module, "router"):
                            # Include with version prefix (e.g., /v1)
                            router.include_router(module.router, prefix=f"/{subdir.name}")
                    except Exception:  # noqa: BLE001, S110
                        pass  # Skip modules that fail to load
            except Exception:  # noqa: BLE001, S110
                pass  # Skip packages that fail to load

    return router


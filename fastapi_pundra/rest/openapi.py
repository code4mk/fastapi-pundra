"""OpenAPI schema generation utilities."""

import importlib
import inspect
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel


def openapi_request_body_schema(
    schema_class: type,
    *,
    required: bool = True,
    description: str | None = None,
    content_type: str = "application/json",
    examples: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Generate OpenAPI request body configuration for FastAPI routes.

    Args:
        schema_class: Pydantic model class to use for the request body schema
        required: Whether the request body is required (default: True)
        description: Optional description for the request body
        content_type: Content type for the request body (default: "application/json")
        examples: Optional dictionary of example requests (name -> example object)

    Returns:
        Dictionary containing OpenAPI requestBody configuration
    """
    content_config: dict[str, Any] = {
        "schema": schema_class.model_json_schema()
    }

    if examples:
        content_config["examples"] = examples

    config: dict[str, Any] = {
        "requestBody": {
            "content": {content_type: content_config},
            "required": required,
        }
    }

    if description:
        config["requestBody"]["description"] = description

    return config


def discover_schemas(schemas_package: str = "app.schemas") -> list[type[BaseModel]]:
    """
    Automatically discover all Pydantic schemas in the schemas package.

    Args:
        schemas_package: The package path to scan for schemas (default: "app.schemas")

    Returns:
        list: List of Pydantic BaseModel classes found

    """
    schemas = []
    
    # Get the schemas directory path
    try:
        package = importlib.import_module(schemas_package)
        package_path = Path(package.__file__).parent
    except (ImportError, AttributeError):
        return schemas

    # Iterate through all Python files in the schemas directory
    for file_path in package_path.glob("*.py"):
        if file_path.stem.startswith("_"):
            continue

        # Import the module
        module_name = f"{schemas_package}.{file_path.stem}"
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        # Find all Pydantic BaseModel subclasses in the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if (
                obj is not BaseModel
                and issubclass(obj, BaseModel)
                and obj.__module__ == module_name
            ):
                schemas.append(obj)

    return schemas


def generate_openapi_schema(app: FastAPI, schemas_to_register: list | None = None) -> dict:
    """
    Generate custom OpenAPI schema with additional schemas registered.

    Args:
        app: The FastAPI application instance
        schemas_to_register: Optional list of Pydantic schema classes to register

    Returns:
        dict: The OpenAPI schema dictionary

    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add custom schemas to components
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}

    # Register additional schemas if provided
    if schemas_to_register:
        for schema in schemas_to_register:
            schema_name = schema.__name__
            openapi_schema["components"]["schemas"][schema_name] = schema.model_json_schema()

    app.openapi_schema = openapi_schema
    return app.openapi_schema



from typing import Dict, Type, TypeVar

from pydantic import BaseModel

ProjectionModelType = TypeVar("ProjectionModelType", bound=BaseModel)


def get_projection(model: Type[ProjectionModelType]) -> Dict[str, int]:
    if hasattr(model, "Settings"):  # MyPy checks
        settings = getattr(model, "Settings")
        if hasattr(settings, "projection"):
            return getattr(settings, "projection")
    document_projection: Dict[str, int] = {
        field.alias: 1 for name, field in model.__fields__.items()
    }
    return document_projection

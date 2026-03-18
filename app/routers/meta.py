"""
/meta endpoint — used by the admin panel to discover available resources,
their fields, and API routes without hardcoding anything.
"""
from fastapi import APIRouter

from app import crud
from app.models.user import User
from app.models.category import Category
from app.models.product import Product

router = APIRouter(prefix="/meta", tags=["meta"])

RESOURCES = {
    "users": User,
    "categories": Category,
    "products": Product,
}


@router.get("/")
def get_meta():
    """
    Returns all registered resources with their field definitions.
    Use this in your admin panel to dynamically build tables and forms.
    """
    resources = []
    for name, model in RESOURCES.items():
        resources.append({
            "name": name,
            "label": name.replace("_", " ").title(),
            "endpoint": f"/api/{name}",
            "fields": crud.get_model_fields(model),
        })
    return {"resources": resources}


@router.get("/{resource}")
def get_resource_meta(resource: str):
    model = RESOURCES.get(resource)
    if not model:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource '{resource}' not found")
    return {
        "name": resource,
        "label": resource.replace("_", " ").title(),
        "endpoint": f"/api/{resource}",
        "fields": crud.get_model_fields(model),
    }

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import create_category, get_categories


router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_new_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_category(category_data, db)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_categories(db)
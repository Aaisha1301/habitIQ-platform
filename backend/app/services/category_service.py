from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def create_category(category_data: CategoryCreate, db: Session):
    existing_category = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=409,
            detail="Category already exists",
        )

    category = Category(**category_data.model_dump())

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session):
    return db.query(Category).order_by(Category.name.asc()).all()
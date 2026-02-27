from sqlalchemy.orm.session import Session
from schemas.category import CategoryBase
from fastapi import HTTPException
from db.models import DbCategory



# Add a new category
def add_category(db: Session, request: CategoryBase):

    category = db.query(DbCategory).filter(DbCategory.name == request.name).first()
    if category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = DbCategory(name=request.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category



# Get all categories
def get_categories(db: Session):
    return db.query(DbCategory).all()



# Delete category
def delete_category(db: Session, name: str):
    category = db.query(DbCategory).filter(DbCategory.name == name).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")

    db.delete(category)
    db.commit()
    return f" category {name} deleted"



# Update category
def update_category(db: Session, name: str, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.name == name).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")

    category.name = request.name
    db.commit()
    return f" category {name} is updated to {request.name}"


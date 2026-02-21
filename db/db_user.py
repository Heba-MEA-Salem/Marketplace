# CRUD for User
from sqlalchemy.orm.session import Session
from schemas.user import UserBase
from fastapi import HTTPException
from db.models import DbUser
from db.hash import Hash


# Create a new user
def create_user(db: Session, request: UserBase):

    # Check if the user is already exists
    existing_user = db.query(DbUser).filter(DbUser.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a user
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password= Hash.bcrypt(request.password)
    )

    """
        Add the new user to the database, 
        commit, refresh to get updated fields,
        and return it
    """
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user





# def get_user_by_id()
# def update_user()
# def delete_user()
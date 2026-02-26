# CRUD for User

from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from db.models import DbUser
from typing import Optional
from db.hash import Hash

# Create a new user
def create_user(db: Session, request: UserCreate):

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



# User login
def login_user(db: Session, request: UserLogin):
    # User can be DbUser or None (why using Optional)
    user: Optional[DbUser] = db.query(DbUser).filter(DbUser.email == request.email).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Compare plaintext password with hashed password
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return user




# def get_user_by_id()
def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")

    return user



# def update_user
def update_user(db: Session, id: int, request: UserCreate):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")


    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    db.commit()
    return 'Data has been updated!'





# def delete_user()
def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    db.delete(user)
    db.commit()
    return "ok"

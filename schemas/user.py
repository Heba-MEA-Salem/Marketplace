# User input/output schemas
from pydantic import BaseModel, EmailStr, field_validator


# Create user class, email validation, password validation function
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    # Validate the password
    @field_validator("confirm_password")
    def password_match(cls, confirm_password, info):
        if confirm_password != info.data.get("password"):
            raise ValueError("Password does not match")
        return confirm_password


# Response model to show user info without exposing passwords
class UserDisplay(BaseModel):
        username: str
        email: EmailStr
        class Config:
            orm_mode = True
# Password hashing (bcrypt)

from fastapi import HTTPException, status
import bcrypt

class Hash:
    @staticmethod
    def bcrypt(password: str):

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed_password: str):

        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')


        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password hash"
            )
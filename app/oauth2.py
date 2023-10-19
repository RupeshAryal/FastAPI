from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=config.settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, config.settings.secret_key, algorithm=config.settings.algorithm)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=config.settings.algorithm)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_expection = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_expection)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

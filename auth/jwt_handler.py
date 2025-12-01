import time
import jwt
from fastapi import HTTPException, status

SECRET = "CHANGE_THIS_PRODUCTION_SECRET"  # später .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 60 * 60 * 24  # 24h


def create_token(user_id: int, role: str):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": int(time.time() + ACCESS_TOKEN_EXPIRE)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token abgelaufen")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Ungültiger Token")

import time
import jwt
from fastapi import HTTPException, status
from decouple import config


# ---------------------------------------------------------
# ⚙️ ENV CONFIG
# ---------------------------------------------------------
SECRET = config("JWT_SECRET", default="CHANGE_ME")
ALGORITHM = "HS256"

ACCESS_EXPIRE = 60 * 60 * 24        # 24h Access Token
REFRESH_EXPIRE = 60 * 60 * 24 * 30  # 30 Tage Refresh Token


# ---------------------------------------------------------
# 🔐 ACCESS TOKEN ERSTELLEN
# ---------------------------------------------------------
def create_access_token(user_id: int, role: str):
    payload = {
        "type": "access",
        "user_id": user_id,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time() + ACCESS_EXPIRE)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


# ---------------------------------------------------------
# 🔐 REFRESH TOKEN ERSTELLEN
# ---------------------------------------------------------
def create_refresh_token(user_id: int):
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "iat": int(time.time()),
        "exp": int(time.time() + REFRESH_EXPIRE)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


# ---------------------------------------------------------
# 🔍 TOKEN DECODIEREN & VALIDIEREN
# ---------------------------------------------------------
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token abgelaufen"
        )

    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Signatur ungültig"
        )

    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token konnte nicht gelesen werden"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültiger Token"
        )

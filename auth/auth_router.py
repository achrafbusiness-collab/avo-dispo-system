from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.auth.password_handler import verify_password
from app.auth.jwt_handler import create_token, decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------------------------------------------------------
# 🔍 Aktuellen User anhand Token validieren
# ---------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Ungültiger Token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Benutzer existiert nicht")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Benutzer ist deaktiviert")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Token ungültig oder abgelaufen")


# ---------------------------------------------------------
# 🔐 LOGIN ENDPOINT
# ---------------------------------------------------------
@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email und Passwort erforderlich")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Benutzer nicht gefunden")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Falsches Passwort")

    token = create_token({"user_id": user.id, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal
from app.models.user import User
from app.auth.password_handler import hash_password, verify_password
from app.auth.jwt_handler import create_token, decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------------
# 🟢 TOKEN VALIDIEREN
# -------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user_id = payload.get("user_id")

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="Benutzer nicht gefunden")

    return user


# -------------------------------
# 🔐 LOGIN
# -------------------------------
@router.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user:
        raise HTTPException(status_code=400, detail="E-Mail existiert nicht")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Passwort falsch")

    token = create_token(user.id, user.role)

    return {"status": "ok", "token": token, "role": user.role}


# -------------------------------
# 👨‍✈️ ADMIN ERSTELLT FAHRER
# -------------------------------
@router.post("/register-driver")
async def register_driver(request: Request):
    data = await request.json()

    email = data.get("email")
    password = data.get("password")
    vorname = data.get("vorname")
    nachname = data.get("nachname")

    db = SessionLocal()

    # Prüfen ob User existiert
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="E-Mail bereits vergeben")

    # USER anlegen
    user = User(
        email=email,
        password_hash=hash_password(password),
        role="driver"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # DRIVER Profil anlegen
    driver = Driver(
        user_id=user.id,
        email=email,
        vorname=vorname,
        nachname=nachname
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)

    db.close()

    return {"status": "ok", "message": "Fahrer wurde erstellt", "driver_id": driver.id}

# -------------------------------
# 🔍 AKTUELLEN USER ABFRAGEN (SEHR WICHTIG FÜR APP)
# -------------------------------
@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }

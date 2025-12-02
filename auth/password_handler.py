from passlib.context import CryptContext
from fastapi import HTTPException

# ---------------------------------------------------------
# Passwort-Kontext: sichere bcrypt-Konfiguration
# ---------------------------------------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12   # höhere Sicherheit, gute Performance
)


# ---------------------------------------------------------
# Passwort hashen
# ---------------------------------------------------------
def hash_password(password: str) -> str:
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Passwort muss mindestens 6 Zeichen haben")

    try:
        return pwd_context.hash(password)
    except Exception:
        raise HTTPException(status_code=500, detail="Fehler beim Hashen des Passworts")


# ---------------------------------------------------------
# Passwort validieren
# ---------------------------------------------------------
def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        raise HTTPException(status_code=400, detail="Passwort-Überprüfung fehlgeschlagen")

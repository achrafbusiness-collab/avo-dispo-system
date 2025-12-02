# app/routes/dashboard.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models import Order, ImportedOrder

router = APIRouter()

# Templates-Verzeichnis korrekt setzen
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Statistiken abrufen
    orders_count = db.query(Order).count()
    pending_imports = db.query(ImportedOrder).count()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "orders_count": orders_count,
            "pending_imports": pending_imports
        }
    )

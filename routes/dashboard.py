# app/routes/dashboard.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.models import Order, ImportedOrder
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(BASE_DIR), "templates"))


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    db = SessionLocal()
    orders_count = db.query(Order).count()
    pending_imports = db.query(ImportedOrder).count()
    db.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "orders_count": orders_count,
        "pending_imports": pending_imports
    })

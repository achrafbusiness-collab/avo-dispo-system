# app/routes/orders.py

from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models import Order, Driver


router = APIRouter()

# Templates-Verzeichnis
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ============================================================
# 📦 Alle Aufträge anzeigen
# ============================================================
@router.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, db: Session = Depends(get_db)):

    orders = db.query(Order).all()

    return templates.TemplateResponse(
        "orders.html",
        {
            "request": request,
            "orders": orders
        }
    )


# ============================================================
# ➕ Neuer Auftrag – Formularseite
# ============================================================
@router.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request, db: Session = Depends(get_db)):

    drivers = db.query(Driver).all()

    return templates.TemplateResponse(
        "new_order.html",
        {
            "request": request,
            "drivers": drivers
        }
    )


# ============================================================
# ➕ Neuer Auftrag – POST (Speichern)
# ============================================================
@router.post("/orders/new")
async def create_order(
    request: Request,
    kennzeichen: str = Form(...),
    modell: str = Form(None),
    vin: str = Form(None),
    fahrer_id: int = Form(None),
    db: Session = Depends(get_db)
):

    new_order = Order(
        kennzeichen=kennzeichen,
        modell=modell,
        vin=vin,
        fahrer_id=fahrer_id,
        status="neu"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return RedirectResponse(f"/orders/{new_order.id}", status_code=303)


# ============================================================
# 📄 Auftragsdetails
# ============================================================
@router.get("/orders/{order_id}", response_class=HTMLResponse)
async def order_detail(order_id: int, request: Request, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Auftrag nicht gefunden")

    drivers = db.query(Driver).all()

    return templates.TemplateResponse(
        "order_detail.html",
        {
            "request": request,
            "order": order,
            "drivers": drivers
        }
    )


# ============================================================
# ✏️ Auftrag bearbeiten – Formularseite
# ============================================================
@router.get("/orders/{order_id}/edit", response_class=HTMLResponse)
async def edit_order_page(order_id: int, request: Request, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Auftrag nicht gefunden")

    drivers = db.query(Driver).all()

    return templates.TemplateResponse(
        "edit_order.html",
        {
            "request": request,
            "order": order,
            "drivers": drivers
        }
    )


# ============================================================
# ✏️ Auftrag aktualisieren – POST
# ============================================================
@router.post("/orders/{order_id}/edit")
async def update_order(
    order_id: int,
    kennzeichen: str = Form(None),
    modell: str = Form(None),
    vin: str = Form(None),
    fahrer_id: int = Form(None),
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Auftrag nicht gefunden")

    order.kennzeichen = kennzeichen
    order.modell = modell
    order.vin = vin
    order.fahrer_id = fahrer_id

    db.commit()

    return RedirectResponse(f"/orders/{order_id}", status_code=303)


# ============================================================
# ❌ Auftrag löschen
# ============================================================
@router.post("/orders/{order_id}/delete")
async def delete_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Auftrag nicht gefunden")

    db.delete(order)
    db.commit()

    return RedirectResponse("/orders", status_code=303)

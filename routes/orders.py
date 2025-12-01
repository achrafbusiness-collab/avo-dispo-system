# app/routes/orders.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.models import Order, Driver
import traceback
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(BASE_DIR), "templates"))


# ============================================================
# 📦 Alle Aufträge anzeigen
# ============================================================
@router.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()

    return templates.TemplateResponse("orders.html", {
        "request": request,
        "orders": orders
    })


# ============================================================
# ➕ Neuer Auftrag – Formularseite
# ============================================================
@router.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request):
    db = SessionLocal()
    drivers = db.query(Driver).all()
    db.close()

    return templates.TemplateResponse("new_order.html", {
        "request": request,
        "drivers": drivers
    })


# ============================================================
# 🟢 Auftrag erstellen
# ============================================================
@router.post("/create-order")
async def create_order(request: Request):
    form = await request.form()
    data = {k: v.strip() if isinstance(v, str) else v for k, v in form.items()}

    # Typen konvertieren
    for key in ["kilometer", "preis", "preis_selbstst"]:
        try:
            data[key] = float(data[key]) if data.get(key) else None
        except:
            data[key] = None

    if data.get("fahrer_id") == "":
        data["fahrer_id"] = None

    db = SessionLocal()
    try:
        order = Order(**data)
        db.add(order)
        db.commit()
        print(f"✅ Auftrag erstellt (ID {order.id})")

    except Exception as e:
        db.rollback()
        print("❌ Fehler beim Erstellen eines Auftrags:", e)
        traceback.print_exc()

    finally:
        db.close()

    return RedirectResponse("/orders", status_code=303)


# ============================================================
# ✏️ Auftrag bearbeiten – Formularseite
# ============================================================
@router.get("/orders/{order_id}/edit", response_class=HTMLResponse)
async def edit_order_page(request: Request, order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    drivers = db.query(Driver).all()
    db.close()

    if not order:
        return RedirectResponse("/orders", status_code=303)

    return templates.TemplateResponse("edit_order.html", {
        "request": request,
        "order": order,
        "drivers": drivers
    })


# ============================================================
# 🔄 Auftrag aktualisieren
# ============================================================
@router.post("/orders/{order_id}/update")
async def update_order(request: Request, order_id: int):
    form = await request.form()
    data = dict(form)

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return RedirectResponse("/orders", status_code=303)

        for k, v in data.items():
            if hasattr(order, k):
                if k in ["kilometer", "preis", "preis_selbstst"]:
                    try:
                        v = float(v)
                    except:
                        v = None

                if k == "fahrer_id" and v == "":
                    v = None

                setattr(order, k, v)

        db.commit()
        print(f"🔄 Auftrag {order_id} aktualisiert.")

    except Exception as e:
        db.rollback()
        print("❌ Fehler beim Update des Auftrags:", e)
        traceback.print_exc()

    finally:
        db.close()

    return RedirectResponse("/orders", status_code=303)


# ============================================================
# 🗑️ Auftrag löschen
# ============================================================
@router.get("/orders/{order_id}/delete")
async def delete_order(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if order:
            db.delete(order)
            db.commit()
            print(f"🗑️ Auftrag {order_id} gelöscht.")

    except Exception as e:
        db.rollback()
        print("❌ Fehler beim Löschen:", e)

    finally:
        db.close()

    return RedirectResponse("/orders", status_code=303)

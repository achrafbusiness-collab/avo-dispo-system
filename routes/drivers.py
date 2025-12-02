# app/routes/drivers.py

from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Driver
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Templates finden
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ============================================================
# Fahrer Liste
# ============================================================
@router.get("/drivers", response_class=HTMLResponse)
async def list_drivers(request: Request, db: Session = Depends(get_db)):
    drivers = db.query(Driver).all()
    return templates.TemplateResponse(
        "drivers.html",
        {"request": request, "drivers": drivers}
    )


# ============================================================
# Fahrer Details
# ============================================================
@router.get("/drivers/{driver_id}", response_class=HTMLResponse)
async def driver_detail(driver_id: int, request: Request, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Fahrer nicht gefunden")

    return templates.TemplateResponse(
        "driver_detail.html",
        {"request": request, "driver": driver}
    )


# ============================================================
# Fahrer bearbeiten – GET FORM
# ============================================================
@router.get("/drivers/{driver_id}/edit", response_class=HTMLResponse)
async def edit_driver_form(driver_id: int, request: Request, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Fahrer nicht gefunden")

    return templates.TemplateResponse(
        "edit_driver.html",
        {"request": request, "driver": driver}
    )


# ============================================================
# Fahrer bearbeiten – POST
# ============================================================
@router.post("/drivers/{driver_id}/edit")
async def update_driver(
    driver_id: int,
    vorname: str = Form(...),
    nachname: str = Form(...),
    telefonnummer: str = Form(None),
    stadt: str = Form(None),
    db: Session = Depends(get_db)
):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Fahrer nicht gefunden")

    driver.vorname = vorname
    driver.nachname = nachname
    driver.telefonnummer = telefonnummer
    driver.stadt = stadt

    db.commit()

    return RedirectResponse(f"/drivers/{driver_id}", status_code=303)


# ============================================================
# Fahrer löschen
# ============================================================
@router.post("/drivers/{driver_id}/delete")
async def delete_driver(driver_id: int, db: Session = Depends(get_db)):

    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Fahrer nicht gefunden")

    db.delete(driver)
    db.commit()

    return RedirectResponse("/drivers", status_code=303)

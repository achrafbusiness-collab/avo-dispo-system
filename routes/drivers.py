from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models import Driver

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ===========================
# Fahrerübersicht
# ===========================
@router.get("/drivers")
async def drivers_page(request: Request):
    db = SessionLocal()
    drivers = db.query(Driver).all()
    db.close()
    return templates.TemplateResponse("drivers.html", {"request": request, "drivers": drivers})


# ===========================
# Neuer Fahrer – Seite laden
# ===========================
@router.get("/drivers/new")
async def new_driver_page(request: Request):
    return templates.TemplateResponse("new_driver.html", {"request": request})


# ===========================
# Neuer Fahrer – absenden
# ===========================
@router.post("/drivers/create")
async def create_driver(request: Request):
    form = await request.form()
    data = {k: (v.strip() if isinstance(v, str) else v) for k, v in form.items()}

    db = SessionLocal()
    try:
        driver = Driver(**data)
        db.add(driver)
        db.commit()
        db.refresh(driver)
        print(f"Neuer Fahrer gespeichert: {driver.vorname} {driver.nachname}")
    except Exception as e:
        db.rollback()
        print("❌ Fehler beim Erstellen des Fahrers:", e)
    finally:
        db.close()

    return RedirectResponse("/drivers", status_code=303)


# ===========================
# Fahrer ansehen
# ===========================
@router.get("/drivers/{driver_id}")
async def driver_detail(request: Request, driver_id: int):
    db = SessionLocal()
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    db.close()

    if not driver:
        return templates.TemplateResponse("driver_not_found.html", {"request": request})

    return templates.TemplateResponse("driver_detail.html", {"request": request, "driver": driver})


# ===========================
# Fahrer bearbeiten – Seite laden
# ===========================
@router.get("/drivers/{driver_id}/edit")
async def edit_driver_page(request: Request, driver_id: int):
    db = SessionLocal()
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    db.close()

    return templates.TemplateResponse("edit_driver.html", {"request": request, "driver": driver})


# ===========================
# Fahrer bearbeiten – absenden
# ===========================
@router.post("/drivers/{driver_id}/update")
async def update_driver(request: Request, driver_id: int):
    form = await request.form()
    data = dict(form)

    db = SessionLocal()
    try:
        driver = db.query(Driver).filter(Driver.id == driver_id).first()

        for key, value in data.items():
            if hasattr(driver, key):
                setattr(driver, key, value if value != "" else None)

        db.commit()
    except Exception as e:
        db.rollback()
        print("❌ Fehler beim Update:", e)
    finally:
        db.close()

    return RedirectResponse(f"/drivers/{driver_id}", status_code=303)


# ===========================
# Fahrer löschen
# ===========================
@router.post("/drivers/{driver_id}/delete")
async def delete_driver(driver_id: int):
    db = SessionLocal()
    try:
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        db.delete(driver)
        db.commit()
    except Exception as e:
        db.rollback()
        print("❌ Fehler beim Löschen:", e)
    finally:
        db.close()

    return RedirectResponse("/drivers", status_code=303)

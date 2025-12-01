# app/routes/import_center.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.models import ImportedOrder, Order, Driver
from app.services.email_service import fetch_imports, test_imap_connection
from app.services.ai_service import extract_with_ai
import traceback
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(BASE_DIR), "templates"))


# ============================================================
# 📥 Import-Center Übersicht
# ============================================================
@router.get("/import", response_class=HTMLResponse)
async def import_page(request: Request):
    db = SessionLocal()
    imports = db.query(ImportedOrder).order_by(ImportedOrder.created_at.desc()).all()
    db.close()

    return templates.TemplateResponse("import.html", {
        "request": request,
        "imports": imports
    })


# ============================================================
# 🟢 IMAP Verbindung testen
# ============================================================
@router.get("/api/import/test")
async def api_import_test():
    try:
        result = test_imap_connection()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================
# 📧 Neue ungelesene Emails importieren
# ============================================================
@router.get("/api/import/fetch")
async def api_fetch_imports():
    try:
        created_ids = fetch_imports()
        return {"status": "ok", "created": created_ids}

    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


# ============================================================
# 📄 Import-Detailseite
# ============================================================
@router.get("/import/{imp_id}", response_class=HTMLResponse)
async def import_detail_page(request: Request, imp_id: int):
    db = SessionLocal()
    imp = db.query(ImportedOrder).filter(ImportedOrder.id == imp_id).first()
    drivers = db.query(Driver).all()
    db.close()

    if not imp:
        return templates.TemplateResponse("import_detail_missing.html", {
            "request": request,
            "id": imp_id
        })

    return templates.TemplateResponse("import_detail.html", {
        "request": request,
        "imp": imp,
        "drivers": drivers
    })


# ============================================================
# 🟡 Import bestätigen → Auftrag erstellen
# ============================================================
@router.post("/api/import/confirm/{imp_id}")
async def confirm_import(request: Request, imp_id: int):
    from app.services.order_service import promote_imported_order

    db = SessionLocal()
    try:
        imp = db.query(ImportedOrder).filter(ImportedOrder.id == imp_id).first()
        if not imp:
            return {"status": "error", "message": "Import nicht gefunden"}

        # Form-Daten überschreiben
        form = await request.form()
        for k, v in form.items():
            if hasattr(imp, k):
                setattr(imp, k, v)

        db.commit()

        new_order_id = promote_imported_order(imp)

        return {"status": "ok", "order_id": new_order_id}

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    finally:
        db.close()


# ============================================================
# 🗑️ Import löschen
# ============================================================
@router.post("/api/import/discard/{imp_id}")
async def discard_import(imp_id: int):
    db = SessionLocal()
    try:
        imp = db.query(ImportedOrder).filter(ImportedOrder.id == imp_id).first()

        if not imp:
            return {"status": "error", "message": "Import nicht gefunden"}

        db.delete(imp)
        db.commit()
        return {"status": "ok"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        db.close()

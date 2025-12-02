# app/routes/import_center.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models import ImportedOrder, Order

router = APIRouter()

# Templates laden
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ============================================================
# Import Center – Liste aller importierten Aufträge
# ============================================================
@router.get("/import", response_class=HTMLResponse)
async def import_list(request: Request, db: Session = Depends(get_db)):

    imports = db.query(ImportedOrder)\
                .order_by(ImportedOrder.received_at.desc())\
                .all()

    return templates.TemplateResponse(
        "import_center.html",
        {
            "request": request,
            "imports": imports
        }
    )


# ============================================================
# Import Detail
# ============================================================
@router.get("/import/{imp_id}", response_class=HTMLResponse)
async def import_detail(imp_id: int, request: Request, db: Session = Depends(get_db)):

    imp = db.query(ImportedOrder).filter(ImportedOrder.id == imp_id).first()

    if not imp:
        raise HTTPException(status_code=404, detail="Import nicht gefunden")

    return templates.TemplateResponse(
        "import_detail.html",
        {
            "request": request,
            "imp": imp
        }
    )


# ============================================================
# Import verwerfen (löschen)
# ============================================================
@router.post("/import/{imp_id}/discard")
async def discard_import(imp_id: int, db: Session = Depends(get_db)):

    imp = db.query(ImportedOrder).filter(ImportedOrder.id == imp_id).first()

    if not imp:
        raise HTTPException(status_code=404, detail="Import nicht gefunden")

    db.delete(imp)
    db.commit()

    return RedirectResponse("/import", status_code=303)


# ============================================================
# Import → Auftrag konvertieren
# ============================================================
@router.post("/import/{imp_id}/convert")
async def convert_import(imp_id: int, db: Session = Depends(get_db)):

    imp = db.query(ImportedOrder).filter(ImportedOrder.id == imp_id).first()

    if not imp:
        raise HTTPException(status_code=404, detail="Import nicht gefunden")

    # Auftrag erzeugen
    new_order = Order(
        status="neu",
        kennzeichen=imp.kennzeichen,
        modell=imp.modell,
        vin=imp.fin,

        abhol_strasse=imp.abhol_strasse,
        abhol_str_nr=imp.abhol_str_nr,
        abhol_plz=imp.abhol_plz,
        abhol_stadt=imp.abhol_stadt,
        ap_abholung=imp.ap_abholung,
        kontakt_abholung=imp.kontakt_abholung,
        abhol_datum=imp.abhol_datum,

        anliefer_strasse=imp.anliefer_strasse,
        anliefer_str_nr=imp.anliefer_str_nr,
        anliefer_plz=imp.anliefer_plz,
        anliefer_stadt=imp.anliefer_stadt,
        ap_anlieferung=imp.ap_anlieferung,
        kontakt_anlieferung=imp.kontakt_anlieferung,
        anliefer_datum=imp.anliefer_datum,
    )

    db.add(new_order)

    # Import als verarbeitet markieren
    imp.converted_to_order = True

    db.commit()

    return RedirectResponse(f"/orders/{new_order.id}", status_code=303)

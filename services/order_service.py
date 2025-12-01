# app/services/order_service.py

from app.database import SessionLocal
from app.models import ImportedOrder, Order
import traceback


# ============================================================
# Importierter Auftrag wird zu echtem Auftrag
# ============================================================

def promote_imported_order(imp: ImportedOrder):
    db = SessionLocal()

    try:
        order = Order(
            mv_nr = imp.mv_nr,
            kennzeichen = imp.kennzeichen,
            modell = imp.modell,
            fin = imp.fin,
            auftraggeber = imp.auftraggeber,
            infofeld = imp.infofeld,

            abhol_stadt = imp.abhol_stadt,
            abhol_strasse = imp.abhol_strasse,
            abhol_str_nr = imp.abhol_str_nr,
            abhol_plz = imp.abhol_plz,
            kontakt_abholung = imp.kontakt_abholung,
            ap_abholung = imp.ap_abholung,
            abholdatum = imp.abholdatum,
            abhol_von = imp.abhol_von,
            abhol_bis = imp.abhol_bis,

            anliefer_stadt = imp.anliefer_stadt,
            anliefer_strasse = imp.anliefer_strasse,
            anliefer_str_nr = imp.anliefer_str_nr,
            anliefer_plz = imp.anliefer_plz,
            kontakt_anlieferung = imp.kontakt_anlieferung,
            ap_anlieferung = imp.ap_anlieferung,
            anlieferdatum = imp.anlieferdatum,
            anliefer_von = imp.anliefer_von,
            anliefer_bis = imp.anliefer_bis,

            kilometer = imp.kilometer,
            preis = imp.preis,
            preis_selbstst = imp.preis_selbstst,
            fahrer_id = imp.fahrer_id
        )

        db.add(order)
        db.delete(imp)
        db.commit()
        db.refresh(order)

        print(f"📦 Neuer Auftrag angelegt aus Import (ID {order.id})")
        return order.id

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        return None

    finally:
        db.close()

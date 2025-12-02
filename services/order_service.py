# app/services/order_service.py

from sqlalchemy.orm import Session
from app.models import ImportedOrder, Order
import traceback


# ============================================================
# IMPORT → ORDER KONVERTIERUNG
# ============================================================
def promote_imported_order(db: Session, imp: ImportedOrder):
    """
    Wandelt einen ImportedOrder in einen echten Order um.
    Erwartet eine bestehende DB-Session (db), nicht SessionLocal().
    """

    try:
        new_order = Order(
            status="neu",

            # Fahrzeugdaten
            kennzeichen=imp.kennzeichen,
            modell=imp.modell,
            vin=imp.fin,

            # Abholung
            abhol_stadt=imp.abhol_stadt,
            abhol_strasse=imp.abhol_strasse,
            abhol_str_nr=imp.abhol_str_nr,
            abhol_plz=imp.abhol_plz,
            ap_abholung=imp.ap_abholung,
            kontakt_abholung=imp.kontakt_abholung,
            abhol_datum=imp.abhol_datum,

            # Anlieferung
            anliefer_stadt=imp.anliefer_stadt,
            anliefer_strasse=imp.anliefer_strasse,
            anliefer_str_nr=imp.anliefer_str_nr,
            anliefer_plz=imp.anliefer_plz,
            ap_anlieferung=imp.ap_anlieferung,
            kontakt_anlieferung=imp.kontakt_anlieferung,
            anliefer_datum=imp.anliefer_datum,

            # Info
            # Falls du später Auftraggeber brauchst – hier müsste es ergänzt werden
        )

        db.add(new_order)

        # Import als umgewandelt markieren
        imp.converted_to_order = True

        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception as e:
        traceback.print_exc()
        db.rollback()
        raise RuntimeError("Fehler beim Konvertieren des ImportedOrder → Order") from e

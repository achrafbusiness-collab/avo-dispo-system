# models/imported_order.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
import datetime
from app.database import Base


class ImportedOrder(Base):
    __tablename__ = "imported_orders"

    id = Column(Integer, primary_key=True, index=True)

    # Original Email Infos
    source_msg_id = Column(String(200))
    subject = Column(String(500))
    sender = Column(String(300))
    received_at = Column(DateTime, default=datetime.datetime.utcnow)
    raw_text = Column(Text)

    # Fahrzeugdaten
    mv_nr = Column(String(100))
    kennzeichen = Column(String(50))
    modell = Column(String(100))
    fin = Column(String(100))

    # Auftraggeber
    auftraggeber = Column(String(200))
    infofeld = Column(Text)

    # Abholung
    abhol_stadt = Column(String(100))
    abhol_strasse = Column(String(200))
    abhol_str_nr = Column(String(50))
    abhol_plz = Column(String(20))
    kontakt_abholung = Column(String(100))
    ap_abholung = Column(String(100))
    abhol_datum = Column(DateTime)
    abhol_von = Column(String(20))
    abhol_bis = Column(String(20))

    # Anlieferung
    anliefer_stadt = Column(String(100))
    anliefer_strasse = Column(String(200))
    anliefer_str_nr = Column(String(50))
    anliefer_plz = Column(String(20))
    kontakt_anlieferung = Column(String(100))
    ap_anlieferung = Column(String(100))
    anliefer_datum = Column(DateTime)

    # Systemstatus
    converted_to_order = Column(Boolean, default=False)  # wurde daraus ein echter Auftrag?
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

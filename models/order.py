# models/order.py

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Allgemein
    mv_nr = Column(String(100))
    kennzeichen = Column(String(50))
    modell = Column(String(100))
    fin = Column(String(100))
    auftraggeber = Column(String(200))
    infofeld = Column(Text)

    # Abholung
    abhol_stadt = Column(String(100))
    abhol_strasse = Column(String(200))
    abhol_str_nr = Column(String(50))
    abhol_plz = Column(String(20))
    kontakt_abholung = Column(String(100))
    ap_abholung = Column(String(100))
    abholdatum = Column(String(50))
    abhol_von = Column(String(50))
    abhol_bis = Column(String(50))

    # Anlieferung
    anliefer_stadt = Column(String(100))
    anliefer_strasse = Column(String(200))
    anliefer_str_nr = Column(String(50))
    anliefer_plz = Column(String(20))
    kontakt_anlieferung = Column(String(100))
    ap_anlieferung = Column(String(100))
    anlieferdatum = Column(String(50))
    anliefer_von = Column(String(50))
    anliefer_bis = Column(String(50))

    # Sonstiges
    kilometer = Column(Float)
    preis = Column(Float)
    preis_selbstst = Column(Float)

    # Fahrer
    fahrer_id = Column(Integer, ForeignKey("drivers.id"))
    fahrer = relationship("Driver", lazy="joined")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Status
    status = Column(
        String(50),
        default="neu"
    )  
    # mögliche Werte:
    # neu / zugewiesen / unterwegs / abgeholt / geliefert / abgeschlossen

    # Fahrzeugdaten
    kennzeichen = Column(String(50))
    modell = Column(String(100))
    vin = Column(String(100))

    # Abholung
    abhol_strasse = Column(String(200))
    abhol_str_nr = Column(String(50))
    abhol_plz = Column(String(20))
    abhol_stadt = Column(String(100))
    kontakt_abholung = Column(String(100))
    ap_abholung = Column(String(100))
    abhol_datum = Column(DateTime)
    abhol_von = Column(String(20))
    abhol_bis = Column(String(20))

    # Anlieferung
    anliefer_strasse = Column(String(200))
    anliefer_str_nr = Column(String(50))
    anliefer_plz = Column(String(20))
    anliefer_stadt = Column(String(100))
    kontakt_anlieferung = Column(String(100))
    ap_anlieferung = Column(String(100))
    anliefer_datum = Column(DateTime)
    anliefer_von = Column(String(20))
    anliefer_bis = Column(String(20))

    # Fahrer (Beziehung)
    fahrer_id = Column(Integer, ForeignKey("drivers.id"))
    fahrer = relationship("Driver", back_populates="orders")

    # Preise & km
    preis_selbstst = Column(Float)
    preis = Column(Float)
    kilometer = Column(Float)

    # System
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow
    )

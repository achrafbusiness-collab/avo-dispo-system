from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from app.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    # Verbindung zu User-Account
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="driver_profile")

    # Fahrerprofil
    vorname = Column(String(50), nullable=False)
    nachname = Column(String(50), nullable=False)
    telefonnummer = Column(String(50))
    stadt = Column(String(100))

    # Dokumente
    fuehrerschein_nummer = Column(String(50))
    fuehrerschein_ablauf = Column(DateTime)   # echtes Datum statt String
    fuehrerschein_vorne_url = Column(String(255))
    fuehrerschein_hinten_url = Column(String(255))
    ausweis_vorne_url = Column(String(255))
    ausweis_hinten_url = Column(String(255))

    # Systemstatus
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    orders = relationship("Order", back_populates="driver")
    checklists = relationship("Checklist", back_populates="driver")

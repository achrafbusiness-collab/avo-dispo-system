from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    # Login-Verknüpfung
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    # Fahrerprofil
    vorname = Column(String(50))
    nachname = Column(String(50))
    telefonnummer = Column(String(50))
    email = Column(String(100))
    stadt = Column(String(100))

    fuehrerschein_nr = Column(String(50))
    fuehrerschein_ablauf = Column(String(50))

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

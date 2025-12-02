# app/models/user.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Login-Daten
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # role = admin / driver
    role = Column(String(50), default="driver", nullable=False)

    # Systemstatus
    is_active = Column(Boolean, default=True)
    failed_attempts = Column(Integer, default=0)
    last_login = Column(DateTime)

    # Zeitstempel
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Beziehung zu Fahrerprofil
    driver_profile = relationship("Driver", back_populates="user", uselist=False)

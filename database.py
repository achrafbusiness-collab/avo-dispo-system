# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Pfad zur SQLite-Datenbank erstellen
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "avo_logistics.db")

# SQLite-Engine
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=False
)

# Basisklasse für Modelle
Base = declarative_base()

# SessionLocal für DB-Operationen
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# main.py — AVO Logistics Dispo AI (modulare Version)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os

# ======================================
# DATABASE
# ======================================
from app.database import Base, engine
from app.models import *  # Driver, Order, ImportedOrder, User

# ======================================
# ROUTES
# ======================================
from app.routes.dashboard import router as dashboard_router
from app.routes.drivers import router as drivers_router
from app.routes.orders import router as orders_router
from app.routes.import_center import router as import_router
from app.auth.auth_router import router as auth_router


# ======================================
# APP INITIALISIEREN
# ======================================
app = FastAPI(title="AVO Logistics Dispo AI")

# --- CORS erlauben (wichtig für App später) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # später beschränken wir das
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Static & Templates ---
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- DB Tabellen generieren ---
Base.metadata.create_all(bind=engine)


# ======================================
# ROUTER REGISTRIEREN
# ======================================
app.include_router(dashboard_router)
app.include_router(drivers_router)
app.include_router(orders_router)
app.include_router(import_router)
app.include_router(auth_router)


# ======================================
# STATUS ROUTE
# ======================================
@app.get("/status")
async def status():
    return {"message": "AVO Logistics Dispo AI läuft"}


# ======================================
# DEV SERVER STARTEN
# ======================================
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

if __name__ == "__main__":
    import uvicorn
    print("Starting AVO Dispo AI on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)

fimport os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Database & Models
from app.database import Base, engine
from app.models import Driver, Order, ImportedOrder, User

# Routers
from app.auth.auth_router import router as auth_router
from app.routes.import_center import router as import_router
from app.routes.orders import router as orders_router
from app.routes.drivers import router as drivers_router
from app.routes.dashboard import router as dashboard_router

# ---------------------------------------------------------
# INITIALISIERUNG
# ---------------------------------------------------------

app = FastAPI(title="AVO Logistics Dispo AI")

# Datenbanktabellen erzeugen (falls nicht vorhanden)
Base.metadata.create_all(bind=engine)

# Basisverzeichnis korrekt bestimmen
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Static Files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


# ---------------------------------------------------------
# CORS – für spätere Fahrer-App wichtig
# ---------------------------------------------------------

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROUTER REGISTRIEREN
# ---------------------------------------------------------

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(import_router, prefix="/import", tags=["Import Center"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(drivers_router, prefix="/drivers", tags=["Drivers"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])


# ---------------------------------------------------------
# ROOT ENDPOINT (Optional)
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"message": "AVO Logistics Dispo AI – Backend läuft erfolgreich."}

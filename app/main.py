# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, upload,  report
import logging
from api.routes import user

# Configura logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ClockPilot API", version="1.0")

@app.get("/")
async def root():
    return {"message": "Bienvenido a ClockPilot API"}

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Registra routers con logging
routers = [
    (auth.router, "/api/auth"),
    (upload.router, "/api/upload"),
    (report.router, "/api/reports"),
    (user.router, "/api") 
]

for router_obj, prefix in routers:
    app.include_router(router_obj, prefix=prefix)
    logger.info(f"Registrado router en {prefix}")

# Log todas las rutas al iniciar
@app.on_event("startup")
async def startup_event():
    for route in app.routes:
        if hasattr(route, "path"):
            logger.info(f"Ruta registrada: {route.path}")
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from api.sintomasAPI import router as sintomas_router
import os

app = FastAPI(title="Dra. Cortex AI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(BASE_DIR, "api", "frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

print("FRONTEND:", FRONTEND_DIR)
print("STATIC:", STATIC_DIR)

# Arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Página inicial
@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# API
app.include_router(sintomas_router, prefix="/sintomas")

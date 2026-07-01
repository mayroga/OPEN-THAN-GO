from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI(title="OPEN THAN GO CORE")

# Directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =========================
# CARGA DE DATOS (DINÁMICA)
# =========================
def load_all_missions():
    """Busca todos los archivos missions_*.json y los une en una sola lista."""
    all_missions = []
    
    # Busca archivos que empiecen con 'missions_' y terminen en '.json'
    files = sorted([f for f in os.listdir(BASE_DIR) if f.startswith("missions_") and f.endswith(".json")])
    
    for file in files:
        path = os.path.join(BASE_DIR, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Extrae la lista de misiones
                missions = data.get("missions", [])
                all_missions.extend(missions)
        except Exception as e:
            print(f"Error cargando {file}: {e}")
            continue
            
    # Ordena por ID
    all_missions = sorted(all_missions, key=lambda x: x.get("id", 0))
    return {"missions": all_missions}

# =========================
# ROUTES
# =========================

@app.get("/")
async def home():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

@app.get("/api/missions")
async def get_missions():
    """Endpoint para que engine.js obtenga todas las misiones."""
    return load_all_missions()

@app.get("/api/health")
async def health():
    return {"status": "ok", "engine": "active"}

# =========================
# RUN
# =========================
if __name__ == "__main__":
    import uvicorn
    # reload=True es ideal para desarrollo
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

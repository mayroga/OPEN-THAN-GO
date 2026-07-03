import json
import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carga de base de conocimiento (Los 3 bloques de 7 misiones)
def get_mission_bank():
    # El sistema carga los 3 archivos para tener acceso al set completo de 21 misiones
    bank = []
    for f in ["missions_01_07.json", "missions_08_14.json", "missions_15_21.json"]:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                bank.extend(data["missions"])
        except: continue
    return bank

@app.get("/")
def read_root():
    return FileResponse("static/session.html")

@app.post("/api/open-than-go")
async def process_intervention(request: Request):
    data = await request.json()
    
    # 1. DIAGNÓSTICO INVISIBLE
    desahogo = data.get("desahogo", "").lower()
    presupuesto = data.get("budget", "cero")
    
    # Mapeo de perfilamiento
    perfil = "bien" # default
    if any(word in desahogo for word in ["dinero", "deuda", "pago", "biles"]):
        perfil = "mal"
    elif any(word in desahogo for word in ["hijos", "niños", "jugar"]):
        perfil = "nino"
    elif any(word in desahogo for word in ["cansado", "trabajo", "agobio"]):
        perfil = "mal"

    # 2. SELECCIÓN TERAPÉUTICA (El algoritmo de azar inteligente)
    bank = get_mission_bank()
    # Filtramos por perfil y presupuesto
    opciones = [m for m in bank if m.get("cat") == perfil]
    if not opciones: opciones = bank # Fallback de seguridad
    
    mision_final = random.choice(opciones)
    
    # 3. RESPUESTA DEFINITIVA (Sin rodeos, sin términos médicos)
    return JSONResponse({
        "status": "success",
        "mision": mision_final,
        "metadata": {
            "perfil_detectado": perfil,
            "objetivo": "equilibrio_biopsicosocial"
        }
    })

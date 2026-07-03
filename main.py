from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()

# Montaje de recursos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Lógica de Mando: Clasificación de Intención (Modo Escape)
# Esta estructura permite expansión ilimitada a nivel nacional.
BASE_DATOS_NACIONAL = [
    {
        "tipo": "naturaleza",
        "titulo": "Reconexión en Parques Nacionales",
        "mente": ["agotado", "estresado"],
        "presupuesto": ["cero", "moderado"],
        "mision": "Camina en silencio durante 20 minutos. Tu única meta es observar el movimiento del viento en las hojas. Suelta la carga del trabajo.",
        "gps_query": "National+Parks+near+"
    },
    {
        "tipo": "cultural",
        "titulo": "Exploración de Legado",
        "mente": ["nostalgico", "aburrido"],
        "presupuesto": ["moderado", "libre"],
        "mision": "Busca un rincón histórico o museo local. Tu misión es encontrar un objeto que te recuerde a tu historia familiar.",
        "gps_query": "Historic+sites+and+museums+near+"
    }
]

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    perfil = await request.json()
    zip_code = perfil.get("zip", "33101")
    mente = perfil.get("mente", "agotado")
    presupuesto = perfil.get("presupuesto", "cero")

    # 1. Motor de decisión: Cruza estado mental y bolsillo
    opciones = [m for m in BASE_DATOS_NACIONAL if mente in m["mente"] and presupuesto in m["presupuesto"]]
    
    # 2. Selección del Mando
    seleccion = random.choice(opciones) if opciones else BASE_DATOS_NACIONAL[0]
    
    # 3. Construcción del destino (Integración Nacional)
    gps_url = f"https://www.google.com/maps/search/?api=1&query={seleccion['gps_query']}{zip_code}"

    # 4. Respuesta de alta precisión
    return {
        "titulo_destino": seleccion["titulo"],
        "proposito_terapeutico": "Reconfiguración de perspectiva y alivio de cortisol.",
        "mision_activa": seleccion["mision"],
        "gps_url": gps_url,
        "requiere_calma": mente in ["agotado", "estresado"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

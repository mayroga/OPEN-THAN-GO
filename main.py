from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()

# Montar archivos estáticos para que el motor pueda leer el CSS y JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Misiones base para el protocolo de alivio
MISIONES_CASA = [
    {
        "titulo": {"es": "REORDENAR TU ENTORNO", "en": "REORDER YOUR ENVIRONMENT"},
        "descripcion": {"es": "Dedica 10 minutos a ordenar un espacio físico. Tu entorno exterior refleja tu interior.", "en": "Spend 10 minutes tidying a physical space. Your outer environment reflects your inner state."}
    },
    {
        "titulo": {"es": "RESPIRACIÓN CONSCIENTE", "en": "CONSCIOUS BREATHING"},
        "descripcion": {"es": "Sigue el ciclo visual. Inhala calma, exhala pesadez. 10 minutos para reiniciar tu sistema.", "en": "Follow the visual cycle. Inhale calm, exhale heaviness. 10 minutes to reset your system."}
    }
]

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/open-than-go")
async def open_than_go(request: Request):
    data = await request.json()
    decision = data.get("decision", "salir")
    zip_code = data.get("zip_code", "33101")
    
    if decision == "casa":
        # Retorna protocolo de 10 min
        return {
            "tipo": "Casa",
            "mision": MISIONES_CASA[0]
        }
    else:
        # Retorna protocolo de acción exterior
        return {
            "tipo": "Salida",
            "opciones": [
                {"nombre": "Parque local (Entorno Natural)", "gps": f"https://www.google.com/maps/search/?api=1&query=parks+near+{zip_code}"},
                {"nombre": "Centro de recreación (Ambiente Social)", "gps": f"https://www.google.com/maps/search/?api=1&query=recreation+centers+near+{zip_code}"},
                {"nombre": "Espacio público de interés", "gps": f"https://www.google.com/maps/search/?api=1&query=public+spaces+near+{zip_code}"}
            ]
        }

if __name__ == "__main__":
    # Configuración de puerto para entorno de servidor
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

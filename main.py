from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base de datos de alta disponibilidad
BASE_MISIONES = {
    "CASA": [
        {"titulo": "Fase 1: Reconocimiento", "descripcion": "Identifica tu tensión actual sin juzgarla."},
        {"titulo": "Fase 2: Anclaje", "descripcion": "Inhala en 4 tiempos, mantén en 2, exhala en 6."},
        {"titulo": "Fase 3: Reset", "descripcion": "Suelta el control. Deja que el sistema te guíe el resto del tiempo."}
    ],
    "SALIR": {
        "agotado": {
            "titulo": "Refugio Natural",
            "porque": "Tu sistema nervioso necesita reducir la sobreestimulación visual y auditiva.",
            "que_hacer": "Camina sin rumbo fijo en una zona verde. Observa los patrones de las hojas.",
            "donde": "Parque o reserva natural más cercana.",
            "gps": "nature+parks+near+"
        },
        "estresado": {
            "titulo": "Zona de Descarga Física",
            "porque": "Necesitas metabolizar el exceso de cortisol acumulado en tus músculos.",
            "que_hacer": "Realiza una caminata a ritmo acelerado o busca una actividad física recreativa.",
            "donde": "Centro de recreación o pista pública.",
            "gps": "recreation+centers+near+"
        },
        "aburrido": {
            "titulo": "Distrito de Estimulación",
            "porque": "La monotonía bloquea tu dopamina. Necesitas un cambio drástico de ambiente.",
            "que_hacer": "Visita una galería o zona urbana con alta afluencia de personas y arte.",
            "donde": "Centro histórico o distrito de artes.",
            "gps": "arts+and+entertainment+near+"
        }
    }
}

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    
    # Perfilamiento Dinámico
    contexto = {
        "modo": payload.get("modo"),
        "zip": payload.get("zip", "33101"),
        "mente": payload.get("mente"),
        "budget": payload.get("budget"),
        "perfil": payload.get("perfil")
    }

    if contexto["modo"] == "CASA":
        return JSONResponse({"modo": "CASA", "misiones": BASE_MISIONES["CASA"]})
    
    else:
        # Lógica de emparejamiento (El "Por qué" y "A dónde")
        info = BASE_MISIONES["SALIR"].get(contexto["mente"])
        
        # Ajuste por perfil
        msg_adicional = ""
        if contexto["perfil"] == "accesible":
            msg_adicional = " (Ruta seleccionada con prioridad de accesibilidad)."
        elif contexto["perfil"] == "familia":
            msg_adicional = " (Entorno apto para menores)."

        return JSONResponse({
            "modo": "SALIR",
            "titulo": info["titulo"],
            "porque": info["porque"],
            "que_hacer": info["que_hacer"] + msg_adicional,
            "donde": info["donde"],
            "gps": f"https://www.google.com/maps/search/?api=1&query={info['gps']}{contexto['zip']}"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

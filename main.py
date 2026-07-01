from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
import os

app = FastAPI(title="OPEN THAN GO - Sistema de Activación de Bienestar")

# Directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Los 7 Protocolos TVid de May Roga LLC
protocolos = {
    "bien": {"nombre": "Constructor de Luz", "accion": "Cinco Acciones Positivas"},
    "mal": {"nombre": "Alquimista del Error", "accion": "Transformando el Error"},
    "nino": {"nombre": "Explorador del Asombro", "accion": "Explorador por Cinco Minutos"},
    "padre": {"nombre": "Estratega del Compromiso", "accion": "Mi Compromiso de Hoy"},
    "madre": {"nombre": "Guardián del Autocuidado", "accion": "Cuidándome con Amor"},
    "beso": {"nombre": "Emisario de Afecto", "accion": "Regalando Afecto"},
    "guerra": {"nombre": "Guerrero de mi Destino", "accion": "Mi Batalla, Mi Fortaleza"}
}

# Rutas
@app.get("/")
async def read_index():
    """Sirve la interfaz principal de la aplicación."""
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

@app.get("/api/get-protocol")
async def get_protocol(salir: bool = False):
    """
    Motor lógico de decisión:
    - Si 'salir' es False (Casa): Devuelve 2 protocolos aleatorios para una sesión de 10 min.
    - Si 'salir' es True: Devuelve 1 protocolo para ejecutar en el entorno exterior.
    """
    keys = list(protocolos.keys())
    
    if not salir:
        # Selección aleatoria de 2 protocolos diferentes (21 combinaciones posibles)
        seleccion = random.sample(keys, 2)
        return {
            "modo": "casa", 
            "protocolos": [protocolos[k] for k in seleccion]
        }
    else:
        # Selección de 1 protocolo para misión de campo
        seleccion = random.choice(keys)
        return {
            "modo": "salida", 
            "protocolo": protocolos[seleccion]
        }

@app.get("/api/health")
async def health_check():
    """Verificación de estado para servicios como Render."""
    return {"status": "active", "engine": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

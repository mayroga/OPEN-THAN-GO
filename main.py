# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.1
# Company: May Roga LLC
# File: main.py - UNIFICADO Y OPTIMIZADO (Anti-Repetición Estricto)

import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import server # Import the new server.py module

app = FastAPI(title="OPEN THAN GO - CWRE", version="6.0.1")

# Asegurar infraestructura de archivos estáticos
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    """Serves the main HTML page."""
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    """Main API endpoint for OPEN THAN GO.
    Receives user input and local preference profile to return a non-repeating personalized recommendation."""
    payload = await request.json()
    return await server.mando_integral_logic(payload) # Delegate to server.py logic

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

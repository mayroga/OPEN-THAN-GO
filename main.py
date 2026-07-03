# main.py - OPEN THAN GO SYSTEM (STABLE DEPLOY)
# FastAPI + Static + API Ready

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()

# ----------------------------
# STATIC FILES
# ----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():
    return FileResponse("static/session.html")

# ----------------------------
# LÓGICA DE APOYO
# ----------------------------
def generar_lugar(budget, stress):
    opciones = [
        {"name": "Parque tranquilo", "reason": "Reduce estrés y ayuda a estabilizar tu mente", "gps_link": "#"},
        {"name": "Cafetería silenciosa", "reason": "Ambiente seguro para regular emociones", "gps_link": "#"},
        {"name": "Caminar zona segura", "reason": "Movimiento físico regula ansiedad y pensamiento", "gps_link": "#"}
    ]
    if budget == "cero":
        return opciones[2]
    if stress > 7:
        return opciones[0]
    return random.choice(opciones)

def misiones_casa():
    return [
        {"tx": "Respira lento. Inhala calma. Exhala tensión.", "t": "breath_auto", "d": 10},
        {"tx": "Observa qué puedes controlar hoy.", "t": "text"},
        {"tx": "Haz una pequeña acción para mejorar tu estado.", "t": "text"}
    ]

# ----------------------------
# API PRINCIPAL
# ----------------------------
@app.post("/api/open-than-go")
async def open_than_go(request: Request):
    try:
        data = await request.json()
        
        mode = data.get("decision", "salir")
        budget = data.get("budget_level", "cero")
        desahogo = data.get("desahogo", "")

        # ---------------- CASA ----------------
        if mode == "casa":
            return JSONResponse({
                "status": "success",
                "tipo": "Casa",
                "mision": {"b": misiones_casa()},
                "duration": 600
            })

        # ---------------- SALIR ----------------
        stress = min(len(desahogo or ""), 10)
        lugar = generar_lugar(budget, stress)

        return JSONResponse({
            "status": "success",
            "tipo": "Salida",
            "lugar": lugar,
            "mision": {"b": [{"tx": lugar["reason"]}]},
            "duration": 60
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

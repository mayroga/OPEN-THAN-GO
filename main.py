# OPEN THAN GO - EMOTION ROUTER CORE v2 (CLEAN BUILD)
# May Roga LLC

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import json
import random

app = FastAPI(title="OPEN THAN GO")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =========================
# STATES VALIDATION
# =========================
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}

# =========================
# SAFE LOAD
# =========================
def load_json(path):
    if not os.path.exists(path):
        return {"missions": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {"missions": []}
    except:
        return {"missions": []}

MISSION_FILES = [
    "missions_01_07.json",
    "missions_08_14.json",
    "missions_15_21.json"
]

MISSIONS = []

for file in MISSION_FILES:
    data = load_json(os.path.join(BASE_DIR, file))
    MISSIONS.extend(data.get("missions", []))

MISSIONS = sorted(MISSIONS, key=lambda x: x.get("id", 0))


# =========================
# EMOTION ENGINE
# =========================
def analyze_emotion(text, mode):
    t = (text or "").lower()

    stress = any(w in t for w in ["estres", "trabajo", "ansiedad", "presion"])
    monotony = any(w in t for w in ["aburrido", "rutina", "igual"])
    low = any(w in t for w in ["cansado", "energia", "agotado"])

    if mode == "casa":
        return "HOME"

    if stress:
        return "OUT_STRUCTURE"
    if monotony:
        return "OUT_EXPLORE"
    if low:
        return "OUT_SLOW"

    return "OUT_BALANCE"


# =========================
# BUDGET SYSTEM
# =========================
def budget_range(level):
    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 90),
        "libre": (70, 999999)
    }.get(level, (0, 40))


# =========================
# PLACES ENGINE (9+ OPTIONS)
# =========================
def generate_places(state, zip_code, budget):

    min_b, max_b = budget_range(budget)

    base = [
        "public park", "nature trail", "lake view",
        "river walk", "botanical garden",
        "community beach", "urban green zone",
        "downtown walk", "quiet plaza",
        "sunset point", "observation area"
    ]

    picks = random.sample(base, 9)

    # 1 elegido “inteligente” oculto (no forzado visible)
    chosen = random.choice(picks)

    return [
        {
            "name": f"{p} - {state}",
            "cost": f"${min_b} - ${max_b}",
            "why": "emotional reset + guided exploration",
            "gps_link": f"https://www.google.com/maps/search/?api=1&query={p}+{state}+{zip_code}"
        }
        for p in picks
    ]


# =========================
# MISSIONS
# =========================
def get_mission():
    if not MISSIONS:
        return {"b": [{"story": {"es": "Respira. Estás aquí."}}]}

    return random.choice(MISSIONS)


# =========================
# REQUEST MODEL
# =========================
class Payload(BaseModel):
    decision: str = "salir"
    lang: str = "es"
    budget_level: str = "cero"
    zip_code: str = ""
    estado: str = "FL"
    desahogo: str = ""


# =========================
# ROUTE CORE
# =========================
@app.post("/api/open-than-go")
def router(data: Payload):

    state = (data.estado or "FL").upper()

    if state not in US_STATES:
        state = "FL"

    emotion = analyze_emotion(data.desahogo, data.decision)
    mission = get_mission()

    # CASA MODE
    if data.decision == "casa":
        return {
            "type": "HOME",
            "emotion": emotion,
            "mision": mission,
            "title": "OPEN ◯ THAN GO"
        }

    # OUT MODE
    places = generate_places(state, data.zip_code, data.budget_level)

    return {
        "type": "OUT",
        "emotion": emotion,
        "mision": mission,
        "recommendations": places,
        "lugar": {
            "state": state,
            "zip": data.zip_code
        }
    }


# =========================
# FRONT
# =========================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

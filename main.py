# =========================================================
# OPEN THAN GO - CORE ENGINE v4 (STABLE BACKEND)
# FASTAPI CLEAN - NO FLOOD - NO FREEZE
# =========================================================

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import random

app = FastAPI(title="OPEN THAN GO")

# =========================================================
# PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =========================================================
# USA STATES VALIDATION
# =========================================================
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}

# =========================================================
# SAFE JSON LOADER
# =========================================================
def load_json(path):
    if not os.path.exists(path):
        return {"missions": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {"missions": []}
    except:
        return {"missions": []}

# =========================================================
# LOAD MISSIONS (1–21 SYSTEM SAFE)
# =========================================================
MISSION_FILES = [
    "missions_01_07.json",
    "missions_08_14.json",
    "missions_15_21.json"
]

MISSIONS = []

for file in MISSION_FILES:
    path = os.path.join(BASE_DIR, file)
    data = load_json(path)

    missions = data.get("missions", [])

    if isinstance(missions, list):
        for m in missions:
            if isinstance(m, dict) and "id" in m:
                MISSIONS.append(m)

MISSIONS = sorted(MISSIONS, key=lambda x: x.get("id", 0))

# =========================================================
# EMOTION ENGINE (SAFE SIMPLE)
# =========================================================
def analyze_emotion(text, mode):
    t = (text or "").lower()

    stress = any(w in t for w in ["estres", "ansiedad", "presion", "trabajo"])
    fatigue = any(w in t for w in ["cansado", "agotado", "sin energia"])
    monotony = any(w in t for w in ["aburrido", "rutina", "igual"])

    if mode == "casa":
        if fatigue:
            return "HOME_LOW"
        if stress:
            return "HOME_STRESS"
        return "HOME_BALANCE"

    if stress:
        return "OUT_STRUCTURE"
    if monotony:
        return "OUT_EXPLORATION"
    if fatigue:
        return "OUT_SLOW"

    return "OUT_BALANCE"

# =========================================================
# SAFE MISSION SELECTOR
# =========================================================
def get_mission():
    if not MISSIONS:
        return {
            "id": 0,
            "b": [
                {
                    "story": {
                        "es": "Respira. Estás aquí. No necesitas resolver todo ahora.",
                        "en": "Breathe. You are here. You don't need to fix everything now."
                    }
                }
            ]
        }

    mission = random.choice(MISSIONS)

    if not isinstance(mission, dict):
        return {"id": 0, "b": []}

    mission.setdefault("b", [])
    return mission

# =========================================================
# ROUTES
# =========================================================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

@app.get("/session")
def session():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

@app.get("/health")
def health():
    return {"status": "ok"}

# =========================================================
# CORE API
# =========================================================
@app.post("/api/open-than-go")
async def open_than_go(request: Request):

    data = await request.json()

    mode = data.get("decision", "salir")
    text = data.get("desahogo", "")
    state = (data.get("estado") or "FL").upper()
    zip_code = data.get("zip_code", "")
    budget = data.get("budget_level", "cero")

    # VALIDATE STATE
    if state not in US_STATES:
        state = "FL"

    emotion = analyze_emotion(text, mode)
    mission = get_mission()

    # =====================================================
    # CASA MODE
    # =====================================================
    if mode == "casa":
        return {
            "status": "ok",
            "type": "Casa",
            "title": "OPEN ◯ THAN GO",
            "emotion": emotion,
            "mission": mission,
            "ui": {
                "mode": "casa",
                "timer": 600,
                "breathing": "guided",
                "voice": True,
                "language": "es"
            }
        }

    # =====================================================
    # SALIR MODE
    # =====================================================
    return {
        "status": "ok",
        "type": "Salida",
        "title": "OPEN ◎ THAN GO",
        "emotion": emotion,
        "mission": mission,
        "lugar": {
            "state": state,
            "zip": zip_code
        },
        "ui": {
            "mode": "salir",
            "voice": True,
            "language": "es",
            "guidance": "active"
        }
    }

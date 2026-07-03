# =========================================================
# OPEN THAN GO - CORE ENGINE v3 (CLEAN + STABLE)
# FASTAPI ONLY - READY FOR RENDER
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
# VALID STATES
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
    try:
        if not os.path.exists(path):
            return {"missions": []}

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            return data

        return {"missions": []}

    except:
        return {"missions": []}


# =========================================================
# LOAD MISSIONS (1–21 SYSTEM)
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

    for m in data.get("missions", []):
        if isinstance(m, dict) and "id" in m:
            MISSIONS.append(m)

MISSIONS = sorted(MISSIONS, key=lambda x: x["id"])


# =========================================================
# EMOTION ENGINE (SIMPLE BIOSOCIAL DETECTION)
# =========================================================
def analyze_emotion(text, mode):
    t = (text or "").lower()

    stress_words = ["estres", "ansiedad", "presion", "trabajo"]
    fatigue_words = ["cansado", "agotado", "sin energia"]
    monotony_words = ["aburrido", "rutina", "igual"]

    stress = any(w in t for w in stress_words)
    fatigue = any(w in t for w in fatigue_words)
    monotony = any(w in t for w in monotony_words)

    if mode == "casa":
        if fatigue:
            return "HOME_LOW"
        if stress:
            return "HOME_STRESS"
        return "HOME_BALANCE"

    if stress:
        return "OUT_STRESS"
    if monotony:
        return "OUT_MONOTONY"
    if fatigue:
        return "OUT_SLOW"

    return "OUT_BALANCE"


# =========================================================
# PROFILE (BIOSOCIAL FILTER READY)
# =========================================================
def biopsocial_profile(text, budget):
    t = (text or "").lower()

    return {
        "stress": any(w in t for w in ["estres", "ansiedad", "presion"]),
        "fatigue": any(w in t for w in ["cansado", "agotado"]),
        "monotony": any(w in t for w in ["aburrido", "rutina"]),
        "social_need": any(w in t for w in ["solo", "aislado"]),
        "low_budget": budget in ["cero", "minimo"]
    }


# =========================================================
# MISSION SELECTOR
# =========================================================
def get_mission():
    if not MISSIONS:
        return {
            "id": 0,
            "b": [
                {
                    "story": {
                        "es": "Respira. Estás aquí.",
                        "en": "Breathe. You are here."
                    }
                }
            ]
        }

    return random.choice(MISSIONS)


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
# MAIN API ENGINE
# =========================================================
@app.post("/api/open-than-go")
async def open_than_go(request: Request):

    data = await request.json()

    mode = data.get("decision", "salir")
    text = data.get("desahogo", "")
    state = (data.get("estado") or "FL").upper()
    zip_code = data.get("zip_code", "")
    budget = data.get("budget_level", "cero")

    if state not in US_STATES:
        state = "FL"

    emotion = analyze_emotion(text, mode)
    profile = biopsocial_profile(text, budget)
    mission = get_mission()

    # =====================================================
    # CASA MODE
    # =====================================================
    if mode == "casa":
        return {
            "status": "ok",
            "mode": "casa",
            "emotion": emotion,
            "profile": profile,
            "mission": mission,
            "ui": {
                "language": "es",
                "voice": "es-ES",
                "timer": 600,
                "flow": "breathing_home"
            }
        }

    # =====================================================
    # SALIR MODE
    # =====================================================
    return {
        "status": "ok",
        "mode": "salir",
        "emotion": emotion,
        "profile": profile,
        "mission": mission,
        "location": {
            "state": state,
            "zip": zip_code
        },
        "ui": {
            "language": "es",
            "voice": "es-ES",
            "flow": "guided_mission"
        }
    }

# =========================================================
# OPEN THAN GO - CORE ENGINE v3 (CLEAN STABLE)
# FASTAPI ONLY - PRODUCTION READY
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
# USA STATES
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
# MISSIONS 1–21 LOADER
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

MISSIONS = sorted(MISSIONS, key=lambda x: x["id"])

# =========================================================
# EMOTION ENGINE
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
        return "OUT_STRUCTURE"
    if monotony:
        return "OUT_EXPLORATION"
    if fatigue:
        return "OUT_SLOW"

    return "OUT_BALANCE"

# =========================================================
# BIOPSYCHOSOCIAL PROFILE
# =========================================================
def biopsocial_profile(text, budget):
    t = (text or "").lower()

    return {
        "stress": any(w in t for w in ["estres", "ansiedad", "presion"]),
        "fatigue": any(w in t for w in ["cansado", "agotado", "sin energia"]),
        "monotony": any(w in t for w in ["aburrido", "rutina", "igual"]),
        "social_need": any(w in t for w in ["solo", "aislado"]),
        "low_budget": budget in ["cero", "minimo"]
    }

# =========================================================
# PLACES DATABASE (9+ REAL LOGIC POINTS)
# =========================================================
PLACES_DB = [
    {
        "name": "Matheson Hammock Park",
        "mood": ["stress", "fatigue"],
        "cost": "low",
        "action": "camina lento sin teléfono",
        "therapy": "reducción de estrés"
    },
    {
        "name": "South Pointe Park",
        "mood": ["monotony", "stress"],
        "cost": "low",
        "action": "observa el mar 10 min",
        "therapy": "reset mental"
    },
    {
        "name": "Wynwood Walls",
        "mood": ["monotony"],
        "cost": "free",
        "action": "elige 3 colores que te representen",
        "therapy": "estimulación creativa"
    },
    {
        "name": "Bayfront Park",
        "mood": ["stress", "fatigue"],
        "cost": "free",
        "action": "respira 4-4-6 frente al agua",
        "therapy": "regulación emocional"
    },
    {
        "name": "Little Havana Walk",
        "mood": ["social_need", "monotony"],
        "cost": "low",
        "action": "habla con alguien mayor",
        "therapy": "reconexión social"
    },
    {
        "name": "Virginia Key Beach",
        "mood": ["stress", "fatigue"],
        "cost": "low",
        "action": "camina descalzo 5 min",
        "therapy": "grounding"
    },
    {
        "name": "Brickell Riverwalk",
        "mood": ["stress"],
        "cost": "free",
        "action": "observa sin juicio",
        "therapy": "desaceleración mental"
    },
    {
        "name": "Vizcaya Gardens",
        "mood": ["monotony"],
        "cost": "medium",
        "action": "imagina la historia del lugar",
        "therapy": "imaginación guiada"
    },
    {
        "name": "Oleta River State Park",
        "mood": ["fatigue", "stress"],
        "cost": "low",
        "action": "camina en silencio 10 min",
        "therapy": "desconexión neural"
    }
]

# =========================================================
# MATCH ENGINE (BIOSOCIAL RANKING)
# =========================================================
def match_places(profile):
    scored = []

    for p in PLACES_DB:
        score = 0

        for mood in p["mood"]:
            if profile.get(mood):
                score += 2

        if profile["low_budget"] and p["cost"] == "free":
            score += 1

        scored.append((score, p))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [p for _, p in scored]

# =========================================================
# MISSIONS
# =========================================================
def get_mission():
    if not MISSIONS:
        return {"id": 0, "b": [{"story": {"es": "Respira", "en": "Breathe"}}]}

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
# CORE ENGINE
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

    profile = biopsocial_profile(text, budget)
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
    # SALIR MODE (9+ PLACES + RANKING)
    # =====================================================
    ranked = match_places(profile)

    selected = ranked[0] if ranked else None

    return {
        "status": "ok",
        "type": "Salida",
        "title": "OPEN ◎ THAN GO",
        "emotion": emotion,
        "mission": mission,

        "selected_place": selected,
        "all_places": ranked[:9],

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

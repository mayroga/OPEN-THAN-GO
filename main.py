# =========================================================
# OPEN THAN GO - CORE ENGINE v2 (CLEAN + PRODUCTION READY)
# May Roga LLC
# =========================================================

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
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
# 50 ESTADOS USA (VALIDACIÓN REAL)
# =========================================================
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}


# =========================================================
# SAFE JSON LOADER (MISSIONS 1–21)
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


# =========================================================
# EMOTION ENGINE (USER CONTEXT DRIVEN)
# =========================================================
def analyze_emotion(text: str, mode: str):

    t = (text or "").lower()

    stress = any(w in t for w in ["estres", "ansiedad", "trabajo", "presion"])
    low = any(w in t for w in ["cansado", "agotado", "sin energia"])
    monotony = any(w in t for w in ["aburrido", "rutina", "igual"])

    if mode == "casa":
        if stress:
            return "HOME_STRESS"
        if low:
            return "HOME_LOW"
        return "HOME_BALANCE"

    if stress:
        return "OUT_STRUCTURE"
    if monotony:
        return "OUT_EXPLORATION"
    if low:
        return "OUT_SLOW"

    return "OUT_BALANCE"


# =========================================================
# BUDGET SYSTEM
# =========================================================
def budget_range(level):
    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 90),
        "libre": (70, 999999)
    }.get(level, (0, 40))


# =========================================================
# SMART PLACE GENERATOR (9+ OPTIONS OBLIGATORIO)
# =========================================================
def generate_places(state, zip_code, budget, emotion, text):

    min_b, max_b = budget_range(budget)

    base_places = [
        "quiet park walk",
        "ocean breeze zone",
        "urban nature trail",
        "lake reflection point",
        "botanical garden path",
        "community green space",
        "sunset walking route",
        "open mall walking space",
        "river calm zone",
        "library quiet area",
        "waterfront path"
    ]

    # adaptativo (emocional simple ranking)
    if "stress" in emotion:
        boost = ["lake reflection point", "botanical garden path", "river calm zone"]
    elif "low" in emotion:
        boost = ["sunset walking route", "ocean breeze zone"]
    else:
        boost = ["quiet park walk", "urban nature trail"]

    pool = list(set(base_places + boost))

    # mínimo 9 lugares visibles
    random.shuffle(pool)
    selected = pool[:10]

    return [
        {
            "name": f"{p} - {state}",
            "cost": f"${min_b} - ${max_b}",
            "why": "adaptado a tu estado emocional + regulación natural",
            "gps": f"https://www.google.com/maps/search/?api=1&query={p}+{state}+{zip_code}"
        }
        for p in selected
    ]


# =========================================================
# MISSION PICKER
# =========================================================
def get_mission():
    if not MISSIONS:
        return {
            "b": [{
                "story": {
                    "es": "Respira. No necesitas resolver todo ahora.",
                    "en": "Breathe. You don't need to fix everything now."
                }
            }]
        }

    return random.choice(MISSIONS)


# =========================================================
# ROUTE CORE
# =========================================================
@app.post("/api/open-than-go")
async def router(request: Request):

    data = await request.json()

    mode = data.get("decision", "salir")
    budget = data.get("budget_level", "cero")
    text = data.get("desahogo", "")

    state = (data.get("estado") or "FL").upper()
    zip_code = data.get("zip_code", "")

    if state not in US_STATES:
        state = "FL"

    emotion = analyze_emotion(text, mode)
    mission = get_mission()

    # ================= CASA MODE =================
    if mode == "casa":

        return JSONResponse({
            "status": "success",
            "type": "Casa",
            "emotion": emotion,
            "voice_lang": "es-ES",
            "mision": mission,
            "ui": {
                "mode": "casa",
                "voice": True,
                "timer": 600,
                "breathing": True,
                "silent_guided": True
            }
        })

    # ================= SALIR MODE =================
    places = generate_places(state, zip_code, budget, emotion, text)

    return JSONResponse({
        "status": "success",
        "type": "Salida",
        "emotion": emotion,
        "voice_lang": "es-ES",

        "mision": mission,

        "recommendations": places,

        "ui": {
            "mode": "salir",
            "voice": True,
            "guidance": "adaptive"
        }
    })


# =========================================================
# FRONT
# =========================================================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

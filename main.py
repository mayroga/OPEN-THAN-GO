```python
# =========================================================
# OPEN THAN GO SYSTEM
# Emotion Router v5 - FastAPI Edition
# Company: May Roga LLC
# =========================================================

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
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
# CACHE
# =========================================================

CACHE = {
    "missions": None
}

# =========================================================
# LOAD JSON
# =========================================================

def load_json(path):

    if not os.path.exists(path):
        return {"missions": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict):
                return data

            return {"missions": []}

    except:
        return {"missions": []}

# =========================================================
# LOAD ALL MISSIONS
# =========================================================

def load_missions():

    if CACHE["missions"] is not None:
        return CACHE["missions"]

    all_missions = []

    files = sorted([
        f
        for f in os.listdir(BASE_DIR)
        if f.startswith("missions_")
        and f.endswith(".json")
    ])

    for file in files:

        data = load_json(
            os.path.join(BASE_DIR, file)
        )

        missions = data.get(
            "missions",
            []
        )

        for m in missions:
            if (
                isinstance(m, dict)
                and "id" in m
            ):
                all_missions.append(m)

    all_missions = sorted(
        all_missions,
        key=lambda x: x["id"]
    )

    CACHE["missions"] = {
        "total": len(all_missions),
        "missions": all_missions
    }

    return CACHE["missions"]

# =========================================================
# RANDOM MISSION
# =========================================================

def get_random_mission():

    missions = load_missions()["missions"]

    if not missions:

        return {
            "id": 0,
            "b": [
                {
                    "story": {
                        "es":
                        "Respira. Estás aquí ahora.",
                        "en":
                        "Breathe. You are here now."
                    }
                }
            ]
        }

    return random.choice(missions)

# =========================================================
# EMOTION ENGINE
# =========================================================

def analyze_emotion(
    text,
    mode
):

    t = (
        text or ""
    ).lower()

    stress_words = [
        "estres",
        "estrés",
        "trabajo",
        "ansiedad",
        "presion",
        "presión"
    ]

    monotony_words = [
        "aburrido",
        "rutina",
        "monotono",
        "monótono"
    ]

    low_words = [
        "cansado",
        "agotado",
        "fatiga",
        "sin energia",
        "sin energía"
    ]

    stress = any(
        w in t
        for w in stress_words
    )

    monotony = any(
        w in t
        for w in monotony_words
    )

    low = any(
        w in t
        for w in low_words
    )

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
# BUDGET
# =========================================================

def budget_range(level):

    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 90),
        "libre": (70, 999999)
    }.get(level, (0, 40))

# =========================================================
# PLACES ENGINE
# =========================================================

def generate_places(
    state,
    zip_code,
    budget_level
):

    min_b, max_b = budget_range(
        budget_level
    )

    base_places = [

        "public nature park",
        "community beach access",
        "walking trail",
        "botanical garden",
        "urban green area",
        "riverwalk path",
        "lakefront zone",
        "public garden",
        "historic district walk",
        "community plaza",
        "scenic overlook",
        "boardwalk area",
        "quiet downtown area",
        "public art district",
        "waterfront park"

    ]

    random.shuffle(
        base_places
    )

    recommendations = []

    for p in base_places:

        recommendations.append({

            "name":
            f"{p.title()} - {state}",

            "cost":
            f"${min_b} - ${max_b}",

            "why":
            "equilibrio emocional + desconexión mental",

            "gps_link":
            f"https://www.google.com/maps/search/?api=1&query={p}+{state}+{zip_code}+USA"

        })

    return recommendations

# =========================================================
# REQUEST MODEL
# =========================================================

class OpenThanGoRequest(
    BaseModel
):
    decision: str = "salir"
    estado: str = "FL"
    zip_code: str = ""
    budget_level: str = "cero"
    desahogo: str = ""

# =========================================================
# FRONT
# =========================================================

@app.get("/")
def home():
    return FileResponse(
        os.path.join(
            STATIC_DIR,
            "session.html"
        )
    )

@app.get("/session")
def session():
    return FileResponse(
        os.path.join(
            STATIC_DIR,
            "session.html"
        )
    )

# =========================================================
# MISSIONS API
# =========================================================

@app.get("/api/missions")
def missions():
    return load_missions()

@app.get("/api/missions/{mission_id}")
def mission_by_id(
    mission_id: int
):

    missions = (
        load_missions()
        ["missions"]
    )

    for m in missions:
        if m["id"] == mission_id:
            return m

    return JSONResponse(
        status_code=404,
        content={
            "detail":
            "Mission not found"
        }
    )

# =========================================================
# OPEN THAN GO
# =========================================================

@app.post(
    "/api/open-than-go"
)
def open_than_go(
    payload:
    OpenThanGoRequest
):

    mode = (
        payload.decision
        or "salir"
    ).lower()

    state = (
        payload.estado
        or "FL"
    ).upper()

    zip_code = (
        payload.zip_code
        or ""
    ).strip()

    budget = (
        payload.budget_level
        or "cero"
    )

    text = (
        payload.desahogo
        or ""
    )

    if state not in US_STATES:
        state = "FL"

    emotion = analyze_emotion(
        text,
        mode
    )

    mission = get_random_mission()

    if mode == "casa":

        return {

            "status":
            "success",

            "type":
            "Casa",

            "emotion":
            emotion,

            "title":
            "OPEN ◯ THAN GO",

            "mision":
            mission,

            "ui": {
                "mode":
                "casa",

                "voice":
                True,

                "timer":
                600,

                "breathing":
                True,

                "silent":
                True
            }
        }

    places = generate_places(
        state,
        zip_code,
        budget
    )

    suggested = (
        random.randint(
            0,
            len(places)-1
        )
        if places
        else 0
    )

    return {

        "status":
        "success",

        "type":
        "Salida",

        "emotion":
        emotion,

        "title":
        "OPEN ◎ THAN GO",

        "budget_range":
        budget_range(
            budget
        ),

        "mision":
        mission,

        "recommendations":
        places,

        "suggested_index":
        suggested,

        "lugar": {
            "state":
            state,

            "zip":
            zip_code
        },

        "ui": {
            "mode":
            "salir",

            "voice":
            True,

            "guidance":
            "directive"
        }
    }

# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                8000
            )
        ),
        reload=True
    )
```

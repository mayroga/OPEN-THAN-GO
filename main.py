# OPEN THAN GO SYSTEM - EMOTION ROUTER v3.1 (BIOPSYCHOSOCIAL CORE FIXED)
# May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import random
import os
import json

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------
# 50 ESTADOS USA (VALIDACIÓN REAL)
# ----------------------------
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}

# ----------------------------
# SAFE JSON LOADER
# ----------------------------
def load_json(path):
    if not os.path.exists(path):
        return {"missions": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {"missions": []}
    except:
        return {"missions": []}

MISSIONS = [
    load_json(os.path.join(BASE_DIR, "missions_01_07.json")),
    load_json(os.path.join(BASE_DIR, "missions_08_14.json")),
    load_json(os.path.join(BASE_DIR, "missions_15_21.json"))
]

# ----------------------------
# EMOTION ENGINE (BIO SIGNAL v1)
# ----------------------------
def analyze_emotion(text, mode):
    t = (text or "").lower()

    stress_words = ["estres", "trabajo", "presion", "ansiedad", "biles"]
    monotony_words = ["aburrido", "rutina", "igual", "monotono"]
    low_words = ["cansado", "sin energia", "agotado", "fatiga"]

    stress = any(w in t for w in stress_words)
    monotony = any(w in t for w in monotony_words)
    low = any(w in t for w in low_words)

    # CASA MODE (regulación interna)
    if mode == "casa":
        if low:
            return "HOME_LOW"
        if stress:
            return "HOME_STRESS"
        return "HOME_BALANCE"

    # SALIR MODE (acción externa)
    if stress:
        return "OUT_STRUCTURE"
    if monotony:
        return "OUT_EXPLORATION"
    if low:
        return "OUT_SLOW"

    return "OUT_BALANCE"

# ----------------------------
# BUDGET SYSTEM (USA REALISTIC RANGE)
# ----------------------------
def budget_range(level):
    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 90),
        "libre": (70, 999999)
    }.get(level, (0, 40))

# ----------------------------
# GENERADOR DE LUGARES (NO TURÍSTICO GENÉRICO → CONTEXTO TERAPÉUTICO)
# ----------------------------
def generate_places(state, zip_code, budget_level):

    min_b, max_b = budget_range(budget_level)

    base_places = [
        "public nature park",
        "community beach access",
        "walking trail",
        "urban green zone",
        "lakefront area",
        "botanical garden",
        "riverwalk path",
        "quiet downtown zone"
    ]

    picks = random.sample(base_places, 3)

    return [
        {
            "name": f"{p} - {state}",
            "cost": f"${min_b} - ${max_b}",
            "why": "biopsychosocial reset + guided emotional reset",
            "gps_link": f"https://www.google.com/maps/search/?api=1&query={p}+{state}+{zip_code}+USA"
        }
        for p in picks
    ]

# ----------------------------
# MISSIONS ENGINE (FIX: CONSISTENTE + SAFE)
# ----------------------------
def get_mission():
    pool = random.choice(MISSIONS).get("missions", [])

    if not pool:
        return {
            "b": [
                {
                    "story": {
                        "es": "Respira. Estás aquí. No tienes que resolver todo ahora.",
                        "en": "Breathe. You are here. You don't need to fix everything now."
                    }
                }
            ]
        }

    return random.choice(pool)

# ----------------------------
# ROUTE API
# ----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def router():

    data = request.get_json(force=True) or {}

    mode = data.get("decision", "salir")
    budget = data.get("budget_level", "cero")
    text = data.get("desahogo", "")

    state = (data.get("estado") or "FL").upper()
    zip_code = (data.get("zip_code") or "").strip()

    # ----------------------------
    # VALIDACIÓN ESTADOS USA
    # ----------------------------
    if state not in US_STATES:
        state = "FL"

    emotion = analyze_emotion(text, mode)
    mission = get_mission()

    # ----------------------------
    # CASA FLOW (INTERVENCIÓN INTERNA)
    # ----------------------------
    if mode == "casa":
        return jsonify({
            "status": "success",
            "type": "Casa",
            "emotion": emotion,
            "title": "OPEN ◯ THAN GO",
            "mision": mission,
            "ui": {
                "mode": "casa",
                "breathing": "deep",
                "voice": True,
                "timer": 600
            }
        })

    # ----------------------------
    # SALIR FLOW (INTERVENCIÓN EXTERNA)
    # ----------------------------
    places = generate_places(state, zip_code, budget)

    return jsonify({
        "status": "success",
        "type": "Salida",
        "emotion": emotion,
        "title": "OPEN ◎ THAN GO",

        "budget_range": budget_range(budget),

        # FIX CRÍTICO: FRONTEND ESPERA ESTO
        "mision": mission,

        "recommendations": places,

        "lugar": {
            "state": state,
            "zip": zip_code
        },

        "ui": {
            "mode": "salir",
            "breathing": "light",
            "voice": True,
            "guidance": "directive"
        }
    })

# ----------------------------
# FRONTEND
# ----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")

# ----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

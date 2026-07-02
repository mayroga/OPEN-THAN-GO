# OPEN THAN GO SYSTEM - EMOTION ROUTER v2 (USA FULL)
# May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import random
import os
import json

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------
# 50 ESTADOS USA (FULL COVER)
# ----------------------------
US_STATES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
]

# ----------------------------
# LOAD MISSIONS
# ----------------------------
def load_json(path):
    if not os.path.exists(path):
        return {"missions": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

MISSIONS = [
    load_json(os.path.join(BASE_DIR, "missions_01_07.json")),
    load_json(os.path.join(BASE_DIR, "missions_08_14.json")),
    load_json(os.path.join(BASE_DIR, "missions_15_21.json"))
]

# ----------------------------
# EMOTION ENGINE (CORE)
# ----------------------------
def analyze_emotion(text, mode):
    t = (text or "").lower()

    stress = any(w in t for w in ["estres", "trabajo", "presion", "ansiedad"])
    monotony = any(w in t for w in ["aburrido", "rutina", "igual", "siempre"])
    low = any(w in t for w in ["cansado", "sin energia", "agotado"])

    if mode == "casa":
        return "HOME_LOW" if low else "HOME_BALANCE"

    if stress:
        return "OUT_STRUCTURE"
    if monotony:
        return "OUT_EXPLORATION"
    if low:
        return "OUT_SLOW"

    return "OUT_BALANCE"

# ----------------------------
# PRESUPUESTO REAL RANGE
# ----------------------------
def budget_range(level):
    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 70),
        "libre": (70, 999999)
    }.get(level, (0, 40))

# ----------------------------
# 3 LUGARES INTELIGENTES USA
# (GENÉRICO POR ESTADO + ZIP)
# ----------------------------
def generate_places(state, budget_level):

    min_b, max_b = budget_range(budget_level)

    base_places = [
        "parque natural público",
        "playa accesible",
        "sendero caminata",
        "lago comunitario",
        "downtown walk zone",
        "botanical garden",
        "river walk",
        "urban park plaza"
    ]

    # siempre 3 opciones (clave UX)
    options = random.sample(base_places, 3)

    return [
        {
            "name": f"{opt} - {state}",
            # 🔥 FIX IMPORTANTE: MAPA USA REAL POR ESTADO
            "map": f"https://www.google.com/maps/search/?api=1&query={opt}+{state}+USA",

            "cost": f"${min_b} - ${max_b}",

            "why": "equilibrio emocional + exploración guiada"
        }
        for opt in options
    ]

# ----------------------------
# MISSIONS SAFE
# ----------------------------
def get_mission():
    pool = random.choice(MISSIONS).get("missions", [])
    if not pool:
        return {
            "b": [{"story": {"es": "Respira. Estás en movimiento.", "en": "You are moving forward."}}]
        }
    return random.choice(pool)

# ----------------------------
# ROUTE EMOTION
# ----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def router():

    data = request.get_json(force=True)

    mode = data.get("decision", "salir")
    budget = data.get("budget_level", "cero")
    text = data.get("desahogo", "")
    state = data.get("estado", "FL").upper()
    zip_code = data.get("zip_code", "")

    # VALIDACIÓN REAL 50 ESTADOS
if state not in US_STATES:
    state = "FL"

zip_code = data.get("zip_code", "").strip()

emotion = analyze_emotion(text, mode)

    # ---------------- CASA ----------------
    if mode == "casa":
        return jsonify({
            "status": "success",
            "type": "HOME",
            "emotion": emotion,
            "title": "OPEN ◯ THAN GO",
            "mission": mission,
            "ui": {
                "mode": "casa",
                "breathing": "deep",
                "voice": True,
                "timer": 600
            }
        })

    # ---------------- SALIR ----------------
    places = generate_places(state, budget)

    return jsonify({
        "status": "success",
        "type": "OUT",
        "emotion": emotion,
        "title": "OPEN ◎ THAN GO",

        "budget_range": budget_range(budget),

        "recommendations": places,

        "mission": mission,

        "ui": {
            "mode": "salir",
            "breathing": "light",
            "voice": True,
            "guidance": "directive"
        }
    })

# ----------------------------
# FRONT
# ----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")

# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

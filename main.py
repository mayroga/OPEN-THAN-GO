# OPEN THAN GO SYSTEM - EMOTION ROUTER v1
# May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import random
import os
import json

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
# EMOTION ANALYZER (CORE)
# ----------------------------
def analyze_emotion(text, decision):
    text = (text or "").lower()

    stress_words = ["trabajo", "estres", "cansado", "ansiedad", "presión"]
    monotony_words = ["aburrido", "igual", "rutina", "nada cambia"]
    low_energy_words = ["sin energia", "agotado", "fatiga"]

    score = {
        "stress": any(w in text for w in stress_words),
        "monotony": any(w in text for w in monotony_words),
        "low_energy": any(w in text for w in low_energy_words),
        "control_desire": "decidir" in text or "elige" in text
    }

    if decision == "casa":
        return "home_low_intensity" if score["low_energy"] else "home_balance"

    if score["stress"]:
        return "out_structured"
    if score["monotony"]:
        return "out_exploration"
    if score["control_desire"]:
        return "out_directive"

    return "out_balance"


# ----------------------------
# BUDGET ENGINE (REAL RANGES)
# ----------------------------
def budget_range(level):
    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 70),
        "libre": (70, 1000000)
    }.get(level, (0, 40))


# ----------------------------
# LOCATION SUGGESTION ENGINE
# ----------------------------
def generate_options(budget_level, mood, location_label):
    min_b, max_b = budget_range(budget_level)

    base = {
        "cero": ["playa pública", "parque natural", "sendero caminata"],
        "minimo": ["cafetería tranquila", "parque con vista", "mercado local"],
        "moderado": ["restaurante casual", "cine", "centro recreativo"],
        "libre": ["experiencia premium", "restaurante top", "hotel lounge"]
    }

    pool = base.get(budget_level, base["cero"])

    # ALWAYS 3 OPTIONS (IMPORTANT)
    return random.sample(pool, k=min(3, len(pool)))


# ----------------------------
# MISSION PICKER
# ----------------------------
def get_mission(mode, budget):
    pool = random.choice(MISSIONS).get("missions", [])

    if not pool:
        return {
            "b": [{"story": {"es": "Sistema en ajuste emocional.", "en": "System adjusting."}}]
        }

    return random.choice(pool)


# ----------------------------
# API EMOTION ROUTE
# ----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def route_emotion():

    data = request.get_json(force=True)

    decision = data.get("decision", "salir")
    budget = data.get("budget_level", "cero")
    text = data.get("desahogo", "")
    lang = data.get("lang", "es")

    emotion_mode = analyze_emotion(text, decision)

    # HOME FLOW (simple + calm)
    if decision == "casa":
        return jsonify({
            "status": "success",
            "type": "HOME",
            "emotion_mode": emotion_mode,
            "mission": get_mission("home", budget),
            "ui": {
                "breathing": "simple_circle",
                "voice": True,
                "guidance_level": "soft"
            }
        })

    # OUT FLOW (directive + 3 options ALWAYS)
    options = generate_options(budget, emotion_mode, "user_location")

    mission = get_mission("out", budget)

    return jsonify({
        "status": "success",
        "type": "OUT",
        "emotion_mode": emotion_mode,

        "recommendations": options,

        "mission": mission,

        "ui": {
            "breathing": "light_intro_only",
            "voice": True,
            "guidance_level": "directive"
        }
    })


# ----------------------------
# FRONT
# ----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

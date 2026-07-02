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
    try:
        if not os.path.exists(path):
            return {"missions": []}
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
# EMOTION ENGINE (CORE)
# ----------------------------
def analyze_emotion(text, decision):
    text = (text or "").lower()

    stress = any(w in text for w in ["trabajo", "estres", "ansiedad", "presion", "cansado"])
    monotony = any(w in text for w in ["aburrido", "rutina", "igual", "siempre lo mismo"])
    low_energy = any(w in text for w in ["sin energia", "agotado", "fatiga", "cansancio"])
    control = any(w in text for w in ["decidir", "elige", "no quiero pensar", "guiame"])

    if decision == "casa":
        return "home_low" if low_energy else "home_balance"

    if stress:
        return "out_structure"
    if monotony:
        return "out_explore"
    if control:
        return "out_directive"
    if low_energy:
        return "out_soft"

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
# LOCATION OPTIONS ENGINE
# ----------------------------
def generate_options(budget_level):

    min_b, max_b = budget_range(budget_level)

    pools = {
        "cero": [
            "playa pública cercana",
            "parque natural",
            "sendero caminata tranquilo",
            "mirador gratuito"
        ],
        "minimo": [
            "cafetería tranquila",
            "parque con vista al agua",
            "mercado local",
            "biblioteca o espacio público"
        ],
        "moderado": [
            "restaurante casual",
            "cine",
            "centro recreativo",
            "actividad cultural local"
        ],
        "libre": [
            "experiencia premium",
            "restaurante top",
            "hotel lounge",
            "evento privado"
        ]
    }

    base = pools.get(budget_level, pools["cero"])

    # 🔥 SIEMPRE 3 OPCIONES
    return random.sample(base, k=3 if len(base) >= 3 else len(base))


# ----------------------------
# MISSION ENGINE
# ----------------------------
def get_mission(mode, budget):
    try:
        pool = random.choice(MISSIONS).get("missions", [])

        if not pool:
            return {
                "b": [{
                    "story": {
                        "es": "Sistema en ajuste emocional.",
                        "en": "System adjusting emotional flow."
                    }
                }]
            }

        return random.choice(pool)

    except:
        return {
            "b": [{
                "story": {
                    "es": "Error de sistema emocional.",
                    "en": "System emotional error."
                }
            }]
        }


# ----------------------------
# API EMOTION ROUTER
# ----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def route_emotion():

    data = request.get_json(force=True) or {}

    decision = data.get("decision", "salir")
    budget = data.get("budget_level", "cero")
    text = data.get("desahogo", "")
    lang = data.get("lang", "es")

    emotion_mode = analyze_emotion(text, decision)

    # ----------------------------
    # CASA MODE (INTERIOR FLOW)
    # ----------------------------
    if decision == "casa":

        return jsonify({
            "status": "success",
            "type": "HOME",
            "emotion_mode": emotion_mode,

            "mission": get_mission("home", budget),

            "ui": {
                "mode": "casa",
                "breathing": "soft_circle",
                "voice": True,
                "guidance": "soft",
                "timer": 600
            }
        })

    # ----------------------------
    # SALIR MODE (EXTERNAL FLOW)
    # ----------------------------
    options = generate_options(budget)

    mission = get_mission("out", budget)

    return jsonify({
        "status": "success",
        "type": "OUT",
        "emotion_mode": emotion_mode,

        # 🔥 CLAVE: SIEMPRE 3 OPCIONES
        "recommendations": options,

        "mission": mission,

        "ui": {
            "mode": "salir",
            "breathing": "intro_light",
            "voice": True,
            "guidance": "directive",
            "map_enabled": True
        }
    })


# ----------------------------
# FRONTEND
# ----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

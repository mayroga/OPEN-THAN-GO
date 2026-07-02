# OPEN THAN GO SYSTEM - BIOPSYCHOSOCIAL EMOTION ROUTER v3
# May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import random
import os
import json

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------
# LOAD MISSIONS (SAFE)
# ----------------------------
def load_json(path):
    if not os.path.exists(path):
        return {"missions": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"missions": []}

MISSIONS = [
    load_json(os.path.join(BASE_DIR, "missions_01_07.json")),
    load_json(os.path.join(BASE_DIR, "missions_08_14.json")),
    load_json(os.path.join(BASE_DIR, "missions_15_21.json"))
]

# ----------------------------
# BIOPSYCHOSOCIAL ENGINE
# ----------------------------
def analyze_user(text, decision):
    text = (text or "").lower()

    profile = {
        "stress": any(w in text for w in ["estres", "trabajo", "ansiedad", "presion"]),
        "monotony": any(w in text for w in ["aburrido", "rutina", "igual"]),
        "low_energy": any(w in text for w in ["cansado", "agotado", "sin energia"]),
        "economic_pressure": any(w in text for w in ["dinero", "biles", "deuda", "caro"]),
        "control_need": any(w in text for w in ["decidir", "elige", "no quiero pensar"]),
        "social_need": any(w in text for w in ["solo", "familia", "hijos", "pareja"])
    }

    if decision == "casa":
        return "HOME_LOW" if profile["low_energy"] else "HOME_BALANCED"

    if profile["stress"]:
        return "OUT_STRUCTURE"
    if profile["monotony"]:
        return "OUT_RECONNECTION"
    if profile["economic_pressure"]:
        return "OUT_AUSTERITY"
    if profile["control_need"]:
        return "OUT_DIRECTIVE"

    return "OUT_BALANCED"

# ----------------------------
# BUDGET SYSTEM (REAL RANGES)
# ----------------------------
def budget_range(level):
    return {
        "cero": (0, 40),
        "minimo": (20, 60),
        "moderado": (40, 70),
        "libre": (70, 999999)
    }.get(level, (0, 40))

# ----------------------------
# DESTINATION ENGINE (3 OPTIONS ALWAYS)
# ----------------------------
def generate_places(budget_level, emotion):
    base = {
        "cero": [
            "parque público accesible",
            "playa gratuita",
            "sendero natural"
        ],
        "minimo": [
            "cafetería tranquila",
            "parque con sombra",
            "biblioteca pública"
        ],
        "moderado": [
            "restaurante casual",
            "cine local",
            "centro recreativo"
        ],
        "libre": [
            "rooftop lounge",
            "hotel experiencia",
            "restaurante premium"
        ]
    }

    pool = base.get(budget_level, base["cero"])

    # SIEMPRE 3 OPCIONES (NO ROMPER CARGA MENTAL)
    return random.sample(pool, k=min(3, len(pool)))

# ----------------------------
# MISSION ENGINE (SAFE FALLBACK)
# ----------------------------
def get_mission():
    pool = random.choice(MISSIONS).get("missions", [])
    if not pool:
        return {
            "b": [{
                "story": {
                    "es": "Sistema en equilibrio.",
                    "en": "System in balance."
                }
            }]
        }
    return random.choice(pool)

# ----------------------------
# ROUTER API
# ----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def router():

    data = request.get_json(force=True)

    decision = data.get("decision", "salir")
    budget = data.get("budget_level", "cero")
    text = data.get("desahogo", "")
    lang = data.get("lang", "es")

    emotion = analyze_user(text, decision)

    # ---------------- CASA MODE ----------------
    if decision == "casa":
        return jsonify({
            "status": "success",
            "mode": "HOME",
            "emotion_profile": emotion,
            "mission": get_mission(),
            "ui": {
                "breathing": "deep_reset_10min",
                "voice": True,
                "guidance": "soft_reset"
            }
        })

    # ---------------- SALIR MODE ----------------
    places = generate_places(budget, emotion)

    return jsonify({
        "status": "success",
        "mode": "OUT",
        "emotion_profile": emotion,

        # 3 OPCIONES CLARAS (NO MÁS)
        "recommendations": places,

        # MISIÓN TERAPÉUTICA OCULTA
        "mission": get_mission(),

        "ui": {
            "breathing": "light_anchor_20sec",
            "voice": True,
            "guidance": "directive_companion"
        }
    })

# ----------------------------
# FRONTEND
# ----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")

# ----------------------------
# START
# ----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

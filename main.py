# =========================================================
# OPEN THAN GO SYSTEM - Backend Engine v4 FINAL STABLE
# Company: May Roga LLC
# =========================================================

from flask import Flask, request, jsonify, send_from_directory
import os
import json
import random

app = Flask(__name__, static_folder="static")

# =========================================================
# PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_FILES = [
    "missions_01_07.json",
    "missions_08_14.json",
    "missions_15_21.json"
]

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
# LOAD MISSIONS
# =========================================================
MISSIONS = []

for file in MISSIONS_FILES:
    path = os.path.join(BASE_DIR, file)
    data = load_json(path)
    missions = data.get("missions", [])

    if isinstance(missions, list):
        for m in missions:
            if isinstance(m, dict) and "id" in m:
                MISSIONS.append(m)

MISSIONS = sorted(MISSIONS, key=lambda x: x["id"])

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
# BIO PROFILE
# =========================================================
def biopsocial_profile(text, budget):
    t = (text or "").lower()

    return {
        "stress": any(w in t for w in ["estres", "ansiedad", "presion"]),
        "fatigue": any(w in t for w in ["cansado", "agotado", "sin energia"]),
        "monotony": any(w in t for w in ["aburrido", "rutina", "igual"]),
        "low_budget": budget in ["cero", "minimo"]
    }

# =========================================================
# MISSIONS
# =========================================================
def get_mission():
    if not MISSIONS:
        return {
            "id": 0,
            "b": [{"story": {"es": "Respira. Estás aquí.", "en": "Breathe. You are here."}}]
        }
    return random.choice(MISSIONS)

# =========================================================
# PLACES SIMPLE ENGINE
# =========================================================
PLACES = [
    {"name": "Beach Walk", "mood": ["stress", "fatigue"]},
    {"name": "City Park", "mood": ["monotony"]},
    {"name": "River Path", "mood": ["stress"]},
    {"name": "Quiet Library Zone", "mood": ["fatigue", "monotony"]},
]

def match_places(profile):
    scored = []

    for p in PLACES:
        score = 0
        for m in p["mood"]:
            if profile.get(m):
                score += 2
        scored.append((score, p))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [p for _, p in scored]

# =========================================================
# ROUTES
# =========================================================
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")

@app.route("/health")
def health():
    return {"status": "ok"}

# =========================================================
# CORE API
# =========================================================
@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():

    data = request.get_json(silent=True) or {}

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

    # ================= CASA =================
    if mode == "casa":
        return jsonify({
            "status": "success",
            "type": "Casa",
            "emotion": emotion,
            "mission": mission,
            "ui": {
                "mode": "casa",
                "voice": True,
                "timer": 600,
                "breathing": True
            }
        })

    # ================= SALIR =================
    places = match_places(profile)
    selected = places[0] if places else None

    return jsonify({
        "status": "success",
        "type": "Salida",
        "emotion": emotion,
        "mission": mission,

        "selected_place": selected,
        "all_places": places[:5],

        "location": {
            "state": state,
            "zip": zip_code
        },

        "ui": {
            "mode": "salir",
            "voice": True,
            "guidance": "active"
        }
    })

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

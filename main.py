# OPEN THAN GO SYSTEM - Backend Engine v5 (ULTRA LIGHT ORCHESTRATOR)
# Company: May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os
import time

app = Flask(__name__, static_folder="static")

# -----------------------------
# BASE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_01 = os.path.join(BASE_DIR, "missions_01_07.json")
MISSIONS_08 = os.path.join(BASE_DIR, "missions_08_14.json")
MISSIONS_15 = os.path.join(BASE_DIR, "missions_15_21.json")

# -----------------------------
# CACHE (CRITICAL PERFORMANCE)
# -----------------------------
CACHE = {
    "01": None,
    "08": None,
    "15": None
}

def load_json(path):
    try:
        if not os.path.exists(path):
            return {"missions": []}

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict) and "missions" in data:
            return data

        return {"missions": []}

    except Exception as e:
        print("JSON ERROR:", e)
        return {"missions": []}


def get_pool(version):
    if CACHE[version] is None:
        if version == "01":
            CACHE["01"] = load_json(MISSIONS_01)
        elif version == "08":
            CACHE["08"] = load_json(MISSIONS_08)
        elif version == "15":
            CACHE["15"] = load_json(MISSIONS_15)

    return CACHE[version].get("missions", [])


# -----------------------------
# FALLBACK
# -----------------------------
def fallback(text_es, text_en):
    return {
        "id": 0,
        "b": [
            {
                "story": {
                    "es": text_es,
                    "en": text_en
                }
            }
        ]
    }


# -----------------------------
# LOCATION ENGINE (LIGHT)
# -----------------------------
def resolve_location(zip_code, region, estado):

    zip_code = (zip_code or "").strip()

    if zip_code:
        p = zip_code[:2]

        if p in ["33", "34"]:
            estado = "FL"
        elif p in ["75", "76", "77", "78", "79"]:
            estado = "TX"
        elif p in ["90", "91", "92", "93", "94", "95"]:
            estado = "CA"

    if estado == "FL" and not region:
        region = "South Florida"
    elif estado == "TX" and not region:
        region = "Central Texas"
    elif estado == "CA" and not region:
        region = "Southern California"

    return f"{region} {estado}".strip(), estado, region


# -----------------------------
# MISSION SELECTOR (CASA ONLY)
# -----------------------------
def get_home_mission(pocket):
    pool = get_pool("01")

    if not pool:
        return fallback("Sistema casa no disponible", "Home system not available")

    filtered = [m for m in pool if pocket in (m.get("pocket_match") or [])]

    return random.choice(filtered) if filtered else random.choice(pool)


# -----------------------------
# OUTSIDE ENGINE (1 MIN RULE)
# -----------------------------
def build_outside_experience(zip_code, region, estado, pocket, desahogo):

    location, estado, region = resolve_location(zip_code, region, estado)

    stress_map = {
        "cero": "calm environments like parks or quiet outdoor spaces",
        "minimo": "light social spaces like cafés or local markets",
        "moderado": "balanced stimulation places like restaurants or activity centers",
        "libre": "high energy environments like entertainment areas or premium venues"
    }

    base_context = stress_map.get(pocket, "neutral environments")

    if any(w in desahogo for w in ["ansiedad", "stress", "estres", "presión"]):
        psychological_reason = "reduce cognitive overload and restore nervous system balance"
    elif any(w in desahogo for w in ["solo", "alone", "soledad"]):
        psychological_reason = "increase social exposure and reduce isolation patterns"
    else:
        psychological_reason = "create emotional reset through environmental change"

    term = base_context

    query = f"{term} near {location}".replace(" ", "+")
    gps = f"https://www.google.com/maps/search/?api=1&query={query}"

    return {
        "name": f"Micro-experience: {term}",
        "address": location,
        "estado": estado,
        "region": region,
        "gps_link": gps,
        "why": psychological_reason,
        "action": "Go to this place for 5–10 minutes. Observe environment, breathe slowly, avoid overstimulation.",
        "duration": 60
    }


# -----------------------------
# API ROUTE (ORCHESTRATOR ONLY)
# -----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():

    try:
        start = time.time()

        data = request.get_json(force=True) or {}

        decision = data.get("decision", "salir")
        pocket = data.get("budget_level", "cero")
        zip_code = data.get("zip_code", "")
        region = data.get("region", "")
        estado = data.get("estado", "FL")
        desahogo = (data.get("desahogo") or "").lower()
        lang = data.get("lang", "es")

        onboarding = [
            "¿Qué emoción domina tu día?",
            "¿Necesitas calma o acción?",
            "¿Tu energía está baja, media o alta?"
        ]

        # -----------------------------
        # CASA MODE (10 MIN FLOW)
        # -----------------------------
        if decision == "casa":

            mission = get_home_mission(pocket)

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "duration_sec": 600,
                "onboarding": onboarding,
                "mision": mission,
                "ui": {
                    "mode": "home",
                    "voice": True,
                    "breathing": True,
                    "timer": 600
                }
            })

        # -----------------------------
        # SALIR MODE (1 MIN FLOW)
        # -----------------------------
        outside = build_outside_experience(
            zip_code, region, estado, pocket, desahogo
        )

        mission = get_home_mission(pocket)

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "duration_sec": 60,
            "onboarding": onboarding,
            "lugar": outside,
            "mision": mission,
            "ui": {
                "mode": "out",
                "voice": True,
                "breathing": False,
                "timer": 60
            }
        })

    except Exception as e:
        print("API ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -----------------------------
# FRONT
# -----------------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "session.html")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )

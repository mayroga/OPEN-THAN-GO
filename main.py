# OPEN THAN GO SYSTEM - Backend Engine v5 (STABLE CORE)
# Company: May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import json, random, os

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_01 = os.path.join(BASE_DIR, "missions_01_07.json")
MISSIONS_08 = os.path.join(BASE_DIR, "missions_08_14.json")
MISSIONS_15 = os.path.join(BASE_DIR, "missions_15_21.json")


# -----------------------------
# JSON SAFE LOAD
# -----------------------------
def load_json(path):
    try:
        if not os.path.exists(path):
            return {"missions": []}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {"missions": []}
    except:
        return {"missions": []}


DATA = [
    load_json(MISSIONS_01),
    load_json(MISSIONS_08),
    load_json(MISSIONS_15)
]


# -----------------------------
# FALLBACK
# -----------------------------
def fallback(es, en):
    return {
        "id": 0,
        "b": [{"story": {"es": es, "en": en}}]
    }


# -----------------------------
# LOCATION FIX SIMPLE
# -----------------------------
def resolver(zip_code, region, estado):

    zip_code = (zip_code or "").strip()
    region = (region or "").strip()
    estado = (estado or "FL").strip()

    if zip_code.startswith("33") or zip_code.startswith("34"):
        estado = "FL"
    elif zip_code[:2] in ["75","76","77","78","79"]:
        estado = "TX"
    elif zip_code[:2] in ["90","91","92","93","94","95"]:
        estado = "CA"

    if not region:
        region = "General Area"

    return estado, region


# -----------------------------
# MISSION
# -----------------------------
def mission(pocket):

    pool = random.choice(DATA).get("missions", [])

    if not pool:
        return fallback("Sistema sin misiones", "No missions available")

    filtered = [m for m in pool if pocket in (m.get("pocket_match") or [])]

    return random.choice(filtered) if filtered else random.choice(pool)


# -----------------------------
# ROUTE
# -----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")


# -----------------------------
# API
# -----------------------------
@app.route("/api/open-than-go", methods=["POST"])
def api():

    try:
        d = request.get_json() or {}

        decision = d.get("decision", "salir")
        pocket = d.get("budget_level", "cero")
        zip_code = d.get("zip_code", "")
        region = d.get("region", "")
        estado = d.get("estado", "FL")

        desahogo = (d.get("desahogo") or "").lower()

        estado, region = resolver(zip_code, region, estado)

        onboarding = [
            "¿Cómo te sientes hoy?",
            "¿Quieres calma o acción?",
            "¿Tu energía está baja o alta?",
            "¿Qué necesitas realmente ahora?"
        ]

        # ---------------- HOME ----------------
        if decision == "casa":

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "mode": "home",
                "onboarding": onboarding,
                "mision": mission("casa", pocket),
                "ui": {
                    "voice": "male_es_only",
                    "breathing": True,
                    "timer_sec": 600
                }
            })

        # ---------------- OUT ----------------
        termino = "parques"
        if "trabajo" in desahogo:
            termino = "empleo oficinas"

        ubicacion = f"{region} {estado}".strip()

        gps = f"https://www.google.com/maps/search/?api=1&query={termino}+en+{ubicacion}".replace(" ", "+")

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "mode": "out",
            "lugar": {
                "termino": termino,
                "ubicacion": ubicacion,
                "gps": gps
            },
            "onboarding": onboarding,
            "mision": mission(pocket),
            "ui": {
                "voice": "locked_by_lang",
                "breathing": True,
                "timer_sec": 600
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

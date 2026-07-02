# OPEN THAN GO SYSTEM - Backend Engine v3 (STABLE + SYNC FIX)
# Company: May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder="static")

# ----------------------------------------------------
# PATHS
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_01 = os.path.join(BASE_DIR, "missions_01_07.json")
MISSIONS_08 = os.path.join(BASE_DIR, "missions_08_14.json")
MISSIONS_15 = os.path.join(BASE_DIR, "missions_15_21.json")

# ----------------------------------------------------
# SAFE JSON
# ----------------------------------------------------
def cargar_json(ruta):
    try:
        if not os.path.exists(ruta):
            return {"missions": []}

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, dict) else {"missions": []}

    except Exception as e:
        print("JSON ERROR:", e)
        return {"missions": []}

DATA_01 = cargar_json(MISSIONS_01)
DATA_08 = cargar_json(MISSIONS_08)
DATA_15 = cargar_json(MISSIONS_15)

# ----------------------------------------------------
# FALLBACK (NO CRASH EVER)
# ----------------------------------------------------
def fallback_mission(es, en=""):
    return {
        "id": 0,
        "cat": "fallback",
        "b": [
            {
                "story": {
                    "es": es,
                    "en": en or es
                }
            }
        ]
    }

# ----------------------------------------------------
# ZIP → STATE FIX (REAL USA LOGIC SIMPLIFIED)
# ----------------------------------------------------
def estado_desde_zip(zip_code, estado_default):
    if not zip_code:
        return estado_default

    prefix = zip_code[:2]

    if prefix in ["33", "34"]:
        return "FL"
    if prefix in ["75", "76", "77", "78", "79"]:
        return "TX"
    if prefix in ["90", "91", "92", "93", "94", "95"]:
        return "CA"

    return estado_default

# ----------------------------------------------------
# REGIÓN CONSISTENTE (IMPORTANT FIX)
# ----------------------------------------------------
REGIONES = {
    "FL": ["South Florida", "Central Florida", "North Florida"],
    "TX": ["North Texas", "Central Texas", "South Texas"],
    "CA": ["Northern California", "Central California", "Southern California"]
}

def asegurar_region(estado, region):
    if estado not in REGIONES:
        return ""

    if region in REGIONES[estado]:
        return region

    return random.choice(REGIONES[estado])

# ----------------------------------------------------
# LOCATION RESOLVER (FINAL FIX)
# ----------------------------------------------------
def resolver_ubicacion(zip_code, region, estado):
    estado = estado_desde_zip(zip_code, estado)
    region = asegurar_region(estado, region)

    if zip_code:
        return f"{region} {estado} ({zip_code})"

    if region:
        return f"{region} {estado}"

    return estado

# ----------------------------------------------------
# MISSIONS
# ----------------------------------------------------
def cargar_mision(decision, pocket):
    try:
        if decision == "casa":
            pool = DATA_01.get("missions", [])
            if not pool:
                return fallback_mission("Sistema doméstico no disponible.")
            return random.choice(pool)

        pool = random.choice([DATA_08, DATA_15]).get("missions", [])
        if not pool:
            pool = DATA_01.get("missions", [])

        if not pool:
            return fallback_mission("No hay misiones disponibles.")

        filtradas = [
            m for m in pool
            if pocket in (m.get("pocket_match") or [])
        ]

        return random.choice(filtradas) if filtradas else random.choice(pool)

    except Exception as e:
        print("MISSION ERROR:", e)
        return fallback_mission("Error interno del sistema.")

# ----------------------------------------------------
# FRONTEND
# ----------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "session.html")

# ----------------------------------------------------
# API
# ----------------------------------------------------
@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():

    try:
        data = request.get_json(silent=True) or {}

        decision = data.get("decision", "salir")
        pocket = data.get("budget_level", "cero")

        zip_code = (data.get("zip_code") or "").strip()
        region = (data.get("region") or "").strip()
        estado = (data.get("estado") or "FL").strip()

        desahogo = (data.get("desahogo") or "").lower()

        # -------------------------
        # CASA MODE
        # -------------------------
        if decision == "casa":

            mision = cargar_mision("casa", "cero")

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "mode": "home",
                "mision": mision,
                "ui": {
                    "breathing_duration": 26000,
                    "auto_end": True
                }
            })

        # -------------------------
        # LOCATION FIXED
        # -------------------------
        ubicacion = resolver_ubicacion(zip_code, region, estado)

        # -------------------------
        # CATEGORY ENGINE
        # -------------------------
        categorias = {
            "cero": ["parques publicos", "playas", "senderos"],
            "minimo": ["cafeterias", "mercados locales"],
            "moderado": ["restaurantes", "centros recreativos"],
            "libre": ["hoteles", "clubs", "restaurantes premium"]
        }

        if any(w in desahogo for w in ["trabajo", "job", "empleo"]):
            termino = "agencias de empleo y trabajo"
        else:
            termino = random.choice(categorias.get(pocket, ["parques"]))

        # -------------------------
        # MAP LINK SAFE
        # -------------------------
        query = f"{termino} {ubicacion}".replace(" ", "+")
        gps_link = f"https://www.google.com/maps/search/?api=1&query={query}"

        # -------------------------
        # MISSION
        # -------------------------
        mision = cargar_mision("salir", pocket)

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "mode": "out",
            "lugar": {
                "name": f"Exploración de {termino}",
                "address": ubicacion,
                "region": region,
                "estado": estado,
                "zip": zip_code,
                "gps_link": gps_link
            },
            "mision": mision,
            "ui": {
                "breathing_duration": 26000,
                "silence_mode": True
            }
        })

    except Exception as e:
        print("API ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ----------------------------------------------------
# RUN
# ----------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )

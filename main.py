# OPEN THAN GO SYSTEM - Backend Engine v5 (STABLE + UX SYNC)
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
# SAFE JSON LOADER
# ----------------------------------------------------
def cargar_json(ruta):
    try:
        if not os.path.exists(ruta):
            return {"missions": []}

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, dict) and "missions" in data else {"missions": []}

    except Exception as e:
        print("JSON ERROR:", e)
        return {"missions": []}


DATA_01 = cargar_json(MISSIONS_01)
DATA_08 = cargar_json(MISSIONS_08)
DATA_15 = cargar_json(MISSIONS_15)

# ----------------------------------------------------
# FALLBACK SAFE
# ----------------------------------------------------
def fallback_mission(es, en):
    return {
        "id": 0,
        "cat": "fallback",
        "b": [
            {
                "story": {
                    "es": es,
                    "en": en
                }
            }
        ]
    }

# ----------------------------------------------------
# LOCATION ENGINE (FIXED + CLEAN)
# ----------------------------------------------------
def resolver_ubicacion(zip_code, region, estado):

    zip_code = (zip_code or "").strip()
    region = (region or "").strip()
    estado = (estado or "FL").strip()

    # ZIP OVERRIDE (prioridad absoluta)
    if zip_code:
        prefix = zip_code[:2]

        if prefix in ["33", "34"]:
            estado = "FL"
        elif prefix in ["75", "76", "77", "78", "79"]:
            estado = "TX"
        elif prefix in ["90", "91", "92", "93", "94", "95"]:
            estado = "CA"

    # NORMALIZACIÓN LIMPIA (SIN CRUCES LÓGICOS)
    regiones_base = {
        "FL": "Florida",
        "TX": "Texas",
        "CA": "California"
    }

    if not region:
        region = regiones_base.get(estado, "Unknown")

    return f"{region} {estado}", estado, region

# ----------------------------------------------------
# MISSION ENGINE
# ----------------------------------------------------
def cargar_mision(decision, pocket):
    try:

        if decision == "casa":
            pool = DATA_01.get("missions", [])
            if not pool:
                return fallback_mission(
                    "Sistema doméstico no disponible.",
                    "Home system not available."
                )
            return random.choice(pool)

        pool = random.choice([DATA_08, DATA_15]).get("missions", [])

        if not pool:
            pool = DATA_01.get("missions", [])

        if not pool:
            return fallback_mission(
                "No hay misiones disponibles.",
                "No missions available."
            )

        filtradas = [
            m for m in pool
            if pocket in (m.get("pocket_match") or [])
        ]

        return random.choice(filtradas) if filtradas else random.choice(pool)

    except Exception as e:
        print("MISSION ERROR:", e)
        return fallback_mission(
            "Error interno del sistema.",
            str(e)
        )

# ----------------------------------------------------
# FRONTEND
# ----------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "session.html")

# ----------------------------------------------------
# API MAIN
# ----------------------------------------------------
@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():

    try:
        data = request.get_json(silent=True) or {}

        decision = data.get("decision", "salir")
        pocket = data.get("budget_level", "cero")

        zip_code = data.get("zip_code", "")
        region = data.get("region", "")
        estado = data.get("estado", "FL")

        desahogo = (data.get("desahogo") or "").lower()
        lang = data.get("lang", "es")

        # ------------------------------------------------
        # ONBOARDING (MEJORADO, MENOS RUIDO)
        # ------------------------------------------------
        onboarding = [
            "¿Qué necesitas ahora: calma o movimiento?",
            "¿Cómo está tu energía hoy?",
            "¿Quieres pensar o desconectar?",
            "¿Prefieres estar solo o acompañado?",
            "¿Qué te aliviaría en este momento?"
        ]

        # ------------------------------------------------
        # CASA MODE (10 MIN EXACTOS)
        # ------------------------------------------------
        if decision == "casa":

            mision = cargar_mision("casa", "cero")

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "mode": "home",
                "onboarding": onboarding,
                "mision": mision,
                "ui": {
                    "voice": {
                        "enabled": True,
                        "lock_by_language": True,
                        "es": "male",
                        "en": "male"
                    },
                    "breathing": {
                        "duration_sec": 600,
                        "style": "single_orb"
                    },
                    "timer": {
                        "duration_sec": 600
                    }
                }
            })

        # ------------------------------------------------
        # LOCATION ENGINE
        # ------------------------------------------------
        ubicacion, estado, region = resolver_ubicacion(zip_code, region, estado)

        categorias = {
            "cero": ["parques publicos", "playas", "senderos"],
            "minimo": ["cafeterias", "mercados locales"],
            "moderado": ["restaurantes", "centros recreativos"],
            "libre": ["hoteles", "clubs", "restaurantes premium"]
        }

        if any(w in desahogo for w in ["trabajo", "job", "empleo"]):
            termino = "agencias de empleo"
        else:
            termino = random.choice(categorias.get(pocket, ["parques"]))

        query = f"{termino} en {ubicacion}".replace(" ", "+")
        gps_link = f"https://www.google.com/maps/search/?api=1&query={query}"

        # ------------------------------------------------
        # IMAGENES (PARA UX VISUAL REAL)
        # ------------------------------------------------
        image_queries = [
            f"{termino} exterior",
            f"{termino} ambiente",
            f"{termino} personas",
            f"{termino} interior"
        ]

        mision = cargar_mision("salir", pocket)

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "mode": "out",

            "lugar": {
                "name": f"Exploración de {termino}",
                "address": f"Cerca de {ubicacion}",
                "estado": estado,
                "region": region,
                "zip": zip_code,
                "gps_link": gps_link,
                "image_queries": image_queries
            },

            "onboarding": onboarding,
            "mision": mision,

            "ui": {
                "voice": {
                    "enabled": True,
                    "lock_by_language": True,
                    "es": "male",
                    "en": "male"
                },
                "breathing": {
                    "duration_sec": 600,
                    "style": "single_orb_pulse"
                },
                "timer": {
                    "duration_sec": 600
                }
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
    app.run(host="0.0.0.0", port=port, debug=True)

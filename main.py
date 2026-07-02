# ======================================================
# OPEN THAN GO SYSTEM - Backend Engine PRO v2
# May Roga LLC
# ======================================================

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder="static")

# ----------------------------------------------------
# PATHS SEGURAS
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_01 = os.path.join(BASE_DIR, "missions_01_07.json")
MISSIONS_08 = os.path.join(BASE_DIR, "missions_08_14.json")
MISSIONS_15 = os.path.join(BASE_DIR, "missions_15_21.json")


# ----------------------------------------------------
# LOAD JSON SAFE
# ----------------------------------------------------
def cargar_json(ruta):
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception as e:
        print("JSON ERROR:", ruta, e)

    return {"missions": []}


DATA_01 = cargar_json(MISSIONS_01)
DATA_08 = cargar_json(MISSIONS_08)
DATA_15 = cargar_json(MISSIONS_15)


# ----------------------------------------------------
# FALLBACK MISSION (SAFE MODE)
# ----------------------------------------------------
def fallback_mission(es, en):
    return {
        "id": 0,
        "cat": "fallback",
        "pocket_match": ["cero", "minimo", "moderado", "libre"],
        "b": [
            {
                "t": "v",
                "tx": {"es": es, "en": en}
            }
        ]
    }


# ----------------------------------------------------
# NORMALIZAR POCKET
# ----------------------------------------------------
def normalize_pocket(pocket):
    valid = ["cero", "minimo", "moderado", "libre"]
    return pocket if pocket in valid else "cero"


# ----------------------------------------------------
# CARGA INTELIGENTE DE MISIÓN
# ----------------------------------------------------
def cargar_mision(decision, pocket):

    try:
        pocket = normalize_pocket(pocket)

        # -------------------------
        # CASA MODE
        # -------------------------
        if decision == "casa":
            pool = DATA_01.get("missions", [])
            if not pool:
                return fallback_mission(
                    "No hay misiones domésticas disponibles.",
                    "No home missions available."
                )

            candidatas = [
                m for m in pool
                if pocket in m.get("pocket_match", ["cero"])
            ]

            return random.choice(candidatas or pool)

        # -------------------------
        # OUT MODE (SALIR)
        # -------------------------
        pool = []
        for dataset in [DATA_08, DATA_15]:
            pool.extend(dataset.get("missions", []))

        if not pool:
            pool = DATA_01.get("missions", [])

        if not pool:
            return fallback_mission(
                "Sistema sin misiones disponibles.",
                "No missions available in system."
            )

        candidatas = [
            m for m in pool
            if pocket in m.get("pocket_match", ["cero"])
        ]

        return random.choice(candidatas or pool)

    except Exception as e:
        print("cargar_mision ERROR:", e)
        return fallback_mission(
            "Error interno generando misión.",
            str(e)
        )


# ----------------------------------------------------
# FRONTEND
# ----------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "session.html")


# ----------------------------------------------------
# API PRINCIPAL
# ----------------------------------------------------
@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():

    try:
        data = request.get_json(silent=True) or {}

        decision = (data.get("decision") or "salir").lower()
        pocket = (data.get("budget_level") or "cero").lower()

        zip_code = (data.get("zip_code") or "").strip()
        region = (data.get("region") or "").strip()
        estado = (data.get("estado") or "FL").strip()

        feeling = (data.get("feeling") or "").lower()

        # ------------------------------------------------
        # CASA MODE
        # ------------------------------------------------
        if decision == "casa":

            mision = cargar_mision("casa", pocket)

            return jsonify({
                "status": "success",
                "mode": "home",
                "mood": "calma",
                "mision": mision,
                "ui": {
                    "timer": 600,
                    "breathing": True,
                    "auto_end": True
                }
            })

        # ------------------------------------------------
        # UBICACIÓN INTELIGENTE
        # ------------------------------------------------
        if zip_code:
            ubicacion = zip_code
        elif region:
            ubicacion = f"{region}, {estado}"
        else:
            ubicacion = estado

        # ------------------------------------------------
        # INTENCIÓN SIMPLE (FUTURO IA AQUÍ)
        # ------------------------------------------------
        categorias = {
            "cero": ["parques naturales", "playas tranquilas", "senderos"],
            "minimo": ["cafeterías locales", "mercados pequeños"],
            "moderado": ["restaurantes", "centros recreativos"],
            "libre": ["hoteles", "clubs", "experiencias premium"]
        }

        if any(w in feeling for w in ["estres", "trabajo", "job"]):
            termino = "centros de relajación"
        elif any(w in feeling for w in ["aburrido", "empty", "solo"]):
            termino = "lugares para reconectar"
        else:
            termino = random.choice(categorias.get(pocket, ["parques"]))

        # ------------------------------------------------
        # GOOGLE MAPS LINK
        # ------------------------------------------------
        query = f"{termino} en {ubicacion}".replace(" ", "+")
        gps_link = f"https://www.google.com/maps/search/?api=1&query={query}"

        # ------------------------------------------------
        # MISIÓN
        # ------------------------------------------------
        mision = cargar_mision("salir", pocket)

        return jsonify({
            "status": "success",
            "mode": "out",
            "location": {
                "label": termino,
                "address": ubicacion,
                "gps_link": gps_link
            },
            "mision": mision,
            "ui": {
                "maps_enabled": True,
                "breathing": True,
                "mission_mode": True
            }
        })

    except Exception as e:
        print("API ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e),
            "fallback": fallback_mission(
                "Error del sistema, reinicia la sesión.",
                "System error, restart session."
            )
        }), 500


# ----------------------------------------------------
# RUN SERVER
# ----------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )

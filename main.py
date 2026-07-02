# OPEN THAN GO SYSTEM - Backend Engine (FIXED VERSION)
# Company: May Roga LLC

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
                if isinstance(data, dict) and "missions" in data:
                    return data
    except Exception as e:
        print("Error cargando JSON:", e)

    return {"missions": []}


DATA_01 = cargar_json(MISSIONS_01)
DATA_08 = cargar_json(MISSIONS_08)
DATA_15 = cargar_json(MISSIONS_15)


# ----------------------------------------------------
# FALLBACK MISSION (NUNCA FALLA)
# ----------------------------------------------------
def fallback_mission(msg_es, msg_en):
    return {
        "id": 0,
        "cat": "fallback",
        "b": [
            {
                "story": {
                    "es": msg_es,
                    "en": msg_en
                }
            }
        ]
    }


# ----------------------------------------------------
# CARGA DE MISIÓN
# ----------------------------------------------------
def cargar_mision(decision, pocket):

    try:

        # CASA
        if decision == "casa":
            pool = DATA_01.get("missions", [])
            if not pool:
                return fallback_mission(
                    "Falta el archivo de misiones domésticas.",
                    "Missing home missions file."
                )
            return random.choice(pool)

        # SALIDA
        pool = random.choice([DATA_08, DATA_15]).get("missions", [])

        if not pool:
            pool = DATA_01.get("missions", [])

        if not pool:
            return fallback_mission(
                "No hay misiones disponibles en el sistema.",
                "No missions available in system."
            )

        # filtro por bolsillo
        filtradas = [
            m for m in pool
            if pocket in m.get("pocket_match", [])
        ]

        return random.choice(filtradas) if filtradas else random.choice(pool)

    except Exception as e:
        print("ERROR cargar_mision:", e)
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

        decision = data.get("decision", "salir")
        pocket = data.get("budget_level", "cero")

        # limpiar strings
        zip_code = (data.get("zip_code") or "").strip()
        region = (data.get("region") or "").strip()
        estado = (data.get("estado") or "FL").strip()

        desahogo = (data.get("desahogo") or "").lower()

        # ---------------------------
        # CASO CASA
        # ---------------------------
        if decision == "casa":

            mision = cargar_mision("casa", "cero")

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "mision": mision
            })

        # ---------------------------
        # UBICACIÓN
        # ---------------------------
        if zip_code:
            ubicacion = zip_code
        elif region:
            ubicacion = f"{region} {estado}"
        else:
            ubicacion = estado

        # ---------------------------
        # CATEGORÍAS
        # ---------------------------
        categorias = {
            "cero": ["parques publicos", "playas", "senderos"],
            "minimo": ["cafeterias", "mercados locales"],
            "moderado": ["restaurantes", "centros recreativos"],
            "libre": ["hoteles", "clubs", "restaurantes premium"]
        }

        # ---------------------------
        # DETECCIÓN SIMPLE
        # ---------------------------
        if any(w in desahogo for w in ["trabajo", "job", "empleo"]):
            termino = "agencias de empleo y trabajo"
        else:
            termino = random.choice(categorias.get(pocket, ["parques"]))

        # ---------------------------
        # MAPA
        # ---------------------------
        query = f"{termino} en {ubicacion}".replace(" ", "+")
        gps_link = f"https://www.google.com/maps/search/?api=1&query={query}"

        # ---------------------------
        # MISIÓN
        # ---------------------------
        mision = cargar_mision("salir", pocket)

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "lugar": {
                "name": f"Exploración de {termino}",
                "address": f"Cerca de {ubicacion}",
                "region": region,
                "gps_link": gps_link
            },
            "mision": mision
        })

    except Exception as e:
        print("ERROR API:", e)

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

# OPEN THAN GO SYSTEM - Backend Engine v5 PRO
# May Roga LLC

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_FILES = [
    "missions_01_07.json",
    "missions_08_14.json",
    "missions_15_21.json"
]

DATASETS = []


# =========================
# LOAD SYSTEM
# =========================
def load_json(path):
    try:
        full = os.path.join(BASE_DIR, path)
        if not os.path.exists(full):
            return {"missions": []}

        with open(full, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if "missions" in data else {"missions": []}

    except Exception as e:
        print("LOAD ERROR:", e)
        return {"missions": []}


for f in MISSIONS_FILES:
    DATASETS.append(load_json(f))


# =========================
# FALLBACK
# =========================
def fallback(es, en):
    return {
        "id": 0,
        "cat": "fallback",
        "pocket_match": ["cero", "moderado", "libre"],
        "b": [
            {"story": {"es": es, "en": en}}
        ]
    }


# =========================
# LOCATION ENGINE (MEJORADO)
# =========================
def resolver_ubicacion(zip_code, region, estado):

    zip_code = (zip_code or "").strip()

    if zip_code:
        prefix = zip_code[:2]

        if prefix in ["33", "34"]:
            estado = "FL"
        elif prefix in ["75", "76", "77", "78", "79"]:
            estado = "TX"
        elif prefix in ["90", "91", "92", "93", "94", "95"]:
            estado = "CA"

    # normalización inteligente
    region_map = {
        "FL": "South Florida",
        "TX": "Central Texas",
        "CA": "Southern California"
    }

    if not region:
        region = region_map.get(estado, "USA")

    return f"{region} {estado}".strip(), estado, region


# =========================
# EMOTION ANALYZER (NUEVO)
# =========================
def analizar_emocion(texto):
    texto = (texto or "").lower()

    if any(w in texto for w in ["ansiedad", "stress", "money", "biles", "deuda"]):
        return "mal"
    if any(w in texto for w in ["feliz", "bien", "love", "tranquilo"]):
        return "bien"
    if any(w in texto for w in ["aburrido", "vacío", "nada"]):
        return "nino"

    return "neutral"


# =========================
# POCKET BOOST (INTENSIDAD)
# =========================
def ajustar_pool(pool, pocket):
    return [
        m for m in pool
        if pocket in (m.get("pocket_match") or [])
    ]


# =========================
# MISSION ENGINE PRO
# =========================
def cargar_mision(decision, pocket, emotion):

    try:
        pool = []

        # CASA MODE
        if decision == "casa":
            pool = DATASETS[0].get("missions", [])

            if not pool:
                return fallback("Sistema doméstico no disponible.", "Home system not available.")

        else:
            # mezcla inteligente de datasets
            candidates = random.choice(DATASETS)
            pool = candidates.get("missions", [])

            if not pool:
                pool = DATASETS[0].get("missions", [])

        # FILTRO POR INTENSIDAD
        filtered = ajustar_pool(pool, pocket)

        if not filtered:
            filtered = pool

        # AJUSTE POR EMOCIÓN
        emotion_filtered = [
            m for m in filtered
            if m.get("cat") in [emotion, "bien", "mal", "nino"]
        ]

        if emotion_filtered:
            return random.choice(emotion_filtered)

        return random.choice(filtered)

    except Exception as e:
        print("MISSION ERROR:", e)
        return fallback("Error interno del sistema.", str(e))


# =========================
# MAIN API
# =========================
@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():

    try:
        data = request.get_json(silent=True) or {}

        decision = data.get("decision", "salir")
        pocket = data.get("budget_level", "cero")

        zip_code = data.get("zip_code", "")
        region = data.get("region", "")
        estado = data.get("estado", "FL")

        desahogo = data.get("desahogo", "")
        lang = data.get("lang", "es")

        emotion = analizar_emocion(desahogo)

        onboarding = [
            "¿Qué emoción domina tu día?",
            "¿Prefieres calma o acción?",
            "¿Tu energía está baja o alta?",
            "¿Quieres escapar o resolver?",
            "¿Qué necesitas ahora?"
        ]

        # =========================
        # CASA MODE
        # =========================
        if decision == "casa":

            mision = cargar_mision("casa", pocket, emotion)

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "mode": "home",
                "emotion": emotion,
                "onboarding": onboarding,
                "mision": mision,
                "ui": {
                    "voice": {"es": "male", "en": "male"},
                    "breathing": {"duration_ms": 25000},
                    "timer": {"duration_sec": 600}
                }
            })

        # =========================
        # OUT MODE
        # =========================
        ubicacion, estado, region = resolver_ubicacion(zip_code, region, estado)

        categorias = {
            "cero": ["parques", "playas"],
            "minimo": ["cafes", "mercados"],
            "moderado": ["restaurantes", "centros"],
            "libre": ["hoteles", "experiencias premium"]
        }

        termino = random.choice(categorias.get(pocket, ["parques"]))

        if any(w in desahogo.lower() for w in ["trabajo", "job"]):
            termino = "empleo agencias"

        query = f"{termino} en {ubicacion}".replace(" ", "+")
        gps_link = f"https://www.google.com/maps/search/?api=1&query={query}"

        mision = cargar_mision("salir", pocket, emotion)

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "mode": "out",
            "emotion": emotion,

            "lugar": {
                "name": f"Exploración de {termino}",
                "gps_link": gps_link,
                "region": region,
                "estado": estado,
                "zip": zip_code
            },

            "onboarding": onboarding,
            "mision": mision,

            "ui": {
                "voice": {"es": "male", "en": "male"},
                "breathing": {"duration_ms": 25000},
                "timer": {"duration_sec": 600}
            }
        })

    except Exception as e:
        print("API ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =========================
# FRONTEND
# =========================
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "session.html")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )

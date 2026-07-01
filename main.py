import json
import random
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")


# ===============================
# LOAD DATA
# ===============================
def load_missions():
    files = [
        "missions_01_07.json",
        "missions_08_14.json",
        "missions_15_21.json"
    ]

    all_missions = []

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
                all_missions.extend(data.get("missions", []))
        except:
            pass

    return all_missions


ALL = load_missions()


# ===============================
# CATEGORY DETECTOR (MEJORADO)
# ===============================
def detectar_categoria(texto):
    t = (texto or "").lower()

    if any(x in t for x in ["deuda", "dinero", "biles", "trabajo", "jefe", "estrés"]):
        return "stress_financiero"

    if any(x in t for x in ["familia", "hijo", "pareja"]):
        return "familia"

    if any(x in t for x in ["solo", "aburrido", "vacío"]):
        return "emocional"

    return "equilibrio"


# ===============================
# DESTINATION ENGINE (REAL LIFE MAP LOGIC)
# ===============================
def generar_tipo_destino(categoria, bolsillo):
    base = ["parks", "nature", "quiet"]

    if categoria == "stress_financiero":
        base = ["cheap_cafes", "libraries", "community_centers", "walkable_areas"]

    if categoria == "familia":
        base = ["family_places", "museums", "zoos", "aquariums", "parks"]

    if categoria == "emocional":
        base = ["beach", "waterfront", "open_spaces", "sunset_points"]

    if bolsillo == "libre":
        base += ["restaurants", "mall", "entertainment", "cinema", "urban_centers"]

    return " OR ".join(base)


# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")


# ===============================
# API
# ===============================
@app.route("/diagnostico-kamizen", methods=["POST"])
def api():

    data = request.get_json(force=True)

    idioma = data.get("idioma", "es")
    bolsillo = data.get("bolsillo", "cero")
    texto = data.get("texto_libre", "")
    salir = data.get("puedes_salir", True)

    estado = data.get("estado", "FL")
    zip_code = data.get("zip_code", "33101")

    categoria = detectar_categoria(texto)

    # ===============================
    # MISSIONS RANDOM PER CATEGORY
    # ===============================
    missions = [m for m in ALL if m.get("cat")]

    if not missions:
        return jsonify({"error": "no_data"})

    mission = random.choice(missions)

    bloques = mission.get("b", [])

    processed = []

    for b in bloques:
        block = dict(b)

        for k in ["tx", "inf", "story"]:
            if isinstance(block.get(k), dict):
                block[k] = block[k].get(idioma, block[k].get("es", ""))

        if isinstance(block.get("q"), dict):
            block["q"] = block["q"].get(idioma, "")

        processed.append(block)

    # ===============================
    # REAL DESTINATION SYSTEM
    # ===============================
    tipo_lugares = generar_tipo_destino(categoria, bolsillo)

    url = f"https://www.google.com/maps/search/{tipo_lugares}+{zip_code}+{estado}".replace(" ", "+")

    # ===============================
    # RESPONSE
    # ===============================
    if not salir:
        return jsonify({
            "mode": "indoor",
            "title": "Inner Reset Mode",
            "blocks": processed,
            "map": None,
            "meta": {
                "loop": 600
            }
        })

    return jsonify({
        "mode": "outdoor",
        "title": "Active Guidance Mode",
        "location": f"{zip_code}, {estado}",
        "blocks": processed,
        "map": url,
        "meta": {
            "loop": 600,
            "system": "decision_engine_v2"
        }
    })


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

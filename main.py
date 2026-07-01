import json
from flask import Flask, request, jsonify

app = Flask(__name__)


# =========================
# LOAD ALL MISSIONS ORDERED
# =========================
def load_missions_ordered():
    files = [
        "missions_01_07.json",
        "missions_08_14.json",
        "missions_15_21.json"
    ]

    missions = []

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
                missions.extend(data.get("missions", []))
        except:
            pass

    # SORT BY ID (CRITICAL FIX)
    missions.sort(key=lambda x: x.get("id", 0))

    return missions


MISSIONS = load_missions_ordered()


# =========================
# SIMPLE STATE MEMORY (NO DB)
# =========================
ENGINE_STATE = {
    "current_index": 0
}


# =========================
# DETECTOR SIMPLE
# =========================
def detectar_categoria(texto):
    t = texto.lower()

    if any(x in t for x in ["dinero", "deuda", "biles", "estrés"]):
        return "mal"

    if any(x in t for x in ["niño", "familia"]):
        return "nino"

    return "bien"


# =========================
# GET NEXT MISSION (SEQUENTIAL LOOP)
# =========================
def get_next_mission():
    global ENGINE_STATE

    mission = MISSIONS[ENGINE_STATE["current_index"]]

    ENGINE_STATE["current_index"] += 1

    # LOOP RESET
    if ENGINE_STATE["current_index"] >= len(MISSIONS):
        ENGINE_STATE["current_index"] = 0

    return mission


# =========================
# TRANSLATE BLOCKS
# =========================
def translate_blocks(mission, lang):
    blocks = []

    for b in mission.get("b", []):
        block = dict(b)

        def pick(v):
            if isinstance(v, dict):
                return v.get(lang) or v.get("es")
            return v

        for k in ["tx", "story", "inf", "q"]:
            if k in block:
                block[k] = pick(block[k])

        if "op" in block:
            block["op"] = [
                o.get(lang) if isinstance(o, dict) else o
                for o in block["op"]
            ]

        blocks.append(block)

    return blocks


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return app.send_static_file("session.html")


# =========================
# MAIN ENGINE (NO RANDOM)
# =========================
@app.route("/safe-loop-engine", methods=["POST"])
def engine():

    data = request.json

    lang = data.get("idioma", "es")
    bolsillo = data.get("bolsillo", "cero")
    texto = data.get("texto_libre", "")
    puede_salir = data.get("puedes_salir", True)

    categoria = detectar_categoria(texto)

    mission = get_next_mission()

    blocks = translate_blocks(mission, lang)

    # =========================
    # OUTDOOR MODE
    # =========================
    if puede_salir:

        zip_code = data.get("zip_code", "33101")
        estado = data.get("estado", "FL")

        query = f"parks nature calm {zip_code} {estado}"
        map_url = "https://www.google.com/maps/search/" + query.replace(" ", "+")

        blocks.insert(0, {
            "t": "system",
            "tx": "Go to location and start sequence"
        })

        return jsonify({
            "mode": "outdoor",
            "mission_id": mission["id"],
            "title": f"MISSION {mission['id']}",
            "blocks": blocks,
            "map_url": map_url,
            "engine": {
                "mode": "sequential",
                "current_id": mission["id"]
            }
        })

    # =========================
    # INDOOR MODE
    # =========================
    return jsonify({
        "mode": "indoor",
        "mission_id": mission["id"],
        "title": f"MISSION {mission['id']}",
        "blocks": blocks,
        "engine": {
            "mode": "sequential",
            "current_id": mission["id"]
        }
    })


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

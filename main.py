import json
import random
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")


# ===============================
# LOAD MISSIONS (SAFE)
# ===============================
def load_all_missions():
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
        except Exception as e:
            print(f"[ERROR] {f}: {e}")

    return all_missions


ALL_MISSIONS = load_all_missions()


# ===============================
# DETECTOR SIMPLE
# ===============================
def detectar_categoria(texto: str):
    texto = (texto or "").lower()

    if any(k in texto for k in ["biles", "dinero", "deuda", "cuenta", "estrés", "problema", "mal"]):
        return "mal"

    if any(k in texto for k in ["niño", "hijo", "familia", "kids"]):
        return "nino"

    return "bien"


# ===============================
# FILTER MISSIONS (NO RANDOM LOGIC HERE)
# ===============================
def filtrar_misiones(categoria, bolsillo):
    return [
        m for m in ALL_MISSIONS
        if m.get("cat") == categoria
        and bolsillo in m.get("pocket_match", ["cero", "moderado", "libre"])
    ]


# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "session.html")


# ===============================
# API MAIN
# ===============================
@app.route("/diagnostico-kamizen", methods=["POST"])
def diagnostico_kamizen():

    data = request.get_json(force=True)

    idioma = data.get("idioma", "es")
    bolsillo = data.get("bolsillo", "cero")
    texto = data.get("texto_libre", "")
    puede_salir = data.get("puedes_salir", True)

    estado = (data.get("estado", "FL") or "FL").strip()
    zip_code = (data.get("zip_code", "33101") or "33101").strip()

    categoria = detectar_categoria(texto)

    missions = filtrar_misiones(categoria, bolsillo)

    if not missions:
        return jsonify({"error": "NO_MISSIONS_AVAILABLE"})

    # ===============================
    # SELECCIÓN SIMPLE (ENGINE MANDA EL LOOP)
    # ===============================
    mission = random.choice(missions)

    bloques = mission.get("b", [])

    # ===============================
    # TRANSLATE SAFE ONLY
    # ===============================
    processed = []

    for b in bloques:
        block = dict(b)

        # translate dict fields
        for key in ["tx", "inf", "story"]:
            if isinstance(block.get(key), dict):
                block[key] = block[key].get(idioma, block[key].get("es", ""))

        # question
        if isinstance(block.get("q"), dict):
            block["q"] = block["q"].get(idioma, block["q"].get("es", ""))

        # options
        if isinstance(block.get("op"), list):
            new_ops = []
            for op in block["op"]:
                if isinstance(op, dict):
                    new_ops.append(op.get(idioma, op.get("es", "")))
                else:
                    new_ops.append(op)
            block["op"] = new_ops

        # explanations
        if isinstance(block.get("ex"), list):
            new_ex = []
            for ex in block["ex"]:
                if isinstance(ex, dict):
                    new_ex.append(ex.get(idioma, ex.get("es", "")))
                else:
                    new_ex.append(ex)
            block["ex"] = new_ex

        processed.append(block)

    # ===============================
    # MAP LOGIC SIMPLE (NO PARK LOCK)
    # ===============================
    tipo = "parks"

    if categoria == "nino":
        tipo = "parks+playgrounds"
    elif categoria == "mal":
        tipo = "quiet+nature+safe+areas"

    query = f"{tipo} {zip_code} {estado} USA"
    url_maps = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    # ===============================
    # MODE RESPONSE
    # ===============================
    if not puede_salir:
        return jsonify({
            "modalidad": "indoor",
            "titulo": "Modo Interior",
            "lugar": "Espacio personal",
            "bloques_interactivos": processed,
            "url_maps": None
        })

    return jsonify({
        "modalidad": "outdoor",
        "titulo": "Active Escape Plan",
        "lugar": f"Zona activa en {zip_code}, {estado}",
        "bloques_interactivos": processed,
        "url_maps": url_maps
    })


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

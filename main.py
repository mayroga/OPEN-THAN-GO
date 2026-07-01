import json
import random
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===============================
# MEMORY SAFE SESSION STORE (NO PII)
# ===============================
SESSION_MEMORY = {}
LOOP_DURATION = 600  # 10 minutos exactos


# ===============================
# LOAD MISSIONS
# ===============================
def cargar_todas_misiones():
    archivos = [
        "missions_01_07.json",
        "missions_08_14.json",
        "missions_15_21.json"
    ]

    misiones = []

    for file in archivos:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                misiones.extend(data.get("missions", []))
        except Exception as e:
            print(f"[ERROR] {file}: {e}")

    return misiones


ALL_MISSIONS = cargar_todas_misiones()


# ===============================
# EMOTIONAL DETECTOR
# ===============================
def detectar_categoria(texto):
    texto = texto.lower()

    if any(x in texto for x in ["deuda", "biles", "dinero", "estrés", "problema", "mal"]):
        return "mal"

    if any(x in texto for x in ["niño", "hijo", "familia"]):
        return "nino"

    if any(x in texto for x in ["solo", "triste", "vacío", "aburrido"]):
        return "bien"

    return "bien"


# ===============================
# SESSION MANAGER SAFE LOOP
# ===============================
def get_session(session_id):
    now = time.time()

    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "start": now,
            "used": set()
        }

    session = SESSION_MEMORY[session_id]

    # RESET AUTOMÁTICO 10 MIN
    if now - session["start"] > LOOP_DURATION:
        session["start"] = now
        session["used"] = set()

    return session


# ===============================
# FILTER MISSIONS
# ===============================
def get_mission(categoria, bolsillo, used_set):
    pool = [
        m for m in ALL_MISSIONS
        if m.get("cat") == categoria
        and bolsillo in m.get("pocket_match", [])
        and m.get("id") not in used_set
    ]

    if not pool:
        pool = [m for m in ALL_MISSIONS if m.get("id") not in used_set]

    if not pool:
        return None

    mission = random.choice(pool)
    return mission


# ===============================
# TRANSLATION ENGINE
# ===============================
def traducir_bloques(mision, idioma):
    bloques = []

    for b in mision.get("b", []):
        bloque = json.loads(json.dumps(b))  # deep copy seguro

        def tr(x):
            if isinstance(x, dict):
                return x.get(idioma, x.get("es", ""))
            return x

        for key in ["tx", "inf", "story"]:
            if key in bloque:
                bloque[key] = tr(bloque[key])

        if bloque.get("t") == "d":
            if isinstance(bloque.get("q"), dict):
                bloque["q"] = tr(bloque["q"])

            if "op" in bloque:
                bloque["op"] = [
                    op.get(idioma, op.get("es", "")) if isinstance(op, dict) else op
                    for op in bloque["op"]
                ]

            if "ex" in bloque:
                bloque["ex"] = [
                    ex.get(idioma, ex.get("es", "")) if isinstance(ex, dict) else ex
                    for ex in bloque["ex"]
                ]

        bloques.append(bloque)

    return bloques


# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    return jsonify({
        "status": "SAFE LOOP ENGINE v1 ACTIVE",
        "loop_duration_seconds": LOOP_DURATION
    })


# ===============================
# MAIN ENGINE ENDPOINT
# ===============================
@app.route("/diagnostico-kamizen", methods=["POST"])
def diagnostico():

    data = request.json

    session_id = data.get("session_id", str(random.randint(100000, 999999)))
    idioma = data.get("idioma", "es")
    bolsillo = data.get("bolsillo", "cero")
    texto = data.get("texto_libre", "")
    puedes_salir = data.get("puedes_salir", True)

    categoria = detectar_categoria(texto)

    session = get_session(session_id)

    mission = get_mission(categoria, bolsillo, session["used"])

    if not mission:
        return jsonify({
            "error": "No missions available"
        })

    session["used"].add(mission["id"])

    bloques = traducir_bloques(mission, idioma)

    # ===============================
    # OUTDOOR MODE
    # ===============================
    if puedes_salir:

        zip_code = str(data.get("zip_code", "33101"))
        estado = str(data.get("estado", "FL"))

        tipo = "parks"

        if categoria == "nino":
            tipo = "parks+playgrounds+family"
        elif categoria == "mal":
            tipo = "quiet+nature+parks"

        query = f"{tipo} {zip_code} {estado} USA"
        url_maps = "https://www.google.com/maps/search/" + query.replace(" ", "+")

        bloques.insert(0, {
            "t": "h",
            "tx": f"Go to {zip_code}. Start your 10-minute reset loop when you arrive."
        })

        return jsonify({
            "mode": "outdoor",
            "session_id": session_id,
            "title": "Active Escape Plan",
            "location": f"{zip_code}, {estado}",
            "loop_seconds": LOOP_DURATION,
            "bloques": bloques,
            "maps": url_maps,
            "reset_in": max(0, LOOP_DURATION - (time.time() - session["start"]))
        })

    # ===============================
    # INDOOR MODE
    # ===============================
    return jsonify({
        "mode": "indoor",
        "session_id": session_id,
        "title": "Indoor Reset Mode",
        "loop_seconds": LOOP_DURATION,
        "bloques": bloques,
        "reset_in": max(0, LOOP_DURATION - (time.time() - session["start"]))
    })


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

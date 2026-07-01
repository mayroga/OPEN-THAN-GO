import json
import random
import time
from fastapi import FastAPI
app = FastAPI()
# ===============================
# LOOP CONFIG
# ===============================
LOOP_DURATION = 600  # 10 minutos exactos
SESSION_MEMORY = {}


# ===============================
# LOAD MISSIONS ONCE (EVITA FREEZES)
# ===============================
def cargar_misiones():
    archivos = [
        "missions_01_07.json",
        "missions_08_14.json",
        "missions_15_21.json"
    ]

    data_total = []

    for file in archivos:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                data_total.extend(data.get("missions", []))
        except Exception as e:
            print(f"[ERROR] {file}: {e}")

    return data_total


ALL_MISSIONS = cargar_misiones()


# ===============================
# DETECTOR EMOCIONAL
# ===============================
def detectar_categoria(texto):
    texto = texto.lower()

    if any(x in texto for x in ["deuda", "dinero", "biles", "estrés", "problema", "mal"]):
        return "mal"

    if any(x in texto for x in ["niño", "hijo", "familia"]):
        return "nino"

    return "bien"


# ===============================
# SESSION SAFE LOOP
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
# GET RANDOM MISSION SIN REPETIR
# ===============================
def get_mission(categoria, bolsillo, used):
    pool = [
        m for m in ALL_MISSIONS
        if m.get("cat") == categoria
        and bolsillo in m.get("pocket_match", [])
        and m.get("id") not in used
    ]

    if not pool:
        pool = [m for m in ALL_MISSIONS if m.get("id") not in used]

    if not pool:
        return None

    return random.choice(pool)


# ===============================
# TRADUCCIÓN SEGURA TVID
# ===============================
def traducir(mision, idioma):
    bloques = []

    for b in mision.get("b", []):

        bloque = json.loads(json.dumps(b))

        def t(x):
            if isinstance(x, dict):
                return x.get(idioma, x.get("es", ""))
            return x

        for k in ["tx", "inf", "story"]:
            if k in bloque:
                bloque[k] = t(bloque[k])

        if bloque.get("t") == "d":
            if isinstance(bloque.get("q"), dict):
                bloque["q"] = t(bloque["q"])

            if "op" in bloque:
                bloque["op"] = [
                    o.get(idioma, o.get("es", "")) if isinstance(o, dict) else o
                    for o in bloque["op"]
                ]

            if "ex" in bloque:
                bloque["ex"] = [
                    e.get(idioma, e.get("es", "")) if isinstance(e, dict) else e
                    for e in bloque["ex"]
                ]

        bloques.append(bloque)

    return bloques


# ===============================
# ROOT → FRONTEND (ESTO ERA EL ERROR)
# ===============================
@app.route("/")
def home():
    return app.send_static_file("session.html")


# ===============================
# ENGINE ENDPOINT
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
        return jsonify({"error": "No missions available"})

    session["used"].add(mission["id"])

    bloques = traducir(mission, idioma)

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

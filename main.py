import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===============================
# CONFIG
# ===============================
MAX_STEPS = 27

# memoria simple en RAM (puedes migrar luego a Redis)
SESSIONS = {}


# ===============================
# EMOTION DETECTOR
# ===============================
def detectar_emocion(texto: str) -> str:
    texto = (texto or "").lower()

    if any(x in texto for x in ["dinero", "deuda", "biles", "cuenta", "trabajo"]):
        return "mal"

    if any(x in texto for x in ["familia", "hijo", "niño", "pareja"]):
        return "conexion"

    if any(x in texto for x in ["solo", "triste", "vacío", "aburrido"]):
        return "bien"

    return "bien"


# ===============================
# SESSION HANDLER
# ===============================
def get_session(session_id):
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "step": 1,
            "emotion": "bien"
        }
    return SESSIONS[session_id]


def clamp_step(step):
    if step > MAX_STEPS:
        return 1
    if step < 1:
        return MAX_STEPS
    return step


# ===============================
# EMOTION-BASED JUMP SYSTEM
# ===============================
def emotion_jump(step, emotion):
    """
    Saltos inteligentes sin romper el loop 1–27
    """
    if emotion == "mal":
        return step + 2
    if emotion == "conexion":
        return step + 1
    return step + 1


# ===============================
# MAIN ENGINE ENDPOINT
# ===============================
@app.route('/safe-loop', methods=['POST'])
def safe_loop():

    data = request.json or {}

    session_id = data.get("session_id") or str(uuid.uuid4())
    texto = data.get("texto_libre", "")
    action = data.get("action", "next")  # next | back | skip

    state = get_session(session_id)

    # ===============================
    # UPDATE EMOTION
    # ===============================
    emotion = detectar_emocion(texto)
    state["emotion"] = emotion

    # ===============================
    # STEP CONTROL
    # ===============================
    if action == "next":
        state["step"] += 1

    elif action == "back":
        state["step"] -= 1

    elif action == "skip":
        state["step"] = emotion_jump(state["step"], emotion)

    # wrap loop
    state["step"] = clamp_step(state["step"])

    # ===============================
    # LOAD MISSION (TVID SYSTEM)
    # ===============================
    mission = {
        "id": state["step"],
        "title": f"MISIÓN {state['step']}",
        "emotion": emotion,

        # sincronizado con engine.js
        "loop_duration_seconds": 600,

        "breathing": {
            "inhale": 4,
            "hold": 2,
            "exhale": 6
        },

        "instruction": build_instruction(state["step"], emotion),

        "allow_back": True,
        "allow_skip": True
    }

    return jsonify({
        "session_id": session_id,
        "state": state,
        "mission": mission,
        "max_steps": MAX_STEPS
    })


# ===============================
# TVID INSTRUCTION MAPPER
# (aquí conectas tus JSON reales después)
# ===============================
def build_instruction(step, emotion):

    base = {
        "es": {
            "mal": "Respira y enfócate en resolver un paso pequeño hoy.",
            "bien": "Observa tu estado y mantén equilibrio interno.",
            "conexion": "Conecta con alguien importante hoy."
        },
        "en": {
            "mal": "Breathe and focus on solving one small step today.",
            "bien": "Observe your state and maintain internal balance.",
            "conexion": "Connect with someone important today."
        }
    }

    if emotion == "mal":
        return base["es"]["mal"]

    if emotion == "conexion":
        return base["es"]["conexion"]

    return base["es"]["bien"]


# ===============================
# HEALTH CHECK
# ===============================
@app.route('/')
def home():
    return jsonify({
        "status": "SAFE LOOP ENGINE ACTIVE",
        "steps": f"1-{MAX_STEPS}",
        "mode": "sequential + emotional jumps"
    })


# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

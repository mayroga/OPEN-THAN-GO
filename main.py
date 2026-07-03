from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="static")

# Misiones base para el protocolo de alivio
MISIONES_CASA = [
    {
        "titulo": {"es": "REORDENAR TU ENTORNO", "en": "REORDER YOUR ENVIRONMENT"},
        "descripcion": {"es": "Dedica 10 minutos a ordenar un espacio físico. Tu entorno exterior refleja tu interior.", "en": "Spend 10 minutes tidying a physical space. Your outer environment reflects your inner state."}
    },
    {
        "titulo": {"es": "RESPIRACIÓN CONSCIENTE", "en": "CONSCIOUS BREATHING"},
        "descripcion": {"es": "Sigue el ciclo visual. Inhala calma, exhala pesadez. 10 minutos para reiniciar tu sistema.", "en": "Follow the visual cycle. Inhale calm, exhale heaviness. 10 minutes to reset your system."}
    }
]

def obtener_opciones_salida(zip_code, presupuesto):
    # Lógica de resolución de destinos basada en proximidad y economía
    return [
        {"nombre": "Parque local (Entorno Natural)", "gps": f"https://www.google.com/maps/search/?api=1&query=parks+near+{zip_code}"},
        {"nombre": "Centro de recreación (Ambiente Social)", "gps": f"https://www.google.com/maps/search/?api=1&query=recreation+centers+near+{zip_code}"},
        {"nombre": "Espacio público de interés", "gps": f"https://www.google.com/maps/search/?api=1&query=public+spaces+near+{zip_code}"}
    ]

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "session.html")

@app.route("/api/open-than-go", methods=["POST"])
def open_than_go():
    try:
        data = request.get_json() or {}
        decision = data.get("decision", "salir")
        zip_code = data.get("zip_code", "33101")
        presupuesto = data.get("budget_level", "cero")
        
        if decision == "casa":
            # Protocolo de Eco-Terapia con Misión de 10 min
            return jsonify({
                "tipo": "Casa",
                "mision": MISIONES_CASA[0]
            })
        else:
            # Protocolo de Acción Exterior
            opciones = obtener_opciones_salida(zip_code, presupuesto)
            return jsonify({
                "tipo": "Salida",
                "opciones": opciones
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

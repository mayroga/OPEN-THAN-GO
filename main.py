# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder='static')

def cargar_mision_por_bloque(decision, pocket_tier):
    """Carga de forma inteligente la misión dividida en bloques de 7."""
    try:
        if decision == "casa":
            archivo = 'missions_01_07.json'
        else:
            archivo = random.choice(['missions_08_14.json', 'missions_15_21.json'])
            if not os.path.exists(archivo):
                archivo = 'missions_01_07.json'

        if not os.path.exists(archivo):
            # Fallback dinámico integrado para que la app NUNCA de error si el archivo no está
            return {
                "id": 1, "cat": "bien", "pocket_match": ["cero", "moderado", "libre"],
                "b": [{"story": {"es": "Sincronizando el sistema de misiones. Presiona continuar.", "en": "Synchronizing system missions. Press continue."}}]
            }

        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return random.choice(data.get('missions', []))
    except Exception as e:
        print(f"Error interno de misiones: {str(e)}")
        return None

@app.route('/')
def index():
    """Sirve session.html en la raíz para evitar fallas de carga en Render."""
    return send_from_directory(app.static_folder, 'session.html')

@app.route('/api/open-than-go', methods=['POST'])
def procesar_sistema_bienestar():
    # Evita que el servidor caiga si los datos llegan nulos
    data = request.json or {}
    decision = data.get('decision', 'salir')
    lang = data.get('lang', 'es')
    desahogo_usuario = data.get('desahogo', '').lower()
    pocket = data.get('budget_level', 'cero')
    zip_code = data.get('zip_code', '').strip()
    region = data.get('region', '').strip()
    estado = data.get('estado', 'FL').strip()

    mision_seleccionada = cargar_mision_por_bloque(decision, pocket)
    if not mision_seleccionada:
        return jsonify({"status": "error", "message": "Inicializando componentes de datos..."}), 500

    if decision == "casa":
        return jsonify({"status": "success", "tipo": "Casa", "mision": mision_seleccionada})

    # Generador elástico de Google Maps en vivo
    categorias_por_bolsillo = {
        "cero": ["parques naturales publicos", "playas publicas", "senderos para caminar"],
        "minimo": ["cafeterias economicas", "mercados locales"],
        "moderado": ["restaurantes familiares", "centros de diversion", "pistas de baile"],
        "libre": ["hoteles resorts", "discotecas club", "restaurantes premium"]
    }

    if any(p in desahogo_usuario for p in ["trabajo", "empleo", "compañia", "compañía", "job"]):
        termino_busqueda = "compañias agencias de trabajo y empleo"
    else:
        termino_busqueda = random.choice(categorias_por_bolsillo.get(pocket, ["parques"]))

    ubicacion_destino = zip_code if zip_code else f"{region} {estado}"
    query_mapa = f"{termino_busqueda} en {ubicacion_destino}".replace(" ", "+")
    link_google_maps_vivo = f"https://google.com{query_mapa}"

    return jsonify({
        "status": "success",
        "tipo": "Salida",
        "lugar": {
            "name": f"Exploración de {termino_busqueda.title()}",
            "address": f"📍 Cerca de tu área ({ubicacion_destino})",
            "gps_link": link_google_maps_vivo
        },
        "mision": mision_seleccionada
    })

# Inyección de cabeceras de seguridad CORS para evitar bloqueos de red en Render
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

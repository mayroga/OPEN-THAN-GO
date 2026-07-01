# OPEN THAN GO SYSTEM - Live Maps Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder='static')

def cargar_mision_por_bloque(decision, pocket_tier):
    """Carga la misión adecuada dividida en bloques de 7 de tus archivos JSON."""
    try:
        if decision == "casa":
            if not os.path.exists('missions_01_07.json'):
                return {"id": 1, "cat": "bien", "b": [{"story": {"es": "Falta el archivo missions_01_07.json.", "en": "Missing missions_01_07.json."}}]}
            with open('missions_01_07.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return random.choice(data['missions'])
        else:
            archivo_elegido = random.choice(['missions_08_14.json', 'missions_15_21.json'])
            if not os.path.exists(archivo_elegido):
                archivo_elegido = 'missions_01_07.json'
            with open(archivo_elegido, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return random.choice(data['missions'])
    except Exception as e:
        print(f"Error en misiones: {str(e)}")
        return None

@app.route('/')
def index():
    """Sirve la pantalla principal de la aplicación."""
    return send_from_directory(app.static_folder, 'session.html')

@app.route('/api/open-than-go', methods=['POST'])
def procesar_sistema_bienestar():
    data = request.json or {}
    decision = data.get('decision') 
    
    # MODALIDAD EN CASA
    if decision == "casa":
        mision_casa = cargar_mision_por_bloque("casa", "cero")
        return jsonify({"status": "success", "tipo": "Casa", "mision": mision_casa})
        
    # MODALIDAD SALIR (Mapeo Biosocial Automático en Vivo)
    zip_code = data.get('zip_code', '').strip()
    region = data.get('region', '').strip()
    estado = data.get('estado', 'FL').strip()
    pocket = data.get('budget_level', 'cero') 

    # Definición de categorías terapéuticas de escape según el bolsillo del cliente
    categorias_por_bolsillo = {
        "cero": ["parques naturales públicos", "playas públicas", "senderos para caminar", "miradores gratis"],
        "minimo": ["cafeterías económicas", "mercados locales al aire libre", "zonas de recreación comunitarias"],
        "moderado": ["restaurantes familiares", "centros de diversión", "pistas de baile", "centros de recreación recreativa"],
        "libre": ["hoteles resorts", "discotecas club", "restaurantes premium", "atracciones turísticas de entretenimiento"]
    }
    
    # Si el cliente menciona "trabajo" o "compañía" en su desahogo, el mapa busca oportunidades de empleo cercanas
    desahogo_usuario = data.get('desahogo', '').lower()
    if "trabajo" in desahogo_usuario or "empleo" in desahogo_usuario or "compañia" in desahogo_usuario:
        termino_busqueda = "compañias agencias de trabajo y empleo"
    else:
        # Si no, elige al azar una categoría divertida/relajante alineada a su billetera
        termino_busqueda = random.choice(categorias_por_bolsillo.get(pocket, ["parques"]))

    # Construir el punto geográfico de partida
    ubicacion_destino = zip_code if zip_code else f"{region} {estado}"
    
    # Crear la URL de búsqueda masiva en vivo de Google Maps
    # Formato oficial: https://google.com
    query_mapa = f"{termino_busqueda} en {ubicacion_destino}".replace(" ", "+")
    link_google_maps_vivo = f"https://google.com{query_mapa}"
    
    mision_salida = cargar_mision_por_bloque("salir", pocket)
    
    return jsonify({
        "status": "success",
        "tipo": "Salida",
        "lugar": {
            "name": f"Exploración de {termino_busqueda.title()}",
            "address": f"Cerca de tu ubicación ({ubicacion_destino})",
            "region": region,
            "gps_link": link_google_maps_vivo
        },
        "mision": mision_salida
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

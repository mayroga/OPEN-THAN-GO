# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__, static_folder='static')
CORS(app)

def cargar_mision_especifica(decision, pocket_tier):
    """Carga la misión adecuada respetando la división exacta de bloques de 7."""
    try:
        if decision == "casa":
            archivo = 'missions_01_07.json'
        else:
            archivo = random.choice(['missions_08_14.json', 'missions_15_21.json'])
            
        if not os.path.exists(archivo):
            archivo = 'missions_01_07.json'
            
        if not os.path.exists(archivo):
            return {
                "id": 1,
                "cat": "bien",
                "pocket_match": ["cero", "minimo", "moderado", "libre"],
                "b": [
                    {"t": "v", "tx": {"es": "SISTEMA OPEN THAN GO ACTIVADO", "en": "OPEN THAN GO SYSTEM ACTIVATED"}},
                    {"story": {"es": "Sincronizando frecuencias emocionales. Presiona continuar.", "en": "Synchronizing emotional frequencies. Press continue."}}
                ]
            }

        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        misiones = data.get('missions', [])
        if not misiones:
            return None

        filtradas = [m for m in misiones if pocket_tier in m.get('pocket_match', ["cero", "minimo", "moderado", "libre"])]
        if filtradas:
            return random.choice(filtradas)
        return random.choice(misiones)
        
    except Exception as e:
        print(f"Error crítico en catálogo de misiones: {str(e)}")
        return None

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'session.html')

@app.route('/api/open-than-go', methods=['POST'])
def procesar_sistema_bienestar():
    data = request.json or {}
    decision = data.get('decision', 'salir')
    lang = data.get('lang', 'es')
    desahogo_usuario = data.get('desahogo', '').lower()
    pocket = data.get('budget_level', 'cero')
    zip_code = data.get('zip_code', '').strip()
    estado = data.get('estado', 'FL').strip()
    region = data.get('region', '').strip()

    mision_seleccionada = cargar_mision_especifica(decision, pocket)
    if not mision_seleccionada:
        return jsonify({"status": "error", "message": "Inicializando bases de datos biosociales..."}), 500

    bloques_processed = []
    for comando in mision_seleccionada.get("b", []):
        bloque_clon = comando.copy()
        for campo in ["tx", "inf", "story", "c"]:
            if campo in bloque_clon and isinstance(bloque_clon[campo], dict):
                bloque_clon[campo] = bloque_clon[campo].get(lang, bloque_clon[campo].get('es', ''))
                
        if bloque_clon.get("t") == "d":
            if isinstance(bloque_clon.get("q"), dict):
                bloque_clon["q"] = bloque_clon["q"].get(lang, bloque_clon["q"].get('es', ''))
            if "op" in bloque_clon:
                bloque_clon["op"] = [op.get(lang, op.get('es', '')) if isinstance(op, dict) else op for op in bloque_clon["op"]]
            if "ex" in bloque_clon:
                bloque_clon["ex"] = [ex.get(lang, ex.get('es', '')) if isinstance(ex, dict) else ex for ex in bloque_clon["ex"]]
                
        bloques_processed.append(bloque_clon)

    mision_final = mision_seleccionada.copy()
    mision_final["b"] = bloques_processed

    if decision == "casa":
        return jsonify({"status": "success", "tipo": "Casa", "mision": mision_final})

    categorias_por_bolsillo = {
        "cero": {
            "busqueda": "parques naturales publicos y playas gratis",
            "sugerencias": {
                "es": "1. El área verde central para desconectar. 2. El sendero abierto para activación corporal. 3. Zonas de descanso frente al paisaje.",
                "en": "1. The central green area to disconnect. 2. The open trail for bodily activation. 3. Rest zones facing the landscape."
            }
        },
        "minimo": {
            "busqueda": "cafeterias economicas y mercados locales comunitarios",
            "sugerencias": {
                "es": "1. El rincón de lectura local. 2. Puestos artesanales exteriores. 3. Barra de café económico.",
                "en": "1. The local reading corner. 2. Outdoor artisan stands. 3. Low-cost coffee bar area."
            }
        },
        "moderado": {
            "busqueda": "restaurantes familiares y centros de diversion con pistas de baile",
            "sugerencias": {
                "es": "1. La pista central de movimiento rítmico. 2. Mesas de integración social. 3. Espacio recreativo familiar.",
                "en": "1. The central rhythmic movement floor. 2. Social integration tables. 3. Family recreational space."
            }
        },
        "libre": {
            "busqueda": "hoteles resorts discotecas club y entretenimiento de lujo",
            "sugerencias": {
                "es": "1. El lounge de relajación premium. 2. Pista de baile de alta energía. 3. Entorno de terraza de escape.",
                "en": "1. The premium relaxation lounge. 2. High-energy dance floor. 3. Terrace escape environment."
            }
        }
    }

    palabras_urgentes = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills"]
    if any(p in desahogo_usuario for p in palabras_urgentes):
        termino_busqueda = "compañias de empleo agencias de trabajo staffings"
        explicacion_sugerencias = {
            "es": "1. Módulo de reclutamiento rápido. 2. Orientación de vacantes disponibles. 3. Agencias de contratación inmediata para solucionar el agobio financiero.",
            "en": "1. Fast recruitment desk. 2. Available openings orientation. 3. Immediate hiring agencies to solve financial stress."
        }
    else:
        config_actual = categorias_por_bolsillo.get(pocket, categorias_por_bolsillo["cero"])
        termino_busqueda = config_actual["busqueda"]
        explicacion_sugerencias = config_actual["sugerencias"]

    ubicacion_destino = zip_code if zip_code else f"{region} {estado}"
    
    from urllib.parse import quote_plus
    query_mapa = quote_plus(f"{termino_busqueda} en {ubicacion_destino}")
    
    # CORRECCIÓN DE LA URL DEL GPS MÓVIL:
    link_google_maps_vivo = f"https://google.com{query_mapa}"

    return jsonify({
        "status": "success",
        "tipo": "Salida",
        "lugar": {
            "name": f"Escape enfocado en {termino_busqueda.upper()}",
            "address": f"📍 Área de Cobertura: {ubicacion_destino}, USA.",
            "gps_link": link_google_maps_vivo,
            "analisis_sugerido": explicacion_sugerencias[lang]
        },
        "mision": mision_final
    })

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

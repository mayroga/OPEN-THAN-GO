# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder='static')

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
                "id": 1, "cat": "bien", "pocket_match": ["cero", "moderado", "libre"],
                "b": [
                    {"t": "v", "tx": {"es": "SISTEMA OPEN THAN GO ACTIVADO", "en": "OPEN THAN GO SYSTEM ACTIVATED"}},
                    {"story": {"es": "Sincronizando tus vectores de escape emocionales. Presiona continuar.", "en": "Synchronizing your emotional escape vectors. Please press continue."}},
                    {"t": "breath_auto", "d": 25, "tx": {"es": "Sincroniza tu respiración con el pulso", "en": "Synchronize your breathing with the pulse"}, "inf": {"es": "Regulación biológica.", "en": "Biological regulation."}}
                ]
            }

        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        misiones = data.get('missions', [])
        if not misiones:
            return None

        if decision == "salir":
            filtradas = [m for m in misiones if pocket_tier in m.get('pocket_match', [])]
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

    # Corrección de llamada interna del cerebro de datos
    mision_seleccionada = cargar_mision_especifica(decision, pocket)
    if not mision_seleccionada:
        return jsonify({"status": "error", "message": "Inicializando bases de datos biosociales..."}), 500

    if decision == "casa":
        return jsonify({"status": "success", "tipo": "Casa", "mision": mision_seleccionada})

    # Escapes de recreación biosocial por billetera
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

    # FILTRO DE SUPERVIVENCIA: Cambia la ruta a agencias corporativas de empleo inmediato
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
    query_mapa = f"{termino_busqueda} en {ubicacion_destino}".replace(" ", "+")
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
        "mision": mision_seleccionada
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

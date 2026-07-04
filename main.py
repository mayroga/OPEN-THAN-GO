# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import os
import re
from urllib.parse import quote_plus

app = Flask(__name__, static_folder='static')
CORS(app)  # Opens network gates to prevent mobile app freezing

def cargar_mision_especifica(decision, pocket_tier, force_id=None):
    """Carga la misión adecuada respetando el orden lineal estricto sin repetición."""
    try:
        # If frontend requests a strict linear ID via LocalStorage
        if force_id is not None:
            fid = int(force_id)
            if 1 <= fid <= 7:
                archivo = 'missions_01_07.json'
            elif 8 <= fid <= 14:
                archivo = 'missions_08_14.json'
            else:
                archivo = 'missions_15_21.json'
        else:
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

        # If strict linear forcing is active, pull exactly that mission ID
        if force_id is not None:
            for m in misiones:
                if int(m.get('id', 0)) == int(force_id):
                    return m

        # Secondary budget fallback filter
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
    desahogo_usuario = data.get('desahogo', '').strip()
    pocket = data.get('budget_level', 'cero')
    zip_code = data.get('zip_code', '').strip()
    estado = data.get('estado', 'FL').strip()
    region = data.get('region', '').strip()
    force_id = data.get('force_id')

    mision_seleccionada = cargar_mision_especifica(decision, pocket, force_id)
    if not mision_seleccionada:
        return jsonify({"status": "error", "message": "Inicializando bases de datos biosociales..."}), 500

    # Kamizen Mirror Engine - Bilingual Mirror Formatter
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

    # =========================================================================
    # MOTOR DE EXTRACCIÓN GEOGRÁFICA UNIVERSAL (PRIORIDAD DE DESEO)
    # =========================================================================
    destino_detectado = None
    desahogo_min = desahogo_usuario.lower()
    
    # Capture movement intent text inside the free venting area
    patrones_viaje = [
        r'(?:ir\s+a|ir\s+hacia|viajar\s+a|en|visitar|ir\s+to|travel\s+to|visit|go\s+to)\s+([a-zA-Z\s]{3,30})'
    ]
    
    for patron in patrones_viaje:
        coincidencia = re.search(patron, desahogo_min)
        if coincidencia:
            posible_destino = coincidencia.group(1).strip()
            # Clean connecting noise words
            palabras_ruido = ["un", "una", "el", "la", "los", "mis", "mis\s+hijos", "familia", "family", "today", "hoy"]
            for ruido in palabras_ruido:
                posible_destino = re.sub(r'\b' + ruido + r'\b', '', posible_destino).strip()
            
            if len(posible_destino) > 2:
                destino_detectado = posible_destino.title()
                break

    # Direct fallback keyword check for frequent cities/countries
    if not destino_detectado:
        ciudades_frecuentes = ["hong kong", "orlando", "tampa", "lehigh acres", "miami", "paris", "new york", "los angeles", "houston", "las vegas", "london", "madrid", "colombia", "bogota", "medellin", "cali", "cartagena"]
        for ciudad in ciudades_frecuentes:
            if ciudad in desahogo_min:
                destino_detectado = ciudad.title()
                break

    # Domestic USA budget criteria mapping
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

    # Domestic USA urgent staffing query mapping
    palabras_urgentes = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills"]
    if any(p in desahogo_min for p in palabras_urgentes):
        termino_busqueda = "compañias de empleo agencias de trabajo staffings"
        explicacion_sugerencias = {
            "es": "1. Módulo de reclutamiento rápido. 2. Orientación de vacantes disponibles. 3. Agencias de contratación inmediata para solucionar el agobio financiero.",
            "en": "1. Fast recruitment desk. 2. Available openings orientation. 3. Immediate hiring agencies to solve financial stress."
        }
    else:
        config_actual = categorias_por_bolsillo.get(pocket, categorias_por_bolsillo["cero"])
        termino_busqueda = config_actual["busqueda"]
        explicacion_sugerencias = config_actual["sugerencias"]

    # =========================================================================
    # VERIFICADOR DE FRONTERA NACIONAL (USA VS INTERNACIONAL)
    # =========================================================================
    fuera_usa_detectado = False
    if destino_detectado:
        ubicacion_destino = destino_detectado
        if not any(x in destino_detectado.lower() for x in ["usa", "fl", "florida", "tx", "texas", "ca", "california", "ny", "new york"]):
            if not any(x in destino_detectado.lower() for x in ["miami", "orlando", "tampa", "houston", "los angeles", "las vegas"]):
                fuera_usa_detectado = True
    else:
        ubicacion_destino = zip_code if zip_code else f"{region} {estado}"
    
    # =========================================================================
    # MOTOR DE GENERACIÓN DE RUTA INTELIGENTE (USA VS GLOBAL SEGURA)
    # =========================================================================
    if fuera_usa_detectado:
        # INTERNATIONAL ACCELERATOR: Suggests exactly 3 top iconic, secure & entertaining destinations
        if "colombia" in ubicacion_destino.lower():
            destinos_sugeridos = "Bogota, Medellin y Cartagena"
                else:
            destinos_sugeridos = f"sitios turisticos principales de {ubicacion_destino}"
            
        query_mapa = quote_plus(f"atracciones turismo en {destinos_sugeridos}")
        nombre_lugar = f"Escape Internacional: {ubicacion_destino.upper()}"
        explicacion_sugerencias[lang] = (
            f"1. Visitar la capital y sus museos históricos. "
            f"2. Explorar zonas urbanas de innovación y flores. "
            f"3. Recorrer la ciudad amurallada frente al mar."
            if lang == "es" else
            f"1. Visit the capital and its historical museums. "
            f"2. Explore urban innovation and flower zones. "
            f"3. Tour the walled city by the sea."
        )
    else:
        # DOMESTIC USA: Normal operation based strictly on ZIP Code/Region, pocket tiers or staffings
        query_mapa = quote_plus(f"{termino_busqueda} en {ubicacion_destino}")
        nombre_lugar = f"Escape enfocado en {termino_busqueda.upper()}"
        
    # OFFICIAL INDESTRUCTIBLE GPS MAPS API URL:
    link_google_maps_vivo = f"https://google.com{query_mapa}"

    return jsonify({
        "status": "success",
        "tipo": "Salida",
        "fuera_usa": fuera_usa_detectado,  # Signals the frontend to play the custom international voice prompt
        "lugar": {
            "name": nombre_lugar,
            "address": f"📍 Área de Cobertura: {ubicacion_destino}.",
            "gps_link": link_google_maps_vivo,
            "analisis_sugerido": explicacion_sugerencias[lang]
        },
        "mision": mision_final
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

# Inicializamos Flask apuntando a la carpeta de archivos estáticos
app = Flask(__name__, static_folder='static')

def cargar_mision_por_bloque(decision, pocket_tier):
    """
    Carga de forma inteligente la misión dividida en bloques de 7.
    - Opción Casa: Extrae del Bloque 1 (Misiones 1-7).
    - Opción Salir: Alterna al azar entre el Bloque 2 (8-14) o el Bloque 3 (15-21).
    """
    try:
        if decision == "casa":
            if not os.path.exists('missions_01_07.json'):
                return {
                    "id": 1, "cat": "bien", 
                    "b": [{"story": {"es": "Falta el archivo missions_01_07.json en el servidor.", "en": "Missing missions_01_07.json file."}}]
                }
            with open('missions_01_07.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return random.choice(data['missions'])
        
        else:
            # Alternar aleatoriamente entre los bloques de salida para romper la monotonía
            archivo_elegido = random.choice(['missions_08_14.json', 'missions_15_21.json'])
            
            # Fallback de seguridad por si algún archivo no está arriba en el servidor
            if not os.path.exists(archivo_elegido):
                archivo_elegido = 'missions_01_07.json'
                
            if not os.path.exists(archivo_elegido):
                return {
                    "id": 1, "cat": "bien", 
                    "b": [{"story": {"es": "Sube tus archivos de misiones (.json) a GitHub.", "en": "Upload your mission files (.json) to GitHub."}}]
                }
                
            with open(archivo_elegido, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Filtra las misiones que coincidan con la etiqueta económica seleccionada
            misiones_filtradas = [
                m for m in data['missions'] 
                if pocket_tier in m.get('pocket_match', [])
            ]
            
            # Si no hay match de presupuesto estricto, devolvemos una del bloque al azar para no congelar la app
            return random.choice(misiones_filtradas) if misiones_filtradas else random.choice(data['missions'])
            
    except Exception as e:
        print(f"Error cargando los bloques de misiones: {str(e)}")
        return None

# ----------------------------------------------------
# ENRUTAMIENTO DE INTERFAZ Y API BIOSOCIAL
# ----------------------------------------------------

@app.route('/')
def index():
    """Ruta raíz obligatoria para servir tu session.html en la nube de Render."""
    return send_from_directory(app.static_folder, 'session.html')

@app.route('/api/open-than-go', methods=['POST'])
def procesar_sistema_bienestar():
    data = request.json or {}
    decision = data.get('decision') # "casa" o "salir"
    
    # 1. PROTOCOLO DOMÉSTICO (Terapia oculta de 10 min en Casa)
    if decision == "casa":
        mision_casa = cargar_mision_por_bloque("casa", "cero")
        if not mision_casa:
            return jsonify({"status": "error", "message": "Error interno en protocolo doméstico."}), 500
        return jsonify({
            "status": "success",
            "tipo": "Casa",
            "mision": mision_casa
        })
        
    # 2. PROTOCOLO DE EXPLORACIÓN (Salida Exterior con Mapas en Vivo)
    zip_code = data.get('zip_code', '').strip()
    region = data.get('region', '').strip()
    estado = data.get('estado', 'FL').strip()
    pocket = data.get('budget_level', 'cero') # cero, minimo, moderado, libre

    # Mapeo de búsqueda inteligente para la API de Google Maps en el celular
    categorias_por_bolsillo = {
        "cero": ["parques naturales publicos", "playas publicas", "senderos para caminar", "miradores gratis"],
        "minimo": ["cafeterias economicas", "mercados locales al aire libre", "zonas de recreacion comunitarias"],
        "moderado": ["restaurantes familiares", "centros de diversion", "pistas de baile", "centros recreativos"],
        "libre": ["hoteles resorts", "discotecas club", "restaurantes premium", "centros de entretenimiento"]
    }
    
    # Filtro Psicológico Avanzado: Si el usuario escribe que busca empleo, el mapa redirige a oportunidades
    desahogo_usuario = data.get('desahogo', '').lower()
    if any(palabra in desahogo_usuario for palabra in ["trabajo", "empleo", "compañia", "compañía"]):
        termino_busqueda = "compañias agencias de trabajo y empleo"
    else:
        # Si no, selecciona una categoría al azar según su dinero para aliviar el estrés
        termino_busqueda = random.choice(categorias_por_bolsillo.get(pocket, ["parques"]))

    # Establecer el anclaje geográfico base elástico
    ubicacion_destino = zip_code if zip_code else f"{region} {estado}"
    
    # Construcción limpia de la URL de búsqueda masiva nativa de Google Maps
    query_mapa = f"{termino_busqueda} en {ubicacion_destino}".replace(" ", "+")
    link_google_maps_vivo = f"https://google.com{query_mapa}"
    
    # Cargar bloques de misiones exteriores (Bloques 2 o 3: Misiones de la 8 a la 21)
    mision_salida = cargar_mision_por_bloque("salir", pocket)
    
    if not mision_salida:
        return jsonify({"status": "error", "message": "Error interno al procesar misión de salida."}), 500
        
    return jsonify({
        "status": "success",
        "tipo": "Salida",
        "lugar": {
            "name": f"Exploración de {termino_busqueda.title()}",
            "address": f"Cerca de tu área ({ubicacion_destino})",
            "region": region,
            "gps_link": link_google_maps_vivo
        },
        "mision": mision_salida
    })

if __name__ == '__main__':
    # Configuración de puerto dinámica requerida por la infraestructura de Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

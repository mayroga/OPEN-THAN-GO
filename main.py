# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify, send_from_directory
import json
import sqlite3
import random
import os

# Inicializamos Flask apuntando correctamente a la carpeta 'static'
app = Flask(__name__, static_folder='static')

# ----------------------------------------------------
# PROTOCOLOS DE SEGURIDAD AUTOMÁTICOS PARA RENDER
# ----------------------------------------------------
def verificar_infraestructura():
    """Garantiza que la base de datos y tablas existan antes de recibir tráfico."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            estado TEXT NOT NULL,
            region TEXT NOT NULL,
            budget_tier TEXT NOT NULL,  -- cero, minimo, moderado, libre
            gps_link TEXT NOT NULL
        )
    ''')
    
    # Insertar un lugar de prueba por defecto si la tabla está completamente vacía
    cursor.execute("SELECT COUNT(*) FROM destinations")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO destinations (name, address, zip_code, estado, region, budget_tier, gps_link)
            VALUES ('Parque Matheson Hammock', '9610 Old Cutler Rd, Coral Gables, FL 33156', '33156', 'FL', 'South Florida', 'cero', 'https://google.com')
        ''')
    conn.commit()
    conn.close()

def cargar_mision_por_bloque(decision, pocket_tier):
    """Carga y selecciona la misión adecuada dividida en bloques de 7."""
    try:
        if decision == "casa":
            if not os.path.exists('missions_01_07.json'):
                return {"id": 1, "cat": "bien", "b": [{"story": {"es": "Falta el archivo missions_01_07.json en el servidor.", "en": "Missing missions_01_07.json file."}}]}
            
            with open('missions_01_07.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return random.choice(data['missions'])
        
        else:
            archivo_elegido = random.choice(['missions_08_14.json', 'missions_15_21.json'])
            if not os.path.exists(archivo_elegido):
                archivo_elegido = 'missions_01_07.json'
                
            if not os.path.exists(archivo_elegido):
                return {"id": 1, "cat": "bien", "b": [{"story": {"es": "Sube tus archivos de misiones a GitHub.", "en": "Upload your mission files to GitHub."}}]}
                
            with open(archivo_elegido, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            misiones_filtradas = [
                m for m in data['missions'] 
                if pocket_tier in m.get('pocket_match', [])
            ]
            return random.choice(misiones_filtradas) if misiones_filtradas else random.choice(data['missions'])
            
    except Exception as e:
        print(f"Error cargando catálogo de misiones: {str(e)}")
        return None

# ----------------------------------------------------
# RUTAS DE NAVEGACIÓN Y API
# ----------------------------------------------------

@app.route('/')
def index():
    """Ruta raíz indispensable para que Render muestre tu HTML y no de Error 500."""
    return send_from_directory(app.static_folder, 'session.html')

@app.route('/api/open-than-go', methods=['POST'])
def procesar_sistema_bienestar():
    data = request.json or {}
    decision = data.get('decision') 
    lang = data.get('lang', 'es')   
    
    if decision == "casa":
        mision_casa = cargar_mision_por_bloque("casa", "cero")
        if not mision_casa:
            return jsonify({"status": "error", "message": "Error interno en protocolo doméstico."}), 500
        return jsonify({
            "status": "success",
            "tipo": "Casa",
            "mision": mision_casa
        })
        
    zip_code = data.get('zip_code', '')
    estado = data.get('estado', '')
    region = data.get('region', '')
    pocket = data.get('budget_level', 'cero') 
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Búsqueda elástica: valida coincidencia geográfica por bolsillo
        cursor.execute('''
            SELECT * FROM destinations 
            WHERE (zip_code = ? OR region = ? OR estado = ?) AND budget_tier = ?
        ''', (zip_code, region, estado, pocket))
        
        lugares_validos = cursor.fetchall()
        
        # Si no hay match exacto en la zona, traemos cualquier lugar del mismo presupuesto para no romper la UX
        if not lugares_validos:
            cursor.execute('SELECT * FROM destinations WHERE budget_tier = ?', (pocket,))
            lugares_validos = cursor.fetchall()
            
        if not lugares_validos:
            return jsonify({
                "status": "error", 
                "message": "Por favor inserta lugares en tu database.db para este nivel de presupuesto."
            }), 404
            
        lugar_seleccionado = random.choice(lugares_validos)
        mision_salida = cargar_mision_por_bloque("salir", pocket)
        
        if not mision_salida:
            return jsonify({"status": "error", "message": "Error interno al procesar misión de salida."}), 500
            
        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "lugar": {
                "name": lugar_seleccionado['name'],
                "address": lugar_seleccionado['address'],
                "region": lugar_seleccionado['region'],
                "gps_link": lugar_seleccionado['gps_link']
            },
            "mision": mision_salida
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    verificar_infraestructura()  # Corre el blindaje antes de encender
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

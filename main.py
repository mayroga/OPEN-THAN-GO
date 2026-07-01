# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify
import json
import sqlite3
import random
import os

app = Flask(__name__, static_folder='static')

def cargar_mision_por_bloque(decision, pocket_tier):
    """
    Carga y selecciona la misión adecuada dividida en bloques de 7.
    - Casa: Bloque 1 (Misiones 1-7) -> Archivo: 'missions_01_07.json'
    - Salir: Bloque 2 (8-14) o Bloque 3 (15-21) -> 'missions_08_14.json' / 'missions_15_21.json'
    """
    try:
        if decision == "casa":
            with open('missions_01_07.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Para casa, tomamos cualquier misión del bloque 1
            return random.choice(data['missions'])
        
        else:
            # Para salidas, elegimos al azar entre el Bloque 2 o el Bloque 3 para romper la monotonía
            archivo_elegido = random.choice(['missions_08_14.json', 'missions_15_21.json'])
            
            if not os.path.exists(archivo_elegido):
                # Fallback de seguridad al Bloque 1 si los otros archivos aún no están creados
                archivo_elegido = 'missions_01_07.json'
                
            with open(archivo_elegido, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Filtramos las misiones del bloque que hagan match con el presupuesto del cliente ('cero', 'moderado', 'libre')
            misiones_filtradas = [
                m for m in data['missions'] 
                if pocket_tier in m.get('pocket_match', [])
            ]
            
            # Si no hay match estricto, devolvemos una al azar del bloque para no romper el flujo
            return random.choice(misiones_filtradas) if misiones_filtradas else random.choice(data['missions'])
            
    except Exception as e:
        print(f"Error cargando catálogo de misiones: {str(e)}")
        return None

@app.route('/api/open-than-go', methods=['POST'])
def procesar_sistema_bienestar():
    data = request.json
    decision = data.get('decision') # "casa" o "salir"
    lang = data.get('lang', 'es')   # "es" o "en"
    
    # ----------------------------------------------------
    # MODALIDAD A: EL CLIENTE SE QUEDA EN CASA (Terapia de 10 min oculta)
    # ----------------------------------------------------
    if decision == "casa":
        # Forzar filtro de bolsillo general ya que no gasta en casa
        mision_casa = cargar_mision_por_bloque("casa", "cero")
        
        if not mision_casa:
            return jsonify({"status": "error", "message": "Error al inicializar el protocolo doméstico."}), 500
            
        return jsonify({
            "status": "success",
            "tipo": "Casa",
            "mision": mision_casa
        })
        
    # ----------------------------------------------------
    # MODALIDAD B: EL CLIENTE DECIDE SALIR (Romper el modo Zombi)
    # ----------------------------------------------------
    zip_code = data.get('zip_code')
    estado = data.get('estado')
    region = data.get('region')
    pocket = data.get('budget_level') # "cero", "minimo", "moderado", "libre"
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Consulta elástica multinivel para evitar que el usuario se quede sin opciones:
        # Intenta emparejar por código postal, si no, escala a región o estado entero, respetando el bolsillo.
        cursor.execute('''
            SELECT * FROM destinations 
            WHERE (zip_code = ? OR region = ? OR estado = ?) AND budget_tier = ?
        ''', (zip_code, region, estado, pocket))
        
        lugares_validos = cursor.fetchall()
        
        if not lugares_validos:
            return jsonify({
                "status": "error", 
                "message": "No encontramos destinos con ese presupuesto exacto en tu zona hoy. Intenta cambiar el rango de bolsillo."
            }), 404
            
        # Selección forzada de UN solo destino (Cero parálisis por análisis)
        lugar_seleccionado = random.choice(lugares_validos)
        
        # Cargar misión de salida (Bloques 2 o 3: Misiones 8 a 21)
        mision_salida = cargar_mision_por_bloque("salir", pocket)
        
        if not mision_salida:
            return jsonify({"status": "error", "message": "Error al inicializar el protocolo de exploración."}), 500
            
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
    # Configuración lista para producción en Render o ejecución local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

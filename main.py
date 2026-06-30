import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cargar la biblioteca estructurada de misiones de OPEN THAN GO
def cargar_biblioteca_tvid():
    # En producción esto lee tu archivo guardado en el repositorio de GitHub
    with open('tvid_missions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/diagnostico-kamizen', methods=['POST'])
def diagnostico_kamizen():
    datos = request.json
    puedes_salir = datos.get('puedes_salir')     # True o False
    idioma = datos.get('idioma', 'es')          # 'es' o 'en'
    zip_code = datos.get('zip_code', '').strip()
    estado = datos.get('estado', 'FL').strip()
    bolsillo = datos.get('bolsillo', 'cero')     # 'cero', 'moderado', 'libre'
    texto_libre = datos.get('texto_libre', '').lower()

    # 1. Leer biblioteca nativa estructurada por bloques de comandos
    biblioteca = cargar_biblioteca_tvid()
    misiones_disponibles = biblioteca["missions"]

    # 2. Analizador de Palabras Clave Emocionales para emparejar la técnica de May Roga LLC
    categoria_tvid = "bien" # Por defecto
    if "error" in texto_libre or "biles" in texto_libre or "cuenta" in texto_libre or "mal" in texto_libre:
        categoria_tvid = "mal"
    elif "aburrid" in texto_libre or "niñ" in texto_libre or "hijo" in texto_libre or "kid" in texto_libre:
        categoria_tvid = "nino"

    # Filtrar misiones que correspondan con la necesidad emocional y el bolsillo del usuario
    filtradas = [m for m in misiones_disponibles if m["cat"] == categoria_tvid and bolsillo in m["pocket_match"]]
    
    if not filtradas:
        mision_elegida = random.choice(misiones_disponibles)
    else:
        mision_elegida = random.choice(filtradas)

    # 3. Formatear los bloques internos en tiempo de ejecución para el idioma activo (Espejo Estricto)
    bloques_procesados = []
    for comando in mision_elegida["b"]:
        bloque_clon = comando.copy()
        
        # Traducir textos simples de encabezados, videos o conclusiones
        if "tx" in bloque_clon:
            bloque_clon["tx"] = bloque_clon["tx"][idioma]
        if "inf" in bloque_clon:
            bloque_clon["inf"] = bloque_clon["inf"][idioma]
        if "story" in bloque_clon:
            bloque_clon["story"] = bloque_clon["story"][idioma]
            
        # Traducir estructuras complejas de preguntas interactivas
        if bloque_clon["t"] == "d":
            bloque_clon["q"] = bloque_clon["q"][idioma]
            opciones_traducidas = [op[idioma] for op in bloque_clon["op"]]
            explicaciones_traducidas = [ex[idioma] for ex in bloque_clon["ex"]]
            bloque_clon["op"] = opciones_traducidas
            bloque_clon["ex"] = explicaciones_traducidas
            
        bloques_procesados.append(bloque_clon)

    # ==========================================================================
    # CASO INDOOR: Ejecuta las misiones interactivas dentro de casa
    # ==========================================================================
    if not puedes_salir:
        titulo = "Escape de Interiores: OPEN THAN GO" if idioma == 'es' else "Indoor Escape: OPEN THAN GO"
        lugar = "Tu espacio seguro en casa / Your home safe space"
        
        return jsonify({
            "modalidad": "indoor",
            "titulo": titulo,
            "lugar": lugar,
            "bloques_interactivos": bloques_procesados,
            "url_maps": None
        })

    # ==========================================================================
    # CASO OUTDOOR: Genera Deep Linking gratuito y adjunta la misión mental
    # ==========================================================================
    else:
        if not zip_code or len(zip_code) != 5:
            zip_code = "33101"

        tipo_mapa = "parks"
        if categoria_tvid == "nino":
            tipo_mapa = "family+parks+playground"
        elif categoria_tvid == "mal":
            tipo_mapa = "nature+reserves+scenic"

        query_busqueda = f"{tipo_mapa}+in+{zip_code}+{estado}+USA"
        url_maps_gratis = f"https://google.com{query_busqueda}"
        
        titulo_out = "Plan de Escape Abierto" if idioma == 'es' else "Open Escape Plan"
        lugar_out = f"Zona de libertad recomendada en {zip_code}, {estado}"

        # Inyectar un bloque inicial de instrucción de viaje en el idioma correspondiente
        instruccion_viaje = {
            "t": "h",
            "tx": f"Conduce al espacio abierto en tu zona postal {zip_code}. Al llegar, ejecuta tu secuencia:" if idioma == 'es' else f"Drive to the open space in your zip code {zip_code}. Upon arrival, start your sequence:"
        }
        bloques_procesados.insert(0, instruccion_viaje)

        return jsonify({
            "modalidad": "outdoor",
            "titulo": titulo_out,
            "lugar": lugar_out,
            "bloques_interactivos": bloques_procesados,
            "url_maps": url_maps_gratis
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

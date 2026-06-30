
def cargar_mision_tvid_desde_archivos(categoria_emocional, bolsillo_usuario):
    # Lista de los archivos donde guardas tus bloques de misiones ordenadas
    archivos_kamizen = ['missions_01_07.json', 'missions_08_14.json', 'missions_15_21.json']
    todas_las_tvid = []
    for nombre_archivo in archivos_kamizen:
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Extraemos todas las misiones (Rango del 1 al 21 completo de OPEN THAN GO)
                for m in data.get("missions", []):
                    if m.get("id", 0) >= 1:
                        todas_las_tvid.append(m)
        except Exception as e:
            print(f"Error cargando {nombre_archivo}: {e}")

    # Filtramos la lista de las misiones por la emoción detectada y el bolsillo del usuario
    filtradas = [
        m for m in todas_las_tvid 
        if m.get("cat") == categoria_emocional and bolsillo_usuario in m.get("pocket_match", ["cero", "moderado", "libre"])
    ]
    # Si encuentra coincidencia exacta la regresa; si no, elige una misión al azar del pozo de 21 misiones
    if filtradas:
        return random.choice(filtradas)
    elif todas_las_tvid:
        return random.choice(todas_las_tvid)
    else:
        return None

@app.route('/')
def home():
    # Esto le indica a Python que cuando alguien entre a tu URL principal,
    # le entregue de inmediato tu archivo visual HTML
    return app.send_static_file('session.html')

@app.route('/diagnostico-kamizen', methods=['POST'])
def diagnostico_kamizen():
    datos = request.json
    puedes_salir = datos.get('puedes_salir', True) # True o False
    idioma = datos.get('idioma', 'es') # 'es' o 'en'
    zip_code = str(datos.get('zip_code', '')).strip()
    estado = str(datos.get('estado', 'FL')).strip()
    bolsillo = datos.get('bolsillo', 'cero') # 'cero', 'moderado', 'libre'
    texto_libre = str(datos.get('texto_libre', '')).lower()

    # 1. Analizador Temático de Palabras Clave para asociar el desahogo a la TVid correcta
    categoria_detectada = "bien" # Por defecto
    if any(x in texto_libre for x in ["error", "biles", "cuenta", "dinero", "mal"]):
        categoria_detectada = "mal"
    elif any(x in texto_libre for x in ["aburrid", "niñ", "hijo", "kid"]):
        categoria_detectada = "nino"

    # 2. Cargar el objeto estructurado de comandos desde tus JSONs existentes (Rango ID 1-21)
    mision_tvid = cargar_mision_tvid_desde_archivos(categoria_detectada, bolsillo)
    if not mision_tvid:
        return jsonify({"error": "No misiones disponibles / No misiones encontradas"})

    # 3. Formateador de Idioma en Espejo (Extrae solo 'es' o 'en' para tu Javascript nativo)
    bloques_processed = []
    for comando in mision_tvid.get("b", []):
        bloque_clon = comando.copy()
        # Traducción protegida: si el idioma falta, intenta con 'es' o deja vacío
        for campo in ["tx", "inf", "story", "c"]:
            if campo in bloque_clon and isinstance(bloque_clon[campo], dict):
                bloque_clon[campo] = bloque_clon[campo].get(idioma, bloque_clon[campo].get('es', ''))
        if bloque_clon.get("t") == "d":
            if isinstance(bloque_clon.get("q"), dict):
                bloque_clon["q"] = bloque_clon["q"].get(idioma, bloque_clon["q"].get('es', ''))
            if "op" in bloque_clon:
                bloque_clon["op"] = [op.get(idioma, op.get('es', '')) if isinstance(op, dict) else op for op in bloque_clon["op"]]
            if "ex" in bloque_clon:
                bloque_clon["ex"] = [ex.get(idioma, ex.get('es', '')) if isinstance(ex, dict) else ex for ex in bloque_clon["ex"]]
        bloques_processed.append(bloque_clon)

    # 4. BIFURCACIÓN DE ENTORNOS DE ESCAPE
    if not puedes_salir:
        titulo = "Escape de Interiores: OPEN THAN GO" if idioma == 'es' else "Indoor Escape: OPEN THAN GO"
        return jsonify({
            "modalidad": "indoor",
            "titulo": titulo,
            "lugar": "Tu espacio seguro en casa / Your home safe space",
            "bloques_interactivos": bloques_processed,
            "url_maps": None
        })
    else:
        if not zip_code or len(zip_code) != 5:
            zip_code = "33101"
        tipo_mapa = "parks"
        if categoria_detectada == "nino":
            tipo_mapa = "family+parks+playground"
        elif categoria_detectada == "mal":
            tipo_mapa = "nature+reserves+scenic"

        query_busqueda = f"{tipo_mapa}+in+{zip_code}+{estado}+USA"
        
        # CORRECCIÓN DEFINITIVA: Enlace universal directo para abrir mapas nativos en teléfonos
        url_maps_gratis = f"https://google.com{query_busqueda}"
        
        titulo_out = "Plan de Escape Abierto: OPEN THAN GO" if idioma == 'es' else "Open Escape Plan: OPEN THAN GO"
        instruccion_viaje = {
            "t": "h",
            "tx": f"Dirígete al área abierta en tu zona postal {zip_code}. Al llegar, ejecuta tu secuencia:" if idioma == 'es' else f"Drive to the open space in your zip code {zip_code}. Upon arrival, start your sequence:"
        }
        bloques_processed.insert(0, instruccion_viaje)
        return jsonify({
            "modalidad": "outdoor",
            "titulo": titulo_out,
            "lugar": f"Zona de libertad recomendada en {zip_code}, {estado}",
            "bloques_interactivos": bloques_processed,
            "url_maps": url_maps_gratis
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

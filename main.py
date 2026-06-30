import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# FUNCIÓN INTELIGENTE: Lee tus archivos JSON existentes tal como están en GitHub
def cargar_mision_tvid_desde_archivos(categoria_emocional, bolsillo_usuario):
    # Lista de los archivos donde guardas tus bloques de misiones
    archivos_kamizen = ['missions_01_07.json', 'missions_08_14.json', 'missions_15_21.json']
    todas_las_tvid = []
    
    for nombre_archivo in archivos_kamizen:
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Extraemos misiones de las Técnicas de Vida (ID >= 5 de tu nueva lista bilingüe)
                for m in data["missions"]:
                    if m.get("id", 0) >= 5:
                        todas_las_tvid.append(m)
        except Exception as e:
            print(f"Error cargando {nombre_archivo}: {e}")

    # Filtramos la lista de las TVid por la emoción detectada y el bolsillo del usuario
    filtradas = [
        m for m in todas_las_tvid 
        if m["cat"] == categoria_emocional and bolsillo_usuario in m.get("pocket_match", ["cero", "moderado", "libre"])
    ]
    
    # Si encuentra coincidencia exacta la regresa; si no, elige una TVid al azar del pozo de 21 misiones
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
    puedes_salir = datos.get('puedes_salir')     # True o False
    idioma = datos.get('idioma', 'es')          # 'es' o 'en'
    zip_code = datos.get('zip_code', '').strip()
    estado = datos.get('estado', 'FL').strip()
    bolsillo = datos.get('bolsillo', 'cero')     # 'cero', 'moderado', 'libre'
    texto_libre = datos.get('texto_libre', '').lower()

    # 1. Analizador Temático de Palabras Clave para asociar el desahogo a la TVid correcta
    categoria_detectada = "bien" # Por defecto
    if "error" in texto_libre or "biles" in texto_libre or "cuenta" in texto_libre or "dinero" in texto_libre or "mal" in texto_libre:
        categoria_detectada = "mal"
    elif "aburrid" in texto_libre or "niñ" in texto_libre or "hijo" in texto_libre or "kid" in texto_libre:
        categoria_detectada = "nino"

    # 2. Cargar el objeto estructurado de comandos desde tus JSONs existentes (Rango ID >= 5)
    mision_tvid = cargar_mision_tvid_desde_archivos(categoria_detectada, bolsillo)
    
    if not mision_tvid:
        return jsonify({"error": "No misiones disponibles / No misiones encontradas"})

    # 3. Formateador de Idioma en Espejo (Extrae solo 'es' o 'en' para tu Javascript nativo)
    bloques_processed = []
    for comando in mision_tvid["b"]:
        bloque_clon = comando.copy()
        
        if "tx" in bloque_clon:
            bloque_clon["tx"] = bloque_clon["tx"][idioma]
        if "inf" in bloque_clon:
            bloque_clon["inf"] = bloque_clon["inf"][idioma]
        if "story" in bloque_clon:
            bloque_clon["story"] = bloque_clon["story"][idioma]
            
        if bloque_clon["t"] == "d":
            bloque_clon["q"] = bloque_clon["q"][idioma]
            bloque_clon["op"] = [op[idioma] for op in bloque_clon["op"]]
            bloque_clon["ex"] = [ex[idioma] for ex in bloque_clon["ex"]]
            
        bloques_processed.append(bloque_clon)

    # 4. BIFURCACIÓN DE ENTORNOS DE ESCAPE
    if not puedes_salir:
        # CASO CASA: Ejecuta directamente tus comandos interactivamente (Círculo azul, silencios)
        titulo = "Escape de Interiores: OPEN THAN GO" if idioma == 'es' else "Indoor Escape: OPEN THAN GO"
        return jsonify({
            "modalidad": "indoor",
            "titulo": titulo,
            "lugar": "Tu espacio seguro en casa / Your home safe space",
            "bloques_interactivos": bloques_processed,
            "url_maps": None
        })
    else:
        # CASO CALLE: Deep Linking Automático y Gratuito usando el ZIP code nacional
        if not zip_code or len(zip_code) != 5:
            zip_code = "33101"

        tipo_mapa = "parks"
        if categoria_detectada == "nino":
            tipo_mapa = "family+parks+playground"
        elif categoria_detectada == "mal":
            tipo_mapa = "nature+reserves+scenic"

        query_busqueda = f"{tipo_mapa}+in+{zip_code}+{estado}+USA"
        
        # REPARACIÓN DE LA URL DE MAPAS CON DEEP LINKING OFICIAL:
        url_maps_gratis = f"https://google.com{query_busqueda}"
        
        titulo_out = "Plan de Escape Abierto: OPEN THAN GO" if idioma == 'es' else "Open Escape Plan: OPEN THAN GO"
        
        # Insertamos el bloque guía de conducción al inicio de tus comandos interactivos
        instruccion_viaje = {
            "t": "h",
            "tx": f"Dirígete al área abierta en tu zona postal {zip_code}. Al llegar, ejecuta tu secuencia:" if idioma == 'es' else f"Drive to the open space in your zip code {zip_code}. Upon arrival, start your sequence:"
        }
        
        # REPARACIÓN DE LA ASIGNACIÓN ERRONEA QUE CAUSABA UNDEFINED:
        bloques_processed.insert(0, instruccion_viaje)

        return jsonify({
            "modalidad": "outdoor",
            "titulo": titulo_out,
            "lugar": f"Zona de libertad recomendada en {zip_code}, {estado}",
            "bloques_interactivos": bloques_processed,
            "url_maps": url_maps_gratis
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

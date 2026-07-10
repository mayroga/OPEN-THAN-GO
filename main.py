# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 2 (Backend Core)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()

# Ensure 'static' directory exists for serving static files
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Default vector for 19 Human Needs, used when a specific environment doesn't define all
# This ensures all dimensions are present for scoring and learning
DEFAULT_NECESSITY_VECTOR = {
    "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
    "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
    "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
    "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50
}

# Your complete original mission base + Vector Injection of 19 Human Needs
BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo."},
        {"id": 2, "titulo": "Desconexión de biles", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer."},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle."},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Deja caer la mochila de deudas. Siente tus hombros libres. Ya no está."},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando."},
        {"id": 6, "titulo": "Liberación de nudos", "descripcion": "Aprieta los puños 3 segundos. Abre de golpe. Suéltalo todo."},
        {"id": 7, "titulo": "El aire de la calle", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior."},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor."},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte."},
        {"id": 10, "titulo": "Orden de tu espacio", "descripcion": "Alinea tres objetos de tu mesa. Orden fuera es orden dentro."},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate."},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe."},
        {"id": 13, "titulo": "Foco en lo olvidado", "descripcion": "Elige una tarea mínima que ignorabas. Hazla ahora. Termínala."},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira."},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza."},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la puerta principal. Deja que el aire ruede. Huele el cambio."},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos."},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque."},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez."},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora."},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana."},
        {"id": 22, "titulo": "Relaja ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad."},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor."},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla."},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros."}
    ],
    "CASA_EXTRA": [
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa."},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado."},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto."},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la boca, mueve mandíbula a los lados."},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto."},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos."},
        {"id": 32, "titulo": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir."},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho."},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total."},
        {"id": 35, "titulo": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido."},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela."},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta."},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces."},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear."},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente."},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel."},
        {"id": 42, "titulo": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento."},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe."},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones."},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros."},
        {"id": 46, "titulo": "Siente base", "descripcion": "Contacto firme de piernas con silla."},
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido."},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti."},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la estabilidad."},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control."}
    ],
    "SALIR": {
        "agotado": [
            {
                "titulo": "Sombra de árbol",
                "porque": "Tu mente necesita descansar de las luces de la pantalla.",
                "que_hacer": "Busca un árbol grande. Toca su madera y quédate un rato bajo su sombra fresca.",
                "donde": "Un parque verde.",
                "gps": "parks+with+shade+",
                "vector_necesidades": {
                    "movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100,
                    "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30,
                    "contemplacion": 95, "trabajo": 10, "descanso": 90, "organizacion": 20, "alimentacion": 0,
                    "musica": 10, "risa": 30, "esperanza": 85
                }
            }
        ],
        "estresado": [
            {
                "titulo": "Caminata en subida",
                "porque": "Tu cuerpo acumuló cansancio y necesitas soltarlo caminando.",
                "que_hacer": "Busca una rampa o escalera pública. Sube a paso firme usando tu fuerza.",
                "donde": "Escalera pública.",
                "gps": "public+stairs+",
                "vector_necesidades": {
                    "movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20,
                    "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20,
                    "contemplacion": 60, "trabajo": 20, "descanso": 10, "organizacion": 30, "alimentacion": 0,
                    "musica": 20, "risa": 20, "esperanza": 75
                }
            }
        ],
        "aburrido": [
            {
                "titulo": "Paseo de colores",
                "porque": "Estás repitiendo los mismos días y necesitas ver cosas nuevas.",
                "que_hacer": "Camina despacio por la calle. Encuentra dibujos grandes en las paredes de tu zona.",
                "donde": "Calle con murales.",
                "gps": "street+art+",
                "vector_necesidades": {
                    "movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50,
                    "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55,
                    "contemplacion": 85, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 20,
                    "musica": 30, "risa": 60, "esperanza": 95
                }
            }
        ],
        "cansado": [
            {
                "titulo": "Lectura en biblioteca",
                "porque": "Necesitas un espacio de calma y aprendizaje sin distracciones.",
                "que_hacer": "Visita tu biblioteca local, busca un libro o simplemente disfruta el silencio.",
                "donde": "Biblioteca pública.",
                "gps": "public+library+",
                "vector_necesidades": {
                    "movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80,
                    "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10,
                    "contemplacion": 90, "trabajo": 40, "descanso": 85, "organizacion": 70, "alimentacion": 0,
                    "musica": 0, "risa": 10, "esperanza": 70
                }
            }
        ],
        "ansioso": [
            {
                "titulo": "Mirar el agua",
                "porque": "El movimiento del agua calma la mente y reduce la ansiedad.",
                "que_hacer": "Encuentra una fuente, lago o río cercano. Observa el agua fluir.",
                "donde": "Fuente de agua o lago.",
                "gps": "public+fountain+or+lake+",
                "vector_necesidades": {
                    "movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50,
                    "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20,
                    "contemplacion": 90, "trabajo": 0, "descanso": 80, "organizacion": 10, "alimentacion": 0,
                    "musica": 50, "risa": 10, "esperanza": 80
                }
            }
        ]
    }
}
# Billion-dollar infrastructure resources hijacked to break monotony
BIG_TECH_RESOURCES = {
    "spotify_audio": "https://open.spotify.com/genre/mood",
    "youtube_audio": "https://www.youtube.com/results?search_query=nature+sounds+relaxing",
    "staffing_agencies": "staffing+agencies"
}

@app.get("/")
async def index():
    """Serves the main HTML page."""
    return FileResponse('static/session.html')

# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.6.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 2 DE 2 (CWRE Logic)

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    """
    Main API endpoint for OPEN THAN GO.
    Receives user input and local preference profile to return a personalized recommendation.
    """
    payload = await request.json()
    opcion_usuario = str(payload.get("modo", "")).strip().upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip() # Default to FL if not provided, though not used in UI now
    region = str(payload.get("region", "")).strip() # Not used in UI now
    mente = str(payload.get("mente", "aburrido")).lower() # Default for `SALIR` mode
    budget = str(payload.get("budget", "0")) # 0: free, 1: low, 2: free
    perfil = str(payload.get("perfil", "solo")).lower() # solo, familia, hijos, adultos_mayores, veteranos_guerra, directivos_empresarios, trabajadores_gobierno
    desahogo = str(payload.get("desahogo", "")).lower() # User's free text input
    lang = str(payload.get("lang", "es")).lower()
   
    # Capture locally accumulated click metrics for the 19 needs from engine.js
    perfil_local = payload.get("perfil_local", DEFAULT_NECESSITY_VECTOR)
    # Ensure all 19 needs are present in perfil_local, with defaults if missing
    for need, default_val in DEFAULT_NECESSITY_VECTOR.items():
        if need not in perfil_local:
            perfil_local[need] = default_val


    # 1. DOMESTIC INTERVENTION (ORIGINAL CASA MODE INTACT)
    if opcion_usuario == "CASA":
        misiones = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        random.shuffle(misiones)  # Avoid monotony by shuffling local challenges
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})

    # 2. FIELD ACTION (SALIR MODE WITH ANTI-REPETITION SELECTION ENGINE)
    # Get initial options based on 'mente', default to 'aburrido' if 'mente' is not found
    opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
   
    # CWRE Logic Integrated: Mathematical weighting based on user's click trail within your app
    # Crosses implicit preferences of the 19 needs sent by the smartphone
    info_seleccionada = None
    if opciones_salir_candidatas:
        mejor_score = -1
        
        for opc in opciones_salir_candidatas:
            # Ensure the environment's vector is complete, merging with defaults
            vector_lugar = {**DEFAULT_NECESSITY_VECTOR, **opc.get("vector_necesidades", {})}
            score_coincidencia = 0
           
            # Sum the weights of the user's internal history against the environment's score
            for necesidad, peso_usuario in perfil_local.items():
                score_coincidencia += vector_lugar.get(necesidad, DEFAULT_NECESSITY_VECTOR.get(necesidad, 50)) * peso_usuario
               
            if score_coincidencia > mejor_score:
                mejor_score = score_coincidencia
                info_seleccionada = opc
    
    # Fallback if no matching options or candidates are empty (shouldn't happen with defaults, but for safety)
    if not info_seleccionada:
        # This takes a random item from the first list in BASE_MISIONES["SALIR"]
        # which is typically 'agotado' but robust enough.
        first_category_options = list(BASE_MISIONES["SALIR"].values())[0]
        info_seleccionada = random.choice(first_category_options)

    # Filter for real price in short action words
    precio_real = ""
    if budget == "0":
        precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if lang == "es" else "COST: Zero dollars. Creative austerity to protect your mind today."
    elif budget == "1":
        precio_real = "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if lang == "es" else "COST: Low range. A minimal treat to break the routine."
    elif budget == "2":
        precio_real = "GASTO: Libre. El dinero es tu herramienta de escape hoy." if lang == "es" else "COST: Free. Money is your escape tool today."
   
    # Filter for real companions - UPDATED FOR NEW PROFILE OPTIONS
    quienes_van = ""
    if perfil == "solo":
        quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if lang == "es" else "COMPANIONSHIP: You go alone to regain your center."
    elif perfil == "familia":
        quienes_van = "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tu familia." if lang == "es" else "COMPANIONSHIP: Environment suitable for your family to unwind."
    elif perfil == "hijos":
        quienes_van = "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños." if lang == "es" else "COMPANIONSHIP: Environment suitable for your children to unwind."
    elif perfil == "adultos_mayores":
        quienes_van = "ACOMPAÑAMIENTO: Ruta plana y accesible por comodidad física o edad." if lang == "es" else "COMPANIONSHIP: Flat and accessible route for physical comfort or age."
    elif perfil == "veteranos_guerra":
        quienes_van = "ACOMPAÑAMIENTO: Vas en solitario a un lugar de paz y reflexión." if lang == "es" else "COMPANIONSHIP: You go alone to a place of peace and reflection."
    elif perfil == "directivos_empresarios":
        quienes_van = "ACOMPAÑAMIENTO: Vas en solitario a un destino de aislamiento total." if lang == "es" else "COMPANIONSHIP: You go alone to a destination of total isolation."
    elif perfil == "trabajadores_gobierno":
        quienes_van = "ACOMPAÑAMIENTO: Vas en solitario a un espacio natural amplio." if lang == "es" else "COMPANIONSHIP: You go alone to a wide natural space."


    # FINANCIAL SURVIVAL AND WELLBEING INTERCEPTOR FILTER
    palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "economy", "money", "work"]
    
    # Default values for external recommendations
    titulo_ganador = info_seleccionada["titulo"]
    donde_base = info_seleccionada["donde"]
    link_base = "https://www.google.com/maps/search/?api=1&query="
    gps_query = info_seleccionada["gps"]
    guia_masticada = ""

    # Check for critical keywords in 'desahogo' to activate the interceptor
    if any(p in desahogo for p in palabras_criticas):
        canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "STAFFING"]) # Added STAFFING as option
        if canal_multimedia == "SPOTIFY":
            titulo_ganador = "RESET AUDITIVO" if lang == "es" else "AUDIO RESET"
            donde_base = "Zona Libre de Consumo" if lang == "es" else "Store-Free Zone"
            guia_masticada = (
                "DESTINO: Spotify Gratis.\n"
                "QUÉ HACER: Escucha los sonidos naturales en silencio.\n"
                "PARA QUÉ: Detener el impulso de gastar dinero en cosas innecesarias hoy."
            ) if lang == "es" else (
                "TARGET: Free Spotify.\n"
                "WHAT TO DO: Listen to nature sounds in silence.\n"
                "WHY: Stop the urge to buy unnecessary items today."
            )
            link_base = BIG_TECH_RESOURCES["spotify_audio"]
            gps_query = "" # No GPS query for Spotify
        elif canal_multimedia == "YOUTUBE":
            titulo_ganador = "REINICIO VISUAL" if lang == "es" else "VISUAL SHOCK"
            donde_base = "Frecuencia de Alivio" if lang == "es" else "Relief Frequency"
            guia_masticada = (
                "DESTINO: Video en YouTube.\n"
                "QUÉ HACER: Pon el video en pantalla completa.\n"
                "PARA QUÉ: Calmar los pensamientos rápidos del día."
            ) if lang == "es" else (
                "TARGET: YouTube Video.\n"
                "WHAT TO DO: Play the video in full screen.\n"
                "WHY: Calm your racing thoughts right now."
            )
            link_base = BIG_TECH_RESOURCES["youtube_audio"]
            gps_query = "" # No GPS query for YouTube
        else: # STAFFING
            titulo_ganador = "ACTIVACIÓN LABORAL" if lang == "es" else "ECONOMIC ACTION"
            donde_base = ("Oficinas de contratación y staffings corporativos en tu zona." if lang == "es" else
                          "Employment Agencies in your area.")
            guia_masticada = (
                f"DESTINO: Oficinas de empleo inmediato.\n"
                f"QUÉ HACER: Entra ya con tu identificación en mano.\n"
                f"PARA QUÉ: Para ganarle al agobio del dinero y tomar el control de tu economía hoy.\n"
                f"{quienes_van}\n{precio_real}"
            ) if lang == "es" else (
                f"TARGET: Employment Agency.\n"
                f"WHAT TO DO: Go out straight with your physical ID.\n"
                f"WHY: Look for a quick job and get cash now.\n"
                f"{quienes_van}\n{precio_real}"
            )
            link_base = "https://www.google.com/maps/search/?api=1&query="
            gps_query = BIG_TECH_RESOURCES["staffing_agencies"]
    else:
        # Regular bilingual field routes, debt-free
        if lang == "en":
            traducciones_guia = {
                "Sombra de árbol": "TARGET: Tree Shade.\nWHAT TO DO: Touch the bark. Stay under its fresh shade.\nWHY: Your eyes need a rest from screen lights.",
                "Caminata en subida": "TARGET: Public Stairs.\nWHAT TO DO: Walk up firmly using your strength.\nWHY: Release the physical stress from your body.",
                "Paseo de colores": "TARGET: Street Art.\nWHAT TO DO: Look at murals in silence. Find hidden details.\nWHY: Break your daily routine with something new.",
                "Lectura en biblioteca": "TARGET: Public Library.\nWHAT TO DO: Visit your local library. Enjoy the silence.\nWHY: Find calm and learning without distractions.",
                "Mirar el agua": "TARGET: Public Fountain or Lake.\nWHAT TO DO: Find a nearby water source. Watch the water flow.\nWHY: The movement of water calms the mind and reduces anxiety."
            }
            guia_masticada = traducciones_guia.get(info_seleccionada["titulo"], f"TARGET: {info_seleccionada['donde']}.\nWHAT TO DO: {info_seleccionada['que_hacer']}\nWHY: {info_seleccionada['porque']}\n{quienes_van}\n{precio_real}")
            titulo_ganador = info_seleccionada["titulo"].upper()
        else:
            guia_masticada = (
                f"DESTINO: {info_seleccionada['titulo']}.\n"
                f"POR QUÉ: {info_seleccionada['porque']}\n"
                f"QUÉ HACER: {info_seleccionada['que_hacer']}\n"
                f"CUÁNDO: Ahora mismo. Levántate de la silla ya.\n"
                f"PARA QUÉ: Para romper el zombi urbano y recordar que la vida es más que pagar cuentas.\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador = info_seleccionada["titulo"].upper()

    # Adaptability of the Biopsychosocial Profile without social exclusion
    # These modifications should be applied only if gps_query is a map query
    if link_base.startswith("https://www.google.com/maps"):
        if perfil == "accesible" or perfil == "adultos_mayores":
            gps_query = "wheelchair+accessible+" + gps_query
        elif perfil == "familia" or perfil == "hijos":
            gps_query = "family+friendly+" + gps_query
        elif perfil == "directivos_empresarios":
            gps_query = "quiet+remote+places+no+signal+" + gps_query
        elif perfil == "trabajadores_gobierno":
            gps_query = "state+parks+secluded+areas+" + gps_query
        elif perfil == "veteranos_guerra":
            gps_query = "war+memorials+peaceful+reflection+" + gps_query

    # ORIGINAL FIXED UNIVERSAL GEOGRAPHIC FORMULA RESTORED WITHOUT CUTTING OR ALTERATIONS
    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}" # Default FL for state is used
   
    final_link = ""
    if gps_query:
        if link_base.startswith("http"): # Check if link_base is a full URL template
            final_link = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        else: # Fallback, though current definitions make link_base a full URL for maps
            final_link = link_base.replace(" ", "+")
    else:
        final_link = link_base.replace(" ", "+") # For Spotify/YouTube, link_base is already the full URL

    # Merge environment's vector_necesidades with DEFAULT_NECESSITY_VECTOR to ensure all 19 are present
    final_vector_necesidades = {**DEFAULT_NECESSITY_VECTOR, **info_seleccionada.get("vector_necesidades", {})}

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_titulo": titulo_ganador,
        "destino_entorno": donde_base,
        "destino_instruccion": guia_masticada.strip(),
        "destino_coordenadas_gps": final_link,
        "vector_entorno_seleccionado": final_vector_necesidades # Inject the full vector for engine.js to add to the dynamic profile
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.1
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 2 (Backend Core)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random
import re # Import for basic validation

app = FastAPI()

# Ensure 'static' directory exists for serving static files
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Default vector for 19 Human Needs, used when a specific environment doesn't define all
# This ensures all dimensions are present for scoring and learning
# NOTE: This is duplicated in frontend for quick access. For larger projects,
# consider a shared configuration file or API endpoint to ensure canonical definition.
DEFAULT_NECESSITY_VECTOR = {
    "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
    "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
    "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
    "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50
}

# Your complete original mision base + Vector Injection of 19 Human Needs
# Corrected: Now includes English translations for SALIR mode for full bilingual support
BASE_MISIONES = {
    "CASA_ES": [ # Separate list for Spanish CASA missions
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
        {"id": 22, "titulo": "Relaxa ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad."},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor."},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla."},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros."}
    ],
    "CASA_EN": [ # Separate list for English CASA missions
        {"id": 1, "titulo": "Cut the autopilot", "descripcion": "Scan your body. Pinpoint the exact weight on your back. See it. You are alive."},
        {"id": 2, "titulo": "Bill Disconnection", "descripcion": "Feel your chair. The floor supports your weight for free. Let yourself fall."},
        {"id": 3, "titulo": "Screen Isolation", "descripcion": "Flip your phone. Look at a corner of the ceiling for 30 seconds. Break the loop."},
        {"id": 4, "titulo": "Release the Burden", "descripcion": "Drop the backpack of debts. Feel your shoulders free. It's gone."},
        {"id": 5, "titulo": "The Water Reset", "descripcion": "A small sip of cold water. Feel the liquid. It's life entering."},
        {"id": 6, "titulo": "Knot Liberation", "descripcion": "Clench your fists for 3 seconds. Open sharply. Let it all go."},
        {"id": 7, "titulo": "Street Air", "descripcion": "Open the window. Let the air hit your face. Feel the outside."},
        {"id": 8, "titulo": "Energy Rotation", "descripcion": "Rotate wrists and ankles. Your body is yours. You govern this engine."},
        {"id": 9, "titulo": "Present Anchor", "descripcion": "Close your eyes. Say one good thing you have today. Say it loud."},
        {"id": 10, "titulo": "Order Your Space", "descripcion": "Align three objects on your table. Order outside is order inside."},
        {"id": 11, "titulo": "Feet on the Ground", "descripcion": "Take off your shoes. Rest soles on the floor. Feel the cold. Connect."},
        {"id": 12, "titulo": "Sky Stretch", "descripcion": "Arm up. Touch the ceiling. Maintain tension. Release suddenly."},
        {"id": 13, "titulo": "Focus on the Forgotten", "descripcion": "Choose a minimal task you ignored. Do it now. Finish it."},
        {"id": 14, "titulo": "Straight Spine", "descripcion": "Straighten your back. An invisible thread pulls your head. Breathe."},
        {"id": 15, "titulo": "Cold Contact", "descripcion": "Touch a cold surface. Feel the real temperature. Ground yourself."},
        {"id": 16, "titulo": "Total Ventilation", "descripcion": "Open the front door. Let the air flow. Smell the change."},
        {"id": 17, "titulo": "Stress Shake-off", "descripcion": "Stand up and shake hands and legs as if shaking off water. Do it for 10 seconds."},
        {"id": 18, "titulo": "Distant Gaze", "descripcion": "Look at the farthest object outside your window. Rest your focus."},
        {"id": 19, "titulo": "Happy Memory", "descripcion": "Close your eyes and recall a real moment of calm from your childhood."},
        {"id": 20, "titulo": "Forced Smile", "descripcion": "Smile for 15 seconds. Change your brain chemistry now."},
        {"id": 21, "titulo": "Gratitude", "descripcion": "Close your eyes. Be thankful for one good thing this week."},
        {"id": 22, "titulo": "Relax Eyes", "descripcion": "Cover your eyes with warm palms. One minute of darkness."},
        {"id": 23, "titulo": "Heart Rate", "descripcion": "Right hand on chest. Feel the heartbeat. It's your engine."},
        {"id": 24, "titulo": "Release Neck", "descripcion": "Slow head circles. Release screen tension."},
        {"id": 25, "titulo": "Palm Exercise", "descripcion": "Rub hands until warm. Place them on shoulders."}
    ],
    "CASA_EXTRA_ES": [ # Extra missions, also separate by language
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
    "CASA_EXTRA_EN": [ # Extra missions in English
        {"id": 26, "titulo": "Distant Sounds", "descripcion": "Identify the farthest sound outside your home."},
        {"id": 27, "titulo": "Side Stretch", "descripcion": "Gently lean your body to each side."},
        {"id": 28, "titulo": "The Empty Glass", "descripcion": "Look at a glass. Focus on its shape for one minute."},
        {"id": 29, "titulo": "Release Jaw", "descripcion": "Open your mouth wide, move your jaw side to side."},
        {"id": 30, "titulo": "Slow Steps", "descripcion": "Ten slow, conscious steps in your room."},
        {"id": 31, "titulo": "Gentle Massage", "descripcion": "Fingertips on temples. Very slow circles."},
        {"id": 32, "titulo": "Air Awareness", "descripcion": "Feel the cold air enter, the warm air leave."},
        {"id": 33, "titulo": "Firm Back", "descripcion": "Shoulder blades back, open your chest."},
        {"id": 34, "titulo": "Total Support", "descripcion": "Feel the chair supporting your full weight."},
        {"id": 35, "titulo": "Countdown", "descripcion": "From 20 to 1. Slowly. Calm the noise."},
        {"id": 36, "titulo": "Touch Texture", "descripcion": "Run fingers over a real texture. Wood or fabric."},
        {"id": 37, "titulo": "Stretch Fingers", "descripcion": "Spread fingers as wide as possible for 5 seconds. Release."},
        {"id": 38, "titulo": "Internal Sound", "descripcion": "Listen to your breath. Don't force it."},
        {"id": 39, "titulo": "Fixed Gaze", "descripcion": "Small spot on the wall. Fixed. Without blinking."},
        {"id": 40, "titulo": "Release Arms", "descripcion": "Hang arms. Shake them gently."},
        {"id": 41, "titulo": "Clothes Contact", "descripcion": "Notice the weight of clothes on your skin."},
        {"id": 42, "titulo": "Deep Air", "descripcion": "Inflate belly, hold 3 seconds, release slowly."},
        {"id": 43, "titulo": "Shoulder Rotation", "descripcion": "Shoulders to ears, drop suddenly."},
        {"id": 44, "titulo": "Listen to Silence", "descripcion": "Search for silence between breaths."},
        {"id": 45, "titulo": "Ceiling Gaze", "descripcion": "Look at the ceiling. Stretch neck without moving shoulders."},
        {"id": 46, "titulo": "Feel Base", "descripcion": "Firm contact of legs with chair."},
        {"id": 47, "titulo": "Firm Fists", "descripcion": "Fists tightly for 3 seconds, open quickly."},
        {"id": 48, "titulo": "Mental Cleanse", "descripcion": "Exhale boring worry. Out of you."},
        {"id": 49, "titulo": "Touch Table", "descripcion": "Palms on table. Note the stability."},
        {"id": 50, "titulo": "Total Presence", "descripcion": "You are here. You are safe. You are in control."}
    ],
    "SALIR": { # SALIR missions now include English translations
        "agotado": [
            {
                "id": 101,
                "titulo": "Sombra de árbol", "titulo_en": "Tree Shade",
                "porque": "Tu mente necesita descansar de las luces de la pantalla.", "porque_en": "Your mind needs to rest from screen lights.",
                "que_hacer": "Busca un árbol grande. Toca su madera y quédate un rato bajo su sombra fresca.", "que_hacer_en": "Find a large tree. Touch its bark and stay a while under its cool shade.",
                "donde": "Un parque verde.", "donde_en": "A green park.",
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
                "id": 102,
                "titulo": "Caminata en subida", "titulo_en": "Uphill Walk",
                "porque": "Tu cuerpo acumuló cansancio y necesitas soltarlo caminando.", "porque_en": "Your body has accumulated tiredness and needs to release it by walking.",
                "que_hacer": "Busca una rampa o escalera pública. Sube a paso firme usando tu fuerza.", "que_hacer_en": "Find a public ramp or stairs. Climb steadily using your strength.",
                "donde": "Escalera pública.", "donde_en": "Public stairs.",
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
                "id": 103,
                "titulo": "Paseo de colores", "titulo_en": "Color Walk",
                "porque": "Estás repitiendo los mismos días y necesitas ver cosas nuevas.", "porque_en": "You are repeating the same days and need to see new things.",
                "que_hacer": "Camina despacio por la calle. Encuentra dibujos grandes en las paredes de tu zona.", "que_hacer_en": "Walk slowly through the street. Find large drawings on the walls in your area.",
                "donde": "Calle con murales.", "donde_en": "Street with murals.",
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
                "id": 104,
                "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading",
                "porque": "Necesitas un espacio de calma y aprendizaje sin distracciones.", "porque_en": "You need a calm space for learning without distractions.",
                "que_hacer": "Visita tu biblioteca local, busca un libro o simplemente disfruta el silencio.", "que_hacer_en": "Visit your local library, find a book or simply enjoy the silence.",
                "donde": "Biblioteca pública.", "donde_en": "Public library.",
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
                "id": 105,
                "titulo": "Mirar el agua", "titulo_en": "Watch the Water",
                "porque": "El movimiento del agua calma la mente y reduce la ansiedad.", "porque_en": "The movement of water calms the mind and reduces anxiety.",
                "que_hacer": "Encuentra una fuente, lago o río cercano. Observa el agua fluir.", "que_hacer_en": "Find a nearby fountain, lake, or river. Watch the water flow.",
                "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.",
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
    "spotify_audio_es": "https://open.spotify.com/genre/mood/relax-stress-relief", # More specific
    "spotify_audio_en": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_es": "https://www.youtube.com/results?search_query=sonidos+naturaleza+relajantes",
    "youtube_audio_en": "https://www.youtube.com/results?search_query=nature+sounds+relaxing",
    "staffing_agencies_es": "agencias+de+empleo",
    "staffing_agencies_en": "employment+agencies"
}

@app.get("/")
async def index():
    """Serves the main HTML page."""
    return FileResponse('static/session.html')

# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.6.0.1
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
    estado = str(payload.get("estado", "FL")).strip() # Default to FL if not provided
    region = str(payload.get("region", "")).strip()
    mente = str(payload.get("mente", "aburrido")).lower() # Default for `SALIR` mode
    budget = str(payload.get("budget", "0")) # 0: free, 1: low, 2: free
    perfil_tipo = str(payload.get("perfil", "solo")).lower() # solo, familia, accesible (renamed to perfil_tipo to avoid conflict with perfil_local)
    desahogo = str(payload.get("desahogo", "")).lower() # User's free text input
    lang = str(payload.get("lang", "es")).lower()
    last_recommendation_id = payload.get("last_recommendation_id", None) # Corrected: For anti-repetition

    # Basic ZIP code validation
    if zip_code and not re.fullmatch(r"^\d{5}$", zip_code):
        return JSONResponse({"error": "Código Postal inválido. Debe ser 5 dígitos numéricos."}, status_code=400)
   
    # Capture locally accumulated click metrics for the 19 needs from engine.js
    perfil_local = payload.get("perfil_local", DEFAULT_NECESSITY_VECTOR)
    # Ensure all 19 needs are present in perfil_local, with defaults if missing
    for need, default_val in DEFAULT_NECESSITY_VECTOR.items():
        if need not in perfil_local:
            perfil_local[need] = default_val

    # 1. DOMESTIC INTERVENTION (ORIGINAL CASA MODE INTACT)
    if opcion_usuario == "CASA":
        misiones = BASE_MISIONES[f"CASA_{lang.upper()}"] + BASE_MISIONES[f"CASA_EXTRA_{lang.upper()}"]
        random.shuffle(misiones)  # Avoid monotony by shuffling local challenges
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})

    # 2. FIELD ACTION (SALIR MODE WITH ANTI-REPETITION SELECTION ENGINE)
    # Get initial options based on 'mente', default to 'aburrido' if 'mente' is not found
    opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
   
    # CWRE Logic Integrated: Mathematical weighting based on user's click trail within your app
    # Crosses implicit preferences of the 19 needs sent by the smartphone
    info_seleccionada = None
    mejor_score = -1
   
    # Corrected: Implement anti-repetition logic for SALIR mode
    candidatos_validos = []
    for opc in opciones_salir_candidatas:
        if opc.get("id") != last_recommendation_id or len(opciones_salir_candidatas) == 1: # Added missing colon
            candidatos_validos.append(opc)
   
    # If all candidates were the last one, or no other options, use the original list
    if not candidatos_validos:
        candidatos_validos = opciones_salir_candidatas

    # Now score from the valid candidates
    for opc in candidatos_validos:
        # Ensure the environment's vector is complete, merging with defaults
        vector_lugar = {**DEFAULT_NECESSITY_VECTOR, **opc.get("vector_necesidades", {})}
        score_coincidencia = 0
       
        # Sum the weights of the user's internal history against the environment's score
        for necesidad, peso_usuario in perfil_local.items():
            # Ensure "indicador_ansiedad" is skipped, as it's an internal metric for engine.js only
            if necesidad != "indicador_ansiedad":
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
   
    # Filter for real companions
    quienes_van = ""
    if perfil_tipo == "solo":
        quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if lang == "es" else "COMPANIONSHIP: You go alone to regain your center."
    elif perfil_tipo == "familia":
        quienes_van = "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia." if lang == "es" else "COMPANIONSHIP: Environment suitable for your children and family to unwind."
    elif perfil_tipo == "accesible":
        quienes_van = "ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad." if lang == "es" else "COMPANIONSHIP: Flat route with full access for physical comfort or age."

    # FINANCIAL SURVIVAL AND WELLBEING INTERCEPTOR FILTER
    palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "economy", "money", "work"]
   
    # Default values for external recommendations
    titulo_ganador = info_seleccionada[f"titulo_{lang}"] if lang == "en" else info_seleccionada["titulo"]
    donde_base = info_seleccionada[f"donde_{lang}"] if lang == "en" else info_seleccionada["donde"]
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
            link_base = BIG_TECH_RESOURCES[f"spotify_audio_{lang}"]
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
            link_base = BIG_TECH_RESOURCES[f"youtube_audio_{lang}"]
            gps_query = "" # No GPS query for YouTube
        else: # STAFFING
            titulo_ganador = "ACTIVACIÓN LABORAL" if lang == "es" else "ECONOMIC ACTION"
            donde_base = (
                ("Oficinas de contratación y staffings corporativos en tu zona." if lang == "es" else
                "Employment Agencies in your area.")
            )
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
            gps_query = BIG_TECH_RESOURCES[f"staffing_agencies_{lang}"]
    else:
        # Regular bilingual field routes, debt-free
        if lang == "en":
            guia_masticada = (
                f"TARGET: {info_seleccionada['titulo_en']}.\n"
                f"WHAT TO DO: {info_seleccionada['que_hacer_en']}\n"
                f"WHY: {info_seleccionada['porque_en']}\n"
                f"WHEN: Right now. Get out of your chair immediately.\n"
                f"FOR WHAT: To break the urban zombie and remember that life is more than paying bills.\n" # Added EN equivalent
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador = info_seleccionada["titulo_en"].upper()
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
        if perfil_tipo == "accesible":
            gps_query = "wheelchair+accessible+" + gps_query
        elif perfil_tipo == "familia":
            gps_query = "family+friendly+" + gps_query

    # ORIGINAL FIXED UNIVERSAL GEOGRAPHIC FORMULA RESTORED WITHOUT CUTTING OR ALTERATIONS
    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}" # Default FL for state is used
   
    final_link = ""
    if gps_query:
        if link_base.startswith("http") and "google.com/maps" in link_base: # Ensure it's a map link for geo
            final_link = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        else: # For Spotify/YouTube or Staffing where link_base is already the full URL, or staffing with generic geo
            # If gps_query is not empty, it implies we want to append it to link_base (e.g., for staffing agencies with anclaje_geografico)
            # Otherwise, link_base is already the complete URL (Spotify/YouTube)
            if "staffing" in gps_query: # Specific case for staffing agencies
                final_link = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
            else: # For spotify/youtube, link_base is already complete
                final_link = link_base.replace(" ", "+")
    else:
        final_link = link_base.replace(" ", "+") # For Spotify/YouTube, link_base is already the full URL

    # Merge environment's vector_necesidades with DEFAULT_NECESSITY_VECTOR to ensure all 19 are present
    final_vector_necesidades = {**DEFAULT_NECESSITY_VECTOR, **info_seleccionada.get("vector_necesidades", {})}

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_id": info_seleccionada.get("id"), # Corrected: Send back the ID for anti-repetition
        "destino_titulo": titulo_ganador,
        "destino_entorno": donde_base,
        "destino_instruccion": guia_masticada.strip(),
        "destino_coordenadas_gps": final_link,
        "vector_entorno_seleccionado": final_vector_necesidades # Inject the full vector for engine.js to add to the dynamic profile
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)

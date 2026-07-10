# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.5.5.0
# Company: May Roga LLC
# File: main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Tu base de misiones original completa + Inyección Vectorial de 19 Necesidades Humanas
BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo.", "vector_necesidades": {"contemplacion":100, "descanso":80, "silencio":70}},
        {"id": 2, "titulo": "Desconexión de biles", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer.", "vector_necesidades": {"descanso":90, "organizacion":60, "esperanza":70}},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle.", "vector_necesidades": {"silencio":95, "descanso":75, "contemplacion":80}},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Deja caer la mochila de deudas. Siente tus hombros libres. Ya no está.", "vector_necesidades": {"esperanza":90, "descanso":85, "organizacion":70}},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando.", "vector_necesidades": {"agua":100, "descanso":60, "aire_fresco":50}},
        {"id": 6, "titulo": "Liberación de nudos", "descripcion": "Aprieta los puños 3 segundos. Abre de golpe. Suéltalo todo.", "vector_necesidades": {"movimiento":80, "descanso":70, "risa":30}},
        {"id": 7, "titulo": "El aire de la calle", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior.", "vector_necesidades": {"aire_fresco":100, "naturaleza":60, "contemplacion":50}},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor.", "vector_necesidades": {"movimiento":90, "descanso":50, "organizacion":40}},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte.", "vector_necesidades": {"esperanza":100, "contemplacion":80, "silencio":70}},
        {"id": 10, "titulo": "Orden de tu espacio", "descripcion": "Alinea tres objetos de tu mesa. Orden fuera es orden dentro.", "vector_necesidades": {"organizacion":100, "descanso":50, "contemplacion":40}},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate.", "vector_necesidades": {"naturaleza":80, "silencio":60, "descanso":70}},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe.", "vector_necesidades": {"movimiento":95, "descanso":65, "aire_fresco":30}},
        {"id": 13, "titulo": "Foco en lo olvidado", "descripcion": "Elige una tarea mínima que ignorabas. Hazla ahora. Termínala.", "vector_necesidades": {"trabajo":80, "organizacion":90, "esperanza":60}},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira.", "vector_necesidades": {"movimiento":70, "descanso":80, "silencio":50}},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza.", "vector_necesidades": {"contemplacion":90, "silencio":70, "descanso":60}},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la puerta principal. Deja que el aire ruede. Huele el cambio.", "vector_necesidades": {"aire_fresco":100, "naturaleza":70, "esperanza":80}},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos.", "vector_necesidades": {"movimiento":100, "risa":60, "juego":50}},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque.", "vector_necesidades": {"contemplacion":95, "silencio":80, "naturaleza":70}},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez.", "vector_necesidades": {"esperanza":100, "descanso":90, "silencio":85}},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora.", "vector_necesidades": {"risa":100, "esperanza":90, "descanso":70}},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana.", "vector_necesidades": {"esperanza":95, "contemplacion":80, "silencio":75}},
        {"id": 22, "titulo": "Relaja ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad.", "vector_necesidades": {"descanso":100, "silencio":90, "contemplacion":80}},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor.", "vector_necesidades": {"contemplacion":100, "silencio":90, "descanso":85}},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla.", "vector_necesidades": {"movimiento":85, "descanso":90, "silencio":70}},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros.", "vector_necesidades": {"movimiento":70, "descanso":80, "silencio":60}}
    ],
    "CASA_EXTRA": [
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa.", "vector_necesidades": {"silencio":90, "contemplacion":95, "naturaleza":80}},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado.", "vector_necesidades": {"movimiento":90, "descanso":80, "silencio":60}},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto.", "vector_necesidades": {"contemplacion":100, "silencio":95, "descanso":70}},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la boca, mueve mandíbula a los lados.", "vector_necesidades": {"movimiento":85, "descanso":80, "silencio":70}},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto.", "vector_necesidades": {"movimiento":70, "contemplacion":80, "silencio":90}},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos.", "vector_necesidades": {"descanso":100, "silencio":90, "contemplacion":80}},
        {"id": 32, "titulo": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir.", "vector_necesidades": {"aire_fresco":100, "contemplacion":90, "silencio":85}},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho.", "vector_necesidades": {"movimiento":80, "descanso":70, "organizacion":60}},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total.", "vector_necesidades": {"descanso":95, "contemplacion":85, "silencio":75}},
        {"id": 35, "titulo": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido.", "vector_necesidades": {"silencio":100, "contemplacion":90, "descanso":80}},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela.", "vector_necesidades": {"contemplacion":95, "silencio":80, "descanso":70}},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta.", "vector_necesidades": {"movimiento":90, "descanso":70, "silencio":50}},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces.", "vector_necesidades": {"silencio":100, "contemplacion":95, "descanso":90}},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear.", "vector_necesidades": {"contemplacion":100, "silencio":90, "descanso":80}},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente.", "vector_necesidades": {"movimiento":80, "descanso":75, "silencio":60}},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel.", "vector_necesidades": {"contemplacion":90, "silencio":80, "descanso":70}},
        {"id": 42, "titulo": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento.", "vector_necesidades": {"aire_fresco":95, "silencio":90, "descanso":95}},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento":90, "descanso":85, "silencio":70}},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones.", "vector_necesidades": {"silencio":100, "contemplacion":95, "descanso":90}},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros.", "vector_necesidades": {"movimiento":70, "descanso":80, "silencio":60}},
        {"id": 46, "titulo": "Siente base", "descripcion": "Contacto firme de piernas con silla.", "vector_necesidades": {"descanso":90, "contemplacion":85, "silencio":75}},
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido.", "vector_necesidades": {"movimiento":80, "descanso":70, "risa":30}},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti.", "vector_necesidades": {"descanso":95, "silencio":80, "esperanza":90}},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la estabilidad.", "vector_necesidades": {"contemplacion":90, "silencio":80, "descanso":70}},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza":100, "contemplacion":95, "silencio":90}}
    ],
    "SALIR": {
        # Opciones SALIR predefinidas, el motor seleccionará la más adecuada
        "parques_naturales": {
            "titulo": "Parque Natural Silencioso",
            "porque": "Tu mente necesita desconectar del ruido urbano. Naturaleza y paz te esperan.",
            "que_hacer": "Camina sin rumbo, solo escucha los sonidos del viento y los pájaros. Apaga tu móvil.",
            "donde": "Parque Natural",
            "gps": "quiet+nature+park+",
            "vector_necesidades": {
                "movimiento": 70, "naturaleza": 100, "silencio": 95, "agua": 60, "sol": 80, "sombra": 80,
                "aire_fresco": 100, "creatividad": 50, "comunidad": 30, "aprendizaje": 40, "juego": 40,
                "contemplacion": 90, "trabajo": 10, "descanso": 90, "organizacion": 20, "alimentacion": 10,
                "musica": 20, "risa": 30, "esperanza": 95
            }
        },
        "bibliotecas_publicas": {
            "titulo": "Biblioteca Pública Tranquila",
            "porque": "Necesitas un espacio de calma para reflexionar, sin presiones de consumo.",
            "que_hacer": "Busca una esquina. Observa a la gente, lee un libro al azar o simplemente quédate en silencio.",
            "donde": "Biblioteca Pública",
            "gps": "quiet+public+library+study+zone+",
            "vector_necesidades": {
                "movimiento": 20, "naturaleza": 10, "silencio": 100, "agua": 30, "sol": 20, "sombra": 50,
                "aire_fresco": 40, "creatividad": 70, "comunidad": 50, "aprendizaje": 100, "juego": 10,
                "contemplacion": 95, "trabajo": 30, "descanso": 80, "organizacion": 70, "alimentacion": 0,
                "musica": 0, "risa": 10, "esperanza": 85
            }
        },
        "senderos_caminata": {
            "titulo": "Sendero Aislado",
            "porque": "Tu cuerpo pide moverse y tu mente despejarse. Rompe la inercia con cada paso.",
            "que_hacer": "Usa ropa cómoda. Elige un camino con árboles y camina a tu propio ritmo. Sin prisas.",
            "donde": "Sendero de Caminata",
            "gps": "isolated+walking+trail+",
            "vector_necesidades": {
                "movimiento": 100, "naturaleza": 90, "silencio": 70, "agua": 50, "sol": 85, "sombra": 70,
                "aire_fresco": 95, "creatividad": 30, "comunidad": 20, "aprendizaje": 30, "juego": 20,
                "contemplacion": 80, "trabajo": 10, "descanso": 70, "organizacion": 20, "alimentacion": 10,
                "musica": 30, "risa": 20, "esperanza": 90
            }
        },
        "centros_culturales": {
            "titulo": "Centro Cultural Gratuito",
            "porque": "Necesitas estimular tu creatividad e intelecto sin gastar dinero. Nuevas perspectivas.",
            "que_hacer": "Visita una exposición, asiste a un taller gratuito o simplemente observa el arte y la gente.",
            "donde": "Centro Cultural",
            "gps": "free+cultural+center+events+",
            "vector_necesidades": {
                "movimiento": 40, "naturaleza": 10, "silencio": 60, "agua": 20, "sol": 10, "sombra": 30,
                "aire_fresco": 30, "creatividad": 100, "comunidad": 80, "aprendizaje": 90, "juego": 30,
                "contemplacion": 70, "trabajo": 20, "descanso": 60, "organizacion": 50, "alimentacion": 10,
                "musica": 60, "risa": 50, "esperanza": 80
            }
        },
        "lugares_contemplacion": {
            "titulo": "Punto de Contemplación",
            "porque": "La prisa te ahoga. Encuentra un lugar donde solo puedas observar y respirar.",
            "que_hacer": "Busca un banco con vista. Mira las nubes, los árboles o el horizonte. Permite que el tiempo pase.",
            "donde": "Punto Panorámico",
            "gps": "scenic+viewpoint+calm+",
            "vector_necesidades": {
                "movimiento": 10, "naturaleza": 90, "silencio": 90, "agua": 50, "sol": 70, "sombra": 60,
                "aire_fresco": 90, "creatividad": 20, "comunidad": 10, "aprendizaje": 20, "juego": 10,
                "contemplacion": 100, "trabajo": 0, "descanso": 95, "organizacion": 10, "alimentacion": 0,
                "musica": 10, "risa": 10, "esperanza": 90
            }
        }
    }
}
# Recursos de infraestructura trillonaria secuestrados para romper la monotonía
BIG_TECH_RESOURCES = {
    "spotify_audio": "https://open.spotify.com/search/nature%20sounds", # Enlace de búsqueda directa
    "youtube_audio": "https://www.youtube.com/results?search_query=relaxing+nature+sounds", # Enlace de búsqueda directa
    "staffing_agencies": "staffing+agencies"
}

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    opcion_usuario = str(payload.get("modo", "")).strip().upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
    
    # Nuevas variables capturadas desde el frontend
    mente_seleccionada = str(payload.get("mente", "ninguno")).lower()
    budget_seleccionado = str(payload.get("budget", "0"))
    perfil_seleccionado = str(payload.get("perfil", "solo")).lower()
    desahogo_texto = str(payload.get("desahogo", "")).lower()
    lang = str(payload.get("lang", "es")).strip()

    # Captura las métricas de clics acumuladas localmente en engine.js para las 19 necesidades
    perfil_local = payload.get("perfil_local", {})

    # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA ORIGINAL INTACTO)
    if opcion_usuario == "CASA":
        # Combina las misiones CASA y CASA_EXTRA
        misiones_disponibles = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        
        # Ponderación para seleccionar 3 misiones de CASA basadas en perfil_local
        if perfil_local:
            misiones_ponderadas = []
            for mision in misiones_disponibles:
                score_mision = 0
                vector_mision = mision.get("vector_necesidades", {})
                for necesidad, peso_usuario in perfil_local.items():
                    score_mision += vector_mision.get(necesidad, 50) * peso_usuario
                misiones_ponderadas.append((score_mision, mision))
            
            # Ordenar por score y seleccionar las 3 mejores
            misiones_ponderadas.sort(key=lambda x: x[0], reverse=True)
            misiones_finales = [m[1] for m in misiones_ponderadas[:3]]
        else:
            random.shuffle(misiones_disponibles)
            misiones_finales = misiones_disponibles[:3]

        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones_finales})

    # 2. ACCIÓN DE CAMPO (MODO SALIR CON MOTOR DE SELECCIÓN ANTI-REPETICIÓN Y TVid)
    # Selecciona la TVid basada en mente_seleccionada y desahogo_texto
    tvid_asignada = "Bien" # Asignación por defecto
    if "ansioso" in mente_seleccionada or "miedo" in desahogo_texto:
        tvid_asignada = "Mal"
    elif "cansado" in mente_seleccionada or "estresado" in mente_seleccionada or "presion corporativa" in desahogo_texto:
        tvid_asignada = "Beso"
    elif "aburrido" in mente_seleccionada or "hijos" in perfil_seleccionado or "familia" in perfil_seleccionado:
        tvid_asignada = "Niño"
    elif "agotado" in mente_seleccionada or "directivos" in perfil_seleccionado or "empresarios" in perfil_seleccionado:
        tvid_asignada = "Madre"
    elif "procrastinacion" in desahogo_texto or "posponiendo" in desahogo_texto:
        tvid_asignada = "Padre"
    elif "veteranos" in perfil_seleccionado or len(desahogo_texto.split()) > 10 or "crisis" in desahogo_texto:
        tvid_asignada = "Guerra"
    
    # LÓGICA CWRE INTEGRADA para destinos SALIR
    # Cruza las preferencias implícitas de las 19 necesidades enviadas por el smartphone
    opciones_salir_candidatas = list(BASE_MISIONES["SALIR"].values())
    
    mejor_score = -1
    info_salida = opciones_salir_candidatas[0] # Fallback por defecto

    for opc in opciones_salir_candidatas:
        vector_lugar = opc.get("vector_necesidades", {})
        score_coincidencia = 0
        
        for necesidad, peso_usuario in perfil_local.items():
            # Peso de usuario es el contador de clicks, vector_lugar es el peso del lugar para esa necesidad
            score_coincidencia += vector_lugar.get(necesidad, 50) * peso_usuario
            
        if score_coincidencia > mejor_score:
            mejor_score = score_coincidencia
            info_salida = opc

    # Filtro de precio real en palabras cortas de acción
    if budget_seleccionado == "0":
        precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy."
    elif budget_seleccionado == "1":
        precio_real = "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina."
    else: # "libre"
        precio_real = "GASTO: Libre. El dinero es tu herramienta de escape hoy."
    
    # Filtro de acompañantes reales
    if perfil_seleccionado == "solo":
        quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro."
    elif perfil_seleccionado == "familia" or perfil_seleccionado == "hijos":
        quienes_van = "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia."
    elif perfil_seleccionado == "adultos mayores":
        quienes_van = "ACOMPAÑAMIENTO: Considera un lugar de fácil acceso."
    elif perfil_seleccionado == "veteranos":
        quienes_van = "ACOMPAÑAMIENTO: Respeto y tranquilidad para tu servicio."
    else: # directivos, trabajadores_gobierno, etc. o cualquier otro
        quienes_van = "ACOMPAÑAMIENTO: Entorno flexible para tu necesidad."

    # FILTRO DE SUPERVIVENCIA LABORAL Y BIENESTAR FINANCIERO INTERCEPTOR
    # Considera también la 'mente_seleccionada' para activar este filtro
    palabras_criticas_finanzas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "economía", "laboral", "pago", "despido", "financiero"]
    
    # Amplía las condiciones para activar el filtro de supervivencia laboral
    activar_filtro_laboral = any(p in desahogo_texto for p in palabras_criticas_finanzas) or \
                             (mente_seleccionada in ["estresado", "ansioso", "agotado"] and \
                             any(p in mente_seleccionada for p in ["trabajo", "biles", "dinero"]))

    canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])

    if activar_filtro_laboral:
        if canal_multimedia == "SPOTIFY":
            titulo_ganador = "RESET AUDITIVO" if lang == "es" else "AUDIO RESET"
            donde_base = "Zona Libre de Consumo" if lang == "es" else "Store-Free Zone"
            guia_masticada = "DESTINO: Spotify Gratis.\nQUÉ HACER: Escucha los sonidos naturales en silencio.\nPARA QUÉ: Detener el impulso de gastar dinero en cosas innecesarias hoy." if lang == "es" else "TARGET: Free Spotify.\nWHAT TO DO: Listen to nature sounds in silence.\nWHY: Stop the urge to buy unnecessary items today."
            link_base = BIG_TECH_RESOURCES["spotify_audio"]
            gps_query = ""
        elif canal_multimedia == "YOUTUBE":
            titulo_ganador = "REINICIO VISUAL" if lang == "es" else "VISUAL SHOCK"
            donde_base = "Frecuencia de Alivio" if lang == "es" else "Relief Frequency"
            guia_masticada = "DESTINO: Video en YouTube.\nQUÉ HACER: Pon el video en pantalla completa.\nPARA QUÉ: Calmar los pensamientos rápidos del día." if lang == "es" else "TARGET: YouTube Video.\nWHAT TO DO: Play the video in full screen.\nWHY: Calm your racing thoughts right now."
            link_base = BIG_TECH_RESOURCES["youtube_audio"]
            gps_query = ""
        else: # MAPS para agencias de empleo
            titulo_ganador = "ACTIVACIÓN LABORAL" if lang == "es" else "ECONOMIC ACTION"
            donde_base = "Oficinas de contratación y staffings corporativos en tu zona." if lang == "es" else "Employment Agency"
            guia_masticada = f"DESTINO: Oficinas de empleo inmediato.\nQUÉ HACER: Entra ya con tu identificación en mano.\nPARA QUÉ: Para ganarle al agobio del dinero y tomar el control de tu economía hoy.\n{quienes_van}\n{precio_real}" if lang == "es" else f"TARGET: Staffing Agencies.\nWHAT TO DO: Go out straight with your physical ID.\nWHY: Look for a quick job and get cash now.\n{quienes_van}\n{precio_real}"
            link_base = "https://www.google.com/maps/search/?api=1&query="
            gps_query = BIG_TECH_RESOURCES["staffing_agencies"]
    else:
        # Rutas bilingües de campo ordinarias libres de deudas
        link_base = "https://www.google.com/maps/search/?api=1&query="
        gps_query = info_salida["gps"]
        donde_base = info_salida["donde"]
        
        if lang == "en":
            traducciones_guia = {
                "Parque Natural Silencioso": "TARGET: Quiet Nature Park.\nWHAT TO DO: Walk aimlessly, listen to the wind and birds. Turn off your phone.\nWHY: Your mind needs to disconnect from urban noise. Nature and peace await you.",
                "Biblioteca Pública Tranquila": "TARGET: Quiet Public Library.\nWHAT TO DO: Find a corner. Observe people, read a random book, or just stay silent.\nWHY: You need a calm space to reflect, without consumer pressure.",
                "Sendero Aislado": "TARGET: Isolated Walking Trail.\nWHAT TO DO: Wear comfortable clothes. Choose a path with trees and walk at your own pace. No rush.\nWHY: Your body needs to move and your mind needs to clear. Break the inertia with every step.",
                "Centro Cultural Gratuito": "TARGET: Free Cultural Center.\nWHAT TO DO: Visit an exhibition, attend a free workshop, or simply observe art and people.\nWHY: You need to stimulate your creativity and intellect without spending money. New perspectives.",
                "Punto de Contemplación": "TARGET: Scenic Viewpoint.\nWHAT TO DO: Find a bench with a view. Look at the clouds, trees, or horizon. Allow time to pass.\nWHY: The rush suffocates you. Find a place where you can just observe and breathe."
            }
            guia_masticada = traducciones_guia.get(info_salida["titulo"], f"TARGET: {info_salida['donde']}.\nWHAT TO DO: {info_salida['que_hacer']}\nWHY: {info_salida['porque']}\n{quienes_van}\n{precio_real}")
            titulo_ganador = info_salida["titulo"].upper()
        else:
            guia_masticada = f"DESTINO: {info_salida['titulo']}.\nPOR QUÉ: {info_salida['porque']}\nQUÉ HACER: {info_salida['que_hacer']}\nCUÁNDO: Ahora mismo. Levántate de la silla ya.\nPARA QUÉ: Para romper el zombi urbano y recordar que la vida es más que pagar cuentas.\n{quienes_van}\n{precio_real}"
            titulo_ganador = info_salida["titulo"].upper()

    # Adaptabilidad del Perfil Biopsicosocial sin exclusión social
    if perfil_seleccionado == "adultos mayores": gps_query = "accessible+for+seniors+" + gps_query
    elif perfil_seleccionado == "familia": gps_query = "family+friendly+" + gps_query
    elif perfil_seleccionado == "hijos": gps_query = "children+friendly+" + gps_query
    elif perfil_seleccionado == "veteranos": gps_query = "veteran+memorials+or+quiet+parks+" + gps_query
    elif perfil_seleccionado == "directivos" or perfil_seleccionado == "empresarios": gps_query = "quiet+isolation+retreats+or+parks+no+signal+" + gps_query
    elif perfil_seleccionado == "trabajadores del gobierno": gps_query = "state+parks+remote+" + gps_query

    # FÓRMULA GEOGRÁFICA UNIVERSAL FIJA ORIGINAL RESTAURADA SIN RECORTE NI ALTERACIONES
    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"

    if gps_query:
        if link_base.startswith("http"):
            link_google_maps_vivo = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        else:
            link_google_maps_vivo = link_base.replace(" ", "+")
    else:
        link_google_maps_vivo = link_base.replace(" ", "+")

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_titulo": titulo_ganador,
        "destino_entorno": donde_base,
        "destino_instruccion": guia_masticada.strip(),
        "destino_coordenadas_gps": link_google_maps_vivo,
        "token_entorno": info_salida["titulo"] if "titulo" in info_salida else "general",
        "tvid_asignada": tvid_asignada
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

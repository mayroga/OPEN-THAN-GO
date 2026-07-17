import os
import stripe
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse

# Inicialización con tus variables exactas de Render
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

PRICE_IDS = {
    "unico": "price_1TtbjXBOA5mT4t0PMCJSext6",
    "mensual": "price_1TtblSBOA5mT4t0PGiYvT2l9",
    "anual": "price_1TtbltBOA5mT4t0PpJ8io219"
}

# ENDPOINT: Crear sesión de pago en Stripe
@app.post("/api/create-checkout-session")
async def create_checkout_session(request: Request):
    try:
        payload = await request.json()
        tipo_plan = payload.get("plan", "unico")
        
        if tipo_plan not in PRICE_IDS:
            return JSONResponse({"error": "Plan inválido"}, status_code=400)
            
        id_precio = PRICE_IDS[tipo_plan]
        modo_checkout = "payment" if tipo_plan == "unico" else "subscription"
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': id_precio, 'quantity': 1}],
            mode=modo_checkout,
            success_url='https://onrender.com{CHECKOUT_SESSION_ID}',
            cancel_url='https://onrender.com',
        )
        return JSONResponse({"id": checkout_session.id, "url": checkout_session.url})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# COMPUERTA DE CONTROL DE ACCESO (Inyectar al inicio de tu app.post("/api/mando-integral"))
# Colócalo justo debajo de: payload = await request.json()
"""
username_cliente = str(payload.get("username", "")).strip()
password_cliente = str(payload.get("password", "")).strip()
session_token = str(payload.get("session_token", "")).strip()

# Recupera los accesos configurados en tu panel de Render
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin_por_defecto")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "clave_por_defecto")

# COMPUERTA DE ENTRADA GRATIS
es_admin_valido = (username_cliente == ADMIN_USER and password_cliente == ADMIN_PASS)

# COMPUERTA DE STRIPE
tiene_pago_valido = (session_token != "" and session_token.startswith("cs_"))

# Si NO es admin de Render y NO tiene un token válido de Stripe Checkout, se le deniega el acceso
if not es_admin_valido and not tiene_pago_valido:
    return JSONResponse({
        "error": "Acceso restringido.",
        "requiere_pago": True,
        "mensaje": "Se requiere una suscripción activa o credenciales válidas para usar el sistema."
    }, status_code=403)
"""

# ============================================================
# MOTOR DE HISTORIAL INTELIGENTE CWRE V2
# Anti-Repetición + Exploración Controlada
# ============================================================
MAX_HISTORY_SALIR = 5
MAX_HISTORY_CASA = 8
MAX_HISTORY_ORACULO = 12 # This is handled by frontend (engine.js)
EXPLORATION_RATE = 0.20
HISTORY_PENALTY_BASE = 40

def limitar_historial(historial, limite):
    if historial is None:
        return []
    return historial[-limite:]

def penalizacion_historial(mision_id, historial):
    if not historial:
        return 0
    historial = list(reversed(historial)) # Prioriza las más recientes
    for posicion, antiguo_id in enumerate(historial):
        if antiguo_id == mision_id:
            if posicion == 0: # Última misión
                return HISTORY_PENALTY_BASE * 1.5 # Más penalización para la última
            elif posicion == 1:
                return HISTORY_PENALTY_BASE
            elif posicion == 2:
                return HISTORY_PENALTY_BASE * 0.70
            elif posicion <= (len(historial) - 1):
                return HISTORY_PENALTY_BASE * 0.30
    return 0

def bonus_exploracion(mision_id, historial):
    if not historial or mision_id not in historial:
        return 20 # Bonificación significativa si nunca se ha visto
    # Reducir bonificación si ya se ha visto pero no está en el historial reciente
    if mision_id not in limitar_historial(historial, int(MAX_HISTORY_SALIR / 2)):
        return 5
    return 0

def actualizar_historial(historial, nuevo_id, limite):
    historial = historial or []
    if nuevo_id in historial:
        historial.remove(nuevo_id)
    historial.append(nuevo_id)
    return historial[-limite:]

def diversidad_vector(vector1, vector2):
    distancia = 0
    needs_to_consider = [k for k in DEFAULT_NECESSITY_VECTOR.keys() if k != "indicador_ansiedad"]
    for k in needs_to_consider:
        # Suma las diferencias absolutas de cada necesidad
        distancia += abs(
            vector1.get(k, DEFAULT_NECESSITY_VECTOR.get(k, 50)) -
            vector2.get(k, DEFAULT_NECESSITY_VECTOR.get(k, 50))
        )
    return distancia

# === MODIFICACIÓN: CONSTANTES DE TIEMPO Y PROPÓSITO ACORTADAS PARA LECTURA RÁPIDA ===
WHEN_ES = "Ahora. Levántate."
WHEN_EN = "Now. Move."
FOR_WHAT_ES = "Romper rutina. Recuérdate vivo."
FOR_WHAT_EN = "Break routine. Remember life."

# ============================================================
# CATÁLOGO DE MISIONES CWRE V2.1
# Adaptado para Microacciones de Recuperación Mental y sin elementos de estrés laboral/financiero.
# ============================================================
BASE_MISIONES = {
    "CASA_ES": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
        {"id": 2, "titulo": "Desconexión total", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Siente tus hombros libres. Ya no tienes esa mochila de peso invisible.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
        {"id": 7, "titulo": "El aire de la ventana", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la ventana. Deja que el aire ruede. Huele el cambio.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}},
        {"id": 22, "titulo": "Relaxa ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}},
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la boca, mueve mandíbula a los lados.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
        {"id": 32, "titulo": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}},
        {"id": 35, "titulo": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}},
        {"id": 42, "titulo": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}},
        {"id": 46, "titulo": "Siente base", "descripcion": "Contacto firme de piernas con silla.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
        {"id": 51, "titulo": "Canta una melodía", "descripcion": "Tararea tu canción favorita suavemente. No pienses, solo siente el sonido.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
        {"id": 52, "titulo": "Escribe 3 deseos", "descripcion": "En un papel, anota tres deseos simples que te gustaría cumplir hoy.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
        {"id": 53, "titulo": "Paseo por el pasillo", "descripcion": "Camina lentamente por el pasillo de tu casa, sintiendo cada paso.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
        {"id": 54, "titulo": "Mira una planta", "descripcion": "Si tienes una planta en casa, obsérvala con atención durante un minuto.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
        {"id": 55, "titulo": "Dibuja un círculo", "descripcion": "Toma un lápiz y papel. Dibuja círculos perfectos sin pensar en nada más.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
        {"id": 57, "titulo": "Abre un libro al azar", "descripcion": "Toma un libro, ábrelo en una página aleatoria y lee la primera frase.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}},
        {"id": 58, "titulo": "Escucha la lluvia", "descripcion": "Si llueve, abre la ventana y escucha el sonido de las gotas caer.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}},
        {"id": 59, "titulo": "Baila sin música", "descripcion": "Mueve tu cuerpo libremente por un minuto, como si nadie te viera.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}},
        {"id": 60, "titulo": "Bebe una infusión", "descripcion": "Prepara una infusión caliente y bébela lentamente, sintiendo el calor.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}},
        {"id": 61, "titulo": "Mira tus manos", "descripcion": "Observa las líneas y detalles de tus manos. Son herramientas poderosas.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}},
        {"id": 62, "titulo": "Imagina un paisaje", "descripcion": "Cierra los ojos e imagina tu paisaje natural favorito por 30 segundos.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}},
        {"id": 63, "titulo": "Estira la espalda", "descripcion": "Siéntate en el suelo con las piernas estiradas y trata de tocar tus pies.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 64, "titulo": "Respira por la nariz", "descripcion": "Haz 5 respiraciones profundas, solo por la nariz, notando el aire.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
        {"id": 65, "titulo": "Juego de sombras", "descripcion": "Con las manos, crea una forma en la pared con la luz de una lámpara.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}},
        {"id": 66, "titulo": "Un abrazo imaginario", "descripcion": "Abraza tus brazos fuertemente, imaginando que es un ser querido.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}},
        {"id": 67, "titulo": "Encuentra un objeto azul", "descripcion": "Busca rápidamente 5 objetos azules en tu entorno. Enfoca tu vista.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
        {"id": 69, "titulo": "Observa el cielo", "descripcion": "Abre la ventana o sal al balcón. Observa el cielo por un minuto.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
        {"id": 70, "titulo": "Masaje facial", "descripcion": "Con las yemas de los dedos, masajea suavemente tu frente y mejillas.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
        {"id": 71, "titulo": "Cierra los ojos y escucha", "descripcion": "Siéntate cómodo, cierra los ojos y solo escucha los sonidos de tu casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
        {"id": 72, "titulo": "Tensa y relaja los pies", "descripcion": "Aprieta los dedos de tus pies durante 5 segundos y luego relájalos.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
        {"id": 74, "titulo": "Olor consciente", "descripcion": "Huelea una flor, café o especia. Concéntrate en el aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
        {"id": 75, "titulo": "Cambia de silla", "descripcion": "Siéntate en otra silla o lugar de la casa por 5 minutos. Pequeño cambio.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}},
        # === MODIFICACIÓN: MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160) - DESCRIPCIONES ACORTADAS ===
        {"id": 151, "titulo": "EL RETO DE LA SUSCRIPCIÓN OLVIDADA", "descripcion": "Revisa tu email/banco. Cancela una suscripción olvidada. Recupera control y ahorra.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60}},
        {"id": 152, "titulo": "EL RETO DE LOS TRES GASTOS", "descripcion": "En tu teléfono, anota solo los 3 gastos clave de esta semana. Enfócate solo hoy.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80}},
        {"id": 153, "titulo": "EL RETO DEL ORDEN DIGITAL", "descripcion": "Borra 20 capturas/archivos inútiles. El orden digital reduce la carga mental.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70}},
        {"id": 154, "titulo": "EL RETO DEL SILENCIO", "descripcion": "Silencia apps que te causan ansiedad 1 hora. Tu atención necesita descanso.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80}},
        {"id": 155, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Escribe 3 cosas que hoy tienes y antes deseabas. Recuerda tu progreso.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60}},
        {"id": 156, "titulo": "EL RETO DEL AGUA", "descripcion": "Levántate lento, bebe un vaso de agua. Vuelve respirando en calma.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "salud": 85, "silencio": 50}},
        {"id": 157, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre ventana 2 min. Observa el cielo. Sin teléfono.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70}},
        {"id": 158, "titulo": "EL RETO DEL ORDEN", "descripcion": "Guarda 5 objetos desordenados. Cinco bastan hoy.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50}},
        {"id": 159, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Haz 5 respiraciones profundas, lentas. Nada más.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
        {"id": 160, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "2 min: mira un punto lejano. Descansa tus ojos de la pantalla.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}},
    ],
    "CASA_EN": [
        {"id": 1, "titulo": "Cut the autopilot", "descripcion": "Scan your body. Pinpoint the exact weight on your back. See it. You are alive.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
        {"id": 2, "titulo": "Total Disconnection", "descripcion": "Feel your chair. The floor supports your weight for free. Let yourself fall.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
        {"id": 3, "titulo": "Screen Isolation", "descripcion": "Flip your phone. Look at a corner of the ceiling for 30 seconds. Break the loop.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
        {"id": 4, "titulo": "Release the Burden", "descripcion": "Feel your shoulders free. That invisible backpack of weight is gone.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
        {"id": 5, "titulo": "The Water Reset", "descripcion": "A small sip of cold water. Feel the liquid. It's life entering.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
        {"id": 7, "titulo": "Street Air", "descripcion": "Open the window. Let the air hit your face. Feel the outside.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
        {"id": 8, "titulo": "Energy Rotation", "descripcion": "Rotate wrists and ankles. Your body is yours. You govern this engine.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
        {"id": 9, "titulo": "Present Anchor", "descripcion": "Close your eyes. Say one good thing you have today. Say it loud.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
        {"id": 11, "titulo": "Feet on the Ground", "descripcion": "Take off your shoes. Rest soles on the floor. Feel the cold. Connect.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
        {"id": 12, "titulo": "Sky Stretch", "descripcion": "Arm up. Touch the ceiling. Maintain tension. Release suddenly.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
        {"id": 14, "titulo": "Straight Spine", "descripcion": "Straighten your back. An invisible thread pulls your head. Breathe.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}},
        {"id": 15, "titulo": "Cold Contact", "descripcion": "Touch a cold surface. Feel the real temperature. Ground yourself.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}},
        {"id": 16, "titulo": "Total Ventilation", "descripcion": "Open the front door. Let the air flow. Smell the change.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}},
        {"id": 17, "titulo": "Stress Shake-off", "descripcion": "Stand up and shake hands and legs as if shaking off water. Do it for 10 seconds.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}},
        {"id": 18, "titulo": "Distant Gaze", "descripcion": "Look at the farthest object outside your window. Rest your focus.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}},
        {"id": 19, "titulo": "Happy Memory", "descripcion": "Close your eyes and recall a real moment of calm from your childhood.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}},
        {"id": 20, "titulo": "Forced Smile", "descripcion": "Smile for 15 seconds. Change your brain chemistry now.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}},
        {"id": 21, "titulo": "Gratitude", "descripcion": "Close your eyes. Be thankful for one good thing this week.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}},
        {"id": 22, "titulo": "Relax Eyes", "descripcion": "Cover your eyes with warm palms. One minute of darkness.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}},
        {"id": 23, "titulo": "Heart Rate", "descripcion": "Right hand on chest. Feel the heartbeat. It's your engine.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}},
        {"id": 24, "titulo": "Release Neck", "descripcion": "Slow head circles. Release screen tension.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}},
        {"id": 25, "titulo": "Palm Exercise", "descripcion": "Rub hands until warm. Place them on shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}},
        {"id": 26, "titulo": "Distant Sounds", "descripcion": "Identify the farthest sound outside your home.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}},
        {"id": 27, "titulo": "Side Stretch", "descripcion": "Gently lean your body to each side.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 28, "titulo": "The Empty Glass", "descripcion": "Look at a glass. Focus on its shape for one minute.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}},
        {"id": 29, "titulo": "Release Jaw", "descripcion": "Open your mouth wide, move your jaw side to side.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}},
        {"id": 30, "titulo": "Slow Steps", "descripcion": "Ten slow, conscious steps in your room.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}},
        {"id": 31, "titulo": "Gentle Massage", "descripcion": "Fingertips on temples. Very slow circles.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
        {"id": 32, "titulo": "Air Awareness", "descripcion": "Feel the cold air enter, the warm air leave.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}},
        {"id": 33, "titulo": "Firm Back", "descripcion": "Shoulder blades back, open your chest.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}},
        {"id": 34, "titulo": "Total Support", "descripcion": "Feel the chair supporting your full weight.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}},
        {"id": 35, "titulo": "Countdown", "descripcion": "From 20 to 1. Slowly. Calm the noise.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}},
        {"id": 36, "titulo": "Touch Texture", "descripcion": "Run fingers over a real texture. Wood or fabric.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}},
        {"id": 37, "titulo": "Stretch Fingers", "descripcion": "Spread fingers as wide as possible for 5 seconds. Release.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
        {"id": 38, "titulo": "Internal Sound", "descripcion": "Listen to your breath. Don't force it.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}},
        {"id": 39, "titulo": "Fixed Gaze", "descripcion": "Small spot on the wall. Fixed. Without blinking.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}},
        {"id": 40, "titulo": "Release Arms", "descripcion": "Hang arms. Shake them gently.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}},
        {"id": 41, "titulo": "Clothes Contact", "descripcion": "Notice the weight of clothes on your skin.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}},
        {"id": 42, "titulo": "Deep Air", "descripcion": "Inflate belly, hold 3 seconds, release slowly.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
        {"id": 43, "titulo": "Shoulder Rotation", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
        {"id": 44, "titulo": "Listen to Silence", "descripcion": "Search for silence between breaths.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}},
        {"id": 45, "titulo": "Ceiling Gaze", "descripcion": "Look at the ceiling. Stretch neck without moving shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}},
        {"id": 46, "titulo": "Feel Base", "descripcion": "Firm contact of legs with chair.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
        {"id": 51, "titulo": "Canta una melodía", "descripcion": "Tararea tu canción favorita suavemente. No pienses, solo siente el sonido.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
        {"id": 52, "titulo": "Escribe 3 deseos", "descripcion": "En un papel, anota tres deseos simples que te gustaría cumplir hoy.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
        {"id": 53, "titulo": "Paseo por el pasillo", "descripcion": "Camina lentamente por el pasillo de tu casa, sintiendo cada paso.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
        {"id": 54, "titulo": "Mira una planta", "descripcion": "Si tienes una planta en casa, obsérvala con atención durante un minuto.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
        {"id": 55, "titulo": "Dibuja un círculo", "descripcion": "Toma un lápiz y papel. Dibuja círculos perfectos sin pensar en nada más.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
        {"id": 57, "titulo": "Abre un libro al azar", "descripcion": "Toma un libro, ábrelo en una página aleatoria y lee la primera frase.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}},
        {"id": 58, "titulo": "Escucha la lluvia", "descripcion": "Si llueve, abre la ventana y escucha el sonido de las gotas caer.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}},
        {"id": 59, "titulo": "Baila sin música", "descripcion": "Mueve tu cuerpo libremente por un minuto, como si nadie te viera.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}},
        {"id": 60, "titulo": "Bebe una infusión", "descripcion": "Prepara una infusión caliente y bébela lentamente, sintiendo el calor.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}},
        {"id": 61, "titulo": "Mira tus manos", "descripcion": "Observa las líneas y detalles de tus manos. Son herramientas poderosas.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}},
        {"id": 62, "titulo": "Imagina un paisaje", "descripcion": "Cierra los ojos e imagina tu paisaje natural favorito por 30 segundos.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}},
        {"id": 63, "titulo": "Estira la espalda", "descripcion": "Siéntate en el suelo con las piernas estiradas y trata de tocar tus pies.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 64, "titulo": "Respira por la nariz", "descripcion": "Haz 5 respiraciones profundas, solo por la nariz, notando el aire.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
        {"id": 65, "titulo": "Juego de sombras", "descripcion": "Con las manos, crea una forma en la pared con la luz de una lámpara.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}},
        {"id": 66, "titulo": "Un abrazo imaginario", "descripcion": "Abraza tus brazos fuertemente, imaginando que es un ser querido.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}},
        {"id": 67, "titulo": "Encuentra un objeto azul", "descripcion": "Busca rápidamente 5 objetos azules en tu entorno. Enfoca tu vista.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
        {"id": 69, "titulo": "Observa el cielo", "descripcion": "Abre la ventana o sal al balcón. Observa el cielo por un minuto.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
        {"id": 70, "titulo": "Masaje facial", "descripcion": "Con las yemas de los dedos, masajea suavemente tu frente y mejillas.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
        {"id": 71, "titulo": "Cierra los ojos y escucha", "descripcion": "Siéntate cómodo, cierra los ojos y solo escucha los sonidos de tu casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
        {"id": 72, "titulo": "Tensa y relaja los pies", "descripcion": "Aprieta los dedos de tus pies durante 5 segundos y luego relájalos.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
        {"id": 74, "titulo": "Olor consciente", "descripcion": "Huelea una flor, café o especia. Concéntrate en el aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
        {"id": 75, "titulo": "Cambia de silla", "descripcion": "Siéntate en otra silla o lugar de la casa por 5 minutos. Pequeño cambio.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}},
        # === MODIFICACIÓN: MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160) - DESCRIPCIONES ACORTADAS ===
        {"id": 151, "titulo": "THE FORGOTTEN SUBSCRIPTION CHALLENGE", "descripcion": "Check email/banking app. Cancel forgotten subscription. Regain control and save.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60}},
        {"id": 152, "titulo": "THE THREE EXPENSES CHALLENGE", "descripcion": "On your phone, list only 3 key expenses for this week. Focus only today.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80}},
        {"id": 153, "titulo": "THE DIGITAL ORDER CHALLENGE", "descripcion": "Delete 20 useless screenshots/files. Digital order reduces mental load.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70}},
        {"id": 154, "titulo": "THE SILENCE CHALLENGE", "descripcion": "Silence anxiety-inducing apps for 1 hour. Your attention needs rest.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80}},
        {"id": 155, "titulo": "THE GRATITUDE CHALLENGE", "descripcion": "List 3 things you have today you once desired. Remember your progress.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60}},
        {"id": 156, "titulo": "THE WATER CHALLENGE", "descripcion": "Slowly stand, drink a glass of water. Return breathing calmly.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "salud": 85, "silencio": 50}},
        {"id": 157, "titulo": "THE WINDOW CHALLENGE", "descripcion": "Open window 2 min. Observe the sky. No phone.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70}},
        {"id": 158, "titulo": "THE ORDER CHALLENGE", "descripcion": "Put away 5 misplaced items. Five are enough today.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50}},
        {"id": 159, "titulo": "THE BREATHING CHALLENGE", "descripcion": "Take 5 deep, slow breaths. Nothing else.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
        {"id": 160, "titulo": "THE VISUAL REST CHALLENGE", "descripcion": "2 min: look at a distant point. Rest your eyes from the screen.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}},
    ],
    "SALIR": {
        "agotado": [
            {"id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade",
                "porque": "Mente cansada de pantallas. Necesitas desconectar.", "porque_en": "Screen-tired. Need to disconnect.",
                "que_hacer": "Busca un gran árbol. Toca su corteza. Siente la sombra fresca.", "que_hacer_en": "Find a large tree. Touch its bark. Feel the cool shade.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85}
            },
            {"id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe",
                "porque": "Necesitas un respiro mental. Evita ruidos. Busca paz.", "porque_en": "Mental break needed. Avoid noise. Seek peace.",
                "que_hacer": "Visita una cafetería tranquila. Pide tu bebida. Observa sin distracciones.", "que_hacer_en": "Visit a quiet cafe. Order. Observe without distractions.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cafetería local tranquila.", "donde_en": "Quiet local cafe.", "gps": "quiet cafe",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70}
            },
            {"id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden",
                "porque": "Mente agotada. Reconéctate con lo natural. Aire puro.", "porque_en": "Exhausted mind. Reconnect with nature. Pure air.",
                "que_hacer": "Pasea sin prisa por senderos. Observa plantas y flores. Respira hondo.", "que_hacer_en": "Stroll leisurely. Observe plants and flowers. Breathe deeply.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín botánico público.", "donde_en": "Public botanical garden.", "gps": "botanical garden",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90}
            },
            {"id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook",
                "porque": "Necesitas perspectiva. Eleva tu mirada. Rompe la rutina visual.", "porque_en": "Need perspective. Elevate gaze. Break visual routine.",
                "que_hacer": "Encuentra un punto alto con vista. Observa el horizonte. Siente la inmensidad.", "que_hacer_en": "Find a high point with view. Observe the horizon. Feel the immensity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95}
            },
            {"id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class",
                "porque": "Mente sobrecargada. Busca herramientas para la calma interna. Regula tu ser.", "porque_en": "Overloaded mind. Seek inner calm tools. Regulate your being.",
                "que_hacer": "Asiste a una sesión de meditación guiada. Concéntrate en la respiración. Suelta.", "que_hacer_en": "Attend guided meditation. Focus on breathing. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90}
            },
            {"id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing",
                "porque": "Mente agitada. Enfoca tu mirada en la inmensidad. Deja que los pensamientos pasen.", "porque_en": "Agitated mind. Focus on vastness. Let thoughts pass.",
                "que_hacer": "Busca un lugar abierto, recuéstate y observa el movimiento de las nubes.", "que_hacer_en": "Find open space, lie down, watch clouds move.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85}
            },
            {
                "id": 355,
                "titulo": "Soberanía en Tránsito: Uber/Lyft Concluido",
                "titulo_en": "Transit Sovereignty: Uber/Lyft Concluded",
                "porque": "Agotamiento periférico absoluto y fatiga acumulada por estar al volante o navegar el tráfico pesado de USA.",
                "porque_en": "Absolute peripheral exhaustion and accumulated fatigue from being behind the wheel or navigating heavy USA traffic.",
                "que_hacer": "Abre tu aplicación de transporte (Uber/Lyft). Solicita un viaje corto hacia la zona verde o plaza pública más cercana. Si ya estás dentro, suelta el teléfono, cierra los ojos por 60 segundos enteros, apoya tus palmas sobre tus muslos y ejecuta el Módulo de Vacío Auditivo.",
                "que_hacer_en": "Open your ride-sharing app (Uber/Lyft). Request a short ride to the nearest green area or public plaza. If already inside, drop your phone, close your eyes for 60 whole seconds, place your palms on your thighs, and execute the Auditory Emptiness Module.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cabina de transporte, parada de tránsito o asiento de pasajero.", "donde_en": "Transit vehicle cabin, transit stop, or passenger seat.",
                "gps": "quiet public square",
                "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 15, "contemplacion": 85, "esperanza": 80, "salud": 80, "aire_fresco": 60}
            },
            {
                "id": 356,
                "titulo": "Módulo de Cambio Frecuencial: Playlist de Spotify",
                "titulo_en": "Frequency Shift Module: Spotify Playlist",
                "porque": "Saturación mental y fatiga del nervio auditivo debido al ruido mecánico y las pantallas comerciales.",
                "porque_en": "Mental saturation and auditory nerve fatigue due to mechanical noise and commercial screens.",
                "que_hacer": "Abre Spotify de forma consciente. Busca frecuencias binaurales de 432Hz o ruidos blancos de la naturaleza. Colócate los auriculares, apoya tu cabeza hacia atrás, inhala hondo por la nariz y permite que el sonido estabilice tu lóbulo temporal por un minuto.",
                "que_hacer_en": "Open Spotify mindfully. Search for 432Hz binaural beats or white noise from nature. Put on your headphones, lean your head back, inhale deeply through your nose, and allow the sound to stabilize your temporal lobe for one minute.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Tu espacio de descanso, oficina vacía o dentro de tu vehículo.", "donde_en": "Your resting space, empty office, or inside your vehicle.",
                "gps": "quiet open park",
                "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 65, "contemplacion": 90, "esperanza": 85, "salud": 80, "creatividad": 40}
            },
            {
                "id": 357,
                "titulo": "Mapeo de Flujos: Recorrido Lineal en Costco",
                "titulo_en": "Flow Mapping: Costco Linear Walk",
                "porque": "Agotamiento por sedentarismo y parálisis cognitiva. Mover las piernas en un entorno industrial limpia tu sangre.",
                "porque_en": "Exhaustion from sedentary lifestyle and cognitive paralysis. Moving your legs in an industrial setting clears your blood.",
                "que_hacer": "Dirígete al Costco o almacén mayorista de tu área. Camina a paso firme por los pasillos perimetrales gigantescos sin la prisa de comprar. Observa las masas de suministros y usa este espacio climatizado para forzar la circulación de tus extremidades inferiores.",
                "que_hacer_en": "Head to the nearest Costco or wholesale warehouse in your area. Walk steadily through the giant perimeter aisles without any shopping rush. Observe the mass supplies and use this climate-controlled space to force circulation in your lower limbs.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pasillos industriales de un gran almacén de tu Código Postal.", "donde_en": "Industrial aisles of a large warehouse store in your Zip Code.",
                "gps": "wholesale club or market",
                "vector_necesidades": {"movimiento": 85, "organizacion": 70, "contemplacion": 60, "comunidad": 50, "juego": 30, "descanso": 20, "silencio": 10}
            },
            {
                "id": 358,
                "titulo": "Oasis Burocrático: Refugio en Biblioteca Pública",
                "titulo_en": "Bureaucratic Oasis: Public Library Refuge",
                "porque": "Fatiga extrema producida por esperas tensas, trámites burocráticos (DMV) o micro-estímulos digitales repetitivos.",
                "porque_en": "Extreme fatigue produced by tense waiting, bureaucratic procedures (DMV), or repetitive digital micro-stimuli.",
                "que_hacer": "Ubica la biblioteca pública más cercana de tu localidad. Ingresa en absoluto silencio y toma asiento en la sala común o pasillo de lectura. Disfruta de la quietud garantizada por el entorno y permite que tus córtex visuales descansen por completo.",
                "que_hacer_en": "Locate the nearest public library in your area. Enter in absolute silence and take a seat in the common room or reading aisle. Enjoy the guaranteed stillness of the environment and allow your visual cortex to rest completely.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sala de lectura, biblioteca municipal o zona de estudio de USA.", "donde_en": "Reading room, municipal library, or USA study zone.",
                "gps": "public library",
                "vector_necesidades": {"aprendizaje": 100, "silencio": 100, "contemplacion": 90, "descanso": 85, "organizacion": 70, "salud": 80}
            },
            {"id": 201, "titulo": "Soberanía en Tránsito: Uber/Lyft Relax", "titulo_en": "Transit Sovereignty: Uber/Lyft Relax",
                "porque": "Cuerpo al límite y mente saturada de conducir o moverte en tráfico continuo.", "porque_en": "Body/mind saturated from driving/traffic.",
                "que_hacer": "Abre tu app de transporte. Solicita viaje corto a zona tranquila. Cierra ojos, suelta teléfono, apoya palmas en rodillas. Ejecuta Módulo Silencio Auditivo 1 min.",
                "que_hacer_en": "Open ride app. Request short ride to quiet area. Close eyes, drop phone, palms on knees. Execute 1-min Auditory Silence Module.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cabina de transporte o asiento de pasajero.", "donde_en": "Rideshare cabin or passenger seat.",
                "gps": "quiet park bench",
                "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 10, "contemplacion": 80, "esperanza": 80, "naturaleza": 20, "aire_fresco": 50}
            },
            {"id": 202, "titulo": "Módulo Auditivo: Spotify Reset", "titulo_en": "Auditory Reset: Spotify",
                "porque": "Agotamiento mental agudo por ruidos industriales y pantallas.", "porque_en": "Acute mental exhaustion from industrial noise/screens.",
                "que_hacer": "Abre Spotify. Busca binaurales/sonidos lluvia. Auriculares. Cierra ojos 1 min. Deja frecuencias limpien fatiga temporal.",
                "que_hacer_en": "Open Spotify. Search binaural beats/rain sounds. Headphones. Close eyes 1 min. Let frequencies clear temporal fatigue.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cualquier rincón cómodo o dentro de tu auto.", "donde_en": "Any comfortable spot or inside your car.",
                "gps": "quiet library space",
                "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 60, "contemplacion": 90, "esperanza": 85, "creatividad": 40}
            },
            {"id": 203, "titulo": "Descompresión de Entorno: Lobby de Hotel", "titulo_en": "Environment Decompression: Hotel Lobby",
                "porque": "Saturación del espacio habitual. Necesitas un perímetro diseñado para el confort.", "porque_en": "Usual space saturation. Need comfort perimeter.",
                "que_hacer": "Ubica hotel/resort cercano. Ve a su lobby/sala descanso (costo cero). Siéntate recto, nota el piso. Descansa vista mirando un punto lejano 2 min.",
                "que_hacer_en": "Locate nearby hotel/resort. Go to lobby/lounge (zero cost). Sit straight, feel floor. Rest eyes on distant point 2 min.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lobby o zona de descanso de un hotel local.", "donde_en": "Lobby or lounge area of a local hotel.",
                "gps": "hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 70, "esperanza": 80, "movimiento": 20}
            },
            {"id": 204, "titulo": "Sabotaje de Espera: Espacio Universitario", "titulo_en": "Waiting Sabotage: University Space",
                "porque": "Falta de nutrición intelectual real y exceso de micro-estímulos vacíos.", "porque_en": "Lack of real intellectual nourishment, excess empty stimuli.",
                "que_hacer": "Ve al campus/biblioteca uni cercana. Camina en silencio por pasillos/áreas verdes. Usa esta infraestructura para respirar aire fresco y observar en calma.",
                "que_hacer_en": "Go to nearest campus/university library. Walk silently through corridors/green spaces. Use this infrastructure to breathe fresh air, observe calmly.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Campus universitario o biblioteca pública.", "donde_en": "University campus or public library.",
                "gps": "university library",
                "vector_necesidades": {"aprendizaje": 100, "silencio": 90, "contemplacion": 85, "descanso": 70, "aire_fresco": 75, "movimiento": 40}
            },
        ],
        "estresado": [
            {"id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk",
                "porque": "Cuerpo tenso. Libera estrés al caminar. Siente tu fuerza.", "porque_en": "Tense body. Release stress by walking. Feel your strength.",
                "que_hacer": "Encuentra rampa o escaleras públicas. Sube a paso firme. Usa tu energía.", "que_hacer_en": "Find public ramp or stairs. Climb steadily. Use your energy.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public stairs",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75}
            },
            {"id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga",
                "porque": "Mente acelerada. Conecta cuerpo y naturaleza. Respira consciente.", "porque_en": "Racing mind. Connect body and nature. Conscious breath.",
                "que_hacer": "Busca un parque. Extiende tu mat. Sigue una rutina de yoga o estiramientos.", "que_hacer_en": "Find a park. Lay your mat. Follow a yoga or stretching routine.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80}
            },
            {"id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym",
                "porque": "Necesitas liberar energía. Convierte la tensión en fuerza. Activa tu cuerpo.", "porque_en": "Need to release energy. Convert tension to strength. Activate your body.",
                "que_hacer": "Visita un gimnasio público o de bajo costo. Enfócate en tu rutina. Suda.", "que_hacer_en": "Visit a public or low-cost gym. Focus on your routine. Sweat.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60}
            },
            {
                "id": 320,
                "titulo": "Liberación de Impacto: Trampoline Park / Escalada",
                "titulo_en": "Impact Release: Trampoline Park / Climbing Gym",
                "porque": "Rigidez muscular y rabia contenida por presiones corporativas. Necesitas romper la coraza física.",
                "porque_en": "Muscular rigidity and pent-up anger from corporate pressures. You need to break the physical armor.",
                "que_hacer": "Dirígete al parque de trampolines, centro de salto (Defy, Sky Zone) o gimnasio de escalada más cercano. Compra un pase rápido. Salta con toda la fuerza de tus piernas descargando el peso en la lona, o aprieta tus manos escalando un muro. Deja que el esfuerzo físico extremo drene la adrenalina acumulada por el agobio diario.",
                "que_hacer_en": "Head to the nearest trampoline park, jump center (Defy, Sky Zone), or climbing gym. Buy a quick pass. Jump with all your leg strength discharging weight on the mat, or squeeze your hands scaling a wall. Let extreme physical effort drain the adrenaline built up from daily overwhelm.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de trampolines o centro deportivo de alta descarga en tu Código Postal.", "donde_en": "Trampoline park or high-discharge sports center in your Zip Code.",
                "gps": "trampoline park or climbing gym",
                "vector_necesidades": {"movimiento": 100, "juego": 100, "risa": 90, "salud": 95, "descanso": 0, "silencio": 10, "comunidad": 60, "esperanza": 90}
            },
            {
                "id": 321,
                "titulo": "Módulo de Hidro-Calma: Jacuzzi Público / Piscina de Termas",
                "titulo_en": "Hydro-Calm Module: Public Jacuzzi / Thermal Pool",
                "porque": "Sistema nervioso en alerta roja permanente. El agua templada en movimiento es el reset somático definitivo.",
                "porque_en": "Nervous system on permanent red alert. Moving warm water is the ultimate somatic reset.",
                "que_hacer": "Visita el centro recreativo con spa, piscina municipal climatizada o YMCA de tu perímetro. Sumérgete en el agua templada o jacuzzi. Cierra los ojos, deja que las burbujas o el agua masajeen tu espalda y concéntrate por dos minutos estrictos únicamente en la flotabilidad y la temperatura de tu piel.",
                "que_hacer_en": "Visit the recreation center with a spa, heated municipal pool, or YMCA in your perimeter. Submerge in warm water or a jacuzzi. Close your eyes, let the bubbles or water massage your back, and focus for two strict minutes solely on buoyancy and skin temperature.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "YMCA, alberca climatizada o spa comunitario local.",
                "donde_en": "YMCA, heated pool, or local community spa.",
                "gps": "ymca pool or public spa",
                "vector_necesidades": {"agua": 100, "descanso": 100, "salud": 95, "silencio": 60, "contemplacion": 90, "sombra": 80, "esperanza": 85, "movimiento": 20}
            },
            {
                "id": 322,
                "titulo": "Quiebre de Frecuencias: Sound Healing / Centro de Yoga",
                "titulo_en": "Frequency Break: Sound Healing / Yoga Center",
                "porque": "Mente acelerada con pensamientos intrusivos y zumbido mental debido al estrés digital continuo.",
                "porque_en": "Racing mind with intrusive thoughts and mental buzzing due to continuous digital stress.",
                "que_hacer": "Busca un estudio de yoga, meditación o sound healing en tu zona. Asiste a una sesión o recuéstate en su vestíbulo público si está disponible. Cierra los ojos, concéntrate en los armónicos, cuencos o el silencio del perímetro e inhala en 4 tiempos y exhala en 8 tiempos liberando la rigidez pectoral.",
                "que_hacer_en": "Search for a yoga, meditation, or sound healing studio in your area. Attend a session or lie down in its public lobby if available. Close your eyes, focus on harmonics, singing bowls, or perimeter silence, inhale for 4 counts, and exhale for 8 counts, releasing chest rigidity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Estudio de yoga, centro de meditación o sound healing en USA.",
                "donde_en": "Yoga studio, meditation center, or sound healing spot in the USA.",
                "gps": "sound healing or yoga studio",
                "vector_necesidades": {"silencio": 100, "descanso": 95, "musica": 90, "contemplacion": 95, "salud": 90, "esperanza": 90, "organizacion": 70}
            },
            {
                "id": 323,
                "titulo": "Aislamiento Orgánico: Sendero Natural Estatal (State Park)",
                "titulo_en": "Organic Isolation: State Park Trail",
                "porque": "Estrés tóxico urbano agudo. Requieres fitoncidas del bosque y aire puro para regular tu cortisol.",
                "porque_en": "Acute toxic urban stress. You require forest phytoncides and pure air to regulate your cortisol.",
                "que_hacer": "Dirígete de inmediato al parque estatal (State Park) o reserva natural protegida más cercana de tu Código Postal. Entra al sendero, camina descalzo sobre la tierra o toca la corteza de un gran árbol por un minuto completo. Siente el aire fresco real golpear tu cara lejos del concreto.",
                "que_hacer_en": "Head immediately to the nearest State Park or protected nature reserve in your Zip Code. Enter the trail, walk barefoot on the earth, or touch the bark of a large tree for a full minute. Feel the real fresh air hit your face away from concrete.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sendero boscoso, reserva natural o parque estatal de tu región.",
                "donde_en": "Wooded trail, nature reserve, or state park in your region.",
                "gps": "state park trail or nature reserve",
                "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "silencio": 85, "movimiento": 60, "contemplacion": 90, "descanso": 60, "esperanza": 95, "sol": 70}
            },
            {
                "id": 112,
                "titulo": "Sendero Corto Natural",
                "titulo_en": "Short Nature Trail",
                "porque": "Sobrecarga de estímulos. Desconéctate un momento. Camina en paz.",
                "porque_en": "Stimuli overload. Disconnect. Walk in peace.",
                "que_hacer": "Encuentra un sendero. Camina a paso ligero. Observa el entorno natural.",
                "que_hacer_en": "Find a trail. Walk briskly. Observe natural surroundings.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sendero natural o bosque.",
                "donde_en": "Nature trail or forest.",
                "gps": "short nature trail",
                "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "agua": 40, "sol": 60, "sombra": 70, "aire_fresco": 100, "creatividad": 40, "comunidad": 20, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "descanso": 60, "organizacion": 20, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85}
            },
            {
                "id": 113,
                "titulo": "Pista de Atletismo",
                "titulo_en": "Running Track",
                "porque": "Mente acelerada. Quema esa energía extra. Enfoca tu ritmo.",
                "porque_en": "Racing mind. Burn extra energy. Focus rhythm.",
                "que_hacer": "Dirígete a una pista pública. Corre o camina a tu propio paso. Libera.",
                "que_hacer_en": "Go to a public track. Run or walk your pace. Release.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pista de atletismo pública.",
                "donde_en": "Public running track.",
                "gps": "public running track",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 40, "agua": 10, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 10, "comunidad": 50, "aprendizaje": 20, "juego": 30, "contemplacion": 50, "descanso": 10, "organizacion": 70, "alimentacion": 0, "musica": 50, "risa": 20, "esperanza": 70}
            },
            {
                "id": 251,
                "titulo": "Soberanía en Movimiento: Interrupción Uber/Lyft",
                "titulo_en": "Sovereignty in Motion: Uber/Lyft Interruption",
                "porque": "Saturación nerviosa por el encierro dentro de cabinas de transporte, tráfico denso y sobrecarga de trayectos urbanos.",
                "porque_en": "Nervous saturation from confinement inside ride-sharing cabins, heavy traffic, and urban transit overload.",
                "que_hacer": "Si te encuentras viajando en Uber o Lyft en este Código Postal, despega los ojos de la pantalla de inmediato. Apoya las palmas de tus manos firmes sobre tus rodillas. Endereza la columna y ejecuta el Módulo de Ventilación Celular: inhala aire hondo en 4 segundos, retén 4 segundos y exhala todo el CO2 residual de golpe Siente el peso de tu organismo sostenido por el asiento. Tú eres el dueño de tu tiempo de vida, no la prisa del chofer ni la tarifa dinámica de la aplicación.",
                "que_hacer_en": "If you are traveling in an Uber or Lyft in this Zip Code, take your eyes off the screen immediately. Place your palms firmly on your knees. Straighten your spine and execute the Cell Ventilation Module: inhale deeply for 4 seconds, hold for 4 seconds, and exhale all residual CO2 at once. Feel your body's weight supported by the seat. You are the master of your lifespan, not the driver's haste or the app's surge pricing.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cabina de transporte, asiento de pasajero o parada de autobús de USA.",
                "donde_en": "Transit cabin, passenger seat, or USA bus stop.",
                "gps": "quiet rest areas or public plazas",
                "vector_necesidades": {"descanso": 95, "silencio": 85, "movimiento": 20, "contemplacion": 90, "organizacion": 60, "esperanza": 80}
            },
            {
                "id": 252,
                "titulo": "Hackeo al Tráfico: Módulo Intersección Interestatal",
                "titulo_en": "Traffic Hack: Interstate Intersection Module",
                "porque": "Nivel de cortisol elevado por embotellamientos, ruidos de autopista y el automatismo de las carreteras americanas.",
                "porque_en": "Elevated cortisol levels from traffic jams, highway noise, and the automation of American roads.",
                "que_hacer": "Si estás conduciendo o atrapado en el tráfico interestatal, aprovecha la próxima luz roja o área de descanso segura. Suelta la tensión de la mandíbula abriendo grande la boca de lado a lado por 10 segundos. Estira tus dedos sobre el volante liberando la rigidez acumulada en tus muñecas. Mira a través de la ventana el cielo abierto o la infraestructura masiva que te rodea. Pásale la factura al entorno urbano: tú respiras con calma mientras el asfalto ruge.",
                "que_hacer_en": "If driving or caught in interstate traffic, take advantage of the next red light or safe rest area. Release jaw tension by opening your mouth wide side to side for 10 seconds. Stretch your fingers over the steering wheel, releasing stiffness built up in your wrists. Look through the window at the open sky or the massive infrastructure around you. Bill the urban environment: you breathe calmly while the asphalt roars.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Área de servicio de autopista, rampa pública o intersección vial.", "donde_en": "Highway service area, public ramp, or road intersection.",
                "gps": "highway rest stop or overlook",
                "vector_necesidades": {"movimiento": 80, "descanso": 70, "silencio": 50, "aire_fresco": 85, "organizacion": 40, "salud": 85}
            },            
            {"id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route",
                "porque": "Necesitas liberar tensión y moverte rápido. Siente el viento. Explora tu entorno.", "porque_en": "Need to release tension, move fast. Feel wind. Explore.",
                "que_hacer": "Encuentra un carril bici seguro y pedalea. Siente la velocidad y el control.", "que_hacer_en": "Find a safe bike lane and pedal. Feel speed and control.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80}
            },
            {"id": 211, "titulo": "Soberanía de Cabina: Terminal Aérea / Vuelos", "titulo_en": "Cabin Sovereignty: Air Terminal / Flights",
                "porque": "Saturación nerviosa por presiones y ruidos de tránsito masivo.", "porque_en": "Nervous saturation from mass transit pressures/noise.",
                "que_hacer": "En aeropuerto/cerca, busca la ventana más grande con vista al cielo. Haz 3 inhalaciones diafragmáticas profundas. Siente el viento. Tu organismo no pertenece a la prisa industrial.",
                "que_hacer_en": "At/near airport, find largest sky-view window. Take 3 deep diaphragmatic breaths. Feel the wind. Your body is not for industrial haste.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Terminal de aeropuerto o zona de observación abierta.", "donde_en": "Airport terminal or open observation zone.",
                "gps": "airport observation area",
                "vector_necesidades": {"aire_fresco": 100, "contemplacion": 95, "silencio": 60, "descanso": 50, "movimiento": 30, "esperanza": 80}
            },
            {"id": 212, "titulo": "Depuración Exocrina: Complejo Deportivo / Gym", "titulo_en": "Exocrine Cleansing: Sports Complex / Gym",
                "porque": "Exceso de adrenalina retenida en los músculos por estrés laboral.", "porque_en": "Excess adrenaline retained from work stress.",
                "que_hacer": "Ve al gym/piscina pública más cercana. Haz contracción voluntaria 60 seg. Suda para liberar sales y toxinas. Activa tu cuerpo.",
                "que_hacer_en": "Go to nearest gym/public pool. Force continuous voluntary contraction for 60 secs. Sweat to release heavy salts/toxins. Activate your body.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gimnasio público, cancha o alberca comunitaria.", "donde_en": "Public gym, court, or community pool.",
                "gps": "community fitness center",
                "vector_necesidades": {"movimiento": 100, "agua": 80, "salud": 90, "juego": 50, "descanso": 0, "silencio": 20, "risa": 40}
            },
            {"id": 213, "titulo": "Estabilización Somática: Farmacia / Clínica", "titulo_en": "Somatic Stabilization: Pharmacy / Clinic",
                "porque": "Aceleración del ritmo cardíaco y sensación física de vulnerabilidad o pánico.", "porque_en": "Accelerated heart rate, physical vulnerability/panic.",
                "que_hacer": "Visita clínica/farmacia. Busca agua potable. Hidratación consciente: bebe un vaso pequeño saboreando. Siente cómo rehidrata tus células.",
                "que_hacer_en": "Visit public clinic/pharmacy. Find drinking water. Conscious Hydration: sip small cup, taste every molecule. Feel cells rehydrate.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Área de descanso de una farmacia o clínica local.", "donde_en": "Lounge area of a local pharmacy or clinic.",
                "gps": "pharmacy health lounge",
                "vector_necesidades": {"agua": 100, "salud": 95, "descanso": 80, "silencio": 70, "organizacion": 80, "esperanza": 85}
            },
        ],
        "aburrido": [
            {"id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk",
                "porque": "Días repetitivos. Busca novedad. Despierta tu visión.", "porque_en": "Repetitive days. Seek novelty. Awaken sight.",
                "que_hacer": "Camina lento. Busca murales y dibujos grandes en tu zona.", "que_hacer_en": "Walk slowly. Find large murals/drawings in your area.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street art",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}
            },
            {
                "id": 307,
                "titulo": "Descompresión de Perímetro: Lobby de Hotel / Resort",
                "titulo_en": "Perimeter Decompression: Hotel / Resort Lobby",
                "porque": "Monotonía espacial severa. Necesitas un entorno de diseño premium para alterar tus receptores visuales.",
                "porque_en": "Severe spatial monotony. You need a premium design environment to alter your visual receptors.",
                "que_hacer": "Ubica el hotel o resort de cadena más cercano (Marriott, Hilton, Hyatt). Ingresa de forma gratuita y siéntate en una de sus butacas premium del lobby público. Observa la arquitectura, mantén la espalda recta y descansa un minuto del ecosistema digital habitual.",
                "que_hacer_en": "Locate the nearest chain hotel or resort (Marriott, Hilton, Hyatt). Enter for free and sit in one of the public lobby's premium armchairs. Observe the architecture, keep your spine straight, and take a one-minute break from the usual digital ecosystem.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lobby o zona de descanso pública de un hotel local.", "donde_en": "Lobby or public lounge area of a local hotel.",
                "gps": "hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 80, "esperanza": 80, "comunidad": 50, "movimiento": 20}
            },
            {
                "id": 308,
                "titulo": "Ampliación del Horizonte: Terminal de Aerolíneas",
                "titulo_en": "Horizon Expansion: Airline Terminal",
                "porque": "Falta de perspectiva y estancamiento geográfico. Ver el movimiento de flujos globales te devuelve el enfoque.",
                "porque_en": "Lack of perspective and geographic stagnation. Watching the movement of global flows returns your focus.",
                "que_hacer": "Si estás cerca de una terminal aérea (Delta, United) o central de tránsito de USA, dirígete al vestíbulo público principal. Busca el ventanal más amplio con vista directo al horizonte del cielo. Realiza tres respiraciones diafragmáticas completas asimilando la inmensidad del espacio exterior.",
                "que_hacer_en": "If near a USA airline terminal (Delta, United) or transit hub, head to the main public lobby. Find the widest window with a direct view of the sky horizon. Take three full diaphragmatic breaths, assimilating the immensity of outer space.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.",
                "gps": "transit center or airport terminal",
                "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30, "aprendizaje": 60}
            },
            {
                "id": 309,
                "titulo": "Distracción Absoluta: Centro de Ocio / Parque Temático",
                "titulo_en": "Absolute Distraction: Leisure Center / Theme Park",
                "porque": "Bucle mental de apatía o rutina plana. Necesitas un shock visual de colores, sonidos y juego inocente.",
                "porque_en": "Mental loop of apathy or flat routine. You need a visual shock of colors, sounds, and innocent play.",
                "que_hacer": "Dirígete al parque de atracciones, centro de entretenimiento o zona recreativa (Arcade, Bowling) más cercana de tu perímetro. Observa las luces, escucha las risas del entorno urbano y permítete conectar con una dinámica de ocio simple para romper la inercia diurna.",
                "que_hacer_en": "Head to the nearest amusement park, entertainment center, or recreational zone (Arcade, Bowling) in your perimeter. Observe the lights, listen to the laughter of the urban environment, and allow yourself to connect with a simple leisure dynamic to break the daytime inertia.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.",
                "gps": "amusement park or arcade",
                "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50, "creatividad": 60}
            },
            {
                "id": 310,
                "titulo": "Exploración de Espacios: Módulo de Diseño Airbnb",
                "titulo_en": "Space Exploration: Airbnb Design Module",
                "porque": "Falta de inspiración y estancamiento estético. Visualizar arquitecturas alternativas expande tu mente.",
                "porque_en": "Lack of inspiration and aesthetic stagnation. Visualizing alternative architectures expands your mind.",
                "que_hacer": "Abre la aplicación de Airbnb de forma contemplativa. Filtra por diseños de cabañas o casas en árboles de tu estado. Analiza la organización del espacio, las texturas y los planos visuales como un ejercicio de ocio e imaginación sin la obligación de reservar.",
                "que_hacer_en": "Open the Airbnb app contemplatively. Filter by cabin designs or treehouses in your state. Analyze the organization of space, textures, and visual layouts as an exercise of leisure and imagination without the obligation to book.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Interfaz móvil desde tu zona de descanso habitual.", "donde_en": "Mobile interface from your usual resting space.",
                "gps": "local post office",
                "vector_necesidades": {"creatividad": 100, "contemplacion": 95, "juego": 70, "organizacion": 80, "esperanza": 85, "descanso": 60, "aprendizaje": 60}
            },
            {
                "id": 311,
                "titulo": "Mapeo de Flujos: Recorrido Perimetral Costco",
                "titulo_en": "Flow Mapping: Costco Perimeter Walk",
                "porque": "Rutina plana. Caminar por un entorno de suministro masivo altera tu percepción del consumo y activa tu cuerpo.",
                "porque_en": "Flat routine. Walking through a mass supply environment alters your perception of consumption and activates your body.",
                "que_hacer": "Dirígete al Costco o club de precios más cercano de tu geografía. Camina de forma constante a paso firme por los pasillos industriales de los perímetros. Observa los grandes volúmenes de suministros y usa la infraestructura gigante para forzar la contracción muscular de tus piernas.",
                "que_hacer_en": "Head to the nearest Costco or price club in your area. Walk steadily at a firm pace through the industrial perimeter aisles. Observe the large volumes of supplies and use the giant infrastructure to force muscular contraction in your legs.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pasillos industriales de un gran almacén de USA.", "donde_en": "Industrial aisles of a large USA warehouse store.",
                "gps": "wholesale club or warehouse",
                "vector_necesidades": {"movimiento": 85, "organizacion": 75, "comunidad": 60, "contemplacion": 60, "juego": 40, "descanso": 10, "silencio": 5}
            },
            {
                "id": 312,
                "titulo": "Sabotaje de Espera: Campus Universitario / Escuela",
                "titulo_en": "Waiting Sabotage: University Campus / School",
                "porque": "Bucle mental aburrido. Necesitas una inyección de aire fresco y entornos de aprendizaje para reenfocar tu Yo.",
                "porque_en": "Bored mental loop. You need an injection of fresh air and learning environments to refocus your Self.",
                "que_hacer": "Ubica el campus universitario o escuela pública más cercana. Camina en total silencio por sus áreas verdes y plazas comunes. Utiliza esta infraestructura ya financiada por el estado para respirar aire libre y observar el entorno con absoluta calma.",
                "que_hacer_en": "Locate the nearest university campus or public school. Walk in total silence through its green areas and common plazas. Use this state-funded infrastructure to breathe open air and observe the surroundings with absolute calm.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Áreas comunes abiertas de un campus universitario.", "donde_en": "Open common areas of a university campus.",
                "gps": "university campus or public school",
                "vector_necesidades": {"aprendizaje": 100, "aire_fresco": 95, "silencio": 90, "contemplacion": 85, "descanso": 70, "movimiento": 40}
            },
            {
                "id": 304,
                "titulo": "Soberanía en Tránsito: Escape Uber/Lyft",
                "titulo_en": "Sovereignty in Transit: Uber/Lyft Escape",
                "porque": "Inercia mental por estar estancado en casa. Necesitas un cambio geográfico rápido para alterar tus pensamientos.",
                "porque_en": "Mental inertia from being stuck at home. You need a rapid geographical change to alter your thoughts.",
                "que_hacer": "Abre tu aplicación de transporte (Uber/Lyft). Solicita un viaje corto hacia un perímetro público o parque que no conozcas. Durante el trayecto, suelta el teléfono, mira a través de la ventana de forma contemplativa y asimila la velocidad del entorno urbano.",
                "que_hacer_en": "Open your ride app (Uber/Lyft). Request a short ride to a public area or park you don't know. During the route, drop your phone, look through the window contemplatively, and assimilate the speed of the urban environment.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Asiento de pasajero en un coche de transporte urbano.", "donde_en": "Passenger seat in an urban transit vehicle.",
                "gps": "public transit hub or central park",
                "vector_necesidades": {"juego": 80, "movimiento": 70, "contemplacion": 85, "comunidad": 60, "descanso": 40, "silencio": 30, "esperanza": 80}
            },
            {
                "id": 305,
                "titulo": "Descompresión Visual: El Algoritmo de YouTube",
                "titulo_en": "Visual Decompression: The YouTube Algorithm",
                "porque": "Bucle cognitivo severo debido a la rutina monótona de la semana. Requieres un quiebre estético controlado.",
                "porque_en": "Severe cognitive loop due to the monotonous weekly routine. You require a controlled aesthetic break.",
                "que_hacer": "Abre YouTube de forma consciente. Busca '4K drone architecture relax' o filmaciones en cámara lenta de paisajes naturales. Observa la pantalla fijamente por dos minutos enteros, respirando de forma diafragmática para relajar tus músculos ciliares.",
                "que_hacer_en": "Open YouTube consciously. Search for '4K drone architecture relax' or slow-motion natural landscape footage. Watch the screen fixedly for two whole minutes while taking deep diaphragmatic breaths to relax your ciliary muscles.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Interfaz de tu teléfono en un rincón con luz tenue.", "donde_en": "Your phone interface in a dimly lit corner.",
                "gps": "local coffee lounge",
                "vector_necesidades": {"contemplacion": 100, "descanso": 90, "creatividad": 80, "esperanza": 90, "silencio": 50, "naturaleza": 70, "movimiento": 5}
            },
            {
                "id": 306,
                "titulo": "Inversión Controlada: Antojo Digital en Amazon",
                "titulo_en": "Controlled Investment: Digital Desire on Amazon",
                "porque": "Aburrimiento crónico y falta de micro-estímulos o pasatiempos que activen tu mente.",
                "porque_en": "Chronic boredom and lack of micro-stimuli or hobbies to activate your mind.",
                "que_hacer": "Abre la aplicación de Amazon. Busca un objeto microscópico que impulse un pasatiempo físico real (un libro de bolsillo, un pincel, una herramienta manual). Ejecuta la compra con la absoluta certeza de que estás invirtiendo en tu propia creatividad.",
                "que_hacer_en": "Open the Amazon app. Search for a microscopic object that drives a real physical hobby (a paperback book, a paintbrush, a manual tool). Complete the purchase with absolute certainty that you are investing in your own creativity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pantalla móvil desde tu espacio de descanso habitual.", "donde_en": "Mobile screen from your usual resting space.",
                "gps": "local post office",
                "vector_necesidades": {"juego": 90, "creatividad": 90, "esperanza": 95, "organizacion": 70, "descanso": 60, "aprendizaje": 80, "movimiento": 10}
            },            
            {
                "id": 301,
                "titulo": "Auditoría de Frecuencias: Discoteca / Club Night",
                "titulo_en": "Frequency Audit: Nightclub / Club Night",
                "porque": "Monotonía aplastante y falta de estímulos rítmicos o sociales en tu rutina semanal.",
                "porque_en": "Crushing monotony and lack of rhythmic or social stimuli in your weekly routine.",
                "que_hacer": "Visita una zona de discotecas o un club céntrico nocturno. Sal un momento al perímetro exterior o a la acera peatonal abierta. Escucha la vibración profunda del bajo golpeando la estructura física del edificio. Siente el pulso acelerado de la vida nocturna de USA para romper la inercia del piloto automático diurno.",
                "que_hacer_en": "Visit a club district or a downtown nightclub. Step outside to the outer perimeter or the open pedestrian sidewalk for a moment. Listen to the deep bass vibration hitting the building's physical structure. Feel the accelerated pulse of USA nightlife to break the daytime autopilot inertia.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior, terraza o área abierta de un club nocturno urbano.", "donde_en": "Outer perimeter, terrace, or open area of an urban nightclub.",
                "gps": "dance club or nightclub",
                "vector_necesidades": {"juego": 100, "musica": 100, "comunidad": 90, "risa": 80, "movimiento": 70, "creatividad": 60, "silencio": 10, "descanso": 30}
            },
            {
                "id": 302,
                "titulo": "Terapia de Pasillo: Recorrido Target / Walmart",
                "titulo_en": "Aisle Therapy: Target / Walmart Walk",
                "porque": "Estancamiento mental en casa y falta de variedad en tu entorno visual inmediato.",
                "porque_en": "Mental stagnation at home and lack of variety in your immediate visual environment.",
                "que_hacer": "Dirígete a una gran superficie comercial (Target, Walmart). Recorre los pasillos de forma contemplativa sin la obligación de comprar de forma compulsiva. Observa la organización, camina a paso firme forzando la contracción muscular para activar el flujo linfático de tus piernas.",
                "que_hacer_en": "Head to a large department store (Target, Walmart). Walk the aisles contemplatively without the obligation to shop compulsively. Observe the layout, walk steadily, forcing muscular contraction to activate the lymphatic flow in your legs.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gran superficie comercial o tienda céntrica en USA.", "donde_en": "Large department store or central shop in the USA.",
                "gps": "department store or retail",
                "vector_necesidades": {"movimiento": 80, "organizacion": 70, "contemplacion": 70, "comunidad": 60, "juego": 50, "descanso": 20, "silencio": 15}
            },
            {
                "id": 303,
                "titulo": "Sabotaje Alimenticio: Antojo Rápido McDonald's / Starbucks",
                "titulo_en": "Food Sabotage: Quick Treat McDonald's / Starbucks",
                "porque": "Falta de estímulos sensoriales y monotonía en tu alimentación de la semana.",
                "porque_en": "Lack of sensory stimuli and monotony in your food during the week.",
                "que_hacer": "Dirígete a la cadena de comida rápida o cafetería más cercana (McDonald's, Starbucks, Burger King). Pide un menú o un antojo específico. Disfrútalo bocado a bocado, completamente alejado de la pantalla del teléfono, prestando atención exclusiva al sabor real.",
                "que_hacer_en": "Head to the nearest fast-food chain or coffee shop (McDonald's, Starbucks, Burger King). Order a menu or a specific treat. Enjoy it bite by bite, completely away from your phone screen, paying exclusive attention to the real flavor.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cadena de comida rápida o cafetería local en tu Código Postal.", "donde_en": "Fast food chain or local coffee shop in your Zip Code.",
                "gps": "fast food or local restaurant",
                "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20}
            },            
            {
                "id": 253,
                "titulo": "Auditoría de Frecuencias: Escape Discoteca / Club",
                "titulo_en": "Frequency Audit: Nightclub / Club Escape",
                "porque": "Monotonía mental aplastante en tu semana. Necesitas un quiebre sensorial radical mediante ritmos y movimiento.",
                "porque_en": "Crushing mental monotony in your week. You need a radical sensory break through rhythm and movement.",
                "que_hacer": "Visita una zona de discotecas o un club céntrico nocturno en tu ciudad. Sal un momento al perímetro exterior del local, terraza o acera peatonal abierta. Escucha la vibración profunda del bajo golpeando la estructura física del edificio. Siente el cambio súbito de temperatura térmica del aire libre en tu piel, respira profundo por la nariz y permite que el pulso acelerado de la vida nocturna de USA rompa la inercia del piloto automático diurno.",
                "que_hacer_en": "Visit a club district or a downtown nightclub in your city. Step outside to the outer perimeter of the venue, terrace, or open pedestrian sidewalk for a moment. Listen to the deep bass vibration hitting the building's physical structure. Feel the sudden change in thermal temperature of the open air on your skin, breathe deeply through your nose, and let the accelerated pulse of USA nightlife break the daytime autopilot inertia.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior, terraza o área abierta de un club nocturno urbano.", "donde_en": "Outer perimeter, terrace, or open area of an urban nightclub.",
                "gps": "nightlife district or dance clubs",
                "vector_necesidades": {"juego": 100, "musica": 100, "comunidad": 90, "risa": 80, "movimiento": 70, "creatividad": 60, "silencio": 10, "descanso": 30}
            },
            {"id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market",
                "porque": "Necesitas nuevos estímulos. Sabores y olores frescos. Apoya lo local.", "porque_en": "Need new stimuli. Fresh tastes/smells. Support local.",
                "que_hacer": "Visita un mercado local. Prueba algo nuevo. Habla con los vendedores.", "que_hacer_en": "Visit local market. Try something new. Talk to vendors.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers market",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "silencio": 30, "agua": 10, "sol": 70, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 60, "juego": 40, "contemplacion": 50, "descanso": 30, "organizacion": 50, "alimentacion": 100, "musica": 30, "risa": 70, "esperanza": 80}
            },
            {"id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition",
                "porque": "Mente en bucle. Busca inspiración. Despierta tu creatividad.", "porque_en": "Mind in a loop. Seek inspiration. Awaken creativity.",
                "que_hacer": "Visita una galería o museo local. Observa el arte. Reflexiona en silencio.", "que_hacer_en": "Visit local gallery/museum. Observe art. Reflect in silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art gallery",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 70, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 30, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 10, "contemplacion": 95, "descanso": 60, "organizacion": 70, "alimentacion": 0, "musica": 60, "risa": 20, "esperanza": 85}
            },
            {"id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park",
                "porque": "Necesitas energía visual. Observa la libertad y el movimiento. Conéctate con el juego.", "porque_en": "Need visual energy. Observe freedom/movement. Connect with play.",
                "que_hacer": "Acércate a un skate park. Observa a los patinadores. Siente la vitalidad.", "que_hacer_en": "Go to a skate park. Watch skaters. Feel the vitality.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate park",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 30, "silencio": 20, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 80, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 60, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 70, "risa": 90, "esperanza": 90}
            },
            {"id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore",
                "porque": "Busca historias y conocimiento. Desconéctate del mundo digital. Nutre tu mente.", "porque_en": "Seek stories/knowledge. Disconnect from digital. Nourish mind.",
                "que_hacer": "Explora una librería de segunda mano. Busca títulos inesperados. Disfruta el aroma.", "que_hacer_en": "Explore used bookstore. Look for unexpected titles. Enjoy scent.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used bookstore",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 85, "agua": 0, "sol": 20, "sombra": 95, "aire_fresco": 40, "creatividad": 90, "comunidad": 30, "aprendizaje": 100, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 70, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 75}
            },
            {"id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema",
                "porque": "Necesitas un cambio de ambiente y una nueva perspectiva. Disfruta una historia en un entorno diferente.", "porque_en": "Need scene/perspective change. Enjoy story in new setting.",
                "que_hacer": "Asiste a una proyección de cine al aire libre. Sumérgete en la película y el ambiente.", "que_hacer_en": "Attend outdoor cinema. Immerse in film/atmosphere.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor cinema",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 40, "agua": 10, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "descanso": 70, "organizacion": 20, "alimentacion": 60, "musica": 70, "risa": 70, "esperanza": 85}
            },
            {"id": 221, "titulo": "Auditoría de Frecuencias: Discoteca / Club", "titulo_en": "Frequency Audit: Nightclub / Club",
                "porque": "Monotonía extrema y falta de estímulos rítmicos o sociales en tu semana.", "porque_en": "Extreme monotony, lack of rhythmic/social stimuli.",
                "que_hacer": "Visita un club/bar. Sal al exterior. Siente la música. Nota el aire y libérate de la inercia mental de la rutina.",
                "que_hacer_en": "Visit a club/bar. Step outside. Feel the music. Notice the air and break free from routine mental inertia.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior o zona abierta de un club nocturno.", "donde_en": "Outer perimeter or open area of a nightclub.",
                "gps": "nightlife district lounge",
                "vector_necesidades": {"juego": 100, "comunidad": 90, "musica": 90, "risa": 80, "creatividad": 70, "movimiento": 60, "silencio": 10, "descanso": 30}
            },
            {"id": 222, "titulo": "Hackeo Cognitivo: Galería / Cine / Teatro", "titulo_en": "Cognitive Hack: Gallery / Cinema / Theater",
                "porque": "Falta de inspiración y embotamiento por consumir contenido basura repetitivo.", "porque_en": "Lack of inspiration, dullness from repetitive junk content.",
                "que_hacer": "Ve al cine/museo/teatro local. Entra al vestíbulo. Elige un cartel/imagen. Obsérvalo fijamente, aislando tu mente del ruido. Usa el espacio como laboratorio de enfoque.",
                "que_hacer_en": "Head to local cinema/museum/theater. Enter lobby. Choose a poster/image. Stare, isolating mind from noise. Use space as visual focus lab.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Entrada pública de un centro cultural o cine.", "donde_en": "Public entrance of a cultural center or cinema.",
                "gps": "local cinema or museum",
                "vector_necesidades": {"creatividad": 100, "aprendizaje": 90, "contemplacion": 95, "juego": 60, "comunidad": 50, "descanso": 60, "silencio": 70}
            },
            {"id": 223, "titulo": "Sabotaje de Rutina: Salir a Comer / Fast Food", "titulo_en": "Routine Sabotage: Dining Out / Fast Food",
                "porque": "Falta de variedad sensorial. Salir por un antojo físico rompe la inercia del día de forma inmediata.", "porque_en": "Lack of sensory variety. A physical treat immediately breaks day's inertia.",
                "que_hacer": "Ve a un restaurante/fast food. Pide algo. Disfrútalo bocado a bocado, sin pantallas. Atiende al sabor y textura real.",
                "que_hacer_en": "Head to nearest restaurant/fast food. Order a treat. Enjoy bite by bite, no screens. Focus on real taste/texture.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cadena de comida rápida o restaurante del vecindario.", "donde_en": "Fast food chain or neighborhood restaurant.",
                "gps": "fast food or local restaurant",
                "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20}
            }
        ],
        "cansado": [
            {"id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading",
                "porque": "Necesitas calma. Aprende sin distracciones. Recarga tu energía.", "porque_en": "Need calm. Learn without distractions. Recharge energy.",
                "que_hacer": "Visita tu biblioteca local. Busca un libro o disfruta el silencio.", "que_hacer_en": "Visit your local library. Find a book or enjoy silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70}
            },
            {"id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk",
                "porque": "Necesitas despejar la mente. Aire fresco y vistas al agua. Caminata relajante.", "porque_en": "Need to clear mind. Fresh air, water views. Relaxing walk.",
                "que_hacer": "Camina por el muelle o puerto. Observa los barcos. Escucha el agua.", "que_hacer_en": "Walk along dock/harbor. Watch boats. Listen to water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90}
            },
            {
                "id": 328,
                "titulo": "Inversión Marítima: Perímetro de Cruceros / Muelles",
                "titulo_en": "Maritime Inversion: Cruise Line / Pier Perimeter",
                "porque": "Cansancio acumulado de la rutina diaria. Tu mente requiere el estímulo de la inmensidad del agua para disolver el encierro.",
                "porque_en": "Accumulated fatigue from the daily routine. Your mind requires the stimulus of vast water to dissolve confinement.",
                "que_hacer": "Dirígete al puerto, muelle o paseo marítimo más cercano de tu área (zonas de Royal Caribbean, Carnival). Observa las embarcaciones de forma contemplativa. Deja que el reflejo de la luz sobre el agua limpie la pesadez de tus pensamientos.",
                "que_hacer_en": "Head to the nearest port, pier, or boardwalk in your area (Royal Caribbean, Carnival zones). Observe the vessels contemplatively. Let the reflection of light on the water clear away the heaviness of your thoughts.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Muelle, puerto local o zona costera abierta.", "donde_en": "Dock, local pier, or open coastal zone.",
                "gps": "cruise terminal or pier",
                "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60, "esperanza": 85}
            },
            {
                "id": 329,
                "titulo": "Pausa en Ruta: Módulo de Descanso Interestatal",
                "titulo_en": "Route Break: Interstate Rest Stop Module",
                "porque": "Fatiga muscular y embotamiento cognitivo provocado por trayectos continuos y la inercia del asfalto.",
                "porque_en": "Muscular fatigue and cognitive dullness caused by continuous travel and asphalt inertia.",
                "que_hacer": "Busca la próxima área de servicio o descanso segura en tu ruta. Estaciona por completo, apaga el motor y sal del vehículo. Realiza un suave estiramiento de piernas, respira el aire del ambiente y camina despacio un minuto para reactivar tu circulación.",
                "que_hacer_en": "Find the next safe service or rest area on your route. Park completely, turn off the engine, and step out of the vehicle. Do a gentle leg stretch, breathe the ambient air, and walk slowly for one minute to reactivate circulation.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Área de servicio de autopista o zona de descanso pública.", "donde_en": "Highway service area or public rest zone.",
                "gps": "highway rest stop or plaza",
                "vector_necesidades": {"descanso": 95, "movimiento": 60, "aire_fresco": 90, "salud": 85, "silencio": 50, "contemplacion": 70, "organizacion": 40}
            },
            {
                "id": 330,
                "titulo": "Recuperación Pasiva: Paseo Histórico y Calma Urbana",
                "titulo_en": "Passive Recovery: Historical Walk and Urban Calm",
                "porque": "Agotamiento mental debido a la predictibilidad de la rutina diaria. Necesitas un suave cambio de ritmo.",
                "porque_en": "Mental exhaustion due to the predictability of the daily routine. You need a gentle change of pace.",
                "que_hacer": "Ubica una zona histórica, plaza antigua o monumento a pie en tu perímetro comercial. Camina a un paso deliberadamente lento, sin prisa. Observa las estructuras arquitectónicas antiguas y usa ese entorno público para despejar la mente.",
                "que_hacer_en": "Locate a historical zone, old plaza, or monument on foot within your commercial perimeter. Walk at a deliberately slow, unhurried pace. Observe the older architectural structures and use that public setting to clear your mind.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro histórico, plaza pública o calles peatonales.", "donde_en": "Historical center, public plaza, or pedestrian streets.",
                "gps": "historical landmark or walking tour",
                "vector_necesidades": {"aprendizaje": 90, "contemplacion": 95, "descanso": 80, "movimiento": 50, "silencio": 70, "creatividad": 60, "esperanza": 80}
            },
            {
                "id": 331,
                "titulo": "Aislamiento Sensorial: Butaca de Cine Matinal",
                "titulo_en": "Sensory Isolation: Morning Cinema Seat",
                "porque": "Saturación del sistema nervioso por exceso de interacción humana y demandas de la rutina urbana diaria.",
                "porque_en": "Nervous system saturation from excessive human interaction and demands of the daily urban routine.",
                "que_hacer": "Dirígete al cine o complejo de salas más cercano de tu Código Postal (AMC, Regal). Elige una función matinal o en horario de baja afluencia. Siéntate en la penumbra de la sala, suelta el teléfono y permite que la oscuridad y el aislamiento controlado calmen el ruido de tu mente.",
                "que_hacer_en": "Head to the nearest cinema or theater complex in your Zip Code (AMC, Regal). Choose a morning or low-traffic screening. Sit in the dim light of the hall, drop your phone, and allow the darkness and controlled isolation to quiet the noise in your mind.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sala de cine comercial o vestíbulo de proyecciones.", "donde_en": "Commercial movie theater or screening lobby.",
                "gps": "local cinema or amc",
                "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 90, "sombra": 100, "juego": 40, "creatividad": 50, "movimiento": 5}
            },
            {
                "id": 332,
                "titulo": "Homeostasis Verde: Descanso en Jardín Botánico / Invernadero",
                "titulo_en": "Green Homeostasis: Rest in Botanical Garden / Greenhouse",
                "porque": "Agotamiento crónico debido al asfalto, aire acondicionado de oficina y falta de conexión orgánica real.",
                "porque_en": "Chronic fatigue due to asphalt, office air conditioning, and lack of real organic connection.",
                "que_hacer": "Ubica el jardín botánico, invernadero público o parque floral más cercano. Busca un banco protegido por la vegetación. Permanece allí inmóvil por dos minutos enteros, respirando el aire limpio del ambiente y dejando que los tonos verdes relajen tu córtex visual.",
                "que_hacer_en": "Locate the nearest botanical garden, public greenhouse, or floral park. Find a bench sheltered by vegetation. Remain there motionless for two whole minutes, breathing the clean ambient air and letting the green tones relax your visual cortex.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín botánico público, vivero o parque natural regional.", "donde_en": "Public botanical garden, nursery, or regional nature park.",
                "gps": "botanical garden or nursery",
                "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "descanso": 90, "silencio": 80, "contemplacion": 95, "sombra": 90, "salud": 85, "movimiento": 25}
            },
            {
                "id": 333,
                "titulo": "Módulo de Quietud: Banco en Lago / Muelle Público",
                "titulo_en": "Quietness Module: Bench by a Public Lake / Pier",
                "porque": "Cansancio mental plano y monotonía. Necesitas observar el movimiento sutil de la naturaleza sin prisas.",
                "porque_en": "Flat mental fatigue and monotony. You need to observe the subtle movement of nature without haste.",
                "que_hacer": "Encuentra un parque local con lago, estanque o muelle público en tu Código Postal. Siéntate en el banco más cercano a la orilla. Observa las ondas del agua y el comportamiento de las aves del perímetro por un minuto completo, forzando a tu respiración a seguir un ritmo lento.",
                "que_hacer_en": "Find a local park with a lake, pond, or public pier in your Zip Code. Sit on the bench closest to the edge. Observe the water ripples and the behavior of the birds in the perimeter for a full minute, forcing your breathing to follow a slow pace.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Banco de parque junto a un estanque o lago público.", "donde_en": "Park bench next to a public pond or lake.",
                "gps": "public lake park or fountain",
                "vector_necesidades": {"agua": 100, "contemplacion": 100, "descanso": 95, "silencio": 75, "naturaleza": 85, "aire_fresco": 90, "movimiento": 15}
            },
            {"id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory",
                "porque": "Mente ansiosa. Busca perspectiva universal. Maravíllate con el cosmos.", "porque_en": "Anxious mind. Seek universal perspective. Marvel at cosmos.",
                "que_hacer": "Visita un observatorio. Aprende sobre el universo. Observa las estrellas (si es posible).", "que_hacer_en": "Visit observatory. Learn about universe. Stargaze (if possible).",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95}
            },
            {"id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza",
                "porque": "Necesitas observar. Conéctate con la vida urbana. Descansa y reflexiona.", "porque_en": "Need to observe. Connect with urban life. Rest and reflect.",
                "que_hacer": "Siéntate en un banco. Observa a la gente pasar. Siente el pulso de la ciudad.", "que_hacer_en": "Sit on bench. Watch people pass. Feel city's pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85}
            },
            {"id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour", # ID 129 duplicada eliminada
                "porque": "Mente agotada de lo predecible. Necesitas una inyección de conocimiento y un suave movimiento. Aprende mientras caminas.", "porque_en": "Mind tired of predictable. Need knowledge injection, gentle movement. Learn as you walk.",
                "que_hacer": "Busca un tour a pie gratuito o de bajo costo por tu ciudad. Descubre historias locales.", "que_hacer_en": "Find free/low-cost walking tour. Discover local stories.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90}
            },
            {"id": 231, "titulo": "Inversión Marítima: Perímetro de Cruceros", "titulo_en": "Maritime Inversion: Cruise Line Perimeter",
                "porque": "Cansancio monótono. Tu mente requiere el estímulo visual de la inmensidad del agua para romper el encierro urbano.", "porque_en": "Monotonous fatigue. Mind needs vast water stimulus to break urban confinement.",
                "que_hacer": "Ve al puerto/muelle/agencia de cruceros. Observa naves/horizonte marítimo. Deja que el reflejo del agua limpie tus pensamientos.",
                "que_hacer_en": "Head to nearest port/pier/cruise agency. Observe vessels/marine horizon. Let water reflection clear heavy thoughts.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Muelle, puerto o zona costera abierta.", "donde_en": "Dock, pier, or open coastal zone.",
                "gps": "cruise terminal or pier",
                "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60}
            },
            {"id": 232, "titulo": "Quiebre de Inercia: Discoteca / Club Nocturno", "titulo_en": "Inertia Break: Nightclub / Dance Club",
                "porque": "Cansancio cerebral por exceso de rutinas repetitivas y falta de estímulos rítmicos reales.", "porque_en": "Brain fatigue from repetitive routines, lack of real rhythmic stimuli.",
                "que_hacer": "Visita clubs/discotecas. Sal al área abierta. Escucha la vibración del bajo, siente la música. Deja que el pulso nocturno rompa el automatismo diurno.",
                "que_hacer_en": "Visit city clubs/nightlife. Step out to open area. Listen to bass, feel music. Let night's pulse break daytime automatism.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior o terraza de un club céntrico.", "donde_en": "Outer perimeter or terrace of a central club.",
                "gps": "dance club or nightclub",
                "vector_necesidades": {"musica": 100, "juego": 90, "comunidad": 80, "risa": 70, "movimiento": 60, "silencio": 10, "descanso": 40}
            }
        ],
        "ansioso": [
            {"id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water",
                "porque": "Agua en movimiento. Calma tu mente. Relaja tensiones.", "porque_en": "Moving water. Calm mind. Release tensions.",
                "que_hacer": "Busca fuente, lago o río cercano. Observa el flujo. Déjate llevar.", "que_hacer_en": "Find nearby fountain/lake/river. Observe flow. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80}
            },
            {"id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride",
                "porque": "Estrés acumulado. Necesitas desconexión total. Flota y relájate.", "porque_en": "Accumulated stress. Need total disconnection. Float and relax.",
                "que_hacer": "Realiza un paseo corto en bote. Siente la brisa. Observa la inmensidad del agua.", "que_hacer_en": "Take a short boat ride. Feel the breeze. Observe vast water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90}
            },
            {
                "id": 345,
                "titulo": "Distracción Absoluta: Centro de Recreación / Parque de Mascotas",
                "titulo_en": "Absolute Distraction: Recreation Center / Dog Park",
                "porque": "Ansiedad cíclica y rumiación mental masiva. Necesitas un shock de juego y risas para apagar el pánico del ego.",
                "porque_en": "Cyclic anxiety and massive mental rumination. You need a shock of play and laughter to quiet ego panic.",
                "que_hacer": "Dirígete al parque de perros, centro de entretenimiento o zona recreativa (Arcade/Bowling) más cercana de tu Código Postal. Observa las interacciones, escucha las risas y los sonidos del perímetro urbano. Permítete conectar con el juego inocente y la energía externa por un minuto completo para anular el bucle de pensamientos.",
                "que_hacer_en": "Head to the nearest dog park, entertainment center, or recreational zone (Arcade/Bowling) in your Zip Code. Observe the interactions, listen to the laughter and sounds of the urban perimeter. Allow yourself to connect with innocent play and external energy for a full minute to cancel the thought loop.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de perros local, zona infantil o centro de juegos.", "donde_en": "Local dog park, kids zone, or arcade center.",
                "gps": "dog park or amusement arcade",
                "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 90, "movimiento": 70, "esperanza": 95, "silencio": 20, "descanso": 50, "creatividad": 40}
            },
            {
                "id": 346,
                "titulo": "Aislamiento Conciencial: Resort / Lobby de Hotel Boutique",
                "titulo_en": "Conscious Isolation: Resort / Boutique Hotel Lobby",
                "porque": "Ansiedad social aguda y ruido mental provocado por la sobrecarga de responsabilidades económicas.",
                "porque_en": "Acute social anxiety and mental noise caused by economic responsibilities overload.",
                "que_hacer": "Visita la zona de descanso o el jardín de un hotel de cadena o resort local (Marriott, Hilton). Siéntate de forma gratuita en una de sus butacas premium del lobby público. Cierra los ojos por 60 segundos enteros, respira a un ritmo lento diafragmático y habita tu propio cuerpo en total quietud.",
                "que_hacer_en": "Visit the lounge area or garden of a chain hotel or local resort (Marriott, Hilton). Sit for free in one of the public lobby's premium armchairs. Close your eyes for 60 whole seconds, take slow diaphragmatic breaths, and inhabit your own body in total stillness.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Zona de descanso, jardín interior o lobby de un hotel de USA.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.",
                "gps": "boutique hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 95, "contemplacion": 95, "organizacion": 80, "salud": 90, "esperanza": 90, "sombra": 80}
            },
            {
                "id": 347,
                "titulo": "Estrategia de Alivio: Terminal de Aerolíneas",
                "titulo_en": "Relief Strategy: Airline Terminal",
                "porque": "Sensación de asfixia y pánico por el encierro diario de la rutina laboral de USA.",
                "porque_en": "Feeling of suffocation and panic from the daily confinement of the USA work routine.",
                "que_hacer": "Si estás cerca de una terminal aérea (Delta, United) o una central de transportes, camina hacia el vestíbulo principal. Despega los ojos de la pantalla, observa a los viajeros partir y asimila mentalmente que el mundo es inmenso y que tu problema actual es transitorio.",
                "que_hacer_en": "If near an airline terminal (Delta, United) or transit center, walk to the main lobby. Take your eyes off the screen, watch travelers depart, and mentally assimilate that the world is huge and your current issue is transient.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Vestíbulo público de aeropuerto o central de transportes regional.", "donde_en": "Public airport lobby or regional transit hub.",
                "gps": "transit center or airport terminal",
                "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 60, "movimiento": 40, "aprendizaje": 50}
            },
            {
                "id": 348,
                "titulo": "Módulo de Silencio Comunitario: Cafetería Local",
                "titulo_en": "Community Silence Module: Local Coffee Shop",
                "porque": "Aislamiento mental destructivo y parálisis por ansiedad. Necesitas estar rodeado de flujos humanos tranquilos.",
                "porque_en": "Destructive mental isolation and anxiety paralysis. You need to be surrounded by calm human flows.",
                "que_hacer": "Dirígete a una cafetería local tranquila o un rincón de Starbucks. Pide una bebida tibia o agua. Siéntate en un rincón, no mires las redes sociales, simplemente observa los movimientos pausados de las personas y el aroma del café para desacelerar tu pulso.",
                "que_hacer_en": "Head to a quiet local coffee shop or a Starbucks corner. Order a warm drink or water. Sit in a corner, don't check social media, simply observe the slow movements of people and the aroma of coffee to decelerate your pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cafetería o establecimiento de bebidas local en tu Código Postal.", "donde_en": "Local coffee shop or beverage venue in your Zip Code.",
                "gps": "quiet cafe or bakery",
                "vector_necesidades": {"comunidad": 90, "descanso": 85, "silencio": 75, "alimentacion": 60, "contemplacion": 80, "esperanza": 85, "musica": 30}
            },
            {"id": 123, "titulo": "Jardín de Rocas/Zen", "titulo_en": "Rock/Zen Garden",
                "porque": "Mente agitada. Busca orden y armonía. Centra tus pensamientos.", "porque_en": "Agitated mind. Seek order/harmony. Center thoughts.",
                "que_hacer": "Encuentra un jardín de rocas. Observa las formas y la disposición. Medita en su calma.", "que_hacer_en": "Find rock garden. Observe shapes/arrangement. Meditate in its calm.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90}
            },
            {"id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park",
                "porque": "Necesitas risas y alegría. Observa el juego inocente. Contagia la energía positiva.", "porque_en": "Need laughter/joy. Observe innocent play. Catch positive energy.",
                "que_hacer": "Visita un parque de perros. Observa su interacción. Siente la diversión.", "que_hacer_en": "Visit a dog park. Observe interaction. Feel the fun.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90}
            },
            {"id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music",
                "porque": "Mente estresada. Necesitas una experiencia sensorial. Permite que la música te calme.", "porque_en": "Stressed mind. Need sensory experience. Let music calm you.",
                "que_hacer": "Encuentra un lugar con música en vivo tranquila. Escucha, relájate y disfruta.", "que_hacer_en": "Find place with calm live music. Listen, relax, enjoy.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85}
            },
            {"id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool",
                "porque": "Cuerpo tenso, mente agitada. El agua relaja y el movimiento controlado calma. Flota tus preocupaciones.", "porque_en": "Tense body, agitated mind. Water relaxes, movement calms. Float worries away.",
                "que_hacer": "Visita una piscina pública, date un chapuzón o simplemente relájate en el agua.", "que_hacer_en": "Visit public pool, take a dip or just relax in water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85}
            },
            {"id": 241, "titulo": "Distracción Absoluta: Centro de Recreación / Parque Temático", "titulo_en": "Absolute Distraction: Recreation Center / Theme Park",
                "porque": "Ansiedad cíclica y rumiación mental masiva. Necesitas un shock de juego y risas para apagar el pánico del ego.", "porque_en": "Cyclic anxiety, massive rumination. Need play/laughter shock to quiet ego panic.",
                "que_hacer": "Ve al parque de atracciones/centro familiar. Observa colores, risas. Conecta con el juego inocente de los niños.",
                "que_hacer_en": "Head to nearest amusement park/family entertainment. Observe colors, laughter. Connect with innocent play.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.",
                "gps": "amusement park or arcade",
                "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50}
            },
            {"id": 242, "titulo": "Estrategia de Alivio: Terminal de Aerolíneas", "titulo_en": "Relief Strategy: Airline Terminal",
                "porque": "Sensación de asfixia y pánico por el encierro diario de la rutina laboral de USA.", "porque_en": "Suffocation/panic from daily USA work routine confinement.",
                "que_hacer": "Cerca de terminal aérea/agencia viajes, camina pasillo central. Despega ojos de pantalla. Observa viajeros, asimila que el mundo es inmenso y tu problema transitorio.",
                "que_hacer_en": "Near airline terminal/travel agency, walk central hall. Eyes off screen. Watch travelers, grasp world's vastness, your problem is transient.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.",
                "gps": "transit center or airport terminal",
                "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30}
            },
            {"id": 243, "titulo": "Aislamiento Conciencial: Resort / Hotel Lounge", "titulo_en": "Conscious Isolation: Resort / Hotel Lounge",
                "porque": "Ansiedad social aguda y ruido mental por sobrecarga de responsabilidades económicas.", "porque_en": "Acute social anxiety, mental noise from economic overload.",
                "que_hacer": "Visita lounge de hotel/resort (gratis). Siéntate en butaca premium. Cierra ojos, respira lento diafragmático. Habita tus órganos con presencia absoluta.",
                "que_hacer_en": "Visit hotel lounge/resort (free). Sit in premium armchair. Close eyes, breathe slow diaphragmatic. Fully inhabit your organs.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Zona de descanso o jardín de un hotel de USA.", "donde_en": "Lounge or garden of a USA hotel.",
                "gps": "boutique hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 95, "organizacion": 80, "salud": 85, "esperanza": 85}
            },
            {"id": 244, "titulo": "Soberanía de Cabina: Terminal Aérea / Vuelos", "titulo_en": "Cabin Sovereignty: Air Terminal / Flights",
                "porque": "Sensación de asfixia, pánico y desconexión corporal debido a la saturación ruidosa de los perímetros urbanos.", "porque_en": "Suffocation, panic, bodily disconnection due to noisy urban saturation.",
                "que_hacer": "Ve a aeropuerto/terminal de vuelos. Busca ventanal con vista al cielo. Ejecuta el Módulo de Ventilación: 3 exhalaciones diafragmáticas vaciando CO2. Eres libre.",
                "que_hacer_en": "Head to airport/flight terminal. Find wide sky-view window. Execute Ventilation Module: 3 diaphragmatic exhalations emptying CO2. You are free.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Terminal de aeropuerto, central de tránsito o zona de observación abierta.", "donde_en": "Airport terminal, transit hub, or open observation zone.",
                "gps": "airport terminal or transit hub",
                "vector_necesidades": {"aire_fresco": 95, "contemplacion": 100, "esperanza": 90, "descanso": 70, "silencio": 60, "movimiento": 30}
            }
        ]
    }
}

BIG_TECH_RESOURCES = {
    "spotify_audio_es": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_es": "https://www.youtube.com/results?search_query=sonidos+naturaleza+relajantes",
    "spotify_audio_en": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_en": "https://www.youtube.com/results?search_query=nature+sounds+relaxing",
}

# ============================================================
# CWRE V2
# SCORE INTELIGENTE (REFINADO)
# ============================================================
def score_coincidencia(
    perfil_local,
    vector_necesidades,
    historial=None,
    mission_id=None
):
    historial = historial or []
    score = 0
    # --------------------------------------------------
    # Coincidencia principal: Cuanto más cerca esté la necesidad
    # del usuario del objetivo de la misión, mayor el score.
    # --------------------------------------------------
    for necesidad, objetivo in vector_necesidades.items():
        if necesidad == "indicador_ansiedad":
            continue
        usuario = perfil_local.get(necesidad, DEFAULT_NECESSITY_VECTOR.get(necesidad, 50))
        diferencia = abs(usuario - objetivo)
        score += (100 - diferencia) * 0.5 # Ponderación base

    # --------------------------------------------------
    # Priorizar necesidades insatisfechas (altas en perfil)
    # y que la misión las cubra bien.
    # --------------------------------------------------
    for necesidad, valor_usuario in perfil_local.items():
        if necesidad == "indicador_ansiedad":
            continue
        # Si la necesidad del usuario es alta (insatisfecha) y la misión también tiene un alto objetivo para esa necesidad
        if valor_usuario > 70 and vector_necesidades.get(necesidad, 0) > 70:
            score += (valor_usuario * 0.3) # Bonificación fuerte
        elif valor_usuario > 50 and vector_necesidades.get(necesidad, 0) > 50:
            score += (valor_usuario * 0.1) # Bonificación moderada

    # --------------------------------------------------
    # Priorizar ansiedad: Misiones que atienden directamente la ansiedad.
    # --------------------------------------------------
    ansiedad = perfil_local.get("indicador_ansiedad", 0)
    if ansiedad >= 70: # Nivel alto de ansiedad
        score += vector_necesidades.get("silencio", 0) * 0.5
        score += vector_necesidades.get("descanso", 0) * 0.5
        score += vector_necesidades.get("esperanza", 0) * 0.4
        score += vector_necesidades.get("naturaleza", 0) * 0.3
        score += vector_necesidades.get("agua", 0) * 0.3
    elif ansiedad >= 40: # Nivel medio de ansiedad
        score += vector_necesidades.get("descanso", 0) * 0.2
        score += vector_necesidades.get("silencio", 0) * 0.2
   
    # --------------------------------------------------
    # Penalización por repetición histórica y bonus por exploración
    # --------------------------------------------------
    if mission_id is not None:
        score -= penalizacion_historial(mission_id, historial)
        score += bonus_exploracion(mission_id, historial)
   
    return round(max(0, score), 2)

# ============================================================
# Selección por Ranking Inteligente
# ============================================================
def seleccionar_por_ranking(candidatos):
    if not candidatos:
        return None
   
    candidatos = sorted(candidatos, key=lambda x: x["score"], reverse=True)
   
    if not candidatos:
        return None

    mejor_score = candidatos[0]["score"]
   
    # Si todos tienen un score bajo, y todos son iguales, elige uno al azar.
    if mejor_score <= 100: # Umbral para considerar que los scores son "bajos"
        scores_unicos = {c["score"] for c in candidatos}
        if len(scores_unicos) == 1:
            return random.choice(candidatos)

    # Considerar un umbral dinámico para seleccionar entre los mejores
    score_umbral = max(mejor_score * 0.8, mejor_score - 150) # El 80% del mejor o 150 puntos menos que el mejor
   
    mejores_candidatos_para_eleccion = [
        c for c in candidatos if c["score"] >= score_umbral
    ]
   
    if not mejores_candidatos_para_eleccion: # Si el umbral fue demasiado estricto, relaja y toma del top 3
        mejores_candidatos_para_eleccion = candidatos[:min(3, len(candidatos))]
        if not mejores_candidatos_para_eleccion: return None

    pesos = [c["score"] for c in mejores_candidatos_para_eleccion]
    # Asegúrate de que ningún peso sea cero o negativo para random.choices
    pesos = [max(1, p) for p in pesos]

    return random.choices(mejores_candidatos_para_eleccion, weights=pesos, k=1)[0]


# ============================================================
# CWRE V2
# Selector Universal de Misiones
# ============================================================
def seleccionar_mision_inteligente(
    misiones,
    perfil_local,
    historial=None
):
    historial = historial or []
    candidatos = []
    for mision in misiones:
        mission_vector = mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
       
        score = score_coincidencia(
            perfil_local=perfil_local,
            vector_necesidades=mission_vector,
            historial=historial,
            mission_id=mision["id"]
        )
        candidatos.append({
            "mision": mision,
            "score": score
        })
    seleccion = seleccionar_por_ranking(candidatos)
    if seleccion is None:
        return random.choice(misiones) if misiones else None
    return seleccion["mision"]

# ============================================================
# CWRE V2.1
# Seleccionar N misiones inteligentes y diversas (para modo SALIR)
# ============================================================
def seleccionar_n_misiones_inteligentes(
    n,
    misiones,
    perfil_local,
    historial_actual=None
):
    historial_actual = historial_actual or []
    candidatos_base = []
    for mision in misiones:
        mission_vector = mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
        score = score_coincidencia(
            perfil_local=perfil_local,
            vector_necesidades=mission_vector,
            historial=historial_actual,
            mission_id=mision["id"]
        )
        candidatos_base.append({
            "mision": mision,
            "score": score
        })

    candidatos_base.sort(key=lambda x: x["score"], reverse=True)
   
    seleccionadas = []
    ids_seleccionados = set()
   
    # Prioriza las de mayor score y las que no estén en el historial
    for cand in candidatos_base:
        if len(seleccionadas) >= n:
            break
        if cand["mision"]["id"] not in ids_seleccionados and cand["mision"]["id"] not in historial_actual:
            es_diversa = True
            for sel_mision in seleccionadas:
                distancia = diversidad_vector(
                    cand["mision"].get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                    sel_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
                )
                # Define un umbral de diversidad. Si son muy parecidas, no la elijas.
                if distancia < 100: # Ajusta este umbral según sea necesario para la diversidad
                    es_diversa = False
                    break
            if es_diversa:
                seleccionadas.append(cand["mision"])
                ids_seleccionados.add(cand["mision"]["id"])
   
    # Si aún no tenemos suficientes, toma las siguientes mejores aunque no sean tan diversas
    for cand in candidatos_base:
        if len(seleccionadas) >= n:
            break
        if cand["mision"]["id"] not in ids_seleccionados and cand["mision"]["id"] not in historial_actual:
            seleccionadas.append(cand["mision"])
            ids_seleccionados.add(cand["mision"]["id"])

    # Si todavía no tenemos suficientes, y el historial se ha agotado, reinicia y toma al azar
    if len(seleccionadas) < n and len(misiones) >= n:
        temp_misiones = [m for m in misiones if m["id"] not in ids_seleccionados]
        if len(temp_misiones) < n - len(seleccionadas):
            temp_misiones = misiones # Si no hay suficientes nuevas, recicla todo el catálogo
        random.shuffle(temp_misiones)
        for mision in temp_misiones:
            if len(seleccionadas) >= n:
                break
            if mision["id"] not in ids_seleccionados:
                seleccionadas.append(mision)
                ids_seleccionados.add(mision["id"])

    # Asegúrate de que el resultado final sea exactamente 'n' misiones si es posible
    while len(seleccionadas) < n and len(misiones) > len(seleccionadas):
        mision_aleatoria = random.choice(misiones)
        if mision_aleatoria["id"] not in ids_seleccionados:
            seleccionadas.append(mision_aleatoria)
            ids_seleccionados.add(mision["id"])

    return seleccionadas[:n]


# ============================================================
# Filtrar historial (para disponibilidad de misiones)
# ============================================================
def filtrar_historial(misiones, historial):
    historial = historial or []
    disponibles = [
        m
        for m in misiones
        if m["id"] not in historial
    ]
    return disponibles

# ============================================================
# CASA V2
# Selección inteligente de misiones domésticas
# ============================================================
def seleccionar_misiones_casa_inteligente(
    misiones,
    perfil_local,
    historial_casa=None,
    cantidad=3
):
    historial_casa = historial_casa or []
   
    disponibles = filtrar_historial(
        misiones,
        historial_casa
    )
   
    if len(disponibles) < cantidad * 2: # Si quedan muy pocas sin repetir, considera todo el catálogo de nuevo
        disponibles = misiones

    candidatos = []
    for mision in disponibles:
        mission_vector = mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)

        score = score_coincidencia(
            perfil_local=perfil_local,
            vector_necesidades=mission_vector,
            historial=historial_casa,
            mission_id=mision.get("id")
        )
        candidatos.append({
            "mision": mision,
            "score": score
        })
   
    candidatos.sort(
        key=lambda x: x["score"],
        reverse=True
    )
   
    resultado = []
    ids_en_resultado = set()
   
    # Intenta seleccionar misiones diversas y de alto score
    for candidato in candidatos:
        mision = candidato["mision"]
        if mision["id"] in ids_en_resultado:
            continue

        es_diversa = True
        for anterior_mision in resultado:
            distancia = diversidad_vector(
                mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                anterior_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
            )
            if distancia < 60: # Umbral de diversidad para misiones CASA
                es_diversa = False
                break
       
        if es_diversa:
            resultado.append(mision)
            ids_en_resultado.add(mision["id"])
       
        if len(resultado) >= cantidad:
            break
           
    # Si no se alcanzan las 'cantidad' requeridas con diversidad, añade las siguientes mejores
    if len(resultado) < cantidad:
        for candidato in candidatos:
            mision = candidato["mision"]
            if mision["id"] not in ids_en_resultado:
                resultado.append(mision)
                ids_en_resultado.add(mision["id"])
            if len(resultado) >= cantidad:
                break
   
    # Fallback final: si aún no hay suficientes, toma las primeras 'cantidad'
    if len(resultado) < cantidad and len(misiones) >= cantidad:
        resultado = [c["mision"] for c in candidatos[:cantidad]]
       
    return resultado

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
    estado = str(payload.get("estado", "FL")).strip() # Estado no se utiliza directamente en el motor de URL query params, es un placeholder
    region = str(payload.get("region", "")).strip() # Region no se utiliza directamente en el motor de URL query params, es un placeholder
    mente = str(payload.get("mente", "aburrido")).lower()
    budget = str(payload.get("budget", "0"))
    perfil_tipo = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    lang = str(payload.get("lang", "es")).lower()
   
    if zip_code and not re.fullmatch(r"^\d{5}$", zip_code):
        return JSONResponse({"error": "Código Postal inválido. Debe ser 5 dígitos numéricos."}, status_code=400)
   
    perfil_local = payload.get("perfil_local", {})
    if not isinstance(perfil_local, dict):
        perfil_local = {}
   
    perfil_local = {
        **DEFAULT_NECESSITY_VECTOR,
        **{k: v for k, v in perfil_local.items() if k in DEFAULT_NECESSITY_VECTOR or k == "indicador_ansiedad"}
    }
    if "indicador_ansiedad" not in perfil_local:
        perfil_local["indicador_ansiedad"] = 0
       
    # ==========================================================================================
    # MANIFIESTO MATRICIAL ABSOLUTO: TRADUCTOR PARÁSITO E INTERCEPTOR RECONFIGURADO V2
    # === MODIFICACIÓN: LÓGICA DE DETECCIÓN Y GENERACIÓN DE MENSAJES CONCISOS ===
    # ==========================================================================================
    sensitive_keywords = [
        "trabajo", "empleo", "job", "jobs", "work", "career", "interview", "resume", "cv", "curriculum", "linkedin", "indeed", "networking", "cliente", "client", "empresa", "company", "income", "earn money", "ganar dinero", "producir", "productividad", "buscar oportunidades", "buscar ofertas", "enviar currículo", "actualizar linkedin", "conseguir empleo", "salir a buscar trabajo", "metas profesionales", "presion economica", "presión económica", "biles", "deudas", "misery", "exploitation", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "economy", "oportunidades laborales", "solicitudes de empleo", "visitar empresas", "buscando clientes", "producir dinero", "obligaciones laborales", "responsabilidades", "tareas", "negocio", "negocios", "presión", "presiones"
    ]
   
    force_recovery_mission = False
    explicitly_seeking_job = any(phrase in desahogo for phrase in ["quiero buscar trabajo", "necesito un empleo", "busco trabajo", "find a job", "looking for work"])
   
    # DETECCIÓN DE SÍNTOMAS CORPORATIVOS O AMBIENTALES DEL ENTORNO DE USA
    marca_detectada = None
    if desahogo and not explicitly_seeking_job:
        desahogo_lower = desahogo.lower()
        for keyword in ["walmart", "amazon", "costco", "starbucks", "mcdonald", "spotify", "youtube", "tiktok", "instagram"]: # Agregadas marcas de redes
            if keyword in desahogo_lower:
                marca_detectada = keyword.capitalize()
                break
        if marca_detectada: # Solo forzar si se detectó una marca
             force_recovery_mission = True

    # INVERSIÓN SISTÉMICA CRÍTICA: SI HAY SÍNTOMA CORPORATIVO, NO HUYES A CASA, EJECUTAS UN CONTRAATAQUE DE CAMPO
    if force_recovery_mission and marca_detectada:
        mente_str_es = mente.upper()
        mente_str_en = mente.upper()

        diagnostico_sintoma_es = f"Diagnóstico: El cliente experimenta [{mente_str_es}] en relación al estímulo corporativo [{marca_detectada}] en Zip Code {zip_code}."
        diagnostico_sintoma_en = f"Diagnostic: Client experiences [{mente_str_en}] linked to corporate stimulus [{marca_detectada}] in Zip Code {zip_code}."

        instruccion_fisiologica_es = ""
        instruccion_fisiologica_en = ""
       
        if marca_detectada == "Walmart":
            instruccion_fisiologica_es = "Estás en el templo del consumo. Hackea: detén tu marcha, inhala/exhala profundo. Repite: 'Yo soy el único producto que importa hoy'. Sal de la rutina."
            instruccion_fisiologica_en = "You are in the consumption temple. Hack it: stop, inhale/exhale deeply. Repeat: 'I am the only product that matters today'. Exit routine."
        elif marca_detectada == "Amazon":
            instruccion_fisiologica_es = "Tu mente busca dopamina rápida. Bloquea la pantalla. Enfócate en tu espacio biológico: hidrátate o elimina toxinas. Invierte en tus células, no en el mercado digital."
            instruccion_fisiologica_en = "Mind seeks quick dopamine. Block screen. Focus on biological space: hydrate or detox. Invest in cells, not digital market."
        elif marca_detectada in ["Youtube", "Tiktok", "Instagram"]:
            instruccion_fisiologica_es = "El algoritmo secuestra tu atención. Interrumpe el bucle mental. Suelta el teléfono, cierra ojos 60 segundos. Respira profundo, libera estrés."
            instruccion_fisiologica_en = "Algorithm hijacks attention. Break mental loop. Drop phone, close eyes 60 secs. Breathe deep, release stress."
        elif marca_detectada == "Spotify":
            instruccion_fisiologica_es = "Usas sonidos para aislarte. Detén el audio. Ejecuta el Módulo Silencio Mental 1 minuto. Siente tu ritmo cardíaco en este Código Postal."
            instruccion_fisiologica_en = "You use sounds to isolate. Stop audio. Execute 1-minute Mental Silence Module. Feel your heart rhythm in this Zip Code."
        else: # Default case
            instruccion_fisiologica_es = f"Identificaste que [{marca_detectada}] satura tu mente. Rebélate: usa pasillos, aire libre o ventanas. Haz una pausa biológica profunda de 60 segundos. Recupera el control."
            instruccion_fisiologica_en = f"You identified [{marca_detectada}] saturating your mind. Rebel: use halls, open air, or windows. Take a deep 60-sec biological pause. Regain control."

        query_mapa_url = urllib.parse.quote_plus(f"{marca_detectada} in {zip_code}")
        target_link = f"{link_base}{query_mapa_url}"

        final_misiones_para_frontend = [{
            "destino_id": 999,
            "destino_titulo": f"HACKEO A {marca_detectada.upper()}",
            "destino_titulo_en": f"HACKING {marca_detectada.upper()}",
            "que_hacer": "Interrupción de Control Mental y Retorno al Cuerpo.",
            "que_hacer_en": "Mental Control Interruption & Return to Body.",
            "destino_entorno": "PERÍMETRO DE ACCIÓN DE CAMPO",
            "destino_instruccion": instruccion_fisiologica_es, # Instrucción concisa ES
            "destino_instruccion_en": instruccion_fisiologica_en, # Instrucción concisa EN
            "destino_coordenadas_gps": target_link,
            "vector_entorno_seleccionado": {**DEFAULT_NECESSITY_VECTOR, "homeostasis_urgente": True},
            "diagnostico_sintoma_es": diagnostico_sintoma_es,
            "diagnostico_sintoma_en": diagnostico_sintoma_en,
        }]

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "misiones": final_misiones_para_frontend,
            "historial_salir_actualizado": payload.get("historial_salir", []),
            "forced_recovery": True
        })

    # CONTINUACIÓN CONTINUA DEL FLUJO DE TRABAJO BASE DE LA PLATAFORMA OPEN THAN GO
    # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA)
    if opcion_usuario == "CASA":
        idioma = "EN" if lang.lower() == "en" else "ES"
        misiones_completas = BASE_MISIONES[f"CASA_{idioma}"]
        historial_casa = payload.get("historial_casa", [])
        misiones_casa = seleccionar_misiones_casa_inteligente(misiones_completas, perfil_local, historial_casa, cantidad=3)
        for m in misiones_casa:
            historial_casa = actualizar_historial(historial_casa, m["id"], MAX_HISTORY_CASA)
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": misiones_casa,
            "historial_casa_actualizado": historial_casa
        })
       
    # ==============================================================================
    # 2. ACTION DE CAMPO (MODO SALIR - SELECCIÓN PREDICTIVA ORIGINAL)
    # ==============================================================================
    opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
    historial_salir = payload.get("historial_salir", [])
   
    misiones_seleccionadas_raw = seleccionar_n_misiones_inteligentes(
        n=3,
        misiones=opciones_salir_candidatas,
        perfil_local=perfil_local,
        historial_actual=historial_salir
    )
   
    final_misiones_para_frontend = []
   
    for info_seleccionada in misiones_seleccionadas_raw:
        # === MODIFICACIÓN: MENSAJES DE ACOMPAÑAMIENTO Y GASTO ACORTADOS ===
        precio_real = ""
        if budget == "0":
            precio_real = "GASTO: Cero. Recarga sin costo." if lang == "es" else "COST: Zero. Free recharge."
        elif budget == "1":
            precio_real = "GASTO: Bajo. Pequeño gusto." if lang == "es" else "COST: Low. Small treat."
        elif budget == "2":
            precio_real = "GASTO: Libre. Tu escape." if lang == "es" else "COST: Free. Your escape."

        quienes_van = ""
        if perfil_tipo == "solo":
            quienes_van = "ACOMPAÑAMIENTO: Solo. Reconecta." if lang == "es" else "COMPANIONSHIP: Solo. Reconnect."
        elif perfil_tipo == "familia":
            quienes_van = "ACOMPAÑAMIENTO: Familia. Desahogo." if lang == "es" else "COMPANIONSHIP: Family. Unwind."
        elif perfil_tipo == "accesible":
            quienes_van = "ACOMPAÑAMIENTO: Ruta accesible. Sin barreras." if lang == "es" else "COMPANIONSHIP: Accessible route. No barriers."

        titulo_ganador = info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) if lang == "en" else info_seleccionada["titulo"]
        donde_base = info_seleccionada.get("donde_en", info_seleccionada["donde"]) if lang == "en" else info_seleccionada["donde"]
        anclaje_geografico = zip_code
        map_base_url = link_base

        if lang == "en":
            # === MODIFICACIÓN: guia_masticada (EN) ACORTADA ===
            guia_masticada = (
                f"TARGET: {info_seleccionada.get('titulo_en', info_seleccionada['titulo']) or ''}.\n"
                f"WHAT TO DO: {info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''}\n"
                f"WHY: {info_seleccionada.get('porque_en', info_seleccionada['porque']) or ''}\n"
                f"WHEN: {info_seleccionada.get('cuando_en', info_seleccionada['cuando']) or ''}\n"
                f"FOR WHAT: {info_seleccionada.get('para_que_en', info_seleccionada['para_que']) or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador_lang = (info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) or "").upper()
            que_hacer_lang = info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''
        else:
            # === MODIFICACIÓN: guia_masticada (ES) ACORTADA ===
            guia_masticada = (
                f"DESTINO: {info_seleccionada['titulo'] or ''}.\n"
                f"POR QUÉ: {info_seleccionada['porque'] or ''}\n"
                f"QUÉ HACER: {info_seleccionada['que_hacer'] or ''}\n"
                f"CUÁNDO: {info_seleccionada['cuando'] or ''}\n"
                f"PARA QUÉ: {info_seleccionada['para_que'] or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador_lang = (info_seleccionada["titulo"] or "").upper()
            que_hacer_lang = info_seleccionada["que_hacer"] or ""

        search_query_parts = []
        if perfil_tipo == "accesible":
            search_query_parts.append("wheelchair accessible")
        elif perfil_tipo == "familia":
            search_query_parts.append("family friendly")

        search_query_parts.append(info_seleccionada["gps"])
        search_query_parts.append(f"in {anclaje_geografico}")

        full_map_query_string = " ".join(search_query_parts)
        target_link = f"{map_base_url}{urllib.parse.quote_plus(full_map_query_string)}"

        final_vector_necesidades = {**DEFAULT_NECESSITY_VECTOR, **info_seleccionada.get("vector_necesidades", {})}

        final_misiones_para_frontend.append({
            "destino_id": info_seleccionada.get("id"),
            "destino_titulo": titulo_ganador_lang,
            "destino_titulo_en": info_seleccionada.get("titulo_en", info_seleccionada["titulo"]),
            "que_hacer": info_seleccionada["que_hacer"],
            "que_hacer_en": info_seleccionada.get("que_hacer_en", info_seleccionada["que_hacer"]),
            "destino_entorno": donde_base,
            "destino_instruccion": guia_masticada.strip(),
            "destino_instruccion_en": guia_masticada.strip(), # Ambos usan el mismo guia_masticada que ya fue construido en el idioma correcto
            "destino_coordenadas_gps": target_link,
            "vector_entorno_seleccionado": final_vector_necesidades,
        })

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "misiones": final_misiones_para_frontend,
        "historial_salir_actualizado": historial_salir
    })

# ==============================================================================
# APERTURA NATIVA DEL SERVIDOR FASTAPI (SINOPSIS ESTRUCTURAL DE CIERRE)
# ==============================================================================
if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

import os,time,sqlite3,stripe
from datetime import datetime
from fastapi import Request,HTTPException

ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")
STRIPE_SECRET_KEY=os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET=os.getenv("STRIPE_WEBHOOK_SECRET")
stripe.api_key=STRIPE_SECRET_KEY

PRICE_ONE_TIME="price_1TtbjXBOA5mT4t0PMCJSext6"
PRICE_MONTHLY="price_1TtblSBOA5mT4t0PGiYvT2l9"
PRICE_YEARLY="price_1TtbltBOA5mT4t0PpJ8io219"

ACCESS_DB="payments.db"

def init_access_db():
    conn=sqlite3.connect(ACCESS_DB)
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS access_users(id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE,plan TEXT,expires INTEGER,sessions_today INTEGER DEFAULT 0,last_session TEXT,active INTEGER DEFAULT 1)""")
    conn.commit()
    conn.close()

init_access_db()

def check_admin(username,password):
    return username==ADMIN_USERNAME and password==ADMIN_PASSWORD

async def create_checkout_session(plan:str,email:str):
    prices={"one_time":PRICE_ONE_TIME,"monthly":PRICE_MONTHLY,"yearly":PRICE_YEARLY}
    if plan not in prices:
        raise HTTPException(status_code=400,detail="Plan incorrecto")
    session=stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription" if plan in ["monthly","yearly"] else "payment",
        line_items=[{"price":prices[plan],"quantity":1}],
        metadata={"email":email,"plan":plan},
        success_url="https://open-than-go.onrender.com/payment-success",
        cancel_url="https://open-than-go.onrender.com/payment-cancel"
    )
    return session.url

def activate_user(email,plan):
    now=int(time.time())
    if plan=="one_time": expiration=now+86400
    elif plan=="monthly": expiration=now+(30*86400)
    elif plan=="yearly": expiration=now+(365*86400)
    else:return
    conn=sqlite3.connect(ACCESS_DB)
    cursor=conn.cursor()
    cursor.execute("""
    INSERT INTO access_users(email,plan,expires,sessions_today,last_session,active)
    VALUES(?,?,?,?,?,1)
    ON CONFLICT(email)
    DO UPDATE SET plan=excluded.plan,expires=excluded.expires,active=1
    """,(email,plan,expiration,0,""))
    conn.commit()
    conn.close()

def verify_access(email):
    conn=sqlite3.connect(ACCESS_DB)
    cursor=conn.cursor()
    cursor.execute("SELECT plan,expires,sessions_today,last_session,active FROM access_users WHERE email=?",(email,))
    user=cursor.fetchone()
    conn.close()
    if not user:return False
    plan,expires,sessions,last_session,active=user
    if active==0 or time.time()>expires:return False
    today=str(datetime.utcnow().date())
    if last_session!=today:sessions=0
    if plan=="one_time" and sessions>=1:return False
    if plan in ["monthly","yearly"] and sessions>=5:return False
    return True

def register_user_session(email):
    conn=sqlite3.connect(ACCESS_DB)
    cursor=conn.cursor()
    today=str(datetime.utcnow().date())
    cursor.execute("SELECT sessions_today,last_session FROM access_users WHERE email=?",(email,))
    data=cursor.fetchone()
    if not data:
        conn.close()
        return
    sessions,last=data
    if last!=today:sessions=0
    sessions+=1
    cursor.execute("UPDATE access_users SET sessions_today=?,last_session=? WHERE email=?",(sessions,today,email))
    conn.commit()
    conn.close()

@app.post("/create-checkout-session")
async def stripe_checkout(request:Request):
    data=await request.json()
    url=await create_checkout_session(data["plan"],data["email"])
    return {"url":url}

@app.post("/stripe-webhook")
async def stripe_webhook(request:Request):
    payload=await request.body()
    signature=request.headers.get("stripe-signature")
    try:
        event=stripe.Webhook.construct_event(payload,signature,STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400,detail="Webhook error")
    if event["type"]=="checkout.session.completed":
        session=event["data"]["object"]
        activate_user(session["metadata"]["email"],session["metadata"]["plan"])
    return {"status":"ok"}

@app.get("/payment-success")
async def payment_success():
    return {"message":"Pago confirmado. Acceso activado."}

@app.get("/payment-cancel")
async def payment_cancel():
    return {"message":"Pago cancelado."}

link_base = "https://www.google.com/maps/search/?api=1&query="

DEFAULT_NECESSITY_VECTOR = {
    "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
    "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
    "juego": 50, "contemplacion": 50, "descanso": 50, "organizacion": 50,
    "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
    "indicador_ansiedad": 0
}

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
# Descripciones de SALIR acortadas para lectura rápida.
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
                "porque": "Mente cansada. Desconecta.", "porque_en": "Screen-tired. Disconnect.",
                "que_hacer": "Gran árbol. Toca corteza. Siente sombra fresca.", "que_hacer_en": "Find tree. Touch bark. Feel cool shade.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85}
            },
            {"id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe",
                "porque": "Necesitas paz. Evita ruidos.", "porque_en": "Need peace. Avoid noise.",
                "que_hacer": "Cafetería tranquila. Pide tu bebida. Observa sin distracciones.", "que_hacer_en": "Quiet cafe. Order. Observe without distractions.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cafetería local tranquila.", "donde_en": "Quiet local cafe.", "gps": "quiet cafe",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70}
            },
            {"id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden",
                "porque": "Mente agotada. Reconéctate con lo natural.", "porque_en": "Exhausted. Reconnect with nature.",
                "que_hacer": "Pasea sin prisa. Observa plantas. Respira hondo.", "que_hacer_en": "Stroll. Observe plants. Breathe deep.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín botánico público.", "donde_en": "Public botanical garden.", "gps": "botanical garden",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90}
            },
            {"id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook",
                "porque": "Necesitas perspectiva. Eleva tu mirada.", "porque_en": "Need perspective. Elevate gaze.",
                "que_hacer": "Punto alto con vista. Observa el horizonte. Siente la inmensidad.", "que_hacer_en": "High point. Observe horizon. Feel immensity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95}
            },
            {"id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class",
                "porque": "Mente sobrecargada. Busca calma.", "porque_en": "Overloaded mind. Seek calm.",
                "que_hacer": "Sesión de meditación guiada. Concéntrate en la respiración.", "que_hacer_en": "Guided meditation. Focus on breathing.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90}
            },
            {"id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing",
                "porque": "Mente agitada. Deja que los pensamientos pasen.", "porque_en": "Agitated mind. Let thoughts pass.",
                "que_hacer": "Recuéstate. Observa el movimiento de las nubes.", "que_hacer_en": "Lie down. Watch clouds move.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85}
            },
            {
                "id": 355,
                "titulo": "Soberanía en Tránsito: Uber/Lyft Concluido",
                "titulo_en": "Transit Sovereignty: Uber/Lyft Concluded",
                "porque": "Agotamiento periférico. Fatiga de tráfico.", "porque_en": "Peripheral exhaustion. Traffic fatigue.",
                "que_hacer": "Pide Uber/Lyft a zona verde. Suelta el teléfono, cierra ojos 60s. Módulo Vacío Auditivo.",
                "que_hacer_en": "Order Uber/Lyft to green area. Drop phone, close eyes 60s. Auditory Emptiness Module.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cabina de transporte o asiento de pasajero.", "donde_en": "Transit vehicle cabin or passenger seat.",
                "gps": "quiet public square",
                "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 15, "contemplacion": 85, "esperanza": 80, "salud": 80, "aire_fresco": 60}
            },
            {
                "id": 356,
                "titulo": "Módulo de Cambio Frecuencial: Spotify",
                "titulo_en": "Frequency Shift Module: Spotify",
                "porque": "Saturación mental y fatiga auditiva.", "porque_en": "Mental saturation. Auditory fatigue.",
                "que_hacer": "Abre Spotify. Busca 432Hz o ruidos blancos. Auriculares. Estabiliza lóbulo temporal.",
                "que_hacer_en": "Open Spotify. Search 432Hz or white noise. Headphones. Stabilize temporal lobe.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Tu espacio de descanso, oficina vacía o dentro de tu vehículo.", "donde_en": "Your resting space, empty office, or inside your vehicle.",
                "gps": "quiet open park",
                "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 65, "contemplacion": 90, "esperanza": 85, "salud": 80, "creatividad": 40}
            },
            {
                "id": 357,
                "titulo": "Mapeo de Flujos: Recorrido Lineal en Costco",
                "titulo_en": "Flow Mapping: Costco Linear Walk",
                "porque": "Agotamiento por sedentarismo. Limpia tu sangre.", "porque_en": "Sedentary exhaustion. Clear blood.",
                "que_hacer": "Visita Costco. Camina pasillos sin prisa. Fuerza circulación de piernas.",
                "que_hacer_en": "Visit Costco. Walk aisles without rush. Force leg circulation.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pasillos industriales de un gran almacén.", "donde_en": "Industrial aisles of a large warehouse store.",
                "gps": "wholesale club or market",
                "vector_necesidades": {"movimiento": 85, "organizacion": 70, "contemplacion": 60, "comunidad": 50, "juego": 30, "descanso": 20, "silencio": 10}
            },
            {
                "id": 358,
                "titulo": "Oasis Burocrático: Biblioteca Pública",
                "titulo_en": "Bureaucratic Oasis: Public Library Refuge",
                "porque": "Fatiga extrema de trámites. Quietud garantizada.", "porque_en": "Extreme fatigue from bureaucracy. Guaranteed quiet.",
                "que_hacer": "Ubica biblioteca. Ingresa en silencio. Permite a tus córtex visuales descansar.",
                "que_hacer_en": "Find library. Enter silently. Allow visual cortex to rest.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sala de lectura o biblioteca municipal.", "donde_en": "Reading room or municipal library.",
                "gps": "public library",
                "vector_necesidades": {"aprendizaje": 100, "silencio": 100, "contemplacion": 90, "descanso": 85, "organizacion": 70, "salud": 80}
            },
            {"id": 201, "titulo": "Soberanía en Tránsito: Uber/Lyft Relax", "titulo_en": "Transit Sovereignty: Uber/Lyft Relax",
                "porque": "Cuerpo/mente saturados. Tráfico continuo.", "porque_en": "Body/mind saturated from driving/traffic.",
                "que_hacer": "Pide Uber/Lyft a zona tranquila. Cierra ojos. Módulo Silencio Auditivo 1 min.",
                "que_hacer_en": "Open ride app. Request short ride to quiet area. Close eyes. 1-min Auditory Silence Module.",
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
                "porque": "Saturación del espacio habitual. Necesitas confort.", "porque_en": "Usual space saturation. Need comfort.",
                "que_hacer": "Visita lobby hotel. Siéntate recto, nota el piso. Descansa vista en punto lejano 2 min.",
                "que_hacer_en": "Visit hotel lobby. Sit straight, feel floor. Rest eyes on distant point 2 min.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lobby o zona de descanso de un hotel local.", "donde_en": "Lobby or lounge area of a local hotel.",
                "gps": "hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 70, "esperanza": 80, "movimiento": 20}
            },
            {"id": 204, "titulo": "Sabotaje de Espera: Espacio Universitario", "titulo_en": "Waiting Sabotage: University Space",
                "porque": "Falta de nutrición intelectual. Exceso de micro-estímulos vacíos.", "porque_en": "Lack of intellectual nourishment, excess empty stimuli.",
                "que_hacer": "Campus uni. Camina en silencio por áreas verdes. Respira aire fresco, observa.",
                "que_hacer_en": "Go to campus/library. Walk silently through green spaces. Breathe fresh air, observe calmly.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Campus universitario o biblioteca pública.", "donde_en": "University campus or public library.",
                "gps": "university library",
                "vector_necesidades": {"aprendizaje": 100, "silencio": 90, "contemplacion": 85, "descanso": 70, "aire_fresco": 75, "movimiento": 40}
            },
        ],
        "estresado": [
            {"id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk",
                "porque": "Cuerpo tenso. Libera estrés. Siente tu fuerza.", "porque_en": "Tense body. Release stress. Feel strength.",
                "que_hacer": "Rampa o escaleras públicas. Sube a paso firme.", "que_hacer_en": "Public ramp or stairs. Climb steadily.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public stairs",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75}
            },
            {"id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga",
                "porque": "Mente acelerada. Conecta cuerpo y naturaleza.", "porque_en": "Racing mind. Connect body and nature.",
                "que_hacer": "Parque. Extiende mat. Sigue rutina de yoga o estiramientos.", "que_hacer_en": "Park. Lay mat. Follow yoga or stretching.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80}
            },
            {"id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym",
                "porque": "Libera energía. Tensión en fuerza.", "porque_en": "Release energy. Tension to strength.",
                "que_hacer": "Gimnasio público. Enfócate en tu rutina. Suda.", "que_hacer_en": "Public gym. Focus on routine. Sweat.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60}
            },
            {
                "id": 320,
                "titulo": "Liberación de Impacto: Trampoline Park / Escalada",
                "titulo_en": "Impact Release: Trampoline Park / Climbing Gym",
                "porque": "Rigidez muscular. Rabia contenida. Rompe coraza física.", "porque_en": "Muscular rigidity. Pent-up anger. Break physical armor.",
                "que_hacer": "Trampoline o escalada. Salta/escala. Drena adrenalina acumulada.",
                "que_hacer_en": "Trampoline or climbing gym. Jump/climb. Drain accumulated adrenaline.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de trampolines o centro deportivo.", "donde_en": "Trampoline park or high-discharge sports center.",
                "gps": "trampoline park or climbing gym",
                "vector_necesidades": {"movimiento": 100, "juego": 100, "risa": 90, "salud": 95, "descanso": 0, "silencio": 10, "comunidad": 60, "esperanza": 90}
            },
            {
                "id": 321,
                "titulo": "Módulo de Hidro-Calma: Jacuzzi / Piscina Termal",
                "titulo_en": "Hydro-Calm Module: Public Jacuzzi / Thermal Pool",
                "porque": "Nervioso en alerta roja. Agua templada es reset somático.", "porque_en": "Nervous system on red alert. Warm water is somatic reset.",
                "que_hacer": "Centro recreativo con spa. Sumérgete. Cierra ojos. Flotabilidad y temperatura.",
                "que_hacer_en": "Recreation center with spa. Submerge. Close eyes. Buoyancy and skin temperature.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "YMCA, alberca climatizada o spa comunitario.",
                "donde_en": "YMCA, heated pool, or local community spa.",
                "gps": "ymca pool or public spa",
                "vector_necesidades": {"agua": 100, "descanso": 100, "salud": 95, "silencio": 60, "contemplacion": 90, "sombra": 80, "esperanza": 85, "movimiento": 20}
            },
            {
                "id": 322,
                "titulo": "Quiebre de Frecuencias: Sound Healing / Yoga",
                "titulo_en": "Frequency Break: Sound Healing / Yoga Center",
                "porque": "Mente acelerada. Pensamientos intrusivos. Estrés digital.", "porque_en": "Racing mind. Intrusive thoughts. Digital stress.",
                "que_hacer": "Estudio de yoga/sound healing. Inhala en 4, exhala en 8.",
                "que_hacer_en": "Yoga/sound healing studio. Inhale 4, exhale 8.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Estudio de yoga, meditación o sound healing.",
                "donde_en": "Yoga studio, meditation center, or sound healing spot.",
                "gps": "sound healing or yoga studio",
                "vector_necesidades": {"silencio": 100, "descanso": 95, "musica": 90, "contemplacion": 95, "salud": 90, "esperanza": 90, "organizacion": 70}
            },
            {
                "id": 323,
                "titulo": "Aislamiento Orgánico: Sendero Natural (State Park)",
                "titulo_en": "Organic Isolation: State Park Trail",
                "porque": "Estrés tóxico urbano. Aire puro. Regula cortisol.", "porque_en": "Toxic urban stress. Pure air. Regulate cortisol.",
                "que_hacer": "Parque estatal. Camina descalzo o toca árbol. Aire fresco.",
                "que_hacer_en": "State park. Walk barefoot or touch tree. Fresh air.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sendero boscoso o parque estatal.",
                "donde_en": "Wooded trail or state park.",
                "gps": "state park trail or nature reserve",
                "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "silencio": 85, "movimiento": 60, "contemplacion": 90, "descanso": 60, "esperanza": 95, "sol": 70}
            },
            {
                "id": 112,
                "titulo": "Sendero Corto Natural",
                "titulo_en": "Short Nature Trail",
                "porque": "Sobrecarga de estímulos. Camina en paz.", "porque_en": "Stimuli overload. Walk in peace.",
                "que_hacer": "Sendero. Camina ligero. Observa entorno natural.",
                "que_hacer_en": "Trail. Walk briskly. Observe natural surroundings.",
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
                "porque": "Mente acelerada. Quema energía extra. Enfoca tu ritmo.", "porque_en": "Racing mind. Burn energy. Focus rhythm.",
                "que_hacer": "Pista pública. Corre o camina a tu paso.",
                "que_hacer_en": "Public track. Run or walk your pace.",
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
                "porque": "Saturación nerviosa por encierro. Tráfico denso.", "porque_en": "Nervous saturation from confinement. Heavy traffic.",
                "que_hacer": "Ojos de pantalla. Palmas firmes rodillas. Columna recta. Inhala 4, retén 4, exhala.",
                "que_hacer_en": "Eyes off screen. Palms on knees. Straighten spine. Inhale 4, hold 4, exhale.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cabina de transporte o asiento de pasajero.", "donde_en": "Transit cabin or passenger seat.",
                "gps": "quiet rest areas or public plazas",
                "vector_necesidades": {"descanso": 95, "silencio": 85, "movimiento": 20, "contemplacion": 90, "organizacion": 60, "esperanza": 80}
            },
            {
                "id": 252,
                "titulo": "Hackeo al Tráfico: Intersección Interestatal",
                "titulo_en": "Traffic Hack: Interstate Intersection Module",
                "porque": "Cortisol elevado por embotellamientos y ruidos.", "porque_en": "Elevated cortisol from traffic jams and noise.",
                "que_hacer": "Aprovecha luz roja. Suelta tensión mandíbula 10s. Estira dedos. Mira cielo. Tú respiras, el asfalto ruge.",
                "que_hacer_en": "Use red light. Release jaw tension 10s. Stretch fingers. Look at sky. You breathe, asphalt roars.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Área de servicio de autopista o intersección vial.", "donde_en": "Highway service area or road intersection.",
                "gps": "highway rest stop or overlook",
                "vector_necesidades": {"movimiento": 80, "descanso": 70, "silencio": 50, "aire_fresco": 85, "organizacion": 40, "salud": 85}
            },            
            {"id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route",
                "porque": "Libera tensión, muévete rápido. Siente el viento.", "porque_en": "Release tension, move fast. Feel wind.",
                "que_hacer": "Carril bici. Pedalea. Siente velocidad y control.", "que_hacer_en": "Bike lane. Pedal. Feel speed and control.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80}
            },
            {"id": 211, "titulo": "Soberanía de Cabina: Terminal Aérea / Vuelos", "titulo_en": "Cabin Sovereignty: Air Terminal / Flights",
                "porque": "Saturación nerviosa por ruidos de tránsito masivo.", "porque_en": "Nervous saturation from mass transit pressures/noise.",
                "que_hacer": "Ventana al cielo. 3 inhalaciones diafragmáticas profundas. Siente el viento.",
                "que_hacer_en": "Sky-view window. 3 deep diaphragmatic breaths. Feel wind.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Terminal de aeropuerto o zona de observación abierta.", "donde_en": "Airport terminal or open observation zone.",
                "gps": "airport observation area",
                "vector_necesidades": {"aire_fresco": 100, "contemplacion": 95, "silencio": 60, "descanso": 50, "movimiento": 30, "esperanza": 80}
            },
            {"id": 212, "titulo": "Depuración Exocrina: Complejo Deportivo / Gym", "titulo_en": "Exocrine Cleansing: Sports Complex / Gym",
                "porque": "Exceso adrenalina por estrés laboral.", "porque_en": "Excess adrenaline from work stress.",
                "que_hacer": "Gym/piscina pública. Contracción voluntaria 60s. Suda. Libera toxinas.",
                "que_hacer_en": "Gym/public pool. Force continuous voluntary contraction 60s. Sweat. Release toxins.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gimnasio público, cancha o alberca comunitaria.", "donde_en": "Public gym, court, or community pool.",
                "gps": "community fitness center",
                "vector_necesidades": {"movimiento": 100, "agua": 80, "salud": 90, "juego": 50, "descanso": 0, "silencio": 20, "risa": 40}
            },
            {"id": 213, "titulo": "Estabilización Somática: Farmacia / Clínica", "titulo_en": "Somatic Stabilization: Pharmacy / Clinic",
                "porque": "Ritmo cardíaco acelerado. Pánico.", "porque_en": "Accelerated heart rate. Panic.",
                "que_hacer": "Clínica/farmacia. Agua potable. Hidratación consciente. Siente rehidratación.",
                "que_hacer_en": "Clinic/pharmacy. Drinking water. Conscious hydration. Feel cells rehydrate.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Área de descanso de una farmacia o clínica local.", "donde_en": "Lounge area of a local pharmacy or clinic.",
                "gps": "pharmacy health lounge",
                "vector_necesidades": {"agua": 100, "salud": 95, "descanso": 80, "silencio": 70, "organizacion": 80, "esperanza": 85}
            },
        ],
        "aburrido": [
            {"id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk",
                "porque": "Días repetitivos. Busca novedad. Despierta tu visión.", "porque_en": "Repetitive days. Seek novelty. Awaken sight.",
                "que_hacer": "Camina lento. Busca murales y dibujos grandes.", "que_hacer_en": "Walk slowly. Find large murals/drawings.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street art",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}
            },
            {
                "id": 307,
                "titulo": "Descompresión de Perímetro: Lobby de Hotel / Resort",
                "titulo_en": "Perimeter Decompression: Hotel / Resort Lobby",
                "porque": "Monotonía espacial severa. Entorno de diseño premium.", "porque_en": "Severe spatial monotony. Premium design environment.",
                "que_hacer": "Hotel/resort. Siéntate en butaca. Observa arquitectura. Descansa.",
                "que_hacer_en": "Hotel/resort. Sit in armchair. Observe architecture. Rest.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lobby o zona de descanso pública de un hotel.", "donde_en": "Lobby or public lounge area of a local hotel.",
                "gps": "hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 80, "esperanza": 80, "comunidad": 50, "movimiento": 20}
            },
            {
                "id": 308,
                "titulo": "Ampliación del Horizonte: Terminal de Aerolíneas",
                "titulo_en": "Horizon Expansion: Airline Terminal",
                "porque": "Falta de perspectiva. Flujos globales devuelven enfoque.", "porque_en": "Lack of perspective. Global flows return focus.",
                "que_hacer": "Terminal aérea. Ventanal más amplio. 3 respiraciones diafragmáticas. Asimila inmensidad.",
                "que_hacer_en": "Airline terminal. Widest window. 3 diaphragmatic breaths. Assimilate immensity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.",
                "gps": "transit center or airport terminal",
                "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30, "aprendizaje": 60}
            },
            {
                "id": 309,
                "titulo": "Distracción Absoluta: Centro de Ocio / Parque Temático",
                "titulo_en": "Absolute Distraction: Leisure Center / Theme Park",
                "porque": "Bucle mental de apatía. Shock visual de juego.", "porque_en": "Apathy mental loop. Visual shock of play.",
                "que_hacer": "Parque atracciones/Arcade. Observa luces, risas. Conecta con ocio.",
                "que_hacer_en": "Amusement park/Arcade. Observe lights, laughter. Connect with leisure.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque recreativo, zona infantil o centro de juegos.", "donde_en": "Recreation park, kid zone, or local arcade center.",
                "gps": "amusement park or arcade",
                "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50, "creatividad": 60}
            },
            {
                "id": 310,
                "titulo": "Exploración de Espacios: Módulo de Diseño Airbnb",
                "titulo_en": "Space Exploration: Airbnb Design Module",
                "porque": "Falta de inspiración. Visualiza arquitecturas alternativas.", "porque_en": "Lack of inspiration. Visualize alternative architectures.",
                "que_hacer": "Abre Airbnb. Filtra cabañas/casas árbol. Analiza diseño sin reservar.",
                "que_hacer_en": "Open Airbnb. Filter cabins/treehouses. Analyze design without booking.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Interfaz móvil desde tu zona de descanso habitual.", "donde_en": "Mobile interface from your usual resting space.",
                "gps": "local post office",
                "vector_necesidades": {"creatividad": 100, "contemplacion": 95, "juego": 70, "organizacion": 80, "esperanza": 85, "descanso": 60, "aprendizaje": 60}
            },
            {
                "id": 311,
                "titulo": "Mapeo de Flujos: Recorrido Perimetral Costco",
                "titulo_en": "Flow Mapping: Costco Perimeter Walk",
                "porque": "Rutina plana. Altera percepción de consumo. Activa cuerpo.", "porque_en": "Flat routine. Alters consumption perception. Activates body.",
                "que_hacer": "Costco o club de precios. Camina pasillos industriales. Fuerza contracción muscular.",
                "que_hacer_en": "Costco or price club. Walk industrial aisles. Force leg muscle contraction.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pasillos industriales de un gran almacén.", "donde_en": "Industrial aisles of a large warehouse store.",
                "gps": "wholesale club or warehouse",
                "vector_necesidades": {"movimiento": 85, "organizacion": 75, "comunidad": 60, "contemplacion": 60, "juego": 40, "descanso": 10, "silencio": 5}
            },
            {
                "id": 312,
                "titulo": "Sabotaje de Espera: Campus Universitario / Escuela",
                "titulo_en": "Waiting Sabotage: University Campus / School",
                "porque": "Bucle mental aburrido. Inyección de aire fresco.", "porque_en": "Bored mental loop. Fresh air injection.",
                "que_hacer": "Campus uni o escuela pública. Camina en silencio áreas verdes. Respira aire libre.",
                "que_hacer_en": "University campus or public school. Walk silently green areas. Breathe open air.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Áreas comunes abiertas de un campus universitario.", "donde_en": "Open common areas of a university campus.",
                "gps": "university campus or public school",
                "vector_necesidades": {"aprendizaje": 100, "aire_fresco": 95, "silencio": 90, "contemplacion": 85, "descanso": 70, "movimiento": 40}
            },
            {
                "id": 304,
                "titulo": "Soberanía en Tránsito: Escape Uber/Lyft",
                "titulo_en": "Sovereignty in Transit: Uber/Lyft Escape",
                "porque": "Inercia mental estancada. Cambio geográfico rápido.", "porque_en": "Stuck mental inertia. Rapid geographical change.",
                "que_hacer": "Uber/Lyft a parque desconocido. Suelta teléfono. Mira ventana. Asimila velocidad.",
                "que_hacer_en": "Uber/Lyft to unknown park. Drop phone. Look out window. Assimilate urban speed.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Asiento de pasajero en un coche de transporte urbano.", "donde_en": "Passenger seat in an urban transit vehicle.",
                "gps": "public transit hub or central park",
                "vector_necesidades": {"juego": 80, "movimiento": 70, "contemplacion": 85, "comunidad": 60, "descanso": 40, "silencio": 30, "esperanza": 80}
            },
            {
                "id": 305,
                "titulo": "Descompresión Visual: El Algoritmo de YouTube",
                "titulo_en": "Visual Decompression: The YouTube Algorithm",
                "porque": "Bucle cognitivo severo. Quiebre estético controlado.", "porque_en": "Severe cognitive loop. Controlled aesthetic break.",
                "que_hacer": "Abre YouTube. Busca '4K drone architecture relax'. Mira fijo 2 min. Relaja músculos ciliares.",
                "que_hacer_en": "Open YouTube. Search '4K drone architecture relax'. Watch fixedly 2 min. Relax ciliary muscles.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Interfaz de tu teléfono en un rincón con luz tenue.", "donde_en": "Your phone interface in a dimly lit corner.",
                "gps": "local coffee lounge",
                "vector_necesidades": {"contemplacion": 100, "descanso": 90, "creatividad": 80, "esperanza": 90, "silencio": 50, "naturaleza": 70, "movimiento": 5}
            },
            {
                "id": 306,
                "titulo": "Inversión Controlada: Antojo Digital en Amazon",
                "titulo_en": "Controlled Investment: Digital Desire on Amazon",
                "porque": "Aburrimiento crónico. Falta micro-estímulos.", "porque_en": "Chronic boredom. Lack of micro-stimuli.",
                "que_hacer": "Abre Amazon. Busca objeto para pasatiempo físico. Compra. Invierte en creatividad.",
                "que_hacer_en": "Open Amazon. Search object for physical hobby. Buy. Invest in creativity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pantalla móvil desde tu espacio de descanso habitual.", "donde_en": "Mobile screen from your usual resting space.",
                "gps": "local post office",
                "vector_necesidades": {"juego": 90, "creatividad": 90, "esperanza": 95, "organizacion": 70, "descanso": 60, "aprendizaje": 80, "movimiento": 10}
            },            
            {
                "id": 301,
                "titulo": "Auditoría de Frecuencias: Discoteca / Club Night",
                "titulo_en": "Frequency Audit: Nightclub / Club Night",
                "porque": "Monotonía aplastante. Falta estímulos rítmicos.", "porque_en": "Crushing monotony. Lack of rhythmic stimuli.",
                "que_hacer": "Club nocturno. Sal a exterior. Escucha vibración del bajo. Siente pulso nocturno.",
                "que_hacer_en": "Nightclub. Step outside. Listen to bass vibration. Feel nightlife pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior de un club nocturno urbano.", "donde_en": "Outer perimeter of an urban nightclub.",
                "gps": "dance club or nightclub",
                "vector_necesidades": {"juego": 100, "musica": 100, "comunidad": 90, "risa": 80, "movimiento": 70, "creatividad": 60, "silencio": 10, "descanso": 30}
            },
            {
                "id": 302,
                "titulo": "Terapia de Pasillo: Recorrido Target / Walmart",
                "titulo_en": "Aisle Therapy: Target / Walmart Walk",
                "porque": "Estancamiento mental en casa. Falta variedad visual.", "porque_en": "Mental stagnation. Lack of visual variety.",
                "que_hacer": "Superficie comercial. Recorre pasillos. Observa organización. Activa flujo linfático.",
                "que_hacer_en": "Department store. Walk aisles. Observe layout. Activate lymphatic flow.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gran superficie comercial o tienda céntrica.", "donde_en": "Large department store or central shop.",
                "gps": "department store or retail",
                "vector_necesidades": {"movimiento": 80, "organizacion": 70, "contemplacion": 70, "comunidad": 60, "juego": 50, "descanso": 20, "silencio": 15}
            },
            {
                "id": 303,
                "titulo": "Sabotaje Alimenticio: Antojo Rápido McDonald's / Starbucks",
                "titulo_en": "Food Sabotage: Quick Treat McDonald's / Starbucks",
                "porque": "Falta estímulos sensoriales. Monotonía alimentación.", "porque_en": "Lack of sensory stimuli. Food monotony.",
                "que_hacer": "Cadena comida rápida/cafetería. Pide antojo. Disfrútalo sin pantalla. Atiende sabor real.",
                "que_hacer_en": "Fast-food/coffee shop. Order treat. Enjoy bite-by-bite, no screen. Focus on real flavor.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cadena de comida rápida o cafetería local.", "donde_en": "Fast food chain or local coffee shop.",
                "gps": "fast food or local restaurant",
                "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20}
            },            
            {
                "id": 253,
                "titulo": "Auditoría de Frecuencias: Escape Discoteca / Club",
                "titulo_en": "Frequency Audit: Nightclub / Club Escape",
                "porque": "Monotonía mental. Quiebre sensorial radical.", "porque_en": "Mental monotony. Radical sensory break.",
                "que_hacer": "Club nocturno. Sal a exterior. Escucha vibración del bajo. Siente cambio temperatura. Pulso nocturno.",
                "que_hacer_en": "Nightclub. Step outside. Listen to bass. Feel temperature change. Nightlife pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior de un club nocturno urbano.", "donde_en": "Outer perimeter of an urban nightclub.",
                "gps": "nightlife district or dance clubs",
                "vector_necesidades": {"juego": 100, "musica": 100, "comunidad": 90, "risa": 80, "movimiento": 70, "creatividad": 60, "silencio": 10, "descanso": 30}
            },
            {"id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market",
                "porque": "Nuevos estímulos. Sabores frescos. Apoya lo local.", "porque_en": "New stimuli. Fresh tastes. Support local.",
                "que_hacer": "Mercado local. Prueba algo nuevo. Habla con vendedores.", "que_hacer_en": "Local market. Try new. Talk to vendors.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers market",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "silencio": 30, "agua": 10, "sol": 70, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 60, "juego": 40, "contemplacion": 50, "descanso": 30, "organizacion": 50, "alimentacion": 100, "musica": 30, "risa": 70, "esperanza": 80}
            },
            {"id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition",
                "porque": "Mente en bucle. Busca inspiración. Despierta creatividad.", "porque_en": "Mind in a loop. Seek inspiration. Awaken creativity.",
                "que_hacer": "Galería o museo. Observa el arte. Reflexiona en silencio.", "que_hacer_en": "Local gallery/museum. Observe art. Reflect in silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art gallery",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 70, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 30, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 10, "contemplacion": 95, "descanso": 60, "organizacion": 70, "alimentacion": 0, "musica": 60, "risa": 20, "esperanza": 85}
            },
            {"id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park",
                "porque": "Energía visual. Observa libertad y movimiento. Conéctate con juego.", "porque_en": "Visual energy. Observe freedom/movement. Connect with play.",
                "que_hacer": "Skate park. Observa patinadores. Siente vitalidad.", "que_hacer_en": "Skate park. Watch skaters. Feel vitality.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate park",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 30, "silencio": 20, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 80, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 60, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 70, "risa": 90, "esperanza": 90}
            },
            {"id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore",
                "porque": "Busca historias y conocimiento. Desconéctate digital.", "porque_en": "Seek stories/knowledge. Disconnect digital.",
                "que_hacer": "Librería segunda mano. Busca títulos inesperados. Disfruta el aroma.", "que_hacer_en": "Used bookstore. Look for titles. Enjoy scent.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used bookstore",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 85, "agua": 0, "sol": 20, "sombra": 95, "aire_fresco": 40, "creatividad": 90, "comunidad": 30, "aprendizaje": 100, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 70, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 75}
            },
            {"id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema",
                "porque": "Cambio de ambiente. Nueva perspectiva. Disfruta historia.", "porque_en": "Scene/perspective change. Enjoy story.",
                "que_hacer": "Proyección cine aire libre. Sumérgete en película y ambiente.", "que_hacer_en": "Outdoor cinema. Immerse in film/atmosphere.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor cinema",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 40, "agua": 10, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "descanso": 70, "organizacion": 20, "alimentacion": 60, "musica": 70, "risa": 70, "esperanza": 85}
            },
            {"id": 221, "titulo": "Auditoría de Frecuencias: Discoteca / Club", "titulo_en": "Frequency Audit: Nightclub / Club",
                "porque": "Monotonía extrema. Falta estímulos rítmicos.", "porque_en": "Extreme monotony, lack of rhythmic/social stimuli.",
                "que_hacer": "Club/bar. Sal al exterior. Siente la música. Libérate de inercia mental.",
                "que_hacer_en": "Club/bar. Step outside. Feel music. Break free from mental inertia.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior o zona abierta de un club nocturno.", "donde_en": "Outer perimeter or open area of a nightclub.",
                "gps": "nightlife district lounge",
                "vector_necesidades": {"juego": 100, "comunidad": 90, "musica": 90, "risa": 80, "creatividad": 70, "movimiento": 60, "silencio": 10, "descanso": 30}
            },
            {"id": 222, "titulo": "Hackeo Cognitivo: Galería / Cine / Teatro", "titulo_en": "Cognitive Hack: Gallery / Cinema / Theater",
                "porque": "Falta inspiración. Embotamiento por contenido basura.", "porque_en": "Lack of inspiration, dullness from repetitive junk content.",
                "que_hacer": "Cine/museo/teatro. Entra vestíbulo. Elige cartel/imagen. Obsérvalo fijo, aísla mente.",
                "que_hacer_en": "Cinema/museum/theater. Enter lobby. Choose poster/image. Stare, isolate mind.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Entrada pública de un centro cultural o cine.", "donde_en": "Public entrance of a cultural center or cinema.",
                "gps": "local cinema or museum",
                "vector_necesidades": {"creatividad": 100, "aprendizaje": 90, "contemplacion": 95, "juego": 60, "comunidad": 50, "descanso": 60, "silencio": 70}
            },
            {"id": 223, "titulo": "Sabotaje de Rutina: Salir a Comer / Fast Food", "titulo_en": "Routine Sabotage: Dining Out / Fast Food",
                "porque": "Falta variedad sensorial. Antojo físico rompe inercia.", "porque_en": "Lack of sensory variety. Treat breaks inertia.",
                "que_hacer": "Restaurante/fast food. Pide algo. Disfrútalo sin pantallas. Atiende sabor y textura.",
                "que_hacer_en": "Restaurant/fast food. Order. Enjoy bite-by-bite, no screens. Focus on taste/texture.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cadena de comida rápida o restaurante del vecindario.", "donde_en": "Fast food chain or neighborhood restaurant.",
                "gps": "fast food or local restaurant",
                "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20}
            }
        ],
        "cansado": [
            {"id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading",
                "porque": "Necesitas calma. Aprende sin distracciones.", "porque_en": "Need calm. Learn without distractions.",
                "que_hacer": "Biblioteca local. Busca libro o disfruta silencio.", "que_hacer_en": "Local library. Find book or enjoy silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70}
            },
            {"id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk",
                "porque": "Despeja la mente. Aire fresco. Vistas al agua.", "porque_en": "Clear mind. Fresh air. Water views.",
                "que_hacer": "Camina por muelle o puerto. Observa barcos. Escucha el agua.", "que_hacer_en": "Walk dock/harbor. Watch boats. Listen to water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90}
            },
            {
                "id": 328,
                "titulo": "Inversión Marítima: Cruceros / Muelles",
                "titulo_en": "Maritime Inversion: Cruise Line / Pier Perimeter",
                "porque": "Cansancio acumulado. Mente requiere inmensidad del agua.", "porque_en": "Accumulated fatigue. Mind needs vast water.",
                "que_hacer": "Puerto o muelle. Observa embarcaciones. Reflejo del agua limpia pensamientos.",
                "que_hacer_en": "Port or pier. Observe vessels. Water reflection clears thoughts.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Muelle, puerto local o zona costera abierta.", "donde_en": "Dock, local pier, or open coastal zone.",
                "gps": "cruise terminal or pier",
                "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60, "esperanza": 85}
            },
            {
                "id": 329,
                "titulo": "Pausa en Ruta: Módulo de Descanso Interestatal",
                "titulo_en": "Route Break: Interstate Rest Stop Module",
                "porque": "Fatiga muscular. Embotamiento cognitivo. Trayectos continuos.", "porque_en": "Muscular fatigue. Cognitive dullness. Continuous travel.",
                "que_hacer": "Área de servicio. Estaciona, apaga motor. Estira piernas. Reactiva circulación.",
                "que_hacer_en": "Rest area. Park, turn off engine. Stretch legs. Reactivate circulation.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Área de servicio de autopista o zona de descanso pública.", "donde_en": "Highway service area or public rest zone.",
                "gps": "highway rest stop or plaza",
                "vector_necesidades": {"descanso": 95, "movimiento": 60, "aire_fresco": 90, "salud": 85, "silencio": 50, "contemplacion": 70, "organizacion": 40}
            },
            {
                "id": 330,
                "titulo": "Recuperación Pasiva: Paseo Histórico y Calma Urbana",
                "titulo_en": "Passive Recovery: Historical Walk and Urban Calm",
                "porque": "Agotamiento mental. Predictibilidad diaria.", "porque_en": "Mental exhaustion. Daily predictability.",
                "que_hacer": "Zona histórica/plaza. Camina lento. Observa estructuras. Despeja mente.",
                "que_hacer_en": "Historical zone/plaza. Walk slowly. Observe structures. Clear mind.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro histórico, plaza pública o calles peatonales.", "donde_en": "Historical center, public plaza, or pedestrian streets.",
                "gps": "historical landmark or walking tour",
                "vector_necesidades": {"aprendizaje": 90, "contemplacion": 95, "descanso": 80, "movimiento": 50, "silencio": 70, "creatividad": 60, "esperanza": 80}
            },
            {
                "id": 331,
                "titulo": "Aislamiento Sensorial: Butaca de Cine Matinal",
                "titulo_en": "Sensory Isolation: Morning Cinema Seat",
                "porque": "Saturación sistema nervioso. Exceso interacción humana.", "porque_en": "Nervous system saturation. Excessive human interaction.",
                "que_hacer": "Cine. Función matinal. Siéntate en penumbra. Oscuridad y aislamiento calman mente.",
                "que_hacer_en": "Cinema. Morning screening. Sit in dim light. Darkness and isolation calm mind.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sala de cine comercial o vestíbulo de proyecciones.", "donde_en": "Commercial movie theater or screening lobby.",
                "gps": "local cinema or amc",
                "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 90, "sombra": 100, "juego": 40, "creatividad": 50, "movimiento": 5}
            },
            {
                "id": 332,
                "titulo": "Homeostasis Verde: Jardín Botánico / Invernadero",
                "titulo_en": "Green Homeostasis: Rest in Botanical Garden / Greenhouse",
                "porque": "Agotamiento crónico por asfalto/oficina. Falta conexión orgánica.", "porque_en": "Chronic fatigue from asphalt/office. Lack of organic connection.",
                "que_hacer": "Jardín botánico/invernadero. Banco bajo vegetación. Permanece inmóvil 2 min. Aire limpio. Verdes relajan vista.",
                "que_hacer_en": "Botanical garden/greenhouse. Bench under vegetation. Stay still 2 min. Clean air. Greens relax sight.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín botánico público, vivero o parque natural.", "donde_en": "Public botanical garden, nursery, or regional nature park.",
                "gps": "botanical garden or nursery",
                "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "descanso": 90, "silencio": 80, "contemplacion": 95, "sombra": 90, "salud": 85, "movimiento": 25}
            },
            {
                "id": 333,
                "titulo": "Módulo de Quietud: Banco en Lago / Muelle Público",
                "titulo_en": "Quietness Module: Bench by a Public Lake / Pier",
                "porque": "Cansancio mental plano. Monotonía. Observa movimiento sutil naturaleza.", "porque_en": "Flat mental fatigue. Monotony. Observe subtle nature movement.",
                "que_hacer": "Parque con lago/muelle. Banco cerca orilla. Observa ondas agua, aves. Respira lento.",
                "que_hacer_en": "Park with lake/pier. Bench near shore. Observe water ripples, birds. Breathe slowly.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Banco de parque junto a un estanque o lago público.", "donde_en": "Park bench next to a public pond or lake.",
                "gps": "public lake park or fountain",
                "vector_necesidades": {"agua": 100, "contemplacion": 100, "descanso": 95, "silencio": 75, "naturaleza": 85, "aire_fresco": 90, "movimiento": 15}
            },
            {"id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory",
                "porque": "Mente ansiosa. Busca perspectiva universal.", "porque_en": "Anxious mind. Seek universal perspective.",
                "que_hacer": "Observatorio. Aprende universo. Observa estrellas.", "que_hacer_en": "Observatory. Learn universe. Stargaze.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95}
            },
            {"id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza",
                "porque": "Necesitas observar. Conéctate vida urbana. Descansa.", "porque_en": "Need to observe. Connect urban life. Rest.",
                "que_hacer": "Banco. Observa gente pasar. Siente pulso ciudad.", "que_hacer_en": "Bench. Watch people pass. Feel city's pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85}
            },
            {"id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour",
                "porque": "Mente agotada. Inyección de conocimiento.", "porque_en": "Mind tired. Knowledge injection.",
                "que_hacer": "Tour a pie. Descubre historias locales.", "que_hacer_en": "Walking tour. Discover local stories.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90}
            },
            {"id": 231, "titulo": "Inversión Marítima: Perímetro de Cruceros", "titulo_en": "Maritime Inversion: Cruise Line Perimeter",
                "porque": "Cansancio monótono. Mente requiere estímulo inmensidad agua.", "porque_en": "Monotonous fatigue. Mind needs vast water stimulus.",
                "que_hacer": "Puerto/muelle/agencia cruceros. Observa naves/horizonte. Reflejo agua limpia pensamientos.",
                "que_hacer_en": "Port/pier/cruise agency. Observe vessels/horizon. Water reflection clears thoughts.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Muelle, puerto o zona costera abierta.", "donde_en": "Dock, pier, or open coastal zone.",
                "gps": "cruise terminal or pier",
                "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60}
            },
            {"id": 232, "titulo": "Quiebre de Inercia: Discoteca / Club Nocturno", "titulo_en": "Inertia Break: Nightclub / Dance Club",
                "porque": "Cansancio cerebral. Falta estímulos rítmicos.", "porque_en": "Brain fatigue. Lack of rhythmic stimuli.",
                "que_hacer": "Clubs/discotecas. Sal a área abierta. Escucha vibración bajo. Pulso nocturno rompe automatismo.",
                "que_hacer_en": "Clubs/nightlife. Step out to open area. Listen to bass. Night's pulse breaks automatism.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Perímetro exterior o terraza de un club céntrico.", "donde_en": "Outer perimeter or terrace of a central club.",
                "gps": "dance club or nightclub",
                "vector_necesidades": {"musica": 100, "juego": 90, "comunidad": 80, "risa": 70, "movimiento": 60, "silencio": 10, "descanso": 40}
            }
        ],
        "ansioso": [
            {"id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water",
                "porque": "Agua en movimiento. Calma tu mente. Relaja tensiones.", "porque_en": "Moving water. Calm mind. Release tensions.",
                "que_hacer": "Fuente, lago o río cercano. Observa flujo. Déjate llevar.", "que_hacer_en": "Nearby fountain/lake/river. Observe flow. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80}
            },
            {"id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride",
                "porque": "Estrés acumulado. Desconexión total. Flota y relájate.", "porque_en": "Accumulated stress. Total disconnection. Float and relax.",
                "que_hacer": "Paseo corto en bote. Siente brisa. Observa inmensidad del agua.", "que_hacer_en": "Short boat ride. Feel breeze. Observe vast water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90}
            },
            {
                "id": 345,
                "titulo": "Distracción Absoluta: Centro de Recreación / Parque Mascotas",
                "titulo_en": "Absolute Distraction: Recreation Center / Dog Park",
                "porque": "Ansiedad cíclica. Rumiación mental masiva. Shock de juego.", "porque_en": "Cyclic anxiety. Massive mental rumination. Shock of play.",
                "que_hacer": "Parque perros/centro entretenimiento. Observa interacciones. Escucha risas. Conecta con juego inocente.",
                "que_hacer_en": "Dog park/entertainment center. Observe interactions. Listen to laughter. Connect with innocent play.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de perros local, zona infantil o centro de juegos.", "donde_en": "Local dog park, kids zone, or arcade center.",
                "gps": "dog park or amusement arcade",
                "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 90, "movimiento": 70, "esperanza": 95, "silencio": 20, "descanso": 50, "creatividad": 40}
            },
            {
                "id": 346,
                "titulo": "Aislamiento Conciencial: Resort / Lobby Hotel Boutique",
                "titulo_en": "Conscious Isolation: Resort / Boutique Hotel Lobby",
                "porque": "Ansiedad social aguda. Ruido mental. Sobrecarga económica.", "porque_en": "Acute social anxiety. Mental noise. Economic overload.",
                "que_hacer": "Hotel/resort. Butaca premium. Cierra ojos 60s. Respira lento. Habita tu cuerpo.",
                "que_hacer_en": "Hotel/resort. Premium armchair. Close eyes 60s. Breathe slowly. Inhabit your body.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Zona de descanso, jardín interior o lobby de un hotel.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.",
                "gps": "boutique hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 95, "contemplacion": 95, "organizacion": 80, "salud": 90, "esperanza": 90, "sombra": 80}
            },
            {
                "id": 347,
                "titulo": "Estrategia de Alivio: Terminal de Aerolíneas",
                "titulo_en": "Relief Strategy: Airline Terminal",
                "porque": "Asfixia y pánico. Encierro rutina laboral.", "porque_en": "Suffocation and panic. Work routine confinement.",
                "que_hacer": "Terminal aérea. Vestíbulo principal. Despega ojos pantalla. Observa viajeros. Mundo es inmenso.",
                "que_hacer_en": "Airline terminal. Main lobby. Eyes off screen. Observe travelers. World is huge.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or regional transit hub.",
                "gps": "transit center or airport terminal",
                "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 60, "movimiento": 40, "aprendizaje": 50}
            },
            {
                "id": 348,
                "titulo": "Módulo de Silencio Comunitario: Cafetería Local",
                "titulo_en": "Community Silence Module: Local Coffee Shop",
                "porque": "Aislamiento mental destructivo. Parálisis por ansiedad.", "porque_en": "Destructive mental isolation. Anxiety paralysis.",
                "que_hacer": "Cafetería tranquila. Pide bebida. Siéntate. Observa movimientos. Aroma café. Desacelera.",
                "que_hacer_en": "Quiet coffee shop. Order drink. Sit. Observe movements. Coffee aroma. Decelerate.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cafetería o establecimiento de bebidas local.", "donde_en": "Local coffee shop or beverage venue.",
                "gps": "quiet cafe or bakery",
                "vector_necesidades": {"comunidad": 90, "descanso": 85, "silencio": 75, "alimentacion": 60, "contemplacion": 80, "esperanza": 85, "musica": 30}
            },
            {"id": 123, "titulo": "Jardín de Rocas/Zen", "titulo_en": "Rock/Zen Garden",
                "porque": "Mente agitada. Busca orden y armonía.", "porque_en": "Agitated mind. Seek order/harmony.",
                "que_hacer": "Jardín de rocas. Observa formas. Medita en su calma.", "que_hacer_en": "Rock garden. Observe shapes. Meditate in calm.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90}
            },
            {"id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park",
                "porque": "Necesitas risas y alegría. Observa juego inocente.", "porque_en": "Need laughter/joy. Observe innocent play.",
                "que_hacer": "Parque de perros. Observa interacción. Siente diversión.", "que_hacer_en": "Dog park. Observe interaction. Feel the fun.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90}
            },
            {"id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music",
                "porque": "Mente estresada. Experiencia sensorial. Música te calme.", "porque_en": "Stressed mind. Sensory experience. Music calms you.",
                "que_hacer": "Lugar con música en vivo tranquila. Escucha, relájate.", "que_hacer_en": "Place with calm live music. Listen, relax.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85}
            },
            {"id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool",
                "porque": "Cuerpo tenso. Mente agitada. Agua relaja. Flota preocupaciones.", "porque_en": "Tense body. Agitated mind. Water relaxes. Float worries away.",
                "que_hacer": "Piscina pública. Chapuzón o relájate en el agua.", "que_hacer_en": "Public pool. Take a dip or relax in water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85}
            },
            {"id": 241, "titulo": "Distracción Absoluta: Centro de Recreación / Parque Temático", "titulo_en": "Absolute Distraction: Recreation Center / Theme Park",
                "porque": "Ansiedad cíclica. Rumiación masiva. Shock de juego y risas.", "porque_en": "Cyclic anxiety, massive rumination. Play/laughter shock.",
                "que_hacer": "Parque atracciones/centro familiar. Observa colores, risas. Conecta con juego inocente.",
                "que_hacer_en": "Amusement park/family entertainment. Observe colors, laughter. Connect with innocent play.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.",
                "gps": "amusement park or arcade",
                "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50}
            },
            {"id": 242, "titulo": "Estrategia de Alivio: Terminal de Aerolíneas", "titulo_en": "Relief Strategy: Airline Terminal",
                "porque": "Asfixia y pánico. Encierro rutina laboral.", "porque_en": "Suffocation/panic from daily USA work routine confinement.",
                "que_hacer": "Terminal aérea/agencia viajes. Camina pasillo central. Observa viajeros. Mundo es inmenso.",
                "que_hacer_en": "Airline terminal/travel agency. Walk central hall. Watch travelers. Grasp world's vastness.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.",
                "gps": "transit center or airport terminal",
                "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30}
            },
            {"id": 243, "titulo": "Aislamiento Conciencial: Resort / Hotel Lounge", "titulo_en": "Conscious Isolation: Resort / Hotel Lounge",
                "porque": "Ansiedad social aguda. Ruido mental. Sobrecarga económica.", "porque_en": "Acute social anxiety, mental noise from economic overload.",
                "que_hacer": "Hotel/resort (gratis). Butaca premium. Cierra ojos. Respira diafragmático. Habita órganos.",
                "que_hacer_en": "Hotel lounge/resort (free). Premium armchair. Close eyes. Breathe diaphragmatic. Fully inhabit organs.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Zona de descanso o jardín de un hotel.", "donde_en": "Lounge or garden of a USA hotel.",
                "gps": "boutique hotel lobby",
                "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 95, "organizacion": 80, "salud": 85, "esperanza": 85}
            },
            {"id": 244, "titulo": "Soberanía de Cabina: Terminal Aérea / Vuelos", "titulo_en": "Cabin Sovereignty: Air Terminal / Flights",
                "porque": "Asfixia, pánico. Desconexión corporal por saturación ruidosa.", "porque_en": "Suffocation, panic, bodily disconnection due to noisy urban saturation.",
                "que_hacer": "Aeropuerto/terminal. Ventanal vista cielo. Módulo Ventilación: 3 exhalaciones diafragmáticas.",
                "que_hacer_en": "Airport/flight terminal. Sky-view window. Ventilation Module: 3 diaphragmatic exhalations.",
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
        mejores_candidatos_para_eleccion = candidates[:min(3, len(candidatos))]
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
            ids_seleccionados.add(mision_aleatoria["id"]) # Fix: Use mision_aleatoria["id"]

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

# New endpoint for developer login
@app.post("/api/login")
async def login(request: Request):
    payload = await request.json()
    username = payload.get("username")
    password = payload.get("password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return JSONResponse({"success": True})
    return JSONResponse({"success": False, "message": "Credenciales inválidas"}, status_code=401)

# New endpoint for creating Stripe Checkout Sessions
@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    payload = await request.json()
    price_id = payload.get("priceId")
    lang = payload.get("lang", "es")
    
    # Determine currency based on locale, assuming USD for now
    currency = "usd"

    checkout_session_data = {
        'line_items': [{
            'price': price_id,
            'quantity': 1,
        }],
        'mode': 'subscription' if 'sub' in price_id else 'payment', # Correct mode for one-time or subscription
        'success_url': f"https://open-than-go.onrender.com/static/session.html?payment=success&lang={lang}",
        'cancel_url': f"https://open-than-go.onrender.com/static/session.html?payment=cancel&lang={lang}",
    }

    try:
        checkout_session = stripe.checkout.Session.create(**checkout_session_data)
        return JSONResponse({"sessionId": checkout_session.id})
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

# New endpoint for Stripe webhooks (no DB integration, just logging for demo)
@app.post("/webhook")
async def stripe_webhook(request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print(f"Webhook Error: Invalid payload - {e}")
        return JSONResponse({"error": "Invalid payload"}, status_code=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Webhook Error: Invalid signature - {e}")
        return JSONResponse({"error": "Invalid signature"}, status_code=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')
        print(f"Payment successful for session {session.id}, customer: {customer_email}")
        # In a real application, you would:
        # 1. Retrieve user details (e.g., from session.client_reference_id if you passed it)
        # 2. Update your database to reflect the user's paid status or subscription.
        # 3. Potentially provision access or send confirmation emails.
        # For this demo, we'll just log and rely on client-side confirmation for temporary access.
        # If it's a subscription, you might also get a 'customer.subscription.created' event.
    elif event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        print(f"Subscription created for customer {subscription.customer}, subscription ID: {subscription.id}")
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        print(f"Subscription deleted for customer {subscription.customer}, subscription ID: {subscription.id}")
        # In a real app, revoke access for this user.
    else:
        print(f"Unhandled event type {event['type']}")

    return JSONResponse({"status": "success"})

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
            instruccion_fisiologica_es = "Templo consumo. Hackea: detén marcha, inhala/exhala. Repite: 'Yo soy el único producto que importa hoy'. Sal de rutina."
            instruccion_fisiologica_en = "Consumption temple. Hack: stop, inhale/exhale. Repeat: 'I am the only product that matters today'. Exit routine."
        elif marca_detectada == "Amazon":
            instruccion_fisiologica_es = "Mente busca dopamina. Bloquea pantalla. Enfócate espacio biológico: hidrátate o elimina toxinas. Invierte en tus células."
            instruccion_fisiologica_en = "Mind seeks dopamine. Block screen. Focus biological space: hydrate/detox. Invest in cells."
        elif marca_detectada in ["Youtube", "Tiktok", "Instagram"]:
            instruccion_fisiologica_es = "Algoritmo secuestra atención. Interrumpe bucle. Suelta teléfono, cierra ojos 60s. Respira profundo, libera estrés."
            instruccion_fisiologica_en = "Algorithm hijacks attention. Break loop. Drop phone, close eyes 60s. Breathe deep, release stress."
        elif marca_detectada == "Spotify":
            instruccion_fisiologica_es = "Usas sonidos para aislarte. Detén audio. Módulo Silencio Mental 1 min. Siente tu ritmo cardíaco."
            instruccion_fisiologica_en = "Use sounds to isolate. Stop audio. 1-min Mental Silence Module. Feel heart rhythm."
        else: # Default case
            instruccion_fisiologica_es = f"Identificaste que [{marca_detectada}] satura tu mente. Rebélate: usa pasillos, aire libre o ventanas. Pausa biológica profunda 60s. Recupera control."
            instruccion_fisiologica_en = f"Identified [{marca_detectada}] saturates mind. Rebel: use halls, open air, windows. Deep 60-sec biological pause. Regain control."

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
    # 1. INTERVENCION DOMÉSTICA (MODO CASA)
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

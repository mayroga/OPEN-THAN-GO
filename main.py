# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.1 # Company: May Roga LLC # File: main.py - SECCIÓN 1 DE 2 (Backend Core)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random
import re
from datetime import datetime
import urllib.parse
import stripe

# ============================================================
# INYECCIÓN CRÍTICA DE CONTROL: PASARELA STRIPE & BYPASS MAESTRO
# ============================================================
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
ADMIN_USER = os.environ.get("ADMIN_USERNAME")
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD")

# Matriz oficial de Price IDs inmutables de Stripe
PLANES_STRIPE = {
    "unico": "price_1TtbjXBOA5mT4t0PMCJSext6",
    "mensual": "price_1TtblSBOA5mT4t0PGiYvT2l9",
    "anual": "price_1TtbltBOA5mT4t0PpJ8io219"
}
# ============================================================

link_base = "https://www.google.com/maps/search/?api=1&query="
app = FastAPI()

# Ensure the 'static' directory exists before mounting
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

DEFAULT_NECESSITY_VECTOR = {
    "movimiento": 50,
    "naturaleza": 50,
    "silencio": 50,
    "agua": 50,
    "sol": 50,
    "sombra": 50,
    "aire_fresco": 50,
    "creatividad": 50,
    "comunidad": 50,
    "aprendizaje": 50,
    "juego": 50,
    "contemplacion": 50,
    "descanso": 50,
    "organizacion": 50,
    "alimentacion": 50,
    "musica": 50,
    "risa": 50,
    "esperanza": 50,
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
    for k in needs_to_consider: # Suma las diferencias absolutas de cada necesidad
        distancia += abs(
            vector1.get(k, DEFAULT_NECESSITY_VECTOR.get(k, 50)) - vector2.get(k, DEFAULT_NECESSITY_VECTOR.get(k, 50))
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
            {"id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade", "porque": "Mente cansada de pantallas. El piloto automático te apaga. El asfalto drena tu energía.", "porque_en": "Screen-tired mind. Autopilot turns you off. Asphalt drains your energy.", "que_hacer": "Encuentra un gran árbol. Toca la corteza con tus manos. Nota la frescura bajo las hojas.", "que_hacer_en": "Find a large tree. Touch the bark with your hands. Notice the coolness under leaves.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade", "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85} }, {"id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe", "porque": "Exiges un respiro mental. Demasiado ruido acumulado en la semana. Buscas calma interior.", "porque_en": "Demanding a mental break. Too much noise accumulated this week. Seek inner calm.", "que_hacer": "Visita una cafetería tranquila. Pide tu bebida favorita. Observa el entorno sin mirar pantallas.", "que_hacer_en": "Visit a quiet coffee shop. Order your favorite drink. Observe surroundings without checking screens.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Establecimiento local pacífico.", "donde_en": "Peaceful local establishment.", "gps": "quiet cafe", "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70} }, {"id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden", "porque": "Cerebro agotado por la rutina urbana. Necesitas reconectarte con lo vivo. Falta aire puro.", "porque_en": "Brain exhausted by urban routine. Need to reconnect with life. Lack of pure air.", "que_hacer": "Pasea sin prisa por los senderos. Contempla las texturas de las hojas. Respira hondo.", "que_hacer_en": "Stroll leisurely through paths. Contemplate the textures of leaves. Breathe deeply.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Paraje botánico público.", "donde_en": "Public botanical site.", "gps": "botanical garden", "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90} },

            {"id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook", "porque": "Requieres perspectiva. La rutina te achica la mirada. Eleva el enfoque para romper la inercia diaria.", "porque_en": "Requiring perspective. Routine narrows your gaze. Elevate focus to break daily inertia.", "que_hacer": "Encuentra un punto alto. Observa la línea del horizonte. Deja que la inmensidad limpie tus pensamientos.", "que_hacer_en": "Find a high point. Observe the horizon line. Let immensity clear your thoughts.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook", "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95} }, {"id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class", "porque": "Mente sobrecargada. Demasiado ruido acumulado en tu ser. Necesitas regular el ritmo biológico.", "porque_en": "Overloaded mind. Too much accumulated noise inside you. Need to regulate biological rhythm.", "que_hacer": "Asiste a una sesión guiada. Cierra los ojos. Concéntrate en el aire y suelta todo control.", "que_hacer_en": "Attend a guided session. Close your eyes. Focus on the air and let go of all control.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class", "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90} }, {"id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing", "porque": "Pensamiento agitado por la prisa. El entorno plano te encierra. Necesitas mirar la inmensidad del cielo.", "porque_en": "Thoughts agitated by rush. Flat environment locks you in. Need to watch the vastness of the sky.", "que_hacer": "Busca un lugar abierto. Recuéstate sobre el suelo. Observa las formas sin juzgar tus ideas.", "que_hacer_en": "Find an open space. Lie down on the ground. Observe shapes without judging your ideas.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing", "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85} },

            {"id": 355, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Agotamiento periférico absoluto. Fatiga acumulada por navegar el tráfico pesado. El volante consume tu paz.", "porque_en": "Absolute peripheral exhaustion. Accumulated fatigue from navigating heavy traffic. The steering wheel consumes your peace.", "que_hacer": "Detén la marcha. Suelta el teléfono. Cierra los ojos. Apoya las palmas sobre tus muslos. Siente la inmovilidad de tu cuerpo por un minuto entero.", "que_hacer_en": "Stop moving. Drop your phone. Close your eyes. Place your palms on your thighs. Feel your body's stillness for a whole minute.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cabina de transporte, parada o asiento de pasajero.", "donde_en": "Transit vehicle cabin, stop, or passenger seat.", "gps": "quiet public square", "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 15, "contemplacion": 85, "esperanza": 80, "salud": 80, "aire_fresco": 60} }, {"id": 356, "titulo": "Módulo de Cambio Frecuencial", "titulo_en": "Frequency Shift Module", "porque": "Saturación mental profunda. Cansancio auditivo por ruido mecánico y pantallas. Tu atención está fragmentada.", "porque_en": "Deep mental saturation. Auditory fatigue from mechanical noise and screens. Your attention is fragmented.", "que_hacer": "Ponte auriculares. Escucha un tono binaural limpio o sonidos de lluvia. Apoya la cabeza hacia atrás. Permite que el silencio acústico ordene tu mente.", "que_hacer_en": "Put on headphones. Listen to a clean binaural beat or rain sounds. Lean your head back. Allow the acoustic silence to organize your mind.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Tu espacio de descanso, oficina vacía o vehículo.", "donde_en": "Your resting space, empty office, or vehicle.", "gps": "quiet open park", "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 65, "contemplacion": 90, "esperanza": 85, "salud": 80, "creatividad": 40} }, {"id": 357, "titulo": "Mapeo de Flujos", "titulo_en": "Flow Mapping", "porque": "Agotamiento por sedentarismo físico. La inactividad estanca tu circulación. Necesitas activar tus piernas de inmediato.", "porque_en": "Exhaustion from physical sedentarism. Inactivity stagnates your circulation. Need to activate your legs immediately.", "que_hacer": "Entra a un gran almacén climatizado. Camina a paso firme por los pasillos perimetrales externos. Siente el movimiento de tus extremidades sin apuro de comprar.", "que_hacer_en": "Enter a large climate-controlled warehouse. Walk steadily through the outer perimeter aisles. Feel your limbs moving with no shopping rush.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Pasillos industriales de una gran tienda de tu Código Postal.", "donde_en": "Industrial aisles of a large warehouse store in your Zip Code.", "gps": "wholesale club or market", "vector_necesidades": {"movimiento": 85, "organizacion": 70, "contemplacion": 60, "comunidad": 50, "juego": 30, "descanso": 20, "silencio": 10} },

            {"id": 358, "titulo": "Oasis Burocrático", "titulo_en": "Bureaucratic Oasis", "porque": "Fatiga extrema por esperas tensas y trámites largos. Las pantallas drenan tu paciencia. Requieres un refugio analógico.", "porque_en": "Extreme fatigue from tense waiting and long paperwork. Screens drain your patience. Require an analog refuge.", "que_hacer": "Entra a la biblioteca pública más cercana. Camina en absoluto silencio. Toma asiento en la zona de lectura. Disfruta la quietud del entorno.", "que_hacer_en": "Enter the nearest public library. Walk in absolute silence. Take a seat in the reading area. Enjoy the stillness of the environment.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Sala de lectura, biblioteca municipal o zona de estudio de USA.", "donde_en": "Reading room, municipal library, or USA study zone.", "gps": "public library", "vector_necesidades": {"aprendizaje": 100, "silencio": 100, "contemplacion": 90, "descanso": 85, "organizacion": 70, "salud": 80} }, {"id": 201, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Mente saturada por conducir bajo tensión. El tráfico continuo bloquea tus pensamientos. Tu cuerpo está al límite.", "porque_en": "Mind saturated from driving under tension. Continuous traffic blocks your thoughts. Your body is at its limit.", "que_hacer": "Detén la marcha de forma segura. Apoya las palmas sobre tus rodillas. Cierra los ojos. Ejecuta un minuto entero de quietud total.", "que_hacer_en": "Stop moving safely. Place your palms on your knees. Close your eyes. Execute a whole minute of total stillness.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cabina de transporte o asiento de pasajero.", "donde_en": "Rideshare cabin or passenger seat.", "gps": "quiet park bench", "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 10, "contemplacion": 80, "esperanza": 80, "naturaleza": 20, "aire_fresco": 50} }, {"id": 202, "titulo": "Módulo Auditivo", "titulo_en": "Auditory Reset", "porque": "Agotamiento mental agudo por ruidos urbanos. Las notificaciones digitales fragmentan tu atención. Requieres un reseteo sonoro inmediato.", "porque_en": "Acute mental exhaustion from urban noises. Digital notifications fragment your attention. Require an immediate sound reset.", "que_hacer": "Colócate auriculares aislantes. Reproduce ruidos de lluvia limpia o frecuencias puras. Cierra los ojos. Nota cómo se ordena tu espacio interior.", "que_hacer_en": "Put on noise-canceling headphones. Play clean rain sounds or pure frequencies. Close your eyes. Notice your inner space organizing itself.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cualquier rincón cómodo o dentro de tu auto.", "donde_en": "Any comfortable spot or inside your car.", "gps": "quiet library space", "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 60, "contemplacion": 90, "esperanza": 85, "creatividad": 40} },

            {"id": 203, "titulo": "Descompresión de Entorno", "titulo_en": "Environment Decompression", "porque": "Saturación del espacio habitual. El piloto automático te encierra en lo conocido. Necesitas un perímetro diseñado para el confort.", "porque_en": "Usual space saturation. Autopilot traps you in the familiar. Need a perimeter designed for comfort.", "que_hacer": "Entra al vestíbulo de un gran hotel. Toma asiento en la sala común de descanso. Relaja la vista mirando un punto lejano dos minutos.", "que_hacer_en": "Enter the lobby of a large hotel. Take a seat in the common lounge area. Relax your eyes by looking at a distant point for two minutes.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Lobby o zona de descanso de un hotel local.", "donde_en": "Lobby or lounge area of a local hotel.", "gps": "hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 70, "esperanza": 80, "movimiento": 20} }, {"id": 204, "titulo": "Sabotaje de Espera", "titulo_en": "Waiting Sabotage", "porque": "Falta de nutrición intelectual real. Tu atención está drenada por estímulos vacíos. Requieres un entorno de conocimiento absoluto.", "porque_en": "Lack of real intellectual nourishment. Your attention is drained by empty stimuli. Require an environment of absolute knowledge.", "que_hacer": "Ve al campus o área de libros de una universidad cercana. Camina en absoluto silencio por los pasillos perimetrales abiertos. Observa en calma.", "que_hacer_en": "Go to the campus or book section of a nearby university. Walk in absolute silence through the open perimeter corridors. Observe calmly.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Campus universitario o biblioteca pública.", "donde_en": "University campus or public library.", "gps": "university library", "vector_necesidades": {"aprendizaje": 100, "silencio": 90, "contemplacion": 85, "descanso": 70, "aire_fresco": 75, "movimiento": 40} }, ], "estresado": [ {"id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk", "porque": "Cuerpo rígido por el estrés diario. Necesitas liberar la tensión muscular mediante la fuerza física. Tu respiración exige intensidad.", "porque_en": "Body stiff from daily stress. Need to release muscle tension through physical strength. Your breathing demands intensity.", "que_hacer": "Encuentra una rampa inclinada o escaleras públicas elevadas. Sube a paso firme. Siente la fuerza real de tus piernas.", "que_hacer_en": "Find a steep ramp or elevated public stairs. Climb at a firm pace. Feel the real strength of your legs.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public stairs", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75} },

            {"id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga", "porque": "Mente acelerada por exigencias externas. Tu atención está fragmentada. Necesitas coordinar cuerpo y naturaleza con respiración consciente.", "porque_en": "Racing mind from external demands. Your attention is fragmented. Need to coordinate body and nature with conscious breathing.", "que_hacer": "Busca un parque tranquilo. Extiende una lona sobre el suelo. Sigue una secuencia firme de estiramientos corporales prolongados.", "que_hacer_en": "Find a quiet park. Lay a mat on the ground. Follow a steady sequence of prolonged body stretches.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park", "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80} }, {"id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym", "porque": "Saturación mental y energía estancada. Necesitas convertir la tensión nerviosa en fuerza física pura. Activa tus extremidades.", "porque_en": "Mental saturation and stagnant energy. Need to convert nervous tension into pure physical strength. Activate your limbs.", "que_hacer": "Entra a un centro deportivo público. Enfócate estrictamente en una rutina pesada de ejercicios. Suda para vaciar la mente.", "que_hacer_en": "Enter a public sports center. Focus strictly on a heavy exercise routine. Sweat to empty your mind.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym", "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60} }, {"id": 320, "titulo": "Liberación de Impacto", "titulo_en": "Impact Release", "porque": "Rigidez muscular severa y rabia acumulada. El sedentarismo te asfixia. Necesitas romper la coraza física de inmediato.", "porque_en": "Severe muscular rigidity and accumulated anger. Sedentary lifestyle suffocates you. Need to break the physical armor immediately.", "que_hacer": "Dirígete a un parque de trampolines o centro de escalada. Ejecuta saltos con fuerza descargando peso en la lona para drenar el agobio diario.", "que_hacer_en": "Head to a trampoline park or climbing center. Execute powerful jumps discharging your weight on the mat to drain daily overwhelm.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque de trampolines o centro deportivo de alta descarga en tu Código Postal.", "donde_en": "Trampoline park or high-discharge sports center in your Zip Code.", "gps": "trampoline park or climbing gym", "vector_necesidades": {"movimiento": 100, "juego": 100, "risa": 90, "salud": 95, "descanso": 0, "silencio": 10, "comunidad": 60, "esperanza": 90} },

            {"id": 321, "titulo": "Módulo de Hidro-Calma", "titulo_en": "Hydro-Calm Module", "porque": "Sistema nervioso en alerta roja permanente. El ruido urbano te asfixia por dentro. El agua templada en movimiento es el alivio somático definitivo.", "porque_en": "Nervous system on permanent red alert. Urban noise suffocates you inside. Moving warm water is the ultimate somatic relief.", "que_hacer": "Visita una piscina municipal o YMCA. Sumérgete en el agua templada. Cierra los ojos. Concéntrate durante dos minutos únicamente en flotar sin hacer esfuerzo.", "que_hacer_en": "Visit a municipal pool or YMCA. Submerge in warm water. Close your eyes. Focus for two minutes solely on floating without making any effort.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "YMCA, alberca climatizada o spa comunitario local.", "donde_en": "YMCA, heated pool, or local community spa.", "gps": "ymca pool or public spa", "vector_necesidades": {"agua": 100, "descanso": 100, "salud": 95, "silencio": 60, "contemplacion": 90, "sombra": 80, "esperanza": 85, "movimiento": 20} }, {"id": 322, "titulo": "Quiebre de Frecuencias", "titulo_en": "Frequency Break", "porque": "Mente acelerada con ideas fijas. Sufres de un zumbido interno debido al estrés digital continuo. Tu atención está fragmentada por las notificaciones.", "porque_en": "Racing mind with fixed ideas. Suffering from internal buzzing due to continuous digital stress. Your attention is fragmented by notifications.", "que_hacer": "Busca un estudio de meditación o yoga. Siéntate en silencio en el vestíbulo o sala común. Escucha la quietud del lugar inhalando profundo.", "que_hacer_en": "Look for a meditation or yoga studio. Sit in silence in the lobby or common room. Listen to the stillness of the place while breathing deeply.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Estudio de yoga, centro de meditación o sound healing en USA.", "donde_en": "Yoga studio, meditation center, or sound healing spot in the USA.", "gps": "sound healing or yoga studio", "vector_necesidades": {"silencio": 100, "descanso": 95, "musica": 90, "contemplacion": 95, "salud": 90, "esperanza": 90, "organizacion": 70} }, {"id": 323, "titulo": "Aislamiento Orgánico", "titulo_en": "Organic Isolation", "porque": "Estrés acumulado por la velocidad de la ciudad. El concreto drena tu vitalidad. Requieres elementos del bosque y aire puro para calmar tu sistema.", "porque_en": "Accumulated stress from city speed. Concrete drains your vitality. Require forest elements and pure air to calm your system.", "que_hacer": "Dirígete a una reserva natural o parque estatal. Entra al sendero. Toca la corteza de un gran árbol por un minuto completo sintiendo la brisa.", "que_hacer_en": "Head to a nature reserve or state park. Enter the trail. Touch the bark of a large tree for a full minute while feeling the breeze.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Sendero boscoso, reserva natural o parque estatal de tu región.", "donde_en": "Wooded trail, nature reserve, or state park in your region.", "gps": "state park trail or nature reserve", "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "silencio": 85, "movimiento": 60, "contemplacion": 90, "descanso": 60, "esperanza": 95, "sol": 70} },

            {"id": 112, "titulo": "Sendero Corto Natural", "titulo_en": "Short Nature Trail", "porque": "Sobrecarga de estímulos artificiales. El piloto automático apaga tus sentidos en el asfalto. Necesitas desconectar caminando en paz.", "porque_en": "Artificial stimuli overload. Autopilot turns off your senses on asphalt. Need to disconnect by walking in peace.", "que_hacer": "Encuentra un camino verde. Camina a paso ligero balanceando tus brazos. Observa el contorno del paisaje sin prisa.", "que_hacer_en": "Find a green path. Walk briskly swinging your arms. Observe the landscape's contour without rush.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Sendero natural o bosque.", "donde_en": "Nature trail or forest.", "gps": "short nature trail", "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "agua": 40, "sol": 60, "sombra": 70, "aire_fresco": 100, "creatividad": 40, "comunidad": 20, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "descanso": 60, "organizacion": 20, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85} }, {"id": 113, "titulo": "Pista de Atletismo", "titulo_en": "Running Track", "porque": "Mente acelerada por la inercia diaria. Acumulas energía estancada en el cuerpo. Libera esa fuerza extra enfocando tu propio ritmo.", "porque_en": "Racing mind from daily inertia. Accumulating stagnant energy in the body. Release that extra strength by focusing your own rhythm.", "que_hacer": "Dirígete a un circuito deportivo público. Corre o avanza a paso firme. Suelta las tensiones con cada zancada sobre la pista.", "que_hacer_en": "Go to a public sports circuit. Run or move at a firm pace. Release tension with every stride on the track.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Pista de atletismo pública.", "donde_en": "Public running track.", "gps": "public running track", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 40, "agua": 10, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 10, "comunidad": 50, "aprendizaje": 20, "juego": 30, "contemplacion": 50, "descanso": 10, "organizacion": 70, "alimentacion": 0, "musica": 50, "risa": 20, "esperanza": 70} }, {"id": 251, "titulo": "Soberanía en Movimiento", "titulo_en": "Sovereignty in Motion", "porque": "Saturación nerviosa por el encierro habitual. El tráfico denso encapsula tu atención. La sobrecarga de trayectos drena tu presencia corporal.", "porque_en": "Nervous saturation from usual confinement. Heavy traffic encapsulates your attention. Transit overload drains your bodily presence.", "que_hacer": "Despega la mirada de la pantalla. Apoya las palmas firmes sobre tus rodillas. Endereza tu columna. Exhala todo el aire residual de golpe.", "que_hacer_en": "Take your eyes off the screen. Place your palms firmly on your knees. Straighten your spine. Exhale all residual air at once.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cabina de transporte, asiento de pasajero o parada de autobús de USA.", "donde_en": "Transit cabin, passenger seat, or USA bus stop.", "gps": "quiet rest areas or public plazas", "vector_necesidades": {"descanso": 95, "silencio": 85, "movimiento": 20, "contemplacion": 90, "organizacion": 60, "esperanza": 80} },

            {"id": 252, "titulo": "Hackeo al Tráfico", "titulo_en": "Traffic Hack", "porque": "Nivel de estrés elevado por embotellamientos continuos. El ruido de la autopista fragmenta tu paz. Caes en el automatismo de las carreteras.", "porque_en": "Elevated stress levels from continuous traffic jams. Highway noise fragments your peace. You fall into the automation of roads.", "que_hacer": "Aprovecha la próxima parada segura o luz roja. Suelta la tensión de tu mandíbula abriendo grande la boca. Estira tus dedos sobre el volante liberando rigidez.", "que_hacer_en": "Take advantage of the next safe stop or red light. Release your jaw tension by opening your mouth wide. Stretch your fingers over the steering wheel releasing stiffness.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Área de servicio de autopista, rampa pública o intersección vial.", "donde_en": "Highway service area, public ramp, or road intersection.", "gps": "highway rest stop or overlook", "vector_necesidades": {"movimiento": 80, "descanso": 70, "silencio": 50, "aire_fresco": 85, "organizacion": 40, "salud": 85} }, {"id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route", "porque": "Necesitas liberar tensión muscular acumulada. Moverte rápido rompe la inercia diaria. El asfalto exige atención y enfoque activo.", "porque_en": "Need to release accumulated muscle tension. Moving fast breaks daily inertia. Asphalt demands attention and active focus.", "que_hacer": "Encuentra un carril bici seguro y pedalea de inmediato. Siente la velocidad del viento en tu rostro. Recupera el control de tu dirección.", "que_hacer_en": "Find a safe bike lane and pedal immediately. Feel the speed of the wind on your face. Regain control of your direction.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route", "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80} }, {"id": 211, "titulo": "Soberanía de Cabina", "titulo_en": "Cabin Sovereignty", "porque": "Saturación nerviosa extrema por ruidos de tránsito masivo. Te rodea la prisa industrial. Necesitas recordar la escala natural del mundo.", "porque_en": "Extreme nervous saturation from mass transit noise. Industrial haste surrounds you. Need to remember the natural scale of the world.", "que_hacer": "Busca la ventana abierta más grande hacia el cielo. Haz tres inhalaciones profundas sosteniendo el aire. Siente tu cuerpo presente lejos de la velocidad.", "que_hacer_en": "Find the largest open window facing the sky. Take three deep breaths holding the air. Feel your body present away from speed.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Terminal de aeropuerto o zona de observación abierta.", "donde_en": "Airport terminal or open observation zone.", "gps": "airport observation area", "vector_necesidades": {"aire_fresco": 100, "contemplacion": 95, "silencio": 60, "descanso": 50, "movimiento": 30, "esperanza": 80} },

            {"id": 212, "titulo": "Depuración Exocrina", "titulo_en": "Exocrine Cleansing", "porque": "Exceso de adrenalina acumulada por estrés laboral crónico. Tu organismo está saturado de alertas digitales. Requieres un vaciado somático.", "porque_en": "Excess adrenaline accumulated from chronic work stress. Your organism is saturated with digital alerts. Require a somatic emptying.", "que_hacer": "Ve al gimnasio o piscina pública más cercana. Haz fuerza de forma continua. Suda intensamente para liberar la tensión de tus músculos.", "que_hacer_en": "Go to the nearest gym or public pool. Use your strength continuously. Sweat intensely to release the tension from your muscles.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Gimnasio público, cancha o alberca comunitaria.", "donde_en": "Public gym, court, or community pool.", "gps": "community fitness center", "vector_necesidades": {"movimiento": 100, "agua": 80, "salud": 90, "juego": 50, "descanso": 0, "silencio": 20, "risa": 40} }, {"id": 213, "titulo": "Estabilización Somática", "titulo_en": "Somatic Stabilization", "porque": "Aceleración del ritmo cardíaco por la prisa. Experimentas una sensación física de vulnerabilidad o agobio. Tu cuerpo exige detenerse por completo.", "porque_en": "Accelerated heart rate from rushing. You experience a physical feeling of vulnerability or overwhelm. Your body demands to stop completely.", "que_hacer": "Entra a una farmacia o clínica local. Consigue agua fresca. Bebe un vaso pequeño muy despacio. Siente cómo el líquido estabiliza tu pulso.", "que_hacer_en": "Enter a local pharmacy or clinic. Get fresh water. Drink a small cup very slowly. Feel the liquid stabilize your pulse.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Área de descanso de una farmacia o clínica local.", "donde_en": "Lounge area of a local pharmacy or clinic.", "gps": "pharmacy health lounge", "vector_necesidades": {"agua": 100, "salud": 95, "descanso": 80, "silencio": 70, "organizacion": 80, "esperanza": 85} }, ], "aburrido": [ {"id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk", "porque": "Días idénticos y repetitivos. La rutina visual apaga tu cerebro. Necesitas buscar novedad para despertar tu curiosidad instintiva.", "porque_en": "Identical and repetitive days. Visual routine turns off your brain. Need to seek novelty to awaken your instinctive curiosity.", "que_hacer": "Camina despacio por la calle. Encuentra murales o expresiones de arte urbano en tu zona. Detente a escanear los detalles y trazos.", "que_hacer_en": "Walk slowly through the street. Find murals or street art expressions in your area. Stop to scan the details and lines.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street art", "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95} },

            {"id": 307, "titulo": "Descompresión de Perímetro", "titulo_en": "Perimeter Decompression", "porque": "Monotonía del espacio habitual. Tu cerebro se apaga en lo conocido. Necesitas un entorno de hermoso diseño para cambiar tus estímulos visuales.", "porque_en": "Usual space monotony. Your brain shuts down in the familiar. Need a beautifully designed environment to change your visual stimuli.", "que_hacer": "Entra al vestíbulo de un gran hotel. Toma asiento en una de sus butacas públicas. Observa la arquitectura y descansa de las pantallas.", "que_hacer_en": "Enter the lobby of a large hotel. Take a seat in one of its public armchairs. Observe the architecture and take a break from screens.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Lobby o zona de descanso pública de un hotel local.", "donde_en": "Lobby or public lounge area of a local hotel.", "gps": "hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 80, "esperanza": 80, "comunidad": 50, "movimiento": 20} }, {"id": 308, "titulo": "Ampliación del Horizonte", "titulo_en": "Horizon Expansion", "porque": "Falta de perspectiva y estancamiento mental. El encierro nubla tus ideas. Ver el movimiento de viajes globales te devuelve el enfoque.", "porque_en": "Lack of perspective and mental stagnation. Confinement clouds your ideas. Watching the movement of global travel returns your focus.", "que_hacer": "Dirígete al vestíbulo de una central de transportes. Busca el ventanal más amplio hacia el cielo. Realiza tres respiraciones lentas asimilando la inmensidad.", "que_hacer_en": "Head to the lobby of a transit center. Find the widest window facing the sky. Take three slow breaths, taking in the immensity.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30, "aprendizaje": 60} }, {"id": 309, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Bucle mental de apatía o rutina plana. El automatismo te quita el entusiasmo. Necesitas un impacto visual de colores, sonidos y juego.", "porque_en": "Mental loop of apathy or flat routine. Automatism strips away your enthusiasm. You need a visual impact of colors, sounds, and play.", "que_hacer": "Visita un centro de juegos o parque recreativo. Observa las luces titilantes. Escucha las risas del entorno para romper la inercia del día.", "que_hacer_en": "Visit an arcade center or recreation park. Observe the blinking lights. Listen to the laughter around you to break the daytime inertia.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.", "gps": "amusement park or arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50, "creatividad": 60} },

            {"id": 310, "titulo": "Exploración de Espacios", "titulo_en": "Space Exploration", "porque": "Falta de inspiración y estancamiento estético. El entorno monótono duerme tus sentidos. Necesitas visualizar arquitecturas alternativas para expandir tu mente.", "porque_en": "Lack of inspiration and aesthetic stagnation. Monotonous environment numbs your senses. Need to visualize alternative architectures to expand your mind.", "que_hacer": "Revisa diseños de cabañas o casas de campo en tu estado. Analiza la estructura, las texturas y los planos visuales como un ejercicio puro de imaginación.", "que_hacer_en": "Check cabin or country house designs in your state. Analyze the structure, textures, and visual layouts as a pure exercise of imagination.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Interfaz móvil desde tu zona de descanso habitual.", "donde_en": "Mobile interface from your usual resting space.", "gps": "local post office", "vector_necesidades": {"creatividad": 100, "contemplacion": 95, "juego": 70, "organizacion": 80, "esperanza": 85, "descanso": 60, "aprendizaje": 60} }, {"id": 311, "titulo": "Mapeo de Flujos", "titulo_en": "Flow Mapping", "porque": "Rutina plana y falta de acción. Tu cuerpo acumula sedentarismo visual. Caminar por un entorno de suministro masivo altera tu percepción y activa tus piernas.", "porque_en": "Flat routine and lack of action. Your body accumulates visual sedentarism. Walking through a mass supply environment alters your perception and activates your legs.", "que_hacer": "Dirígete al club de precios más cercano. Avanza a paso firme por los pasillos perimetrales externos. Siente el movimiento de tus extremidades de forma constante.", "que_hacer_en": "Head to the nearest price club. Walk steadily through the outer perimeter aisles. Feel your limbs moving constantly.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Pasillos industriales de un gran almacén de USA.", "donde_en": "Industrial aisles of a large USA warehouse store.", "gps": "wholesale club or warehouse", "vector_necesidades": {"movimiento": 85, "organizacion": 75, "comunidad": 60, "contemplacion": 60, "juego": 40, "descanso": 10, "silencio": 5} }, {"id": 312, "titulo": "Sabotaje de Espera", "titulo_en": "Waiting Sabotage", "porque": "Bucle mental aburrido y predecible. Las mismas paredes de siempre te quitan el entusiasmo. Necesitas una inyección de aire fresco y entornos de estudio.", "porque_en": "Bored and predictable mental loop. The same old walls take away your enthusiasm. You need an injection of fresh air and learning environments.", "que_hacer": "Ubica el campus universitario más cercano. Camina en total silencio por sus áreas verdes y plazas comunes. Utiliza este espacio abierto para respirar libremente.", "que_hacer_en": "Locate the nearest university campus. Walk in total silence through its green areas and common plazas. Use this open space to breathe freely.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Áreas comunes abiertas de un campus universitario.", "donde_en": "Open common areas of a university campus.", "gps": "university campus or public school", "vector_necesidades": {"aprendizaje": 100, "aire_fresco": 95, "silencio": 90, "contemplacion": 85, "descanso": 70, "movimiento": 40} },

            {"id": 304, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Inercia mental por estar estancado en el interior. Tu cerebro se duerme en las mismas cuatro paredes de siempre. Necesitas un cambio geográfico rápido para alterar el curso de tus pensamientos.", "porque_en": "Mental inertia from being stuck indoors. Your brain falls asleep within the same four walls. You need a rapid geographical change to alter the course of your thoughts.", "que_hacer": "Sal de tu espacio habitual. Súbete al transporte o camina hacia una zona desconocida. Suelta el teléfono por completo. Mira a través del cristal de forma contemplativa.", "que_hacer_en": "Step out of your usual space. Get on transit or walk towards an unknown area. Drop your phone completely. Look through the glass contemplatively.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Asiento de pasajero en un coche de transporte urbano.", "donde_en": "Passenger seat in an urban transit vehicle.", "gps": "public transit hub or central park", "vector_necesidades": {"juego": 80, "movimiento": 70, "contemplacion": 85, "comunidad": 60, "descanso": 40, "silencio": 30, "esperanza": 80} }, {"id": 305, "titulo": "Descompresión Visual", "titulo_en": "Visual Decompression", "porque": "Bucle cognitivo severo debido a la rutina monótona. Tus ojos están cansados del plano cercano y los entornos grises. Requieres un quiebre estético controlado de forma inmediata.", "porque_en": "Severe cognitive loop due to monotonous routine. Your eyes are tired of near-focus and gray surroundings. Require an immediate controlled aesthetic break.", "que_hacer": "Encuentra un rincón con luz tenue. Busca filmaciones aéreas de horizontes abiertos y paisajes naturales masivos. Observa fijamente la inmensidad por dos minutos para relajar tu musculatura ocular.", "que_hacer_en": "Find a dimly lit corner. Search for aerial footage of open horizons and massive natural landscapes. Stare fixedly at the immensity for two minutes to relax your ocular muscles.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Interfaz de tu teléfono en un rincón con luz tenue.", "donde_en": "Your phone interface in a dimly lit corner.", "gps": "local coffee lounge", "vector_necesidades": {"contemplacion": 100, "descanso": 90, "creatividad": 80, "esperanza": 90, "silencio": 50, "naturaleza": 70, "movimiento": 5} }, {"id": 306, "titulo": "Inversión Controlada", "titulo_en": "Controlled Investment", "porque": "Aburrimiento crónico y parálisis por apatía. Caes en el consumo pasivo de contenido vacío. Requieres una herramienta física real que impulse tu propia capacidad de crear.", "porque_en": "Chronic boredom and paralysis from apathy. You fall into passive consumption of empty content. Require a real physical tool that drives your own capacity to create.", "que_hacer": "Busca un objeto físico pequeño que reactive tu acción, como un libro técnico, un cuaderno o un pincel básico. Haz la adquisición con la certeza absoluta de activar tu motricidad y tu mente.", "que_hacer_en": "Search for a small physical object that reactivates your action, such as a technical book, notebook, or a basic paintbrush. Acquire it with the absolute certainty of activating your motor skills and mind.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Pantalla móvil desde tu espacio de descanso habitual.", "donde_en": "Mobile screen from your usual resting space.", "gps": "local post office", "vector_necesidades": {"juego": 90, "creatividad": 90, "esperanza": 95, "organizacion": 70, "descanso": 60, "aprendizaje": 80, "movimiento": 10} },

            {"id": 301, "titulo": "Auditoría de Frecuencias", "titulo_en": "Frequency Audit", "porque": "Monotonía aplastante en tu rutina diaria. Te faltan estímulos rítmicos y sociales intensos. Tu cerebro necesita un pulso de choque externo.", "porque_en": "Crushing monotony in your daily routine. You lack intense rhythmic and social stimuli. Your brain needs an external shock pulse.", "que_hacer": "Visita una zona de discotecas o club nocturno. Quédate en el perímetro exterior abierto. Nota la vibración profunda del bajo golpeando los muros.", "que_hacer_en": "Visit a club district or nightclub. Stay in the open outer perimeter. Notice the deep bass vibration hitting the walls.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Perímetro exterior, terraza o área abierta de un club nocturno urbano.", "donde_en": "Outer perimeter, terrace, or open area of an urban nightclub.", "gps": "dance club or nightclub", "vector_necesidades": {"juego": 100, "musica": 100, "comunidad": 90, "risa": 80, "movimiento": 70, "creatividad": 60, "silencio": 10, "descanso": 30} }, {"id": 302, "titulo": "Terapia de Pasillo", "titulo_en": "Aisle Therapy", "porque": "Estancamiento mental por el encierro doméstico. Falta variedad en tu entorno visual inmediato. Necesitas estímulos geométricos ordenados y movimiento fluido.", "porque_en": "Mental stagnation from domestic confinement. Lack of variety in your immediate visual environment. Need orderly geometric stimuli and fluid movement.", "que_hacer": "Dirígete a una gran superficie comercial. Recorre los pasillos de forma contemplativa sin intenciones de compra. Camina a paso firme activando tus piernas.", "que_hacer_en": "Head to a large department store. Walk through the aisles contemplatively with no intention to shop. Walk steadily activating your legs.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Gran superficie comercial o tienda céntrica en USA.", "donde_en": "Large department store or central shop in the USA.", "gps": "department store or retail", "vector_necesidades": {"movimiento": 80, "organizacion": 70, "contemplacion": 70, "comunidad": 60, "juego": 50, "descanso": 20, "silencio": 15} }, {"id": 303, "titulo": "Sabotaje Alimenticio", "titulo_en": "Food Sabotage", "porque": "Apatía sensorial por alimentación monótona durante la semana. Comes en piloto automático frente a las pantallas. Requieres un quiebre de sabor real inmediato.", "porque_en": "Sensory apathy from monotonous food during the week. You eat on autopilot in front of screens. Require an immediate real flavor break.", "que_hacer": "Ve a una cafetería o local de comida rápida. Pide un antojo dulce o salado. Cómelo despacio alejando tu teléfono por completo.", "que_hacer_en": "Go to a coffee shop or fast-food spot. Order a sweet or savory treat. Eat it slowly, putting your phone completely away.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cadena de comida rápida o cafetería local en tu Código Postal.", "donde_en": "Fast food chain or local coffee shop in your Zip Code.", "gps": "fast food or local restaurant", "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20} },

            {"id": 253, "titulo": "Auditoría de Frecuencias", "titulo_en": "Frequency Audit", "porque": "Monotonía mental aplastante en tu semana. Te faltan impactos sensoriales reales. Necesitas un quiebre radical mediante ritmos y movimiento.", "porque_en": "Crushing mental monotony in your week. You lack real sensory impacts. You need a radical break through rhythm and movement.", "que_hacer": "Visita una zona de discotecas o club nocturno. Quédate en la acera peatonal exterior abierta. Siente la vibración profunda del bajo golpeando los muros.", "que_hacer_en": "Visit a club district or nightclub. Stay on the open outer pedestrian sidewalk. Feel the deep bass vibration hitting the walls.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Perímetro exterior, terraza o área abierta de un club nocturno urbano.", "donde_en": "Outer perimeter, terrace, or open area of an urban nightclub.", "gps": "nightlife district or dance clubs", "vector_necesidades": {"juego": 100, "musica": 100, "comunidad": 90, "risa": 80, "movimiento": 70, "creatividad": 60, "silencio": 10, "descanso": 30} }, {"id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market", "porque": "Días idénticos que apagan tus sentidos. Necesitas nuevos estímulos orgánicos en tu entorno. Sabores, texturas y olores frescos rompen la inercia visual.", "porque_en": "Identical days that dull your senses. Need new organic stimuli in your environment. Fresh tastes, textures, and smells break visual inertia.", "que_hacer": "Visita un mercado local. Avanza despacio entre los puestos de comida. Prueba un producto artesanal diferente y conversa con los productores.", "que_hacer_en": "Visit a local market. Move slowly through the food stalls. Try a different artisanal product and talk to the producers.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers market", "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "silencio": 30, "agua": 10, "sol": 70, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 60, "juego": 40, "contemplacion": 50, "descanso": 30, "organizacion": 50, "alimentacion": 100, "musica": 30, "risa": 70, "esperanza": 80} }, {"id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition", "porque": "Mente atrapada en un bucle repetitivo. El piloto automático del entorno gris bloquea tu pensamiento. Necesitas buscar inspiración externa para despertar la creatividad.", "porque_en": "Mind trapped in a repetitive loop. Autopilot from gray surroundings blocks your thoughts. Need to seek external inspiration to awaken creativity.", "que_hacer": "Visita una galería o museo local. Camina despacio deteniendo tu marcha frente a una obra específica. Contempla los trazos en absoluto silencio.", "que_hacer_en": "Visit a local gallery or museum. Walk slowly, stopping your pace in front of a specific piece. Contemplate the strokes in absolute silence.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art gallery", "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 70, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 30, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 10, "contemplacion": 95, "descanso": 60, "organizacion": 70, "alimentacion": 0, "musica": 60, "risa": 20, "esperanza": 85} },

            {"id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park", "porque": "Necesitas energía visual. Observa la libertad y el movimiento. Conéctate con el juego.", "porque_en": "Need visual energy. Observe freedom and movement. Connect with play.", "que_hacer": "Acércate a un skate park. Observa a los patinadores. Siente la vitalidad.", "que_hacer_en": "Go to a skate park. Watch skaters. Feel the vitality.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate park", "vector_necesidades": {"movimiento": 70, "naturaleza": 30, "silencio": 20, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 80, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 60, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 70, "risa": 90, "esperanza": 90} }, {"id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore", "porque": "Busca historias and conocimiento. Desconéctate del mundo digital. Nutre tu mente.", "porque_en": "Seek stories and knowledge. Disconnect from digital. Nourish your mind.", "que_hacer": "Explora un local de libros usados. Busca títulos inesperados. Disfruta el aroma.", "que_hacer_en": "Explore a used bookstore. Look for unexpected titles. Enjoy the scent.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used bookstore", "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 85, "agua": 0, "sol": 20, "sombra": 95, "aire_fresco": 40, "creatividad": 90, "comunidad": 30, "aprendizaje": 100, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 70, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 75} }, {"id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema", "porque": "Necesitas un cambio de ambiente y una nueva perspectiva. Disfruta una historia en un entorno diferente.", "porque_en": "Need scene and perspective change. Enjoy a story in a new setting.", "que_hacer": "Asiste a una proyeccion en el exterior. Sumérgete en la película y el ambiente.", "que_hacer_en": "Attend an outdoor screening. Immerse yourself in the film and atmosphere.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor cinema", "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 40, "agua": 10, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "descanso": 70, "organizacion": 20, "alimentacion": 60, "musica": 70, "risa": 70, "esperanza": 85} }, {"id": 221, "titulo": "Auditoría de Frecuencias", "titulo_en": "Frequency Audit", "porque": "Monotonía extrema y falta de estímulos rítmicos o sociales en tu semana.", "porque_en": "Extreme monotony, lack of rhythmic or social stimuli.", "que_hacer": "Visita un club nocturno. Sal al exterior. Siente la música. Nota el aire. Libérate de la inercia mental.", "que_hacer_en": "Visit a nightclub. Step outside. Feel the music. Notice the air. Break free from mental inertia.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Perímetro exterior o zona abierta de un club nocturno.", "donde_en": "Outer perimeter or open area of a nightclub.", "gps": "nightlife district lounge", "vector_necesidades": {"juego": 100, "comunidad": 90, "musica": 90, "risa": 80, "creatividad": 70, "movimiento": 60, "silencio": 10, "descanso": 30} }, {"id": 222, "titulo": "Hackeo Cognitivo", "titulo_en": "Cognitive Hack", "porque": "Falta de inspiración y embotamiento por consuming contenido basura repetitivo.", "porque_en": "Lack of inspiration, dullness from repetitive junk content.", "que_hacer": "Ve al cine o museo local. Entra al vestíbulo. Elige un cartel. Obsérvalo fijamente aislando tu mente del ruido. Usa el espacio como laboratorio de enfoque.", "que_hacer_en": "Head to a local cinema or museum. Enter the lobby. Choose a poster. Stare at it, isolating your mind from noise. Use the space as a focus lab.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Entrada pública de un centro cultural o cine.", "donde_en": "Public entrance of a cultural center or cinema.", "gps": "local cinema or museum", "vector_necesidades": {"creatividad": 100, "aprendizaje": 90, "contemplacion": 95, "juego": 60, "comunidad": 50, "descanso": 60, "silencio": 70} }, {"id": 223, "titulo": "Sabotaje de Rutina", "titulo_en": "Routine Sabotage", "porque": "Falta de variedad sensorial. Salir por un antojo físico rompe la inercia del día de forma inmediata.", "porque_en": "Lack of sensory variety. A physical treat immediately breaks the day's inertia.", "que_hacer": "Ve a un restaurante local. Pide algo. Disfrútalo bocado a bocado sin pantallas. Atiende al sabor y la textura real.", "que_hacer_en": "Head to a local restaurant. Order a treat. Enjoy it bite by byte with no screens. Focus on real taste and texture.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cadena de comida rápida o restaurante del vecindario.", "donde_en": "Fast food chain or neighborhood restaurant.", "gps": "fast food or local restaurant", "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20} },

            {"id": 222, "titulo": "Hackeo Cognitivo", "titulo_en": "Cognitive Hack", "porque": "Falta de inspiración y embotamiento por rumiación masiva. Consumir contenido basura digital bloquea tu capacidad de crear. Requieres un laboratorio de enfoque inmediato.", "porque_en": "Lack of inspiration and dullness from massive rumination. Consuming junk digital content blocks your ability to create. Require an immediate focus lab.", "que_hacer": "Ve al cine o museo local. Entra al vestíbulo. Elige un cartel o pintura. Obsérvalo fijamente aislando tu mente del ruido ambiental.", "que_hacer_en": "Head to a local cinema or museum. Enter the lobby. Choose a poster or painting. Stare at it fixedly, isolating your mind from ambient noise.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Entrada pública de un centro cultural o cine.", "donde_en": "Public entrance of a cultural center or cinema.", "gps": "local cinema or museum", "vector_necesidades": {"creatividad": 100, "aprendizaje": 90, "contemplacion": 95, "juego": 60, "comunidad": 50, "descanso": 60, "silencio": 70} }, {"id": 223, "titulo": "Sabotaje de Rutina", "titulo_en": "Routine Sabotage", "porque": "Falta crónica de variedad sensorial. El piloto automático apaga tus impulsos biológicos. Salir por un antojo físico rompe la inercia del día de forma inmediata.", "porque_en": "Chronic lack of sensory variety. Autopilot turns off your biological impulses. Going out for a physical treat immediately breaks the day's inertia.", "que_hacer": "Ve a un restaurante local. Pide un bocadillo dulce o salado. Disfrútalo bocado a bocado manteniendo tu teléfono guardado. Atiende al sabor real.", "que_hacer_en": "Head to a local restaurant. Order a sweet or savory snack. Enjoy it bite by bite keeping your phone away. Focus on real taste.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cadena de comida rápida o restaurante del vecindario.", "donde_en": "Fast food chain or neighborhood restaurant.", "gps": "fast food or local restaurant", "vector_necesidades": {"alimentacion": 100, "risa": 75, "juego": 70, "comunidad": 80, "movimiento": 30, "descanso": 50, "esperanza": 85, "silencio": 20} } ],

        "cansado": [
            {"id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading", "porque": "Necesitas calma analógica absoluta. Tu atención está drenada por la sobrecarga digital. Requieres aprender sin notificaciones.", "porque_en": "Need absolute analog calm. Your attention is drained by digital overload. Require learning without notifications.", "que_hacer": "Entra a la biblioteca pública local. Camina despacio entre los estantes. Toma un libro al azar y lee diez páginas en completo silencio.", "que_hacer_en": "Enter the local public library. Walk slowly through the shelves. Pick a random book and read ten pages in complete silence.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library", "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70} }, {"id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk", "porque": "Mente asfixiada por la rutina del cemento. Necesitas aire fresco y un horizonte abierto. El agua rompe el bucle de tus pensamientos.", "porque_en": "Mind suffocated by concrete routine. Need fresh air and an open horizon. Water breaks the loop of your thoughts.", "que_hacer": "Camina despacio por el muelle. Observa el movimiento de las embarcaciones. Escucha el sonido constante del oleaje contra las rocas.", "que_hacer_en": "Walk slowly along the pier. Watch the movement of vessels. Listen to the steady sound of waves crashing against rocks.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier", "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90} }, {"id": 328, "titulo": "Inversión Marítima", "titulo_en": "Maritime Inversion", "porque": "Cansancio acumulado de la inercia diaria. Tu cerebro experimenta el ahogo del encierro urbano. La inmensidad marina disuelve la monotonía.", "porque_en": "Accumulated fatigue from daily inertia. Your brain experiences the suffocation of urban confinement. Marine immensity dissolves monotony.", "que_hacer": "Dirígete al paseo costero más cercano. Contempla el desplazamiento de los barcos grandes. Deja que la brisa limpie la pesadez mental.", "que_hacer_en": "Head to the nearest coastal boardwalk. Contemplate the displacement of large ships. Let the breeze clear away your mental heaviness.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Muelle, puerto local o zona costera abierta.", "donde_en": "Dock, local pier, or open coastal zone.", "gps": "cruise terminal or pier", "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60, "esperanza": 85} },

            {"id": 329, "titulo": "Pausa en Ruta", "titulo_en": "Route Break", "porque": "Fatiga muscular severa por el sedentarismo del volante. El asfalto continuo embota tus reflejos cognitivos. Tu cuerpo exige un corte inmediato.", "porque_en": "Severe muscular fatigue from driving sedentarism. Continuous asphalt dulls your cognitive reflexes. Your body demands an immediate break.", "que_hacer": "Estaciona en la próxima área de servicio segura. Apaga el motor y baja del auto. Haz estiramientos suaves respirando el aire libre.", "que_hacer_en": "Park at the next safe service area. Turn off the engine and step out of the car. Do gentle stretches while breathing fresh air.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Área de servicio de autopista o zona de descanso pública.", "donde_en": "Highway service area or public rest zone.", "gps": "highway rest stop or plaza", "vector_necesidades": {"descanso": 95, "movimiento": 60, "aire_fresco": 90, "salud": 85, "silencio": 50, "contemplacion": 70, "organizacion": 40} }, {"id": 330, "titulo": "Recuperación Pasiva", "titulo_en": "Passive Recovery", "porque": "Agotamiento mental por la predictibilidad absoluta de tus días. Te rodea la inercia comercial repetitiva. Exiges un cambio sutil de estímulos.", "porque_en": "Mental exhaustion from the absolute predictability of your days. Repetitive commercial inertia surrounds you. Require a subtle stimuli shift.", "que_hacer": "Visita una plaza histórica o monumento antiguo. Camina a un paso exageradamente lento. Contempla los muros y la arquitectura en calma.", "que_hacer_en": "Visit a historical plaza or old monument. Walk at an deliberately slow pace. Contemplate the walls and architecture calmly.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Centro histórico, plaza pública o calles peatonales.", "donde_en": "Historical center, public plaza, or pedestrian streets.", "gps": "historical landmark or walking tour", "vector_necesidades": {"aprendizaje": 90, "contemplacion": 95, "descanso": 80, "movimiento": 50, "silencio": 70, "creatividad": 60, "esperanza": 80} }, {"id": 331, "titulo": "Aislamiento Sensorial", "titulo_en": "Sensory Isolation", "porque": "Saturación del sistema nervioso por exceso de demandas externas. Demasiada interacción humana agota tu presencia. Requieres un perímetro de penumbra analógica.", "porque_en": "Nervous system saturation from excessive external demands. Too much human interaction drains your presence. Require an analog dim-lit perimeter.", "que_hacer": "Entra a una sala de cine local. Elige una función con poca afluencia. Siéntate en la oscuridad y guarda el teléfono por completo.", "que_hacer_en": "Enter a local movie theater. Choose a low-traffic screening. Sit in the darkness and put your phone completely away.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Sala de cine comercial o vestíbulo de proyecciones.", "donde_en": "Commercial movie theater or screening lobby.", "gps": "local cinema or amc", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 90, "sombra": 100, "juego": 40, "creatividad": 50, "movimiento": 5} },

            {"id": 332, "titulo": "Homeostasis Verde", "titulo_en": "Green Homeostasis", "porque": "Agotamiento crónico por el asfalto. El aire acondicionado de oficina seca tu vitalidad. Necesitas urgentemente un corte y una conexión orgánica real.", "porque_en": "Chronic fatigue from asphalt. Office air conditioning dries up your vitality. You urgently need a break and a real organic connection.", "que_hacer": "Ubica un vivero o jardín botánico. Encuentra un banco protegido por vegetación espesa. Quédate allí inmóvil respirando el aire limpio.", "que_hacer_en": "Locate a nursery or botanical garden. Find a bench sheltered by thick vegetation. Remain there motionless, breathing the clean air.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Jardín botánico público, vivero o parque natural regional.", "donde_en": "Public botanical garden, nursery, or regional nature park.", "gps": "botanical garden or nursery", "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "descanso": 90, "silencio": 80, "contemplacion": 95, "sombra": 90, "salud": 85, "movimiento": 25} }, {"id": 333, "titulo": "Módulo de Quietud", "titulo_en": "Quietness Module", "porque": "Cansancio mental plano y monotonía. El piloto automático apaga tus impulsos. Necesitas observar el movimiento sutil de la naturaleza viva.", "porque_en": "Flat mental fatigue and monotony. Autopilot turns off your impulses. You need to observe the subtle movement of live nature.", "que_hacer": "Busca un parque local con lago o estanque. Siéntate frente a la orilla. Sigue las ondas del agua y las aves con tu mirada en calma.", "que_hacer_en": "Find a local park with a lake or pond. Sit facing the shore. Follow the water ripples and birds with a calm gaze.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Banco de parque junto a un estanque o lago público.", "donde_en": "Park bench next to a public pond or lake.", "gps": "public lake park or fountain", "vector_necesidades": {"agua": 100, "contemplacion": 100, "descanso": 95, "silencio": 75, "naturaleza": 85, "aire_fresco": 90, "movimiento": 15} }, {"id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory", "porque": "Mente atrapada en una prisión mental. El entorno predecible bloquea tu curiosidad. Necesitas maravillarte con el cosmos para ganar perspectiva universal.", "porque_en": "Mind trapped in a mental prison. Predictable surroundings block your curiosity. Need to marvel at the cosmos to gain universal perspective.", "que_hacer": "Visita un centro astronómico o planetario local. Camina por el vestíbulo contemplando las maquetas del espacio en absoluto silencio.", "que_hacer_en": "Visit an astronomical center or local planetarium. Walk through the lobby contemplating space models in absolute silence.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory", "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95} },

            {"id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza", "porque": "Necesitas observar el entorno real. El aislamiento digital apaga tu empatía natural. Conéctate con los flujos de la vida urbana.", "porque_en": "Need to observe real surroundings. Digital isolation dims your natural empathy. Connect with the flows of urban life.", "que_hacer": "Siéntate en un asiento público céntrico. Contempla a las personas pasar sin juzgarlas. Siente el pulso colectivo de tu comunidad.", "que_hacer_en": "Sit on a central public bench. Watch people pass without judgment. Feel the collective pulse of your community.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza", "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85} }, {"id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour", "porque": "Mente agotada de la predictibilidad rutinaria. Necesitas una inyección de conocimiento analógico y movimiento físico suave para despertar tu curiosidad.", "porque_en": "Mind exhausted by routine predictability. Need an injection of analog knowledge and gentle physical movement to awaken your curiosity.", "que_hacer": "Busca un recorrido peatonal local. Avanza a paso firme entre las estructuras antiguas. Descubre las crónicas olvidadas de tu entorno.", "que_hacer_en": "Find a local walking tour. Move steadily among ancient structures. Discover the forgotten chronicles of your surroundings.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour", "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90} }, {"id": 231, "titulo": "Inversión Marítima", "titulo_en": "Maritime Inversion", "porque": "Cansancio monótono por el plano urbano cerrado. Tu mente requiere el estímulo visual de la inmensidad marina para romper el piloto automático.", "porque_en": "Monotonous fatigue from closed urban layouts. Your mind requires the visual stimulus of marine immensity to break the autopilot.", "que_hacer": "Ve al puerto costero o muelle abierto. Observa el desplazamiento de las grandes naves. Deja que el reflejo del agua limpie tus pensamientos.", "que_hacer_en": "Head to the coastal port or open pier. Observe the movement of large vessels. Let the reflection of water clear your thoughts.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Muelle, puerto o zona costera abierta.", "donde_en": "Dock, pier, or open coastal zone.", "gps": "cruise terminal or pier", "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60} },

            {"id": 232, "titulo": "Quiebre de Inercia", "titulo_en": "Inertia Break", "porque": "Cansancio cerebral agudo por exceso de automatismos repetitivos. Te faltan estímulos rítmicos reales que sacudan el estancamiento. Tu atención exige un impacto acústico.", "porque_en": "Acute brain fatigue from excess repetitive automatisms. You lack real rhythmic stimuli to shake the stagnation. Your attention demands an acoustic impact.", "que_hacer": "Visita una zona de ocio nocturno. Quédate en la terraza o área abierta de un club. Escucha la vibración del bajo golpeando el aire para disolver la inercia.", "que_hacer_en": "Visit a nightlife zone. Stay on the terrace or open area of a club. Listen to the bass vibration hitting the air to dissolve inertia.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Perímetro exterior o terraza de un club céntrico.", "donde_en": "Outer perimeter or terrace of a central club.", "gps": "dance club or nightclub", "vector_necesidades": {"musica": 100, "juego": 90, "comunidad": 80, "risa": 70, "movimiento": 60, "silencio": 10, "descanso": 40} } ], "ansioso": [ {"id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water", "porque": "El oleaje y el agua en movimiento apagan la hiperactividad cerebral. Tus pensamientos acelerados necesitan un ritmo continuo y predecible. Busca el fluir natural.", "porque_en": "Waves and moving water turn off cerebral hyperactivity. Your racing thoughts need a continuous and predictable rhythm. Seek the natural flow.", "que_hacer": "Busca una fuente pública o un lago cercano. Siéntate frente a la orilla. Observa el flujo de la corriente sin apartar la mirada por tres minutos.", "que_hacer_en": "Find a public fountain or nearby lake. Sit facing the shore. Observe the stream flow without looking away for three minutes.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake", "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80} }, {"id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride", "porque": "Estrés acumulado que tensa tu sistema nervioso. El plano urbano te asfixia con su rigidez. Necesitas una desconexión total flotando sobre el entorno.", "porque_en": "Accumulated stress tensing your nervous system. The urban layout suffocates you with its rigidity. Need total disconnection by floating over the surroundings.", "que_hacer": "Realiza un viaje corto en una embarcación local. Siente la brisa marina directa. Contempla la inmensidad del paisaje líquido para ganar paz.", "que_hacer_en": "Take a short trip on a local vessel. Feel the direct marine breeze. Contemplate the vastness of the liquid landscape to gain peace.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river", "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90} },

            {"id": 345, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Ansiedad cíclica y rumiación mental masiva. El pánico te paraliza. Necesitas un impacto inmediato de juego y risas para apagar la alerta cerebral.", "porque_en": "Cyclic anxiety and massive mental rumination. Panic paralyzes you. You need an immediate shock of play and laughter to quiet the brain alert.", "que_hacer": "Dirígete al parque de mascotas más cercano. Observa la interacción de los animales sin pensar en tus obligaciones. Conéctate con su diversión inocente.", "que_hacer_en": "Head to the nearest dog park. Observe animal interactions without thinking about your obligations. Connect with their innocent fun.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque de perros local, zona infantil o centro de juegos.", "donde_en": "Local dog park, kids zone, or arcade center.", "gps": "dog park or amusement arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 90, "movimiento": 70, "esperanza": 95, "silencio": 20, "descanso": 50, "creatividad": 40} }, {"id": 346, "titulo": "Aislamiento Conciencial", "titulo_en": "Conscious Isolation", "porque": "Inquietud social aguda y ruido mental constante. La sobrecarga de responsabilidades satura tu sistema nervioso. Requieres un espacio de completo resguardo analógico.", "porque_en": "Acute social uneasiness and constant mental noise. Responsibilities overload saturates your nervous system. Require a space of complete analog shelter.", "que_hacer": "Visita el vestíbulo o jardín de un gran hotel. Siéntate en una de sus butacas públicas. Cierra los ojos sesenta segundos asimilando tu quietud.", "que_hacer_en": "Visit the lobby or garden of a large hotel. Sit in one of its public armchairs. Close your eyes for sixty seconds taking in your stillness.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Zona de descanso, jardín interior o lobby de un hotel de USA.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.", "gps": "boutique hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 95, "contemplacion": 95, "organizacion": 80, "salud": 90, "esperanza": 90, "sombra": 80} }, {"id": 347, "titulo": "Estrategia de Alivio", "titulo_en": "Relief Strategy", "porque": "Sensación de asfixia debido al encierro diario de tu rutina. El automatismo achica tu realidad. Requieres un impacto visual masivo para recordar el mundo exterior.", "porque_en": "Feeling of suffocation from your routine's daily confinement. Automatism shrinks your reality. Require a massive visual impact to remember the outside world.", "que_hacer": "Ve al vestíbulo de una gran central de transportes. Contempla el flujo de los viajeros al partir. Recuerda que tu problema actual es transitorio.", "que_hacer_en": "Head to the lobby of a large transit hub. Contemplate the flow of departing travelers. Remember that your current issue is transient.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Vestíbulo público de aeropuerto o central de transportes regional.", "donde_en": "Public airport lobby or regional transit hub.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 60, "movimiento": 40, "aprendizaje": 50} },

            {"id": 348, "titulo": "Módulo de Silencio Comunitario", "titulo_en": "Community Silence Module", "porque": "Aislamiento mental nocivo y parálisis por ansiedad intensa. Tu mente rumia en soledad. Necesitas estar rodeado de flujos humanos tranquilos.", "porque_en": "Harmful mental isolation and intense anxiety paralysis. Your mind ruminates in solitude. You need to be surrounded by calm human flows.", "que_hacer": "Dirígete a una cafetería tranquila. Pide una bebida tibia o agua. Siéntate en un rincón apartado sin revisar redes sociales y observa el entorno.", "que_hacer_en": "Head to a quiet coffee shop. Order a warm drink or water. Sit in a distant corner without checking social media and observe the environment.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Cafetería o establecimiento de bebidas local en tu Código Postal.", "donde_en": "Local coffee shop or beverage venue in your Zip Code.", "gps": "quiet cafe or bakery", "vector_necesidades": {"comunidad": 90, "descanso": 85, "silencio": 75, "alimentacion": 60, "contemplacion": 80, "esperanza": 85, "musica": 30} }, {"id": 123, "titulo": "Jardín de Rocas Zen", "titulo_en": "Rock Zen Garden", "porque": "Mente agitada por la velocidad del día. Experimentas caos interno. Requieres un espacio de orden y armonía absoluta para centrar tus pensamientos.", "porque_en": "Mind agitated by the day's speed. You experience internal chaos. Require a space of absolute order and harmony to center your thoughts.", "que_hacer": "Encuentra un parque de piedras o jardín japonés. Observa la disposición fija de las formas. Medita en su quietud analógica inmutable.", "que_hacer_en": "Find a stone park or Japanese garden. Observe the fixed arrangement of shapes. Meditate in its immutable analog stillness.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden", "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90} }, {"id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park", "porque": "Ansiedad cíclica y rigidez emocional. El piloto automático bloquea tu alegría instintiva. Necesitas observar el juego inocente de los animales.", "porque_en": "Cyclic anxiety and emotional rigidity. Autopilot blocks your instinctive joy. You need to observe the innocent play of animals.", "que_hacer": "Visita un recinto canino público. Siente la diversión espontánea de los cachorros. Contágiate de su energía positiva libre de preocupaciones.", "que_hacer_en": "Visit a public canine enclosure. Feel the spontaneous fun of the pups. Catch their worry-free positive energy.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park", "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90} },

            {"id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music", "porque": "Mente saturada por el ruido de la rutina. Experimentas fatiga auditiva y tensión acumulada. Requieres una inyección de arte armónico para restaurar tu paz.", "porque_en": "Mind saturated by routine noise. Experiencing auditory fatigue and built-up tension. Require an injection of harmonic art to restore your peace.", "que_hacer": "Busca un local con melodías acústicas o jazz sutil. Cierra los ojos. Sigue el compás de los instrumentos aislando cualquier preocupación.", "que_hacer_en": "Find a venue with acoustic melodies or subtle jazz. Close your eyes. Follow the beat of instruments, isolating any worry.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar", "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85} }, {"id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool", "porque": "Cuerpo rígido y mente acelerada por la prisa. La inercia del concreto estanca tus músculos. El contacto líquido reinicia tu balance biológico de inmediato.", "porque_en": "Stiff body and racing mind from rushing. Concrete inertia stagnates your muscles. Liquid contact restarts your biological balance immediately.", "que_hacer": "Visita una alberca municipal o comunitaria. Date un chapuzón sin prisas. Quédate flotando de espaldas para liberar el peso de la gravedad.", "que_hacer_en": "Visit a municipal or community pool. Take an unhurried dip. Stay floating on your back to release the weight of gravity.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool", "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85} }, {"id": 241, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Ansiedad cíclica y rumiación mental masiva. El pánico bloquea tu discernimiento lógico. Requieres un impacto visual festivo de colores y estímulos lúdicos infantiles.", "porque_en": "Cyclic anxiety and massive mental rumination. Panic blocks your logical discernment. Require a festive visual impact of colors and playful childhood stimuli.", "que_hacer": "Ve a un centro de juegos o parque recreativo. Observa la dinámica de movimiento del lugar. Conéctate con la diversión espontánea para romper el bucle.", "que_hacer_en": "Head to an arcade or recreation park. Observe the movement dynamic of the venue. Connect with spontaneous fun to break the loop.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.", "gps": "amusement park or arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50} },

            {"id": 242, "titulo": "Estrategia de Alivio", "titulo_en": "Relief Strategy", "porque": "Sensación de asfixia debido al encierro de la rutina laboral.", "porque_en": "Feeling of suffocation due to work routine confinement.", "que_hacer": "Si estás cerca de una central de transportes, camina por el pasillo principal. Despega la mirada de la pantalla. Observa a los viajeros partir. Asimila que la Tierra es inmensa y tu problema transitorio.", "que_hacer_en": "If near a transit hub, walk through the main hall. Take your eyes off the screen. Watch travelers depart. Realize the Earth is huge and your issue is transient.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30} }, {"id": 243, "titulo": "Aislamiento Conciencial", "titulo_en": "Conscious Isolation", "porque": "Inquietud social aguda y ruido mental por sobrecarga de responsabilidades.", "porque_en": "Acute social uneasiness and mental noise from responsibilities overload.", "que_hacer": "Visita la sala común de un hospedaje local de forma gratuita. Siéntate en una butaca cómoda. Cierra los ojos. Respira a un ritmo lento. Habita tu cuerpo con presencia absoluta.", "que_hacer_en": "Visit the common room of a local lodging for free. Sit in a comfortable armchair. Close your eyes. Breathe at a slow pace. Inhabit your body with absolute presence.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Zona de descanso o jardín de un hotel de USA.", "donde_en": "Lounge or garden of a USA hotel.", "gps": "boutique hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 95, "organizacion": 80, "salud": 85, "esperanza": 85} }, {"id": 244, "titulo": "Soberanía de Cabina", "titulo_en": "Cabin Sovereignty", "porque": "Pánico y desconexión corporal debido a la saturación ruidosa de los perímetros urbanos.", "porque_en": "Panic and bodily disconnection due to noisy urban perimeter saturation.", "que_hacer": "Ve a la terminal de vuelos. Busca un ventanal amplio con vista al cielo. Vacía el aire de tus pulmones tres veces profundamente. Siéntete libre.", "que_hacer_en": "Head to the flight terminal. Find a wide sky-view window. Empty the air from your lungs deeply three times. Feel free.", "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN, "donde": "Terminal de aeropuerto, central de tránsito o zona de observación abierta.", "donde_en": "Airport terminal, transit hub, or open observation zone.", "gps": "airport terminal or transit hub", "vector_necesidades": {"aire_fresco": 95, "contemplacion": 100, "esperanza": 90, "descanso": 70, "silencio": 60, "movimiento": 30} } ] } }


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

# ==========================================================================================
# INYECCIÓN OPERATIVA: CONTROLADORES DE COMPRA Y ACCESO ADMINISTRATIVO CON REQUEST SEGURO
# ==========================================================================================
@app.post("/crear-checkout")
async def crear_checkout(request: Request):
    try:
        data = await request.json()
        tipo_plan = data.get("tipo_plan")
        user_id = data.get("user_id", "cliente_otg")
        if tipo_plan not in PLANES_STRIPE:
            raise HTTPException(status_code=400, detail="Plan inválido")
       
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PLANES_STRIPE[tipo_plan], "quantity": 1}],
            mode="subscription" if tipo_plan != "unico" else "payment",
            success_url="https://onrender.com",
            cancel_url="https://onrender.com",
            client_reference_id=user_id
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/login-admin")
async def login_admin(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        if username == ADMIN_USER and password == ADMIN_PASS:
            return {"status": "success", "role": "admin", "user_id": "admin_master"}
        return JSONResponse(status_code=401, content={"error": "Credenciales incorrectas"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "Payload malformado"})

@app.post("/webhook-stripe")
async def webhook_stripe(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Pago exitoso para usuario: {session.get('client_reference_id')}")
    return {"status": "success"}
# ==========================================================================================

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
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
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

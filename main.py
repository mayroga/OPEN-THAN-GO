# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.1
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 2 (Backend Core)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random
import re
from datetime import datetime
import urllib.parse

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
MAX_HISTORY_ORACULO = 12
EXPLORATION_RATE = 0.20
HISTORY_PENALTY_BASE = 40
DECAY_PER_DAY = 0.985

def limitar_historial(historial, limite):
    if historial is None:
        return []
    return historial[-limite:]

def penalizacion_historial(mision_id, historial):
    if not historial:
        return 0
    historial = list(reversed(historial))
    for posicion, antiguo in enumerate(historial):
        if antiguo == mision_id:
            if posicion == 0:
                return HISTORY_PENALTY_BASE
            elif posicion == 1:
                return HISTORY_PENALTY_BASE * 0.85
            elif posicion == 2:
                return HISTORY_PENALTY_BASE * 0.70
            elif posicion <= (len(historial) - 1):
                return HISTORY_PENALTY_BASE * 0.30
    return 0

def bonus_exploracion(mision_id, historial):
    if not historial:
        return 20
    if mision_id not in historial:
        return 15
    return 0

def actualizar_historial(historial, nuevo_id, limite):
    # This function is not used in the backend for SALIR mode anymore,
    # as SALIR history update is now handled on the frontend client-side
    # once a mission is *selected* and its external link is opened.
    # It is still used for CASA mode.
    historial = historial or []
    if nuevo_id in historial:
        historial.remove(nuevo_id)
    historial.append(nuevo_id)
    return historial[-limite:]

def diversidad_vector(vector1, vector2):
    distancia = 0
    needs_to_consider = [k for k in DEFAULT_NECESSITY_VECTOR.keys() if k != "indicador_ansiedad"]
    for k in needs_to_consider:
        distancia += abs(
            vector1.get(k, 50) -
            vector2.get(k, 50)
        )
    return distancia

def decay_profile(profile, dias):
    return profile

WHEN_ES = "Ahora mismo. Levántate de la silla ya."
WHEN_EN = "Right now. Get out of your chair immediately."
FOR_WHAT_ES = "Para romper el zombi urbano y recordar que la vida es más que pagar cuentas."
FOR_WHAT_EN = "To break the urban zombie and remember that life is more than paying bills."

# ============================================================
# CATÁLOGO DE MISIONES CWRE V2.1
# Adaptado para Microacciones de Recuperación Mental y sin elementos de estrés laboral/financiero.
# ============================================================
BASE_MISIONES = {
    "CASA_ES": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}, "nivel_profundidad": 1},
        {"id": 2, "titulo": "Desconexión total", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}, "nivel_profundidad": 1},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}, "nivel_profundidad": 1},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Siente tus hombros libres. Ya no tienes esa mochila de peso invisible.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}, "nivel_profundidad": 1},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}, "nivel_profundidad": 1},
        {"id": 7, "titulo": "El aire de la ventana", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}, "nivel_profundidad": 1},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}, "nivel_profundidad": 1},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}, "nivel_profundidad": 1},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}, "nivel_profundidad": 1},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}, "nivel_profundidad": 1},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la ventana. Deja que el aire ruede. Huele el cambio.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}, "nivel_profundidad": 1},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}, "nivel_profundidad": 1},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}, "nivel_profundidad": 1},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}, "nivel_profundidad": 1},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}, "nivel_profundidad": 1},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}, "nivel_profundidad": 1},
        {"id": 22, "titulo": "Relaxa ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}, "nivel_profundidad": 1},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}, "nivel_profundidad": 1},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}, "nivel_profundidad": 1},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}, "nivel_profundidad": 1},
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la boca, mueve mandíbula a los lados.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}, "nivel_profundidad": 1},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}, "nivel_profundidad": 1},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}, "nivel_profundidad": 1},
        {"id": 32, "titulo": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}, "nivel_profundidad": 1},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}, "nivel_profundidad": 1},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}, "nivel_profundidad": 1},
        {"id": 35, "titulo": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}, "nivel_profundidad": 1},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}, "nivel_profundidad": 1},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}, "nivel_profundidad": 1},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}, "nivel_profundidad": 1},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}, "nivel_profundidad": 1},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}, "nivel_profundidad": 1},
        {"id": 42, "titulo": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}, "nivel_profundidad": 1},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}, "nivel_profundidad": 1},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}, "nivel_profundidad": 1},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}, "nivel_profundidad": 1},
        {"id": 46, "titulo": "Siente base", "descripcion": "Contacto firme de piernas con silla.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}, "nivel_profundidad": 1},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}, "nivel_profundidad": 1},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}, "nivel_profundidad": 1},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}, "nivel_profundidad": 1},
        {"id": 51, "titulo": "Canta una melodía", "descripcion": "Tararea tu canción favorita suavemente. No pienses, solo siente el sonido.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}, "nivel_profundidad": 1},
        {"id": 52, "titulo": "Escribe 3 deseos", "descripcion": "En un papel, anota tres deseos simples que te gustaría cumplir hoy.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 53, "titulo": "Paseo por el pasillo", "descripcion": "Camina lentamente por el pasillo de tu casa, sintiendo cada paso.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}, "nivel_profundidad": 1},
        {"id": 54, "titulo": "Mira una planta", "descripcion": "Si tienes una planta en casa, obsérvala con atención durante un minuto.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}, "nivel_profundidad": 1},
        {"id": 55, "titulo": "Dibuja un círculo", "descripcion": "Toma un lápiz y papel. Dibuja círculos perfectos sin pensar en nada más.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}, "nivel_profundidad": 1},
        {"id": 57, "titulo": "Abre un libro al azar", "descripcion": "Toma un libro, ábrelo en una página aleatoria y lee la primera frase.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}, "nivel_profundidad": 1},
        {"id": 58, "titulo": "Escucha la lluvia", "descripcion": "Si llueve, abre la ventana y escucha el sonido de las gotas caer.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}, "nivel_profundidad": 1},
        {"id": 59, "titulo": "Baila sin música", "descripcion": "Mueve tu cuerpo libremente por un minuto, como si nadie te viera.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}, "nivel_profundidad": 1},
        {"id": 60, "titulo": "Bebe una infusión", "descripcion": "Prepara una infusión caliente y bébela lentamente, sintiendo el calor.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 61, "titulo": "Mira tus manos", "descripcion": "Observa las líneas y detalles de tus manos. Son herramientas poderosas.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}, "nivel_profundidad": 1},
        {"id": 62, "titulo": "Imagina un paisaje", "descripcion": "Cierra los ojos e imagina tu paisaje natural favorito por 30 segundos.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}, "nivel_profundidad": 1},
        {"id": 63, "titulo": "Estira la espalda", "descripcion": "Siéntate en el suelo con las piernas estiradas y trata de tocar tus pies.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 64, "titulo": "Respira por la nariz", "descripcion": "Haz 5 respiraciones profundas, solo por la nariz, notando el aire.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}, "nivel_profundidad": 1},
        {"id": 65, "titulo": "Juego de sombras", "descripcion": "Con las manos, crea una forma en la pared con la luz de una lámpara.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}, "nivel_profundidad": 1},
        {"id": 66, "titulo": "Un abrazo imaginario", "descripcion": "Abraza tus brazos fuertemente, imaginando que es un ser querido.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 67, "titulo": "Encuentra un objeto azul", "descripcion": "Busca rápidamente 5 objetos azules en tu entorno. Enfoca tu vista.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 69, "titulo": "Observa el cielo", "descripcion": "Abre la ventana o sal al balcón. Observa el cielo por un minuto.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 70, "titulo": "Masaje facial", "descripcion": "Con las yemas de los dedos, masajea suavemente tu frente y mejillas.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 71, "titulo": "Cierra los ojos y escucha", "descripcion": "Siéntate cómodo, cierra los ojos y solo escucha los sonidos de tu casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}, "nivel_profundidad": 1},
        {"id": 72, "titulo": "Tensa y relaja los pies", "descripcion": "Aprieta los dedos de tus pies durante 5 segundos y luego relájalos.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 74, "titulo": "Olor consciente", "descripcion": "Huelea una flor, café o especia. Concéntrate en el aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 75, "titulo": "Cambia de silla", "descripcion": "Siéntate en otra silla o lugar de la casa por 5 minutos. Pequeño cambio.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}, "nivel_profundidad": 1},
        # NUEVAS MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160)
        {"id": 151, "titulo": "EL RETO DE LA SUSCRIPCIÓN OLVIDADA", "descripcion": "Abre tu correo o tu aplicación bancaria. Busca 'Subscription', 'Invoice' o 'Payment' y cancela una sola suscripción que ya no utilices. Recuperar el control también es ahorrar.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60}, "nivel_profundidad": 1},
        {"id": 152, "titulo": "EL RETO DE LOS TRES GASTOS", "descripcion": "Abre una nota en tu teléfono y escribe únicamente los tres gastos inevitables de esta semana. No pienses en todo el mes. Solo en esta semana.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80}, "nivel_profundidad": 1},
        {"id": 153, "titulo": "EL RETO DEL ORDEN DIGITAL", "descripcion": "Borra veinte capturas de pantalla, archivos o documentos que ya no necesites. El orden digital también reduce la carga mental.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 154, "titulo": "EL RETO DEL SILENCIO", "descripcion": "Silencia durante una hora las aplicaciones que más ansiedad te generan. Tu atención también necesita descansar.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80}, "nivel_profundidad": 1},
        {"id": 155, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Escribe tres cosas que hoy tienes y que hace algunos años deseabas. Tu mente necesita recordar que también has avanzado.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60}, "nivel_profundidad": 1},
        {"id": 156, "titulo": "EL RETO DEL AGUA", "descripcion": "Levántate despacio, bebe un vaso completo de agua y vuelve respirando con calma.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "salud": 85, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 157, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre una ventana durante dos minutos y observa el cielo sin mirar el teléfono.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70}, "nivel_profundidad": 1},
        {"id": 158, "titulo": "EL RETO DEL ORDEN", "descripcion": "Guarda únicamente cinco objetos que estén fuera de lugar. Cinco son suficientes por hoy.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 159, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Realiza cinco respiraciones profundas siguiendo un ritmo lento. No tienes que hacer nada más.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}, "nivel_profundidad": 1},
        {"id": 160, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "Durante dos minutos mira un punto lejano para permitir que tus ojos descansen de la pantalla.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}, "nivel_profundidad": 1},
        # NUEVAS MICROACCIONES DE PROFUNDIDAD (NIVEL 2)
        {"id": 161, "titulo": "DIARIO DE PENSAMIENTOS", "descripcion": "En una hoja, anota 3 pensamientos recurrentes que te agobian. No los juzgues, solo obsérvalos.", "vector_necesidades": {"contemplacion": 100, "organizacion": 90, "aprendizaje": 80, "silencio": 85, "descanso": 70, "esperanza": 75}, "nivel_profundidad": 2},
        {"id": 162, "titulo": "IMAGINA TU LUGAR SEGURO", "descripcion": "Cierra los ojos y visualiza con detalle un lugar donde te sientes absolutamente seguro y en paz. Quédate ahí por un minuto.", "vector_necesidades": {"creatividad": 95, "contemplacion": 100, "silencio": 90, "descanso": 95, "esperanza": 90}, "nivel_profundidad": 2},
        {"id": 163, "titulo": "ESCULTURA DE MANOS", "descripcion": "Usa tus manos para moldear un objeto imaginario de tus preocupaciones. Luego, deshazlo lentamente. Siente el control.", "vector_necesidades": {"creatividad": 100, "movimiento": 80, "juego": 70, "contemplacion": 80, "risa": 50}, "nivel_profundidad": 2},
        {"id": 164, "titulo": "RECUENTO DE LOS SENTIDOS", "descripcion": "Nombra 5 cosas que puedes ver, 4 que puedes sentir, 3 que puedes oír, 2 que puedes oler y 1 que puedes saborear. Anclaje total.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "aprendizaje": 85, "organizacion": 95, "descanso": 80}, "nivel_profundidad": 2},
        {"id": 165, "titulo": "LA CARTA SIN ENVIAR", "descripcion": "Escribe una carta a una persona o situación que te cause estrés. No la envíes, solo escribe todo lo que sientes y luego deséchala.", "vector_necesidades": {"creatividad": 90, "organizacion": 85, "descanso": 80, "esperanza": 70, "contemplacion": 60}, "nivel_profundidad": 2},
        # MÁS MICROACCIONES DE NIVEL 1 PARA VARIAR
        {"id": 166, "titulo": "Cambia el tono de voz", "descripcion": "Habla contigo mismo en un tono suave y calmado durante un minuto. Sé tu propio refugio.", "vector_necesidades": {"silencio": 80, "contemplacion": 70, "descanso": 80, "esperanza": 90, "risa": 60}, "nivel_profundidad": 1},
        {"id": 167, "titulo": "Mira el reloj en silencio", "descripcion": "Observa el segundero de un reloj por un minuto sin pensar en el tiempo que pasa. Solo el movimiento.", "vector_necesidades": {"contemplacion": 90, "silencio": 100, "organizacion": 70, "aprendizaje": 60, "descanso": 80}, "nivel_profundidad": 1},
        {"id": 168, "titulo": "Tensa y relaja el cuerpo", "descripcion": "Tensa todos tus músculos por 5 segundos y luego suelta. Repite 3 veces. Libera tensiones.", "vector_necesidades": {"movimiento": 90, "descanso": 95, "salud": 85, "silencio": 70, "organizacion": 50}, "nivel_profundidad": 1},
        {"id": 169, "titulo": "Ondas sonoras de un vaso", "descripcion": "Llena un vaso con agua, golpea suavemente y observa las ondas. Pequeños detalles, gran calma.", "vector_necesidades": {"agua": 90, "silencio": 80, "contemplacion": 95, "creatividad": 70, "aprendizaje": 60}, "nivel_profundidad": 1},
        {"id": 170, "titulo": "El sonido de la página", "descripcion": "Pasa una página de un libro. Escucha el sonido. Siente la textura. Vuelve al presente.", "vector_necesidades": {"aprendizaje": 80, "silencio": 90, "contemplacion": 85, "descanso": 70, "creatividad": 60}, "nivel_profundidad": 1},
    ],
    "CASA_EN": [
        {"id": 1, "titulo": "Cut the autopilot", "descripcion": "Scan your body. Pinpoint the exact weight on your back. See it. You are alive.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}, "nivel_profundidad": 1},
        {"id": 2, "titulo": "Total Disconnection", "descripcion": "Feel your chair. The floor supports your weight for free. Let yourself fall.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}, "nivel_profundidad": 1},
        {"id": 3, "titulo": "Screen Isolation", "descripcion": "Flip your phone. Look at a corner of the ceiling for 30 seconds. Break the loop.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}, "nivel_profundidad": 1},
        {"id": 4, "titulo": "Release the Burden", "descripcion": "Feel your shoulders free. That invisible backpack of weight is gone.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}, "nivel_profundidad": 1},
        {"id": 5, "titulo": "The Water Reset", "descripcion": "A small sip of cold water. Feel the liquid. It's life entering.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}, "nivel_profundidad": 1},
        {"id": 7, "titulo": "Street Air", "descripcion": "Open the window. Let the air hit your face. Feel the outside.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}, "nivel_profundidad": 1},
        {"id": 8, "titulo": "Energy Rotation", "descripcion": "Rotate wrists and ankles. Your body is yours. You govern this engine.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}, "nivel_profundidad": 1},
        {"id": 9, "titulo": "Present Anchor", "descripcion": "Close your eyes. Say one good thing you have today. Say it loud.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}, "nivel_profundidad": 1},
        {"id": 11, "titulo": "Feet on the Ground", "descripcion": "Take off your shoes. Rest soles on the floor. Feel the cold. Connect.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 12, "titulo": "Sky Stretch", "descripcion": "Arm up. Touch the ceiling. Maintain tension. Release suddenly.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}, "nivel_profundidad": 1},
        {"id": 14, "titulo": "Straight Spine", "descripcion": "Straighten your back. An invisible thread pulls your head. Breathe.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 15, "titulo": "Cold Contact", "descripcion": "Touch a cold surface. Feel the real temperature. Ground yourself.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}, "nivel_profundidad": 1},
        {"id": 16, "titulo": "Total Ventilation", "descripcion": "Open the front door. Let the air flow. Smell the change.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}, "nivel_profundidad": 1},
        {"id": 17, "titulo": "Stress Shake-off", "descripcion": "Stand up and shake hands and legs as if shaking off water. Do it for 10 seconds.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}, "nivel_profundidad": 1},
        {"id": 18, "titulo": "Distant Gaze", "descripcion": "Look at the farthest object outside your window. Rest your focus.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}, "nivel_profundidad": 1},
        {"id": 19, "titulo": "Happy Memory", "descripcion": "Close your eyes and recall a real moment of calm from your childhood.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}, "nivel_profundidad": 1},
        {"id": 20, "titulo": "Forced Smile", "descripcion": "Smile for 15 seconds. Change your brain chemistry now.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}, "nivel_profundidad": 1},
        {"id": 21, "titulo": "Gratitude", "descripcion": "Close your eyes. Be thankful for one good thing this week.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}, "nivel_profundidad": 1},
        {"id": 22, "titulo": "Relax Eyes", "descripcion": "Cover your eyes with warm palms. One minute of darkness.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}, "nivel_profundidad": 1},
        {"id": 23, "titulo": "Heart Rate", "descripcion": "Right hand on chest. Feel the heartbeat. It's your engine.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}, "nivel_profundidad": 1},
        {"id": 24, "titulo": "Release Neck", "descripcion": "Slow head circles. Release screen tension.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}, "nivel_profundidad": 1},
        {"id": 25, "titulo": "Palm Exercise", "descripcion": "Rub hands until warm. Place them on shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}, "nivel_profundidad": 1},
        {"id": 26, "titulo": "Distant Sounds", "descripcion": "Identify the farthest sound outside your home.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 27, "titulo": "Side Stretch", "descripcion": "Gently lean your body to each side.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 28, "titulo": "The Empty Glass", "descripcion": "Look at a glass. Focus on its shape for one minute.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 29, "titulo": "Release Jaw", "descripcion": "Open your mouth wide, move your jaw side to side.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}, "nivel_profundidad": 1},
        {"id": 30, "titulo": "Slow Steps", "descripcion": "Ten slow, conscious steps in your room.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}, "nivel_profundidad": 1},
        {"id": 31, "titulo": "Gentle Massage", "descripcion": "Fingertips on temples. Very slow circles.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}, "nivel_profundidad": 1},
        {"id": 32, "titulo": "Air Awareness", "descripcion": "Feel the cold air enter, the warm air leave.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}, "nivel_profundidad": 1},
        {"id": 33, "titulo": "Firm Back", "descripcion": "Shoulder blades back, open your chest.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}, "nivel_profundidad": 1},
        {"id": 34, "titulo": "Total Support", "descripcion": "Feel the chair supporting your full weight.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}, "nivel_profundidad": 1},
        {"id": 35, "titulo": "Countdown", "descripcion": "From 20 to 1. Slowly. Calm the noise.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 36, "titulo": "Touch Texture", "descripcion": "Run fingers over a real texture. Wood or fabric.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}, "nivel_profundidad": 1},
        {"id": 37, "titulo": "Stretch Fingers", "descripcion": "Spread fingers as wide as possible for 5 seconds. Release.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}, "nivel_profundidad": 1},
        {"id": 38, "titulo": "Internal Sound", "descripcion": "Listen to your breath. Don't force it.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}, "nivel_profundidad": 1},
        {"id": 39, "titulo": "Fixed Gaze", "descripcion": "Small spot on the wall. Fixed. Without blinking.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}, "nivel_profundidad": 1},
        {"id": 40, "titulo": "Release Arms", "descripcion": "Hang arms. Shake them gently.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}, "nivel_profundidad": 1},
        {"id": 41, "titulo": "Clothes Contact", "descripcion": "Notice the weight of clothes on your skin.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}, "nivel_profundidad": 1},
        {"id": 42, "titulo": "Deep Air", "descripcion": "Inflate belly, hold 3 seconds, release slowly.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}, "nivel_profundidad": 1},
        {"id": 43, "titulo": "Shoulder Rotation", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}, "nivel_profundidad": 1},
        {"id": 44, "titulo": "Listen to Silence", "descripcion": "Search for silence between breaths.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}, "nivel_profundidad": 1},
        {"id": 45, "titulo": "Ceiling Gaze", "descripcion": "Look at the ceiling. Stretch neck without moving shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}, "nivel_profundidad": 1},
        {"id": 46, "titulo": "Feel Base", "descripcion": "Firm contact of legs with chair.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}, "nivel_profundidad": 1},
        {"id": 48, "titulo": "Mental Cleanse", "descripcion": "Exhale boring worry. Out of you.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}, "nivel_profundidad": 1},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}, "nivel_profundidad": 1},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}, "nivel_profundidad": 1},
        {"id": 51, "titulo": "Canta una melodía", "descripcion": "Tararea tu canción favorita suavemente. No pienses, solo siente el sonido.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}, "nivel_profundidad": 1},
        {"id": 52, "titulo": "Escribe 3 deseos", "descripcion": "En un papel, anota tres deseos simples que te gustaría cumplir hoy.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 53, "titulo": "Paseo por el pasillo", "descripcion": "Camina lentamente por el pasillo de tu casa, sintiendo cada paso.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}, "nivel_profundidad": 1},
        {"id": 54, "titulo": "Mira una planta", "descripcion": "Si tienes una planta en casa, obsérvala con atención durante un minuto.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}, "nivel_profundidad": 1},
        {"id": 55, "titulo": "Dibuja un círculo", "descripcion": "Toma un lápiz y papel. Dibuja círculos perfectos sin pensar en nada más.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}, "nivel_profundidad": 1},
        {"id": 57, "titulo": "Abre un libro al azar", "descripcion": "Toma un libro, ábrelo en una página aleatoria y lee la primera frase.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}, "nivel_profundidad": 1},
        {"id": 58, "titulo": "Escucha la lluvia", "descripcion": "Si llueve, abre la ventana y escucha el sonido de las gotas caer.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}, "nivel_profundidad": 1},
        {"id": 59, "titulo": "Baila sin música", "descripcion": "Mueve tu cuerpo libremente por un minuto, como si nadie te viera.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}, "nivel_profundidad": 1},
        {"id": 60, "titulo": "Bebe una infusión", "descripcion": "Prepara una infusión caliente y bébela lentamente, sintiendo el calor.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 61, "titulo": "Mira tus manos", "descripcion": "Observa las líneas y detalles de tus manos. Son herramientas poderosas.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}, "nivel_profundidad": 1},
        {"id": 62, "titulo": "Imagina un paisaje", "descripcion": "Cierra los ojos e imagina tu paisaje natural favorito por 30 segundos.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}, "nivel_profundidad": 1},
        {"id": 63, "titulo": "Estira la espalda", "descripcion": "Siéntate en el suelo con las piernas estiradas y trata de tocar tus pies.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 64, "titulo": "Respira por la nariz", "descripcion": "Haz 5 respiraciones profundas, solo por la nariz, notando el aire.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}, "nivel_profundidad": 1},
        {"id": 65, "titulo": "Juego de sombras", "descripcion": "Con las manos, crea una forma en la pared con la luz de una lámpara.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}, "nivel_profundidad": 1},
        {"id": 66, "titulo": "Un abrazo imaginario", "descripcion": "Abraza tus brazos fuertemente, imaginando que es un ser querido.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 67, "titulo": "Encuentra un objeto azul", "descripcion": "Busca rápidamente 5 objetos azules en tu entorno. Enfoca tu vista.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 69, "titulo": "Observa el cielo", "descripcion": "Abre la ventana o sal al balcón. Observa el cielo por un minuto.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 70, "titulo": "Masaje facial", "descripcion": "Con las yemas de los dedos, masajea suavemente tu frente y mejillas.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 71, "titulo": "Cierra los ojos y escucha", "descripcion": "Siéntate cómodo, cierra los ojos y solo escucha los sonidos de tu casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}, "nivel_profundidad": 1},
        {"id": 72, "titulo": "Tensa y relaja los pies", "descripcion": "Aprieta los dedos de tus pies durante 5 segundos y luego relájalos.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 74, "titulo": "Olor consciente", "descripcion": "Huelea una flor, café o especia. Concéntrate en el aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}, "nivel_profundidad": 1},
        {"id": 75, "titulo": "Cambia de silla", "descripcion": "Siéntate en otra silla o lugar de la casa por 5 minutos. Pequeño cambio.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}, "nivel_profundidad": 1},
        # NUEVAS MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160)
        {"id": 151, "titulo": "THE FORGOTTEN SUBSCRIPTION CHALLENGE", "descripcion": "Open your email or banking app. Search for 'Subscription', 'Invoice', or 'Payment' and cancel a single subscription you no longer use. Regaining control is also saving.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60}, "nivel_profundidad": 1},
        {"id": 152, "titulo": "THE THREE EXPENSES CHALLENGE", "descripcion": "Open a note on your phone and write down only the three unavoidable expenses for this week. Don't think about the whole month. Just this week.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80}, "nivel_profundidad": 1},
        {"id": 153, "titulo": "THE DIGITAL ORDER CHALLENGE", "descripcion": "Delete twenty screenshots, files, or documents you no longer need. Digital order also reduces mental load.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70}, "nivel_profundidad": 1},
        {"id": 154, "titulo": "THE SILENCE CHALLENGE", "descripcion": "Silence the apps that generate the most anxiety for an hour. Your attention also needs rest.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80}, "nivel_profundidad": 1},
        {"id": 155, "titulo": "THE GRATITUDE CHALLENGE", "descripcion": "Write down three things you have today that you wished for a few years ago. Your mind needs to remember that you have also made progress.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60}, "nivel_profundidad": 1},
        {"id": 156, "titulo": "THE WATER CHALLENGE", "descripcion": "Slowly stand up, drink a full glass of water, and return, breathing calmly.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "salud": 85, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 157, "titulo": "THE WINDOW CHALLENGE", "descripcion": "Open a window for two minutes and observe the sky without looking at your phone.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70}, "nivel_profundidad": 1},
        {"id": 158, "titulo": "THE ORDER CHALLENGE", "descripcion": "Put away only five objects that are out of place. Five are enough for today.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50}, "nivel_profundidad": 1},
        {"id": 159, "titulo": "THE BREATHING CHALLENGE", "descripcion": "Take five deep breaths following a slow rhythm. You don't have to do anything else.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}, "nivel_profundidad": 1},
        {"id": 160, "titulo": "THE VISUAL REST CHALLENGE", "descripcion": "For two minutes, look at a distant point to allow your eyes to rest from the screen.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}, "nivel_profundidad": 1},
        # NUEVAS MICROACCIONES DE PROFUNDIDAD (NIVEL 2)
        {"id": 161, "titulo": "THOUGHT JOURNALING", "descripcion": "On a paper, write down 3 recurring thoughts that bother you. Don't judge them, just observe them.", "vector_necesidades": {"contemplacion": 100, "organizacion": 90, "aprendizaje": 80, "silencio": 85, "descanso": 70, "esperanza": 75}, "nivel_profundidad": 2},
        {"id": 162, "titulo": "IMAGINE YOUR SAFE PLACE", "descripcion": "Close your eyes and vividly visualize a place where you feel absolutely safe and peaceful. Stay there for a minute.", "vector_necesidades": {"creatividad": 95, "contemplacion": 100, "silencio": 90, "descanso": 95, "esperanza": 90}, "nivel_profundidad": 2},
        {"id": 163, "titulo": "HAND SCULPTURE", "descripcion": "Use your hands to sculpt an imaginary object of your worries. Then, slowly undo it. Feel the control.", "vector_necesidades": {"creatividad": 100, "movimiento": 80, "juego": 70, "contemplacion": 80, "risa": 50}, "nivel_profundidad": 2},
        {"id": 164, "titulo": "SENSES RECOUNT", "descripcion": "Name 5 things you can see, 4 you can feel, 3 you can hear, 2 you can smell, and 1 you can taste. Total anchoring.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "aprendizaje": 85, "organizacion": 95, "descanso": 80}, "nivel_profundidad": 2},
        {"id": 165, "titulo": "THE UNSENT LETTER", "descripcion": "Write a letter to a person or situation causing you stress. Don't send it, just write everything you feel and then discard it.", "vector_necesidades": {"creatividad": 90, "organizacion": 85, "descanso": 80, "esperanza": 70, "contemplacion": 60}, "nivel_profundidad": 2},
        # MORE LEVEL 1 MICROACTIONS FOR VARIETY
        {"id": 166, "titulo": "Change your voice tone", "descripcion": "Speak to yourself in a soft, calm tone for a minute. Be your own refuge.", "vector_necesidades": {"silencio": 80, "contemplacion": 70, "descanso": 80, "esperanza": 90, "risa": 60}, "nivel_profundidad": 1},
        {"id": 167, "titulo": "Watch the clock in silence", "descripcion": "Observe the second hand of a clock for a minute without thinking about the passing time. Just the movement.", "vector_necesidades": {"contemplacion": 90, "silencio": 100, "organizacion": 70, "aprendizaje": 60, "descanso": 80}, "nivel_profundidad": 1},
        {"id": 168, "titulo": "Tense and relax your body", "descripcion": "Tighten all your muscles for 5 seconds and then release. Repeat 3 times. Release tension.", "vector_necesidades": {"movimiento": 90, "descanso": 95, "salud": 85, "silencio": 70, "organizacion": 50}, "nivel_profundidad": 1},
        {"id": 169, "titulo": "Water ripples in a glass", "descripcion": "Fill a glass with water, gently tap it, and observe the ripples. Small details, great calm.", "vector_necesidades": {"agua": 90, "silencio": 80, "contemplacion": 95, "creatividad": 70, "aprendizaje": 60}, "nivel_profundidad": 1},
        {"id": 170, "titulo": "The sound of the page", "descripcion": "Turn a page in a book. Listen to the sound. Feel the texture. Return to the present.", "vector_necesidades": {"aprendizaje": 80, "silencio": 90, "contemplacion": 85, "descanso": 70, "creatividad": 60}, "nivel_profundidad": 1},
    ],
    "SALIR": {
        "agotado": [
            {
                "id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade",
                "porque": "Mente cansada de pantallas. Necesitas desconectar.", "porque_en": "Screen-tired mind. You need to disconnect.",
                "que_hacer": "Busca un gran árbol. Toca su corteza. Siente la sombra fresca.", "que_hacer_en": "Find a large tree. Touch its bark. Feel the cool shade.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85}
            },
            {
                "id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe",
                "porque": "Necesitas un respiro mental. Evita ruidos. Busca paz.", "porque_en": "Need a mental break. Avoid noise. Seek peace.",
                "que_hacer": "Visita una cafetería tranquila. Pide tu bebida. Observa sin distracciones.", "que_hacer_en": "Visit a quiet cafe. Order your drink. Observe without distractions.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cafetería local tranquila.", "donde_en": "Quiet local cafe.", "gps": "quiet cafe",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70}
            },
            {
                "id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden",
                "porque": "Mente agotada. Reconéctate con lo natural. Aire puro.", "porque_en": "Exhausted mind. Reconnect with nature. Pure air.",
                "que_hacer": "Pasea sin prisa por senderos. Observa plantas y flores. Respira hondo.", "que_hacer_en": "Stroll leisurely on paths. Observe plants and flowers. Breathe deeply.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín botánico público.", "donde_en": "Public botanical garden.", "gps": "botanical garden",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90}
            },
            {
                "id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook",
                "porque": "Necesitas perspectiva. Eleva tu mirada. Rompe la rutina visual.", "porque_en": "Need perspective. Elevate your gaze. Break visual routine.",
                "que_hacer": "Encuentra un punto alto con vista. Observa el horizonte. Siente la inmensidad.", "que_hacer_en": "Find a high point with a view. Observe the horizon. Feel the immensity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95}
            },
            {
                "id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class",
                "porque": "Mente sobrecargada. Busca herramientas para la calma interna. Regula tu ser.", "porque_en": "Overloaded mind. Seek tools for inner calm. Regulate your being.",
                "que_hacer": "Asiste a una sesión de meditación guiada. Concéntrate en la respiración. Suelta.", "que_hacer_en": "Attend a guided meditation session. Focus on breathing. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90}
            },
            {
                "id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing",
                "porque": "Mente agitada. Enfoca tu mirada en la inmensidad. Deja que los pensamientos pasen.", "porque_en": "Agitated mind. Focus your gaze on vastness. Let thoughts pass.",
                "que_hacer": "Busca un lugar abierto, recuéstate y observa el movimiento de las nubes.", "que_hacer_en": "Find an open space, lie down, and watch the clouds move.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85}
            },
        ],
        "estresado": [
            {
                "id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk",
                "porque": "Cuerpo tenso. Libera estrés al caminar. Siente tu fuerza.", "porque_en": "Tense body. Release stress by walking. Feel your strength.",
                "que_hacer": "Encuentra rampa o escaleras públicas. Sube a paso firme. Usa tu energía.", "que_hacer_en": "Find public ramp or stairs. Climb steadily. Use your energy.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public stairs",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75}
            },
            {
                "id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga",
                "porque": "Mente acelerada. Conecta cuerpo y naturaleza. Respira consciente.", "porque_en": "Racing mind. Connect body and nature. Conscious breath.",
                "que_hacer": "Busca un parque. Extiende tu mat. Sigue una rutina de yoga o estiramientos.", "que_hacer_en": "Find a park. Lay your mat. Follow a yoga or stretching routine.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80}
            },
            {
                "id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym",
                "porque": "Necesitas liberar energía. Convierte la tensión en fuerza. Activa tu cuerpo.", "porque_en": "Need to release energy. Convert tension to strength. Activate your body.",
                "que_hacer": "Visita un gimnasio público o de bajo costo. Enfócate en tu rutina. Suda.", "que_hacer_en": "Visit a public or low-cost gym. Focus on your routine. Sweat.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60}
            },
            {
                "id": 112, "titulo": "Sendero Corto Natural", "titulo_en": "Short Nature Trail",
                "porque": "Sobrecarga de estímulos. Desconéctate un momento. Camina en paz.", "porque_en": "Overload of stimuli. Disconnect for a moment. Walk in peace.",
                "que_hacer": "Encuentra un sendero. Camina a paso ligero. Observa el entorno natural.", "que_hacer_en": "Find a trail. Walk briskly. Observe the natural surroundings.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sendero natural o bosque.", "donde_en": "Nature trail or forest.", "gps": "short nature trail",
                "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "agua": 40, "sol": 60, "sombra": 70, "aire_fresco": 100, "creatividad": 40, "comunidad": 20, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "descanso": 60, "organizacion": 20, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85}
            },
            {
                "id": 113, "titulo": "Pista de Atletismo", "titulo_en": "Running Track",
                "porque": "Mente acelerada. Quema esa energía extra. Enfoca tu ritmo.", "porque_en": "Racing mind. Burn off extra energy. Focus your rhythm.",
                "que_hacer": "Dirígete a una pista pública. Corre o camina a tu propio paso. Libera.", "que_hacer_en": "Go to a public track. Run or walk at your own pace. Release.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pista de atletismo pública.", "donde_en": "Public running track.", "gps": "public running track",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 40, "agua": 10, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 10, "comunidad": 50, "aprendizaje": 20, "juego": 30, "contemplacion": 50, "descanso": 10, "organizacion": 70, "alimentacion": 0, "musica": 50, "risa": 20, "esperanza": 70}
            },
            {
                "id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route",
                "porque": "Necesitas liberar tensión y moverte rápido. Siente el viento. Explora tu entorno.", "porque_en": "Need to release tension and move fast. Feel the wind. Explore your surroundings.",
                "que_hacer": "Encuentra un carril bici seguro y pedalea. Siente la velocidad y el control.", "que_hacer_en": "Find a safe bike lane and pedal. Feel the speed and control.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80}
            },
        ],
        "aburrido": [
            {
                "id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk",
                "porque": "Días repetitivos. Busca novedad. Despierta tu visión.", "porque_en": "Repetitive days. Seek novelty. Awaken your sight.",
                "que_hacer": "Camina lento. Busca murales y dibujos grandes en tu zona.", "que_hacer_en": "Walk slowly. Find large murals and drawings in your area.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street art",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}
            },
            {
                "id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market",
                "porque": "Necesitas nuevos estímulos. Sabores y olores frescos. Apoya lo local.", "porque_en": "Need new stimuli. Fresh tastes and smells. Support local.",
                "que_hacer": "Visita un mercado local. Prueba algo nuevo. Habla con los vendedores.", "que_hacer_en": "Visit a local market. Try something new. Talk to vendors.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers market",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "silencio": 30, "agua": 10, "sol": 70, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 60, "juego": 40, "contemplacion": 50, "descanso": 30, "organizacion": 50, "alimentacion": 100, "musica": 30, "risa": 70, "esperanza": 80}
            },
            {
                "id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition",
                "porque": "Mente en bucle. Busca inspiración. Despierta tu creatividad.", "porque_en": "Mind in a loop. Seek inspiration. Awaken your creativity.",
                "que_hacer": "Visita una galería o museo local. Observa el arte. Reflexiona en silencio.", "que_hacer_en": "Visit a local gallery or museum. Observe the art. Reflect in silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art gallery",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 70, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 30, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 10, "contemplacion": 95, "descanso": 60, "organizacion": 70, "alimentacion": 0, "musica": 60, "risa": 20, "esperanza": 85}
            },
            {
                "id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park",
                "porque": "Necesitas energía visual. Observa la libertad y el movimiento. Conéctate con el juego.", "porque_en": "Need visual energy. Observe freedom and movement. Connect with play.",
                "que_hacer": "Acércate a un skate park. Observa a los patinadores. Siente la vitalidad.", "que_hacer_en": "Go to a skate park. Watch the skaters. Feel the vitality.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate park",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 30, "silencio": 20, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 80, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 60, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 70, "risa": 90, "esperanza": 90}
            },
            {
                "id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore",
                "porque": "Busca historias y conocimiento. Desconéctate del mundo digital. Nutre tu mente.", "porque_en": "Seek stories and knowledge. Disconnect from digital. Nourish your mind.",
                "que_hacer": "Explora una librería de segunda mano. Busca títulos inesperados. Disfruta el aroma.", "que_hacer_en": "Explore a used bookstore. Look for unexpected titles. Enjoy the scent.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used bookstore",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 85, "agua": 0, "sol": 20, "sombra": 95, "aire_fresco": 40, "creatividad": 90, "comunidad": 30, "aprendizaje": 100, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 70, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 75}
            },
            {
                "id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema",
                "porque": "Necesitas un cambio de ambiente y una nueva perspectiva. Disfruta una historia en un entorno diferente.", "porque_en": "Need a change of scenery and new perspective. Enjoy a story in a different setting.",
                "que_hacer": "Asiste a una proyección de cine al aire libre. Sumérgete en la película y el ambiente.", "que_hacer_en": "Attend an outdoor cinema screening. Immerse yourself in the film and atmosphere.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor cinema",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 40, "agua": 10, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "descanso": 70, "organizacion": 20, "alimentacion": 60, "musica": 70, "risa": 70, "esperanza": 85}
            },
        ],
        "cansado": [
            {
                "id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading",
                "porque": "Necesitas calma. Aprende sin distracciones. Recarga tu energía.", "porque_en": "Need calm. Learn without distractions. Recharge your energy.",
                "que_hacer": "Visita tu biblioteca local. Busca un libro o disfruta el silencio.", "que_hacer_en": "Visit your local library. Find a book or enjoy the silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70}
            },
            {
                "id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk",
                "porque": "Necesitas despejar la mente. Aire fresco y vistas al agua. Caminata relajante.", "porque_en": "Need to clear mind. Fresh air and water views. Relaxing walk.",
                "que_hacer": "Camina por el muelle o puerto. Observa los barcos. Escucha el agua.", "que_hacer_en": "Walk along the dock or harbor. Watch the boats. Listen to the water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90}
            },
            {
                "id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory",
                "porque": "Mente ansiosa. Busca perspectiva universal. Maravíllate con el cosmos.", "porque_en": "Anxious mind. Seek universal perspective. Marvel at the cosmos.",
                "que_hacer": "Visita un observatorio. Aprende sobre el universo. Observa las estrellas (si es posible).", "que_hacer_en": "Visit an observatory. Learn about the universe. Stargaze (if possible).",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95}
            },
            {
                "id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza",
                "porque": "Necesitas observar. Conéctate con la vida urbana. Descansa y reflexiona.", "porque_en": "Need to observe. Connect with urban life. Rest and reflect.",
                "que_hacer": "Siéntate en un banco. Observa a la gente pasar. Siente el pulso de la ciudad.", "que_hacer_en": "Sit on a bench. Watch people pass by. Feel the city's pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85}
            },
            {
                "id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour",
                "porque": "Mente agotada de lo predecible. Necesitas una inyección de conocimiento y un suave movimiento. Aprende mientras caminas.", "porque_en": "Mind tired of predictability. Need an injection of knowledge and gentle movement. Learn as you walk.",
                "que_hacer": "Busca un tour a pie gratuito o de bajo costo por tu ciudad. Descubre historias locales.", "que_hacer_en": "Find a free or low-cost walking tour of your city. Discover local stories.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90}
            },
        ],
        "ansioso": [
            {
                "id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water",
                "porque": "Agua en movimiento. Calma tu mente. Relaja tensiones.", "porque_en": "Moving water. Calm your mind. Release tensions.",
                "que_hacer": "Busca fuente, lago o río cercano. Observa el flujo. Déjate llevar.", "que_hacer_en": "Find nearby fountain, lake, or river. Observe the flow. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80}
            },
            {
                "id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride",
                "porque": "Estrés acumulado. Necesitas desconexión total. Flota y relájate.", "porque_en": "Accumulated stress. Need total disconnection. Float and relax.",
                "que_hacer": "Realiza un paseo corto en bote. Siente la brisa. Observa la inmensidad del agua.", "que_hacer_en": "Take a short boat ride. Feel the breeze. Observe the vastness of water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90}
            },
            {
                "id": 123, "titulo": "Jardín de Rocas/Zen", "titulo_en": "Rock/Zen Garden",
                "porque": "Mente agitada. Busca orden y armonía. Centra tus pensamientos.", "porque_en": "Agitated mind. Seek order and harmony. Center your thoughts.",
                "que_hacer": "Encuentra un jardín de rocas. Observa las formas y la disposición. Medita en su calma.", "que_hacer_en": "Find a rock garden. Observe the shapes and arrangement. Meditate in its calm.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90}
            },
            {
                "id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park",
                "porque": "Necesitas risas y alegría. Observa el juego inocente. Contagia la energía positiva.", "porque_en": "Need laughter and joy. Observe innocent play. Catch positive energy.",
                "que_hacer": "Visita un parque de perros. Observa su interacción. Siente la diversión.", "que_hacer_en": "Visit a dog park. Observe their interaction. Feel the fun.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90}
            },
            {
                "id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music",
                "porque": "Mente estresada. Necesitas una experiencia sensorial. Permite que la música te calme.", "porque_en": "Stressed mind. Need a sensory experience. Let music calm you.",
                "que_hacer": "Encuentra un lugar con música en vivo tranquila. Escucha, relájate y disfruta.", "que_hacer_en": "Find a place with calm live music. Listen, relax, and enjoy.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85}
            },
            {
                "id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool",
                "porque": "Cuerpo tenso, mente agitada. El agua relaja y el movimiento controlado calma. Flota tus preocupaciones.", "porque_en": "Tense body, agitated mind. Water relaxes and controlled movement calms. Float your worries away.",
                "que_hacer": "Visita una piscina pública, date un chapuzón o simplemente relájate en el agua.", "que_hacer_en": "Visit a public pool, take a dip or just relax in the water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85}
            },
        ],
    }
}

BIG_TECH_RESOURCES = {
    "spotify_audio_es": "https://open.spotify.com/playlist/37i9dQZF1DWVpI8wA5B7T2?si=5b07a5d1b3334258", # Spotify Relax & Focus
    "youtube_audio_es": "https://www.youtube.com/results?search_query=sonidos+naturaleza+relajantes+meditacion",
    "spotify_audio_en": "https://open.spotify.com/playlist/37i9dQZF1DWVpI8wA5B7T2?si=5b07a5d1b3334258", # Spotify Relax & Focus
    "youtube_audio_en": "https://www.youtube.com/results?search_query=relaxing+nature+sounds+meditation",
    "spotify_music_es": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=e2b207a9425048b3", # Ambient Relaxing Instrumental
    "youtube_music_es": "https://www.youtube.com/results?search_query=musica+relajante+instrumental+calma",
    "spotify_music_en": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=e2b207a9425048b3", # Ambient Relaxing Instrumental
    "youtube_music_en": "https://www.youtube.com/results?search_query=calm+relaxing+instrumental+music",
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
        score += (100 - diferencia) * 0.5

    # --------------------------------------------------
    # Priorizar necesidades insatisfechas (altas en perfil)
    # y que la misión las cubra bien.
    # --------------------------------------------------
    for necesidad, valor_usuario in perfil_local.items():
        if necesidad == "indicador_ansiedad":
            continue
        if valor_usuario > 70 and vector_necesidades.get(necesidad, 0) > 70:
            score += (valor_usuario * 0.3)
        elif valor_usuario > 50 and vector_necesidades.get(necesidad, 0) > 50:
             score += (valor_usuario * 0.1)

    # --------------------------------------------------
    # Priorizar ansiedad: Misiones que atienden directamente la ansiedad.
    # --------------------------------------------------
    ansiedad = perfil_local.get("indicador_ansiedad", 0)
    if ansiedad >= 70:
        score += vector_necesidades.get("silencio", 0) * 0.5
        score += vector_necesidades.get("descanso", 0) * 0.5
        score += vector_necesidades.get("esperanza", 0) * 0.4
        score += vector_necesidades.get("naturaleza", 0) * 0.3
        score += vector_necesidades.get("agua", 0) * 0.3
    elif ansiedad >= 40:
        score += vector_necesidades.get("descanso", 0) * 0.2
        score += vector_necesidades.get("silencio", 0) * 0.2
   
    # --------------------------------------------------
    # Bonus/Penalización por nivel de profundidad (para misiones CASA)
    # --------------------------------------------------
    nivel_profundidad_mision = vector_necesidades.get("nivel_profundidad", 1) # Default 1 if not specified
    if nivel_profundidad_mision == 2:
        if ansiedad < 30: # Usuario calmado, puede buscar más profundidad
            score += 30 # Gran bonus para misiones de profundidad 2
        elif ansiedad < 60: # Ansiedad moderada
            score += 15 # Pequeño bonus
        else: # Ansiedad alta, no priorizar profundidad 2
            score -= 10 # Pequeña penalización para evitar sobrecarga
    
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
    # Esto evita que un score bajo pero único siempre gane por poco.
    if mejor_score <= 100: # Threshold adjusted for more typical scores, but still allows variety
        scores_unicos = {c["score"] for c in candidatos}
        if len(scores_unicos) == 1:
             return random.choice(candidatos)

    score_umbral = max(mejor_score * 0.8, mejor_score - 150)
   
    mejores_candidatos_para_eleccion = [
        c for c in candidatos if c["score"] >= score_umbral
    ]
   
    if len(mejores_candidatos_para_eleccion) == 1:
        return mejores_candidatos_para_eleccion[0]

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
    if seleccion is None: # Error mecánico: '==' en vez de 'is' o '=='
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
            ids_seleccionados.add(mision_aleatoria["id"])

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
   
    # Si quedan muy pocas sin repetir, o si la ansiedad es alta, considerar todo el catálogo de nuevo
    ansiedad = perfil_local.get("indicador_ansiedad", 0)
    if len(disponibles) < cantidad * 2 or ansiedad > 70:
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

# ============================================================
# NLP-LITE para Ajuste de Perfil desde Desahogo (Mejora 1)
# ============================================================
def ajustar_perfil_por_desahogo(perfil_local, desahogo_text):
    if not desahogo_text:
        return perfil_local

    desahogo_lower = desahogo_text.lower()
    ajustes = {
        # Ansiedad/Estrés
        "ansiedad": {"indicador_ansiedad": 25, "descanso": -15, "silencio": -10},
        "estres": {"indicador_ansiedad": 20, "descanso": -10, "organizacion": -10},
        "agobio": {"indicador_ansiedad": 20, "esperanza": -10, "contemplacion": -10},
        "presion": {"indicador_ansiedad": 15, "descanso": -5},
        "overwhelmed": {"indicador_ansiedad": 25, "organizacion": -15},
        "stressed": {"indicador_ansiedad": 20, "descanso": -10},
        
        # Silencio/Ruido
        "ruido": {"silencio": -20, "contemplacion": -10},
        "noisy": {"silencio": -20, "contemplacion": -10},

        # Movimiento/Estatismo
        "sentado": {"movimiento": -15},
        "estatico": {"movimiento": -15, "juego": -10},
        "sedentario": {"movimiento": -20},
        "sitting": {"movimiento": -15},
        "static": {"movimiento": -15},
        
        # Creatividad/Aburrimiento
        "aburrido": {"creatividad": 15, "aprendizaje": 10, "juego": 10},
        "monotono": {"creatividad": 15, "aprendizaje": 10},
        "bored": {"creatividad": 15, "aprendizaje": 10},
        
        # Comunidad/Aislamiento
        "solo": {"comunidad": -15, "esperanza": -5},
        "aislado": {"comunidad": -20, "esperanza": -10},
        "lonely": {"comunidad": -15, "esperanza": -5},
        "isolated": {"comunidad": -20, "esperanza": -10},

        # Naturaleza/Encierro
        "encerrado": {"naturaleza": -15, "aire_fresco": -15},
        "inside": {"naturaleza": -15, "aire_fresco": -15},
        
        # Esperanza/Desmotivación
        "desesperanza": {"esperanza": -20},
        "hopeless": {"esperanza": -20},

        # descanso/cansancio
        "cansado": {"descanso": -20, "movimiento": -10},
        "agotado": {"descanso": -25, "energia": -10}, # 'energia' not in default, but could be conceptual. Use existing.
        "tired": {"descanso": -20, "movimiento": -10},
        "exhausted": {"descanso": -25},
    }

    for keyword, efectos in ajustes.items():
        if keyword in desahogo_lower:
            for necesidad, cambio in efectos.items():
                current_value = perfil_local.get(necesidad, DEFAULT_NECESSITY_VECTOR.get(necesidad, 50))
                new_value = current_value + cambio
                perfil_local[necesidad] = max(0, min(100, new_value)) # Clamp between 0 and 100

    # Especial: si se menciona explícitamente "trabajo" o "dinero" sin buscar empleo, aumenta ansiedad levemente
    sensitive_non_job_keywords = ["trabajo", "dinero", "bills", "work", "money"]
    explicitly_seeking_job = any(phrase in desahogo_lower for phrase in ["quiero buscar trabajo", "necesito un empleo", "busco trabajo", "find a job", "looking for work"])
    
    if any(k in desahogo_lower for k in sensitive_non_job_keywords) and not explicitly_seeking_job:
        current_ansiedad = perfil_local.get("indicador_ansiedad", 0)
        perfil_local["indicador_ansiedad"] = max(0, min(100, current_ansiedad + 10))

    return perfil_local


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

    # Aplicar ajustes de perfil_local basados en el desahogo (Mejora 1)
    perfil_local = ajustar_perfil_por_desahogo(perfil_local, desahogo)

    # ============================================================
    # TERAPEUTIC STRESS INTERCEPTOR FILTER
    # Eliminar cualquier elemento que pueda aumentar el estrés del cliente.
    # Si el desahogo contiene palabras críticas, se fuerza una microacción de recuperación mental.
    # ============================================================
    sensitive_keywords = [
        "trabajo", "empleo", "job", "jobs", "work", "career", "interview", "resume", "cv", "curriculum",
        "linkedin", "indeed", "networking", "cliente", "client", "empresa", "company", "income",
        "earn money", "ganar dinero", "producir", "productividad", "buscar oportunidades",
        "buscar ofertas", "enviar currículo", "actualizar linkedin", "conseguir empleo",
        "salir a buscar trabajo", "metas profesionales", "presion economica", "presión económica",
        "biles", "deudas", "misery", "exploitation", "amazon", "walmart", "costco", "fresco",
        "tienda", "comprar", "dinero", "economy", "oportunidades laborales", "solicitudes de empleo",
        "visitar empresas", "buscando clientes", "producir dinero", "obligaciones laborales",
        "responsabilidades", "tareas", "negocio", "negocios", "presión", "presiones"
    ]

    force_recovery_mission = False
    # Check if *explicitly* asking for work, as per rule
    explicitly_seeking_job = any(phrase in desahogo for phrase in ["quiero buscar trabajo", "necesito un empleo", "busco trabajo", "find a job", "looking for work"])
   
    if desahogo and not explicitly_seeking_job: # Only apply stress filter if not explicitly seeking job
        desahogo_lower = desahogo.lower()
        if any(keyword in desahogo_lower for keyword in sensitive_keywords):
            force_recovery_mission = True
            opcion_usuario = "CASA" # Force CASA mode for recovery mission

    if force_recovery_mission:
        idioma = "EN" if lang.lower() == "en" else "ES"
        # Seleccionar una de las 10 nuevas microacciones (IDs 151 a 160)
        microacciones_ids = list(range(151, 161))
       
        # Filtrar misiones_completas para incluir solo las microacciones
        misiones_completas_casa = [m for m in BASE_MISIONES[f"CASA_{idioma}"] if m["id"] in microacciones_ids]
       
        if not misiones_completas_casa: # Fallback if for some reason no microactions are found
            misiones_completas_casa = BASE_MISIONES[f"CASA_{idioma}"]

        historial_casa = payload.get("historial_casa", [])
       
        info_seleccionada = seleccionar_mision_inteligente(
            misiones=misiones_completas_casa,
            perfil_local=perfil_local,
            historial=historial_casa # Use CASA history for this selection
        )
       
        if not info_seleccionada: # Fallback just in case
            info_seleccionada = random.choice(misiones_completas_casa)
           
        historial_casa = actualizar_historial(historial_casa, info_seleccionada["id"], MAX_HISTORY_CASA)

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": [info_seleccionada], # Return as a list for consistency with normal CASA flow
            "historial_casa_actualizado": historial_casa,
            "forced_recovery": True # Indicate that this was a forced recovery
        })

    # 1. DOMESTIC INTERVENTION (CASA MODE)
    if opcion_usuario == "CASA":
        idioma = "EN" if lang.lower() == "en" else "ES"
        misiones_completas = (
            BASE_MISIONES[f"CASA_{idioma}"]
        )
       
        historial_casa = payload.get("historial_casa", [])
       
        misiones_casa = seleccionar_misiones_casa_inteligente(
            misiones_completas,
            perfil_local,
            historial_casa,
            cantidad=3
        )
       
        for m in misiones_casa:
            historial_casa = actualizar_historial(historial_casa, m["id"], MAX_HISTORY_CASA)
        
        # Generar enlace de audio sugerido para CASA (Mejora 2)
        suggested_audio_link = None
        ansiedad = perfil_local.get("indicador_ansiedad", 0)
        necesidad_silencio = perfil_local.get("silencio", 50)
        necesidad_musica = perfil_local.get("musica", 50)

        if ansiedad > 60 or necesidad_silencio < 40:
            suggested_audio_link = BIG_TECH_RESOURCES[f"youtube_audio_{lang}"] if random.random() < 0.5 else BIG_TECH_RESOURCES[f"spotify_audio_{lang}"]
        elif necesidad_musica < 40:
            suggested_audio_link = BIG_TECH_RESOURCES[f"youtube_music_{lang}"] if random.random() < 0.5 else BIG_TECH_RESOURCES[f"spotify_music_{lang}"]

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": misiones_casa,
            "historial_casa_actualizado": historial_casa,
            "suggested_audio_link": suggested_audio_link # Añadido el link de audio
        })

    # ============================================================
    # 2. FIELD ACTION (SALIR MODE - CWRE INTELLIGENT ENGINE V2)
    #    Ahora devuelve 3 opciones para que el frontend elija.
    # ============================================================
    opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(
        mente,
        BASE_MISIONES["SALIR"]["aburrido"]
    )
   
    historial_salir = payload.get(
        "historial_salir",
        []
    )
   
    # Selecciona 3 misiones diversas y de alto score
    misiones_seleccionadas_raw = seleccionar_n_misiones_inteligentes(
        n=3,
        misiones=opciones_salir_candidatas,
        perfil_local=perfil_local,
        historial_actual=historial_salir # Usa historial para penalización
    )

    final_misiones_para_frontend = []

    for info_seleccionada in misiones_seleccionadas_raw:
        precio_real = ""
        if budget == "0":
            precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if lang == "es" else "COST: Zero dollars. Creative austerity to protect your mind today."
        elif budget == "1":
            precio_real = "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if lang == "es" else "COST: Low range. A minimal treat to break the routine."
        elif budget == "2":
            precio_real = "GASTO: Libre. El dinero es tu herramienta de escape hoy." if lang == "es" else "COST: Free. Money is your escape tool today."
       
        quienes_van = ""
        if perfil_tipo == "solo":
            quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if lang == "es" else "COMPANIONSHIP: You go alone to regain your center."
        elif perfil_tipo == "familia":
            quienes_van = "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia." if lang == "es" else "COMPANIONSHIP: Environment suitable for your children and family to unwind."
        elif perfil_tipo == "accesible":
            quienes_van = "ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad." if lang == "es" else "COMPANIONSHIP: Flat route with full access for physical comfort or age."
       
        titulo_ganador = info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) if lang == "en" else info_seleccionada["titulo"]
        donde_base = info_seleccionada.get("donde_en", info_seleccionada["donde"]) if lang == "en" else info_seleccionada["donde"]
       
        anclaje_geografico = zip_code
        map_base_url = "https://www.google.com/maps/search/?api=1&query="
        target_link = ""

        if lang == "en":
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
            guia_masticada = (
                f"DESTINO: {info_seleccionada['titulo'] or ''}.\n"
                f"POR QUÉ: {info_seleccionada['porque'] or ''}\n"
                f"QUÉ HACER: {info_seleccionada['que_hacer'] or ''}\n"
                f"CUÁNDO: {info_seleccionada['cuando'] or ''}\n"
                f"PARA QUÉ: {info_seleccionada['para_que'] or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador_lang = (info_seleccionada["titulo"] or "").upper()
            que_hacer_lang = info_seleccionada['que_hacer'] or ''
       
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
            "destino_titulo_en": info_seleccionada.get("titulo_en", info_seleccionada["titulo"]), # Incluir ambos para frontend
            "que_hacer": info_seleccionada["que_hacer"], # Incluir ambos para frontend
            "que_hacer_en": info_seleccionada.get("que_hacer_en", info_seleccionada["que_hacer"]), # Incluir ambos para frontend
            "destino_entorno": donde_base,
            "destino_instruccion": guia_masticada.strip(),
            "destino_instruccion_en": (
                f"TARGET: {info_seleccionada.get('titulo_en', info_seleccionada['titulo']) or ''}.\n"
                f"WHAT TO DO: {info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''}\n"
                f"WHY: {info_seleccionada.get('porque_en', info_seleccionada['porque']) or ''}\n"
                f"WHEN: {info_seleccionada.get('cuando_en', info_seleccionada['cuando']) or ''}\n"
                f"FOR WHAT: {info_seleccionada.get('para_que_en', info_seleccionada['para_que']) or ''}\n"
                f"{quienes_van}\n{precio_real}"
            ).strip(),
            "destino_coordenadas_gps": target_link,
            "vector_entorno_seleccionado": final_vector_necesidades,
        })
   
    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "misiones": final_misiones_para_frontend,
        "historial_salir_actualizado": historial_salir # Se devuelve, pero la actualización principal se hará en el frontend.
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

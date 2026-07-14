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

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

DEFAULT_NECESSITY_VECTOR = {
    "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
    "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
    "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
    "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
    "indicador_ansiedad": 0 # This is an internal indicator, not a "need" to match locations, but part of profile
}

# ============================================================
# MOTOR DE HISTORIAL INTELIGENTE CWRE V2
# Anti-Repetición + Exploración Controlada
# ============================================================
MAX_HISTORY_SALIR = 5
MAX_HISTORY_CASA = 8
MAX_HISTORY_ORACULO = 12 # Not used directly in backend, but good to keep consistent
EXPLORATION_RATE = 0.20 # Added, but not explicitly used in scoring for this version.
HISTORY_PENALTY_BASE = 40
DECAY_PER_DAY = 0.985

def limitar_historial(historial, limite):
    if historial is None:
        return []
    return historial[-limite:]

def penalizacion_historial(mision_id, historial):
    if not historial:
        return 0
    historial = list(reversed(historial)) # Check most recent first
    for posicion, antiguo in enumerate(historial):
        if antiguo == mision_id:
            # Penalización más fuerte para los más recientes
            if posicion == 0: # Última misión
                return HISTORY_PENALTY_BASE
            elif posicion == 1: # Penúltima
                return HISTORY_PENALTY_BASE * 0.85
            elif posicion == 2: # Antepenúltima
                return HISTORY_PENALTY_BASE * 0.70
            elif posicion <= (len(historial) - 1): # Más allá de las 3, pero aún en historial
                return HISTORY_PENALTY_BASE * 0.30
    return 0

def bonus_exploracion(mision_id, historial):
    if not historial:
        return 20 # Strong bonus for first mission
    if mision_id not in historial:
        return 15 # Bonus for trying something new
    return 0

def actualizar_historial(historial, nuevo_id, limite):
    historial = historial or []
    # Remove if already present to ensure it moves to the end
    if nuevo_id in historial:
        historial.remove(nuevo_id)
    historial.append(nuevo_id)
    return historial[-limite:]

def diversidad_vector(vector1, vector2):
    distancia = 0
    # Consider only actual needs for diversity calculation
    needs_to_consider = [k for k in DEFAULT_NECESSITY_VECTOR.keys() if k != "indicador_ansiedad"]
    for k in needs_to_consider:
        distancia += abs(
            vector1.get(k, 50) -
            vector2.get(k, 50)
        )
    return distancia

def decay_profile(profile, dias):
    # This decay logic is now primarily handled by the frontend `obtenerPerfilLocal`
    # for client-side consistency and less backend state management.
    # The backend will receive an already decayed profile.
    return profile

WHEN_ES = "Ahora mismo. Levántate de la silla ya."
WHEN_EN = "Right now. Get out of your chair immediately."
FOR_WHAT_ES = "Para romper el zombi urbano y recordar que la vida es más que pagar cuentas."
FOR_WHAT_EN = "To break the urban zombie and remember that life is more than paying bills."

# ============================================================
# CATÁLOGO DE MISIONES CWRE V2.1
# Expandido a >100 misiones CASA y 6+ por estado mental en SALIR
# Cada misión CASA ahora tiene un vector_necesidades
# ============================================================
BASE_MISIONES = {
    "CASA_ES": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
        {"id": 2, "titulo": "Desconexión de biles", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Deja caer la mochila de deudas. Siente tus hombros libres. Ya no está.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
        {"id": 6, "titulo": "Liberación de nudos", "descripcion": "Aprieta los puños 3 segundos. Abre de golpe. Suéltalo todo.", "vector_necesidades": {"movimiento": 90, "descanso": 70, "risa": 50, "trabajo": 30, "organizacion": 40}},
        {"id": 7, "titulo": "El aire de la calle", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
        {"id": 10, "titulo": "Orden de tu espacio", "descripcion": "Alinea tres objetos de tu mesa. Orden fuera es orden dentro.", "vector_necesidades": {"organizacion": 100, "trabajo": 70, "contemplacion": 60, "silencio": 50, "descanso": 50}},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
        {"id": 13, "titulo": "Foco en lo olvidado", "descripcion": "Elige una tarea mínima que ignorabas. Hazla ahora. Termínala.", "vector_necesidades": {"organizacion": 100, "trabajo": 80, "aprendizaje": 70, "movimiento": 30, "esperanza": 60}},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la puerta principal. Deja que el aire ruede. Huele el cambio.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}},
        {"id": 22, "titulo": "Relaxa ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}},
        # Más de 50 misiones CASA para cumplir el requisito
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
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido.", "vector_necesidades": {"movimiento": 95, "risa": 70, "descanso": 60, "trabajo": 40, "organizacion": 50}},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
        {"id": 51, "titulo": "Canta una melodía", "descripcion": "Tararea tu canción favorita suavemente. No pienses, solo siente el sonido.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
        {"id": 52, "titulo": "Escribe 3 deseos", "descripcion": "En un papel, anota tres deseos simples que te gustaría cumplir hoy.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
        {"id": 53, "titulo": "Paseo por el pasillo", "descripcion": "Camina lentamente por el pasillo de tu casa, sintiendo cada paso.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
        {"id": 54, "titulo": "Mira una planta", "descripcion": "Si tienes una planta en casa, obsérvala con atención durante un minuto.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
        {"id": 55, "titulo": "Dibuja un círculo", "descripcion": "Toma un lápiz y papel. Dibuja círculos perfectos sin pensar en nada más.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
        {"id": 56, "titulo": "Ordena un cajón", "descripcion": "Elige un cajón pequeño y ordénalo. La mente ordena cuando el espacio lo hace.", "vector_necesidades": {"organizacion": 100, "trabajo": 70, "descanso": 60, "silencio": 50, "movimiento": 40}},
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
        {"id": 68, "titulo": "Haz una lista de pendientes", "descripcion": "Escribe 3 tareas que te preocupan. Solo escribirlas ya ayuda.", "vector_necesidades": {"organizacion": 100, "trabajo": 90, "esperanza": 80, "descanso": 70, "silencio": 60}},
        {"id": 69, "titulo": "Observa el cielo", "descripcion": "Abre la ventana o sal al balcón. Observa el cielo por un minuto.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
        {"id": 70, "titulo": "Masaje facial", "descripcion": "Con las yemas de los dedos, masajea suavemente tu frente y mejillas.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
        {"id": 71, "titulo": "Cierra los ojos y escucha", "descripcion": "Siéntate cómodo, cierra los ojos y solo escucha los sonidos de tu casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
        {"id": 72, "titulo": "Tensa y relaja los pies", "descripcion": "Aprieta los dedos de tus pies durante 5 segundos y luego relájalos.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
        {"id": 73, "titulo": "Visualiza el éxito", "descripcion": "Piensa en un pequeño logro que quieras tener hoy y visualízate haciéndolo.", "vector_necesidades": {"esperanza": 100, "creatividad": 90, "contemplacion": 80, "aprendizaje": 70, "trabajo": 60}},
        {"id": 74, "titulo": "Olor consciente", "descripcion": "Huelea una flor, café o especia. Concéntrate en el aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
        {"id": 75, "titulo": "Cambia de silla", "descripcion": "Siéntate en otra silla o lugar de la casa por 5 minutos. Pequeño cambio.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}},
    ],
    "CASA_EN": [
        {"id": 1, "titulo": "Cut the autopilot", "descripcion": "Scan your body. Pinpoint the exact weight on your back. See it. You are alive.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
        {"id": 2, "titulo": "Bill Disconnection", "descripcion": "Feel your chair. The floor supports your weight for free. Let yourself fall.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
        {"id": 3, "titulo": "Screen Isolation", "descripcion": "Flip your phone. Look at a corner of the ceiling for 30 seconds. Break the loop.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
        {"id": 4, "titulo": "Release the Burden", "descripcion": "Drop the backpack of debts. Feel your shoulders free. It's gone.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
        {"id": 5, "titulo": "The Water Reset", "descripcion": "A small sip of cold water. Feel the liquid. It's life entering.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
        {"id": 6, "titulo": "Knot Liberation", "descripcion": "Clench your fists for 3 seconds. Open sharply. Let it all go.", "vector_necesidades": {"movimiento": 90, "descanso": 70, "risa": 50, "trabajo": 30, "organizacion": 40}},
        {"id": 7, "titulo": "Street Air", "descripcion": "Open the window. Let the air hit your face. Feel the outside.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
        {"id": 8, "titulo": "Energy Rotation", "descripcion": "Rotate wrists and ankles. Your body is yours. You govern this engine.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
        {"id": 9, "titulo": "Present Anchor", "descripcion": "Close your eyes. Say one good thing you have today. Say it loud.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
        {"id": 10, "titulo": "Order Your Space", "descripcion": "Align three objects on your table. Order outside is order inside.", "vector_necesidades": {"organizacion": 100, "trabajo": 70, "contemplacion": 60, "silencio": 50, "descanso": 50}},
        {"id": 11, "titulo": "Feet on the Ground", "descripcion": "Take off your shoes. Rest soles on the floor. Feel the cold. Connect.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
        {"id": 12, "titulo": "Sky Stretch", "descripcion": "Arm up. Touch the ceiling. Maintain tension. Release suddenly.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
        {"id": 13, "titulo": "Focus on the Forgotten", "descripcion": "Choose a minimal task you ignored. Do it now. Finish it.", "vector_necesidades": {"organizacion": 100, "trabajo": 80, "aprendizaje": 70, "movimiento": 30, "esperanza": 60}},
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
        # More than 50 CASA missions to meet the requirement
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
        {"id": 43, "titulo": "Shoulder Rotation", "descripcion": "Shoulders to ears, drop suddenly.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
        {"id": 44, "titulo": "Listen to Silence", "descripcion": "Search for silence between breaths.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}},
        {"id": 45, "titulo": "Ceiling Gaze", "descripcion": "Look at the ceiling. Stretch neck without moving shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}},
        {"id": 46, "titulo": "Feel Base", "descripcion": "Firm contact of legs with chair.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}},
        {"id": 47, "titulo": "Firm Fists", "descripcion": "Fists tightly for 3 seconds, open quickly.", "vector_necesidades": {"movimiento": 95, "risa": 70, "descanso": 60, "trabajo": 40, "organizacion": 50}},
        {"id": 48, "titulo": "Mental Cleanse", "descripcion": "Exhale boring worry. Out of you.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
        {"id": 49, "titulo": "Touch Table", "descripcion": "Palms on table. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
        {"id": 50, "titulo": "Total Presence", "descripcion": "You are here. You are safe. You are in control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
        {"id": 51, "titulo": "Hum a melody", "descripcion": "Hum your favorite song softly. Don't think, just feel the sound.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
        {"id": 52, "titulo": "Write 3 wishes", "descripcion": "On a piece of paper, write down three simple wishes you'd like to fulfill today.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
        {"id": 53, "titulo": "Hallway walk", "descripcion": "Walk slowly down your house's hallway, feeling each step.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
        {"id": 54, "titulo": "Look at a plant", "descripcion": "If you have a houseplant, observe it carefully for one minute.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
        {"id": 55, "titulo": "Draw a circle", "descripcion": "Take a pen and paper. Draw perfect circles without thinking about anything else.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
        {"id": 56, "titulo": "Organize a drawer", "descripcion": "Choose a small drawer and organize it. The mind organizes when space does.", "vector_necesidades": {"organizacion": 100, "trabajo": 70, "descanso": 60, "silencio": 50, "movimiento": 40}},
        {"id": 57, "titulo": "Open a random book", "descripcion": "Pick up a book, open it to a random page, and read the first sentence.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}},
        {"id": 58, "titulo": "Listen to the rain", "descripcion": "If it's raining, open the window and listen to the sound of raindrops falling.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}},
        {"id": 59, "titulo": "Dance without music", "descripcion": "Move your body freely for a minute, as if no one is watching.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}},
        {"id": 60, "titulo": "Drink an infusion", "descripcion": "Prepare a hot infusion and drink it slowly, feeling the warmth.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}},
        {"id": 61, "titulo": "Look at your hands", "descripcion": "Observe the lines and details of your hands. They are powerful tools.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}},
        {"id": 62, "titulo": "Imagine a landscape", "descripcion": "Close your eyes and imagine your favorite natural landscape for 30 seconds.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}},
        {"id": 63, "titulo": "Stretch your back", "descripcion": "Sit on the floor with your legs straight and try to touch your feet.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 64, "titulo": "Breathe through your nose", "descripcion": "Take 5 deep breaths, only through your nose, noticing the air.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
        {"id": 65, "titulo": "Shadow play", "descripcion": "With your hands, create a shape on the wall with the light of a lamp.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}},
        {"id": 66, "titulo": "An imaginary hug", "descripcion": "Hug your arms tightly, imagining it's a loved one.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}},
        {"id": 67, "titulo": "Find a blue object", "descripcion": "Quickly find 5 blue objects in your surroundings. Focus your sight.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
        {"id": 68, "titulo": "Make a to-do list", "descripcion": "Write down 3 tasks that worry you. Just writing them helps.", "vector_necesidades": {"organizacion": 100, "trabajo": 90, "esperanza": 80, "descanso": 70, "silencio": 60}},
        {"id": 69, "titulo": "Observe the sky", "descripcion": "Open the window or go to the balcony. Observe the sky for a minute.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
        {"id": 70, "titulo": "Facial massage", "descripcion": "With your fingertips, gently massage your forehead and cheeks.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
        {"id": 71, "titulo": "Close your eyes and listen", "descripcion": "Sit comfortably, close your eyes, and just listen to the sounds of your house.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
        {"id": 72, "titulo": "Tense and relax feet", "descripcion": "Squeeze your toes for 5 seconds and then relax them.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
        {"id": 73, "titulo": "Visualize success", "descripcion": "Think of a small achievement you want to have today and visualize yourself doing it.", "vector_necesidades": {"esperanza": 100, "creatividad": 90, "contemplacion": 80, "aprendizaje": 70, "trabajo": 60}},
        {"id": 74, "titulo": "Conscious smell", "descripcion": "Smell a flower, coffee, or spice. Concentrate on the aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
        {"id": 75, "titulo": "Change chairs", "descripcion": "Sit in a different chair or spot in the house for 5 minutes. Small change.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}},
    ],
    "SALIR": {
        "agotado": [
            {
                "id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade",
                "porque": "Mente cansada de pantallas. Necesitas desconectar.", "porque_en": "Screen-tired mind. You need to disconnect.",
                "que_hacer": "Busca un gran árbol. Toca su corteza. Siente la sombra fresca.", "que_hacer_en": "Find a large tree. Touch its bark. Feel the cool shade.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks+with+shade+",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "trabajo": 10, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85}
            },
            {
                "id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe",
                "porque": "Necesitas un respiro mental. Evita ruidos. Busca paz.", "porque_en": "Need a mental break. Avoid noise. Seek peace.",
                "que_hacer": "Visita una cafetería tranquila. Pide tu bebida. Observa sin distracciones.", "que_hacer_en": "Visit a quiet cafe. Order your drink. Observe without distractions.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Cafetería local tranquila.", "donde_en": "Quiet local cafe.", "gps": "quiet+cafe+",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "trabajo": 20, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70}
            },
            {
                "id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden",
                "porque": "Mente agotada. Reconéctate con lo natural. Aire puro.", "porque_en": "Exhausted mind. Reconnect with nature. Pure air.",
                "que_hacer": "Pasea sin prisa por senderos. Observa plantas y flores. Respira hondo.", "que_hacer_en": "Stroll leisurely on paths. Observe plants and flowers. Breathe deeply.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín botánico público.", "donde_en": "Public botanical garden.", "gps": "botanical+garden+",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "trabajo": 10, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90}
            },
            {
                "id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook",
                "porque": "Necesitas perspectiva. Eleva tu mirada. Rompe la rutina visual.", "porque_en": "Need perspective. Elevate your gaze. Break visual routine.",
                "que_hacer": "Encuentra un punto alto con vista. Observa el horizonte. Siente la inmensidad.", "que_hacer_en": "Find a high point with a view. Observe the horizon. Feel the immensity.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic+overlook+",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "trabajo": 5, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95}
            },
            {
                "id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class",
                "porque": "Mente sobrecargada. Busca herramientas para la calma interna. Regula tu ser.", "porque_en": "Overloaded mind. Seek tools for inner calm. Regulate your being.",
                "que_hacer": "Asiste a una sesión de meditación guiada. Concéntrate en la respiración. Suelta.", "que_hacer_en": "Attend a guided meditation session. Focus on breathing. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation+class+",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "trabajo": 0, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90}
            },
            {   # Added for 6+ missions
                "id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing",
                "porque": "Mente agitada. Enfoca tu mirada en la inmensidad. Deja que los pensamientos pasen.", "porque_en": "Agitated mind. Focus your gaze on vastness. Let thoughts pass.",
                "que_hacer": "Busca un lugar abierto, recuéstate y observa el movimiento de las nubes.", "que_hacer_en": "Find an open space, lie down, and watch the clouds move.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open+field+for+cloud+gazing+",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "trabajo": 5, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85}
            },
        ],
        "estresado": [
            {
                "id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk",
                "porque": "Cuerpo tenso. Libera estrés al caminar. Siente tu fuerza.", "porque_en": "Tense body. Release stress by walking. Feel your strength.",
                "que_hacer": "Encuentra rampa o escaleras públicas. Sube a paso firme. Usa tu energía.", "que_hacer_en": "Find public ramp or stairs. Climb steadily. Use your energy.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public+stairs+",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "trabajo": 20, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75}
            },
            {
                "id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga",
                "porque": "Mente acelerada. Conecta cuerpo y naturaleza. Respira consciente.", "porque_en": "Racing mind. Connect body and nature. Conscious breath.",
                "que_hacer": "Busca un parque. Extiende tu mat. Sigue una rutina de yoga o estiramientos.", "que_hacer_en": "Find a park. Lay your mat. Follow a yoga or stretching routine.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor+yoga+park+",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "trabajo": 10, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80}
            },
            {
                "id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym",
                "porque": "Necesitas liberar energía. Convierte el estrés en fuerza. Activa tu cuerpo.", "porque_en": "Need to release energy. Convert stress to strength. Activate your body.",
                "que_hacer": "Visita un gimnasio público o de bajo costo. Enfócate en tu rutina. Suda.", "que_hacer_en": "Visit a public or low-cost gym. Focus on your routine. Sweat.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community+gym+",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "trabajo": 50, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60}
            },
            {
                "id": 112, "titulo": "Sendero Corto Natural", "titulo_en": "Short Nature Trail",
                "porque": "Sobrecarga de estímulos. Desconéctate un momento. Camina en paz.", "porque_en": "Overload of stimuli. Disconnect for a moment. Walk in peace.",
                "que_hacer": "Encuentra un sendero. Camina a paso ligero. Observa el entorno natural.", "que_hacer_en": "Find a trail. Walk briskly. Observe the natural surroundings.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Sendero natural o bosque.", "donde_en": "Nature trail or forest.", "gps": "short+nature+trail+",
                "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "agua": 40, "sol": 60, "sombra": 70, "aire_fresco": 100, "creatividad": 40, "comunidad": 20, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "trabajo": 10, "descanso": 60, "organizacion": 20, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85}
            },
            {
                "id": 113, "titulo": "Pista de Atletismo", "titulo_en": "Running Track",
                "porque": "Mente acelerada. Quema esa energía extra. Enfoca tu ritmo.", "porque_en": "Racing mind. Burn off extra energy. Focus your rhythm.",
                "que_hacer": "Dirígete a una pista pública. Corre o camina a tu propio paso. Libera.", "que_hacer_en": "Go to a public track. Run or walk at your own pace. Release.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Pista de atletismo pública.", "donde_en": "Public running track.", "gps": "public+running+track+",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 40, "agua": 10, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 10, "comunidad": 50, "aprendizaje": 20, "juego": 30, "contemplacion": 50, "trabajo": 30, "descanso": 10, "organizacion": 70, "alimentacion": 0, "musica": 50, "risa": 20, "esperanza": 70}
            },
            {   # Added for 6+ missions
                "id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route",
                "porque": "Necesitas liberar tensión y moverte rápido. Siente el viento. Explora tu entorno.", "porque_en": "Need to release tension and move fast. Feel the wind. Explore your surroundings.",
                "que_hacer": "Encuentra un carril bici seguro y pedalea. Siente la velocidad y el control.", "que_hacer_en": "Find a safe bike lane and pedal. Feel the speed and control.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike+lane+or+route+",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "trabajo": 20, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80}
            },
        ],
        "aburrido": [
            {
                "id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk",
                "porque": "Días repetitivos. Busca novedad. Despierta tu visión.", "porque_en": "Repetitive days. Seek novelty. Awaken your sight.",
                "que_hacer": "Camina lento. Busca murales y dibujos grandes en tu zona.", "que_hacer_en": "Walk slowly. Find large murals and drawings in your area.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street+art+",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}
            },
            {
                "id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market",
                "porque": "Necesitas nuevos estímulos. Sabores y olores frescos. Apoya lo local.", "porque_en": "Need new stimuli. Fresh tastes and smells. Support local.",
                "que_hacer": "Visita un mercado local. Prueba algo nuevo. Habla con los vendedores.", "que_hacer_en": "Visit a local market. Try something new. Talk to vendors.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers+market+",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "silencio": 30, "agua": 10, "sol": 70, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 60, "juego": 40, "contemplacion": 50, "trabajo": 20, "descanso": 30, "organizacion": 50, "alimentacion": 100, "musica": 30, "risa": 70, "esperanza": 80}
            },
            {
                "id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition",
                "porque": "Mente en bucle. Busca inspiración. Despierta tu creatividad.", "porque_en": "Mind in a loop. Seek inspiration. Awaken your creativity.",
                "que_hacer": "Visita una galería o museo local. Observa el arte. Reflexiona en silencio.", "que_hacer_en": "Visit a local gallery or museum. Observe the art. Reflect in silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art+gallery+",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 70, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 30, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 10, "contemplacion": 95, "trabajo": 10, "descanso": 60, "organizacion": 70, "alimentacion": 0, "musica": 60, "risa": 20, "esperanza": 85}
            },
            {
                "id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park",
                "porque": "Necesitas energía visual. Observa la libertad y el movimiento. Conéctate con el juego.", "porque_en": "Need visual energy. Observe freedom and movement. Connect with play.",
                "que_hacer": "Acércate a un skate park. Observa a los patinadores. Siente la vitalidad.", "que_hacer_en": "Go to a skate park. Watch the skaters. Feel the vitality.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate+park+",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 30, "silencio": 20, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 80, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 60, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 70, "risa": 90, "esperanza": 90}
            },
            {
                "id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore",
                "porque": "Busca historias y conocimiento. Desconéctate del mundo digital. Nutre tu mente.", "porque_en": "Seek stories and knowledge. Disconnect from digital. Nourish your mind.",
                "que_hacer": "Explora una librería de segunda mano. Busca títulos inesperados. Disfruta el aroma.", "que_hacer_en": "Explore a used bookstore. Look for unexpected titles. Enjoy the scent.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used+bookstore+",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 85, "agua": 0, "sol": 20, "sombra": 95, "aire_fresco": 40, "creatividad": 90, "comunidad": 30, "aprendizaje": 100, "juego": 20, "contemplacion": 90, "trabajo": 20, "descanso": 80, "organizacion": 70, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 75}
            },
            {   # Added for 6+ missions
                "id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema",
                "porque": "Necesitas un cambio de ambiente y una nueva perspectiva. Disfruta una historia en un entorno diferente.", "porque_en": "Need a change of scenery and new perspective. Enjoy a story in a different setting.",
                "que_hacer": "Asiste a una proyección de cine al aire libre. Sumérgete en la película y el ambiente.", "que_hacer_en": "Attend an outdoor cinema screening. Immerse yourself in the film and atmosphere.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor+cinema+",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 40, "agua": 10, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "trabajo": 10, "descanso": 70, "organizacion": 20, "alimentacion": 60, "musica": 70, "risa": 70, "esperanza": 85}
            },
        ],
        "cansado": [
            {
                "id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading",
                "porque": "Necesitas calma. Aprende sin distracciones. Recarga tu energía.", "porque_en": "Need calm. Learn without distractions. Recharge your energy.",
                "que_hacer": "Visita tu biblioteca local. Busca un libro o disfruta el silencio.", "que_hacer_en": "Visit your local library. Find a book or enjoy the silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public+library+",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "trabajo": 40, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70}
            },
            {
                "id": 118, "titulo": "Espacio de Coworking", "titulo_en": "Coworking Space",
                "porque": "Mente dispersa. Necesitas un foco. Organiza tus ideas.", "porque_en": "Scattered mind. Need a focus. Organize your thoughts.",
                "que_hacer": "Encuentra un espacio de coworking tranquilo. Trabaja en algo pendiente. Siente la productividad.", "que_hacer_en": "Find a quiet coworking space. Work on pending tasks. Feel productive.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Espacio de coworking.", "donde_en": "Coworking space.", "gps": "coworking+space+",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 5, "silencio": 80, "agua": 10, "sol": 20, "sombra": 90, "aire_fresco": 50, "creatividad": 80, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 70, "trabajo": 100, "descanso": 50, "organizacion": 100, "alimentacion": 30, "musica": 30, "risa": 10, "esperanza": 80}
            },
            {
                "id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk",
                "porque": "Necesitas despejar la mente. Aire fresco y vistas al agua. Caminata relajante.", "porque_en": "Need to clear mind. Fresh air and water views. Relaxing walk.",
                "que_hacer": "Camina por el muelle o puerto. Observa los barcos. Escucha el agua.", "que_hacer_en": "Walk along the dock or harbor. Watch the boats. Listen to the water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor+walk+or+pier+",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "trabajo": 10, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90}
            },
            {
                "id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory",
                "porque": "Mente ansiosa. Busca perspectiva universal. Maravíllate con el cosmos.", "porque_en": "Anxious mind. Seek universal perspective. Marvel at the cosmos.",
                "que_hacer": "Visita un observatorio. Aprende sobre el universo. Observa las estrellas (si es posible).", "que_hacer_en": "Visit an observatory. Learn about the universe. Stargaze (if possible).",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical+observatory+",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "trabajo": 0, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95}
            },
            {
                "id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza",
                "porque": "Necesitas observar. Conéctate con la vida urbana. Descansa y reflexiona.", "porque_en": "Need to observe. Connect with urban life. Rest and reflect.",
                "que_hacer": "Siéntate en un banco. Observa a la gente pasar. Siente el pulso de la ciudad.", "que_hacer_en": "Sit on a bench. Watch people pass by. Feel the city's pulse.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public+plaza+",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "trabajo": 10, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85}
            },
            {   # Added for 6+ missions
                "id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour",
                "porque": "Mente agotada de lo predecible. Necesitas una inyección de conocimiento y un suave movimiento. Aprende mientras caminas.", "porque_en": "Mind tired of predictability. Need an injection of knowledge and gentle movement. Learn as you walk.",
                "que_hacer": "Busca un tour a pie gratuito o de bajo costo por tu ciudad. Descubre historias locales.", "que_hacer_en": "Find a free or low-cost walking tour of your city. Discover local stories.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free+walking+tour+",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "trabajo": 10, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90}
            },
        ],
        "ansioso": [
            {
                "id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water",
                "porque": "Agua en movimiento. Calma tu mente. Relaja tensiones.", "porque_en": "Moving water. Calm your mind. Release tensions.",
                "que_hacer": "Busca fuente, lago o río cercano. Observa el flujo. Déjate llevar.", "que_hacer_en": "Find nearby fountain, lake, or river. Observe the flow. Let go.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public+fountain+or+lake+",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "trabajo": 0, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80}
            },
            {
                "id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride",
                "porque": "Estrés acumulado. Necesitas desconexión total. Flota y relájate.", "porque_en": "Accumulated stress. Need total disconnection. Float and relax.",
                "que_hacer": "Realiza un paseo corto en bote. Siente la brisa. Observa la inmensidad del agua.", "que_hacer_en": "Take a short boat ride. Feel the breeze. Observe the vastness of water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat+rentals+lake+or+river+",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "trabajo": 0, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90}
            },
            {
                "id": 123, "titulo": "Jardín de Rocas/Zen", "titulo_en": "Rock/Zen Garden",
                "porque": "Mente agitada. Busca orden y armonía. Centra tus pensamientos.", "porque_en": "Agitated mind. Seek order and harmony. Center your thoughts.",
                "que_hacer": "Encuentra un jardín de rocas. Observa las formas y la disposición. Medita en su calma.", "que_hacer_en": "Find a rock garden. Observe the shapes and arrangement. Meditate in its calm.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen+garden+",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "trabajo": 0, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90}
            },
            {
                "id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park",
                "porque": "Necesitas risas y alegría. Observa el juego inocente. Contagia la energía positiva.", "porque_en": "Need laughter and joy. Observe innocent play. Catch positive energy.",
                "que_hacer": "Visita un parque de perros. Observa su interacción. Siente la diversión.", "que_hacer_en": "Visit a dog park. Observe their interaction. Feel the fun.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog+park+",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "trabajo": 0, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90}
            },
            {
                "id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music",
                "porque": "Mente estresada. Necesitas una experiencia sensorial. Permite que la música te calme.", "porque_en": "Stressed mind. Need a sensory experience. Let music calm you.",
                "que_hacer": "Encuentra un lugar con música en vivo tranquila. Escucha, relájate y disfruta.", "que_hacer_en": "Find a place with calm live music. Listen, relax, and enjoy.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live+jazz+bar+",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "trabajo": 0, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85}
            },
            {   # Added for 6+ missions
                "id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool",
                "porque": "Cuerpo tenso, mente agitada. El agua relaja y el movimiento controlado calma. Flota tus preocupaciones.", "porque_en": "Tense body, agitated mind. Water relaxes and controlled movement calms. Float your worries away.",
                "que_hacer": "Visita una piscina pública, date un chapuzón o simplemente relájate en el agua.", "que_hacer_en": "Visit a public pool, take a dip or just relax in the water.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public+swimming+pool+",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "trabajo": 10, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85}
            },
        ],
        "aburrido": [ # Duplicated for the last state as it was not present
            {
                "id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk",
                "porque": "Días repetitivos. Busca novedad. Despierta tu visión.", "porque_en": "Repetitive days. Seek novelty. Awaken your sight.",
                "que_hacer": "Camina lento. Busca murales y dibujos grandes en tu zona.", "que_hacer_en": "Walk slowly. Find large murals and drawings in your area.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street+art+",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}
            },
            {
                "id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market",
                "porque": "Necesitas nuevos estímulos. Sabores y olores frescos. Apoya lo local.", "porque_en": "Need new stimuli. Fresh tastes and smells. Support local.",
                "que_hacer": "Visita un mercado local. Prueba algo nuevo. Habla con los vendedores.", "que_hacer_en": "Visit a local market. Try something new. Talk to vendors.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers+market+",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "silencio": 30, "agua": 10, "sol": 70, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 60, "juego": 40, "contemplacion": 50, "trabajo": 20, "descanso": 30, "organizacion": 50, "alimentacion": 100, "musica": 30, "risa": 70, "esperanza": 80}
            },
            {
                "id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition",
                "porque": "Mente en bucle. Busca inspiración. Despierta tu creatividad.", "porque_en": "Mind in a loop. Seek inspiration. Awaken your creativity.",
                "que_hacer": "Visita una galería o museo local. Observa el arte. Reflexiona en silencio.", "que_hacer_en": "Visit a local gallery or museum. Observe the art. Reflect in silence.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art+gallery+",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 70, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 30, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 10, "contemplacion": 95, "trabajo": 10, "descanso": 60, "organizacion": 70, "alimentacion": 0, "musica": 60, "risa": 20, "esperanza": 85}
            },
            {
                "id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park",
                "porque": "Necesitas energía visual. Observa la libertad y el movimiento. Conéctate con el juego.", "porque_en": "Need visual energy. Observe freedom and movement. Connect with play.",
                "que_hacer": "Acércate a un skate park. Observa a los patinadores. Siente la vitalidad.", "que_hacer_en": "Go to a skate park. Watch the skaters. Feel the vitality.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate+park+",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 30, "silencio": 20, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 80, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 60, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 70, "risa": 90, "esperanza": 90}
            },
            {
                "id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore",
                "porque": "Busca historias y conocimiento. Desconéctate del mundo digital. Nutre tu mente.", "porque_en": "Seek stories and knowledge. Disconnect from digital. Nourish your mind.",
                "que_hacer": "Explora una librería de segunda mano. Busca títulos inesperados. Disfruta el aroma.", "que_hacer_en": "Explore a used bookstore. Look for unexpected titles. Enjoy the scent.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used+bookstore+",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 85, "agua": 0, "sol": 20, "sombra": 95, "aire_fresco": 40, "creatividad": 90, "comunidad": 30, "aprendizaje": 100, "juego": 20, "contemplacion": 90, "trabajo": 20, "descanso": 80, "organizacion": 70, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 75}
            },
            {   # Added for 6+ missions
                "id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema",
                "porque": "Necesitas un cambio de ambiente y una nueva perspectiva. Disfruta una historia en un entorno diferente.", "porque_en": "Need a change of scenery and new perspective. Enjoy a story in a different setting.",
                "que_hacer": "Asiste a una proyección de cine al aire libre. Sumérgete en la película y el ambiente.", "que_hacer_en": "Attend an outdoor cinema screening. Immerse yourself in the film and atmosphere.",
                "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
                "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor+cinema+",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 40, "agua": 10, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "trabajo": 10, "descanso": 70, "organizacion": 20, "alimentacion": 60, "musica": 70, "risa": 70, "esperanza": 85}
            },
        ],
    }
}

BIG_TECH_RESOURCES = {
    "spotify_audio_es": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_es": "https://www.youtube.com/results?search_query=sonidos+naturaleza+relajantes",
    "spotify_audio_en": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_en": "https://www.youtube.com/results?search_query=nature+sounds+relaxing",
    "staffing_agencies_es": "agencias+de+empleo",
    "staffing_agencies_en": "employment+agencies"
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
        if necesidad == "indicador_ansiedad": # Ignore for direct matching
            continue
        usuario = perfil_local.get(necesidad, DEFAULT_NECESSITY_VECTOR.get(necesidad, 50))
        diferencia = abs(usuario - objetivo)
        score += (100 - diferencia) * 0.5 # Ponderar esta coincidencia básica

    # --------------------------------------------------
    # Priorizar necesidades insatisfechas (altas en perfil)
    # y que la misión las cubra bien.
    # --------------------------------------------------
    for necesidad, valor_usuario in perfil_local.items():
        if necesidad == "indicador_ansiedad":
            continue
        # Si una necesidad del usuario es alta (>70)
        # y la misión también la atiende (objetivo > 70),
        # se da un bonus.
        if valor_usuario > 70 and vector_necesidades.get(necesidad, 0) > 70:
            score += (valor_usuario * 0.3) # Bonus más fuerte si es una necesidad prioritaria del usuario
        elif valor_usuario > 50 and vector_necesidades.get(necesidad, 0) > 50:
             score += (valor_usuario * 0.1) # Bonus suave

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
    elif ansiedad >= 40: # Nivel moderado de ansiedad
        score += vector_necesidades.get("descanso", 0) * 0.2
        score += vector_necesidades.get("silencio", 0) * 0.2

    # --------------------------------------------------
    # Penalización por repetición histórica y bonus por exploración
    # --------------------------------------------------
    if mission_id is not None:
        score -= penalizacion_historial(mission_id, historial)
        score += bonus_exploracion(mission_id, historial)
   
    # Asegurar que el score mínimo sea 0
    return round(max(0, score), 2)

# ============================================================
# Selección por Ranking Inteligente
# ============================================================
def seleccionar_por_ranking(candidatos):
    if not candidatos:
        return None
   
    # Ordenar por score de mayor a menor
    candidatos = sorted(candidatos, key=lambda x: x["score"], reverse=True)
   
    if not candidatos:
        return None

    mejor_score = candidatos[0]["score"]
   
    # Si todos los scores son 0 (o muy bajos y cercanos), elegir uno aleatorio
    if mejor_score <= 100: # Asumiendo un score máximo posible de 1900 para todos los 19 items con 100, y una base de ~0.
        scores_unicos = {c["score"] for c in candidatos}
        if len(scores_unicos) == 1: # Todos tienen el mismo score bajo
             return random.choice(candidatos) # Elegir aleatoriamente

    # Identificar el rango de los mejores scores (ej. top 20% del mejor score)
    # o un margen fijo si el mejor score es muy alto.
    score_umbral = max(mejor_score * 0.8, mejor_score - 150) # El 80% del mejor o 150 puntos menos, el que sea mayor.
   
    mejores_candidatos_para_eleccion = [
        c for c in candidatos if c["score"] >= score_umbral
    ]
   
    # Si solo hay uno en el rango superior, lo elegimos directamente
    if len(mejores_candidatos_para_eleccion) == 1:
        return mejores_candidatos_para_eleccion[0]

    # Si hay múltiples candidatos en el rango superior, elegir aleatoriamente
    # pero ponderando por su score para que los más altos tengan más chance.
    pesos = [c["score"] for c in mejores_candidatos_para_eleccion]
    # Asegurar que los pesos sean positivos para random.choices
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
        # Asegurarse de que cada misión tenga un vector_necesidades, usar DEFAULT si falta
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
    if seleccion is None: # Si no se pudo seleccionar, fallback a random de todas las misiones
        return random.choice(misiones) if misiones else None
    return seleccion["mision"]

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
   
    # Primero, intentamos seleccionar de misiones no vistas recientemente
    disponibles = filtrar_historial(
        misiones,
        historial_casa
    )
   
    # Si hay muy pocas opciones no vistas, o ninguna, ampliamos el catálogo
    # con TODAS las misiones para asegurar variedad y evitar bloqueos.
    # Esto implementa la "rotación inteligente" si el catálogo es limitado.
    if len(disponibles) < cantidad * 2: # Considerar más del doble de la cantidad a seleccionar
        disponibles = misiones

    candidatos = []
    for mision in disponibles:
        # Asegurarse de que cada misión CASA tenga un vector_necesidades
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
   
    # Ordenar por relevancia para seleccionar las mejores candidatas
    candidatos.sort(
        key=lambda x: x["score"],
        reverse=True
    )
   
    resultado = []
    ids_en_resultado = set()
   
    for candidato in candidatos:
        mision = candidato["mision"]
        if mision["id"] in ids_en_resultado: # Ya la hemos añadido
            continue

        # Control de diversidad:
        # Asegurar que las misiones seleccionadas sean suficientemente diferentes
        # en sus vectores de necesidades.
        diferente = True
        for anterior_mision in resultado:
            distancia = diversidad_vector(
                mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                anterior_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
            )
            # Umbral de diversidad: si la distancia es muy baja,
            # las misiones son demasiado similares. Reducido a 60 para más diversidad.
            if distancia < 60:
                diferente = False
                break
       
        if diferente:
            resultado.append(mision)
            ids_en_resultado.add(mision["id"])
       
        if len(resultado) >= cantidad:
            break
           
    # Seguridad: si no encontró la cantidad deseada con diversidad,
    # completa con las mejores restantes, incluso si son similares.
    if len(resultado) < cantidad:
        for candidato in candidatos:
            mision = candidato["mision"]
            if mision["id"] not in ids_en_resultado:
                resultado.append(mision)
                ids_en_resultado.add(mision["id"])
            if len(resultado) >= cantidad:
                break
   
    # Si aun así no tenemos suficientes (catálogo muy pequeño), simplemente
    # tomamos las primeras `cantidad` del catálogo ordenado por score.
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
    estado = str(payload.get("estado", "FL")).strip() # Estado/Region not used actively in current GPS queries
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
   
    # Asegurarse de que el perfil local tenga todas las necesidades por defecto
    # y el indicador de ansiedad
    perfil_local = {
        **DEFAULT_NECESSITY_VECTOR,
        **{k: v for k, v in perfil_local.items() if k in DEFAULT_NECESSITY_VECTOR or k == "indicador_ansiedad"}
    }
    # Asegurar que el indicador_ansiedad siempre exista, por si el frontend no lo inicializa
    if "indicador_ansiedad" not in perfil_local:
        perfil_local["indicador_ansiedad"] = 0

    # 1. DOMESTIC INTERVENTION (CASA MODE)
    if opcion_usuario == "CASA":
        idioma = "EN" if lang.lower() == "en" else "ES"
        misiones_completas = (
            BASE_MISIONES[f"CASA_{idioma}"]
        ) # All CASA missions are now combined in one key for brevity
       
        historial_casa = payload.get("seen_ids_casa", []) # frontend should send this key for CASA mode
       
        misiones_casa = seleccionar_misiones_casa_inteligente(
            misiones_completas,
            perfil_local,
            historial_casa,
            cantidad=3
        )
       
        # Actualizar historial para cada misión seleccionada
        for m in misiones_casa:
            historial_casa = actualizar_historial(historial_casa, m["id"], MAX_HISTORY_CASA)
       
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": misiones_casa,
            "historial_casa_actualizado": historial_casa
        })

    # ============================================================
    # 2. FIELD ACTION (SALIR MODE - CWRE INTELLIGENT ENGINE V2)
    # ============================================================
    opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(
        mente,
        BASE_MISIONES["SALIR"]["aburrido"] # Fallback to 'aburrido' if mental state is unknown
    )
   
    historial_salir = payload.get(
        "seen_ids", # frontend should send this key for SALIR mode
        []
    )
   
    # Priorizar misiones no vistas recientemente
    opciones_disponibles = filtrar_historial(
        opciones_salir_candidatas,
        historial_salir
    )
   
    # Si no quedan opciones no vistas, o muy pocas, reusar todo el catálogo
    if len(opciones_disponibles) < 3: # Permitir cierta repetición si el catálogo es pequeño
        opciones_disponibles = opciones_salir_candidatas
   
    info_seleccionada = seleccionar_mision_inteligente(
        misiones=opciones_disponibles,
        perfil_local=perfil_local,
        historial=historial_salir
    )
   
    if not info_seleccionada: # Fallback si por algún motivo la selección falla
        info_seleccionada = random.choice(opciones_salir_candidatas)
   
    # Actualizar historial para la misión seleccionada de SALIR
    historial_salir = actualizar_historial(
        historial_salir,
        info_seleccionada["id"],
        MAX_HISTORY_SALIR
    )
   
    # Construcción de la respuesta dinámica (precio, acompañamiento, etc.)
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
   
    # FINANCIAL SURVIVAL AND WELLBEING INTERCEPTOR FILTER
    palabras_criticas_es = ["trabajo", "empleo", "compañia", "compañía", "biles", "deudas", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "economy"]
    palabras_criticas_en = ["job", "bills", "debts", "misery", "exploitation", "amazon", "walmart", "costco", "fresh", "store", "buy", "money", "economy", "work"]

    palabras_criticas = palabras_criticas_es if lang == "es" else palabras_criticas_en

    titulo_ganador = info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) if lang == "en" else info_seleccionada["titulo"]
    donde_base = info_seleccionada.get("donde_en", info_seleccionada["donde"]) if lang == "en" else info_seleccionada["donde"]
    link_base = "https://www.google.com/maps/search/?api=1&query="
    gps_query = info_seleccionada["gps"]
    guia_masticada = ""

    if any(p in desahogo for p in palabras_criticas):
        canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "STAFFING"])
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
            gps_query = ""
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
            gps_query = ""
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
        if lang == "en":
            guia_masticada = (
                f"TARGET: {info_seleccionada.get('titulo_en', info_seleccionada['titulo']) or ''}.\n"
                f"WHAT TO DO: {info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''}\n"
                f"WHY: {info_seleccionada.get('porque_en', info_seleccionada['porque']) or ''}\n"
                f"WHEN: {info_seleccionada.get('cuando_en', info_seleccionada['cuando']) or ''}\n"
                f"FOR WHAT: {info_seleccionada.get('para_que_en', info_seleccionada['para_que']) or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador = (info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) or "").upper()
        else:
            guia_masticada = (
                f"DESTINO: {info_seleccionada['titulo'] or ''}.\n"
                f"POR QUÉ: {info_seleccionada['porque'] or ''}\n"
                f"QUÉ HACER: {info_seleccionada['que_hacer'] or ''}\n"
                f"CUÁNDO: {info_seleccionada['cuando'] or ''}\n"
                f"PARA QUÉ: {info_seleccionada['para_que'] or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador = (info_seleccionada["titulo"] or "").upper()
   
    # Construcción del enlace GPS
    if link_base.startswith("https://www.google.com/maps"):
        if perfil_tipo == "accesible":
            gps_query = "wheelchair+accessible+" + gps_query
        elif perfil_tipo == "familia":
            gps_query = "family+friendly+" + gps_query
   
    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}" # Fallback for geolocation
   
    final_link = ""
    if gps_query:
        if link_base.startswith("http") and "google.com/maps" in link_base:
            final_link = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        else: # For spotify/youtube/staffing, link_base already contains the full URL
            final_link = link_base
    else:
        final_link = link_base
           
    final_vector_necesidades = {**DEFAULT_NECESSITY_VECTOR, **info_seleccionada.get("vector_necesidades", {})}
   
    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_id": info_seleccionada.get("id"),
        "destino_titulo": titulo_ganador,
        "destino_entorno": donde_base,
        "destino_instruccion": guia_masticada.strip(),
        "destino_coordenadas_gps": final_link,
        "vector_entorno_seleccionado": final_vector_necesidades,
        "historial_salir_actualizado": historial_salir # Devolver el historial actualizado para que el frontend lo guarde
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

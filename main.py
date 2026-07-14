# ==========================================================================================
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.1
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 2 (Backend Core)
from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
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

# Variables de internacionalización para el CWRE original
WHEN_ES_CWRE = "Ahora mismo. Levántate de la silla ya."
WHEN_EN_CWRE = "Right now. Get out of your chair immediately."
FOR_WHAT_ES_CWRE = "Para romper el zombi urbano y recordar que la vida es más que pagar cuentas."
FOR_WHAT_EN_CWRE = "To break the urban zombie and remember that life is more than paying bills."

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
        # NUEVAS MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160)
        {"id": 151, "titulo": "EL RETO DE LA SUSCRIPCIÓN OLVIDADA", "descripcion": "Abre tu correo o tu aplicación bancaria. Busca 'Subscription', 'Invoice' o 'Payment' y cancela una sola suscripción que ya no utilices. Recuperar el control también es ahorrar.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60}},
        {"id": 152, "titulo": "EL RETO DE LOS TRES GASTOS", "descripcion": "Abre una nota en tu teléfono y escribe únicamente los tres gastos inevitables de esta semana. No pienses en todo el mes. Solo en esta semana.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80}},
        {"id": 153, "titulo": "EL RETO DEL ORDEN DIGITAL", "descripcion": "Borra veinte capturas de pantalla, archivos o documentos que ya no necesites. El orden digital también reduce la carga mental.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70}},
        {"id": 154, "titulo": "EL RETO DEL SILENCIO", "descripcion": "Silencia durante una hora las aplicaciones que más ansiedad te generan. Tu atención también necesita descansar.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80}},
        {"id": 155, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Escribe tres cosas que hoy tienes y que hace algunos años deseabas. Tu mente necesita recordar que también has avanzado.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60}},
        {"id": 156, "titulo": "EL RETO DEL AGUA", "descripcion": "Levántate despacio, bebe un vaso completo de agua y vuelve respirando con calma.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "salud": 85, "silencio": 50}},
        {"id": 157, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre una ventana durante dos minutos y observa el cielo sin mirar el teléfono.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70}},
        {"id": 158, "titulo": "EL RETO DEL ORDEN", "descripcion": "Guarda únicamente cinco objetos que estén fuera de lugar. Cinco son suficientes por hoy.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50}},
        {"id": 159, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Realiza cinco respiraciones profundas siguiendo un ritmo lento. No tienes que hacer nada más.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
        {"id": 160, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "Durante dos minutos mira un punto lejano para permitir que tus ojos descansen de la pantalla.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}},
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
        {"id": 48, "titulo": "Mental Cleanse", "descripcion": "Exhale boring worry. Out of you.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
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
        # NUEVAS MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160)
        {"id": 151, "titulo": "THE FORGOTTEN SUBSCRIPTION CHALLENGE", "descripcion": "Open your email or banking app. Search for 'Subscription', 'Invoice', or 'Payment' and cancel a single subscription you no longer use. Regaining control is also saving.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60}},
        {"id": 152, "titulo": "THE THREE EXPENSES CHALLENGE", "descripcion": "Open a note on your phone and write down only the three unavoidable expenses for this week. Don't think about the whole month. Just this week.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80}},
        {"id": 153, "titulo": "THE DIGITAL ORDER CHALLENGE", "descripcion": "Delete twenty screenshots, files, or documents you no longer need. Digital order also reduces mental load.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70}},
        {"id": 154, "titulo": "THE SILENCE CHALLENGE", "descripcion": "Silence the apps that generate the most anxiety for an hour. Your attention also needs rest.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80}},
        {"id": 155, "titulo": "THE GRATITUDE CHALLENGE", "descripcion": "Write down three things you have today that you wished for a few years ago. Your mind needs to remember that you have also made progress.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60}},
        {"id": 156, "titulo": "THE WATER CHALLENGE", "descripcion": "Slowly stand up, drink a full glass of water, and return, breathing calmly.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "salud": 85, "silencio": 50}},
        {"id": 157, "titulo": "THE WINDOW CHALLENGE", "descripcion": "Open a window for two minutes and observe the sky without looking at your phone.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70}},
        {"id": 158, "titulo": "THE ORDER CHALLENGE", "descripcion": "Put away only five objects that are out of place. Five are enough for today.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50}},
        {"id": 159, "titulo": "THE BREATHING CHALLENGE", "descripcion": "Take five deep breaths following a slow rhythm. You don't have to do anything else.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
        {"id": 160, "titulo": "THE VISUAL REST CHALLENGE", "descripcion": "For two minutes, look at a distant point to allow your eyes to rest from the screen.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}},
    ],
    "SALIR": {
        "agotado": [
            {
                "id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade",
                "porque": "Mente cansada de pantallas. Necesitas desconectar.", "porque_en": "Screen-tired mind. You need to disconnect.",
                "que_hacer": "Busca un gran árbol. Toca su corteza. Siente la sombra fresca.", "que_hacer_en": "Find a large tree. Touch its bark. Feel the cool shade.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85},
                "destino_titulo": "Parque Urbano con Árboles", "destino_titulo_en": "Urban Park with Trees",
                "destino_instruccion": "Ve al parque más cercano. Siéntate bajo la sombra de un árbol grande. Cierra los ojos y escucha el sonido del viento en las hojas durante cinco minutos. Desconecta tu mente del mundo digital.",
                "destino_instruccion_en": "Go to the nearest park. Sit under the shade of a large tree. Close your eyes and listen to the sound of the wind in the leaves for five minutes. Disconnect your mind from the digital world.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/nearby+parks"
            },
            {
                "id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe",
                "porque": "Necesitas un respiro mental. Evita ruidos. Busca paz.", "porque_en": "Need a mental break. Avoid noise. Seek peace.",
                "que_hacer": "Visita una cafetería tranquila. Pide tu bebida. Observa sin distracciones.", "que_hacer_en": "Visit a quiet cafe. Order your drink. Observe without distractions.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Cafetería local tranquila.", "donde_en": "Quiet local cafe.", "gps": "quiet cafe",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70},
                "destino_titulo": "Cafetería Silenciosa", "destino_titulo_en": "Quiet Coffee Shop",
                "destino_instruccion": "Encuentra una cafetería con poca gente. Pide un café o té. Observa a la gente pasar por la ventana sin usar tu teléfono. Permítete simplemente existir en el momento presente.",
                "destino_instruccion_en": "Find a coffee shop with few people. Order a coffee or tea. Watch people pass by the window without using your phone. Allow yourself to simply exist in the present moment.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/quiet+coffee+shop"
            },
            {
                "id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden",
                "porque": "Mente agotada. Reconéctate con lo natural. Aire puro.", "porque_en": "Exhausted mind. Reconnect with nature. Pure air.",
                "que_hacer": "Pasea sin prisa por senderos. Observa plantas y flores. Respira hondo.", "que_hacer_en": "Stroll leisurely on paths. Observe plants and flowers. Breathe deeply.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Jardín botánico público.", "donde_en": "Public botanical garden.", "gps": "botanical garden",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90},
                "destino_titulo": "Jardín Botánico Local", "destino_titulo_en": "Local Botanical Garden",
                "destino_instruccion": "Visita el jardín botánico de tu ciudad. Camina por los senderos y enfócate en los colores, las formas y los aromas de las plantas. Déjate llevar por la tranquilidad y la belleza natural.",
                "destino_instruccion_en": "Visit your city's botanical garden. Walk the paths and focus on the colors, shapes, and aromas of the plants. Let yourself be carried away by the tranquility and natural beauty.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/botanical+garden"
            },
            {
                "id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook",
                "porque": "Necesitas perspectiva. Eleva tu mirada. Rompe la rutina visual.", "porque_en": "Need perspective. Elevate your gaze. Break visual routine.",
                "que_hacer": "Encuentra un punto alto con vista. Observa el horizonte. Siente la inmensidad.", "que_hacer_en": "Find a high point with a view. Observe the horizon. Feel the immensity.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95},
                "destino_titulo": "Mirador con Vista a la Ciudad", "destino_titulo_en": "City Overlook",
                "destino_instruccion": "Dirígete a un mirador elevado. Contempla la vista de la ciudad o el paisaje. Deja que tu mente se expanda con la amplitud del horizonte. No pienses en nada, solo observa.",
                "destino_instruccion_en": "Go to an elevated viewpoint. Contemplate the view of the city or the landscape. Let your mind expand with the vastness of the horizon. Don't think about anything, just observe.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/scenic+overlook"
            },
            {
                "id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class",
                "porque": "Mente sobrecargada. Busca herramientas para la calma interna. Regula tu ser.", "porque_en": "Overloaded mind. Seek tools for inner calm. Regulate your being.",
                "que_hacer": "Asiste a una sesión de meditación guiada. Concéntrate en tu respiración. Libera tensiones.", "que_hacer_en": "Attend a guided meditation session. Focus on your breath. Release tensions.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Centro de meditación o yoga.", "donde_en": "Meditation or yoga center.", "gps": "meditation classes",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 20, "sol": 10, "sombra": 70, "aire_fresco": 30, "creatividad": 40, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 80, "alimentacion": 0, "musica": 30, "risa": 10, "esperanza": 90},
                "destino_titulo": "Sesión de Meditación o Yoga", "destino_titulo_en": "Meditation or Yoga Session",
                "destino_instruccion": "Encuentra una clase de meditación o yoga para principiantes. Concéntrate en las instrucciones y en tu propia respiración. Permite que tu cuerpo y mente se relajen y se centren en el presente. (Considera opciones gratuitas o de prueba).",
                "destino_instruccion_en": "Find a beginner meditation or yoga class. Focus on the instructions and your own breath. Allow your body and mind to relax and center in the present. (Consider free or trial options).",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/free+meditation+classes"
            },
            {
                "id": 110, "titulo": "Biblioteca Pública", "titulo_en": "Public Library",
                "porque": "Necesitas un ambiente tranquilo para el enfoque. Estimula la mente sin distracciones.", "porque_en": "Need a quiet environment for focus. Stimulate the mind without distractions.",
                "que_hacer": "Visita una biblioteca. Encuentra un rincón tranquilo. Lee un libro o simplemente observa el silencio.", "que_hacer_en": "Visit a library. Find a quiet corner. Read a book or simply observe the silence.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library",
                "vector_necesidades": {"movimiento": 15, "naturaleza": 5, "silencio": 100, "agua": 10, "sol": 20, "sombra": 90, "aire_fresco": 20, "creatividad": 70, "comunidad": 40, "aprendizaje": 100, "juego": 5, "contemplacion": 90, "descanso": 80, "organizacion": 85, "alimentacion": 0, "musica": 5, "risa": 5, "esperanza": 75},
                "destino_titulo": "Rincón de Lectura en Biblioteca", "destino_titulo_en": "Library Reading Nook",
                "destino_instruccion": "Dirígete a la biblioteca pública. Busca una silla cómoda lejos del ruido. Elige un libro al azar y lee sus primeras páginas, o simplemente disfruta del silencio y la energía de la calma.",
                "destino_instruccion_en": "Head to the public library. Find a comfortable chair away from the noise. Choose a random book and read its first few pages, or simply enjoy the silence and calm energy.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/public+library"
            }
        ],
        "aburrido": [
            {
                "id": 111, "titulo": "Sendero natural", "titulo_en": "Nature Trail",
                "porque": "Mente aburrida. Necesitas estímulo suave y aire libre. Despertar la curiosidad.", "porque_en": "Bored mind. Need gentle stimulation and fresh air. Awaken curiosity.",
                "que_hacer": "Busca un sendero. Camina observando detalles. Siente la tierra bajo tus pies.", "que_hacer_en": "Find a trail. Walk observing details. Feel the earth under your feet.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Sendero natural cercano.", "donde_en": "Nearby nature trail.", "gps": "nature trails",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 100, "silencio": 70, "agua": 50, "sol": 80, "sombra": 70, "aire_fresco": 100, "creatividad": 80, "comunidad": 30, "aprendizaje": 70, "juego": 60, "contemplacion": 85, "descanso": 60, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 30, "esperanza": 90},
                "destino_titulo": "Caminata por Sendero Natural", "destino_titulo_en": "Nature Trail Walk",
                "destino_instruccion": "Encuentra un sendero para caminar en la naturaleza. Presta atención a los sonidos de los pájaros, el olor de la tierra y la vista de los árboles. Deja que tu mente se despeje con el movimiento y el entorno natural.",
                "destino_instruccion_en": "Find a nature trail for a walk. Pay attention to the sounds of birds, the smell of the earth, and the sight of the trees. Let your mind clear with movement and the natural environment.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/nature+trails"
            },
            {
                "id": 112, "titulo": "Galería de arte gratuita", "titulo_en": "Free Art Gallery",
                "porque": "Mente aburrida. Necesitas estímulo visual y creativo. Inspiración.", "porque_en": "Bored mind. Need visual and creative stimulation. Inspiration.",
                "que_hacer": "Visita una galería o museo gratuito. Observa las obras. Deja que tu mente divague.", "que_hacer_en": "Visit a free gallery or museum. Observe the artworks. Let your mind wander.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Galería de arte local.", "donde_en": "Local art gallery.", "gps": "free art galleries",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 60, "agua": 10, "sol": 10, "sombra": 80, "aire_fresco": 20, "creatividad": 100, "comunidad": 50, "aprendizaje": 90, "juego": 20, "contemplacion": 95, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 30, "risa": 15, "esperanza": 80},
                "destino_titulo": "Exploración de Galería de Arte", "destino_titulo_en": "Art Gallery Exploration",
                "destino_instruccion": "Busca una galería de arte con entrada gratuita. Recorre las salas y observa las obras que te llamen la atención. No necesitas entenderlas, solo permítete sentir la inspiración y la belleza. (Busca exposiciones locales gratuitas).",
                "destino_instruccion_en": "Look for an art gallery with free admission. Walk through the rooms and observe the works that catch your eye. You don't need to understand them, just allow yourself to feel the inspiration and beauty. (Look for free local exhibitions).",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/free+art+galleries"
            },
            {
                "id": 113, "titulo": "Mercado local al aire libre", "titulo_en": "Local Outdoor Market",
                "porque": "Mente aburrida. Necesitas estímulo sensorial y social ligero. Conectar con el entorno.", "porque_en": "Bored mind. Need light sensory and social stimulation. Connect with the environment.",
                "que_hacer": "Visita un mercado al aire libre. Observa la gente, los colores y olores. Sin comprar.", "que_hacer_en": "Visit an outdoor market. Observe people, colors, and smells. Without buying.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Mercado de agricultores o pulgas.", "donde_en": "Farmers' or flea market.", "gps": "farmers market near me",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 60, "silencio": 30, "agua": 20, "sol": 90, "sombra": 40, "aire_fresco": 80, "creatividad": 70, "comunidad": 90, "aprendizaje": 50, "juego": 50, "contemplacion": 70, "descanso": 40, "organizacion": 30, "alimentacion": 70, "musica": 60, "risa": 70, "esperanza": 80},
                "destino_titulo": "Paseo por Mercado de Agricultores", "destino_titulo_en": "Farmers Market Stroll",
                "destino_instruccion": "Visita un mercado de agricultores o un mercado local al aire libre. Observa los productos frescos, los colores vibrantes y el bullicio de la gente. Permite que tus sentidos se activen sin la necesidad de comprar nada.",
                "destino_instruccion_en": "Visit a farmers market or local outdoor market. Observe the fresh produce, vibrant colors, and bustling crowd. Allow your senses to activate without the need to buy anything.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/farmers+market"
            }
        ],
        "estresado": [
            {
                "id": 114, "titulo": "Fuente de agua o lago", "titulo_en": "Water Fountain or Lake",
                "porque": "Mente estresada. Necesitas el sonido calmante del agua. Paz mental.", "porque_en": "Stressed mind. Need the calming sound of water. Peace of mind.",
                "que_hacer": "Busca una fuente o un lago. Escucha el agua. Deja que el sonido te relaje.", "que_hacer_en": "Find a fountain or lake. Listen to the water. Let the sound relax you.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Parque con agua o paseo marítimo.", "donde_en": "Park with water or boardwalk.", "gps": "public fountains or lakes",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 90, "silencio": 80, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 85, "creatividad": 50, "comunidad": 20, "aprendizaje": 30, "juego": 10, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85},
                "destino_titulo": "Visita a una Fuente o Lago", "destino_titulo_en": "Visit a Fountain or Lake",
                "destino_instruccion": "Encuentra un lugar con una fuente de agua o un pequeño lago. Siéntate y escucha el sonido del agua. Siente cómo el flujo del agua se lleva tus preocupaciones. Permite que la calma te envuelva.",
                "destino_instruccion_en": "Find a place with a water fountain or a small lake. Sit down and listen to the sound of the water. Feel how the flow of water carries away your worries. Let calmness envelop you.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/public+fountain+or+lake"
            },
            {
                "id": 115, "titulo": "Piscina pública al aire libre", "titulo_en": "Outdoor Public Pool",
                "porque": "Mente estresada. Necesitas liberar tensión física y mental. Flotar.", "porque_en": "Stressed mind. Need to release physical and mental tension. Float.",
                "que_hacer": "Visita una piscina pública. Flota en el agua. Siente tu cuerpo ligero.", "que_hacer_en": "Visit a public pool. Float in the water. Feel your body light.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 70, "silencio": 40, "agua": 100, "sol": 90, "sombra": 30, "aire_fresco": 80, "creatividad": 40, "comunidad": 60, "aprendizaje": 20, "juego": 70, "contemplacion": 60, "descanso": 95, "organizacion": 20, "alimentacion": 0, "musica": 50, "risa": 80, "esperanza": 70},
                "destino_titulo": "Sesión de Flotación en Piscina", "destino_titulo_en": "Pool Floating Session",
                "destino_instruccion": "Dirígete a una piscina pública. Concéntrate en el acto de flotar. Deja que el agua sostenga tu cuerpo y libera cualquier tensión. Siente la ingravidez y la calma. (Considera ir en horas de baja afluencia).",
                "destino_instruccion_en": "Head to a public pool. Focus on the act of floating. Let the water support your body and release any tension. Feel the weightlessness and calm. (Consider going during off-peak hours).",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/public+swimming+pool"
            }
        ],
        "cansado": [
            {
                "id": 116, "titulo": "Banco de parque tranquilo", "titulo_en": "Quiet Park Bench",
                "porque": "Cansancio físico y mental. Necesitas sentarte en paz. Observar sin hacer.", "porque_en": "Physical and mental tiredness. Need to sit in peace. Observe without doing.",
                "que_hacer": "Encuentra un banco tranquilo en un parque. Siéntate. Cierra los ojos. Solo respira.", "que_hacer_en": "Find a quiet bench in a park. Sit. Close your eyes. Just breathe.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Parque local.", "donde_en": "Local park.", "gps": "quiet park benches",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 90, "agua": 20, "sol": 70, "sombra": 80, "aire_fresco": 95, "creatividad": 30, "comunidad": 10, "aprendizaje": 20, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 10, "alimentacion": 0, "musica": 10, "risa": 5, "esperanza": 90},
                "destino_titulo": "Descanso en Banco de Parque", "destino_titulo_en": "Park Bench Rest",
                "destino_instruccion": "Busca un banco desocupado en un parque. Siéntate con la espalda recta, los hombros relajados. Cierra los ojos o mira un punto fijo. Permite que el cansancio se disipe con el aire fresco y el silencio relativo.",
                "destino_instruccion_en": "Find an empty bench in a park. Sit with your back straight, shoulders relaxed. Close your eyes or look at a fixed point. Allow tiredness to dissipate with the fresh air and relative silence.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/quiet+park+benches"
            },
            {
                "id": 117, "titulo": "Jardín comunitario", "titulo_en": "Community Garden",
                "porque": "Cansancio. Necesitas un espacio con vida. Conectar con algo orgánico.", "porque_en": "Tiredness. Need a space with life. Connect with something organic.",
                "que_hacer": "Visita un jardín comunitario. Observa las plantas, los colores. Siéntate y solo sé.", "que_hacer_en": "Visit a community garden. Observe the plants, colors. Sit and just be.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Jardín o huerto comunitario.", "donde_en": "Community garden or allotment.", "gps": "community garden",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 100, "silencio": 70, "agua": 40, "sol": 80, "sombra": 60, "aire_fresco": 90, "creatividad": 60, "comunidad": 70, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "descanso": 85, "organizacion": 40, "alimentacion": 50, "musica": 30, "risa": 20, "esperanza": 90},
                "destino_titulo": "Paseo por Jardín Comunitario", "destino_titulo_en": "Community Garden Walk",
                "destino_instruccion": "Encuentra un jardín comunitario cerca de ti. Observa el crecimiento de las plantas, las flores y los pequeños detalles de la naturaleza. Este ambiente de crecimiento y colaboración es un buen antídoto contra el cansancio.",
                "destino_instruccion_en": "Find a community garden near you. Observe the growth of plants, flowers, and small details of nature. This environment of growth and collaboration is a good antidote to tiredness.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/community+garden"
            }
        ],
        "ansioso": [
            {
                "id": 118, "titulo": "Playa o río (agua)", "titulo_en": "Beach or River (water)",
                "porque": "Ansiedad. Necesitas el poder purificador del agua. Sentir la inmensidad.", "porque_en": "Anxiety. Need the purifying power of water. Feel the immensity.",
                "que_hacer": "Visita una playa o río. Mira el agua moverse. Respira su energía.", "que_hacer_en": "Visit a beach or river. Watch the water move. Breathe its energy.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Playa, río o embalse cercano.", "donde_en": "Nearby beach, river, or reservoir.", "gps": "beach or river access",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 70, "agua": 100, "sol": 90, "sombra": 40, "aire_fresco": 100, "creatividad": 60, "comunidad": 50, "aprendizaje": 40, "juego": 80, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 95},
                "destino_titulo": "Mirar el Agua: Playa o Río", "destino_titulo_en": "Observe Water: Beach or River",
                "destino_instruccion": "Dirígete a la orilla de un cuerpo de agua (playa, río, lago). Observa el movimiento del agua y escucha el sonido de las olas o la corriente. Permite que la vastedad y la fluidez del agua calmen tu ansiedad.",
                "destino_instruccion_en": "Go to the edge of a body of water (beach, river, lake). Observe the movement of the water and listen to the sound of the waves or current. Allow the vastness and fluidity of the water to calm your anxiety.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/beach+or+river+access"
            },
            {
                "id": 119, "titulo": "Parque de perros", "titulo_en": "Dog Park",
                "porque": "Ansiedad. Necesitas distracción, alegría espontánea. Contacto con vida.", "porque_en": "Anxiety. Need distraction, spontaneous joy. Contact with life.",
                "que_hacer": "Visita un parque de perros. Observa el juego. Ríe con ellos.", "que_hacer_en": "Visit a dog park. Observe the play. Laugh with them.",
                "cuando": WHEN_ES_CWRE, "cuando_en": WHEN_EN_CWRE, "para_que": FOR_WHAT_ES_CWRE, "para_que_en": FOR_WHAT_EN_CWRE,
                "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 70, "silencio": 20, "agua": 30, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 40, "comunidad": 80, "aprendizaje": 30, "juego": 100, "contemplacion": 70, "descanso": 60, "organizacion": 20, "alimentacion": 10, "musica": 50, "risa": 100, "esperanza": 90},
                "destino_titulo": "Observar en Parque de Perros", "destino_titulo_en": "Observe at Dog Park",
                "destino_instruccion": "Visita un parque de perros en tu zona. Siéntate en un banco y observa a los perros jugar. La energía libre y la alegría de los animales pueden ser muy terapéuticas para la ansiedad. No interactúes si no te sientes cómodo, solo observa.",
                "destino_instruccion_en": "Visit a local dog park. Sit on a bench and watch the dogs play. The free energy and joy of animals can be very therapeutic for anxiety. Don't interact if you don't feel comfortable, just observe.",
                "destino_coordenadas_gps": "https://www.google.com/maps/search/dog+park"
            }
        ]
    }
}

# --- Catálogos para el módulo de Matriz de Inversión ---
EMOTIONAL_STATES = [
    "ansioso", "estresado", "agotado", "aburrido", "irritable",
    "distraído", "culpable", "frustrado", "indeciso", "solitario",
    "sobrepasado", "impaciente", "pesimista", "resentido", "vacío",
    "esperanzado", "creativo", "calmado", "presente", "observador"
]

USA_BRANDS = [
    "Instagram", "TikTok", "Facebook", "Twitter", "Netflix",
    "YouTube", "Amazon", "Starbucks", "McDonald's", "Disney+",
    "Uber", "Lyft", "Doordash", "Walmart", "Target",
    "Google", "Apple", "Microsoft", "Zoom", "Spotify"
]

USA_INFRASTRUCTURE = [
    "centro comercial", "autopista", "oficina", "transporte público", "casa/apartamento",
    "parque industrial", "gimnasio", "restaurante", "cine", "aeropuerto",
    "hospital", "escuela/universidad", "calles concurridas", "estadio", "supermercado",
    "museo", "biblioteca", "playa", "montaña", "bosque"
]

# --- Pydantic Models for API Request Bodies ---
class MandoIntegralRequest(BaseModel):
    zip: str
    modo: str
    desahogo: str
    lang: str
    mente: str
    budget: str
    perfil: str
    perfil_local: dict
    historial_salir: list = []
    historial_casa: list = []

class MatrixCaptureRequest(BaseModel):
    pass # No body needed for this GET request

class MatrixInvestmentRequest(BaseModel):
    estado: str
    elemento: str
    zip_code: str

# --- API Endpoints ---
@app.get("/")
async def read_root():
    return FileResponse("static/session.html")

@app.post("/api/mando-integral")
async def mando_integral(request: MandoIntegralRequest):
    lang = request.lang
    modo = request.modo
    mente_key = request.mente
    budget_level = int(request.budget)
    perfil_user = request.perfil
    user_profile = request.perfil_local
    zip_code = request.zip

    if modo == "CASA":
        misiones_candidatas = BASE_MISIONES[f"CASA_{lang.upper()}"]
        historial = request.historial_casa
        
        # Filtrar misiones basadas en el historial
        misiones_filtradas = []
        for mision in misiones_candidatas:
            if mision["id"] not in historial:
                misiones_filtradas.append(mision)
        
        # Si ya se usaron todas, resetear historial
        if not misiones_filtradas:
            historial = []
            misiones_filtradas = misiones_candidatas
        
        # Seleccionar 3 misiones aleatorias y agregarlas al historial
        misiones_elegidas = random.sample(misiones_filtradas, min(3, len(misiones_filtradas)))
        
        nuevos_ids_historial = [m.get("id") for m in misiones_elegidas]
        for new_id in nuevos_ids_historial:
            historial = actualizar_historial(historial, new_id, MAX_HISTORY_CASA)

        response_data = {
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": misiones_elegidas,
            "historial_casa_actualizado": historial
        }
    elif modo == "SALIR":
        misiones_candidatas_base = BASE_MISIONES["SALIR"].get(mente_key, [])
        historial_salir_frontend = request.historial_salir # Already updated on frontend on mission selection

        # Filtrar y ponderar las misiones para SALIR
        misiones_ponderadas = []
        for mision in misiones_candidatas_base:
            score = 100
            score -= penalizacion_historial(mision["id"], historial_salir_frontend)
            score += bonus_exploracion(mision["id"], historial_salir_frontend)

            # Ajuste por presupuesto
            if budget_level == 0: # Gratis
                if not ("gratis" in mision.get("tags", ["gratis"]) or "free" in mision.get("tags", ["free"]) or mision.get("gps", "").startswith("parks") or mision.get("gps", "").startswith("public library") or mision.get("gps", "").startswith("nature trails")):
                    score -= 50
            elif budget_level == 1: # Bajo (ej. un cafe, transporte)
                if ("gratis" in mision.get("tags", ["gratis"]) or "free" in mision.get("tags", ["free"])):
                    score += 10
            # budget_level 2 (Abierto) no aplica penalización ni bonus por presupuesto

            # Ajuste por perfil (solo/familia/accesible) - simplificado para este ejemplo
            if perfil_user == "familia":
                if "familia" not in mision.get("tags", []):
                    score -= 20
            elif perfil_user == "accesible":
                if "accesible" not in mision.get("tags", []):
                    score -= 30

            misiones_ponderadas.append({"mision": mision, "score": max(0, score)})

        # Ordenar por score y seleccionar las 3 mejores
        misiones_ponderadas.sort(key=lambda x: x["score"], reverse=True)
        
        # Asegurarse de tener al menos 3 misiones, si no, rellenar con las disponibles
        misiones_elegidas = [item["mision"] for item in misiones_ponderadas[:3]]
        
        # Si menos de 3 únicas se encontraron, rellenar aleatoriamente
        if len(misiones_elegidas) < 3:
            todas_misiones = BASE_MISIONES["SALIR"].get(mente_key, [])
            random.shuffle(todas_misiones)
            for m in todas_misiones:
                if m not in misiones_elegidas:
                    misiones_elegidas.append(m)
                if len(misiones_elegidas) == 3:
                    break

        # Randomize the order of the chosen missions to give a sense of variety
        random.shuffle(misiones_elegidas)

        response_data = {
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "misiones": misiones_elegidas,
            "historial_salir_actualizado": historial_salir_frontend # Frontend handles direct update
        }
    else:
        response_data = {"error": "Modo no reconocido"}
        return JSONResponse(content=response_data, status_code=400)

    return JSONResponse(content=response_data)

# ==========================================================================================
# OPEN THAN GO - API PARA EL MOTOR LOGÍSTICO DE INVERSIÓN SISTÉMICA Y TELEMETRÍA INVERSA
# ==========================================================================================

@app.get("/api/v1/algoritmo-captura")
async def algoritmo_captura():
    """
    Endpoint para proveer los datos necesarios para el formulario de la matriz de inversión.
    """
    return JSONResponse(content={
        "status": "success",
        "data": {
            "estados_emocionales": EMOTIONAL_STATES,
            "marcas_usa": USA_BRANDS,
            "infraestructura_usa": USA_INFRASTRUCTURE
        }
    })

@app.post("/api/v1/algoritmo-procesar-inversion")
async def algoritmo_procesar_inversion(request_data: MatrixInvestmentRequest):
    """
    Endpoint para procesar los datos de la matriz de inversión y devolver un 'comando'
    para la desconexión.
    """
    estado = request_data.estado
    elemento = request_data.elemento
    zip_code = request_data.zip_code

    # Lógica simple para generar respuestas basadas en inputs.
    # Esto puede ser mucho más complejo con IA/ML, pero para el prototipo es suficiente.
    
    comando = "PROTOCOLO DE DESCONEXIÓN EMOCIONAL INICIADO"
    diagnostico = f"Tu mente se siente {estado} y está atrapada en {elemento} ({zip_code})."
    ejecucion = f"URGENCIA CRÍTICA: Desconecta inmediatamente. Levántate, respira profundamente y busca un punto fijo en la distancia por 60 segundos. NO MIRES TU PANTALLA."

    if "ansioso" in estado or "estresado" in estado:
        comando = "COMANDO DE PAUSA Y REGULACIÓN ACTIVADO"
        ejecucion = "Acuestate en el suelo boca arriba. Siente el piso. Cierra los ojos. 60 segundos."
    elif "aburrido" in estado or "agotado" in estado:
        comando = "COMANDO DE ACTIVACIÓN CONSCIENTE INICIADO"
        ejecucion = "Sal a la ventana o al balcón. Mira el cielo sin parpadear por 60 segundos. Luego inhala 4 segundos, retén 4, exhala 6. Repite 5 veces."
    
    # Simulación de telemetría inversa
    telemetria_inversa_data = {
        "comando_sistema": comando,
        "diagnostico_sintoma": diagnostico,
        "ejecucion_fisiologica_obligatoria": ejecucion,
        "status": "success"
    }
    return JSONResponse(content=telemetria_inversa_data)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

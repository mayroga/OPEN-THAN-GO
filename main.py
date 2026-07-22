# ==========================================================================================
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.0.1
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 2 (Backend Core)
# ==========================================================================================

import os
import random
import re
import urllib.parse
from datetime import datetime

import stripe
import uvicorn
from fastapi import FastAPI, Request, HTTPException # HTTPException import fixed
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ==========================================================================================
# MATRIZ INFINITA DE MANIFIESTOS EXISTENCIALES PARA EL ORÁCULO DE BIENESTAR (3 POR ESTADO)
# ==========================================================================================
MANIFIESTOS_ORACULO = {
    "agotado": [
        "Una persona que abre esta aplicación muchas veces no está buscando un parque. Está buscando "
        "sentirse diferente. Lo que desgasta no es la falta de destinos, sino la rutina de salir siempre "
        "sin un propósito. El verdadero problema no es encontrar un sitio nuevo, el problema es que las "
        "salidas comienzan con la pregunta equivocada. En lugar de preguntarse a dónde vamos, sería mucho "
        "más útil preguntarse qué necesitamos hoy como familia. Cuando primero se identifica esa necesidad, "
        "elegir el destino deja de ser un problema y pasa a ser una consecuencia natural. Un parque deja de "
        "ser otro parque cuando la misión es construir juntos el barco más creativo usando hojas y ramas. "
        "El lugar cambia muy poco; lo que realmente cambia es la experiencia y el propósito con el que se vive. "
        "No se trata únicamente de decirte a dónde ir. Se trata de entender cómo te sientes y proponerte una "
        "experiencia con un propósito.",

        "Quien abre esta pantalla carga con un cansancio que el descanso pasivo no puede curar. El agobio no "
        "es falta de sueño, es un exceso de entorno predecible. Te encierras en el auto huyendo de la rutina, "
        "pero manejas con la mente fija en los problemas de la semana. El error fundamental es creer que un "
        "lugar nuevo va a cambiar tu estado interno por arte de magia. El espacio físico no hace nada si tu "
        "atención sigue secuestrada por las mismas preocupaciones. Un rincón con sombra deja de ser un simple "
        "banco cuando tu objetivo real es escuchar tres sonidos diferentes de la naturaleza. El entorno cambia "
        "radicalmente cuando tú inyectas una intención clara a tus sentidos. No busques que el mundo te "
        "entretenga. Cambia tu frecuencia interna antes de abrir la puerta. Tu misión es detener el piloto automático.",

        "Quien abre esta pantalla siente que arrastra el peso del mundo sobre los hombros. El agotamiento no "
        "es solo cansancio muscular, es fatiga de decisiones acumuladas. Tu cerebro ha procesado demasiadas "
        "elecciones obligatorias durante la semana. Buscas un escape pero te mueves en piloto automático, "
        "repitiendo los mismos recorridos sin registrar el entorno. Una plaza pública deja de ser un fondo "
        "borroso cuando te sientas en un banco céntrico a observar el flujo de los transeúntes en silencio. "
        "Ver la vida avanzar a su propio ritmo te devuelve la perspectiva de inmediato. El mundo es inmenso "
        "y tus problemas actuales son transitorios. No busques resolver tu existencia hoy. Sal a recuperar tu espacio."
    ],
    "estresado": [
        "Quien abre esta aplicación muchas veces cree que le falta tiempo, pero lo que realmente le falta es "
        "espacio interior. La prisa industrial nos enseña a correr hacia destinos vacíos solo para tachar una "
        "lista de tareas los fines de semana. Subes al auto con el pulso acelerado, manejas con tensión y "
        "exiges que el lugar te cure el estrés en cinco minutos. El verdadero problema no es la velocidad del "
        "mundo exterior, sino que intentas habitar un lugar nuevo cargando con el mismo cuerpo rígido y la "
        "misma mente saturada. Una cafetería deja de ser un sitio de consumo rápido cuando tu misión es cerrar "
        "los ojos y aislar el ruido del entorno durante dos minutos. No busques que el destino te calme; cambia "
        "tu frecuencia somática antes de llegar. Hoy tu misión es desacelerar el ritmo biológico.",

        "Tu cuerpo está rígido por la velocidad del día y las notificaciones continuas. Buscas un escape pero "
        "caminas con prisa, devorando el paisaje sin registrar nada de lo que te rodea. La ansiedad te hace "
        "saltar de un estímulo a otro sin encontrar paz en ningún rincón. El asfalto y las pantallas "
        "fragmentan tu atención por completo. Un sendero natural deja de ser un camino genérico cuando el "
        "reto es sincronizar cada paso con una exhalación profunda y prolongada. Tocar la corteza rugosa de "
        "un árbol te devuelve al suelo de inmediato. No corras hacia el destino para huir de ti mismo. Detén "
        "la marcha. Siente el aire fresco en tu rostro. Tu organismo exige recuperar el ritmo natural de la vida.",

        "Tu mente corre más rápido que tus piernas y tu respiración es corta. Las alertas del teléfono y las "
        "demandas del día han fragmentado tu atención por completo. Buscas un rincón de paz pero caminas "
        "apurado, devorando el trayecto con tensión muscular en el cuello y la mandíbula. Estás huyendo de "
        "la prisa cometiendo el error de correr hacia el destino. Un espejo de agua o una fuente local dejan "
        "de ser paisaje invisible cuando te detienes frente a la orilla por tres minutos exactos. Seguir el "
        "flujo de la corriente estabiliza tu ritmo cardíaco de forma somática. No le exijas velocidad al día. "
        "Detén la marcha. Siente la inmovilidad de tu cuerpo en este instante."
    ],
    "aburrido": [
        "Muchas personas salen de casa con la falsa certeza de que comprar algo nuevo va a llenar el vacío de "
        "un día plano. La inercia te arrastra hacia el centro comercial, las tiendas de descuento o el "
        "restaurante de moda. Gastas dinero en objetos que no necesitas y a la hora regresas al mismo sillón "
        "con la rumiación intacta. Lo que tu mente busca desesperadamente no es una mercancía, es una "
        "experiencia sensorial viva. Un almacén gigante deja de ser una prisión de consumo cuando lo utilizas "
        "como un laboratorio para activar tus piernas caminando a paso firme. El aburrimiento no se cura "
        "acumulando cosas, se cura inyectando intención a tus movimientos. Sal a descubrir con los ojos "
        "abiertos, no con la tarjeta de crédito.",

        "Pasamos el día entero atrapados a través de una ventana de cristal de cinco pulgadas. Miras el mapa "
        "digital, caminas respondiendo mensajes y te sientas a comer fotografiando el plato para personas "
        "que no están ahí. Tu cuerpo se mueve por la ciudad, pero tu mente nunca sale del ecosistema de las "
        "redes sociales. Lo que desgasta tu existencia es la desconexión total con la materia real que te "
        "rodea. Una plaza pública deja de ser un fondo borroso cuando te obligas a observar el flujo de los "
        "seres humanos en silencio. El mundo físico está vivo y lleno de misterios esperando por ti. Tu misión "
        "de hoy exige un acto de soberanía: guarda el teléfono en el bolsillo. Habita el día de verdad.",

        "La rutina predecible ha apagado tu curiosidad y tus días se sienten idénticos. Caes en el bucle de "
        "consumir contenido digital basura esperando que una pantalla te devuelva el entusiasmo por vivir. "
        "Tu cuerpo está estancado en el sedentarismo visual de las mismas cuatro paredes. Lo que tu organismo "
        "exige con urgencia es un impacto de asombro analógico real. Una librería de segunda mano o un "
        "pequeño museo local dejan de ser espacios estáticos cuando buscas un título o un cartel inesperado. "
        "Perderte entre objetos físicos reales despierta tu agudeza óptica de inmediato. El aburrimiento no "
        "está en tu ciudad, está en la forma predecible de mirar tu entorno. Guarda el teléfono. Sal a "
        "descubrir el mundo con los ojos abiertos."
    ],
    # Añadido manifiestos para "cansado" y "ansioso" para completar la coherencia del diccionario
    "cansado": [
        "Sientes que el día se ha estirado demasiado y cada tarea pesa. El cansancio no es solo físico, es mental. "
        "Necesitas un respiro que nutra tu espíritu, no solo tu cuerpo. No busques excusas para quedarte, busca "
        "una excusa para revitalizarte. Una simple caminata se transforma en un ritual de recarga cuando tu "
        "propósito es observar las hojas cayendo y sentir el pulso de la tierra bajo tus pies. La clave es "
        "cambiar el enfoque: de lo que 'tienes que hacer' a lo que 'necesitas experimentar'.",

        "Cuando el agotamiento te invade, la inercia te empuja a la pasividad, pero tu ser anhela movimiento y "
        "estímulo gentil. El verdadero descanso no es la ausencia de actividad, sino la presencia de una "
        "actividad que resuene con tu alma. Un museo deja de ser un edificio frío cuando tu misión es "
        "encontrar una obra de arte que te hable, que te despierte la curiosidad dormida. Permítete la "
        "ligereza de la exploración sin presión. Tu energía no está agotada, solo mal dirigida.",

        "El zumbido constante de la vida moderna drena tu energía. Te sientes pesado, pero no enfermo. Lo que "
        "te falta es un espacio de quietud donde tu mente pueda desenredarse. No busques el silencio absoluto, "
        "busca un silencio que te permita escuchar tus propios pensamientos sin interrupciones. Una biblioteca "
        "no es solo un lugar de libros, es un santuario de la mente. Sumérgete en su atmósfera, respira lento, "
        "y permite que la calma del lugar te envuelva. Hoy, tu misión es recuperar tu centro."
    ],
    "ansioso": [
        "Tu mente es un torbellino de 'y si' y 'tengo que'. La ansiedad no te deja en paz ni un minuto. No se trata "
        "de huir de lo que te preocupa, sino de anclarte en el presente. El problema no es el mundo exterior, "
        "sino la velocidad con la que tu mente procesa cada estímulo. Un simple banco en una plaza no es "
        "solo un asiento, es un punto de observación para la vida que fluye sin prisas. Concéntrate en un "
        "detalle pequeño: el aleteo de un pájaro, el brillo del sol en una hoja. Tu misión es devolverle "
        "la calma a tu ritmo interno.",

        "Sientes un nudo en el estómago, una presión en el pecho. La prisa del día a día te asfixia. Lo que tu "
        "cuerpo grita no es por más acción, sino por una pausa profunda y consciente. No busques soluciones, "
        "busca serenidad. El agua tiene el poder de calmar. Un chorro de una fuente, el flujo de un arroyo, "
        "o las olas del mar son espejos de la fluidez que tu ser anhela. Permítete observar, sentir la frescura, "
        "y dejar que el ritmo del agua se convierta en el tuyo. Tu misión es encontrar tu propio caudal.",

        "La necesidad de control te consume, y cada pequeña incertidumbre se magnifica. Crees que necesitas "
        "resolverlo todo ahora. El error es creer que el pensamiento constante es sinónimo de solución. "
        "Necesitas un espacio donde la distracción sea pura e inocente, donde la risa y el juego te devuelvan "
        "a un estado primario de ligereza. Un parque con niños jugando, una mascota corriendo, te recuerdan "
        "que la vida es también espontaneidad y asombro. Suelta la necesidad de planificar y permite que el "
        "momento te sorprenda. Tu misión es recordar la alegría de lo impredecible."
    ]
}


# ==========================================================================================
# INYECCIÓN CRÍTICA DE CONTROL: PASARELA STRIPE & BYPASS MAESTRO
# ==========================================================================================
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

# ==========================================================================================
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
# ==========================================================================================
# MOTOR DE HISTORIAL INTELIGENTE CWRE V2
# Anti-Repetición + Exploración Controlada
# ==========================================================================================
MAX_HISTORY_SALIR = 5
MAX_HISTORY_CASA = 8
MAX_HISTORY_ORACULO = 12

# This is handled by frontend (engine.js)
EXPLORATION_RATE = 0.20
HISTORY_PENALTY_BASE = 40

def limitar_historial(historial, limite):
    if historial is None:
        return []
    return historial[-limite:]

def penalizacion_historial(mision_id, historial):
    if not historial:
        return 0

    # Prioriza las más recientes
    historial = list(reversed(historial))

    for posicion, antiguo_id in enumerate(historial):
        if antiguo_id == mision_id:
            if posicion == 0:  # Última misión
                return HISTORY_PENALTY_BASE * 1.5
            elif posicion == 1:
                return HISTORY_PENALTY_BASE
            elif posicion == 2:
                return HISTORY_PENALTY_BASE * 0.70
            elif posicion <= (len(historial) - 1):
                return HISTORY_PENALTY_BASE * 0.30
    return 0

def bonus_exploracion(mision_id, historial):
    if not historial or mision_id not in historial:
        return 20  # Bonificación significativa si nunca se ha visto

    # Reducir bonificación si ya se ha visto pero no está en el historial reciente
    limite_reciente = int(MAX_HISTORY_SALIR / 2)
    if mision_id not in limitar_historial(historial, limite_reciente):
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
        v1_val = vector1.get(k, DEFAULT_NECESSITY_VECTOR.get(k, 50))
        v2_val = vector2.get(k, DEFAULT_NECESSITY_VECTOR.get(k, 50))
        distancia += abs(v1_val - v2_val)

    return distancia

# === MODIFICACIÓN: CONSTANTES DE TIEMPO Y PROPÓSITO ACORTADAS PARA LECTURA RÁPIDA ===
WHEN_ES = "Ahora. Levántate."
WHEN_EN = "Now. Move."
FOR_WHAT_ES = "Romper rutina. Recuérdate estoy vivo."
FOR_WHAT_EN = "Break routine. Remember life."

# ============================================================
# CATÁLOGO DE MISIONES CWRE V2.1
# Adaptado para Microacciones de Recuperación Mental y sin elementos de estrés laboral/financiero.
# CORRECCIÓN MECÁNICA: Unificadas las definiciones de claves duplicadas ("estresado", "aburrido", "ansioso")
# dentro del diccionario "SALIR" para evitar la sobrescritura silenciosa de datos.
# Completadas las descripciones truncadas y aseguradas las comas y cierres de diccionarios/listas.
# ============================================================
BASE_MISIONES = {
   "CASA_ES": [
       {"id": 1, "titulo": "Corta el piloto automático", "titulo_en": "Break the autopilot", "descripcion": "Toma un instante para escanear tu cuerpo por completo. Ubica el peso exacto acumulado en tu espalda alta y míralo con absoluta calma. Siente tus latidos y recuérdate vivo en este segundo de paz.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
  {"id": 2, "titulo": "Desconexión total", "titulo_en": "Total disconnection", "descripcion": "Siente la forma de la silla debajo de tu cuerpo ahora mismo. El suelo firme sostiene todo tu peso de manera completamente gratuita y segura. No luches, déjate caer en una total calma en este instante.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
  {"id": 3, "titulo": "Aislamiento de pantalla", "titulo_en": "Screen isolation", "descripcion": "Voltea tu teléfono celular hacia abajo con total tranquilidad en este instante. Mira una esquina del techo por treinta segundos seguidos y permite que tu mente rompa el bucle de la prisa digital ahora.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
  {"id": 4, "titulo": "Soltar la carga", "titulo_en": "Let go of the load", "descripcion": "Siente tus hombros completamente libres y livianos en este momento. Visualiza que ya no cargas con esa mochila de peso invisible sobre ti. Libera la rigidez mental acumulada y respira con total soltura.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
  {"id": 5, "titulo": "El reset del agua", "titulo_en": "The water reset", "descripcion": "Toma un trago pequeño y pausado de agua fría en este momento. Siente el recorrido exacto del líquido fresco pasar por tu garganta. Es la vida pura ingresando a renovar tu organismo por completo.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
  {"id": 7, "titulo": "El aire de la ventana", "titulo_en": "Window breeze", "descripcion": "Abre la ventana de tu habitación por completo de inmediato. Deja que el aire fresco te golpee suavemente la cara en este conteo. Siente el mundo exterior y límpiate del encierro de la rutina.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
  {"id": 8, "titulo": "Rotación de energía", "titulo_en": "Energy rotation", "descripcion": "Gira suavemente tus muñecas y tus tobillos en círculos pausados. Recuerda que este cuerpo es completamente tuyo y tú gobiernas este motor. Siente cómo la energía natural vuelve a fluir libremente por tu ser.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
  {"id": 9, "titulo": "Anclaje del presente", "titulo_en": "Anchor to the present", "descripcion": "Cierra los ojos en total silencio acústico ahora mismo. Piensa detalladamente en una cosa buena y hermosa que tienes en tu vida el día de hoy. Dilo con fuerza en tu mente en calma.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
  {"id": 11, "titulo": "Pies en la tierra", "titulo_en": "Feet on the ground", "descripcion": "Quítate los zapatos ahora mismo, sin prisa alguna. Apoya las plantas de tus pies directo sobre el piso frío de la habitación. Siente la firmeza del suelo debajo de ti y conéctate.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
  {"id": 12, "titulo": "Estiramiento al cielo", "titulo_en": "Stretch to the sky", "descripcion": "Estira tu brazo firmemente hacia arriba e intenta tocar el techo con la punta de tus dedos. Mantén la tensión muscular por un segundo exacto en este conteo. Ahora suelta todo de golpe.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
  {"id": 14, "titulo": "Columna recta", "titulo_en": "Straight spine", "descripcion": "Endereza la espalda por completo en este mismo instante. Un hilo invisible tira suavemente de tu cabeza hacia el cielo. Siente cómo tu pecho se abre libremente y habita tu respiración profunda ahora.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}},
  {"id": 15, "titulo": "Contacto frío", "titulo_en": "Cold touch", "descripcion": "Busca un objeto o superficie que esté fría al tacto en tu habitación y pon tu mano encima. Siente la temperatura real por unos segundos. Esto te ayuda a calmar la mente de inmediato en tu hogar.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}},
  {"id": 16, "titulo": "Ventilación total", "titulo_en": "Total ventilation", "descripcion": "Abre la ventana más cercana de tu habitación actual. Deja que el aire nuevo entre y ruede por todo el espacio disponible. Respira despacio y nota cómo cambia el ambiente de tu casa con tranquilidad.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}},
  {"id": 17, "titulo": "Sacudida de estrés", "titulo_en": "Stress shake", "descripcion": "Ponte de pie con cuidado en tu espacio seguro. Sacude tus manos y tus piernas de forma suave como si te estuvieras quitando gotitas de agua. Haz este movimiento alegre por diez segundos en casa.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}},
  {"id": 18, "titulo": "Mirada lejana", "titulo_en": "Distant gaze", "descripcion": "Mira a través de la ventana y busca el objeto o la casa que esté más lejos de ti. Quédate observando ese punto fijo para que tus ojos descansen de las pantallas en completa paz.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}},
  {"id": 19, "titulo": "Memoria feliz", "titulo_en": "Happy memory", "descripcion": "Cierra tus ojos con suavidad por un momento en tu rincón cómodo. Trae a tu mente un recuerdo hermoso e inocente de cuando eras niño. Siente la paz que te da ese lindo día.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}},
  {"id": 20, "titulo": "Sonrisa forzada", "titulo_en": "Forced smile", "descripcion": "Dibuja una sonrisa grande en tu rostro y mantenla fija durante quince segundos completos en este momento. Este pequeño gesto le avisa a tu mente que es momento de estar en total bienestar.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}},
  {"id": 21, "titulo": "Agradecimiento", "titulo_en": "Gratitude", "descripcion": "Cierra tus ojos en completo silencio en tu sala. Piensa detenidamente en una sola cosa buena y bonita que te haya pasado durante esta semana y da las gracias en tu mente en calma.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}},
  {"id": 22, "titulo": "Relaxa ojos", "titulo_en": "Eye relax", "descripcion": "Frota las palmas de tus manos para entibiar la piel de inmediato. Colócalas suavemente sobre tus ojos cerrados y disfruta de un minuto completo de oscuridad y descanso total en tu habitación.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}},
  {"id": 23, "titulo": "Ritmo cardíaco", "titulo_en": "Heart rate", "descripcion": "Coloca tu mano derecha en el centro de tu pecho con tranquilidad. Siente el latido constante y tranquilo de tu corazón. Recuerda que este es el motor hermoso de tu vida ahora.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}},
  {"id": 24, "titulo": "Suelta cuello", "titulo_en": "Neck release", "descripcion": "Mueve tu cabeza dibujando círculos muy lentos y suaves en el aire. Siente cómo se va toda la tensión acumulada en tu cuello por culpa de mirar el teléfono en tu hogar.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}},
  {"id": 25, "titulo": "Ejercicio de palmas", "titulo_en": "Palm exercise", "descripcion": "Frota tus manos con energía hasta que sientas el calorcito en la piel. Coloca de inmediato tus palmas sobre tus hombros para regalarte un abrazo reconfortante en este momento presente.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}},
  {"id": 26, "titulo": "Sonidos lejanos", "titulo_en": "Distant sounds", "descripcion": "Quédate quieto por unos momentos en tu sala y presta mucha atención al entorno. Intenta identificar el sonido más lejano que se escuche afuera de tu casa en este instante de paz.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}},
  {"id": 27, "titulo": "Estiramiento lateral", "titulo_en": "Lateral stretch", "descripcion": "Inclina tu cuerpo de forma muy suave hacia el lado derecho y luego hacia el izquierdo con calma. Siente cómo se estira tu cintura con total comodidad y ligereza dentro de tu habitación.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
  {"id": 28, "titulo": "El vaso vacío", "titulo_en": "The empty glass", "descripcion": "Busca un vaso transparente en tu cocina. Observa su forma y cómo le entra la luz durante un minuto completo. Nota los hermosos reflejos en absoluto silencio y despeja tu mente.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}},
  {"id": 29, "titulo": "Suelta mandíbula", "titulo_en": "Jaw release", "descripcion": "Abre grande tu boca con cuidado en tu rincón cómodo. Mueve tu mandíbula despacio de un lado al otro. Siente cómo se libera toda la rigidez y la tensión acumulada del rostro.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}},
  {"id": 30, "titulo": "Pasos lentos", "titulo_en": "Slow steps", "descripcion": "Ponte de pie con suavidad en tu espacio seguro. Da diez pasos muy lentos y tranquilos dentro de tu habitación actual. Siente el apoyo completo de cada pie al caminar con calma.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}},
  {"id": 31, "titulo": "Masaje suave", "titulo_en": "Gentle massage", "descripcion": "Coloca las yemas de tus dedos sobre tus sienes ahora mismo. Dibuja círculos muy lentos y tiernos sin presionar fuerte. Siente el alivio inmediato en tu cabeza y relaja tus pensamientos.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
  {"id": 32, "titulo": "Conciencia aire", "titulo_en": "Air awareness", "descripcion": "Presta atención a tu nariz en este momento. Siente el aire fresco que entra al tomar aire y el aire tibio que sale al soltarlo. Hazlo de forma natural en tu espacio.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}},
  {"id": 33, "titulo": "Espalda firme", "titulo_en": "Firm back", "descripcion": "Lleva tus hombros suavemente hacia atrás y abre tu pecho con ligereza en este instante. Siente cómo tu cuerpo recupera su postura natural, recta y cómoda dentro de tu casa.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}},
  {"id": 34, "titulo": "Apoyo total", "titulo_en": "Total support", "descripcion": "Toma asiento con tranquilidad y relaja tu espalda. Siente cómo la silla sostiene todo el peso de tu cuerpo con total seguridad. Suelta los músculos ahora y descansa de verdad.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}},
  {"id": 35, "titulo": "Cuenta atrás", "titulo_en": "Countdown", "descripcion": "Cuenta los números al revés, comenzando desde el veinte hasta llegar al uno. Hazlo de forma muy pausada en tu mente para calmar todos tus pensamientos y encontrar total paz.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}},
  {"id": 36, "titulo": "Toca textura", "titulo_en": "Touch texture", "descripcion": "Pasa las yemas de tus dedos sobre una superficie real que tengas cerca, como una mesa de madera o una prenda de tela limpia. Nota su textura con absoluta calma.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}},
  {"id": 37, "titulo": "Estira dedos", "titulo_en": "Stretch fingers", "descripcion": "Separa y estira los dedos de tus manos lo más que puedas durante cinco segundos enteros. Después, relájalos por completo para que descansen de las pantallas en este instante.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
  {"id": 38, "titulo": "Sonido interno", "titulo_en": "Internal sound", "descripcion": "Quédate en silencio en tu rincón cómodo y escucha el sonido suave de tu propia respiración. No intentes forzarla ni cambiarla, solo nota cómo tu cuerpo respira solo.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}},
  {"id": 39, "titulo": "Mirada fija", "titulo_en": "Fixed gaze", "descripcion": "Busca un punto pequeño o una marca en la pared frente a ti. Quédate mirando ese lugar fijo con tranquilidad, permitiendo que tus ojos se enfoquen lejos de las pantallas.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}},
  {"id": 40, "titulo": "Suelta brazos", "titulo_en": "Drop arms", "descripcion": "Deja colgar tus brazos con total flojedad a los lados de tu cuerpo en tu sala. Sacúdelos de forma muy suave para eliminar cualquier rastro de pesadez acumulada.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}},
  {"id": 41, "titulo": "Contacto ropa", "titulo_en": "Clothing contact", "descripcion": "Cierra tus ojos un instante en tu asiento. Intenta notar la sensación sutil y el peso suave de la ropa descansando sobre la piel de tus hombros y tus brazos.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}},
  {"id": 42, "titulo": "Aire profundo", "titulo_en": "Deep air", "descripcion": "Toma aire despacio inflando tu vientre en tu espacio seguro, mantén el aire guardado por tres segundos y luego suéltalo muy suavemente por la boca con calma.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
  {"id": 43, "titulo": "Rotación hombros", "titulo_en": "Shoulder rotation", "descripcion": "Sube tus hombros despacio como si quisieras tocar tus orejas, mantén la fuerza un momento y déjalos caer de golpe para soltar la carga del día en tu casa.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
  {"id": 44, "titulo": "Escucha silencio", "titulo_en": "Listen to silence", "descripcion": "Quédate en completa calma por unos momentos en tu habitación e intenta escuchar el pequeño espacio de silencio que ocurre entre cada respiración natural en paz.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}},
  {"id": 45, "titulo": "Mirada techo", "titulo_en": "Ceiling gaze", "descripcion": "Mira hacia arriba en dirección al techo con suavidad en tu asiento. Estira tu cuello con total comodidad sin levantar ni mover tus hombros para nada.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}},
  {"id": 46, "titulo": "Siente base", "titulo_en": "Feel the base", "descripcion": "Presta atención a la parte de atrás de tus piernas ahora mismo. Nota el contacto firme y seguro que hacen contra el asiento de tu silla en tu comedor.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}},
  {"id": 48, "titulo": "Limpieza mental", "titulo_en": "Mental cleansing", "descripcion": "Imagina que al soltar el aire sacas de tu cuerpo cualquier preocupación aburrida y pesada en tu hogar, dejándola fuera de ti por completo en este segundo.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
  {"id": 49, "titulo": "Toca mesa", "titulo_en": "Touch the table", "descripcion": "Apoya las palmas de tus manos abiertas sobre la mesa. Siente la firmeza del mueble de tu casa y conéctate con esa agradable sensación de estabilidad.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
  {"id": 50, "titulo": "Presencia total", "titulo_en": "Total presence", "descripcion": "Recuerda que estás aquí en este instante, estás completamente a salvo en el cobijo de tu hogar y tienes el control absoluto de tu tranquilidad.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
  {"id": 51, "titulo": "Canta una melodía", "titulo_en": "Sing a melody", "descripcion": "Tararea tu canción favorita de forma muy suave y bajita en tu habitación. Deja de pensar en tus tareas y simplemente disfruta de la música en paz.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
  {"id": 52, "titulo": "Escribe 3 deseos", "titulo_en": "Write 3 wishes", "descripcion": "Toma un papel blanco en tu escritorio y escribe tres cosas sencillas y bonitas que te gustaría cumplir o disfrutar durante las horas de hoy con calma.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
  {"id": 53, "titulo": "Paseo por el pasillo", "titulo_en": "Hallway stroll", "descripcion": "Camina lentamente y con pasos muy suaves a lo largo del pasillo de tu casa, prestando atención a cómo apoyas cada pie al andar.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
  {"id": 54, "titulo": "Mira una planta", "titulo_en": "Look at a plant", "descripcion": "Busca una planta o una hojita verde que tengas cerca en tu sala. Observa sus colores y sus formas detalladamente durante un minuto en silencio.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
  {"id": 55, "titulo": "Dibuja un círculo", "titulo_en": "Draw a circle", "descripcion": "Toma un lápiz y dibuja círculos redondos en una hoja de papel de forma muy tranquila, concentrándote solo en el trazo de tu mano en casa.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
  {"id": 57, "titulo": "Abre un libro al azar", "titulo_en": "Open a book at random", "descripcion": "Toma un libro que tengas cerca en tu estante, abre una página cualquiera sin mirar y lee con atención la primera frase que encuentren tus ojos.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}},
  {"id": 58, "titulo": "Escucha la lluvia", "titulo_en": "Listen to the rain", "descripcion": "Abre tu ventana con cuidado y escucha el sonido tranquilo de las gotas al caer contra el suelo o las superficies por un momento en paz.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}},
  {"id": 59, "titulo": "Baila sin música", "titulo_en": "Dance without music", "descripcion": "Ponte de pie en tu habitación y mueve tu cuerpo libremente durante un minuto completo. Hazlo con alegría y soltura, como si nadie te estuviera viendo.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}},
  {"id": 60, "titulo": "Bebe una infusión", "titulo_en": "Drink a herbal tea", "descripcion": "Prepara una tacita de té o una infusión caliente en tu cocina. Dale pequeños sorbos muy despacio, sintiendo el calorcito reconfortante que entra a tu cuerpo.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}},
  {"id": 61, "titulo": "Mira tus manos", "titulo_en": "Look at your hands", "descripcion": "Extiende tus manos frente a ti en tu asiento. Observa detenidamente cada una de las líneas, los dedos y los pequeños detalles de tu piel humana.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}},
  {"id": 62, "titulo": "Imagina un paisaje", "titulo_en": "Imagine a landscape", "descripcion": "Cierra tus ojos suavemente en tu sofá. Imagina que estás caminando por tu lugar de la naturaleza favorito, como un bosque o una playa tranquila hoy.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}},
  {"id": 63, "titulo": "Estira la espalda", "titulo_en": "Stretch your back", "descripcion": "Siéntate en el suelo de tu sala con tus piernas bien estiradas hacia el frente. Lleva tus manos despacio hacia adelante e intenta tocar tus pies.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
  {"id": 64, "titulo": "Respira por la nariz", "titulo_en": "Breathe through your nose", "descripcion": "Toma aire de forma muy profunda y lenta utilizando únicamente tu nariz en tu silla. Siente cómo entra el aire fresco y hazlo cinco veces seguidas para darte calma.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
  {"id": 65, "titulo": "Juego de sombras", "titulo_en": "Shadow play", "descripcion": "Enciende una lámpara pequeña frente a una pared limpia de tu habitación. Usa tus manos y tus dedos para inventar formas divertidas de animalitos usando las sombras de la luz.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}},
  {"id": 66, "titulo": "Un abrazo imaginario", "titulo_en": "An imaginary hug", "descripcion": "Cruza tus brazos sobre tu pecho en tu sofá y apriétate a ti mismo con fuerza. Imagina con mucho cariño que estás recibiendo un lindo abrazo de un ser muy querido.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}},
  {"id": 67, "titulo": "Encuentra un objeto azul", "titulo_en": "Find a blue object", "descripcion": "Mira a tu alrededor rápidamente dentro de tu sala. Intenta descubrir cinco objetos diferentes que sean de color azul para entrenar tu atención con total tranquilidad hoy.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
  {"id": 69, "titulo": "Observa el cielo", "titulo_en": "Observe the sky", "descripcion": "Asómate a la ventana de tu cuarto un momento. Levanta la mirada con calma hacia el horizonte exterior y quédate observando el cielo despejado durante un minuto entero.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
  {"id": 70, "titulo": "Masaje facial", "titulo_en": "Facial massage", "descripcion": "Usa las yemas de tus dedos para darte un masaje muy suave en el rostro frente al espejo. Dibuja círculos tranquilos por tu frente, tus mejillas y tu mandíbula en silencio.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
  {"id": 71, "titulo": "Cierra los ojos y escucha", "titulo_en": "Close your eyes and listen", "descripcion": "Toma una postura muy cómoda en tu asiento de descanso y cierra los ojos con suavidad. Presta mucha atención e intenta identificar tres sonidos diferentes dentro de casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
  {"id": 72, "titulo": "Tensa y relaja los pies", "titulo_en": "Tense and relax your feet", "descripcion": "Aprieta con fuerza los dedos de tus dos pies hacia adentro en tu alfombra durante cinco segundos enteros para acumular tensión. Después, suéltalos de golpe para que descansen.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
  {"id": 74, "titulo": "Olor consciente", "titulo_en": "Mindful scent", "descripcion": "Busca algo en tu alacena que tenga un aroma agradable que te guste mucho, como un granito de café o una especia. Acércalo a tu nariz y concéntrate en su olor.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
  {"id": 75, "titulo": "Copia un dibujo simple", "titulo_en": "Copy a simple drawing", "descripcion": "Busca un dibujo pequeño y muy sencillo en una revista o un libro de tu mesa. Toma un lápiz e intenta copiar sus líneas en una hoja de papel de forma tranquila.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
  {"id": 76, "titulo": "Encuentra tres objetos rojos", "titulo_en": "Find three red objects", "descripcion": "Mira a tu alrededor velozmente dentro de tu habitación actual. Intenta descubrir tres objetos diferentes que sean de color rojo para activar tu enfoque consciente en total calma.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
  {"id": 78, "titulo": "Escribe una palabra bonita", "titulo_en": "Write a beautiful word", "descripcion": "Toma un bolígrafo y escribe una palabra hermosa que te guste mucho en un papel limpio, como Paz o Calma. Dibuja letras grandes y ordenadas en tu escritorio.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 100, "contemplacion": 60}},
  {"id": 79, "titulo": "Masaje en las manos", "titulo_en": "Hand massage", "descripcion": "Usa el dedo pulgar de tu mano derecha para dar un masaje suave en la palma de tu mano izquierda. Dibuja círculos lentos por toda la piel con mucha ternura en tu asiento.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 30, "contemplacion": 60}},
  {"id": 81, "titulo": "Estiramiento de cuello lateral", "titulo_en": "Lateral neck stretch", "descripcion": "Inclina tu cabeza despacio llevando tu oreja derecha hacia el hombro derecho sin levantar los hombros. Mantén la postura tres segundos y cambia de lado con suavidad en tu sofá.", "vector_necesidades": {"movimiento": 85, "salud": 90, "descanso": 80, "silencio": 70, "organizacion": 20}},
  {"id": 82, "titulo": "Observa una sombra", "titulo_en": "Observe a shadow", "descripcion": "Busca una sombra proyectada en el piso o en la pared de tu habitación actual. Observa detalladamente sus bordes oscuros y sus formas en silencio por un minuto entero.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 50, "descanso": 75, "naturaleza": 20}},
  {"id": 83, "titulo": "Siente tus latidos", "titulo_en": "Feel your heartbeat", "descripcion": "Coloca dos de tus dedos suavemente sobre tu muñeca izquierda o en tu cuello en tu rincón cómodo. Quédate quieto sintiendo el latido constante y fuerte de tu pulso.", "vector_necesidades": {"contemplacion": 100, "silencio": 95, "descanso": 90, "salud": 90, "movimiento": 10}},
  {"id": 159, "titulo": "EL RETO DE LA RESPIRACIÓN", "titulo_en": "THE BREATHING CHALLENGE", "descripcion": "Quédate sentado en una postura muy cómoda en tu sala. Haz cinco respiraciones profundas y lentas por la nariz, sintiendo cómo entra el aire puro a tu cuerpo. Nada más.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
  {"id": 160, "titulo": "EL RETO DEL DESCANSO VISUAL", "titulo_en": "THE VISUAL REST CHALLENGE", "descripcion": "Busca un punto u objeto que esté muy lejano a ti a través de la ventana de tu cuarto. Quédate mirando ese lugar fijamente durante dos minutos para descansar tus ojos de las pantallas.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}} 
   ],
    "CASA_EN": [
  {"id": 1, "titulo": "Break the autopilot", "titulo_en": "Break the autopilot", "descripcion": "Take a brief moment to scan your body completely. Locate the exact weight built up on your upper back and observe it with absolute calm. Feel your heartbeat and remember that you are alive in this peaceful second.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
  {"id": 2, "titulo": "Total disconnection", "titulo_en": "Total disconnection", "descripcion": "Feel the shape of the chair beneath your body right now. The firm floor supports your entire weight completely for free and safely. Do not fight it, let yourself fall into total calm at this instant.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
  {"id": 3, "titulo": "Screen isolation", "titulo_en": "Screen isolation", "descripcion": "Turn your cell phone face down with total peace of mind at this instant. Stare closely at a corner of the ceiling for thirty straight seconds and allow your mind to break the loop of digital rush now.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
  {"id": 4, "titulo": "Let go of the load", "titulo_en": "Let go of the load", "descripcion": "Feel your shoulders completely free and lightweight right now. Imagine that you no longer carry that heavy invisible backpack on you. Let go of all accumulated mental stiffness and breathe with complete ease.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
  {"id": 5, "titulo": "The water reset", "titulo_en": "The water reset", "descripcion": "Take a small, unhurried sip of cold water at this moment. Feel the exact path of the fresh liquid passing down your throat. It is pure life entering to fully renew your entire organism completely.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
  {"id": 7, "titulo": "Window breeze", "titulo_en": "Window breeze", "descripcion": "Open your room's window completely right now. Let the fresh outdoor air gently touch your face during this count. Feel the outside world and clear your mind from all the confinement of routine.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
  {"id": 8, "titulo": "Energy rotation", "titulo_en": "Energy rotation", "descripcion": "Gently rotate your wrists and your ankles in slow circles. Remember that this body belongs completely to you and you govern this engine. Feel how natural energy begins to flow freely through your entire being.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
  {"id": 9, "titulo": "Anchor to the present", "titulo_en": "Anchor to the present", "descripcion": "Close your eyes in complete acoustic silence right now. Think closely about one good and beautiful thing you have in your life today. Say it with strength in your mind in absolute calm.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
  {"id": 11, "titulo": "Feet on the ground", "titulo_en": "Feet on the ground", "descripcion": "Take off your shoes right now, without any rush. Place the soles of your feet directly on the cool floor of the room. Feel the firmness of the ground beneath you and connect.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
  {"id": 12, "titulo": "Stretch to the sky", "titulo_en": "Stretch to the sky", "descripcion": "Stretch your arm firmly upward and try to touch the ceiling with your fingertips. Hold that muscle tension for an exact second during this count. Now release everything all at once dynamically.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
  {"id": 14, "titulo": "Straight spine", "titulo_en": "Straight spine", "descripcion": "Straighten your back completely at this very moment. An invisible string gently pulls your head toward the sky. Feel how your chest opens freely and inhabit your deep and peaceful breathing now.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}},
  {"id": 15, "titulo": "Contacto frío", "titulo_en": "Cold touch", "descripcion": "Look for an object or surface that is cold to the touch in your room and place your hand on it. Feel the real temperature for a few seconds. This helps calm your mind immediately at home.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}},
  {"id": 16, "titulo": "Ventilación total", "titulo_en": "Total ventilation", "descripcion": "Open the nearest window in your current room. Let the new air enter and roll through the entire available space. Breathe slowly and notice how your home's environment changes peacefully.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}},
  {"id": 17, "titulo": "Sacudida de estrés", "titulo_en": "Stress shake", "descripcion": "Stand up carefully in your safe space. Shake your hands and legs gently as if you were shaking off small drops of water. Do this cheerful movement for ten seconds at home.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}},
  {"id": 18, "titulo": "Distant gaze", "titulo_en": "Distant gaze", "descripcion": "Look through the window and find the object or house that is furthest away from you. Keep observing that fixed point to rest your eyes from screens in complete and deep peace.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}},
  {"id": 19, "titulo": "Memoria feliz", "titulo_en": "Happy memory", "descripcion": "Close your eyes gently for a moment in your cozy corner. Bring to your mind a beautiful and innocent memory from when you were a child. Feel the peace that pretty day gives you.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}},
  {"id": 20, "titulo": "Sonrisa forzada", "titulo_en": "Forced smile", "descripcion": "Draw a big smile on your face and keep it fixed for fifteen full seconds at this moment. This small gesture lets your mind know it is time to be in total well-being.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}},
  {"id": 21, "titulo": "Agradecimiento", "titulo_en": "Gratitude", "descripcion": "Close your eyes in complete silence in your living room. Think carefully about a single good and beautiful thing that has happened to you this week and give thanks in your calm mind.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}},
  {"id": 22, "titulo": "Relaxa ojos", "titulo_en": "Eye relax", "descripcion": "Rub the palms of your hands to warm the skin immediately. Place them gently over your closed eyes and enjoy a full minute of darkness and total rest inside your quiet room.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}},
  {"id": 23, "titulo": "Ritmo cardíaco", "titulo_en": "Heart rate", "descripcion": "Place your right hand in the center of your chest peacefully. Feel the steady and peaceful beat of your heart. Remember that this is the beautiful engine of your life now.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}},
  {"id": 24, "titulo": "Suelta cuello", "titulo_en": "Neck release", "descripcion": "Move your head drawing very slow and gentle circles in the air. Feel how all the tension built up in your neck from looking at the phone goes away inside your home.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}},
  {"id": 25, "titulo": "Palm exercise", "titulo_en": "Palm exercise", "descripcion": "Rub your hands with energy until you feel the warmth on your skin. Immediately place your palms on your shoulders to give yourself a comforting hug at this exact present moment.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}},
  {"id": 26, "titulo": "Distant sounds", "titulo_en": "Distant sounds", "descripcion": "Stay still for a few moments in your living room and pay close attention to your surroundings. Try to identify the furthest sound that can be heard outside your house in this peaceful instant.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}},
  {"id": 27, "titulo": "Lateral stretch", "titulo_en": "Lateral stretch", "descripcion": "Tilt your body very gently to the right side and then to the left with complete calm. Feel how your waist stretches with total comfort and muscular lightness inside your room.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
  {"id": 28, "titulo": "The empty glass", "titulo_en": "The empty glass", "descripcion": "Look for a clear glass in your kitchen. Observe its shape and how the light enters it for one full minute. Notice the beautiful reflections in absolute silence and clear your mind.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}},
  {"id": 29, "titulo": "Jaw release", "titulo_en": "Jaw release", "descripcion": "Open your mouth wide carefully in your cozy corner. Move your jaw slowly from one side to the other. Feel how all the stiffness and accumulated tension leaves your face.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}},
  {"id": 30, "titulo": "Slow steps", "titulo_en": "Slow steps", "descripcion": "Stand up gently in your safe space. Take ten very slow and quiet steps inside your current room. Feel the full support of each foot as you walk with calm.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}},
  {"id": 31, "titulo": "Gentle massage", "titulo_en": "Gentle massage", "descripcion": "Place your fingertips on your temples right now. Draw very slow and tender circles without pressing hard. Feel the immediate relief in your head and relax your thoughts.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
  {"id": 32, "titulo": "Air awareness", "titulo_en": "Air awareness", "descripcion": "Pay attention to your nose at this moment. Feel the fresh air coming in as you breathe in and the warm air coming out as you let it go. Do it naturally in your space.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}},
  {"id": 33, "titulo": "Firm back", "titulo_en": "Firm back", "descripcion": "Bring your shoulders gently back and open your chest lightly at this instant. Feel how your body recovers its natural, straight and comfortable posture inside your house.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}},
  {"id": 34, "titulo": "Total support", "titulo_en": "Total support", "descripcion": "Take a seat quietly and relax your back. Feel how the chair holds all the weight of your body with total safety. Release your muscles now and truly rest.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}},
  {"id": 35, "titulo": "Countdown", "titulo_en": "Countdown", "descripcion": "Count the numbers backwards, starting from twenty until you reach one. Do it very slowly in your mind to calm all your thoughts and find absolute peace.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}},
  {"id": 36, "titulo": "Touch texture", "titulo_en": "Touch texture", "descripcion": "Pass your fingertips over a real surface nearby, such as a wooden table or a piece of clean cloth. Notice its texture with absolute calm.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}},
  {"id": 37, "titulo": "Stretch fingers", "titulo_en": "Stretch fingers", "descripcion": "Separate and stretch your fingers as much as you can for five whole seconds with energy. Afterwards, relax them completely so they can rest from screens at this instant.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
  {"id": 38, "titulo": "Internal sound", "titulo_en": "Internal sound", "descripcion": "Stay in silence in your cozy corner and listen to the soft sound of your own breathing. Do not try to force it or change it, just notice how your body breathes on its own.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}},
  {"id": 39, "titulo": "Fixed gaze", "titulo_en": "Fixed gaze", "descripcion": "Look for a small spot or a mark on the wall in front of you. Keep looking at that fixed place peacefully, allowing your eyes to focus far away from the screens.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}},
  {"id": 40, "titulo": "Drop arms", "titulo_en": "Drop arms", "descripcion": "Let your arms hang completely loose at the sides of your body in your living room. Shake them very gently to remove any trace of accumulated heaviness.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}},
  {"id": 41, "titulo": "Clothing contact", "titulo_en": "Clothing contact", "descripcion": "Close your eyes for a moment in your seat. Try to notice the subtle sensation and smooth weight of your clothes resting on the skin of your shoulders and arms.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}},
  {"id": 42, "titulo": "Deep air", "titulo_en": "Deep air", "descripcion": "Breathe in slowly inflating your belly in your safe space, hold the air for three seconds, and then release it very gently through your mouth with calm.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
  {"id": 43, "titulo": "Shoulder rotation", "titulo_en": "Shoulder rotation", "descripcion": "Raise your shoulders slowly as if you wanted to touch your ears, hold the strength for a moment, and let them drop suddenly to release the day's load in your house.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
  {"id": 44, "titulo": "Listen to silence", "titulo_en": "Listen to silence", "descripcion": "Stay in complete calm for a few moments in your room and try to listen to the small space of silence that happens between each natural breath in peace.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}},
  {"id": 45, "titulo": "Ceiling gaze", "titulo_en": "Ceiling gaze", "descripcion": "Look up toward the ceiling gently in your seat. Stretch your neck with total comfort without lifting or moving your shoulders at all.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}},
  {"id": 46, "titulo": "Feel the base", "titulo_en": "Feel the base", "descripcion": "Pay attention to the back of your legs right now. Notice the firm and secure contact they make against the seat of your chair in your dining room.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}},
  {"id": 48, "titulo": "Mental cleansing", "titulo_en": "Mental cleansing", "descripcion": "Imagine that as you release your breath you take out from your body any boring and heavy worry in your home, leaving it completely outside of you in this second.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
  {"id": 49, "titulo": "Touch the table", "titulo_en": "Touch the table", "descripcion": "Place the palms of your open hands on the table. Feel the firmness of the piece of furniture of your house and connect with that feeling of stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
  {"id": 50, "titulo": "Total presence", "titulo_en": "Total presence", "descripcion": "Remember that you are here at this moment, you are completely safe in the shelter of your home, and you have control of your tranquility.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
  {"id": 51, "titulo": "Sing a melody", "titulo_en": "Sing a melody", "descripcion": "Hum your favorite song very softly and quietly in your room. Stop thinking about your tasks and simply enjoy the music in absolute peace.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
  {"id": 52, "titulo": "Write 3 wishes", "titulo_en": "Write 3 wishes", "descripcion": "Take a white piece of paper at your desk and write down three simple and beautiful things you would like to fulfill or enjoy during the hours of today calmly.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
  {"id": 53, "titulo": "Hallway stroll", "titulo_en": "Hallway stroll", "descripcion": "Walk slowly and with very soft steps along the hallway of your house, paying close attention to how you support each foot as you move along.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
  {"id": 54, "titulo": "Look at a plant", "titulo_en": "Look at a plant", "descripcion": "Look for a plant or a green leaf nearby in your living room. Observe its colors and shapes in close detail for one minute in silence.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
  {"id": 55, "titulo": "Draw a circle", "titulo_en": "Draw a circle", "descripcion": "Take a pencil and draw round circles on a sheet of paper very quietly, focusing only on the steady stroke of your hand inside your house.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
  {"id": 57, "titulo": "Open a book at random", "titulo_en": "Open a book at random", "descripcion": "Take a book nearby from your shelf, open any page without looking, and read carefully the first phrase your eyes find right away.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}},
  {"id": 58, "titulo": "Listen to the rain", "titulo_en": "Listen to the rain", "descripcion": "Open your window carefully and listen to the peaceful sound of the drops falling against the ground or surfaces for a moment in complete quietness.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}},
  {"id": 59, "titulo": "Dance without music", "titulo_en": "Dance without music", "descripcion": "Stand up in your room and move your body freely for one full minute. Do it with joy and ease, as if nobody were watching you.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}},
  {"id": 60, "titulo": "Drink a herbal tea", "titulo_en": "Drink a herbal tea", "descripcion": "Prepare a cup of tea or a hot herbal infusion in your kitchen. Take small sips very slowly, feeling the comforting warmth entering your body.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}},
  {"id": 61, "titulo": "Look at your hands", "titulo_en": "Look at your hands", "descripcion": "Extend your hands in front of you in your seat. Closely observe each of the lines, fingers, and tiny details of your human skin.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}},
  {"id": 62, "titulo": "Imagine a landscape", "titulo_en": "Imagine a landscape", "descripcion": "Close your eyes gently on your couch. Imagine that you are walking through your favorite nature spot, like a forest or a quiet beach today.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}},
  {"id": 63, "titulo": "Stretch your back", "titulo_en": "Stretch your back", "descripcion": "Sit on the floor of your living room with your legs well stretched forward. Slowly bring your hands forward and try to touch your feet.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
  {"id": 64, "titulo": "Breathe through your nose", "titulo_en": "Breathe through your nose", "descripcion": "Breathe in very deeply and slowly using only your nose while sitting on your chair. Feel how the fresh air comes in and do it five times in a row to calm yourself.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
  {"id": 65, "titulo": "Shadow play", "titulo_en": "Shadow play", "descripcion": "Turn on a small lamp in front of a clean wall in your room. Use your hands and fingers to make up fun little animal shapes using the light shadows beautifully.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}},
  {"id": 66, "titulo": "An imaginary hug", "titulo_en": "An imaginary hug", "descripcion": "Cross your arms over your chest while sitting on your couch and squeeze yourself tightly. Imagine with much affection that you are receiving a nice hug from a loved one.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}},
  {"id": 67, "titulo": "Find a blue object", "titulo_en": "Find a blue object", "descripcion": "Look around you quickly inside your living room. Try to discover five different objects that are blue to train your mindful attention with complete peace of mind today.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
  {"id": 69, "titulo": "Observe the sky", "titulo_en": "Observe the sky", "descripcion": "Look out the window of your room for a moment. Calmly look up toward the outer horizon and stay observing the clear sky for one full minute in peace.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
  {"id": 70, "titulo": "Facial massage", "titulo_en": "Facial massage", "descripcion": "Use your fingertips to give yourself a very gentle face massage in front of your mirror. Draw peaceful circles across your forehead, cheeks, and jaw in complete silence.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
  {"id": 71, "titulo": "Close your eyes and listen", "titulo_en": "Close your eyes and listen", "descripcion": "Take a very comfortable position in your resting seat and close your eyes gently. Pay close attention and try to identify three different sounds happening inside the house.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
  {"id": 72, "titulo": "Tense and relax your feet", "titulo_en": "Tense and relax your feet", "descripcion": "Tightly squeeze the toes of both your feet inward on your rug for five full seconds to build up tension. Afterwards, release them all at once to let them rest.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
  {"id": 74, "titulo": "Mindful scent", "titulo_en": "Mindful scent", "descripcion": "Look for something in your pantry that has a pleasant aroma you like a lot, such as a coffee bean or a spice. Bring it close to your nose and focus.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
  {"id": 75, "titulo": "Copy a simple drawing", "titulo_en": "Copy a simple drawing", "descripcion": "Look for a small and very simple drawing in a magazine or a book on your table. Take a pencil and try to copy its lines on paper peacefully.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
  {"id": 76, "titulo_en": "Find three red objects", "descripcion_en": "Look around you quickly inside your current room. Try to discover three different objects that are red to activate your mindful focus in total calm today.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
  {"id": 78, "titulo_en": "Write a beautiful word", "descripcion_en": "Take a pen and write a beautiful word you like a lot on a clean paper, such as Peace or Calm. Draw large and neat letters at your desk.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 100, "contemplacion": 60}},
  {"id": 79, "titulo_en": "Hand massage", "descripcion_en": "Use the thumb of your right hand to give a gentle massage to the palm of your left hand. Draw slow circles across the entire skin with great tenderness in your seat.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 30, "contemplacion": 60}},
  {"id": 81, "titulo_en": "Lateral neck stretch", "descripcion_en": "Tilt your head slowly bringing your right ear toward your right shoulder without lifting your shoulders. Hold the posture for three seconds and switch sides gently on your couch.", "vector_necesidades": {"movimiento": 85, "salud": 90, "descanso": 80, "silencio": 70, "organizacion": 20}},
  {"id": 82, "titulo_en": "Observe a shadow", "descripcion_en": "Look for a shadow projected on the floor or wall of your current room. Closely observe its dark edges and shapes in absolute silence for one full minute.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 50, "descanso": 75, "naturaleza": 20}},
  {"id": 83, "titulo_en": "Feel your heartbeat", "descripcion_en": "Place two of your fingers gently on your left wrist or on your neck in your cozy corner. Stay still feeling the steady and strong beat of your biological pulse.", "vector_necesidades": {"contemplacion": 100, "silencio": 95, "descanso": 90, "salud": 90, "movimiento": 10}},
  {"id": 159, "titulo_en": "THE BREATHING CHALLENGE", "descripcion_en": "Stay seated in a very comfortable posture in your living room. Take five deep and slow breaths through your nose, feeling how the pure air enters your body. Nothing more.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
  {"id": 160, "titulo_en": "THE VISUAL REST CHALLENGE", "descripcion_en": "Look for a spot or an object that is very far away from you through your bedroom window. Keep your eyes on that place fixedly for two minutes to rest your eyes from screens completely.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}} 
    ],
"SALIR": {
   "agotado": [
         {"id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade", "porque": "Hoy vas a buscar un gran árbol frondoso en un parque verde cercano. Si tu mente se encuentra cansada de mirar tantas pantallas y tu cuerpo necesita desconectarse de la prisa digital, camina despacio y acércate con calma a su tronco. Toca su corteza rugosa y quédate disfrutando de su sombra fresca en completo silencio. Levántate ahora mismo, siente el aire fresco y permítete contemplar la naturaleza para romper la rutina y descansar de verdad. Tu respiración se equilibra en este refugio de paz.", "porque_en": "Today you will look for a large leafy tree in a green park nearby. If your mind feels tired from looking at so many screens and your body needs to disconnect from the digital rush, walk slowly and approach its trunk calmly. Touch its rough bark and stay enjoying its cool shade in complete silence. Get up right now, feel the fresh air, and allow yourself to contemplate nature to break the routine and truly rest. Your breathing finds its balance in this peaceful refuge.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade", "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85} },
{"id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe", "porque": "Hoy vas a visitar una cafetería local pacífica y tranquila. Si tu mente te exige un pequeño respiro para evitar los ruidos molestos y poder encontrar un dulce momento de paz, dirígete allí sin prisa. Pide tu bebida favorita, toma asiento y dedícate a observar el entorno con absoluta calma, manteniendo el teléfono guardado. Levántate ahora mismo, regálate este descanso mental y disfruta el silencio para romper el piloto automático diario y recargar energías. Siente el calor de tu taza y conecta con el presente.", "porque_en": "Today you will visit a peaceful and quiet local cafe. If your mind demands a small break to avoid annoying noises and find a sweet moment of peace, head there without any rush. Order your favorite drink, take a seat, and dedicate yourself to observing your surroundings with absolute calm, keeping your phone away. Get up right now, grant yourself this mental rest, and enjoy the silence to break the daily automatic pilot and recharge. Feel the warmth of your cup and connect with the present.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Establecimiento local pacífico.", "donde_en": "Peaceful local establishment.", "gps": "quiet cafe", "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70} },
{"id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden", "porque": "Hoy vas a explorar un hermoso paraje botánico público. Si sientes el cerebro un poco agotado y necesitas reconectarte con las plantas reales para respirar aire puro, camina de forma muy pausada y sin ninguna prisa por los senderos verdes. Quédate contemplando la enorme variedad de hojas a tu alrededor y respira hondo. Levántate ahora mismo, abraza esta tregua natural and permite que tu mente descanse de las obligaciones diarias en este oasis tranquilo. Siente el suelo firme bajo tus pies y vive este instante.", "porque_en": "Today you will explore a beautiful public botanical site. If you feel your brain is a bit exhausted and you need to reconnect with real plants to breathe pure air, stroll very slowly and without any rush through the green paths. Keep contemplating the massive variety of leaves around you and take a deep breath. Get up right now, embrace this natural truce, and allow your mind to rest from daily obligations in this quiet oasis. Feel the firm ground beneath your feet and live this instant.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Paraje botánico público.", "donde_en": "Public botanical site.", "gps": "botanical garden", "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90} },
 
         {"id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook", "porque": "Hoy vas a buscar un lugar alto o un punto despejado en la ciudad. Si tu mente necesita una nueva perspectiva, eleva tu mirada hacia el frente para romper con el aburrimiento visual de todos los días. Quédate observando fijamente la línea del horizonte y siente la inmensidad del entorno con absoluta tranquilidad. Levántate ahora mismo, dirígete a un mirador público y permítete contemplar el paisaje para romper la rutina diaria. Siente el viento fresco en tu rostro mientras recuperas tu centro en total paz y libertad.", "porque_en": "Today you will find a high spot or a clear point in the city. If your mind needs a new perspective, elevate your gaze to break away from the everyday visual routine. Keep observing the horizon and feel the vastness of your surroundings in total peace. Get up right now, head to a public overlook, and allow yourself to contemplate the scenery to break your routine. Feel the fresh air on your face while you recover your core in total quietness and calm.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook", "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95} },
  {"id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class", "porque": "Hoy vas a buscar una sesión guiada o un momento tranquilo en un centro de yoga o meditación. Si sientes la mente muy sobrecargada por las tareas, te vendrá excelente encontrar un rincón de calma interna para regular tu cuerpo. Concéntrate únicamente en la entrada y salida del aire por tu nariz y suelta por completo las preocupaciones del día. Levántate ahora mismo, regálate este descanso mental profundo and habita el silencio absoluto para romper la rutina. Siente los latidos de tu corazón y relájate de verdad.", "porque_en": "Today you will find a guided session or a quiet moment in a yoga or meditation center. If you feel your mind is heavily overloaded with tasks, it will do you excellent to find a quiet space for inner calm to regulate your body. Concentrate only on the air entering and leaving your nose and let go of your worries completely. Get up right now, grant yourself this deep mental rest, and inhabit absolute silence to break the routine. Feel your heartbeat and truly relax into this space.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class", "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90} },
  {"id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing", "porque": "Hoy vas a buscar un espacio abierto al aire libre en un parque o campo abierto. Si tus pensamientos avanzan con mucha agitación, enfocar la mirada en la inmensidad del cielo te ayudará a dejar fluir tus ideas con total libertad. Recuéstate cómodamente sobre el pasto o en una silla y observa detalladamente las hermosas formas en el firmamento. Levántate ahora mismo, regálate este descanso contemplativo y respira aire puro para romper la rutina y serenar tu cuerpo. Siente la inmensidad del cielo rodeándote.", "porque_en": "Today you will find an open space outdoors in a park or open field. If your thoughts are racing with too much excitement, focusing your gaze on the vastness of the sky will help you let your ideas flow with total freedom. Lie down comfortably on the grass or in a chair and closely observe the shapes in the sky. Get up right now, grant yourself this contemplative rest, and breathe fresh air to break the routine and calm your body. Feel the vastness of the sky surrounding you.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing", "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85} },

          {"id": 355, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Hoy vas a pedir un viaje muy corto hacia la plaza o parque verde más cercano usando tu aplicación de transporte favorita. Si sientes un cansancio muy grande en tus ojos y tu cuerpo debido a la pesadez de manejar en el tráfico ruidoso de la ciudad, esta pausa pasiva te protegerá. Cuando estés adentro del auto, guarda tu teléfono en el bolsillo. Cierra tus ojos por un minuto completo, apoya tus manos sobre las piernas y respira muy despacio. Siente el movimiento suave del vehículo mientras descansas tu mente de forma segura. El recorrido empieza ahora.", "porque_en": "Today you will request a very short trip to the nearest public square or green park using your favorite rideshare app. If your eyes and body feel very tired from the heaviness of driving through the noisy city traffic, this passive break will protect you. Once inside the car, put your phone away in your pocket. Close your eyes for one whole minute, rest your hands on your lap, and breathe very slowly. Feel the gentle motion of the vehicle while resting your mind safely. Your journey begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cabina de transporte, parada o asiento de pasajero.", "donde_en": "Transit vehicle cabin, stop, or passenger seat.", "gps": "quiet public square", "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 15, "contemplacion": 85, "esperanza": 80, "salud": 80, "aire_fresco": 60} },
  {"id": 356, "titulo": "Módulo de Cambio Frecuencial", "titulo_en": "Frequency Shift Module", "porque": "Hoy vas a abrir tu aplicación de música con calma en tu espacio de descanso o vehículo. Si tu mente se encuentra muy llena de pensamientos y tus oídos están cansados por culpa de los ruidos fuertes y las pantallas, busca sonidos de la naturaleza como el canto de los pajaritos o la lluvia cayendo. Colócate tus auriculares, apoya tu cabeza hacia atrás y toma aire de forma profunda para que tu mente se sienta tranquila. Levántate ahora mismo, regálate este quiebre acústico y permite que tu respiración recupere su curso natural en paz.", "porque_en": "Today you will open your music app calmly in your resting space or vehicle. If your mind feels overloaded with thoughts and your ears are tired from loud noises and looking at screens, search for peaceful nature sounds like birds singing or gentle rain falling. Put on your headphones, lean your head back, and take a deep breath to make your mind feel completely quiet. Get up right now, grant yourself this acoustic break, and allow your breathing to find its natural course in peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Tu espacio de descanso, oficina vacía o vehículo.", "donde_en": "Your resting space, empty office, or vehicle.", "gps": "quiet open park", "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 65, "contemplacion": 90, "esperanza": 85, "salud": 80, "creatividad": 40} },
  {"id": 357, "titulo": "Mapeo de Flujos", "titulo_en": "Flow Mapping", "porque": "Hoy vas a caminar hacia la tienda o almacén más grande que esté cerca de ti. Si llevas mucho tiempo sentado en el mismo lugar y tu cuerpo necesita mover las piernas en un espacio grande para activar tu energía, camina a paso firme y tranquilo por los pasillos más largos sin ninguna prisa por comprar nada. Observa los objetos a tu alrededor y aprovecha este sitio fresco y techado para estirar tus extremidades. Levántate ahora mismo, rompe el piloto automático diario y activa tu musculatura de forma gratuita.", "porque_en": "Today you will walk to the largest store or warehouse club near you. If you have been sitting in the same spot for too long and your body needs to move your legs in a large space to boost your energy, walk steadily and peacefully through the longest aisles without any rush to buy anything. Look around at the items and use this cool, indoor space to stretch your limbs nicely. Get up right now, break the daily automatic pilot, and activate your body's circulation completely free.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Pasillos industriales de una gran tienda de tu Código Postal.", "donde_en": "Industrial aisles of a large warehouse store in your Zip Code.", "gps": "wholesale club or market", "vector_necesidades": {"movimiento": 85, "organizacion": 70, "contemplacion": 60, "comunidad": 50, "juego": 30, "descanso": 20, "silencio": 10} },

          {"id": 358, "titulo": "Oasis Burocrático", "titulo_en": "Bureaucratic Oasis", "porque": "Hoy vas a buscar la biblioteca pública más cercana en tu vecindario e ingresarás despacio y en completo silencio. Si sientes un cansancio muy grande en la mente debido a las esperas largas, las filas, los papeles o los letreros de la calle, toma asiento en una silla de la zona de lectura de inmediato. Disfruta de la tranquilidad absoluta del lugar y permite que tus ojos descansen por completo de las pantallas. Levántate ahora mismo, regálate este respiro intelectual y desconecta del ruido urbano. Tu mente recupera su claridad en este espacio sagrado.", "porque_en": "Today you will look for the nearest public library in your neighborhood and walk inside slowly and in complete silence. If you feel a lot of mental tiredness from long waits, paperwork, lines, or staring at bright street signs, take a seat on a chair in the reading room immediately. Enjoy the absolute quietness of the place and let your eyes rest completely from screens. Get up right now, grant yourself this intellectual break, and disconnect from the urban rush. Your mind recovers its clarity in this sacred space.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sala de lectura, biblioteca municipal o zona de estudio de USA.", "donde_en": "Reading room, municipal library, or USA study zone.", "gps": "public library", "vector_necesidades": {"aprendizaje": 100, "silencio": 100, "contemplacion": 90, "descanso": 85, "organizacion": 70, "salud": 80} },
  {"id": 201, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Hoy vas a abrir tu aplicación de transporte en el teléfono y pedirás un viaje muy corto hacia un rincón tranquilo de tu vecindario. Si sientes el cuerpo cansado y la mente muy pesada por culpa de estar manejando todo el día o moverte en medio del tráfico ruidoso, esta pausa pasiva te protegerá. Cuando subas al auto, guarda tu teléfono, cierra los ojos por un minuto entero y quédate descansando con tus manos apoyadas sobre tus rodillas. Siente el vaivén seguro del trayecto mientras el estrés se desvanece.", "porque_en": "Today you will open your rideshare application on your phone and request a very short trip to a quiet corner of your neighborhood. If your body feels tired and your mind is very heavy from driving all day or moving through noisy city traffic, this passive break will protect you. Once inside the car, put your phone away, close your eyes for a whole minute, and stay resting with your hands placed on your knees. Feel the safe movement of the ride as the entire stress fades away into the background.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cabina de transporte o asiento de pasajero.", "donde_en": "Rideshare cabin or passenger seat.", "gps": "quiet park bench", "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 10, "contemplacion": 80, "esperanza": 80, "naturaleza": 20, "aire_fresco": 50} },
  {"id": 202, "titulo": "Módulo Auditivo", "titulo_en": "Auditory Reset", "porque": "Hoy vas a abrir tu aplicación de música favorita en cualquier rincón cómodo o dentro de tu auto. Si tu mente se encuentra muy agotada por culpa de escuchar tantos ruidos molestos de la calle y mirar el brillo de las pantallas, busca sonidos de la lluvia cayendo o una melodía muy suave. Colócate tus auriculares, cierra tus ojos por un minuto entero y permite que los sonidos tranquilos se lleven todo el cansancio de tu cabeza. Levántate ahora mismo, abraza esta tregua acústica y siente la paz recuperando tu centro.", "porque_en": "Today you will open your favorite music app in any comfortable spot or inside your car. If your mind feels very exhausted from hearing so much annoying street noise and staring at bright screens, search for gentle rain sounds or a very soft melody. Put on your headphones, close your eyes for a whole minute, and let the peaceful sounds take away all the tiredness from your head. Get up right now, embrace this acoustic truce, and feel the gentle peace recovering your inner core completely.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cualquier rincón cómodo o dentro de tu auto.", "donde_en": "Any comfortable spot or inside your car.", "gps": "quiet library space", "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 60, "contemplacion": 90, "esperanza": 85, "creatividad": 40} },

         {"id": 203, "titulo": "Descompresión de Entorno", "titulo_en": "Environment Decompression", "porque": "Hoy vas a buscar un hotel que te quede cerca para caminar con total tranquilidad hacia su vestíbulo principal. Si sientes el aburrimiento de estar encerrado en el mismo lugar de siempre y tu cuerpo te pide cambiar a un espacio bonito y ordenado, toma asiento en un sillón cómodo de inmediato. Apoya tus pies firmes en el piso y descansa tu mirada contemplando un punto lejano por dos minutos enteros. Levántate ahora mismo, regálate este quiebre espacial y permite que tu respiración recupere su curso natural en paz. Tu mente se renueva en este entorno elegante.", "porque_en": "Today you will look for a hotel nearby to walk completely peacefully into its main lobby or lounge area. If you feel bored from being cooped up in the same old place and your body is asking to switch to a beautiful, orderly space, take a seat in a comfy chair immediately. Place your feet flat on the floor and rest your eyes by looking at a distant spot for two full minutes. Get up right now, grant yourself this spatial break, and allow your breathing to find its natural course in peace. Your mind completely renews in this elegant environment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Lobby o zona de descanso de un hotel local.", "donde_en": "Lobby or lounge area of a local hotel.", "gps": "hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 70, "esperanza": 80, "movimiento": 20} },
  {"id": 204, "titulo": "Sabotaje de Espera", "titulo_en": "Waiting Sabotage", "porque": "Hoy te dirigirás hacia el patio exterior o la zona de libros de una escuela o universidad cercana. Si tu mente lleva mucho tiempo atrapada en el teléfono mirando cosas vacías y necesitas alimentar tu imaginación con ideas nuevas, camina despacio y en absoluto silencio por sus senderos verdes. Respira el aire fresco, observa los árboles con total tranquilidad y desconéctate por completo de las pantallas. Levántate ahora mismo, regálate este respiro intelectual y rompe el piloto automático diario para reconectar con tu creatividad. El recorrido de bienestar empieza ya.", "porque_en": "Today you will head toward the outdoor courtyard or the book section of a nearby school or university. If your mind has been trapped looking at empty things on your phone for too long and you need to feed your imagination with new ideas, walk slowly and silently along its green paths. Breathe the fresh air, observe the trees in total peace, and completely disconnect from screens. Get up right now, grant yourself this intellectual break, and break the daily automatic pilot to reconnect with your creativity. Your wellness journey begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Campus universitario o biblioteca pública.", "donde_en": "University campus or public library.", "gps": "university library", "vector_necesidades": {"aprendizaje": 100, "silencio": 90, "contemplacion": 85, "descanso": 70, "aire_fresco": 75, "movimiento": 40} } 
   ],
    "estresado": [
  {"id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk", "porque": "Hoy vas a buscar una rampa inclinada, una colina o unas escaleras públicas al aire libre en tu entorno. Si sientes la musculatura muy tensa por culpa de las preocupaciones diarias y necesitas mover las piernas para liberar esa energía pesada, sube los escalones a un paso firme y constante. Siente el impulso dinámico y la fuerza real de tu cuerpo en cada pisada. Levántate ahora mismo, regálate esta pausa activa y permite que tu respiración se acelere de forma saludable para romper el estrés cotidiano. Quema esa carga mental and reconecta con tu poder físico de inmediato.", "porque_en": "Today you will look for a sloped ramp, a hill, or public stairs outdoors in your area. If you feel your muscles are very tense from daily worries and you need to move your legs to release that heavy energy, walk up the steps with a steady and firm pace. Feel the dynamic push and the real strength of your body with every single stride. Get up right now, grant yourself this active break, and allow your breathing to increase healthily to break through daily stress. Burn away that mental load and reconnect with your physical power immediately.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public stairs", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75} },

          {"id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga", "porque": "Hoy vas a buscar un parque que sea muy tranquilo. Si tu mente corre demasiado rápido por la prisa del día y necesitas unir tus movimientos con la naturaleza para volver a respirar en calma, extiende una lona o manta sobre el césped verde. Haz algunos estiramientos suaves con tus brazos y quédate de pie sintiendo el aire fresco en tu rostro. Levántate ahora mismo, regálate este respiro corporal y permite que la quietud del entorno repare tu balance interno. Rompe el piloto automático, libérate del estrés y conecta profundamente con tu presente ahora mismo.", "porque_en": "Today you will look for a park that is very quiet. If your mind is racing too fast from the daily rush and you need to unite your movements with nature to breathe calmly again, lay a mat or blanket on the green grass. Do some gentle arm stretches and stand still feeling the fresh air on your face. Get up right now, grant yourself this bodily break, and allow the environment's stillness to repair your inner balance. Break the automatic pilot, release your stress, and connect deeply with your present right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park", "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80} },
  {"id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym", "porque": "Hoy vas a visitar un centro deportivo o parque público que tenga aparatos de ejercicio. Si tienes mucha energía acumulada en el cuerpo y necesitas transformar la pesadez de los problemas diarios en fuerza física real, concéntrate en mover tus piernas y tus brazos de forma constante. Siente el motor activo de tu cuerpo encenderse en cada movimiento. Levántate ahora mismo, regálate esta descarga dinámica y permite que la fatiga mental se disuelva a través del esfuerzo físico controlado. Rompe tu rutina diaria, libera la tensión muscular y recupera tu poder corporal de inmediato.", "porque_en": "Today you will visit a sports center or public park with exercise equipment. If you have a lot of built-up energy in your body and you need to transform the heaviness of daily problems into real physical strength, focus on moving your legs and arms steadily. Feel your body's active engine turn on with every movement. Get up right now, grant yourself this dynamic discharge, and allow mental fatigue to dissolve through controlled physical effort. Break your daily routine, release muscle tension, and recover your bodily power immediately.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym", "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60} },
  {"id": 320, "titulo": "Liberación de Impacto", "titulo_en": "Impact Release", "porque": "Hoy vas a buscar el parque de trampolines o centro de juegos con colchonetas más cercano. Si sientes los músculos muy rígidos debido a los momentos de tensión de la semana y tu cuerpo necesita un juego activo para soltar el enojo, salta con alegría descargando todo el peso de tus pies en la lona. Diviértete subiendo un muro seguro usando tus manos con fuerza. Levántate ahora mismo, regálate este espacio recreativo de alta descarga física y permite que tu respiración se acelere felizmente. Rompe el estrés acumulado y reconecta con tu vitalidad.", "porque_en": "Today you will look for the nearest trampoline park or play center with mats. If you feel your muscles are very stiff from the tense moments of the week and your body needs an active game to release any anger, jump with joy launching your full weight onto the canvas. Have fun climbing a safe wall using the strength of your hands. Get up right now, grant yourself this recreational space of high physical discharge, and allow your breathing to increase happily. Break through accumulated stress and reconnect with your vitality.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque de trampolines o centro deportivo de alta descarga en tu Código Postal.", "donde_en": "Trampoline park or high-discharge sports center in your Zip Code.", "gps": "trampoline park or climbing gym", "vector_necesidades": {"movimiento": 100, "juego": 100, "risa": 90, "salud": 95, "descanso": 0, "silencio": 10, "comunidad": 60, "esperanza": 90} },

          {"id": 321, "titulo": "Módulo de Hidro-Calma", "titulo_en": "Hydro-Calm Module", "porque": "Hoy vas a visitar el centro deportivo con piscina pública o la YMCA más cercana de tu vecindario. Si tu cuerpo se siente muy cansado por las preocupaciones y los ruidos fuertes de la calle, el agua templada es perfecta para darte un descanso reconfortante de inmediato. Entra al agua climatizada con cuidado, cierra tus ojos por un momento y deja que las burbujas suaves te den un masaje en la espalda mientras flotas plácidamente. Levántate ahora mismo, regálate este quiebre de hidroterapia pasiva y permite que tu respiración se equilibre con la calma del agua.", "porque_en": "Today you will visit the nearest community pool sports center or YMCA in your neighborhood. If your body feels very tired from worries and loud street noise, warm water is perfect to give you a comforting rest immediately. Get into the heated water carefully, close your eyes for a moment, and let the gentle bubbles massage your back while you float placidly. Get up right now, grant yourself this passive hydrotherapy break, and allow your breathing to find its balance with the water's calm.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "YMCA, alberca climatizada o spa comunitario local.", "donde_en": "YMCA, heated pool, or local community spa.", "gps": "ymca pool or public spa", "vector_necesidades": {"agua": 100, "descanso": 100, "salud": 95, "silencio": 60, "contemplacion": 90, "sombra": 80, "esperanza": 85, "movimiento": 20} },
  {"id": 322, "titulo": "Quiebre de Frecuencias", "titulo_en": "Frequency Break", "porque": "Hoy vas a buscar un centro de meditación o un salón de yoga cercano para equilibrarte. Si tu mente corre demasiado rápido por culpa de mirar tanto el teléfono y necesitas encontrar un lugar silencioso para calmar tus pensamientos, entra despacio a su espacio de espera de inmediato. Toma asiento en un lugar cómodo, cierra tus ojos en completo silencio y toma aire de forma lenta y muy suave. Levántate ahora mismo, regálate este descanso mental profundo y habita el silencio acústico absoluto para romper el piloto automático. Tu mente sana en este entorno.", "porque_en": "Today you will look for a nearby meditation center or yoga studio to balance yourself. If your mind is racing too fast from looking at your phone so much and you need to find a quiet place to calm your thoughts, walk slowly into its waiting area immediately. Take a seat in a comfy spot, close your eyes in complete silence, and breathe in and out slowly and very gently. Get up right now, grant yourself this deep mental rest, and inhabit absolute acoustic silence to break the automatic pilot. Your mind heals in this environment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Estudio de yoga, centro de meditación o sound healing en USA.", "donde_en": "Yoga studio, meditation center, or sound healing spot in the USA.", "gps": "sound healing or yoga studio", "vector_necesidades": {"silencio": 100, "descanso": 95, "musica": 90, "contemplacion": 95, "salud": 90, "esperanza": 90, "organizacion": 70} },
  {"id": 323, "titulo": "Aislamiento Orgánico", "titulo_en": "Organic Isolation", "porque": "Hoy te dirigirás hacia el parque natural o la reserva de árboles más cercana en tu región. Si el ruido de la ciudad te tiene un poco abrumado y tu cuerpo te pide respirar el aire limpio de los árboles para sentirte mejor, camina despacio por el sendero boscoso. Quédate un minuto entero tocando la madera de un gran árbol y siente el viento fresco en tu cara lejos de los autos. Levántate ahora mismo, regálate este respiro natural y permite que tu cuerpo descargue la tensión de la semana de forma gratuita. Vive este instante.", "porque_en": "Today you will head toward the nearest nature park or tree reserve in your region. If the city noise has you a bit overwhelmed and your body is asking to breathe the clean air from the trees to feel better, walk slowly along the wooded trail. Spend one full minute touching the wood of a large tree and feel the fresh wind on your face away from cars. Get up right now, grant yourself this natural break, and allow your body to release the week's tension completely free. Live this moment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sendero boscoso, reserva natural o parque estatal de tu región.", "donde_en": "Wooded trail, nature reserve, or state park in your region.", "gps": "state park trail or nature reserve", "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "silencio": 85, "movimiento": 60, "contemplacion": 90, "descanso": 60, "esperanza": 95, "sol": 70} },

        {"id": 112, "titulo": "Sendero Corto Natural", "titulo_en": "Short Nature Trail", "porque": "Hoy vas a buscar un camino rodeado de árboles o plantas verdes en un sendero natural o bosque cercano. Si tu mente se siente muy cansada por culpa de tantos ruidos molestos y pantallas, te vendrá excelente desconectarte un momento para caminar en paz. Avanza de forma tranquila, a tu propio ritmo constante, mientras observas con calma los hermosos colores de la naturaleza. Levántate ahora mismo, regálate este respiro natural al aire libre y permite que tu respiración recupere su curso armonioso. Rompe tu rutina diaria y descansa de verdad.", "porque_en": "Today you will look for a path surrounded by trees or green plants in a nearby nature trail or forest. If your mind feels very tired from too much noise and looking at screens, it will do you excellent to disconnect for a moment and walk in peace. Walk peacefully at your own steady pace while calmly observing the beautiful colors of nature. Get up right now, grant yourself this natural break outdoors, and allow your breathing to find its harmonious course. Break away from your daily routine and truly rest.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sendero natural o bosque.", "donde_en": "Nature trail or forest.", "gps": "short nature track", "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "agua": 40, "sol": 60, "sombra": 70, "aire_fresco": 100, "creatividad": 40, "comunidad": 20, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "descanso": 60, "organizacion": 20, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85} },
  {"id": 113, "titulo": "Pista de Atletismo", "titulo_en": "Running Track", "porque": "Hoy te dirigirás hacia un circuito deportivo o pista de atletismo pública al aire libre en tu zona. Si sientes los pensamientos muy acelerados por la prisa del día y necesitas liberar toda esa fuerza acumulada para enfocar tu energía, avanza o trota a un paso cómodo para ti. Siente la fuerza real de tu cuerpo en cada zancada y nota cómo se va toda la tensión muscular. Levántate ahora mismo, regálate esta descarga física activa y permite que tu mente se despeje por completo del estrés diario. El recorrido empieza ya.", "porque_en": "Today you will head to an outdoor sports circuit or public running track in your local area. If you feel your thoughts are racing from the daily rush and you need to release all that built-up strength to focus your energy, walk or jog at a comfortable pace. Feel the real power of your body with every single stride and notice how all muscle tension washes away completely. Get up right now, grant yourself this active physical discharge, and allow your mind to clear from daily stress. Your journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Pista de atletismo pública.", "donde_en": "Public running track.", "gps": "public running track", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 40, "agua": 10, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 10, "comunidad": 50, "aprendizaje": 20, "juego": 30, "contemplacion": 50, "descanso": 10, "organizacion": 70, "alimentacion": 0, "musica": 50, "risa": 20, "esperanza": 70} },
  {"id": 251, "titulo": "Soberanía en Movimiento", "titulo_en": "Sovereignty in Motion", "porque": "Hoy vas a despegar tus ojos de la pantalla por un momento en tu cabina de transporte o asiento de pasajero. Si llevas mucho tiempo viajando encerrado en el auto o atrapado en medio del tráfico pesado y tu cuerpo necesita un momento de descompresión, reacciona. Apoya las palmas de tus manos firmes sobre tus rodillas, endereza la espalda y toma aire de forma lenta y profunda. Siente el peso real de tu cuerpo descansando sobre el asiento mientras dejas ir el agobio diario. Regálate este respiro pasivo de inmediato.", "porque_en": "Today you will take your eyes off the screen for a moment in your transit cabin or passenger seat. If you have been traveling cooped up inside the car or trapped in heavy traffic for too long and your body needs a moment of decompression, react now. Place the palms of your hands firmly on your knees, straighten your back, and take a slow, deep breath. Feel the real weight of your body resting on the seat while letting go of daily overload. Grant yourself this passive break immediately.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cabina de transporte, asiento de pasajero o parada de autobús de USA.", "donde_en": "Transit cabin, passenger seat, or USA bus stop.", "gps": "quiet rest areas or public plazas", "vector_necesidades": {"descanso": 95, "silencio": 85, "movimiento": 20, "contemplacion": 90, "organizacion": 60, "esperanza": 80} },
 
          {"id": 252, "titulo": "Hackeo al Tráfico", "titulo_en": "Traffic Hack", "porque": "Hoy vas a buscar una estación de servicio segura, semáforo o área de descanso en la autopista. Si sientes mucha pesadez y un nivel de estrés elevado debido a las filas largas de autos en la calle y a los ruidos molestos, aprovecha la luz roja para reaccionar. Abre grande tu boca por diez segundos para relajar tu mandíbula por completo. Estira los dedos de tus manos sobre el volante liberando la rigidez acumulada en tus muñecas. Mira a través de la ventana hacia el cielo abierto y toma aire con total calma. Regálate este respiro pasivo de inmediato.", "porque_en": "Today you will look for a safe service station, traffic light, or highway rest area. If you feel a high level of stress and heaviness from long lines of cars on the road and annoying highway noise, use the red light to react. Open your mouth wide for ten seconds to completely relax your jaw. Stretch your fingers over the steering wheel, releasing the tightness built up in your wrists. Look through the window at the open sky and take a deep breath with total calm. Grant yourself this passive break immediately.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Área de servicio de autopista, rampa pública o intersección vial.", "donde_en": "Highway service area, public ramp, or road intersection.", "gps": "highway rest stop or overlook", "vector_necesidades": {"movimiento": 80, "descanso": 70, "silencio": 50, "aire_fresco": 85, "organizacion": 40, "salud": 85} },
  {"id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route", "porque": "Hoy vas a buscar una ruta o un carril para bicicletas muy seguro en tu vecindario. Si tienes la necesidad urgente de liberar toda la tensión acumulada y moverte con ligereza sintiendo el viento fresco en tu cara, pedalea de forma tranquila y constante. Siente la velocidad agradable bajo tu control y disfruta de mantener el dominio de tu camino en una nueva aventura al aire libre. Levántate ahora mismo, regálate este quiebre de dinámica activa y permite que tu mente se despeje por completo de las preocupaciones diarias. Tu viaje empieza ya.", "porque_en": "Today you will look for a very safe bike lane or route in your neighborhood. If you have the urgent need to release all the built-up tension and move lightly, feeling the fresh wind on your face, pedal peacefully and steadily. Feel the pleasant speed under your control and enjoy keeping full dominance of your path in a new outdoor adventure. Get up right now, grant yourself this active dynamic break, and allow your mind to clear completely from daily worries. Your journey begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route", "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80} },
  {"id": 211, "titulo": "Soberanía de Cabina", "titulo_en": "Cabin Sovereignty", "porque": "Hoy vas a buscar la ventana más grande que tengas cerca en esta terminal de transporte con una hermosa vista despejada hacia afuera. Si sientes la mente muy saturada por las presiones del día y los ruidos fuertes causados por los viajes continuos en el transporte masivo, detén tu prisa. Toma aire de forma profunda y lenta tres veces seguidas para relajar los hombros por completo. Recuerda que tu cuerpo merece un momento legítimo de descanso libre de todo apuro. Siente el aire fresco y recupera tu calma interna ahora.", "porque_en": "Today you will look for the largest window nearby in this transit terminal that has a beautiful, clear view outside. If you feel your mind heavily overloaded from the pressures of the day and loud noises caused by continuous travel on mass transit, stop your rush. Take a deep, slow breath three times in a row to completely relax your shoulders. Remember that your body deserves a legitimate moment of rest free from any hurry. Feel the fresh air and recover your inner calm right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Terminal de aeropuerto o zona de observación abierta.", "donde_en": "Airport terminal or open observation zone.", "gps": "airport observation area", "vector_necesidades": {"aire_fresco": 100, "contemplacion": 95, "silencio": 60, "descanso": 50, "movimiento": 30, "esperanza": 80} },

          {"id": 212, "titulo": "Depuración de Tensión", "titulo_en": "Tension Cleansing", "porque": "Hoy vas a ir al centro deportivo, gimnasio o piscina pública que tengas más cerca en tu vecindario. Si sientes el cuerpo cargado de energía pesada debido al estrés del trabajo diario y necesitas sacudirte esa presión de encima, reacciona de inmediato. Haz un ejercicio de fuerza de forma constante por un momento, activa tus brazos y piernas, y permite que tu cuerpo suelte toda la rigidez acumulada. Levántate ahora mismo, regálate esta descarga física activa y deja que el agobio mental se disuelva mediante el esfuerzo muscular. Tu poder físico regresa ya.", "porque_en": "Today you will go to the nearest sports center, gym, or public pool in your neighborhood. If you feel your body loaded with heavy energy due to daily work stress and you need to shake that pressure off, react immediately. Do a strength exercise steadily for a moment, activate your arms and legs, and allow your body to release all the built-up stiffness. Get up right now, grant yourself this active physical discharge, and let the mental burden dissolve through muscular effort. Your physical power returns right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Gimnasio público, cancha o alberca comunitaria.", "donde_en": "Public gym, court, or community pool.", "gps": "community fitness center", "vector_necesidades": {"movimiento": 100, "agua": 80, "salud": 90, "juego": 50, "descanso": 0, "silencio": 20, "risa": 40} },
  {"id": 213, "titulo": "Estabilización Somática", "titulo_en": "Somatic Stabilization", "porque": "Hoy vas a visitar la farmacia o clínica local más cercana en tu vecindario. Si sientes los latidos del corazón un poco rápidos debido al agobio y tu cuerpo te pide una pausa suave en un lugar seguro para recuperar la tranquilidad, toma asiento cómodamente en su área de descanso de inmediato. Busca un vaso con agua fresca y bébelo muy despacio. Saborea con calma cada trago y nota cómo todo tu organismo se refresca y desacelera en completa paz. Regálate este respiro clínico protector y estabiliza tu ritmo biológico.", "porque_en": "Today you will visit the nearest local pharmacy or clinic in your neighborhood. If you feel your heartbeat a bit fast due to overwhelm and your body is asking for a gentle break in a safe place to recover your peace, take a comfortable seat in its lounge area immediately. Look for a cup of fresh water and drink it very slowly. Calmly taste every sip and notice how your entire organism refreshes and slows down in complete peace. Grant yourself this protective medical break and stabilize your biological rhythm.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Área de descanso de una farmacia o clínica local.", "donde_en": "Lounge area of a local pharmacy or clinic.", "gps": "pharmacy health lounge", "vector_necesidades": {"agua": 100, "salud": 95, "descanso": 80, "silencio": 70, "organizacion": 80, "esperanza": 85} } 
    ],
   "aburrido": [
  {"id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk", "porque": "Hoy vas a iniciar un hermoso paseo de colores. Si sientes que tus días se están volviendo idénticos y repetitivos, es el momento justo para despertar tu imaginación buscando novedades en las calles. Levántate ahora mismo y camina de forma muy lenta y tranquila por tu zona. Dedica este tiempo a buscar paredes con pintura, dibujos o murales de arte urbano llenos de vida. Haz este trayecto a solas para reconectar contigo mismo; es una recarga sin costo que romperá tu rutina y te hará sentir presente en el mundo. El viaje empieza ya.", "porque_en": "Today you will start a beautiful color walk. If you feel your days are becoming identical and repetitive, it is the right moment to awaken your imagination by seeking novelty out on the streets. Get up right now and walk very slowly and peacefully through your area. Dedicate this time to looking for walls with colorful paintings, drawings, or street art murals full of life. Do this journey alone to reconnect with yourself; it is a free recharge that will break your routine and make you feel present. Your journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street art", "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95} },

          {"id": 307, "titulo": "Descompresión de Perímetro", "titulo_en": "Perimeter Decompression", "porque": "Hoy vas a buscar un hotel o lugar de descanso que te quede cerca en tu vecindario. Si sientes el aburrimiento de estar encerrado en el mismo sitio de siempre y tu cuerpo te pide cambiar a un espacio bonito y ordenado, camina con total tranquilidad hacia su vestíbulo principal. Toma asiento en un sillón cómodo de inmediato, mantén tu espalda recta y descansa tu mirada de las pantallas por un minuto entero. Levántate ahora mismo, regálate este quiebre de entorno y permite que tu respiración se equilibre en este ambiente refinado. Tu mente se renueva ya.", "porque_en": "Today you will look for a hotel or resort close to you in your neighborhood. If you feel bored from being cooped up in the same old place and your body is asking to switch to a beautiful, orderly space, walk completely peacefully into its main lobby. Take a seat in a comfy chair immediately, keep your spine straight, and rest your eyes from screens for one full minute. Get up right now, grant yourself this change of scenery, and allow your breathing to find its balance in this refined environment. Your mind renews now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Lobby o zona de descanso pública de un hotel local.", "donde_en": "Lobby or public lounge area of a local hotel.", "gps": "hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 80, "esperanza": 80, "comunidad": 50, "movimiento": 20} },
  {"id": 308, "titulo": "Ampliación del Horizonte", "titulo_en": "Horizon Expansion", "porque": "Hoy te dirigirás hacia el vestíbulo o sala principal de una central de transportes o aeropuerto cercano. Si sientes la mente atascada en la rutina diaria y necesitas mirar hacia un espacio inmenso y abierto para recuperar tus ganas de explorar, busca el ventanal más grande. Quédate observando el cielo abierto y haz tres respiraciones lentas mientras contemplas la inmensidad del espacio exterior. Levántate ahora mismo, abraza este estímulo visual profundo y rompe el piloto automático diario expandiendo tus pensamientos con tranquilidad. Tu aventura interior comienza ya.", "porque_en": "Today you will head toward the lobby or main hall of a nearby transit center or airport. If you feel your mind stuck in the daily routine and you need to look at a vast, open space to recover your desire to explore, find the largest window. Keep observing the open sky and take three slow breaths while contemplating the vastness of space outside. Get up right now, embrace this deep visual stimulus, and break the daily automatic pilot by expanding your thoughts with tranquility. Your inner adventure begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30, "aprendizaje": 60} },
  {"id": 309, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Hoy vas a ir al parque de juegos o centro de entretenimiento más cercano en tu región. Si tu mente cayó en un bucle aburrido, plano y monótono, te vendrá excelente recibir un impacto alegre de colores vivos, risas y dinámicas divertidas. Observa los colores de las luces parpadeantes, escucha las risas de las personas a tu alrededor y permítete disfrutar de una actividad muy sencilla para romper con la monotonía del día. Levántate ahora mismo, regálate este respiro recreativo gratuito y activa tu energía positiva de inmediato.", "porque_en": "Today you will go to the nearest amusement park or play center in your region. If your mind fell into a boring, flat, and monotonous loop, it will do you excellent to get a joyful boost of bright colors, laughter, and fun dynamics. Observe the colorful flashing lights, listen to the laughter of the people around you, and allow yourself to enjoy a very simple activity to break the daytime monotony. Get up right now, grant yourself this free recreational break, and activate your positive energy immediately.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.", "gps": "amusement park or arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50, "creatividad": 60} },

          {"id": 313, "titulo": "Cazador de Sombras Urbano", "titulo_en": "Urban Shadow Hunter", "porque": "Hoy vas a salir a caminar por tu vecindario con un paso muy lento y pausado. Si sientes que tu rutina se ha vuelto monótona, gris y aburrida, necesitas un quiebre visual que active tu imaginación de inmediato. Concéntrate únicamente en buscar y observar cómo se proyectan las formas de las sombras de los árboles, postes y edificios sobre las aceras. Mira el mundo desde este ángulo geométrico diferente sin juzgar nada. Levántate ahora mismo, regálate este respiro contemplativo gratuito y rompe el piloto automático diario en total paz.", "porque_en": "Today you will go out for a walk in your neighborhood with a very slow and unhurried pace. If you feel your routine has become monotonous, gray, and boring, you need a visual break to activate your imagination immediately. Focus solely on looking and observing how the shapes of shadows from trees, poles, and buildings project onto the sidewalks. Look at the world from this different geometric angle without judging anything. Get up right now, grant yourself this free contemplative break, and break the daily automatic pilot in total peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Calles, aceras y callejones seguros de tu vecindario.", "donde_en": "Safe streets, sidewalks, and alleys in your neighborhood.", "gps": "public walking trail or neighborhood", "vector_necesidades": {"movimiento": 75, "contemplacion": 100, "creatividad": 95, "silencio": 60, "aire_fresco": 85, "juego": 40, "descanso": 30} },
  {"id": 314, "titulo": "Inmersión Textural", "titulo_en": "Textural Immersion", "porque": "Hoy te dirigirás hacia la plaza pública o parque arbolado más cercano de tu área. Si sientes el aburrimiento plano de estar atrapado en el teléfono mirando cosas vacías, es el momento de despertar tus sentidos mediante el tacto real. Camina despacio y busca tres superficies con texturas totalmente diferentes, como la madera rugosa de un tronco, el metal frío de una banca o la suavidad de una hoja limpia. Levántate ahora mismo, abraza este estímulo sensorial profundo de forma gratuita y permite que tu mente recupere su curiosidad natural ya.", "porque_en": "Today you will head toward the nearest public plaza or wooded park in your area. If you feel the flat boredom of being trapped on your phone looking at empty things, it is time to awaken your senses through real touch. Walk slowly and look for three surfaces with totally different textures, like the rough wood of a trunk, the cold metal of a bench, or the softness of a clean leaf. Get up right now, embrace this deep sensory stimulus for free, and allow your mind to regain its natural curiosity right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Plaza pública, parque o entorno urbano abierto.", "donde_en": "Public plaza, park, or open urban environment.", "gps": "public plaza or community park", "vector_necesidades": {"naturaleza": 90, "movimiento": 60, "creatividad": 85, "contemplacion": 95, "silencio": 70, "aire_fresco": 90, "juego": 30} },
  {"id": 315, "titulo": "Módulo de Exploración Gráfica", "titulo_en": "Graphic Exploration Module", "porque": "Hoy vas a visitar la biblioteca municipal o la librería más cercana en tu vecindario. Si sientes que tus pensamientos cayeron en un bucle repetitivo y aburrido, necesitas alimentar tu imaginación con estímulos visuales artísticos de inmediato. Ingresa despacio, camina en completo silencio hacia la sección de arte, diseño o fotografía y toma un libro grande. Abre sus páginas al azar y quédate contemplando detalladamente las ilustraciones o fotos por unos minutos. Levántate ahora mismo, regálate este respiro intelectual protector y rompe la rutina diaria en total calma.", "porque_en": "Today you will visit the municipal library or the nearest bookstore in your neighborhood. If you feel your thoughts fell into a repetitive and boring loop, you need to feed your imagination with artistic visual stimuli immediately. Enter slowly, walk in complete silence to the art, design, or photography section, and pick up a large book. Open its pages at random and stay closely contemplating the illustrations or photos for a few minutes. Get up right now, grant yourself this protective intellectual break, and break your daily routine in total calm.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sección de lectura, librería local o biblioteca pública.", "donde_en": "Reading section, local bookstore, or public library.", "gps": "public library or local bookstore", "vector_necesidades": {"aprendizaje": 100, "creatividad": 100, "contemplacion": 90, "silencio": 100, "descanso": 80, "organizacion": 60, "juego": 20} },

         {"id": 310, "titulo": "Exploración de Espacios", "titulo_en": "Space Exploration", "porque": "Hoy vas a abrir la aplicación de alquiler de casas en tu teléfono con total tranquilidad desde tu zona de descanso habitual. Si sientes que te falta imaginación y que tus días son aburridos, mirar fotos de lugares hermosos te ayudará a despertar tu creatividad de inmediato. Busca cabañas de madera o casitas de campo dentro de tu estado. Mira las fotos de las habitaciones y los landscapes como un juego interactivo para hacer volar tu mente, sin ninguna obligación de reservar nada. Regálate este viaje mental profundo y reconecta con tu inspiración ahora.", "porque_en": "Today you will open the home rental app on your phone with total peace of mind from your usual resting space. If you feel a lack of imagination and your days are boring, looking at pictures of beautiful places will help awaken your creativity immediately. Look for wooden cabins or country houses inside your state. Look at the photos of the rooms and landscapes as an interactive game to let your imagination fly, without any obligation to book anything. Grant yourself this deep mental journey and reconnect with your inspiration now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Interfaz móvil desde tu zona de descanso habitual.", "donde_en": "Mobile interface from your usual resting space.", "gps": "local post office", "vector_necesidades": {"creatividad": 100, "contemplacion": 95, "juego": 70, "organizacion": 80, "esperanza": 85, "descanso": 60, "aprendizaje": 60} },
  {"id": 311, "titulo": "Mapeo de Flujos", "titulo_en": "Flow Mapping", "porque": "Hoy te dirigirás a la tienda gigante o club de precios más conocer cercano en tu Código Postal. Si tu rutina se siente plana y aburrida y necesitas activar tu cuerpo, caminar por un lugar inmenso y lleno de movimiento despertará tus sentidos de inmediato. Camina a paso firme y tranquilo por los pasillos más largos del borde externo. Observa la gran cantidad de cajas y objetos a tu alrededor, y aprovecha este espacio techado y fresco para mover tus piernas de forma constante. Levántate ahora mismo, rompe el piloto automático y actívate.", "porque_en": "Today you will head to the nearest giant store or price club in your Zip Code. If your routine feels flat and boring and you need to activate your body, walking through a huge place full of movement will awaken your senses immediately. Walk steadily and peacefully through the long outer aisles. Observe the large amount of boxes and items around you, and use this indoor, cool space to move your legs constantly. Get up right now, break away from your daily automatic pilot, and activate your body.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Pasillos industriales de un gran almacén de USA.", "donde_en": "Industrial aisles of a large USA warehouse store.", "gps": "wholesale club or warehouse", "vector_necesidades": {"movimiento": 85, "organizacion": 75, "comunidad": 60, "contemplacion": 60, "juego": 40, "descanso": 10, "silencio": 5} },
  {"id": 312, "titulo": "Sabotaje de Espera", "titulo_en": "Waiting Sabotage", "porque": "Hoy vas a buscar la escuela o universidad pública que te quede más cerca en tu vecindario. Si tu mente cayó en un bucle aburrido, plano y pesado, te vendrá excelente recibir una inyección de aire fresco en un ambiente de estudio para recuperar tu enfoque de inmediato. Camina despacio y en completo silencio por sus jardines y plazas abiertas, respira el aire limpio con total libertad y observa el entorno con absoluta tranquilidad. Levántate ahora mismo, regálate este respiro intelectual gratuito y rompa la rutina diaria por completo.", "porque_en": "Today you will look for the public school or university closest to you in your neighborhood. If your mind fell into a boring, flat, and heavy loop, it will do you excellent to get a fresh air boost in a learning environment to regain your focus immediately. Walk slowly and in complete silence through its lawns and open squares, breathe the clean air freely, and observe the surroundings with absolute peace. Get up right now, grant yourself this free intellectual break, and completely break your everyday routine.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Áreas comunes abiertas de un campus universitario.", "donde_en": "Open common areas of a university campus.", "gps": "university campus or public school", "vector_necesidades": {"aprendizaje": 100, "aire_fresco": 95, "silencio": 90, "contemplacion": 85, "descanso": 70, "movimiento": 40} } 
   ],
    "cansado": [
  {"id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading", "porque": "Hoy vas a visitar la biblioteca pública de tu vecindario e ingresarás despacio. Si tu cuerpo te pide un momento legítimo de calma para aprender cosas bonitas sin ruidos y recargar tu energía en un lugar apacible, camina sin prisa entre los estantes. Busca un libro de cuentos o imágenes interesantes y disfruta del silencio absoluto del entorno. Levántate ahora mismo, regálate este respiro intelectual protector y permite que tus ojos descansen por completo de las pantallas. Rompe el piloto automático diario y sana tus pensamientos en paz.", "porque_en": "Today you will visit the public library in your neighborhood and enter slowly. If your body asks for a legitimate quiet moment to learn beautiful things without distractions and recharge your energy in a peaceful place, walk without rush among the shelves. Look for a storybook or interesting pictures and enjoy the absolute silence of the environment. Get up right now, grant yourself this protective intellectual break, and let your eyes rest completely from screens. Break the daily automatic pilot and heal your thoughts in total peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library", "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70} },
  {"id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk", "porque": "Hoy vas a dar una caminata muy tranquila por el muelle del puerto cercano. Si necesitas despejar tu mente por completo recibiendo aire fresco y contemplando paisajes hermosos junto al agua para relajarte profundamente, detén tu paso de inmediato. Observa detenidamente los barcos grandes que se mueven despacio en la distancia y escucha el sonido suave del oleaje rompiendo en la orilla. Levántate ahora mismo, regálate esta tregua marina restauradora y permite que tu respiración se sincronice con el ritmo del mar en calma. El viaje empieza ya.", "porque_en": "Today you will take a very peaceful walk along the nearby harbor pier. If you need to clear your mind completely by breathing fresh air and looking at beautiful landscapes by the water to relax deeply, stop your steps immediately. Closely watch the large boats moving slowly in the distance and listen to the soft sound of the waves breaking on the shore. Get up right now, grant yourself this restoring marine truce, and allow your breathing to synchronize with the calm sea's rhythm. Your journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier", "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90} },
  {"id": 328, "titulo": "Paseo junto al Mar", "titulo_en": "Maritime Stroll", "porque": "Hoy te dirigirás hacia el paseo costero o muelle más cercano de tu área. Si sientes un cansancio acumulado por la rutina de todos los días y tu mente te pide mirar el mar inmenso para olvidar el encierro de casa, detén tu marcha de inmediato. Quédate observando las grandes embarcaciones en el horizonte y permite que el brillo del sol reflejado sobre el agua se lleve la pesadez de tus pensamientos. Levántate ahora mismo, regálate este respiro pasivo frente al agua y activa tu bienestar natural de forma gratuita.", "porque_en": "Today you will head to the nearest coastal boardwalk or pier in your area. If you feel accumulated tiredness from the daily routine and your mind is asking to look at the vast sea to forget being cooped up at home, stop your pace immediately. Spend some time watching the large vessels on the horizon and let the bright sun reflecting on the water wash away the heaviness of your thoughts. Get up right now, grant yourself this passive break by the water, and activate your natural well-being completely free.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Muelle, puerto local o zona costera abierta.", "donde_en": "Dock, local pier, or open coastal zone.", "gps": "cruise terminal or pier", "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60, "esperanza": 85} },

         {"id": 329, "titulo": "Pausa en Ruta", "titulo_en": "Route Break", "porque": "Hoy vas a buscar la próxima estación o área de servicio segura en tu camino. Si sientes el cuerpo cansado y la mente muy pesada por culpa de estar viajando mucho tiempo o manejando en la autopista, estaciónate bien, apaga el motor y sal de tu auto inmediatamente. Haz un estiramiento muy suave con tus brazos, respira el aire fresco con tranquilidad y camina despacio por las inmediaciones. Levántate ahora mismo, regálate esta tregua en la carretera y permite que tu respiración recupere su curso natural en paz. Tu mente se despeja por completo.", "porque_en": "Today you will look for the next safe gas station or service area on your path. If you feel your body tired and your mind very heavy from traveling for a long time or driving on the highway, park well, turn off the engine, and step out of your car immediately. Do a very gentle stretch with your arms, breathe the fresh air calmly, and walk slowly around the vicinity. Get up right now, grant yourself this highway break, and allow your breathing to find its natural course in peace. Your mind clears completely.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Área de servicio de autopista o zona de descanso pública.", "donde_en": "Highway service area or public rest zone.", "gps": "highway rest stop or plaza", "vector_necesidades": {"descanso": 95, "movimiento": 60, "aire_fresco": 90, "salud": 85, "silencio": 50, "contemplacion": 70, "organizacion": 40} },
  {"id": 330, "titulo": "Recuperación Pasiva", "titulo_en": "Passive Recovery", "porque": "Hoy vas a buscar una zona histórica bonita o una plaza antigua cercana en tu vecindario. Si tu mente se encuentra agotada de hacer siempre las mismas cosas todos los días y necesitas un cambio de ritmo muy suave, camina a un paso lento y sin prisa. Quédate contemplando los edificios antiguos del lugar y usa este hermoso entorno urbano para despejar tu cabeza por completo. Levántate ahora mismo, regálate este respiro arquitectónico pasivo y permite que tu cuerpo desacelere de forma gratuita. Tu curiosidad despierta en total quietud.", "porque_en": "Today you will look for a beautiful historical zone or an old plaza nearby in your neighborhood. If your mind feels exhausted from doing the same exact things every day and you need a very gentle change of pace, walk at a slow and unhurried pace. Keep contemplating the old buildings of the place and use this beautiful urban environment to clear your head completely. Get up right now, grant yourself this passive architectural break, and allow your body to slow down for free. Your curiosity awakens in total stillness.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Centro histórico, plaza pública o calles peatonales.", "donde_en": "Historical center, public plaza, or pedestrian streets.", "gps": "historical landmark or walking tour", "vector_necesidades": {"aprendizaje": 90, "contemplacion": 95, "descanso": 80, "movimiento": 50, "silencio": 70, "creatividad": 60, "esperanza": 80} },
  {"id": 331, "titulo": "Aislamiento Sensorial", "titulo_en": "Sensory Isolation", "porque": "Hoy vas a ir al cine más cercano de tu vecindario para aislarte del ajetreo. Si sientes la mente muy llena de ruidos por hablar con demasiadas personas y hacer tantas tareas apuradas en la ciudad, elige una película que esté en un horario con poca gente. Toma asiento en la oscuridad reconfortante de la sala, guarda tu teléfono en el bolsillo y disfruta de la tranquilidad absoluta del lugar. Levántate ahora mismo, regálate este descanso mental profundo en las sombras y desconecta del mundo exterior de forma segura.", "porque_en": "Today you will go to the nearest movie theater in your neighborhood to isolate yourself from the hustle. If you feel your mind heavily overloaded from talking to too many people and doing so many rushed tasks in the city, choose a film playing at a time with very few people. Take a seat in the comforting dim light of the room, put your phone away in your pocket, and enjoy the absolute quietness of the place. Get up right now, grant yourself this deep mental rest in the shadows, and safely disconnect from the outside world.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sala de cine comercial o vestíbulo de proyecciones.", "donde_en": "Commercial movie theater or screening lobby.", "gps": "local cinema or amc", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 90, "sombra": 100, "juego": 40, "creatividad": 50, "movimiento": 5} },

          {"id": 332, "titulo": "Refugio Verde", "titulo_en": "Green Shelter", "porque": "Hoy vas a buscar el jardín botánico o el parque de flores más cercano en tu región. Si sientes el cuerpo cansado por culpa de estar encerrado todo el día respirando el aire frío de la oficina y necesitas tocar las plantas, encuentra un banco tranquilo rodeado de hojas verdes de inmediato. Quédate allí sentado en absoluta calma por dos minutos enteros y respira el aire limpio de la naturaleza. Levántate ahora mismo, regálate esta tregua natural protectora y permite que tu cuerpo recupere su vitalidad libre de estrés. Rompe el piloto automático diario y descansa en paz.", "porque_en": "Today you will look for the nearest botanical garden or flower park in your region. If you feel your body tired from being cooped up all day breathing cold office air and you need to touch the plants, find a quiet bench surrounded by green leaves immediately. Sit there peacefully for two whole minutes and breathe the clean air of nature. Get up right now, grant yourself this protective natural break, and allow your body to recover its vitality free from stress. Break away from the daily automatic pilot and truly rest in peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Jardín botánico público, vivero o parque natural regional.", "donde_en": "Public botanical garden, nursery, or regional nature park.", "gps": "botanical garden or nursery", "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "descanso": 90, "silencio": 80, "contemplacion": 95, "sombra": 90, "salud": 85, "movimiento": 25} },
  {"id": 333, "titulo": "Un Momento de Quietud", "titulo_en": "A Moment of Quietness", "porque": "Hoy vas a buscar un parque cercano que tenga un pequeño lago o estanque público. Si tu mente se encuentra aburrida por hacer siempre las mismas cosas y te vendrá excelente mirar el movimiento suave del agua para descansar, toma asiento en la orilla de inmediato. Quédate un minuto completo mirando cómo se mueven las ondas del agua y los pajaritos, y respira de forma muy lenta. Levántate ahora mismo, regálate este respiro visual pasivo y permite que la quietud de la superficie repare tu balance interno. Tu imaginación despierta en total calma.", "porque_en": "Today you will look for a nearby park that has a small public lake or pond. If your mind feels bored from always doing the same exact things and it will be excellent to watch the gentle movement of water to rest, take a seat by the edge immediately. Spend one full minute watching the water ripples and the birds, and breathe very slowly. Get up right now, grant yourself this passive visual break, and allow the surface's stillness to repair your inner balance. Your imagination awakens in total calm right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Banco de parque junto a un estanque o lago público.", "donde_en": "Park bench next to a public pond or lake.", "gps": "public lake park or fountain", "vector_necesidades": {"agua": 100, "contemplacion": 100, "descanso": 95, "silencio": 75, "naturaleza": 85, "aire_fresco": 90, "movimiento": 15} },
  {"id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory", "porque": "Hoy vas a visitar una pequeña sala de ciencia o centro astronómico cercano en tu ciudad. Si sientes la mente muy apurada por las tareas diarias y necesitas levantar la mirada hacia el cielo inmenso para maravillarte con el universo, dedica tu tiempo a aprender cosas bonitas sobre el espacio exterior. Contempla las estrellas si la noche está totalmente despejada y deja ir la prisa. Levántate ahora mismo, regálate este quiebre intelectual profundo y permite que la inmensidad del cosmos disuelva tus preocupaciones mundanas por completo. Tu mente sana hoy.", "porque_en": "Today you will visit a small science room or nearby astronomical center in your city. If you feel your mind in a big hurry from daily tasks and you need to lift your gaze to the vast sky to marvel at the universe, dedicate your time to learning beautiful things about outer space. Look at the stars if the night is totally clear and let go of the rush. Get up right now, grant yourself this deep intellectual break, and allow the cosmos' vastness to completely dissolve your worldly worries. Your mind heals today.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory", "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95} },

          {"id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza", "porque": "Hoy vas a buscar una plaza pública o parque para tomar asiento de forma muy cómoda en un banco público. Si tu mente necesita detener la marcha para conectarse con la vida de tu comunidad, descansar los hombros y observar el entorno con tranquilidad, quédate contemplando el caminar lento de las personas a tu alrededor. Siente el ritmo de la ciudad en completo silencio. Levántate ahora mismo, regálate este respiro pasivo de bienestar y permite que tu respiración recupere su curso natural en paz. Tu mente se renueva por completo hoy.", "porque_en": "Today you will look for a public plaza or park to take a very comfortable seat on a public bench. If your mind needs to slow down to connect with your community's life, rest your shoulders, and observe your surroundings with peace, stay contemplating the slow walking of the people around you. Feel the city's rhythm in complete silence. Get up right now, grant yourself this passive wellness break, and allow your breathing to find its natural course in peace. Your mind completely renews itself today.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza", "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85} },
  {"id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour", "porque": "Hoy te unirás a una caminata guiada o harás un recorrido peatonal por las calles antiguas de tu ciudad. Si te encuentras cansado de ver siempre los mismos caminos predecibles y tu cuerpo te pide un paseo suave para aprender historias nuevas, descubre los relatos del pasado con absoluta calma. Estira tus piernas alegremente y mantén tu mente curiosa lejos de los dispositivos digitales. Levántate ahora mismo, regálate este quiebre intelectual activo y permite que tu cuerpo active su energía. Tu nueva aventura urbana empieza ya.", "porque_en": "Today you will join a guided walk or take a pedestrian tour through the old streets of your city. If you feel tired of always seeing the same predictable paths and your body is asking for a gentle stroll to learn new stories, discover the tales of the past with absolute calm. Stretch your legs joyfully and keep your curious mind away from digital devices. Get up right now, grant yourself this active intellectual break, and allow your body to activate its energy. Your new urban adventure begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour", "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90} },
  {"id": 231, "titulo": "Paseo junto al Mar", "titulo_en": "Maritime Stroll", "porque": "Hoy te dirigirás hacia el muelle, puerto o zona costera abierta más cercana de tu región. Si sientes un cansancio monótono por pasar mucho tiempo encerrado y tu mente te pide mirar el mar inmenso para olvidar los ruidos del concreto de la calle, detén tu marcha de inmediato. Quédate observando las grandes embarcaciones en la línea del horizonte y permite que el reflejo de la luz sobre el agua limpie todos tus pensamientos. Levántate ahora mismo, regálate este descanso contemplativo pasivo y respira el aire marino.", "porque_en": "Today you will head to the nearest dock, pier, or open coastal zone in your region. If you feel a monotonous tiredness from spending too much time cooped up and your mind is asking to look at the vast sea to forget the street's concrete noises, stop your pace immediately. Spend some time watching the large vessels on the horizon line and let the light reflecting on the water clear away all your thoughts. Get up right now, grant yourself this passive contemplative rest, and breathe the fresh marine air.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Muelle, puerto o zona costera abierta.", "donde_en": "Dock, pier, or open coastal zone.", "gps": "cruise terminal or pier", "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60} },

          {"id": 232, "titulo": "Ritmo en la Ciudad", "titulo_en": "City Rhythm", "porque": "Hoy vas a caminar por una zona alegre del centro de la ciudad donde haya música. Si sientes el aburrimiento de una rutina muy callada y tu cuerpo te pide escuchar canciones alegres para activarte, quédate un momento en la acera al aire libre. Escucha el ritmo de la música de fondo y siente la energía divertida de las luces de la calle que rompen tu monotonía por completo. Levántate ahora mismo, regálate este estímulo acústico dinámico y permite que tu cuerpo recupere su entusiasmo natural de inmediato. El viaje y la música empiezan ya.", "porque_en": "Today you will walk through a cheerful downtown area where there is music. If you feel the boredom of a very quiet routine and your body is asking to hear some cheerful music to activate yourself, stay for a moment on the open sidewalk. Listen to the rhythm of the songs playing in the background and feel the fun energy of the street lights breaking your monotony completely. Get up right now, grant yourself this dynamic acoustic boost, and allow your body to recover its natural enthusiasm immediately. Your journey starts now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Perímetro exterior o terraza de un club céntrico.", "donde_en": "Outer perimeter or terrace of a central club.", "gps": "dance club or nightclub", "vector_necesidades": {"musica": 100, "juego": 90, "comunidad": 80, "risa": 70, "movimiento": 60, "silencio": 10, "descanso": 40} } 
    ],
    "ansioso": [
  {"id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water", "porque": "Hoy vas a buscar una hermosa fuente, un lago tranquilo o un río cercano en tu zona. Si sientes que la prisa mental te agobia, recuerda que el agua en movimiento es ideal para darte calma de inmediato. Te ayuda a despejar la mente de preocupaciones y relajar por completo las tensiones acumuladas de tus hombros. Siéntate en la orilla a observar detalladamente el flujo constante de la corriente y relájate. Levántate ahora mismo, regálate este respiro visual pasivo y permite que tu respiración se equilibre con la naturaleza. Todo está bien en este instante.", "porque_en": "Today you will look for a beautiful fountain, a quiet lake, or a nearby river in your area. If you feel that mental rush overwhelms you, remember that moving water is ideal for bringing you calm immediately. It helps clear your mind of worries and completely relax the built-up tension in your shoulders. Sit by the edge to closely observe the steady flow of the stream and relax. Get up right now, grant yourself this passive visual break, and allow your breathing to find its balance with nature. Everything is fine at this moment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake", "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80} },
  {"id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride", "porque": "Hoy vas a realizar un paseo corto en una lancha o bote pequeño en un lago o río cercano. Si llevas mucho estrés acumulado en la semana y tu mente te pide una desconexión total para flotar con ligereza y descansar profundamente, este quiebre es para ti. Siente la brisa fresca del aire sobre tu rostro y contempla la inmensidad del agua con absoluta tranquilidad. Levántate ahora mismo, regálate esta tregua acuática liberadora y permite que tu mente se limpie de toda prisa. Tu camino de bienestar y paz empieza en este mismo segundo.", "porque_en": "Today you will take a short ride in a motorboat or a small rowboat on a nearby lake or river. If you have a lot of built-up stress from the week and your mind is asking for a total disconnection to float lightly and rest deeply, this break is for you. Feel the fresh breeze of the air on your face and contemplate the vastness of the water in absolute peace. Get up right now, grant yourself this liberating aquatic truce, and allow your mind to clear from all rush. Your path to well-being and peace begins this very second.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river", "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90} },

          {"id": 345, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Hoy vas a dirigirte al parque de mascotas o zona de juegos más cercana de tu Código Postal. Si sientes pensamientos repetitivos y mucha inquietud en tu cabeza, te vendrá excelente un momento de juego y risas para calmar tus nervios de inmediato. Quédate mirando cómo juegan los animalitos de forma divertida, escucha los sonidos alegres del lugar y conéctate con esa diversión inocente por un minuto completo. Levántate ahora mismo, regálate este respiro recreativo pasivo y permite que tu respiración se equilibre con la alegría del entorno. Tu ansiedad se disuelve aquí.", "porque_en": "Today you will head to the nearest pet park or play area in your Zip Code. If you feel repetitive thoughts and a lot of restlessness in your head, a moment of play and laughter will be excellent to calm your nerves immediately. Spend some time watching the animals play in a fun way, listen to the cheerful sounds of the place, and connect with that innocent fun for one full minute. Get up right now, grant yourself this passive recreational break, and allow your breathing to find its balance with the joy around you. Your anxiety fades away.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque de perros local, zona infantil o centro de juegos.", "donde_en": "Local dog park, kids zone, or arcade center.", "gps": "dog park or amusement arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 90, "movimiento": 70, "esperanza": 95, "silencio": 20, "descanso": 50, "creatividad": 40} },
  {"id": 346, "titulo": "Un Momento de Quietud", "titulo_en": "A Moment of Stillness", "porque": "Hoy vas a visitar el jardín o el patio interior de un hotel cercano. Si sientes un poco de timidez o cansancio por estar con muchas personas y tu cabeza está pesada debido a tantas responsabilidades, toma asiento tranquilamente en uno de los sillones públicos de inmediato. Cierra tus ojos por un minuto entero and respira de forma muy lenta para descansar tu cuerpo por completo. Levántate ahora mismo, regálate este quiebre de entorno protector y permite que el silencio repare tu balance interno en paz. Tu mente descansa en total comodidad.", "porque_en": "Today you will visit the garden or inner courtyard of a nearby hotel. If you feel a bit of shyness or tiredness from being around too many people and your head is heavy due to so many responsibilities, take a seat peacefully in one of the public armchairs immediately. Close your eyes for one whole minute and breathe very slowly to rest your body completely. Get up right now, grant yourself this protective change of scenery, and allow the stillness to repair your inner balance in peace. Your mind rests in total comfort.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Zona de descanso, jardín interior o lobby de un hotel de USA.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.", "gps": "boutique hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 95, "contemplacion": 95, "organizacion": 80, "salud": 90, "esperanza": 90, "sombra": 80} },
  {"id": 347, "titulo": "Estrategia de Alivio", "titulo_en": "Relief Strategy", "porque": "Hoy caminarás hacia la sala principal de la central de autobuses o aeropuerto más cercano. Si sientes una sensación de encierro debido a la rutina de trabajar todos los días en el mismo lugar y necesitas estirar la mirada, guarda tu teléfono en el bolsillo de inmediato. Observa con calma a las personas viajar y recuerda que el mundo es inmenso y este momento de inquietud pasará pronto. Levántate ahora mismo, abraza este estímulo visual profundo y rompe el piloto automático diario expandiendo tus pensamientos. Tu viaje interior comienza ya.", "porque_en": "Today you will walk to the main hall of the nearest transit station or airport. If you feel a sense of confinement from the routine of working every day in the same place and you need to stretch your gaze, put your phone away in your pocket immediately. Calmly watch the people traveling and remember that the world is huge and this moment of restlessness will pass soon. Get up right now, embrace this deep visual stimulus, and break the daily automatic pilot by expanding your thoughts. Your inner journey begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Vestíbulo público de aeropuerto o central de transportes regional.", "donde_en": "Public airport lobby or regional transit hub.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 60, "movimiento": 40, "aprendizaje": 50} },
  {"id": 348, "titulo": "Pausa en la Cafetería", "titulo_en": "Coffee Shop Pause", "porque": "Hoy vas a dirigirte a una cafetería tranquila de tu vecindario en tu Código Postal. Si sientes mucha inquietud en tu cabeza por estar solo con tus preocupaciones y tu cuerpo te pide estar rodeado de un ambiente amable y pacífico, toma asiento en un rincón cómodo de inmediato. Pide una bebida tibia o un vaso de agua fresca y guarda tu teléfono en el bolsillo. Quédate sintiendo el aroma del lugar mientras descansas profundamente. Levántate ahora mismo, regálate este respiro social pasivo y permite que tu respiración se estabilice en este espacio seguro. Tu mente descansa ya.", "porque_en": "Today you will head to a quiet coffee shop in your neighborhood within your Zip Code. If you feel a lot of restlessness in your head from being alone with your worries and your body is asking to be surrounded by a warm, quiet space, take a seat in a cozy corner immediately. Order a warm drink or a fresh glass of water and put your phone away in your pocket. Stay feeling the pleasant aroma of the place while you rest deeply. Get up right now, grant yourself this passive social break, and allow your breathing to stabilize in this safe space. Your mind rests now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cafetería o establecimiento de bebidas local en tu Código Postal.", "donde_en": "Local coffee shop or beverage venue in your Zip Code.", "gps": "quiet cafe or bakery", "vector_necesidades": {"comunidad": 90, "descanso": 85, "silencio": 75, "alimentacion": 60, "contemplacion": 80, "esperanza": 85, "musica": 30} },
  {"id": 123, "titulo": "Jardín de Rocas Zen", "titulo_en": "Rock Zen Garden", "porque": "Hoy vas a buscar un parque de piedras o un jardín de estilo japonés cercano en tu zona. Si tus pensamientos avanzan de forma muy apurada y necesitas buscar un espacio con un orden hermoso para equilibrar tu mente en calma, detén tu prisa de inmediato. Observa detenidamente las formas redondas de las rocas y disfruta de la tranquilidad profunda de este entorno protector. Levántate ahora mismo, regálate este quiebre visual contemplativo y permite que la armonía del diseño repare tu balance interno en paz. Tu mente se serena en total quietud.", "porque_en": "Today you will look for a nearby stone park or a Japanese-style garden in your area. If your thoughts are racing too fast and you need to find a space with a beautiful layout to bring balance to your mind in calm, stop your rush immediately. Closely observe the round shapes of the rocks and enjoy the deep quietness of this protective environment. Get up right now, grant yourself this contemplative visual break, and allow the design's harmony to repair your inner balance in peace. Your mind calms in total stillness.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden", "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90} },
  {"id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park", "porque": "Hoy vas a visitar un parque de mascotas local de tu zona. Si te hace falta una dosis urgente de risas y alegría sincera para apagar tus nervios, quédate un momento sentado en un banco observando el entorno. Mira el juego inocente de los animales que te contagiará de una energía muy positiva mientras corren y se divierten los perritos con total soltura. Levántate ahora mismo, regálate esta distracción pasiva y permite que tu respiración recupere su ritmo natural en paz lejos de tus responsabilidades diarias. La alegría pura te abraza hoy.", "porque_en": "Today you will visit a local dog park in your area. If you need an urgent boost of smiles and sincere joy to turn off your nerves, spend some time sitting on a bench observing the environment. Watch the innocent play of animals that will catch you with a very positive energy as the puppies run and have fun with total ease. Get up right now, grant yourself this passive distraction, and allow your breathing to find its natural rhythm in peace away from daily responsibilities. Pure joy embraces you today.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park", "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90} },

         {"id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music", "porque": "Hoy vas a encontrar una pequeña cafetería o rincón local con canciones tranquilas de fondo. Si sientes la mente un poco cansada y te vendrá muy bien disfrutar de una experiencia hermosa escuchando melodías tranquilas para calmar tus hombros, toma asiento de inmediato. Quédate un momento sentado escuchando los instrumentos musicales con atención y sin mirar tu teléfono celular. Levántate ahora mismo, regálate este estímulo acústico protector y permite que tu respiración se equilibre con la melodía en paz. Tu mente se libera de toda prisa.", "porque_en": "Today you will find a small coffee shop or local spot with calm songs playing in the background. If you feel your mind is a bit tired and it will do you very good to enjoy a beautiful experience listening to calm melodies to relax your shoulders, take a seat immediately. Stay seated for a moment listening to the instruments with attention and without looking at your cell phone. Get up right now, grant yourself this protective acoustic boost, and allow your breathing to balance with the melody in peace. Your mind breaks free from all rush.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar", "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85} },
  {"id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool", "porque": "Hoy vas a visitar la alberca municipal o el centro deportivo con piscina de tu vecindario. Si sientes el cuerpo tenso debido a las tareas diarias y necesitas el abrazo fresco del agua para flotar tranquilo y olvidar las preocupaciones del día, date un chapuzón suave con mucho cuidado. Descansa tu musculatura por completo mientras flotas en la superficie del agua en total quietud. Levántate ahora mismo, regálate este quiebre de hidroterapia pasiva y permite que tu mente se limpie de todo agobio rutinario de forma gratuita.", "porque_en": "Today you will visit the municipal pool or the community sports center in your neighborhood. If you feel your body tense from daily tasks and you need the fresh embrace of water to float peacefully and forget your day's worries, take a gentle dip very carefully. Rest your muscles completely while floating on the water's surface in total stillness. Get up right now, grant yourself this passive hydrotherapy break, and allow your mind to clear from all routine overload completely free.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool", "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85} },
  {"id": 241, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Hoy vas a ir al parque de juegos o centro recreativo familiar más cercano en tu zona. Si tus pensamientos están dando vueltas en círculos aburridos, planos y pesados, te vendrá excelente recibir una inyección de risas y diversión inocente de inmediato. Observa los colores alegres de los letreros luminosos y conéctate con las actividades lúdicas más sencillas para alegrar tu mente sin presiones. Levántate ahora mismo, regálate este respiro recreativo pasivo y permite que tu cuerpo active su vitalidad natural de forma gratuita hoy.", "porque_en": "Today you will go to the nearest amusement park or family recreation center in your area. If your thoughts are spinning around in boring, flat, and heavy circles, it will do you excellent to get a boost of laughter and innocent fun immediately. Observe the cheerful colors of the bright signs and connect with the simplest playful activities to brighten your mind without pressures. Get up right now, grant yourself this passive recreational break, and allow your body to activate its natural vitality completely free today.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.", "gps": "amusement park or arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50} },

  {"id": 242, "titulo": "Estrategia de Alivio", "titulo_en": "Relief Strategy", "porque": "Hoy caminarás hacia la sala principal de la central de autobuses o aeropuerto más cercano. Si sientes una sensación de encierro debido a la rutina de trabajar todos los días en el mismo lugar y necesitas estirar la mirada, guarda tu teléfono en el bolsillo de inmediato. Observa con calma a las personas viajar y recuerda que el mundo es inmenso y este momento de inquietud pasará pronto. Levántate ahora mismo, abraza este estímulo visual profundo y rompe el piloto automático diario expandiendo tus pensamientos. Tu viaje interior comienza ya.", "porque_en": "Today you will walk to the main hall of the nearest transit station or airport. If you feel a sense of confinement from the routine of working every day in the same place and you need to stretch your gaze, put your phone away in your pocket immediately. Calmly watch the people traveling and remember that the world is huge and this moment of restlessness will pass soon. Get up right now, embrace this deep visual stimulus, and break the daily automatic pilot by expanding your thoughts. Your inner journey begins right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30} },
  {"id": 243, "titulo": "Un Momento de Quietud", "titulo_en": "A Moment of Stillness", "porque": "Hoy vas a visitar el jardín o el patio interior de un hotel cercano. Si sientes un poco de timidez o cansancio por estar con muchas personas y tu cabeza está pesada debido a tantas responsabilidades, toma asiento tranquilamente en uno de los sillones públicos de inmediato. Cierra tus ojos por un minuto entero y respira de forma muy lenta para descansar tu cuerpo por completo. Levántate ahora mismo, regálate este quiebre de entorno protector y permite que el silencio repare tu balance interno en paz. Tu mente descansa en total comodidad.", "porque_en": "Today you will visit the garden or inner courtyard of a nearby hotel. If you feel a bit of shyness or tiredness from being around too many people and your head is heavy due to so many responsibilities, take a seat peacefully in one of the public armchairs immediately. Close your eyes for one whole minute and breathe very slowly to rest your body completely. Get up right now, grant yourself this protective change of scenery, and allow the stillness to repair your inner balance in peace. Your mind rests in total comfort.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Zona de descanso o jardín de un hotel de USA.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.", "gps": "boutique hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 95, "organizacion": 80, "salud": 85, "esperanza": 85} },
  {"id": 244, "titulo": "Soberanía de Cabina", "titulo_en": "Cabin Sovereignty", "porque": "Hoy vas a buscar la ventana más grande que tengas cerca en esta terminal de transporte con una vista despejada hacia afuera. Si sientes la mente muy saturada por las presiones del día y los ruidos fuertes causados por los viajes continuos en el transporte masivo, detén tu prisa de inmediato. Toma aire de forma profunda y lenta tres veces seguidas para relajar los hombros por completo. Recuerda que tu cuerpo merece un momento legítimo de descanso libre de todo apuro. Siente el aire fresco y recupera tu calma interna ahora.", "porque_en": "Today you will look for the largest window nearby in this transit terminal that has a beautiful, clear view outside. If you feel your mind heavily overloaded from the pressures of the day and loud noises caused by continuous travel on mass transit, stop your rush immediately. Take a deep, slow breath three times in a row to completely relax your shoulders. Remember that your body deserves a legitimate moment of rest free from any hurry. Feel the fresh air and recover your inner calm right now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Terminal de aeropuerto, central de tránsito o zona de observación abierta.", "donde_en": "Airport terminal, transit hub, or open observation zone.", "gps": "airport terminal or transit hub", "vector_necesidades": {"aire_fresco": 95, "contemplacion": 100, "esperanza": 90, "descanso": 70, "silencio": 60, "movimiento": 30} }
] 
} 
}

BIG_TECH_RESOURCES = {
    "spotify_audio_es": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_es": "https://www.youtube.com/results?search_query=sonidos+naturaleza+relajantes",
    "spotify_audio_en": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_en": "https://www.youtube.com/results?search_query=nature+sounds+relaxing",
}

# ==========================================================================================
# CWRE V2
# SCORE INTELIGENTE (REFINADO)
# ==========================================================================================
def score_coincidencia(perfil_local, vector_necesidades, historial=None, mission_id=None):
    historial = historial or []
    score = 0

    # --------------------------------------------------------------------------------------
    # Coincidencia principal: Cuanto más cerca esté la necesidad
    # del usuario del objetivo de la misión, mayor el score.
    # --------------------------------------------------------------------------------------
    for necesidad, objetivo in vector_necesidades.items():
        if necesidad == "indicador_ansiedad":
            continue
        usuario = perfil_local.get(necesidad, DEFAULT_NECESSITY_VECTOR.get(necesidad, 50))
        diferencia = abs(usuario - objetivo)
        score += (100 - diferencia) * 0.5  # Ponderación base

    # --------------------------------------------------------------------------------------
    # Priorizar necesidades insatisfechas (altas en perfil) y que la misión las cubra bien.
    # --------------------------------------------------------------------------------------
    for necesidad, valor_usuario in perfil_local.items():
        if necesidad == "indicador_ansiedad":
            continue

        # Si la necesidad del usuario es alta (insatisfecha) y la misión la cubre bien
        obj_mision = vector_necesidades.get(necesidad, 0)
        if valor_usuario > 70 and obj_mision > 70:
            score += (valor_usuario * 0.3)  # Bonificación fuerte
        elif valor_usuario > 50 and obj_mision > 50:
            score += (valor_usuario * 0.1)  # Bonificación moderada

    # --------------------------------------------------------------------------------------
    # Priorizar ansiedad: Misiones que atienden directamente la ansiedad.
    # --------------------------------------------------------------------------------------
    ansiedad = perfil_local.get("indicador_ansiedad", 0)

    if ansiedad >= 70:  # Nivel alto de ansiedad
        score += vector_necesidades.get("silencio", 0) * 0.5
        score += vector_necesidades.get("descanso", 0) * 0.5
        score += vector_necesidades.get("esperanza", 0) * 0.4
        score += vector_necesidades.get("naturaleza", 0) * 0.3
        score += vector_necesidades.get("agua", 0) * 0.3
    elif ansiedad >= 40:  # Nivel medio de ansiedad
        score += vector_necesidades.get("descanso", 0) * 0.2
        score += vector_necesidades.get("silencio", 0) * 0.2

    # --------------------------------------------------------------------------------------
    # Penalización por repetición histórica y bonus por exploración
    # --------------------------------------------------------------------------------------
    if mission_id is not None:
        score -= penalizacion_historial(mission_id, historial)
        score += bonus_exploracion(mission_id, historial)

    return round(max(0, score), 2)

# ==========================================================================================
# Selección por Ranking Inteligente
# ==========================================================================================
def seleccionar_por_ranking(candidatos):
    if not candidatos:
        return None

    candidatos = sorted(candidatos, key=lambda x: x["score"], reverse=True)
    if not candidatos:
        return None

    mejor_score = candidatos[0]["score"]

    # Si todos tienen un score bajo, y todos son iguales, elige uno al azar.
    if mejor_score <= 100:  # Umbral para considerar que los scores son "bajos"
        scores_unicos = {c["score"] for c in candidatos}
        if len(scores_unicos) == 1:
            return random.choice(candidatos)

    # Considerar un umbral dinámico para seleccionar entre los mejores
    score_umbral = max(mejor_score * 0.8, mejor_score - 150)  # El 80% del mejor o 150 puntos menos que el mejor
    mejores_candidatos_para_eleccion = [
        c for c in candidatos if c["score"] >= score_umbral
    ]

    if not mejores_candidatos_para_eleccion:
        # Si el umbral fue demasiado estricto, relaja y toma del top 3
        mejores_candidatos_para_eleccion = candidatos[:min(3, len(candidatos))]

    if not mejores_candidatos_para_eleccion:
        return None

    pesos = [c["score"] for c in mejores_candidatos_para_eleccion]
    # Asegúrate de que ningún peso sea cero o negativo para random.choices
    pesos = [max(1, p) for p in pesos]

    return random.choices(mejores_candidatos_para_eleccion, weights=pesos, k=1)[0]

# ==========================================================================================
# CWRE V2
# Selector Universal de Misiones
# ==========================================================================================
def seleccionar_mision_inteligente(misiones, perfil_local, historial=None):
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

# ==========================================================================================
# CWRE V2.1
# Seleccionar N misiones inteligentes y diversas (para modo SALIR)
# ==========================================================================================
def seleccionar_n_misiones_inteligentes(n, misiones, perfil_local, historial_actual=None):
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

        mision_id = cand["mision"]["id"]
        if mision_id not in ids_seleccionados and mision_id not in historial_actual:
            es_diversa = True

            for sel_mision in seleccionadas:
                distancia = diversidad_vector(
                    cand["mision"].get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                    sel_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
                )
                # Define un umbral de diversidad. Si son muy parecidas, no la elijas.
                if distancia < 100:  # Ajusta este umbral según sea necesario para la diversidad
                    es_diversa = False
                    break

            if es_diversa:
                seleccionadas.append(cand["mision"])
                ids_seleccionados.add(mision_id)

    # Si aún no tenemos suficientes, toma las siguientes mejores aunque no sean tan diversas
    for cand in candidatos_base:
        if len(seleccionadas) >= n:
            break

        mision_id = cand["mision"]["id"]
        if mision_id not in ids_seleccionados and mision_id not in historial_actual:
            seleccionadas.append(cand["mision"])
            ids_seleccionados.add(mision_id)

    # Si todavía no tenemos suficientes, y el historial se ha agotado, reinicia y toma al azar
    if len(seleccionadas) < n and len(misiones) >= n:
        temp_misiones = [m for m in misiones if m["id"] not in ids_seleccionados]

        # Si no hay suficientes nuevas, recicla todo el catálogo
        if len(temp_misiones) < n - len(seleccionadas):
            temp_misiones = misiones

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
        mision_aleatoria_id = mision_aleatoria["id"]
        if mision_aleatoria_id not in ids_seleccionados:
            seleccionadas.append(mision_aleatoria)
            ids_seleccionados.add(mision_aleatoria_id)

    return seleccionadas[:n]

# ==========================================================================================
# Filtrar historial (para disponibilidad de misiones)
# ==========================================================================================
def filtrar_historial(misiones, historial):
    historial = historial or []
    disponibles = [m for m in misiones if m["id"] not in historial]
    return disponibles

# ==========================================================================================
# CASA V2
# Selección inteligente de misiones domésticas
# ==========================================================================================
def seleccionar_misiones_casa_inteligente(misiones, perfil_local, historial_casa=None, cantidad=3):
    historial_casa = historial_casa or []
    disponibles = filtrar_historial(misiones, historial_casa)
    
    if len(disponibles) < cantidad * 2:
        # Si quedan muy pocas sin repetir, considera todo el catálogo de nuevo
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

    candidatos.sort(key=lambda x: x["score"], reverse=True)
    resultado = []
    ids_en_resultado = set()

    # Intenta seleccionar misiones diversas y de alto score
    for candidato in candidatos:
        mision_actual = candidato["mision"]
        mision_id = mision_actual["id"]
        
        if mision_id in ids_en_resultado:
            continue

        es_diversa = True
        for anterior_mision in resultado:
            distancia = diversidad_vector(
                mision_actual.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                anterior_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
            )
            if distancia < 60:  # Umbral de diversidad para misiones CASA
                es_diversa = False
                break

        if es_diversa:
            resultado.append(mision_actual)
            ids_en_resultado.add(mision_id)

        if len(resultado) >= cantidad:
            break

    # [CORRECCIÓN DUMP]: Bucle de respaldo seguro si la diversidad fue muy estricta
    if len(resultado) < cantidad and len(misiones) >= cantidad:
        for candidato in candidatos:
            mision_actual = candidato["mision"]
            if mision_actual["id"] not in ids_en_resultado:
                resultado.append(mision_actual)
                ids_en_resultado.add(mision_actual["id"])
            if len(resultado) >= cantidad:
                break

    return resultado
    # Si no se alcanzan las 'cantidad' requeridas con diversidad, añade las siguientes mejores
    if len(resultado) < cantidad:
        for candidato in candidatos:
            mision_actual = candidato["mision"]
            mision_id = mision_actual["id"]

            if mision_id not in ids_en_resultado:
                resultado.append(mision_actual)
                ids_en_resultado.add(mision_id)

            if len(resultado) >= cantidad:
                break

    # Fallback final: si aún no hay suficientes, toma las primeras 'cantidad'
    if len(resultado) < quantity and len(misiones) >= quantity:
        resultado = [c["mision"] for c in candidatos[:quantity]]

    return resultado

@app.get("/")
async def index():
    """Serves the main HTML page."""
    return FileResponse('static/session.html')

# ==========================================================================================
# INYECCIÓN OPERATIVA: CONTROLADORES DE COMPRA Y ACCESO ADMINISTRATIVO CON REQUEST SEGURO
# ==========================================================================================
# from fastapi import HTTPException  # Asegura la importación para evitar fallos de ejecución (already at the top)

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
            success_url="https://open-than-go.onrender.com",
            cancel_url="https://open-than-go.onrender.com",
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
# ==========================================================================================
@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    """
    Main API endpoint for OPEN THAN GO.
    Receives user input and local preference profile to return a personalized recommendation.
    """
    payload = await request.json()
    opcion_usuario = str(payload.get("modo", "")).strip().upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip() # 'estado' parameter is defined but not used elsewhere in this function
    region = str(payload.get("region", "")).strip() # 'region' parameter is defined but not used elsewhere in this function
    mente = str(payload.get("mente", "aburrido")).lower()
    budget = str(payload.get("budget", "0"))
    perfil_tipo = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    lang = str(payload.get("lang", "es")).lower()

    if zip_code and not re.fullmatch(r"^\d{5}$", zip_code):
        return JSONResponse(
            status_code=400,
            content={"error": "Código Postal inválido. Debe ser 5 dígitos numéricos."}
        )

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
        "trabajo", "empleo", "job", "jobs", "work", "career", "interview", "resume", "cv",
        "curriculum", "linkedin", "indeed", "networking", "cliente", "client", "empresa",
        "company", "income", "earn money", "ganar dinero", "producir", "productividad",
        "buscar oportunidades", "buscar ofertas", "enviar currículo", "actualizar linkedin",
        "conseguir empleo", "salir a buscar trabajo", "metas profesionales", "presion economica",
        "presión económica", "biles", "deudas", "misery", "exploitation", "amazon", "walmart",
        "costco", "fresco", "tienda", "comprar", "dinero", "economy", "oportunidades laborales",
        "solicitudes de empleo", "visitar empresas", "buscando clientes", "producir dinero",
        "obligaciones laborales", "responsabilidades", "tareas", "negocio", "negocios",
        "presión", "presiones"
    ]

    force_recovery_mission = False
    explicitly_seeking_job = any(
        phrase in desahogo
        for phrase in ["quiero buscar trabajo", "necesito un empleo", "busco trabajo", "find a job", "looking for work"]
    )

    # DETECCIÓN DE SÍNTOMAS CORPORATIVOS O AMBIENTALES DEL ENTORNO DE USA
    marca_detectada = None
    if desahogo and not explicitly_seeking_job:
        desahogo_lower = desahogo.lower()
        target_brands = [
            "walmart", "amazon", "costco", "starbucks", "mcdonald",
            "spotify", "youtube", "tiktok", "instagram"
        ]
        for keyword in target_brands:
            if keyword in desahogo_lower:
                marca_detectada = keyword.capitalize()
                break

    # If the detected brand implies a digital service, use Big Tech Resources, otherwise proceed with
    # location-based activity if `force_recovery_mission` is true.
    if marca_detectada:
        force_recovery_mission = True # Always force a recovery mission if a brand is detected

    if force_recovery_mission and marca_detectada:
        mente_str_es = mente.upper()
        mente_str_en = mente.upper()
        diagnostico_sintoma_es = f"Diagnóstico: El cliente experimenta [{mente_str_es}] en relación al estímulo corporativo [{marca_detectada}] en Zip Code {zip_code}."
        diagnostico_sintoma_en = f"Diagnostic: Client experiences [{mente_str_en}] linked to corporate stimulus [{marca_detectada}] in Zip Code {zip_code}."

        instruccion_fisiologica_es = ""
        instruccion_fisiologica_en = ""
        enlace_yt = ""
        enlace_sp = ""

        # Using BIG_TECH_RESOURCES for specific brands
        if marca_detectada == "Walmart":
            instruccion_fisiologica_es = "Estás en el templo del consumo. Hackea: detén tu marcha, inhala/exhala profundo. Repite: 'Yo soy el único producto que importa hoy'. Sal de la rutina."
            instruccion_fisiologica_en = "You are in the consumption temple. Hack it: stop, inhale/exhale deeply. Repeat: 'I am the only product that matters today'. Exit routine."
            # Fallback to general search if no specific resource
            enlace_yt = BIG_TECH_RESOURCES.get("youtube_audio_es" if lang == "es" else "youtube_audio_en")
            enlace_sp = BIG_TECH_RESOURCES.get("spotify_audio_es" if lang == "es" else "spotify_audio_en")
        elif marca_detectada == "Amazon":
            instruccion_fisiologica_es = "Tu mente busca dopamina rápida. Bloquea la pantalla. Enfócate en tu espacio biológico: hidrátate o elimina toxinas. Invierte en tus células, no en el mercado digital."
            instruccion_fisiologica_en = "Mind seeks quick dopamine. Block screen. Focus on biological space: hydrate or detox. Invest in cells, not digital market."
            enlace_yt = BIG_TECH_RESOURCES.get("youtube_audio_es" if lang == "es" else "youtube_audio_en")
            enlace_sp = BIG_TECH_RESOURCES.get("spotify_audio_es" if lang == "es" else "spotify_audio_en")
        elif marca_detectada in ["Youtube", "Tiktok", "Instagram"]:
            instruccion_fisiologica_es = "El algoritmo secuestra tu atención. Interrumpe el bucle mental. Suelta el teléfono, cierra ojos 60 segundos. Respira profundo, libera estrés."
            instruccion_fisiologica_en = "Algorithm hijacks attention. Break mental loop. Drop phone, close eyes 60 secs. Breathe deep, release stress."
            # For these, directly link to appropriate resource from BIG_TECH_RESOURCES if it makes sense, or general relaxation sounds
            receta_key_yt = antidotos_digitales.get(mente, antidotos_digitales["aburrido"])["yt"]
            receta_key_sp = antidotos_digitales.get(mente, antidotos_digitales["aburrido"])["sp"]
            enlace_yt = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(receta_key_yt)}"
            enlace_sp = f"https://open.spotify.com/search/{urllib.parse.quote_plus(receta_key_sp)}"
        elif marca_detectada == "Spotify":
            instruccion_fisiologica_es = "Usas sonidos para aislarte. Detén el audio. Ejecuta el Módulo Silencio Mental 1 minuto. Siente tu ritmo cardíaco en este Código Postal."
            instruccion_fisiologica_en = "You use sounds to isolate. Stop audio. Execute 1-minute Mental Silence Module. Feel your heart rhythm in this Zip Code."
            enlace_yt = BIG_TECH_RESOURCES.get("youtube_audio_es" if lang == "es" else "youtube_audio_en") # Link to YouTube for visual rest
            enlace_sp = BIG_TECH_RESOURCES.get("spotify_audio_es" if lang == "es" else "spotify_audio_en") # Link to general Spotify for calming
        else:
            # Default case for other brands not explicitly handled above
            instruccion_fisiologica_es = f"Identificaste que [{marca_detectada}] satura tu mente. Rebélate: usa pasillos, aire libre o ventanas. Haz una pausa biológica profunda de 60 segundos. Recupera el control."
            instruccion_fisiologica_en = f"You identified [{marca_detectada}] saturating your mind. Rebel: use halls, open air, or windows. Take a deep 60-sec biological pause. Regain control."
            enlace_yt = BIG_TECH_RESOURCES.get("youtube_audio_es" if lang == "es" else "youtube_audio_en")
            enlace_sp = BIG_TECH_RESOURCES.get("spotify_audio_es" if lang == "es" else "spotify_audio_en")

        # ==========================================================================================
        # CONSTRUCCIÓN DE CONSULTA DINÁMICA DE ECONOMÍA REAL (GOOGLE MAPS UNIVERSAL)
        # ==========================================================================================
        # Respetamos rigurosamente tu formato de budget ("0", "1", "2") y perfil_tipo ("solo", "familia", "accesible")
        nucleos_ocio = {
            "ansioso": {
                "0": "nature+preserves+botanical+gardens",
                "1": "cozy+tea+house+bookstore+cafe",
                "2": "luxury+spa+wellness+resort"
            },
            "estresado": {
                "0": "public+beaches+hiking+trails",
                "1": "jazz+club+lounge+bar+comedy",
                "2": "fine+dining+restaurant+boutique+hotel"
            },
            "aburrido": {
                "0": "skate+parks+street+art+squares",
                "1": "bowling+alley+arcade+sports+bar",
                "2": "theme+parks+live+concerts+cruises"
            },
            "agotado": {
                "0": "scenic+lakes+quiet+public+parks",
                "1": "local+coffee+shop+bakery",
                "2": "glamping+resort+cabin+rental"
            },
            "cansado": { # Added for consistency, although 'mente' fallback is 'aburrido'
                "0": "public+library+museums",
                "1": "historic+sites+walking+tours",
                "2": "calm+beach+resort+towns"
            }
        }

        matriz_ocio = nucleos_ocio.get(mente, nucleos_ocio["aburrido"])
        gasto_key = budget if budget in ["0", "1", "2"] else "0"
        actividad_base = matriz_ocio[gasto_key]

        modificador_compania = ""
        if perfil_tipo == "familia":
            modificador_compania = "+family+friendly"
        elif perfil_tipo == "accesible":
            modificador_compania = "+wheelchair+accessible"
        elif perfil_tipo == "solo":
            modificador_compania = "+hidden+gems"

        # Armamos el misil exacto para Google Maps respetando el código postal original
        full_query = f"{actividad_base}{modificador_compania}+in+{zip_code}"
        target_link = f"{link_base}{urllib.parse.quote_plus(full_query)}"

        # Inyectamos de forma segura las variables al objeto de la misión respetando tu esquema original
        final_misiones_para_frontend = [{
            "destino_id": 999,
            "destino_titulo": f"HACKEO A {marca_detectada.upper()}",
            "destino_titulo_en": f"HACKING {marca_detectada.upper()}",
            "que_hacer": "Interrupción de Control Mental y Retorno al Cuerpo.",
            "que_hacer_en": "Mental Control Interruption & Return to Body.",
            "destino_entorno": "PERÍMETRO DE ACCIÓN DE CAMPO",
            "destino_instruccion": instruccion_fisiologica_es,
            "destino_instruccion_en": instruccion_fisiologica_en,
            "destino_coordenadas_gps": target_link,
            "enlace_youtube": enlace_yt,  # Variables seguras integradas en la estructura de la misión
            "enlace_spotify": enlace_sp,  # Variables seguras integradas en la estructura de la misión
            "vector_entorno_seleccionado": {**DEFAULT_NECESSITY_VECTOR, "homeostasis_urgente": True},
            "diagnostico_sintoma_es": diagnostico_sintoma_es,
            "diagnostico_sintoma_en": diagnostico_sintoma_en,
        }]

        # Retornamos el JSONResponse respetando estrictamente los campos originales que tus scripts esperan
        # Retiramos inyecciones pesadas de texto para proteger la sincronización y evitar congelamientos
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "misiones": final_misiones_para_frontend,
            "historial_salir_actualizado": payload.get("historial_salir", []),
            "forced_recovery": True
        })
        
                  # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA)
    if opcion_usuario == "CASA":
        # Captura el manifiesto existencial para el 1% de Calidez Humana
        textos_oraculo_casa = MANIFIESTOS_ORACULO.get(mente, MANIFIESTOS_ORACULO["aburrido"])
        manifiesto_humano_casa = random.choice(textos_oraculo_casa)
        
        idioma = "EN" if lang == "en" else "ES"
        target_key = f"CASA_{idioma}"
        
        # Recupera el catálogo de misiones de forma directa y segura
        misiones_completas = []
        if "BASE_MISIONES" in globals():
            misiones_completas = BASE_MISIONES.get(target_key, BASE_MISIONES.get("casa", []))
            
        # Purgamos y preparamos las misiones asegurando que tengan 'titulo' y 'descripcion'
        final_misiones_casa = []
        for m in misiones_completas:
            if isinstance(m, dict):
                final_misiones_casa.append({
                    "id": m.get("id", 800),
                    "titulo": m.get("titulo", "Misión Interna"),
                    "descripcion": m.get("descripcion", m.get("que_hacer", m.get("porque", "Pausa de bienestar somática."))),
                    "vector_necesidades": m.get("vector_necesidades", {})
                })

        # RESPALDO: Solo si tu catálogo global estuviera completamente vacío o ilegible
        if not final_misiones_casa:
            if idioma == "ES":
                final_misiones_casa = [
                    {
                        "id": 801,
                        "titulo": "Pausa de Respiración Somática",
                        "descripcion": "Rompe el bucle del estrés digital. Inhala profundamente durante 4 segundos, mantén el aire por 4 segundos y exhala en 4 segundos.",
                        "vector_necesidades": {}
                    }
                ]
            else:
                final_misiones_casa = [
                    {
                        "id": 801,
                        "titulo": "Somatic Breathing Pause",
                        "descripcion": "Break the digital stress loop. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale for 4 seconds.",
                        "vector_necesidades": {}
                    }
                ]

          # ==========================================================================================
    # 1. INTERVENCIÓN DOMÉSTICA (RESTABLECIMIENTO DE FÁBRICA MODO CASA)
    # ==========================================================================================
    if opcion_usuario == "CASA":
        idioma = "EN" if lang == "en" else "ES"
        target_key = f"CASA_{idioma}"
        
        # Recupera el catálogo de misiones de forma directa y segura
        misiones_completas = BASE_MISIONES.get(target_key, [])
        
        # Selección inteligente utilizando la función CASA V2 purificada
        misiones_casa = seleccionar_misiones_casa_inteligente(
            misiones=misiones_completas,
            perfil_local=perfil_local,
            historial_casa=payload.get("historial_casa", []),
            cantidad=3
        )

        # Actualizamos el historial del catálogo de forma segura
        historial_casa = payload.get("historial_casa", [])
        for m in misiones_casa:
            historial_casa = actualizar_historial(historial_casa, m["id"], MAX_HISTORY_CASA)

        # RETORNO LIMPIO DE CASA: Evita colisiones eliminando la calidez humana inflada
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": misiones_casa,
            "historial_casa_actualizado": historial_casa
        })

    # ==========================================================================================
    # 2. ACTION DE CAMPO (RESTABLECIMIENTO DE FÁBRICA MODO SALIR)
    # ==========================================================================================
    else:
        opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
        historial_salir = payload.get("historial_salir", [])
        
        misiones_seleccionadas_raw = seleccionar_n_misiones_inteligentes(
            n=3,
            misiones=opciones_salir_candidatas,
            perfil_local=perfil_local,
            historial_actual=historial_salir
        )

        final_misiones_para_frontend = []
        antidotos_digitales = {
            "youtube": "https://youtube.com",
            "spotify": "https://spotify.com"
        }

        for info_seleccionada in misiones_seleccionadas_raw:
            # === MENSAJES DE ACOMPAÑAMIENTO Y GASTO AISLADOS PARA LA INTERFAZ ===
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

            # CONDICIONALES DE IDIOMA TOTALMENTE SIMÉTRICOS E INDEPENDIENTES
            if lang == "en":
                guia_masticada_es = info_seleccionada.get('porque', '')
                guia_masticada_en = info_seleccionada.get('porque_en', info_seleccionada.get('porque', ''))
                titulo_ganador_lang = (info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) or "").upper()
                que_hacer_lang = info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''
            else:
                guia_masticada_es = info_seleccionada.get('porque', '')
                guia_masticada_en = info_seleccionada.get('porque_en', info_seleccionada.get('porque', ''))
                titulo_ganador_lang = (info_seleccionada['titulo'] or "").upper()
                que_hacer_lang = info_seleccionada["que_hacer"] or ""

            search_query_parts = []
            if perfil_tipo == "accesible":
                search_query_parts.append("wheelchair accessible")
            elif perfil_tipo == "familia":
                search_query_parts.append("family friendly")
                
            search_query_parts.append(info_seleccionada.get("gps", "park"))
            target_link = f"{map_base_url}?q={'+'.join(search_query_parts)}+{anclaje_geografico}"
            final_vector_necesidades = info_seleccionada.get("vector_necesidades", {})

            enlace_yt = info_seleccionada.get("enlace_youtube", antidotos_digitales["youtube"])
            enlace_sp = info_seleccionada.get("enlace_spotify", antidotos_digitales["spotify"])

            # === ASIGNACIÓN SIMÉTRICA DE DATOS ORIGINALES ===
            final_misiones_para_frontend.append({
                "destino_id": info_seleccionada.get("id"),
                "destino_titulo": titulo_ganador_lang,
                "destino_titulo_en": titulo_ganador,
                "que_hacer": que_hacer_lang,
                "que_hacer_en": info_seleccionada.get("que_hacer_en", info_seleccionada["que_hacer"]),
                "destino_entorno": donde_base,
                "destino_instruccion": guia_masticada_es.strip(),
                "destino_instruccion_en": guia_masticada_en.strip(),
                "destino_coordenadas_gps": target_link,
                "vector_entorno_seleccionado": final_vector_necesidades,
                "enlace_youtube": enlace_yt,
                "enlace_spotify": enlace_sp
            })
            historial_salir = actualizar_historial(historial_salir, info_seleccionada["id"], MAX_HISTORY_SALIR)

        # RETORNO LIMPIO DE SALIR: Alineado con la función principal para evitar SyntaxError
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "misiones": final_misiones_para_frontend,
            "historial_salir_actualizado": historial_salir
        }) 
# ==========================================================================================
# APERTURA NATIVA DEL SERVIDOR FASTAPI (SINOPSIS ESTRUCTURAL DE CIERRE)
# ==========================================================================================
if __name__ == "__main__":
    port_env = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port_env, reload=False)

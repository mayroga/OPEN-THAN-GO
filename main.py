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
from fastapi import FastAPI, Request, HTTPException # HTTPException import fixed
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

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

# ==========================================================================================
# UTILIDAD MECÁNICA: Cálculo de Diversidad de Vectores
# (Añadido para resolver NameError debido a la invocación en la lógica existente)
# ==========================================================================================
def diversidad_vector(vec1, vec2):
    score = 0
    all_keys = set(vec1.keys()).union(vec2.keys())
    for key in all_keys:
        val1 = vec1.get(key, 0)
        val2 = vec2.get(key, 0)
        score += abs(val1 - val2)
    return score

# === CONFIGURACIÓN DE PAUSA EXTENDIDA Y PROPÓSITO HUMANO CON CALIDEZ ===
# Se corrigen y estandarizan los 15 minutos exactos del ciclo de vida de sesión somática en frontend.
TIEMPO_EXTRA_REPOSO_SEGUNDOS = 240
VELOCIDAD_VOZ_HUMANA = 0.95
WHEN_ES = "Tómate tu tiempo. Respira. Levántate sin prisa."
WHEN_EN = "Take your time. Breathe. Move without rushing."
FOR_WHAT_ES = "Romper el piloto automático. Sentirte libre y recordar que estás vivo."
FOR_WHAT_EN = "Break the autopilot. Feel completely free and remember you are alive."

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
  {"id": 1, "titulo": "Break the autopilot", "titulo_en": "Break the autopilot", "descripcion": "Take a brief moment to scan your body completely. Locate the exact weight built up on your upper back and observe it with absolute calm. Feel your heartbeat and remember that you are alive in this peaceful second.", "descripcion_en": "Take a brief moment to scan your body completely. Locate the exact weight built up on your upper back and observe it with absolute calm. Feel your heartbeat and remember that you are alive in this peaceful second.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
  {"id": 2, "titulo": "Total disconnection", "titulo_en": "Total disconnection", "descripcion": "Feel the shape of the chair beneath your body right now. The firm floor supports your entire weight completely for free and safely. Do not fight it, let yourself fall into total calm at this instant.", "descripcion_en": "Feel the shape of the chair beneath your body right now. The firm floor supports your entire weight completely for free and safely. Do not fight it, let yourself fall into total calm at this instant.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
  {"id": 3, "titulo": "Screen isolation", "titulo_en": "Screen isolation", "descripcion": "Turn your cell phone face down with total peace of mind at this instant. Stare closely at a corner of the ceiling for thirty straight seconds and allow your mind to break the loop of digital rush now.", "descripcion_en": "Turn your cell phone face down with total peace of mind at this instant. Stare closely at a corner of the ceiling for thirty straight seconds and allow your mind to break the loop of digital rush now.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
  {"id": 4, "titulo": "Let go of the load", "titulo_en": "Let go of the load", "descripcion": "Feel your shoulders completely free and lightweight right now. Imagine that you no longer carry that heavy invisible backpack on you. Let go of all accumulated mental stiffness and breathe with complete ease.", "descripcion_en": "Feel your shoulders completely free and lightweight right now. Imagine that you no longer carry that heavy invisible backpack on you. Let go of all accumulated mental stiffness and breathe with complete ease.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
  {"id": 5, "titulo": "The water reset", "titulo_en": "The water reset", "descripcion": "Take a small, unhurried sip of cold water at this moment. Feel the exact path of the fresh liquid passing down your throat. It is pure life entering to fully renew your entire organism completely.", "descripcion_en": "Take a small, unhurried sip of cold water at this moment. Feel the exact path of the fresh liquid passing down your throat. It is pure life entering to fully renew your entire organism completely.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "salud": 80}},
  {"id": 7, "titulo": "Window breeze", "titulo_en": "Window breeze", "descripcion": "Open your room's window completely right now. Let the fresh outdoor air gently touch your face during this count. Feel the outside world and clear your mind from all the confinement of routine.", "descripcion_en": "Open your room's window completely right now. Let the fresh outdoor air gently touch your face during this count. Feel the outside world and clear your mind from all the confinement of routine.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30}},
  {"id": 8, "titulo": "Energy rotation", "titulo_en": "Energy rotation", "descripcion": "Gently rotate your wrists and your ankles in slow circles. Remember that this body belongs completely to you and you govern this engine. Feel how natural energy begins to flow freely through your entire being.", "descripcion_en": "Gently rotate your wrists and your ankles in slow circles. Remember that this body belongs completely to you and you govern this engine. Feel how natural energy begins to flow freely through your entire being.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "salud": 80, "creatividad": 20}},
  {"id": 9, "titulo": "Anchor to the present", "titulo_en": "Anchor to the present", "descripcion": "Close your eyes in complete acoustic silence right now. Think closely about one good and beautiful thing you have in your life today. Say it with strength in your mind in absolute calm.", "descripcion_en": "Close your eyes in complete acoustic silence right now. Think closely about one good and beautiful thing you have in your life today. Say it with strength in your mind in absolute calm.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30}},
  {"id": 11, "titulo": "Feet on the ground", "titulo_en": "Feet on the ground", "descripcion": "Take off your shoes right now, without any rush. Place the soles of your feet directly on the cool floor of the room. Feel the firmness of the ground beneath you and connect.", "descripcion_en": "Take off your shoes right now, without any rush. Place the soles of your feet directly on the cool floor of the room. Feel the firmness of the ground beneath you and connect.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70}},
  {"id": 12, "titulo": "Stretch to the sky", "titulo_en": "Stretch to the sky", "descripcion": "Stretch your arm firmly upward and try to touch the ceiling with your fingertips. Hold that muscle tension for an exact second during this count. Now release everything all at once dynamically.", "descripcion_en": "Stretch your arm firmly upward and try to touch the ceiling with your fingertips. Hold that muscle tension for an exact second during this count. Now release everything all at once dynamically.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "salud": 80, "creatividad": 30, "juego": 20}},
  {"id": 14, "titulo": "Straight spine", "titulo_en": "Straight spine", "descripcion": "Straighten your back completely at this very moment. An invisible string gently pulls your head toward the sky. Feel how your chest opens freely and inhabit your deep and peaceful breathing now.", "descripcion_en": "Straighten your back completely at this very moment. An invisible string gently pulls your head toward the sky. Feel how your chest opens freely and inhabit your deep and peaceful breathing now.", "vector_necesidades": {"salud": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70}},
  {"id": 15, "titulo": "Cold touch", "titulo_en": "Cold touch", "descripcion": "Look for an object or surface that is cold to the touch in your room and place your hand on it. Feel the real temperature for a few seconds. This helps calm your mind immediately at home.", "descripcion_en": "Look for an object or surface that is cold to the touch in your room and place your hand on it. Feel the real temperature for a few seconds. This helps calm your mind immediately at home.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20}},
  {"id": 16, "titulo": "Total ventilation", "titulo_en": "Total ventilation", "descripcion": "Open the nearest window in your current room. Let the new air enter and roll through the entire available space. Breathe slowly and notice how your home's environment changes peacefully.", "descripcion_en": "Open the nearest window in your current room. Let the new air enter and roll through the entire available space. Breathe slowly and notice how your home's environment changes peacefully.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40}},
  {"id": 17, "titulo": "Stress shake", "titulo_en": "Stress shake", "descripcion": "Stand up carefully in your safe space. Shake your hands and legs gently as if you were shaking off small drops of water. Do this cheerful movement for ten seconds at home.", "descripcion_en": "Stand up carefully in your safe space. Shake your hands and legs gently as if you were shaking off small drops of water. Do this cheerful movement for ten seconds at home.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70}},
  {"id": 18, "titulo": "Distant gaze", "titulo_en": "Distant gaze", "descripcion": "Look through the window and find the object or house that is furthest away from you. Keep observing that fixed point to rest your eyes from screens in complete and deep peace.", "descripcion_en": "Look through the window and find the object or house that is furthest away from you. Keep observing that fixed point to rest your eyes from screens in complete and deep peace.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40}},
  {"id": 19, "titulo": "Happy memory", "titulo_en": "Happy memory", "descripcion": "Close your eyes gently for a moment in your cozy corner. Bring to your mind a beautiful and innocent memory from when you were a child. Feel the peace that pretty day gives you.", "descripcion_en": "Close your eyes gently for a moment in your cozy corner. Bring to your mind a beautiful and innocent memory from when you were a child. Feel the peace that pretty day gives you.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85}},
  {"id": 20, "titulo": "Forced smile", "titulo_en": "Forced smile", "descripcion": "Draw a big smile on your face and keep it fixed for fifteen full seconds at this moment. This small gesture lets your mind know it is time to be in total well-being.", "descripcion_en": "Draw a big smile on your face and keep it fixed for fifteen full seconds at this moment. This small gesture lets your mind know it is time to be in total well-being.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "salud": 80}},
  {"id": 21, "titulo": "Gratitude", "titulo_en": "Gratitude", "descripcion": "Close your eyes in complete silence in your living room. Think carefully about a single good and beautiful thing that has happened to you this week and give thanks in your calm mind.", "descripcion_en": "Close your eyes in complete silence in your living room. Think carefully about a single good and beautiful thing that has happened to you this week and give thanks in your calm mind.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60}},
  {"id": 22, "titulo": "Eye relax", "titulo_en": "Eye relax", "descripcion": "Rub the palms of your hands to warm the skin immediately. Place them gently over your closed eyes and enjoy a full minute of darkness and total rest inside your quiet room.", "descripcion_en": "Rub the palms of your hands to warm the skin immediately. Place them gently over your closed eyes and enjoy a full minute of darkness and total rest inside your quiet room.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "salud": 70, "naturaleza": 20}},
  {"id": 23, "titulo": "Heart rate", "titulo_en": "Heart rate", "descripcion": "Place your right hand in the center of your chest peacefully. Feel the steady and peaceful beat of your heart. Remember that this is the beautiful engine of your life now.", "descripcion_en": "Place your right hand in the center of your chest peacefully. Feel the steady and peaceful beat of your heart. Remember that this is the beautiful engine of your life now.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "salud": 70, "movimiento": 10}},
  {"id": 24, "titulo": "Neck release", "titulo_en": "Neck release", "descripcion": "Move your head drawing very slow and gentle circles in the air. Feel how all the tension built up in your neck from looking at the phone goes away inside your home.", "descripcion_en": "Move your head drawing very slow and gentle circles in the air. Feel how all the tension built up in your neck from looking at the phone goes away inside your home.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "salud": 90, "silencio": 70, "organizacion": 30}},
  {"id": 25, "titulo": "Palm exercise", "titulo_en": "Palm exercise", "descripcion": "Rub your hands with energy until you feel the warmth on your skin. Immediately place your palms on your shoulders to give yourself a comforting hug at this exact present moment.", "descripcion_en": "Rub your hands with energy until you feel the warmth on your skin. Immediately place your palms on your shoulders to give yourself a comforting hug at this exact present moment.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 85, "silencio": 60, "contemplacion": 50}},
  {"id": 26, "titulo": "Distant sounds", "titulo_en": "Distant sounds", "descripcion": "Stay still for a few moments in your living room and pay close attention to your surroundings. Try to identify the furthest sound that can be heard outside your house in this peaceful instant.", "descripcion_en": "Stay still for a few moments in your living room and pay close attention to your surroundings. Try to identify the furthest sound that can be heard outside your house in this peaceful instant.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70}},
  {"id": 27, "titulo": "Lateral stretch", "titulo_en": "Lateral stretch", "descripcion": "Tilt your body very gently to the right side and then to the left with complete calm. Feel how your waist stretches with total comfort and muscular lightness inside your room.", "descripcion_en": "Tilt your body very gently to the right side and then to the left with complete calm. Feel how your waist stretches with total comfort and muscular lightness inside your room.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
  {"id": 28, "titulo": "The empty glass", "titulo_en": "The empty glass", "descripcion": "Look for a clear glass in your kitchen. Observe its shape and how the light enters it for one full minute. Notice the beautiful reflections in absolute silence and clear your mind.", "descripcion_en": "Look for a clear glass in your kitchen. Observe its shape and how the light enters it for one full minute. Notice the beautiful reflections in absolute silence and clear your mind.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70}},
  {"id": 29, "titulo": "Jaw release", "titulo_en": "Jaw release", "descripcion": "Open your mouth wide carefully in your cozy corner. Move your jaw slowly from one side to the other. Feel how all the stiffness and accumulated tension leaves your face.", "descripcion_en": "Open your mouth wide carefully in your cozy corner. Move your jaw slowly from one side to the other. Feel how all the stiffness and accumulated tension leaves your face.", "vector_necesidades": {"movimiento": 80, "salud": 90, "risa": 70, "descanso": 80, "silencio": 60}},
  {"id": 30, "titulo": "Slow steps", "titulo_en": "Slow steps", "descripcion": "Stand up gently in your safe space. Take ten very slow and quiet steps inside your current room. Feel the full support of each foot as you walk with calm.", "descripcion_en": "Stand up gently in your safe space. Take ten very slow and quiet steps inside your current room. Feel the full support of each foot as you walk with calm.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60}},
  {"id": 31, "titulo": "Gentle massage", "titulo_en": "Gentle massage", "descripcion": "Place your fingertips on your temples right now. Draw very slow and tender circles without pressing hard. Feel the immediate relief in your head and relax your thoughts.", "descripcion_en": "Place your fingertips on your temples right now. Draw very slow and tender circles without pressing hard. Feel the immediate relief in your head and relax your thoughts.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
  {"id": 32, "titulo": "Air awareness", "titulo_en": "Air awareness", "descripcion": "Pay attention to your nose at this moment. Feel the fresh air coming in as you breathe in and the warm air coming out as you let it go. Do it naturally in your space.", "descripcion_en": "Pay attention to your nose at this moment. Feel the fresh air coming in as you breathe in and the warm air coming out as you let it go. Do it naturally in your space.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70}},
  {"id": 33, "titulo": "Firm back", "titulo_en": "Firm back", "descripcion": "Bring your shoulders gently back and open your chest lightly at this instant. Feel how your body recovers its natural, straight and comfortable posture inside your house.", "descripcion_en": "Bring your shoulders gently back and open your chest lightly at this instant. Feel how your body recovers its natural, straight and comfortable posture inside your house.", "vector_necesidades": {"movimiento": 85, "salud": 90, "organizacion": 70, "descanso": 70, "esperanza": 60}},
  {"id": 34, "titulo": "Total support", "titulo_en": "Total support", "descripcion": "Take a seat quietly and relax your back. Feel how the chair holds all the weight of your body with total safety. Release your muscles now and truly rest.", "descripcion_en": "Take a seat quietly and relax your back. Feel how the chair holds all the weight of your body with total safety. Release your muscles now and truly rest.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10}},
  {"id": 35, "titulo": "Countdown", "titulo_en": "Countdown", "descripcion": "Count the numbers backwards, starting from twenty until you reach one. Do it very slowly in your mind to calm all your thoughts and find absolute peace.", "descripcion_en": "Count the numbers backwards, starting from twenty until you reach one. Do it very slowly in your mind to calm all your thoughts and find absolute peace.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70}},
  {"id": 36, "titulo": "Touch texture", "titulo_en": "Touch texture", "descripcion": "Pass your fingertips over a real surface nearby, such as a wooden table or a piece of clean cloth. Notice its texture with absolute calm.", "descripcion_en": "Pass your fingertips over a real surface nearby, such as a wooden table or a piece of clean cloth. Notice its texture with absolute calm.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70}},
  {"id": 37, "titulo": "Stretch fingers", "titulo_en": "Stretch fingers", "descripcion": "Separate and stretch your fingers as much as you can for five whole seconds with energy. Afterwards, relax them completely so they can rest from screens at this instant.", "descripcion_en": "Separate and stretch your fingers as much as you can for five whole seconds with energy. Afterwards, relax them completely so they can rest from screens at this instant.", "vector_necesidades": {"movimiento": 90, "salud": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
  {"id": 38, "titulo": "Internal sound", "titulo_en": "Internal sound", "descripcion": "Stay in silence in your cozy corner and listen to the soft sound of your own breathing. Do not try to force it or change it, just notice how your body breathes on its own.", "descripcion_en": "Stay in silence in your cozy corner and listen to the soft sound of your own breathing. Do not try to force it or change it, just notice how your body breathes on its own.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "salud": 85, "naturaleza": 60}},
  {"id": 39, "titulo": "Fixed gaze", "titulo_en": "Fixed gaze", "descripcion": "Look for a small spot or a mark on the wall in front of you. Keep looking at that fixed place peacefully, allowing your eyes to focus far away from the screens.", "descripcion_en": "Look for a small spot or a mark on the wall in front of you. Keep looking at that fixed place peacefully, allowing your eyes to focus far away from the screens.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75}},
  {"id": 40, "titulo": "Drop arms", "titulo_en": "Drop arms", "descripcion": "Let your arms hang completely loose at the sides of your body in your living room. Shake them very gently to remove any trace of accumulated heaviness.", "descripcion_en": "Let your arms hang completely loose at the sides of your body in your living room. Shake them very gently to remove any trace of accumulated heaviness.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "salud": 85, "risa": 60, "juego": 50}},
  {"id": 41, "titulo": "Clothing contact", "titulo_en": "Clothing contact", "descripcion": "Close your eyes for a moment in your seat. Try to notice the subtle sensation and smooth weight of your clothes resting on the skin of your shoulders and arms.", "descripcion_en": "Close your eyes for a moment in your seat. Try to notice the subtle sensation and smooth weight of your clothes resting on the skin of your shoulders and arms.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10}},
  {"id": 42, "titulo": "Deep air", "titulo_en": "Deep air", "descripcion": "Breathe in slowly inflating your belly in your safe space, hold the air for three seconds, and then release it very gently through your mouth with calm.", "descripcion_en": "Breathe in slowly inflating your belly in your safe space, hold the air for three seconds, and then release it very gently through your mouth with calm.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
  {"id": 43, "titulo": "Shoulder rotation", "titulo_en": "Shoulder rotation", "descripcion": "Raise your shoulders slowly as if you wanted to touch your ears, hold the strength for a moment, and let them drop suddenly to release the day's load in your house.", "descripcion_en": "Raise your shoulders slowly as if you wanted to touch your ears, hold the strength for a moment, and let them drop suddenly to release the day's load in your house.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
  {"id": 44, "titulo": "Listen to silence", "titulo_en": "Listen to silence", "descripcion": "Stay in complete calm for a few moments in your room and try to listen to the small space of silence that happens between each natural breath in peace.", "descripcion_en": "Stay in complete calm for a few moments in your room and try to listen to the small space of silence that happens that happens between each natural breath in peace.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70}},
  {"id": 45, "titulo": "Ceiling gaze", "titulo_en": "Ceiling gaze", "descripcion": "Look up toward the ceiling gently in your seat. Stretch your neck with total comfort without lifting or moving your shoulders at all.", "descripcion_en": "Look up toward the ceiling gently in your seat. Stretch your neck with total comfort without lifting or moving your shoulders at all.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "salud": 80, "contemplacion": 70, "silencio": 60}},
  {"id": 46, "titulo": "Feel the base", "titulo_en": "Feel the base", "descripcion": "Pay attention to the back of your legs right now. Notice the firm and secure contact they make against the seat of your chair in your dining room.", "descripcion_en": "Pay attention to the back of your legs right now. Notice the firm and secure contact they make against the seat of your chair in your dining room.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20}},
  {"id": 48, "titulo": "Mental cleansing", "titulo_en": "Mental cleansing", "descripcion": "Imagine that as you release your breath you take out from your body any boring and heavy worry in your home, leaving it completely outside of you in this second.", "descripcion_en": "Imagine that as you release your breath you take out from your body any boring and heavy worry in your home, leaving it completely outside of you in this second.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60}},
  {"id": 49, "titulo": "Touch the table", "titulo_en": "Touch the table", "descripcion": "Place the palms of your open hands on the table. Feel the firmness of the piece of furniture of your house and connect with that feeling of stability.", "descripcion_en": "Place the palms of your open hands on the table. Feel the firmness of the piece of furniture of your house and connect with that feeling of stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30}},
  {"id": 50, "titulo": "Total presence", "titulo_en": "Total presence", "descripcion": "Remember that you are here at this moment, you are completely safe in the shelter of your home, and you have control of your tranquility.", "descripcion_en": "Remember that you are here at this moment, you are completely safe in the shelter of your home, and you have control of your tranquility.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70}},
  {"id": 51, "titulo": "Sing a melody", "titulo_en": "Sing a melody", "descripcion": "Hum your favorite song very softly and quietly in your room. Stop thinking about your tasks and simply enjoy the music in absolute peace.", "descripcion_en": "Hum your favorite song very softly and quietly in your room. Stop thinking about your tasks and simply enjoy the music in absolute peace.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50}},
  {"id": 52, "titulo": "Write 3 wishes", "titulo_en": "Write 3 wishes", "descripcion": "Take a white piece of paper at your desk and write down three simple and beautiful things you would like to fulfill or enjoy during the hours of today calmly.", "descripcion_en": "Take a white piece of paper at your desk and write down three simple and beautiful things you would like to fulfill or enjoy during the hours of today calmly.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70}},
  {"id": 53, "titulo": "Hallway stroll", "titulo_en": "Hallway stroll", "descripcion": "Walk slowly and with very soft steps along the hallway of your house, paying close attention to how you support each foot as you move along.", "descripcion_en": "Walk slowly and with very soft steps along the hallway of your house, paying close attention to how you support each foot as you move along.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50}},
  {"id": 54, "titulo": "Look at a plant", "titulo_en": "Look at a plant", "descripcion": "Look for a plant or a green leaf nearby in your living room. Observe its colors and shapes in close detail for one minute in silence.", "descripcion_en": "Look for a plant or a green leaf nearby in your living room. Observe its colors and shapes in close detail for one minute in silence.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60}},
  {"id": 55, "titulo": "Draw a circle", "titulo_en": "Draw a circle", "descripcion": "Take a pencil and draw round circles on a sheet of paper very quietly, focusing only on the steady stroke of your hand inside your house.", "descripcion_en": "Take a pencil and draw round circles on a sheet of paper very quietly, focusing only on the steady stroke of your hand inside your house.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
  {"id": 57, "titulo": "Open a book at random", "titulo_en": "Open a book at random", "descripcion": "Take a book nearby from your shelf, open any page without looking, and read carefully the first phrase your eyes find right away.", "descripcion_en": "Take a book nearby from your shelf, open any page without looking, and read carefully the first phrase your eyes find right away.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60}},
  {"id": 58, "titulo": "Listen to the rain", "titulo_en": "Listen to the rain", "descripcion": "Open your window carefully and listen to the peaceful sound of the drops falling against the ground or surfaces for a moment in complete quietness.", "descripcion_en": "Open your window carefully and listen to the peaceful sound of the drops falling against the ground or surfaces for a moment in complete quietness.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85}},
  {"id": 59, "titulo": "Dance without music", "titulo_en": "Dance without music", "descripcion": "Stand up in your room and move your body freely for one full minute. Do it with joy and ease, as if nobody were watching you.", "descripcion_en": "Stand up in your room and move your body freely for one full minute. Do it with joy and ease, as if nobody were watching you.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50}},
  {"id": 60, "titulo": "Drink a herbal tea", "titulo_en": "Drink a herbal tea", "descripcion": "Prepare a cup of tea or a hot herbal infusion in your kitchen. Take small sips very slowly, feeling the comforting warmth entering your body.", "descripcion_en": "Prepare a cup of tea or a hot herbal infusion in your kitchen. Take small sips very slowly, feeling the comforting warmth entering your body.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "salud": 70, "contemplacion": 70}},
  {"id": 61, "titulo": "Look at your hands", "titulo_en": "Look at your hands", "descripcion": "Extend your hands in front of you in your seat. Closely observe each of the lines, fingers, and tiny details of your human skin.", "descripcion_en": "Extend your hands in front of you in your seat. Closely observe each of the lines, fingers, and tiny details of your human skin.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50}},
  {"id": 62, "titulo": "Imagine a landscape", "titulo_en": "Imagine a landscape", "descripcion": "Close your eyes gently on your couch. Imagine that you are walking through your favorite nature spot, like a forest or a quiet beach today.", "descripcion_en": "Close your eyes gently on your couch. Imagine that you are walking through your favorite nature spot, like a forest or a quiet beach today.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80}},
  {"id": 63, "titulo": "Stretch your back", "titulo_en": "Stretch your back", "descripcion": "Sit on the floor of your living room with your legs well stretched forward. Slowly bring your hands forward and try to touch your feet.", "descripcion_en": "Sit on the floor of your living room with your legs well stretched forward. Slowly bring your hands forward and try to touch your feet.", "vector_necesidades": {"movimiento": 90, "salud": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
  {"id": 64, "titulo": "Breathe through your nose", "titulo_en": "Breathe through your nose", "descripcion": "Breathe in very deeply and slowly using only your nose while sitting on your chair. Feel how the fresh air comes in and do it five times in a row to calm yourself.", "descripcion_en": "Breathe in very deeply and slowly using only your nose while sitting on your chair. Feel how the fresh air comes in and do it five times in a row to calm yourself.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "aire_fresco": 80, "contemplacion": 90}},
  {"id": 65, "titulo": "Shadow play", "titulo_en": "Shadow play", "descripcion": "Turn on a small lamp in front of a clean wall in your room. Use your hands and fingers to make up fun little animal shapes using the light shadows beautifully.", "descripcion_en": "Turn on a small lamp in front of a clean wall in your room. Use your hands and fingers to make up fun little animal shapes using the light shadows beautifully.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50}},
  {"id": 66, "titulo": "An imaginary hug", "titulo_en": "An imaginary hug", "descripcion": "Cross your arms over your chest while sitting on your couch and squeeze yourself tightly. Imagine with much affection that you are receiving a nice hug from a loved one.", "descripcion_en": "Cross your arms over your chest while sitting on your couch and squeeze yourself tightly. Imagine with much affection that you are receiving a nice hug from a loved one.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50}},
  {"id": 67, "titulo": "Find a blue object", "titulo_en": "Find a blue object", "descripcion": "Look around you quickly inside your living room. Try to discover five different objects that are blue to train your mindful attention with complete peace of mind today.", "descripcion_en": "Look around you quickly inside your living room. Try to discover five different objects that are blue to train your mindful attention with complete peace of mind today.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
  {"id": 69, "titulo": "Observe the sky", "titulo_en": "Observe the sky", "descripcion": "Look out the window of your room for a moment. Calmly look up toward the outer horizon and stay observing the clear sky for one full minute in peace.", "descripcion_en": "Look out the window of your room for a moment. Calmly look up toward the outer horizon and stay observing the clear sky for one full minute in peace.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70}},
  {"id": 70, "titulo": "Facial massage", "titulo_en": "Facial massage", "descripcion": "Use your fingertips to give yourself a very gentle face massage in front of your mirror. Draw peaceful circles across your forehead, cheeks, and jaw in complete silence.", "descripcion_en": "Use your fingertips to give yourself a very gentle face massage in front of your mirror. Draw peaceful circles across your forehead, cheeks, and jaw in complete silence.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
  {"id": 71, "titulo": "Close your eyes and listen", "titulo_en": "Close your eyes and listen", "descripcion": "Take a very comfortable position in your resting seat and close your eyes gently. Pay close attention and try to identify three different sounds happening inside the house.", "descripcion_en": "Take a very comfortable position in your resting seat and close your eyes gently. Pay close attention and try to identify three different sounds happening inside the house.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60}},
  {"id": 72, "titulo": "Tense and relax your feet", "titulo_en": "Tense and relax your feet", "descripcion": "Tightly squeeze the toes of both your feet inward on your rug for five full seconds to build up tension. Afterwards, release them all at once to let them rest.", "descripcion_en": "Tightly squeeze the toes of both your feet inward on your rug for five full seconds to build up tension. Afterwards, release them all at once to let them rest.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "salud": 70, "organizacion": 40, "silencio": 50}},
  {"id": 74, "titulo": "Mindful scent", "titulo_en": "Mindful scent", "descripcion": "Look for something in your pantry that has a pleasant aroma you like a lot, such as a coffee bean or a spice. Bring it close to your nose and focus.", "descripcion_en": "Look for something in your pantry that has a pleasant aroma you like a lot, such as a coffee bean or a spice. Bring it close to your nose and focus.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70}},
  {"id": 75, "titulo": "Copy a simple drawing", "titulo_en": "Copy a simple drawing", "descripcion": "Look for a small and very simple drawing in a magazine or a book on your table. Take a pencil and try to copy its lines on paper peacefully.", "descripcion_en": "Look for a small and very simple drawing in a magazine or a book on your table. Take a pencil and try to copy its lines on paper peacefully.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50}},
  {"id": 76, "titulo": "Find three red objects", "titulo_en": "Find three red objects", "descripcion": "Look around you quickly inside your current room. Try to discover three different objects that are red to activate your mindful focus in total calm today.", "descripcion_en": "Look around you quickly inside your current room. Try to discover three different objects that are red to activate your mindful focus in total calm today.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70}},
  {"id": 78, "titulo": "Write a beautiful word", "titulo_en": "Write a beautiful word", "descripcion": "Take a pen and write a beautiful word you like a lot on a clean paper, such as Peace or Calm. Draw large and neat letters at your desk.", "descripcion_en": "Take a pen and write a beautiful word you like a lot on a clean paper, such as Peace or Calm. Draw large and neat letters at your desk.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 100, "contemplacion": 60}},
  {"id": 79, "titulo": "Hand massage", "titulo_en": "Hand massage", "descripcion": "Use the thumb of your right hand to give a gentle massage to the palm of your left hand. Draw slow circles across the entire skin with great tenderness in your seat.", "descripcion_en": "Use the thumb of your right hand to give a gentle massage to the palm of your left hand. Draw slow circles across the entire skin with great tenderness in your seat.", "vector_necesidades": {"descanso": 100, "salud": 90, "silencio": 85, "movimiento": 30, "contemplacion": 60}},
  {"id": 81, "titulo": "Lateral neck stretch", "titulo_en": "Lateral neck stretch", "descripcion": "Tilt your head slowly bringing your right ear toward your right shoulder without lifting your shoulders. Hold the posture for three seconds and switch sides gently on your couch.", "descripcion_en": "Tilt your head slowly bringing your right ear toward your right shoulder without lifting your shoulders. Hold the posture for three seconds and switch sides gently on your couch.", "vector_necesidades": {"movimiento": 85, "salud": 90, "descanso": 80, "silencio": 70, "organizacion": 20}},
  {"id": 82, "titulo": "Observe a shadow", "titulo_en": "Observe a shadow", "descripcion": "Look for a shadow projected on the floor or wall of your current room. Closely observe its dark edges and shapes in absolute silence for one full minute.", "descripcion_en": "Look for a shadow projected on the floor or wall of your current room. Closely observe its dark edges and shapes in absolute silence for one full minute.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 50, "descanso": 75, "naturaleza": 20}},
  {"id": 83, "titulo": "Feel your heartbeat", "titulo_en": "Feel your heartbeat", "descripcion": "Place two of your fingers gently on your left wrist or on your neck in your cozy corner. Stay still feeling the steady and strong beat of your biological pulse.", "descripcion_en": "Place two of your fingers gently on your left wrist or on your neck in your cozy corner. Stay still feeling the steady and strong beat of your biological pulse.", "vector_necesidades": {"contemplacion": 100, "silencio": 95, "descanso": 90, "salud": 90, "movimiento": 10}},
  {"id": 159, "titulo": "THE BREATHING CHALLENGE", "titulo_en": "THE BREATHING CHALLENGE", "descripcion": "Stay seated in a very comfortable posture in your living room. Take five deep and slow breaths through your nose, feeling how the pure air enters your body. Nothing more.", "descripcion_en": "Stay seated in a very comfortable posture in your living room. Take five deep and slow breaths through your nose, feeling how the pure air enters your body. Nothing more.", "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90, "contemplacion": 90, "aire_fresco": 80}},
  {"id": 160, "titulo": "THE VISUAL REST CHALLENGE", "titulo_en": "THE VISUAL REST CHALLENGE", "descripcion": "Look for a spot or an object that is very far away from you through your bedroom window. Keep your eyes on that place fixedly for two minutes to rest your eyes from screens completely.", "descripcion_en": "Look for a spot or an object that is very far away from you through your bedroom window. Keep your eyes on that place fixedly for two minutes to rest your eyes from screens completely.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "salud": 80}}
   ],
    "SALIR": {
        "agotado": [
            {"id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade", "porque": "Hoy busca un árbol majestuoso en un parque vibrante. Si tu mente está cansada de pantallas y tu cuerpo necesita desconectar del ritmo digital, camina lento. Acércate a su tronco, toca su corteza y disfruta su sombra fresca en silencio reparador. Levántate, siente el aire puro y contempla la naturaleza. Rompe la rutina y descansa. Tu respiración se equilibra plenamente aquí.", "porque_en": "Today, find a majestic tree in a vibrant park. If your mind is tired of screens and your body needs a digital detox, walk slowly. Approach its robust trunk, touch its ancient bark, and enjoy its cool shade in restorative silence. Get up now, feel the pure air, and contemplate nature. Break your routine, truly rest. Your breathing finds perfect balance in this peaceful refuge.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Un parque verde.", "donde_en": "A green park.", "gps": "parks with shade", "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "descanso": 90, "organizacion": 20, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85}},
            {"id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe", "porque": "Hoy visita una cafetería local pacífica. Si tu mente necesita un respiro del ruido y busca paz interior, dirígete allí sin prisa. Pide tu bebida, siéntate cómodamente y observa el entorno con calma, guarda tu teléfono. Levántate, regálate este descanso mental y disfruta el silencio sereno. Rompe la rutina, recarga energías. Siente el calor de tu taza y conecta con el presente.", "porque_en": "Today, visit a peaceful local cafe. If your mind needs a break from noise and seeks inner peace, go without rush. Order your favorite drink, sit comfortably, and observe calmly, keeping your phone away. Get up, grant yourself this mental rest, and enjoy the serene silence. Break the routine, recharge energies. Feel your cup's warmth and deeply connect with the present.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Establecimiento local pacífico.", "donde_en": "Peaceful local establishment.", "gps": "quiet cafe", "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 90, "agua": 30, "sol": 30, "sombra": 80, "aire_fresco": 40, "creatividad": 60, "comunidad": 50, "aprendizaje": 70, "juego": 10, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "musica": 40, "risa": 20, "esperanza": 70}},
            {"id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden", "porque": "Hoy explora un paraje botánico expansivo. Si tu cerebro está agotado y necesitas reconectar con plantas para respirar aire puro, camina pausado. Contempla la variedad de hojas y respira hondo. Levántate, abraza esta tregua natural, deja que tu mente descanse de obligaciones. Este oasis tranquilo te restaurará. Siente el suelo firme, vive el instante plenamente.", "porque_en": "Today, explore a vast botanical site. If your brain is exhausted and needs to reconnect with plants for pure air, stroll slowly. Contemplate the fascinating leaves, breathe deeply. Get up, embrace this natural truce, let your mind rest from obligations. This quiet oasis will restore you. Feel the firm ground, live this instant fully.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Paraje botánico público.", "donde_en": "Public botanical site.", "gps": "botanical garden", "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "agua": 50, "sol": 70, "sombra": 90, "aire_fresco": 100, "creatividad": 80, "comunidad": 40, "aprendizaje": 80, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 30, "alimentacion": 10, "musica": 50, "risa": 30, "esperanza": 90}},
            {"id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook", "porque": "Hoy busca un lugar alto en la ciudad. Si tu mente necesita una nueva perspectiva, eleva tu mirada. Observa fijamente la vasta línea del horizonte y siente la inmensidad del entorno con tranquilidad. Levántate, dirígete a un mirador público y contempla el majestuoso paisaje para romper la rutina. Siente el viento fresco, recupera tu centro en paz, renovado.", "porque_en": "Today, find a high spot in the city. If your mind needs a new perspective, elevate your gaze. Observe the vast horizon, feel the immensity of your surroundings in peace. Get up, head to a public overlook, and contemplate the majestic scenery to break your routine. Feel the fresh air, recover your core in total quietness, deeply renewed.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook", "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "agua": 60, "sol": 80, "sombra": 50, "aire_fresco": 95, "creatividad": 70, "comunidad": 30, "aprendizaje": 50, "juego": 10, "contemplacion": 100, "descanso": 70, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 95}},
            {"id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class", "porque": "Hoy busca un momento tranquilo en un centro de meditación. Si tu mente está sobrecargada, halla calma interna para regular tu cuerpo. Concéntrate en el aire entrando y saliendo, suelta preocupaciones y tensiones. Levántate, regálate este descanso mental profundo, habita el silencio absoluto. Rompe la rutina. Siente los latidos serenos de tu corazón y relájate en este espacio.", "porque_en": "Today, find a quiet moment in a meditation center. If your mind is overloaded, find inner calm to regulate your body. Concentrate on your breath, let go of worries and tension. Get up, grant yourself this deep mental rest, inhabit absolute silence. Break the routine. Feel your serene heartbeat and truly relax in this sacred space.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class", "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 100, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 60, "creatividad": 50, "comunidad": 60, "aprendizaje": 90, "juego": 5, "contemplacion": 100, "descanso": 100, "organizacion": 80, "alimentacion": 0, "musica": 70, "risa": 5, "esperanza": 90}},
            {"id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing", "porque": "Hoy busca un espacio abierto en un parque o campo. Si tus pensamientos están agitados, mira el cielo. Enfoca tu mirada en su inmensidad para que tus ideas fluyan libremente. Recuéstate, observa las cambiantes formas de las nubes. Levántate, regálate este descanso contemplativo, respira aire puro para romper la rutina. Serena tu cuerpo. Siente el cielo azul sanando tu interior.", "porque_en": "Today, find an open space in a park or field. If your thoughts are racing, gaze at the sky. Focus on its vastness to let your ideas flow freely. Lie down, observe the ever-changing cloud shapes. Get up, grant yourself this contemplative rest, breathe pure air to break the routine. Calm your body. Feel the blue sky healing your inner being.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing", "vector_necesidades": {"movimiento": 20, "naturaleza": 95, "silencio": 90, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 90, "creatividad": 60, "comunidad": 10, "aprendizaje": 40, "juego": 20, "contemplacion": 100, "descanso": 95, "organizacion": 10, "alimentacion": 0, "musica": 20, "risa": 15, "esperanza": 85}},
            {"id": 355, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Hoy pide un viaje corto a la plaza o parque cercano con tu app. Si tus ojos y cuerpo están cansados del tráfico ruidoso, esta pausa te restaurará. En el auto, guarda el teléfono. Cierra los ojos un minuto, apoya tus manos y respira despacio. Siente el movimiento suave del vehículo mientras descansas tu mente segura. Tu recorrido revitalizante empieza ahora.", "porque_en": "Today, request a short trip to a nearby park with your app. If your eyes and body are tired from noisy traffic, this passive break will restore you. In the car, put your phone away. Close your eyes for one minute, rest your hands, and breathe slowly. Feel the gentle motion of the vehicle, resting your mind safely. Your journey begins now, offering deep peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cabina de transporte, parada o asiento de pasajero.", "donde_en": "Transit vehicle cabin, stop, or passenger seat.", "gps": "quiet public square", "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 15, "contemplacion": 85, "esperanza": 80, "salud": 80, "aire_fresco": 60}},
            {"id": 356, "titulo": "Módulo de Cambio Frecuencial", "titulo_en": "Frequency Shift Module", "porque": "Hoy abre tu app de música en tu espacio de descanso. Si tu mente está llena de pensamientos y tus oídos cansados de ruidos y pantallas, busca sonidos de la naturaleza, como pájaros o lluvia. Usa auriculares, apoya tu cabeza y respira profundo para que tu mente esté serena. Levántate, regálate este quiebre acústico. Tu respiración recupera su curso natural en paz interior.", "porque_en": "Today, open your music app in your resting space. If your mind is overloaded with thoughts and your ears tired from noise and screens, find nature sounds like birds or rain. Put on headphones, lean back, and breathe deeply for a serene mind. Get up, grant yourself this acoustic break. Your breathing will find its natural course in complete inner peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Tu espacio de descanso, oficina vacía o vehículo.", "donde_en": "Your resting space, empty office, or vehicle.", "gps": "quiet open park", "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 65, "contemplacion": 90, "esperanza": 85, "salud": 80, "creatividad": 40}},
            {"id": 357, "titulo": "Mapeo de Flujos", "titulo_en": "Flow Mapping", "porque": "Hoy camina hacia la tienda o almacén más grande cercano. Si llevas mucho tiempo sentado y tu cuerpo necesita mover las piernas para activar tu energía, camina tranquilo por los pasillos más largos. Observa los objetos, aprovecha este sitio fresco para estirar tus músculos. Levántate, rompe el piloto automático diario y activa tu musculatura de forma gratuita y revitalizante.", "porque_en": "Today, walk to the largest store or warehouse club nearby. If you've been sitting too long and your body needs to move for vital energy, walk steadily through the longest aisles. Observe items, use this cool indoor space to stretch limbs and muscles. Get up, break the daily automatic pilot, and activate your body's circulation completely free and revitalized.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Pasillos industriales de una gran tienda de tu Código Postal.", "donde_en": "Industrial aisles of a large warehouse store in your Zip Code.", "gps": "wholesale club or market", "vector_necesidades": {"movimiento": 85, "organizacion": 70, "contemplacion": 60, "comunidad": 50, "juego": 30, "descanso": 20, "silencio": 10}},
            {"id": 358, "titulo": "Oasis Burocrático", "titulo_en": "Bureaucratic Oasis", "porque": "Hoy visita la biblioteca pública más cercana. Ingresa despacio, en silencio. Si sientes cansancio mental por esperas, filas o letreros, toma asiento cómodo en la zona de lectura. Disfruta la tranquilidad absoluta, permite que tus ojos descansen de pantallas. Levántate, regálate este respiro intelectual, desconecta del ruido urbano. Tu mente recupera su claridad en este espacio sagrado y sereno.", "porque_en": "Today, find the nearest public library. Walk inside slowly, in silence. If you feel mental tiredness from waits, lines, or signs, take a comfortable seat in the reading room. Enjoy absolute quietness, let your eyes rest from screens. Get up, grant yourself this intellectual break, disconnect from urban rush. Your mind recovers clarity in this sacred, serene space.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sala de lectura, biblioteca municipal o zona de estudio de USA.", "donde_en": "Reading room, municipal library, or USA study zone.", "gps": "public library", "vector_necesidades": {"aprendizaje": 100, "silencio": 100, "contemplacion": 90, "descanso": 85, "organizacion": 70, "salud": 80}},
            {"id": 201, "titulo": "Soberanía en Tránsito", "titulo_en": "Transit Sovereignty", "porque": "Hoy abre tu app de transporte, pide un viaje corto a un rincón tranquilo. Si sientes el cuerpo cansado y la mente pesada por manejar o el tráfico, esta pausa pasiva te renovará. En el auto, guarda el teléfono, cierra los ojos un minuto. Descansa con las manos sobre tus rodillas. Siente el vaivén seguro del trayecto mientras el estrés se desvanece.", "porque_en": "Today, open your rideshare app and request a short trip to a quiet corner. If your body is tired and mind heavy from driving or traffic, this passive break will renew you. In the car, put your phone away, close your eyes for one minute. Rest with hands on your knees. Feel the safe movement as stress fades away.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cabina de transporte o asiento de pasajero.", "donde_en": "Rideshare cabin or passenger seat.", "gps": "quiet park bench", "vector_necesidades": {"descanso": 100, "silencio": 90, "movimiento": 10, "contemplacion": 80, "esperanza": 80, "naturaleza": 20, "aire_fresco": 50}},
            {"id": 202, "titulo": "Módulo Auditivo", "titulo_en": "Auditory Reset", "porque": "Hoy abre tu app de música en un rincón cómodo o en tu auto. Si tu mente está agotada por ruidos de la calle y pantallas, busca sonidos de lluvia o una melodía suave. Ponte auriculares, cierra los ojos un minuto. Permite que los sonidos tranquilos se lleven el cansancio. Levántate, abraza esta tregua acústica, siente la paz recuperando tu centro vital serenamente.", "porque_en": "Today, open your music app in a comfortable spot or your car. If your mind is exhausted from street noise and screens, find gentle rain sounds or a soft melody. Put on headphones, close your eyes for one minute. Let peaceful sounds take away tiredness. Get up, embrace this acoustic truce, feel peace recovering your inner core serenely.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cualquier rincón cómodo o dentro de tu auto.", "donde_en": "Any comfortable spot or inside your car.", "gps": "quiet library space", "vector_necesidades": {"musica": 100, "descanso": 95, "silencio": 60, "contemplacion": 90, "esperanza": 85, "creatividad": 40}},
            {"id": 203, "titulo": "Descompresión de Entorno", "titulo_en": "Environment Decompression", "porque": "Hoy busca un hotel cercano, camina tranquilo hacia su vestíbulo. Si sientes aburrimiento de estar encerrado y tu cuerpo pide un espacio ordenado, toma asiento cómodo. Apoya tus pies, descansa tu mirada contemplando un punto lejano por dos minutos. Levántate, regálate este quiebre espacial, permite que tu respiración recupere su curso natural en paz. Tu mente se renueva en este entorno sereno.", "porque_en": "Today, find a nearby hotel, walk peacefully to its lobby. If you feel bored and your body needs an orderly space, take a comfortable seat. Place your feet flat, rest your eyes on a distant spot for two minutes. Get up, grant yourself this spatial break, let your breathing find its natural course in peace. Your mind renews in this elegant, serene environment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Lobby o zona de descanso de un hotel local.", "donde_en": "Lobby or lounge area of a local hotel.", "gps": "hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 70, "esperanza": 80, "movimiento": 20}},
            {"id": 204, "titulo": "Sabotaje de Espera", "titulo_en": "Waiting Sabotage", "porque": "Hoy dirígete al patio o zona de libros de una escuela cercana. Si tu mente está atrapada en el teléfono y necesitas alimentar tu imaginación con ideas nuevas, camina despacio y en silencio por sus senderos. Respira aire fresco, observa los árboles con tranquilidad, desconéctate de pantallas. Levántate, regálate este respiro intelectual, rompe el piloto automático para reconectar con tu creatividad. Empieza ya.", "porque_en": "Today, head to a nearby school's courtyard or book section. If your mind is phone-trapped and needs new ideas, walk slowly and silently along its paths. Breathe fresh air, observe trees peacefully, disconnect from screens. Get up, grant yourself this intellectual break, break the automatic pilot to reconnect with creativity. Your wellness journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Campus universitario o biblioteca pública.", "donde_en": "University campus or public library.", "gps": "university library", "vector_necesidades": {"aprendizaje": 100, "silencio": 90, "contemplacion": 85, "descanso": 70, "aire_fresco": 75, "movimiento": 40}}
        ],
        "estresado": [
            {"id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk", "porque": "Hoy busca una rampa o escaleras públicas al aire libre. Si tu musculatura está tensa por preocupaciones y necesitas liberar esa energía, sube a paso firme. Siente el impulso dinámico y la fuerza de tu cuerpo en cada pisada. Levántate, regálate esta pausa activa. Tu respiración se acelerará saludablemente. Rompe el estrés, quema la carga mental y reconecta con tu poder físico.", "porque_en": "Today, find a sloped ramp or public stairs outdoors. If your muscles are tense from worries and you need to release heavy energy, walk up steadily. Feel your body's dynamic push and strength in each stride. Get up, grant yourself this active break. Your breathing will increase healthily. Break daily stress, burn mental load, and reconnect with your physical power.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Escalera pública.", "donde_en": "Public stairs.", "gps": "public stairs", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75}},
            {"id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga", "porque": "Hoy busca un parque tranquilo y natural. Si tu mente corre rápido y necesitas unir movimientos con la naturaleza para respirar en calma, extiende una manta. Haz estiramientos suaves, siente el aire fresco en tu rostro. Levántate, regálate este respiro corporal, permite que la quietud repare tu balance interno. Rompe el piloto automático, libérate del estrés y conecta con tu presente sin apuros.", "porque_en": "Today, find a quiet natural park. If your mind races and you need to unite movements with nature to breathe calmly, lay a mat. Do gentle stretches, feel fresh air on your face. Get up, grant yourself this bodily break, let the stillness repair your inner balance. Break the automatic pilot, release stress, and connect deeply with your present without hurry.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park", "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 70, "sombra": 60, "aire_fresco": 95, "creatividad": 60, "comunidad": 40, "aprendizaje": 50, "juego": 10, "contemplacion": 80, "descanso": 70, "organizacion": 50, "alimentacion": 0, "musica": 40, "risa": 20, "esperanza": 80}},
            {"id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym", "porque": "Hoy visita un centro deportivo o parque con aparatos. Si tienes energía acumulada y necesitas transformar problemas en fuerza física, mueve piernas y brazos constante y rítmicamente. Siente el motor de tu cuerpo encenderse. Levántate, regálate esta descarga dinámica. La fatiga mental se disolverá con esfuerzo físico controlado. Rompe la rutina, libera tensión y recupera tu poder corporal con vitalidad.", "porque_en": "Today, visit a sports center or park with exercise equipment. If you have built-up energy and need to transform problems into physical strength, move your legs and arms steadily and rhythmically. Feel your body's active engine turn on. Get up, grant yourself this dynamic discharge. Mental fatigue will dissolve through controlled physical effort. Break your routine, release tension, and recover your bodily power with vitality.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym", "vector_necesidades": {"movimiento": 100, "naturaleza": 5, "silencio": 20, "agua": 10, "sol": 20, "sombra": 80, "aire_fresco": 60, "creatividad": 20, "comunidad": 70, "aprendizaje": 40, "juego": 30, "contemplacion": 5, "descanso": 0, "organizacion": 80, "alimentacion": 0, "musica": 80, "risa": 40, "esperanza": 60}},
            {"id": 320, "titulo": "Liberación de Impacto", "titulo_en": "Impact Release", "porque": "Hoy busca un parque de trampolines o centro de juegos con colchonetas. Si tus músculos están rígidos por tensión y tu cuerpo necesita soltar enojo, salta con alegría. Descarga tu peso en la lona elástica. Sube un muro usando fuerza y agilidad. Levántate, regálate este espacio de descarga física. Permite que tu respiración se acelere felizmente. Rompe el estrés y reconecta con tu vitalidad y energía.", "porque_en": "Today, find the nearest trampoline park or play center with mats. If your muscles are stiff from tension and your body needs to release anger, jump with joy. Launch your weight onto the elastic canvas. Have fun climbing a safe wall using strength and agility. Get up, grant yourself this high physical discharge space. Let your breathing increase happily. Break accumulated stress and reconnect with your full vitality and energy.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque de trampolines o centro deportivo de alta descarga en tu Código Postal.", "donde_en": "Trampoline park or high-discharge sports center in your Zip Code.", "gps": "trampoline park or climbing gym", "vector_necesidades": {"movimiento": 100, "juego": 100, "risa": 90, "salud": 95, "descanso": 0, "silencio": 10, "comunidad": 60, "esperanza": 90}},
            {"id": 321, "titulo": "Módulo de Hidro-Calma", "titulo_en": "Hydro-Calm Module", "porque": "Hoy visita el centro deportivo con piscina o la YMCA cercana. Si tu cuerpo está cansado por preocupaciones y ruidos, el agua templada es perfecta para un descanso. Entra al agua climatizada, cierra tus ojos. Deja que las burbujas te den un masaje mientras flotas plácidamente. Levántate, regálate este quiebre de hidroterapia pasiva. Permite que tu respiración se equilibre con la calma del agua. Tu cuerpo y mente se relajan.", "porque_en": "Today, visit the nearest community pool or YMCA. If your body is tired from worries and loud noises, warm water is perfect for a comforting rest. Enter the heated water, close your eyes. Let gentle bubbles massage your back as you float placidly. Get up, grant yourself this passive hydrotherapy break. Allow your breathing to balance with the water's calm. Your body and mind relax.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "YMCA, alberca climatizada o spa comunitario local.", "donde_en": "YMCA, heated pool, or local community spa.", "gps": "ymca pool or public spa", "vector_necesidades": {"agua": 100, "descanso": 100, "salud": 95, "silencio": 60, "contemplacion": 90, "sombra": 80, "esperanza": 85, "movimiento": 20}},
            {"id": 322, "titulo": "Quiebre de Frecuencias", "titulo_en": "Frequency Break", "porque": "Hoy busca un centro de meditación o yoga cercano para equilibrarte. Si tu mente corre rápido por el teléfono y necesitas calmar tus pensamientos, entra despacio a su sala de espera. Toma asiento cómodo, cierra tus ojos en silencio. Respira lento y suave, sintiendo cada inhalación. Levántate, regálate este descanso mental profundo. Habita el silencio absoluto para romper el piloto automático. Tu mente sana en este entorno sereno.", "porque_en": "Today, find a nearby meditation center or yoga studio for balance. If your mind races from phone use and needs quiet to calm thoughts, walk slowly into its waiting area. Take a comfortable seat, close your eyes in silence. Breathe slowly and gently, feeling each breath. Get up, grant yourself this deep mental rest. Inhabit absolute acoustic silence to break the automatic pilot. Your mind heals in this serene environment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Estudio de yoga, centro de meditación o sound healing en USA.", "donde_en": "Yoga studio, meditation center, or sound healing spot in the USA.", "gps": "sound healing or yoga studio", "vector_necesidades": {"silencio": 100, "descanso": 95, "musica": 90, "contemplacion": 95, "salud": 90, "esperanza": 90, "organizacion": 70}},
            {"id": 323, "titulo": "Aislamiento Orgánico", "titulo_en": "Organic Isolation", "porque": "Hoy dirígete al parque natural o reserva de árboles más cercana. Si el ruido de la ciudad te abruma y tu cuerpo pide aire limpio, camina despacio por el sendero boscoso. Quédate un minuto tocando la madera de un árbol. Siente el viento fresco en tu cara, lejos del bullicio. Levántate, regálate este respiro natural. Tu cuerpo descargará la tensión, gratuita y profundamente. Vive este instante plenamente.", "porque_en": "Today, head to the nearest nature park or tree reserve. If city noise overwhelms you and your body needs clean air, walk slowly along the wooded trail. Spend one minute touching a large tree's wood, feel the fresh wind on your face, away from urban noise. Get up, grant yourself this natural break. Let your body release the week's tension freely and deeply. Live this moment fully.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sendero boscoso, reserva natural o parque estatal de tu región.", "donde_en": "Wooded trail, nature reserve, or state park in your region.", "gps": "state park trail or nature reserve", "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "silencio": 85, "movimiento": 60, "contemplacion": 90, "descanso": 60, "esperanza": 95, "sol": 70}},
            {"id": 112, "titulo": "Sendero Corto Natural", "titulo_en": "Short Nature Trail", "porque": "Hoy busca un camino rodeado de árboles o plantas en un sendero natural. Si tu mente está cansada por ruidos y pantallas, desconéctate para caminar en paz. Avanza tranquilo, a tu ritmo, observando los colores vibrantes de la naturaleza. Levántate, regálate este respiro natural al aire libre. Tu respiración recuperará su curso armonioso. Rompe tu rutina y descansa, sintiendo la renovación.", "porque_en": "Today, find a path surrounded by trees or plants in a nature trail. If your mind is tired from noise and screens, disconnect to walk in peace. Walk peacefully at your steady pace, calmly observing nature's vibrant colors. Get up, grant yourself this natural outdoor break. Let your breathing find its harmonious course. Break your routine, truly rest, feeling renewed.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sendero natural o bosque.", "donde_en": "Nature trail or forest.", "gps": "short nature track", "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "agua": 40, "sol": 60, "sombra": 70, "aire_fresco": 100, "creatividad": 40, "comunidad": 20, "aprendizaje": 50, "juego": 20, "contemplacion": 90, "descanso": 60, "organizacion": 20, "alimentacion": 0, "musica": 20, "risa": 10, "esperanza": 85}},
            {"id": 113, "titulo": "Pista de Atletismo", "titulo_en": "Running Track", "porque": "Hoy dirígete a un circuito deportivo o pista de atletismo pública. Si tus pensamientos están acelerados y necesitas liberar fuerza para enfocar tu energía, avanza o trota a un paso cómodo, sintiendo el ritmo. Siente la fuerza de tu cuerpo en cada zancada. Nota cómo se va la tensión. Levántate, regálate esta descarga física activa. Tu mente se despejará del estrés diario. El recorrido empieza ya, con renovada vitalidad.", "porque_en": "Today, head to an outdoor sports circuit or public running track. If your thoughts are racing and you need to release strength to focus energy, walk or jog at a comfortable pace, feeling the rhythm. Feel your body's power in each stride. Notice muscle tension wash away. Get up, grant yourself this active physical discharge. Your mind will clear from daily stress. Your journey begins now, with renewed vitality.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Pista de atletismo pública.", "donde_en": "Public running track.", "gps": "public running track", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 40, "agua": 10, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 10, "comunidad": 50, "aprendizaje": 20, "juego": 30, "contemplacion": 50, "descanso": 10, "organizacion": 70, "alimentacion": 0, "musica": 50, "risa": 20, "esperanza": 70}},
            {"id": 251, "titulo": "Soberanía en Movimiento", "titulo_en": "Sovereignty in Motion", "porque": "Hoy despega tus ojos de la pantalla en tu cabina o asiento de pasajero. Si llevas mucho tiempo viajando atrapado en el tráfico ruidoso y tu cuerpo necesita descompresión, reacciona con consciencia. Apoya las manos firmes sobre tus rodillas, endereza la espalda, respira lento y profundo, sintiendo la calma. Siente el peso de tu cuerpo descansando mientras dejas ir el agobio. Regálate este respiro pasivo con gratitud.", "porque_en": "Today, take your eyes off the screen in your transit cabin or passenger seat. If you've been traveling trapped in noisy traffic and your body needs decompression, react with awareness. Place hands firmly on knees, straighten your back, breathe slow and deep, feeling calm. Feel your body's weight resting, letting go of daily overload. Grant yourself this passive break with gratitude.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cabina de transporte, asiento de pasajero o parada de autobús de USA.", "donde_en": "Transit cabin, passenger seat, or USA bus stop.", "gps": "quiet rest areas or public plazas", "vector_necesidades": {"descanso": 95, "silencio": 85, "movimiento": 20, "contemplacion": 90, "organizacion": 60, "esperanza": 80}},
            {"id": 252, "titulo": "Hackeo al Tráfico", "titulo_en": "Traffic Hack", "porque": "Hoy busca una estación de servicio o área de descanso en la autopista. Si sientes pesadez y estrés por el tráfico y ruidos, aprovecha la luz roja. Abre grande tu boca diez segundos para relajar la mandíbula y liberar tensión. Estira los dedos en el volante, liberando rigidez de muñecas. Mira al cielo abierto y toma aire con calma. Regálate este respiro pasivo.", "porque_en": "Today, find a safe service station or rest area on the highway. If you feel stress and heaviness from traffic and noise, use the red light to react. Open your mouth wide for ten seconds to relax your jaw, release tension. Stretch your fingers on the steering wheel, releasing wrist tightness. Look at the open sky, take a deep breath calmly. Grant yourself this passive break.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Área de servicio de autopista, rampa pública o intersección vial.", "donde_en": "Highway service area, public ramp, or road intersection.", "gps": "highway rest stop or overlook", "vector_necesidades": {"movimiento": 80, "descanso": 70, "silencio": 50, "aire_fresco": 85, "organizacion": 40, "salud": 85}},
            {"id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route", "porque": "Hoy busca una ruta o carril bici seguro en tu vecindario. Si necesitas liberar tensión y moverte con ligereza, pedalea tranquilo, sintiendo el viento fresco. Disfruta la velocidad bajo tu control y el dominio de tu camino. Levántate, regálate este quiebre dinámico activo. Permite que tu mente se despeje de preocupaciones diarias. Tu viaje personal y revitalizante empieza ya.", "porque_en": "Today, find a safe bike lane or route in your neighborhood. If you need to release tension and move lightly, pedal peacefully, feeling the fresh wind. Enjoy the speed under your control and the dominance of your path. Get up, grant yourself this active dynamic break. Allow your mind to clear from daily worries. Your personal and revitalizing journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route", "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 80, "sombra": 40, "aire_fresco": 95, "creatividad": 30, "comunidad": 50, "aprendizaje": 40, "juego": 70, "contemplacion": 60, "descanso": 30, "organizacion": 60, "alimentacion": 0, "musica": 50, "risa": 40, "esperanza": 80}},
            {"id": 211, "titulo": "Soberanía de Cabina", "titulo_en": "Cabin Sovereignty", "porque": "Hoy busca la ventana más grande en esta terminal de transporte con vista despejada. Si tu mente está saturada por presiones y ruidos de viajes, detén tu prisa. Toma aire profundo y lento tres veces para relajar hombros. Recuerda que tu cuerpo merece un descanso libre de apuro. Siente el aire fresco y recupera tu calma interna ahora, en este espacio tranquilo.", "porque_en": "Today, find the largest window in this transit terminal with a clear view. If your mind is overloaded by pressures and travel noise, stop your rush. Take deep, slow breaths three times to relax shoulders. Remember, your body deserves rest free from hurry. Feel the fresh air and recover inner calm now, in this tranquil space.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Terminal de aeropuerto o zona de observación abierta.", "donde_en": "Airport terminal or open observation zone.", "gps": "airport observation area", "vector_necesidades": {"aire_fresco": 100, "contemplacion": 95, "silencio": 60, "descanso": 50, "movimiento": 30, "esperanza": 80}},
            {"id": 212, "titulo": "Depuración de Tensión", "titulo_en": "Tension Cleansing", "porque": "Hoy ve al centro deportivo, gimnasio o piscina pública cercana. Si sientes el cuerpo cargado de energía pesada por estrés y necesitas sacudirte esa presión, reacciona. Haz un ejercicio de fuerza, activa tus brazos y piernas. Permite que tu cuerpo suelte la rigidez. Levántate, regálate esta descarga física activa. Deja que el agobio mental se disuelva con el esfuerzo muscular. Tu poder físico regresa, lleno de vitalidad.", "porque_en": "Today, go to the nearest sports center, gym, or public pool. If your body is loaded with heavy energy from stress and needs to shake off pressure, react. Do a strength exercise, activate arms and legs. Let your body release stiffness. Get up, grant yourself this active physical discharge. Let mental burden dissolve through muscular effort. Your physical power returns now, full of vitality.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Gimnasio público, cancha o alberca comunitaria.", "donde_en": "Public gym, court, or community pool.", "gps": "community fitness center", "vector_necesidades": {"movimiento": 100, "agua": 80, "salud": 90, "juego": 50, "descanso": 0, "silencio": 20, "risa": 40}},
            {"id": 213, "titulo": "Estabilización Somática", "titulo_en": "Somatic Stabilization", "porque": "Hoy visita la farmacia o clínica local más cercana. Si sientes el corazón rápido por agobio y tu cuerpo pide una pausa, toma asiento cómodo en su área de descanso. Busca un vaso con agua fresca, bébelo despacio. Saborea cada trago. Nota cómo tu organismo se refresca y desacelera en paz. Regálate este respiro clínico protector y estabiliza tu ritmo biológico naturalmente.", "porque_en": "Today, visit the nearest local pharmacy or clinic. If your heartbeat is fast from overwhelm and your body needs a gentle break, take a comfortable seat in its lounge area. Find fresh water, drink it slowly. Calmly taste each sip, notice how your organism refreshes and slows down in peace. Grant yourself this protective medical break, stabilize your biological rhythm naturally.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Área de descanso de una farmacia o clínica local.", "donde_en": "Lounge area of a local pharmacy or clinic.", "gps": "pharmacy health lounge", "vector_necesidades": {"agua": 100, "salud": 95, "descanso": 80, "silencio": 70, "organizacion": 80, "esperanza": 85}}
        ],
        "aburrido": [
            {"id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk", "porque": "Hoy inicia un vibrante paseo de colores. Si tus días son repetitivos, despierta tu imaginación buscando novedades visuales en las calles. Levántate, camina lento por tu zona. Busca paredes con pintura, dibujos o murales de arte urbano. Haz este trayecto a solas para reconectar contigo. Es una recarga sin costo que romperá tu rutina y te hará sentir presente. El viaje personal empieza ya.", "porque_en": "Today, start a vibrant color walk. If your days are repetitive, awaken your imagination by seeking visual novelty on the streets. Get up, walk slowly through your area. Look for walls with colorful paintings, drawings, or street art murals. Do this journey alone to reconnect. It's a free recharge that will break your routine and make you feel present. Your personal journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Calle con murales.", "donde_en": "Street with murals.", "gps": "street art", "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}},
            {"id": 307, "titulo": "Descompresión de Perímetro", "titulo_en": "Perimeter Decompression", "porque": "Hoy busca un hotel o lugar de descanso cercano. Si sientes aburrimiento de estar encerrado y tu cuerpo pide un espacio ordenado, camina tranquilo hacia su vestíbulo. Toma asiento cómodo, mantén tu espalda recta, descansa tu mirada de pantallas por un minuto. Levántate, regálate este quiebre de entorno, permite que tu respiración se equilibre. Tu mente se renueva ya, con calma en este ambiente sereno.", "porque_en": "Today, find a hotel or resort close by. If you feel bored and your body needs an orderly space, walk peacefully into its main lobby. Take a comfortable seat, keep your spine straight, and rest your eyes from screens for one minute. Get up, grant yourself this change of scenery, allow your breathing to balance. Your mind renews now, with deep calm in this serene environment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Lobby o zona de descanso pública de un hotel local.", "donde_en": "Lobby or public lounge area of a local hotel.", "gps": "hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 95, "organizacion": 80, "esperanza": 80, "comunidad": 50, "movimiento": 20}},
            {"id": 308, "titulo": "Ampliación del Horizonte", "titulo_en": "Horizon Expansion", "porque": "Hoy dirígete al vestíbulo de una central de transportes o aeropuerto cercano. Si tu mente está atascada en la rutina y necesitas un espacio inmenso para explorar, busca el ventanal más grande. Observa el cielo abierto, haz tres respiraciones lentas contemplando la inmensidad. Levántate, abraza este estímulo visual, rompe el piloto automático expandiendo tus pensamientos. Tu aventura interior comienza ya, con nuevas perspectivas.", "porque_en": "Today, head to the lobby of a nearby transit center or airport. If your mind is stuck in routine and needs a vast space to explore, find the largest window. Observe the open sky, take three slow breaths contemplating its immensity. Get up, embrace this visual stimulus, break the automatic pilot by expanding thoughts. Your inner adventure begins now, with fresh perspectives.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30, "aprendizaje": 60}},
            {"id": 309, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Hoy ve al parque de juegos o centro de entretenimiento cercano. Si tu mente está en un bucle aburrido y monótono, recibe un impacto alegre de colores, risas y dinámicas divertidas. Observa las luces, escucha las risas genuinas y disfruta una actividad sencilla para romper la monotonía. Levántate, regálate este respiro recreativo gratuito y activa tu energía positiva con entusiasmo.", "porque_en": "Today, go to the nearest amusement park or play center. If your mind is in a boring, monotonous loop, get a joyful boost of bright colors, laughter, and fun dynamics. Observe flashing lights, listen to genuine laughter, and enjoy a simple activity to break monotony. Get up, grant yourself this free recreational break, and activate your positive energy with enthusiasm.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.", "gps": "amusement park or arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50, "creatividad": 60}},
            {"id": 313, "titulo": "Cazador de Sombras Urbano", "titulo_en": "Urban Shadow Hunter", "porque": "Hoy camina por tu vecindario, lento y pausado. Si tu rutina es monótona, necesitas un quiebre visual para activar tu imaginación. Concéntrate en observar las sombras de árboles, postes y edificios proyectadas sobre las aceras. Mira el mundo desde este ángulo geométrico diferente. Levántate, regálate este respiro contemplativo gratuito, rompe el piloto automático en paz y con renovada curiosidad.", "porque_en": "Today, walk in your neighborhood, slow and unhurried. If your routine is monotonous, you need a visual break to activate imagination. Focus on observing shadows from trees, poles, and buildings projected onto sidewalks. Look at the world from this different geometric angle. Get up, grant yourself this free contemplative break, break the automatic pilot in peace with renewed curiosity.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Calles, aceras y callejones seguros de tu vecindario.", "donde_en": "Safe streets, sidewalks, and alleys in your neighborhood.", "gps": "public walking trail or neighborhood", "vector_necesidades": {"movimiento": 75, "contemplacion": 100, "creatividad": 95, "silencio": 60, "aire_fresco": 85, "juego": 40, "descanso": 30}},
            {"id": 314, "titulo": "Inmersión Textural", "titulo_en": "Textural Immersion", "porque": "Hoy dirígete a la plaza pública o parque arbolado cercano. Si sientes el aburrimiento de estar atrapado en el teléfono, despierta tus sentidos con el tacto. Camina despacio, busca tres superficies con texturas diferentes: madera, metal frío o una hoja suave. Levántate, abraza este estímulo sensorial profundo y gratuito. Permite que tu mente recupere su curiosidad natural explorando el mundo.", "porque_en": "Today, head to the nearest public plaza or wooded park. If you feel bored being phone-trapped, awaken your senses with conscious touch. Walk slowly, look for three surfaces with different textures: rough wood, cold metal, or a soft leaf. Get up, embrace this deep, free sensory stimulus. Let your mind regain natural curiosity now, exploring the vibrant world.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Plaza pública, parque o entorno urbano abierto.", "donde_en": "Public plaza, park, or open urban environment.", "gps": "public plaza or community park", "vector_necesidades": {"naturaleza": 90, "movimiento": 60, "creatividad": 85, "contemplacion": 95, "silencio": 70, "aire_fresco": 90, "juego": 30}},
            {"id": 315, "titulo": "Módulo de Exploración Gráfica", "titulo_en": "Graphic Exploration Module", "porque": "Hoy visita la biblioteca municipal o librería cercana. Si tus pensamientos están en un bucle aburrido, alimenta tu imaginación con estímulos visuales artísticos. Ingresa despacio y en silencio a la sección de arte o fotografía. Toma un libro fascinante. Abre sus páginas al azar, contempla ilustraciones o fotos por minutos, dejando volar tu mente. Levántate, regálate este respiro intelectual. Rompe la rutina en calma. Tu creatividad se eleva.", "porque_en": "Today, visit the municipal library or nearest bookstore. If your thoughts are in a boring loop, feed your imagination with artistic visual stimuli. Enter slowly, in silence, to the art or photography section. Pick up a fascinating book. Open its pages randomly, contemplate illustrations or photos for minutes, letting your mind wander. Get up, grant yourself this intellectual break. Break your routine in calm. Your creativity soars freely.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sección de lectura, librería local o biblioteca pública.", "donde_en": "Reading section, local bookstore, or public library.", "gps": "public library or local bookstore", "vector_necesidades": {"aprendizaje": 100, "creatividad": 100, "contemplacion": 90, "silencio": 100, "descanso": 80, "organizacion": 60, "juego": 20}},
            {"id": 310, "titulo": "Exploración de Espacios", "titulo_en": "Space Exploration", "porque": "Hoy abre tu app de alquiler de casas desde tu descanso. Si te falta imaginación y tus días son aburridos, ver fotos de lugares hermosos despertará tu creatividad. Busca cabañas o casitas de campo en tu estado. Mira fotos de habitaciones y paisajes como un juego interactivo, sin obligación de reservar. Regálate este viaje mental, reconecta con tu inspiración y sueños ahora.", "porque_en": "Today, open your home rental app from your resting space. If you lack imagination and your days are boring, beautiful place photos will awaken your creativity. Look for wooden cabins or country houses in your state. View room and landscape photos as an interactive game, with no booking obligation. Grant yourself this mental journey, reconnect with inspiration and dreams now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Interfaz móvil desde tu zona de descanso habitual.", "donde_en": "Mobile interface from your usual resting space.", "gps": "local post office", "vector_necesidades": {"creatividad": 100, "contemplacion": 95, "juego": 70, "organizacion": 80, "esperanza": 85, "descanso": 60, "aprendizaje": 60}},
            {"id": 311, "titulo": "Mapeo de Flujos", "titulo_en": "Flow Mapping", "porque": "Hoy dirígete a la tienda gigante o club de precios cercano. Si tu rutina es plana y aburrida y necesitas activar tu cuerpo, caminar por un lugar inmenso despertará tus sentidos. Camina a paso firme por los pasillos más largos. Observa las cajas y objetos. Aprovecha este espacio techado y fresco para mover tus piernas de forma constante y revitalizante. Levántate, rompe el piloto automático, actívate con energía renovada.", "porque_en": "Today, head to the nearest giant store or price club. If your routine feels flat and boring and you need to activate your body, walking through a huge place will awaken your senses. Walk steadily through the longest outer aisles. Observe boxes and items. Use this cool indoor space to move your legs constantly and revitalizingly. Get up, break the automatic pilot, and activate with renewed energy.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Pasillos industriales de un gran almacén de USA.", "donde_en": "Industrial aisles of a large USA warehouse store.", "gps": "wholesale club or warehouse", "vector_necesidades": {"movimiento": 85, "organizacion": 75, "comunidad": 60, "contemplacion": 60, "juego": 40, "descanso": 10, "silencio": 5}},
            {"id": 312, "titulo": "Sabotaje de Espera", "titulo_en": "Waiting Sabotage", "porque": "Hoy busca la escuela o universidad pública más cercana. Si tu mente cayó en un bucle aburrido y pesado, recibe aire fresco en un ambiente de estudio para recuperar el enfoque. Camina despacio y en silencio por sus jardines y plazas. Respira aire limpio libremente, observa el entorno con tranquilidad. Levántate, regálate este respiro intelectual gratuito. Rompe la rutina diaria, sintiendo la renovación interior.", "porque_en": "Today, find the nearest public school or university. If your mind fell into a boring, heavy loop, get a fresh air boost in a study environment to regain focus. Walk slowly and silently through its gardens and plazas. Breathe clean air freely, observe surroundings with tranquility. Get up, grant yourself this free intellectual break. Break your routine, feeling inner renewal.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Áreas comunes abiertas de un campus universitario.", "donde_en": "Open common areas of a university campus.", "gps": "university campus or public school", "vector_necesidades": {"aprendizaje": 100, "aire_fresco": 95, "silencio": 90, "contemplacion": 85, "descanso": 70, "movimiento": 40}}
        ],
        "cansado": [
            {"id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading", "porque": "Hoy visita la biblioteca pública de tu vecindario. Ingresa despacio. Si tu cuerpo pide calma para aprender sin ruidos y recargar energía, camina sin prisa entre estantes. Busca un libro de cuentos o imágenes. Disfruta el silencio absoluto. Levántate, regálate este respiro intelectual, permite que tus ojos descansen de pantallas. Rompe el piloto automático, sana tus pensamientos en paz.", "porque_en": "Today, visit your neighborhood's public library, enter slowly. If your body asks for quiet to learn and recharge energy, walk without rush among shelves. Find a storybook or interesting pictures. Enjoy absolute silence. Get up, grant yourself this intellectual break, let your eyes rest from screens. Break the automatic pilot, heal your thoughts in total peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library", "vector_necesidades": {"movimiento": 30, "naturaleza": 10, "silencio": 100, "agua": 0, "sol": 10, "sombra": 80, "aire_fresco": 50, "creatividad": 70, "comunidad": 50, "aprendizaje": 95, "juego": 10, "contemplacion": 90, "descanso": 85, "organizacion": 70, "alimentacion": 0, "musica": 0, "risa": 10, "esperanza": 70}},
            {"id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk", "porque": "Hoy da una caminata tranquila por el muelle del puerto. Si necesitas despejar tu mente con aire fresco y paisajes junto al agua, detén tu paso. Observa barcos moviéndose en la distancia, escucha el suave sonido del oleaje. Levántate, regálate esta tregua marina restauradora. Permite que tu respiración se sincronice con el ritmo del mar en calma. Tu viaje interior empieza ya.", "porque_en": "Today, take a peaceful walk along the nearby harbor pier. If you need to clear your mind with fresh air and waterscapes to relax, stop. Observe large boats moving in the distance, listen to soft waves breaking ashore. Get up, grant yourself this restoring marine truce. Allow your breathing to synchronize with the calm sea's rhythm. Your inner journey begins now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier", "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "sol": 70, "sombra": 50, "aire_fresco": 95, "creatividad": 50, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 80, "organizacion": 20, "alimentacion": 20, "musica": 50, "risa": 40, "esperanza": 90}},
            {"id": 328, "titulo": "Paseo junto al Mar", "titulo_en": "Maritime Stroll", "porque": "Hoy dirígete al paseo costero o muelle cercano. Si sientes cansancio por la rutina y tu mente pide mirar el mar para olvidar el encierro, detén tu marcha. Observa grandes embarcaciones en el horizonte. Permite que el sol reflejado en el agua se lleve la pesadez de tus pensamientos. Levántate, regálate este respiro pasivo frente al agua. Activa tu bienestar natural gratuito. Siente la brisa marina.", "porque_en": "Today, head to the nearest coastal boardwalk or pier. If you feel tired from routine and your mind asks to gaze at the vast sea to forget confinement, stop. Observe large vessels on the horizon. Let the sun's reflection on the water wash away heavy thoughts. Get up, grant yourself this passive break by the water. Activate your natural well-being for free. Feel the ocean breeze.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Muelle, puerto local o zona costera abierta.", "donde_en": "Dock, local pier, or open coastal zone.", "gps": "cruise terminal or pier", "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60}},
            {"id": 329, "titulo": "Pausa en Ruta", "titulo_en": "Route Break", "porque": "Hoy busca la próxima estación o área de servicio segura en tu camino. Si sientes el cuerpo cansado y la mente pesada por viajar o manejar, estaciónate, apaga el motor y sal. Haz un estiramiento suave con tus brazos, respira aire fresco tranquilo y camina despacio. Levántate, regálate esta tregua en carretera. Permite que tu respiración recupere su curso natural en paz. Tu mente se despeja por completo, encontrando serenidad.", "porque_en": "Today, find the next safe gas station or service area. If your body is tired and mind heavy from traveling or driving, park, turn off the engine, and exit your car. Do a gentle arm stretch, breathe fresh air calmly, and walk slowly nearby. Get up, grant yourself this highway break. Let your breathing recover its natural course in peace. Your mind clears completely, finding deep serenity.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Área de servicio de autopista o zona de descanso pública.", "donde_en": "Highway service area or public rest zone.", "gps": "highway rest stop or plaza", "vector_necesidades": {"descanso": 95, "movimiento": 60, "aire_fresco": 90, "salud": 85, "silencio": 50, "contemplacion": 70, "organizacion": 40}},
            {"id": 330, "titulo": "Recuperación Pasiva", "titulo_en": "Passive Recovery", "porque": "Hoy busca una zona histórica o plaza antigua cercana. Si tu mente está agotada de la rutina y necesitas un cambio de ritmo suave, camina lento. Contempla los edificios antiguos, usa este entorno urbano para despejar tu cabeza. Levántate, regálate este respiro arquitectónico pasivo. Permite que tu cuerpo desacelere gratuitamente. Tu curiosidad despierta en quietud, observando detalles.", "porque_en": "Today, find a beautiful historical zone or old plaza nearby. If your mind is exhausted from routine and needs a gentle change of pace, walk slowly. Contemplate old buildings, use this urban environment to clear your head. Get up, grant yourself this passive architectural break. Let your body slow down for free. Your curiosity awakens in stillness, observing details.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Centro histórico, plaza pública o calles peatonales.", "donde_en": "Historical center, public plaza, or pedestrian streets.", "gps": "historical landmark or walking tour", "vector_necesidades": {"aprendizaje": 90, "contemplacion": 95, "descanso": 80, "movimiento": 50, "silencio": 70, "creatividad": 60, "esperanza": 80}},
            {"id": 331, "titulo": "Aislamiento Sensorial", "titulo_en": "Sensory Isolation", "porque": "Hoy ve al cine más cercano para aislarte del ajetreo. Si tu mente está llena de ruidos por hablar con gente y tareas apuradas, elige una película con poca gente. Toma asiento en la oscuridad de la sala, guarda tu teléfono. Disfruta la tranquilidad absoluta. Levántate, regálate este descanso mental profundo en las sombras. Desconecta del mundo exterior segura y placenteramente.", "porque_en": "Today, go to the nearest movie theater to isolate from hustle. If your mind is overloaded by noise and rushed tasks, choose a film with few people. Take a seat in the comforting dark, put your phone away. Enjoy absolute quietness. Get up, grant yourself this deep mental rest in the shadows. Safely disconnect from the outside world pleasantly.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Sala de cine comercial o vestíbulo de proyecciones.", "donde_en": "Commercial movie theater or screening lobby.", "gps": "local cinema or amc", "vector_necesidades": {"descanso": 100, "silencio": 85, "contemplacion": 90, "sombra": 100, "juego": 40, "creatividad": 50, "movimiento": 5}},
            {"id": 332, "titulo": "Refugio Verde", "titulo_en": "Green Shelter", "porque": "Hoy busca el jardín botánico o parque de flores más cercano. Si tu cuerpo está cansado por el encierro y aire frío, y necesitas tocar plantas, encuentra un banco tranquilo rodeado de hojas verdes. Siéntate allí en calma por dos minutos, respira aire limpio de la naturaleza. Levántate, regálate esta tregua natural. Tu cuerpo recuperará su vitalidad, libre de estrés. Rompe el piloto automático, descansa en paz.", "porque_en": "Today, find the nearest botanical garden or flower park. If your body is tired from being cooped up, breathing cold air, and needs to touch plants, find a quiet bench surrounded by green leaves. Sit peacefully for two minutes, breathe clean nature air. Get up, grant yourself this protective natural break. Your body will recover vitality, stress-free. Break the automatic pilot, rest in peace.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Jardín botánico público, vivero o parque natural regional.", "donde_en": "Public botanical garden, nursery, or regional nature park.", "gps": "botanical garden or nursery", "vector_necesidades": {"naturaleza": 100, "aire_fresco": 100, "descanso": 90, "silencio": 80, "contemplacion": 95, "sombra": 90, "salud": 85, "movimiento": 25}},
            {"id": 333, "titulo": "Un Momento de Quietud", "titulo_en": "A Moment of Stillness", "porque": "Hoy busca un parque cercano con un lago o estanque público. Si tu mente está aburrida y necesitas mirar el agua para descansar, toma asiento en la orilla. Quédate un minuto observando las ondas y pajaritos, respira lento y consciente. Levántate, regálate este respiro visual pasivo. Permite que la quietud de la superficie repare tu balance interno. Tu imaginación despierta en calma y plenitud.", "porque_en": "Today, find a nearby park with a small public lake or pond. If your mind is bored and needs to watch water for rest, take a seat by the edge. Spend one minute watching ripples and birds, breathe slowly and consciously. Get up, grant yourself this passive visual break. Let the surface's stillness repair your inner balance. Your imagination awakens in calm and fullness now.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Banco de parque junto a un estanque o lago público.", "donde_en": "Park bench next to a public pond or lake.", "gps": "public lake park or fountain", "vector_necesidades": {"agua": 100, "contemplacion": 100, "descanso": 95, "silencio": 75, "naturaleza": 85, "aire_fresco": 90, "movimiento": 15}},
            {"id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory", "porque": "Hoy visita una sala de ciencia o centro astronómico cercano. Si tu mente está apurada y necesitas levantar la mirada al cielo para maravillarte con el universo, dedica tiempo a aprender sobre el espacio. Contempla estrellas si la noche está despejada, deja ir la prisa. Levántate, regálate este quiebre intelectual profundo. Permite que la inmensidad del cosmos disuelva tus preocupaciones. Tu mente sana hoy, explorando el infinito.", "porque_en": "Today, visit a small science room or nearby astronomical center. If your mind is hurried and needs to gaze at the vast sky to marvel at the universe, learn about outer space. Contemplate stars if the night is clear, let go of the rush. Get up, grant yourself this deep intellectual break. Let the cosmos' vastness dissolve your worries. Your mind heals today, exploring the infinite.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory", "vector_necesidades": {"movimiento": 10, "naturaleza": 70, "silencio": 90, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 70, "creatividad": 80, "comunidad": 40, "aprendizaje": 100, "juego": 10, "contemplacion": 100, "descanso": 90, "organizacion": 60, "alimentacion": 0, "musica": 30, "risa": 5, "esperanza": 95}},
            {"id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza", "porque": "Hoy busca una plaza o parque para sentarte en un banco público. Si tu mente necesita detenerse para conectar con la comunidad, descansar hombros y observar el entorno, contempla el caminar lento de las personas. Siente el ritmo vibrante de la ciudad en silencio. Levántate, regálate este respiro pasivo. Tu respiración recuperará su curso natural en paz. Tu mente se renueva hoy, sintiendo la conexión.", "porque_en": "Today, find a public plaza or park to sit comfortably on a bench. If your mind needs to slow down to connect with community, rest shoulders, and observe surroundings, contemplate people walking. Feel the vibrant city rhythm in silence. Get up, grant yourself this passive wellness break. Let your breathing find its natural course in peace. Your mind renews today, feeling profound connection.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza", "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "agua": 10, "sol": 90, "sombra": 70, "aire_fresco": 80, "creatividad": 50, "comunidad": 80, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "descanso": 100, "organizacion": 20, "alimentacion": 10, "musica": 60, "risa": 50, "esperanza": 85}},
            {"id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour", "porque": "Hoy únete a una caminata guiada o haz un recorrido por las calles históricas. Si estás cansado de caminos predecibles y tu cuerpo pide aprender historias, descubre relatos del pasado con calma. Estira tus piernas, mantén tu mente curiosa lejos de dispositivos. Levántate, regálate este quiebre intelectual activo. Permite que tu cuerpo active su energía. Tu nueva aventura urbana empieza ya, llena de descubrimientos.", "porque_en": "Today, join a guided walk or take a tour through your city's historical streets. If you're tired of predictable paths and your body asks to learn new stories, discover past tales with calm. Stretch your legs, keep your mind curious, away from devices. Get up, grant yourself this active intellectual break. Let your body activate its energy. Your new urban adventure begins now, full of discoveries.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour", "vector_necesidades": {"movimiento": 80, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 70, "comunidad": 70, "aprendizaje": 100, "juego": 20, "contemplacion": 80, "descanso": 60, "organizacion": 50, "alimentacion": 20, "musica": 30, "risa": 40, "esperanza": 90}},
            {"id": 231, "titulo": "Paseo junto al Mar", "titulo_en": "Maritime Stroll", "porque": "Hoy dirígete al muelle, puerto o zona costera abierta más cercana. Si sientes cansancio monótono por el encierro y tu mente pide mirar el mar inmenso para olvidar ruidos, detén tu marcha. Observa las grandes embarcaciones en el horizonte. Permite que el reflejo de la luz sobre el agua limpie tus pensamientos. Levántate, regálate este descanso contemplativo pasivo. Respira el aire marino, lleno de frescura.", "porque_en": "Today, head to the nearest dock, pier, or open coastal zone. If you feel monotonous tiredness from confinement and your mind asks to gaze at the vast sea to forget street noises, stop. Observe large vessels on the horizon. Let light reflecting on water clear your thoughts. Get up, grant yourself this passive contemplative rest. Breathe fresh marine air, invigorating.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Muelle, puerto o zona costera abierta.", "donde_en": "Dock, pier, or open coastal zone.", "gps": "cruise terminal or pier", "vector_necesidades": {"agua": 100, "contemplacion": 95, "descanso": 90, "aire_fresco": 90, "naturaleza": 80, "silencio": 60}},
            {"id": 232, "titulo": "Ritmo en la Ciudad", "titulo_en": "City Rhythm", "porque": "Hoy camina por una zona alegre del centro con música. Si sientes el aburrimiento de una rutina callada y tu cuerpo pide canciones alegres para activarte, quédate en la acera. Escucha el ritmo de fondo, siente la energía divertida de las luces que rompen tu monotonía. Levántate, regálate este estímulo acústico dinámico. Permite que tu cuerpo recupere su entusiasmo natural. El viaje y la música empiezan ya, llenos de vida.", "porque_en": "Today, walk through a cheerful downtown area with music. If you feel the boredom of a quiet routine and your body asks for cheerful songs to activate, stay on the sidewalk. Listen to the background rhythm, feel the fun energy of street lights breaking monotony. Get up, grant yourself this dynamic acoustic boost. Let your body recover natural enthusiasm. Your journey starts now, full of vibrant life and sound.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Perímetro exterior o terraza de un club céntrico.", "donde_en": "Outer perimeter or terrace of a central club.", "gps": "dance club or nightclub", "vector_necesidades": {"musica": 100, "juego": 90, "comunidad": 80, "risa": 70, "movimiento": 60, "silencio": 10, "descanso": 40}}
        ],
        "ansioso": [
            {"id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water", "porque": "Hoy busca una fuente, lago tranquilo o río cercano. Si la prisa mental te agobia, el agua en movimiento te dará calma. Despeja tu mente de preocupaciones, relaja tensiones de hombros. Siéntate en la orilla, observa el flujo constante de la corriente y relájate. Levántate, regálate este respiro visual pasivo. Permite que tu respiración se equilibre con la naturaleza. Todo está bien, con serenidad.", "porque_en": "Today, find a beautiful fountain, quiet lake, or nearby river. If mental rush overwhelms you, moving water brings calm. Clear your mind of worries, completely relax shoulder tension. Sit by the edge, observe the stream's constant flow, relax deeply. Get up, grant yourself this passive visual break. Let your breathing balance with nature. Everything is fine now, in total serenity.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake", "vector_necesidades": {"movimiento": 40, "naturaleza": 80, "silencio": 70, "agua": 100, "sol": 60, "sombra": 50, "aire_fresco": 90, "creatividad": 20, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 0, "musica": 50, "risa": 10, "esperanza": 80}},
            {"id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride", "porque": "Hoy haz un paseo corto en lancha o bote en un lago o río cercano. Si tienes estrés acumulado y tu mente pide desconexión para flotar y descansar, este quiebre es para ti. Siente la brisa fresca en tu rostro, contempla la inmensidad del agua. Levántate, regálate esta tregua acuática liberadora. Permite que tu mente se limpie de prisa. Tu camino de bienestar y paz empieza ya, lleno de calma.", "porque_en": "Today, take a short ride in a motorboat or rowboat on a nearby lake or river. If you have stress and your mind asks for total disconnection to float and rest deeply, this break is for you. Feel the fresh breeze on your face, contemplate the water's vastness. Get up, grant yourself this liberating aquatic truce. Let your mind clear from all rush. Your path to well-being and peace begins now, filled with calm.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river", "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "sol": 80, "sombra": 60, "aire_fresco": 100, "creatividad": 50, "comunidad": 50, "aprendizaje": 30, "juego": 60, "contemplacion": 95, "descanso": 90, "organizacion": 10, "alimentacion": 20, "musica": 60, "risa": 30, "esperanza": 90}},
            {"id": 345, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Hoy dirígete al parque de mascotas o zona de juegos cercana. Si sientes pensamientos repetitivos e inquietud, te vendrá excelente un momento de juego y risas para calmar nervios. Mira cómo juegan los animalitos, escucha los sonidos alegres, conéctate con esa diversión inocente por un minuto. Levántate, regálate este respiro recreativo pasivo. Tu respiración se equilibrará con la alegría del entorno. Tu ansiedad se disuelve aquí, en pura diversión.", "porque_en": "Today, head to the nearest pet park or play area. If you feel repetitive thoughts and restlessness, a moment of play and laughter will calm your nerves. Watch animals play, listen to cheerful sounds, connect with innocent fun for one minute. Get up, grant yourself this passive recreational break. Your breathing will balance with the joy around you. Your anxiety fades here, in pure enjoyment.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque de perros local, zona infantil o centro de juegos.", "donde_en": "Local dog park, kids zone, or arcade center.", "gps": "dog park or amusement arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 90, "movimiento": 70, "esperanza": 95, "silencio": 20, "descanso": 50, "creatividad": 40}},
            {"id": 346, "titulo": "Un Momento de Quietud", "titulo_en": "A Moment of Stillness", "porque": "Hoy visita el jardín o patio interior de un hotel cercano. Si sientes timidez o cansancio por estar con mucha gente y tu cabeza está pesada por responsabilidades, toma asiento en un sillón público. Cierra tus ojos un minuto, respira lento para descansar tu cuerpo. Levántate, regálate este quiebre de entorno protector. Permite que el silencio repare tu balance interno en paz. Tu mente descansa en comodidad y serenidad profunda.", "porque_en": "Today, visit a nearby hotel's garden or inner courtyard. If you feel shyness or tiredness from crowds and your head is heavy with responsibilities, take a seat in a public armchair. Close your eyes for one minute, breathe slowly to rest your body. Get up, grant yourself this protective change of scenery, and let stillness repair your inner balance in peace. Your mind rests in comfort and profound serenity.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Zona de descanso, jardín interior o lobby de un hotel de USA.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.", "gps": "boutique hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 95, "contemplacion": 95, "organizacion": 80, "salud": 90, "esperanza": 90, "sombra": 80}},
            {"id": 347, "titulo": "Estrategia de Alivio", "titulo_en": "Relief Strategy", "porque": "Hoy camina hacia la sala principal de la central de autobuses o aeropuerto cercano. Si sientes encierro por la rutina y necesitas estirar la mirada, guarda tu teléfono. Observa con calma a las personas viajar. Recuerda que el mundo es inmenso y tu inquietud pasará pronto. Levántate, abraza este estímulo visual. Rompe el piloto automático, expande tus pensamientos. Tu viaje interior comienza ya, con nuevas perspectivas y esperanza.", "porque_en": "Today, walk to the main hall of the nearest transit station or airport. If you feel confined by routine and need to stretch your gaze, put your phone away. Calmly watch people travel. Remember the world is huge and your restlessness will pass soon. Get up, embrace this visual stimulus. Break the automatic pilot, expand your thoughts. Your inner journey begins now, with new perspectives and hope.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Vestíbulo público de aeropuerto o central de transportes regional.", "donde_en": "Public airport lobby or regional transit hub.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 60, "movimiento": 40, "aprendizaje": 50}},
            {"id": 348, "titulo": "Pausa en la Cafetería", "titulo_en": "Coffee Shop Pause", "porque": "Hoy dirígete a una cafetería tranquila en tu vecindario. Si sientes inquietud por preocupaciones y tu cuerpo pide un ambiente pacífico, toma asiento en un rincón cómodo. Pide una bebida tibia o agua fresca, guarda tu teléfono. Siente el aroma del lugar mientras descansas. Levántate, regálate este respiro social pasivo. Permite que tu respiración se estabilice en este espacio seguro. Tu mente descansa ya, con profunda gratitud.", "porque_en": "Today, head to a quiet coffee shop in your neighborhood. If you feel restlessness from worries and your body asks for a peaceful environment, take a comfortable seat in a cozy corner. Order a warm drink or fresh water, put your phone away. Feel the aroma while resting deeply. Get up, grant yourself this passive social break. Let your breathing stabilize in this safe space. Your mind rests now, with profound gratitude.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Cafetería o establecimiento de bebidas local en tu Código Postal.", "donde_en": "Local coffee shop or beverage venue in your Zip Code.", "gps": "quiet cafe or bakery", "vector_necesidades": {"comunidad": 90, "descanso": 85, "silencio": 75, "alimentacion": 60, "contemplacion": 80, "esperanza": 85, "musica": 30}},
            {"id": 123, "titulo": "Jardín de Rocas Zen", "titulo_en": "Rock Zen Garden", "porque": "Hoy busca un parque de piedras o jardín japonés cercano. Si tus pensamientos avanzan apurados y necesitas un espacio con orden para equilibrar tu mente, detén tu prisa. Observa las formas redondas de las rocas. Disfruta la tranquilidad profunda de este entorno protector. Levántate, regálate este quiebre visual contemplativo. Permite que la armonía del diseño repare tu balance interno en paz. Tu mente se serena en quietud, encontrando su centro.", "porque_en": "Today, find a nearby stone park or Japanese garden. If your thoughts race and you need an orderly space to calm your mind, stop your rush. Observe the round shapes of rocks. Enjoy the deep quietness of this protective environment. Get up, grant yourself this contemplative visual break. Let the design's harmony repair your inner balance in peace. Your mind calms in stillness, finding its center.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden", "vector_necesidades": {"movimiento": 10, "naturaleza": 90, "silencio": 100, "agua": 50, "sol": 50, "sombra": 80, "aire_fresco": 90, "creatividad": 70, "comunidad": 20, "aprendizaje": 60, "juego": 5, "contemplacion": 100, "descanso": 95, "organizacion": 100, "alimentacion": 0, "musica": 20, "risa": 5, "esperanza": 90}},
            {"id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park", "porque": "Hoy visita un parque de mascotas local. Si necesitas risas y alegría sincera para apagar nervios, siéntate en un banco observando. Mira el juego inocente de los animales que te contagiará energía positiva. Verás perritos correr y divertirse. Levántate, regálate esta distracción pasiva. Tu respiración recuperará su ritmo natural en paz, lejos de responsabilidades. La alegría pura te abraza hoy, llenándote de energía vital.", "porque_en": "Today, visit a local dog park. If you need smiles and sincere joy to calm nerves, sit on a bench observing. Watch innocent animal play for positive energy as puppies run and have fun. Get up, grant yourself this passive distraction. Let your breathing find its natural rhythm in peace, away from responsibilities. Pure joy embraces you today, filling you with vital energy.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park", "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "silencio": 30, "agua": 20, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 100, "contemplacion": 40, "descanso": 60, "organizacion": 10, "alimentacion": 10, "musica": 20, "risa": 100, "esperanza": 90}},
            {"id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music", "porque": "Hoy encuentra una cafetería o rincón local con canciones tranquilas de fondo. Si tu mente está cansada y necesitas melodías relajantes para calmar hombros, toma asiento. Quédate escuchando los instrumentos con atención, sin mirar tu teléfono. Levántate, regálate este estímulo acústico protector. Permite que tu respiración se equilibre con la melodía en paz. Tu mente se libera de prisa, encontrando profunda serenidad.", "porque_en": "Today, find a small coffee shop or local spot with calm music playing. If your mind is tired and you need tranquil melodies to relax shoulders, take a seat. Stay listening to musical instruments attentively, without your phone. Get up, grant yourself this protective acoustic boost. Let your breathing balance with the melody in peace. Your mind breaks free from rush, finding profound serenity.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar", "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 10, "sombra": 90, "aire_fresco": 50, "creatividad": 90, "comunidad": 70, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "descanso": 80, "organizacion": 10, "alimentacion": 50, "musica": 100, "risa": 40, "esperanza": 85}},
            {"id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool", "porque": "Hoy visita la alberca municipal o centro deportivo con piscina. Si sientes el cuerpo tenso por tareas y necesitas el abrazo fresco del agua para flotar y olvidar preocupaciones, date un chapuzón suave. Descansa tu musculatura mientras flotas en quietud. Levántate, regálate este quiebre de hidroterapia pasiva. Permite que tu mente se limpie de agobio rutinario, gratuita y refrescantemente.", "porque_en": "Today, visit the municipal pool or community sports center. If your body is tense from tasks and needs water's fresh embrace to float and forget worries, take a gentle dip. Rest your muscles completely while floating in stillness. Get up, grant yourself this passive hydrotherapy break. Let your mind clear from routine overload, freely and refreshingly.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool", "vector_necesidades": {"movimiento": 90, "naturaleza": 40, "silencio": 50, "agua": 100, "sol": 70, "sombra": 60, "aire_fresco": 80, "creatividad": 30, "comunidad": 70, "aprendizaje": 20, "juego": 80, "contemplacion": 70, "descanso": 90, "organizacion": 20, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 85}},
            {"id": 241, "titulo": "Distracción Absoluta", "titulo_en": "Absolute Distraction", "porque": "Hoy ve al parque de juegos o centro recreativo familiar cercano. Si tus pensamientos dan vueltas aburridas y pesadas, recibe una inyección de risas y diversión inocente. Observa los colores alegres de los letreros luminosos, conéctate con actividades lúdicas sencillas para alegrar tu mente. Levántate, regálate este respiro recreativo pasivo. Permite que tu cuerpo active su vitalidad natural gratuitamente hoy, sintiendo ligereza.", "porque_en": "Today, go to the nearest amusement park or family recreation center. If your thoughts are spinning boringly, receive a boost of laughter and innocent fun. Observe cheerful colors of bright signs, connect with simple playful activities to brighten your mind. Get up, grant yourself this passive recreational break. Let your body activate its natural vitality freely today, feeling lightness.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Parque recreativo, zona infantil o centro de juegos local.", "donde_en": "Recreation park, kid zone, or local arcade center.", "gps": "amusement park or arcade", "vector_necesidades": {"juego": 100, "risa": 100, "comunidad": 80, "movimiento": 70, "esperanza": 90, "silencio": 20, "descanso": 50}},
            {"id": 242, "titulo": "Estrategia de Alivio", "titulo_en": "Relief Strategy", "porque": "Hoy camina hacia la sala principal de la central de autobuses o aeropuerto cercano. Si sientes encierro por la rutina y necesitas estirar la mirada, guarda tu teléfono. Observa con calma a las personas viajar. Recuerda que el mundo es inmenso y tu inquietud pasará pronto. Levántate, abraza este estímulo visual. Rompe el piloto automático, expande tus pensamientos. Tu viaje interior comienza ya, con serenidad y nuevas ideas.", "porque_en": "Today, walk to the main hall of the nearest transit station or airport. If you feel confined by routine and need to stretch your gaze, put your phone away. Calmly watch people travel. Remember the world is huge and your restlessness will pass soon. Get up, embrace this visual stimulus. Break the automatic pilot, expand your thoughts. Your inner journey begins now, with serenity and new ideas.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Vestíbulo público de aeropuerto o central de transportes.", "donde_en": "Public airport lobby or transit center.", "gps": "transit center or airport terminal", "vector_necesidades": {"contemplacion": 100, "aire_fresco": 90, "esperanza": 95, "descanso": 70, "silencio": 50, "movimiento": 30}},
            {"id": 243, "titulo": "Un Momento de Quietud", "titulo_en": "A Moment of Stillness", "porque": "Hoy visita el jardín o patio interior de un hotel cercano. Si sientes timidez o cansancio por estar con mucha gente y tu cabeza está pesada por responsabilidades, toma asiento en un sillón público. Cierra tus ojos un minuto, respira lento para descansar tu cuerpo. Levántate, regálate este quiebre de entorno protector. Permite que el silencio repare tu balance interno en paz. Tu mente descansa en comodidad y armonía profunda.", "porque_en": "Today, visit a nearby hotel's garden or inner courtyard. If you feel shyness or tiredness from crowds and your head is heavy with responsibilities, take a seat in a public armchair. Close your eyes for one minute, breathe slowly to rest your body. Get up, grant yourself this protective change of scenery, and let stillness repair your inner balance in peace. Your mind rests in comfort and profound harmony.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Zona de descanso o jardín de un hotel de USA.", "donde_en": "Lobby, interior garden, or lounge area of a USA hotel.", "gps": "boutique hotel lobby", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 95, "organizacion": 80, "salud": 85, "esperanza": 85}},
            {"id": 244, "titulo": "Soberanía de Cabina", "titulo_en": "Cabin Sovereignty", "porque": "Hoy busca la ventana más grande en esta terminal de transporte con vista despejada. Si tu mente está saturada por presiones y ruidos de viajes, detén tu prisa. Toma aire profundo y lento tres veces para relajar hombros. Recuerda que tu cuerpo merece un descanso libre de apuro. Siente el aire fresco y recupera tu calma interna ahora, en este apacible refugio.", "porque_en": "Today, find the largest window in this transit terminal with a clear view. If your mind is overloaded by pressures and travel noise, stop your rush. Take deep, slow breaths three times to relax shoulders. Remember, your body deserves rest free from hurry. Feel the fresh air and recover inner calm now, in this peaceful refuge.", "que_hacer": "", "que_hacer_en": "", "cuando": "", "cuando_en": "", "para_que": "", "para_que_en": "", "donde": "Terminal de aeropuerto, central de tránsito o zona de observación abierta.", "donde_en": "Airport terminal, transit hub, or open observation zone.", "gps": "airport terminal or transit hub", "vector_necesidades": {"aire_fresco": 95, "contemplacion": 100, "esperanza": 90, "descanso": 70, "silencio": 60, "movimiento": 30}}
        ]
    }
}
BIG_TECH_RESOURCES = {
    "youtube_base_url": "https://www.youtube.com/results?search_query=",
    "spotify_base_search_url": "https://open.spotify.com/search/",
    "spotify_base_genre_url": "https://open.spotify.com/genre/mood/",

    "youtube_default_search_es": "sonidos naturaleza relajantes",
    "youtube_default_search_en": "nature sounds relaxing",
    "spotify_default_genre_link_es": "relax-stress-relief",
    "spotify_default_genre_link_en": "relax-stress-relief",

    # Placeholder search terms for recovery missions when no specific brand handling exists
    "youtube_audio_es": "sonidos relajantes para desconectar",
    "youtube_audio_en": "calming sounds to disconnect",
    "spotify_audio_es": "musica relajante para la ansiedad",
    "spotify_audio_en": "calming music for anxiety",
}

# === CONSTANTES DE RESCATE EMOCIONAL Y ANTÍDOTOS DIGITALES UNIFICADOS ===
ANTIDOTOS_DIGITALES_SEARCH_TERMS = {
    "agotado": "ambient nature sounds calming 4k",
    "estresado": "guias de respiracion profunda 4 minutos",
    "aburrido": "documentales cortos de asombro analogo",
    "cansado": "musica binaural recarga de energia celular",
    "ansioso": "sonidos de agua fluyendo para calmar la mente"
}

# ==========================================================================================
# NUEVA MATRIZ DE PREGUNTAS ESPECÍFICAS POR EMPRESA (Bilingüe)
# ==========================================================================================
COMPANY_QUESTIONS = {
    "walmart": {
        "es": [
            {"id": 1, "pregunta": "¿Sientes que la rutina de compras te genera ansiedad o agobio?", "mente": "ansioso", "calidez_humana": "El gigante del consumo te atrapa con el ruido. Respira profundo. Tu calma es tu mejor compra."},
            {"id": 2, "pregunta": "¿Te abruma la cantidad de opciones y no sabes qué elegir?", "mente": "agotado", "calidez_humana": "Demasiadas opciones fatigan. Simplifica. Elige tu paz, no el producto."},
            {"id": 3, "pregunta": "¿Buscas productos para llenar un vacío o por necesidad real?", "mente": "aburrido", "calidez_humana": "El vacío no se llena con objetos. Conecta contigo. El valor está en tu experiencia, no en la compra."}
        ],
        "en": [
            {"id": 1, "pregunta": "Does the shopping routine cause you anxiety or overwhelm?", "mente": "anxious", "calidez_humana": "The consumption giant traps you with noise. Breathe deeply. Your calm is your best purchase."},
            {"id": 2, "pregunta": "Are you overwhelmed by the number of options and don't know what to choose?", "mente": "exhausted", "calidez_humana": "Too many choices tire. Simplify. Choose your peace, not the product."},
            {"id": 3, "pregunta": "Are you looking for products to fill a void or out of real need?", "mente": "bored", "calidez_humana": "The void is not filled with objects. Connect with yourself. Value is in your experience, not in the purchase."}
        ],
        "logo_path": "/static/walmart_logo.svg"
    },
    "amazon": {
        "es": [
            {"id": 4, "pregunta": "¿La inmediatez de la compra online te genera más estrés o impaciencia?", "mente": "estresado", "calidez_humana": "La velocidad digital cansa. Desconecta y reconecta con el tiempo real. Tu bienestar no se entrega en 24 horas."},
            {"id": 5, "pregunta": "¿Sientes que el algoritmo dirige tus deseos de consumo sin que te des cuenta?", "mente": "aburrido", "calidez_humana": "El algoritmo no conoce tu alma. Desactiva. Crea tus propios deseos, no los dictados por una pantalla."},
            {"id": 6, "pregunta": "¿Te preguntas si necesitas realmente todo lo que pides online?", "mente": "cansado", "calidez_humana": "El exceso desgasta. Reflexiona. Invierte en experiencias, no en acumulación. Tu energía es limitada."}
        ],
        "en": [
            {"id": 4, "pregunta": "Does the immediacy of online shopping generate more stress or impatience?", "mente": "stressed", "calidez_humana": "Digital speed tires. Disconnect and reconnect with real time. Your well-being is not delivered in 24 hours."},
            {"id": 5, "pregunta": "Do you feel the algorithm directs your consumption desires without you realizing it?", "mente": "bored", "calidez_humana": "The algorithm doesn't know your soul. Deactivate. Create your own desires, not those dictated by a screen."},
            {"id": 6, "pregunta": "Do you wonder if you really need everything you order online?", "mente": "tired", "calidez_humana": "Excess wears you down. Reflect. Invest in experiences, not accumulation. Your energy is limited."}
        ],
        "logo_path": "/static/amazon_logo.svg"
    },
    "youtube": {
        "es": [
            {"id": 7, "pregunta": "¿Pierdes la noción del tiempo viendo videos sin propósito?", "mente": "agotado", "calidez_humana": "El tiempo es tu bien más preciado. Recupera el control. Conéctate con lo que nutre tu espíritu, no lo que lo drena."},
            {"id": 8, "pregunta": "¿Buscas contenido para escapar de tus pensamientos recurrentes o inquietudes?", "mente": "ansioso", "calidez_humana": "La evasión es un espejismo. Enfrenta tus pensamientos con calma. La paz reside dentro, no en el siguiente video."},
            {"id": 9, "pregunta": "¿Sientes que la creatividad de otros te hace sentir menos creativo?", "mente": "aburrido", "calidez_humana": "La inspiración es un espejo, no una competencia. Despierta tu propia chispa. Tu creatividad es única y valiosa."}
        ],
        "en": [
            {"id": 7, "pregunta": "Do you lose track of time watching purposeless videos?", "mente": "exhausted", "calidez_humana": "Time is your most precious asset. Regain control. Connect with what nourishes your spirit, not what drains it."},
            {"id": 8, "pregunta": "Are you looking for content to escape your recurring thoughts or worries?", "mente": "anxious", "calidez_humana": "Evasion is a mirage. Face your thoughts calmly. Peace resides within, not in the next video."},
            {"id": 9, "pregunta": "Do you feel that the creativity of others makes you feel less creative?", "mente": "bored", "calidez_humana": "Inspiration is a mirror, not a competition. Awaken your own spark. Your creativity is unique and valuable."}
        ],
        "logo_path": "/static/youtube_logo.svg"
    }
}
# ==========================================================================================


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
    if seleccion == None:
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
    if len(seleccionadas) < n:
        for cand in candidatos_base:
            if len(seleccionadas) >= n:
                break

            mision_id = cand["mision"]["id"]
            if mision_id not in ids_seleccionados and mision_id not in historial_actual:
                seleccionadas.append(cand["mision"])
                ids_seleccionados.add(mision_id)

    # Si todavía no tenemos suficientes, y el historial se ha agotado, reinicia y toma al azar
    # o desde las que ya están en historial pero con menos penalización.
    if len(seleccionadas) < n:
        temp_misiones_a_añadir = []
        for cand in candidatos_base:
            if cand["mision"]["id"] not in ids_seleccionados:
                temp_misiones_a_añadir.append(cand["mision"])
                if len(temp_misiones_a_añadir) >= (n - len(seleccionadas)):
                    break
       
        # Si todavía faltan, toma aleatorias de todo el catálogo si es necesario
        if len(temp_misiones_a_añadir) < (n - len(seleccionadas)):
            random_misions_pool = [m for m in misiones if m["id"] not in ids_seleccionados and m not in temp_misiones_a_añadir]
            random.shuffle(random_misions_pool)
            temp_misiones_a_añadir.extend(random_misions_pool[:(n - len(seleccionadas) - len(temp_misiones_a_añadir))])
       
        seleccionadas.extend(temp_misiones_a_añadir)
        for m in temp_misiones_a_añadir:
            ids_seleccionados.add(m["id"])

    return seleccionadas[:n] # Asegura que el resultado final sea exactamente 'n' misiones si es posible

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
   
    if len(disponibles) < cantidad * 2 and len(misiones) > 0:
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

    # Bucle de respaldo seguro si la diversidad fue muy estricta o no se alcanzó la cantidad
    if len(resultado) < cantidad:
        # Usar la lista 'candidatos' ya ordenada por score
        for candidato in candidatos:
            mision_actual = candidato["mision"]
            if mision_actual["id"] not in ids_en_resultado:
                resultado.append(mision_actual)
                ids_en_resultado.add(mision_actual["id"])
            if len(resultado) >= cantidad:
                break
   
    # Fallback final: si aún no hay suficientes, toma las primeras 'cantidad' del catálogo completo
    # Asegúrate de no tomar duplicados si el catálogo es pequeño.
    while len(resultado) < cantidad and len(misiones) > len(ids_en_resultado):
        mision_aleatoria = random.choice(misiones)
        if mision_aleatoria["id"] not in ids_en_resultado:
            resultado.append(mision_aleatoria)
            ids_en_resultado.add(mision_aleatoria["id"])

    return resultado[:cantidad]


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
# NUEVO ENDPOINT: Obtener preguntas específicas por empresa
# ==========================================================================================
@app.get("/api/get-company-questions")
async def get_company_questions(company: str, lang: str = "es"):
    company_lower = company.lower()
    if company_lower not in COMPANY_QUESTIONS:
        raise HTTPException(status_code=404, detail="Company not found")
   
    questions = COMPANY_QUESTIONS[company_lower][lang]
    logo_path = COMPANY_QUESTIONS[company_lower]["logo_path"]
    return JSONResponse({"questions": questions, "logo_path": logo_path})

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
    # estado = str(payload.get("estado", "FL")).strip() # Not used in current logic, but kept
    # region = str(payload.get("region", "")).strip() # Not used in current logic, but kept
    mente = str(payload.get("mente", "aburrido")).lower()
    budget = str(payload.get("budget", "0"))
    perfil_tipo = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    lang = str(payload.get("lang", "es")).lower()
    
    # NEW: calidez_humana_pregunta is passed from frontend company flow
    calidez_humana_pregunta = payload.get("calidez_humana_pregunta", "")

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

    # === INTERCEPCIÓN DE SEGURIDAD Y AVISO LEGAL OBLIGATORIO ===
    ADVERTENCIA_LEGAL_ES = (
        "AVISO DE SEGURIDAD: Está prohibido usar Open Than Go mientras manejas. Tu seguridad es lo primero. "
        "El uso es bajo tu propio riesgo y exime de toda responsabilidad a May Roga LLC."
    )
    ADVERTENCIA_LEGAL_EN = (
        "SAFETY NOTICE: Using Open Than Go while driving is strictly prohibited. Your safety comes first. "
        "Use is at your own risk and exempts May Roga LLC from all liability."
    )

    # Inicialización de variables para evitar NameError en todas las ramas de ejecución
    marca_detectada = None
    instruccion_fisiologica_es = "Detente, respira libre."
    instruccion_fisiologica_en = "Stop, breathe free."
    diagnostico_sintoma_es = "Agotamiento rutinario."
    diagnostico_sintoma_en = "Routine exhaustion."
    enlace_yt = ""
    enlace_sp = ""
   
    # ==========================================================================================
    # MANIFIESTO MATRICIAL ABSOLUTO: TRADUCTOR PARÁSITO E INTERCEPTOR RECONFIGURADO V2
    # === MODIFICACIÓN: LÓGICA DE DETECCIÓN Y GENERACIÓN DE MENSAJES CONCISOS ===
    # ==========================================================================================
   
    force_recovery_mission = False
    explicitly_seeking_job = any(
        phrase in desahogo for phrase in ["quiero buscar trabajo", "necesito un empleo", "busco trabajo", "find a job", "looking for work"]
    )

    # DETECCIÓN DE SÍNTOMAS CORPORATIVOS O AMBIENTALES DEL ENTORNO DE USA
    if desahogo and not explicitly_seeking_job:
        desahogo_lower = desahogo.lower()
        target_brands = [
            "walmart", "amazon", "costco", "starbucks", "mcdonald",
            "spotify", "youtube", "tiktok", "instagram"
        ]
        for keyword in target_brands:
            if keyword in desahogo_lower:
                marca_detectada = keyword.capitalize()
                force_recovery_mission = True # Force recovery if a brand is detected
                break

    if force_recovery_mission:
        mente_str_es = mente.upper()
        mente_str_en = mente.upper()
        diagnostico_sintoma_es = f"Diagnóstico: El cliente experimenta [{mente_str_es}] en relación al estímulo corporativo [{marca_detectada}] en Zip Code {zip_code}."
        diagnostico_sintoma_en = f"Diagnostic: Client experiences [{mente_str_en}] linked to corporate stimulus [{marca_detectada}] in Zip Code {zip_code}."

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
        else:
            # Default case for other brands not explicitly handled above
            instruccion_fisiologica_es = f"Identificaste que [{marca_detectada}] satura tu mente. Rebélate: usa pasillos, aire libre o ventanas. Haz una pausa biológica profunda de 60 segundos. Recupera el control."
            instruccion_fisiologica_en = f"You identified [{marca_detectada}] saturating your mind. Rebel: use halls, open air, or windows. Take a deep 60-sec biological pause. Regain control."

        search_term_antidoto = ANTIDOTOS_DIGITALES_SEARCH_TERMS.get(mente, BIG_TECH_RESOURCES[f'youtube_default_search_{lang}'])
        enlace_yt = f"{BIG_TECH_RESOURCES['youtube_base_url']}{urllib.parse.quote_plus(search_term_antidoto)}"
        enlace_sp = f"{BIG_TECH_RESOURCES['spotify_base_search_url']}{urllib.parse.quote_plus(search_term_antidoto)}"

        # ==========================================================================================
        # CONSTRUCCIÓN DE CONSULTA DINÁMICA DE ECONOMÍA REAL - EL ORÁCULO AUTOMÁTICO MULTICANAL
        # ==========================================================================================
        # DETECTOR DE ESPECIALIDAD: Si el cliente habla explícitamente de buscar trabajo o empleo,
        # la app lo asiste en su necesidad real. Si no, bloquea lo corporativo y ejecuta liberación pura.
        pide_trabajo = any(palabra in marca_detectada.lower() or palabra in diagnostico_sintoma_es.lower() for palabra in ["trabajo", "empleo", "work", "job", "curriculum", "vacantes"])

        if pide_trabajo:
            query_maps = f"explore+employment+agencies+and+career+recruitment+centers+near+me+in+{zip_code}"
            enlace_yt = "https://youtube.com"
            enlace_sp = "https://spotify.com"
            destino_titulo_dinamico = "DIRECCIÓN DE ENFOQUE: DESARROLLO Y EMPLEO ACTIVO"
            que_hacer_dinamico = "Canalización de recursos y herramientas para inserción laboral inmediata."
        else:
            # EL ADIVINO SOMÁTICO: Diversidad humana absoluta sin dogmas (Viajes, baile, miradores, expectación, ocio)
            # Cada canal hackea un fragmento distinto de las Big Tech para suplir el vacío sin que el usuario escriba nada.
            matriz_diversidad_total = {
                "ansioso": {
                    "maps": [
                        "explore+hidden+panoramic+city+viewpoints+at+sunset+near+me",
                        "explore+cat+cafe+or+secret+pet+sanctuaries+near+me",
                        "explore+botanical+greenhouses+and+indoor+gardens+near+me",
                        "explore+vintage+vinyl+record+shops+and+music+stores+near+me"
                    ],
                    "youtube": "cinematic+aesthetic+lofi+live+animation+session+with+deep+meaningful+lyrics",
                    "spotify": "high+energy+70s+80s+funk+and+disco+classics+groove+dance+party"
                },
                "estresado": {
                    "maps": [
                        "explore+cozy+independent+bookstores+with+hidden+patios+near+me",
                        "explore+independent+comic+bookstores+and+retro+toy+shops+near+me",
                        "explore+scenic+lake+drives+and+isolated+forest+parking+near+me",
                        "explore+artisan+tea+houses+with+gardens+near+me"
                    ],
                    "youtube": "slow+cinematic+indie+music+video+session+melancholic+validation+lyrics",
                    "spotify": "upbeat+bossa+nova+jazz+samba+rhythms+sunshine+escape+groove"
                },
                "aburrido": {
                    "maps": [
                        "explore+classic+arcade+and+retro+pinball+venues+near+me",
                        "explore+local+street+art+graffiti+walks+and+flea+markets+near+me",
                        "explore+go+kart+racing+or+indoor+climbing+centers+near+me",
                        "explore+theme+parks+and+live+entertainment+hubs+near+me"
                    ],
                    "youtube": "high+energy+cyberpunk+synthwave+dynamic+visual+mix+neon+art",
                    "spotify": "indie+dance+post+punk+high+energy+dancefloor+hits"
                },
                "agotado": {
                    "maps": [
                        "explore+gourmet+specialty+coffee+roasters+and+pastry+shops+near+me",
                        "explore+thermal+mineral+baths+and+relaxation+lounges+near+me",
                        "explore+historic+hidden+cloisters+and+secret+courtyards+near+me",
                        "explore+boutique+hotels+with+panoramic+terraces+near+me"
                    ],
                    "youtube": "deep+relaxation+melancholic+dark+ambient+piano+visual+chords+soothing",
                    "spotify": "afro+house+organic+grooves+vibrant+tribal+rhythms+revival+dance"
                },
                "cansado": {
                    "maps": [
                        "explore+interactive+sensory+modern+art+galleries+near+me",
                        "explore+scenic+coastal+lookouts+or+mountain+passes+near+me",
                        "explore+local+flea+markets+and+antiques+shops+near+me",
                        "explore+independent+theaters+and+art+cinemas+near+me"
                    ],
                    "youtube": "acoustic+folk+live+session+intimate+performance+sad+beautiful+lyrics",
                    "spotify": "indie+pop+road+trip+sun+drenched+motivational+anthems+freedom"
                }
            }

            config_somatico = matriz_diversidad_total.get(mente, matriz_diversidad_total["aburrido"])
            # Selección aleatoria pura para que NUNCA repita el mismo destino o caiga en monotonía
            termino_maps_elegido = random.choice(config_somatico["maps"])
            
            modificador_compania = ""
            if perfil_tipo == "familia": modificador_compania = "+family+friendly"
            elif perfil_tipo == "accesible": modificador_compania = "+wheelchair+accessible"
            elif perfil_tipo == "solo": modificador_compania = "+hidden+gems"

            query_maps = f"{termino_maps_elegido}{modificador_compania}+in+{zip_code}"
            enlace_yt = f"https://youtube.com{config_somatico['youtube']}"
            enlace_sp = f"https://spotify.com{config_somatico['spotify']}"
            destino_titulo_dinamico = f"DIRECCIÓN DE ESCAPE A: {marca_detectada.upper()}"
            que_hacer_dinamico = "Interrupción autónoma de la burbuja rutinaria y apertura del mapa de expectación."

        target_link = f"{link_base}{urllib.parse.quote_plus(query_maps)}"

        # Estructuración segura e inyectada en tu diccionario nativo de misiones de campo
        final_misiones_para_frontend = [{
            "destino_id": 999,
            "destino_titulo": destino_titulo_dinamico,
            "destino_titulo_en": f"ESCAPE ROUTE TO: {marca_detectada.upper()}" if not pide_trabajo else "CAREER PATH DIRECTION",
            "que_hacer": que_hacer_dinamico,
            "que_hacer_en": "Immediate breakout from the mental prison through multichannel routing.",
            "destino_entorno": "ZONA DE HOMEOCINESIS ACTIVA" if not pide_trabajo else "ZONA DE FOCO PROFESIONAL",
            "destino_instruccion": instruccion_fisiologica_es,
            "destino_instruccion_en": instruccion_fisiologica_en,
            "destino_coordenadas_gps": target_link,
            "enlace_youtube": enlace_yt,
            "enlace_spotify": enlace_sp,
            "vector_entorno_seleccionado": {**DEFAULT_NECESSITY_VECTOR, "homeostasis_urgente": True},
            "diagnostico_sintoma_es": diagnostico_sintoma_es,
            "diagnostico_sintoma_en": diagnostico_sintoma_en,
        }]

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "misiones": final_misiones_para_frontend,
            "forced_recovery": True,
            "legal_notice_es": ADVERTENCIA_LEGAL_ES,
            "legal_notice_en": ADVERTENCIA_LEGAL_EN,
            "drive_prohibited": True
        })

    elif opcion_usuario == "CASA":

        # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA)
        textos_oraculo_casa = MANIFIESTOS_ORACULO.get(mente, MANIFIESTOS_ORACULO["aburrido"])
        manif_humano_casa = random.choice(textos_oraculo_casa)
        idioma = "EN" if lang == "en" else "ES"
        target_key = f"CASA_{idioma}"
       
        misiones_completas_base = BASE_MISIONES.get(target_key, [])
           
        final_misiones_casa = []
        if not misiones_completas_base: # Fallback if specific language mission not found
            if idioma == "ES":
                final_misiones_casa = [{
                    "id": 801,
                    "titulo": "Pausa de Respiración Somática",
                    "titulo_en": "Somatic Breathing Pause",
                    "descripcion": "Rompe el bucle del estrés digital. Inhala profundamente durante 4 segundos, mantén el aire por 4 segundos y exhala en 4 segundos.",
                    "descripcion_en": "Break the digital stress loop. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale for 4 seconds.",
                    "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90}
                }]
            else:
                final_misiones_casa = [{
                    "id": 801,
                    "titulo": "Somatic Breathing Pause",
                    "titulo_en": "Somatic Breathing Pause",
                    "descripcion": "Break the digital stress loop. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale for 4 seconds.",
                    "descripcion_en": "Break the digital stress loop. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale for 4 seconds.",
                    "vector_necesidades": {"silencio": 100, "descanso": 95, "salud": 90}
                }]
        else: # Use missions from BASE_MISIONES if available
             for m in misiones_completas_base:
                if isinstance(m, dict):
                    final_misiones_casa.append({
                        "id": m.get("id", 800),
                        "titulo": m.get("titulo", "Misión Interna"),
                        "titulo_en": m.get("titulo_en", "Internal Mission"),
                        "descripcion": m.get("descripcion", m.get("que_hacer", m.get("porque", "Pausa de bienestar somática."))),
                        "descripcion_en": m.get("descripcion_en", m.get("que_hacer_en", m.get("porque_en", "Somatic wellness pause."))),
                        "vector_necesidades": m.get("vector_necesidades", {})
                    })

        # SELECCIÓN INTELIGENTE UTILIZANDO LA FUNCIÓN CASA V2 PURIFICADA
        misiones_domesticas_finales = seleccionar_misiones_casa_inteligente(
            misiones=final_misiones_casa, # Use the prepared list
            perfil_local=perfil_local,
            historial_casa=payload.get("historial_casa", []),
            cantidad=3
        )
       
        historial_casa_actualizado = payload.get("historial_casa", [])
        for m in misiones_domesticas_finales:
            historial_casa_actualizado = actualizar_historial(historial_casa_actualizado, m["id"], MAX_HISTORY_CASA)

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "MODO_CASA",
            "misiones": misiones_domesticas_finales,
            "oraculo_manifiesto": manif_humano_casa,
            "historial_casa_actualizado": historial_casa_actualizado,
            "forced_recovery": False,
            "legal_notice_es": ADVERTENCIA_LEGAL_ES,
            "drive_prohibited": False
        })

    else:
        # 2. INTERVENCIÓN EXTERNA (MODO SALIR) - ENTRADA POR DEFECTO
        opciones_salir_candidatas = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
        historial_salir = payload.get("historial_salir", [])
       
        misiones_seleccionadas_raw = seleccionar_n_misiones_inteligentes(
            n=3,
            misiones=opciones_salir_candidatas,
            perfil_local=perfil_local,
            historial_actual=historial_salir
        )

        final_misiones_para_frontend = []
        antidotos_digitales_default_yt = BIG_TECH_RESOURCES[f'youtube_base_url'] + urllib.parse.quote_plus(BIG_TECH_RESOURCES[f'youtube_default_search_{lang}'])
        antidotos_digitales_default_sp = BIG_TECH_RESOURCES[f'spotify_base_search_url'] + urllib.parse.quote_plus(BIG_TECH_RESOURCES[f'spotify_default_genre_link_{lang}'])


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

            # CONDICIONALES DE IDIOMA TOTALMENTE SIMÉTRICOS E INDEPENDIENTES
            titulo_ganador_lang = (info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) or "").upper() if lang == "en" else (info_seleccionada["titulo"] or "").upper()
            que_hacer_lang = info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or '' if lang == "en" else info_seleccionada["que_hacer"] or ""
            donde_base_lang = info_seleccionada.get("donde_en", info_seleccionada["donde"]) if lang == "en" else info_seleccionada["donde"]
            guia_masticada_lang = info_seleccionada.get('porque_en', info_seleccionada.get('porque', '')) if lang == "en" else info_seleccionada.get('porque', '')

            search_query_parts = []
            if perfil_tipo == "accesible":
                search_query_parts.append("wheelchair accessible")
            elif perfil_tipo == "familia":
                search_query_parts.append("family friendly")
               
            search_query_parts.append(info_seleccionada.get("gps", "park"))
            target_link = f"{link_base}{urllib.parse.quote_plus('+'.join(search_query_parts))}+{zip_code}"
            final_vector_necesidades = info_seleccionada.get("vector_necesidades", {})

            # Usar los enlaces por defecto si no están definidos en la misión
            enlace_yt = info_seleccionada.get("enlace_youtube", antidotos_digitales_default_yt)
            enlace_sp = info_seleccionada.get("enlace_spotify", antidotos_digitales_default_sp)

            # === ASIGNACIÓN SIMÉTRICA DE DATOS ORIGINALES ===
            final_misiones_para_frontend.append({
                "destino_id": info_seleccionada.get("id"),
                "destino_titulo": titulo_ganador_lang,
                "destino_titulo_en": (info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) or "").upper(),
                "que_hacer": que_hacer_lang,
                "que_hacer_en": info_seleccionada.get("que_hacer_en", info_seleccionada["que_hacer"]),
                "destino_entorno": donde_base_lang,
                "destino_instruccion": guia_masticada_lang.strip(),
                "destino_instruccion_en": info_seleccionada.get("porque_en", info_seleccionada.get("porque", "")).strip(),
                "destino_coordenadas_gps": target_link,
                "vector_entorno_seleccionado": final_vector_necesidades,
                "enlace_youtube": enlace_yt,
                "enlace_spotify": enlace_sp
            })
            historial_salir = actualizar_historial(historial_salir, info_seleccionada["id"], MAX_HISTORY_SALIR)

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "misiones": final_misiones_para_frontend,
            "historial_salir_actualizado": historial_salir,
            "forced_recovery": False,
            "legal_notice_es": ADVERTENCIA_LEGAL_ES,
            "legal_notice_en": ADVERTENCIA_LEGAL_EN,
            "drive_prohibited": True
        })
# ==========================================================================================
# APERTURA NATIVA DEL SERVIDOR FASTAPI (SINOPSIS ESTRUCTURAL DE CIERRE)
# ==========================================================================================
if __name__ == "__main__":
    port_env = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port_env, reload=False)

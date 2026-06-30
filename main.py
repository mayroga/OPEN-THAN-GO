import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==============================================================================
# 🗂️ BIBLIOTECA NACIONAL BILINGÜE DE LAS 7 TÉCNICAS DE VIDA (TVid) - MAY ROGA LLC
# ==============================================================================
# Contiene exactamente 3 variantes de ejercicios de 5 minutos por cada técnica.
# Total: 21 ejercicios humanos e inmersivos diseñados para OPEN THAN GO.
# ==============================================================================

TVID_LIBRARY = [
    # --- 1. TÉCNICA DEL BIEN ---
    {
        "tecnica": "bien", "id": "bien_01",
        "titulo_es": "Misión: La Cadena de Gratitud", "titulo_en": "Mission: The Gratitude Chain",
        "pasos_es": "1. Piensa en tres personas por las que sientes agradecimiento real hoy.\n2. Di en voz alta una razón específica para agradecer a cada una de ellas.\n3. Sostén una sonrisa constante en tu rostro durante 30 segundos.\n4. Finaliza repitiendo mentalmente: 'La gratitud aumenta el bien en mi vida.'",
        "pasos_en": "1. Think of three people you feel genuine gratitude for today.\n2. Say out loud one specific reason to thank each of them.\n3. Hold a steady smile on your face for 30 seconds.\n4. Finish by repeating mentally: 'Gratitude increases the good in my life.'"
    },
    {
        "tecnica": "bien", "id": "bien_02",
        "titulo_es": "Misión: El Espejo Positivo", "titulo_en": "Mission: The Positive Mirror",
        "pasos_es": "1. Mírate en un espejo cercano o imagínate frente a uno de forma nítida.\n2. Di con voz firme y clara cinco cualidades o virtudes positivas sobre ti.\n3. Respira profundamente tres veces, soltando el aire despacio.\n4. Finaliza diciendo: 'Reconocer mi valor fortalece mi bienestar.'",
        "pasos_en": "1. Look into a nearby mirror or imagine yourself clearly in front of one.\n2. Say firmly and clearly five positive qualities or virtues about yourself.\n3. Take three deep breaths, releasing the air slowly.\n4. Finish by saying: 'Recognizing my value strengthens my well-being.'"
    },
    {
        "tecnica": "bien", "id": "bien_03",
        "titulo_es": "Misión: La Acción de Bondad", "titulo_en": "Mission: The Act of Kindness",
        "pasos_es": "1. Piensa en una buena acción concreta que puedas realizar hoy por alguien.\n2. Imagina detalladamente cómo se sentirá esa otra persona al recibirla.\n3. Haz el compromiso firme contigo mismo de llevarla a cabo antes de que acabe el día.\n4. Finaliza afirmando: 'Cada acto de bondad mejora mi mundo.'",
        "pasos_en": "1. Think of a specific good deed you can do for someone today.\n2. Imagine in detail how that other person will feel upon receiving it.\n3. Make a firm commitment to yourself to carry it out before the day ends.\n4. Finish by affirming: 'Every act of kindness improves my world.'"
    },
    # --- 2. TÉCNICA DEL MAL ---
    {
        "tecnica": "mal", "id": "mal_01",
        "titulo_es": "Misión: El Semáforo Mental", "titulo_en": "Mission: The Mental Traffic Light",
        "pasos_es": "1. Piensa en una situación negativa o frustrante que hayas vivido recientemente.\n2. Luz Roja: Identifica qué conductas o pensamientos debes detener de inmediato.\n3. Luz Amarilla: Analiza qué puedes reflexionar y aprender de lo ocurrido.\n4. Luz Verde: Define qué acción harás totalmente diferente la próxima vez.\n5. Finaliza diciendo: 'Puedo transformar las dificultades en aprendizaje.'",
        "pasos_en": "1. Think of a recent negative or frustrating situation you experienced.\n2. Red Light: Identify which behaviors or thoughts you must stop immediately.\n3. Yellow Light: Analyze what you can reflect on and learn from what happened.\n4. Green Light: Define what action you will do completely differently next time.\n5. Finish by saying: 'I can transform difficulties into learning.'"
    },
    {
        "tecnica": "mal", "id": "mal_02",
        "titulo_es": "Misión: La Mochila Pesada", "titulo_en": "Mission: The Heavy Backpack",
        "pasos_es": "1. Visualiza mentalmente esa preocupación o rencor negativo que traes encima.\n2. Imagina de forma consciente que te quitas esa carga y la dejas dentro de una mochila en el suelo.\n3. Pregúntate con seriedad qué lección te deja esta experiencia.\n4. Nota cómo la mochila se vuelve ligera y se desvanece de tu vista.\n5. Finaliza diciendo: 'Aprendo, crezco y continúo.'",
        "pasos_en": "1. Mentally visualize that negative worry or resentment you are carrying.\n2. Consciously imagine taking off that load and placing it inside a backpack on the floor.\n3. Ask yourself seriously what lesson this experience leaves you with.\n4. Notice how the backpack becomes light and fades from your sight.\n5. Finish by saying: 'I learn, I grow, and I continue.'"
    },
    {
        "tecnica": "mal", "id": "mal_03",
        "titulo_es": "Misión: Del Problema a la Solución", "titulo_en": "Mission: From Problem to Solution",
        "pasos_es": "1. Piensa detenidamente en un problema que te esté quitando el sueño hoy.\n2. Escribe o imagina tres soluciones posibles, por más locas o raras que parezcan.\n3. Elige la solución más viable y comprométete a dar el primer paso hoy mismo.\n4. Finaliza diciendo: 'Siempre existe un camino hacia adelante.'",
        "pasos_en": "1. Think carefully about a problem that is keeping you awake today.\n2. Write down or imagine three possible solutions, no matter how crazy or strange they seem.\n3. Choose the most viable solution and commit to taking the first step today.\n4. Finish by saying: 'There is always a way forward.'"
    },
    # --- 3. TÉCNICA DEL NIÑO ---
    {
        "tecnica": "nino", "id": "nino_01",
        "titulo_es": "Misión: El Juego de las Preguntas", "titulo_en": "Mission: The Question Game",
        "pasos_es": "1. Elige cualquier objeto simple que tengas cerca de la mano ahora mismo.\n2. Hazte diez preguntas rápidas, curiosas e inusuales sobre su estructura o color.\n3. Inventa un uso alternativo, divertido o fantástico para ese objeto.\n4. Finaliza diciendo: 'La curiosidad hace crecer mi mente.'",
        "pasos_en": "1. Choose any simple object you have close at hand right now.\n2. Ask yourself ten quick, curious, and unusual questions about its structure or color.\n3. Invent an alternative, fun, or fantastic use for that object.\n4. Finish by saying: 'Curiosity makes my mind grow.'"
    },
    {
        "tecnica": "nino", "id": "nino_02",
        "titulo_es": "Misión: La Sonrisa Infantil", "titulo_en": "Mission: The Childlike Smile",
        "pasos_es": "1. Cierra los ojos y viaja en tu mente a un momento intensamente feliz de tu niñez.\n2. Revívelo intentando recordar los olores, la risa y el entorno de tu país natal.\n3. Sostén una sonrisa franca y amplia en tu rostro durante un minuto completo.\n4. Finaliza diciendo: 'La alegría vive dentro de mí.'",
        "pasos_en": "1. Close your eyes and travel in your mind to an intensely happy moment from your childhood.\n2. Relive it trying to remember the smells, the laughter, and the environment of your home country.\n3. Hold a genuine, wide smile on your face for a full minute.\n4. Finish by saying: 'Joy lives inside of me.'"
    },
    {
        "tecnica": "nino", "id": "nino_03",
        "titulo_es": "Misión: Inventando un Mundo", "titulo_en": "Mission: Inventing a World",
        "pasos_es": "1. Cierra los ojos e imagina un paisaje maravilloso, libre de biles o preocupaciones.\n2. Describe mentalmente sus colores vivos, sus sonidos pacíficos y su clima perfecto.\n3. Piensa qué gran lección de calma te llevarías si pudieras pasar el día entero ahí.\n4. Finaliza diciendo: 'Mi imaginación me ayuda a crecer.'",
        "pasos_en": "1. Close your eyes and imagine a wonderful landscape, free of bills or worries.\n2. Mentally describe its vivid colors, its peaceful sounds, and its perfect weather.\n3. Think about what great lesson of calm you would take away if you could spend the entire day there.\n4. Finish by saying: 'My imagination helps me grow.'"
    },
    # --- 4. TÉCNICA DEL PADRE ---
    {
        "tecnica": "padre", "id": "padre_01",
        "titulo_es": "Misión: La Decisión Responsable", "titulo_en": "Mission: The Responsible Decision",
        "pasos_es": "1. Trae a tu mente una decisión o tarea importante que tengas postergada.\n2. Analiza mentalmente y de forma madura sus consecuencias positivas y negativas.\n3. Elige la alternativa más honesta, recta y responsable para tu vida.\n4. Finaliza afirmando: 'Las buenas decisiones construyen mi futuro.'",
        "pasos_en": "1. Bring to your mind an important decision or task that you have been postponing.\n2. Mentally and maturely analyze its positive and negative consequences.\n3. Choose the most honest, upright, and responsible alternative for your life.\n4. Finish by affirming: 'Good decisions build my future.'"
    },
    {
        "tecnica": "padre", "id": "padre_02",
        "titulo_es": "Misión: El Minuto del Orden", "titulo_en": "Mission: The Minute of Order",
        "pasos_es": "1. Observa a tu alrededor e identifica un pequeño espacio o rincón que esté desordenado.\n2. Dedica exactamente un minuto reloj a limpiarlo y organizarlo a la perfección.\n3. Contempla el resultado y respira profundo disfrutando el control sobre tu entorno.\n4. Finaliza diciendo: 'El orden fortalece mi disciplina.'",
        "pasos_en": "1. Look around you and identify a small space or corner that is cluttered.\n2. Spend exactly one clock minute cleaning and organizing it to perfection.\n3. Contemplate the result and take a deep breath, enjoying control over your environment.\n4. Finish by saying: 'Order strengthens my discipline.'"
    },
    {
        "tecnica": "padre", "id": "padre_03",
        "titulo_es": "Misión: El Plan de Tres Pasos", "titulo_en": "Mission: The Three-Step Plan",

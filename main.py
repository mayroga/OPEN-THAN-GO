# OPEN THAN GO SYSTEM - Kernel Absolute Human Awakening Engine V.7.0.0
# Company: May Roga LLC
# File: main.py
# PARTE 1 DE 6: Inicialización de Servidor ASGI de Alta Velocidad y Fusibles de Red

import os
import random
from datetime import datetime
import urllib.parse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Asegura la existencia de la carpeta estática para el hardware del cliente
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def leer_raiz():
    # Busca y sirve el archivo html principal de forma directa
    ruta_html = os.path.join("static", "session.html")
    if os.path.exists(ruta_html):
        return FileResponse(ruta_html)
    return JSONResponse(
        {"error": "Archivo static/session.html no encontrado en el servidor."}, 
        status_code=404
    )

HISTORIAL_IDEAS_NUEVAS = []

BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Paso 1: Detén tu máquina", "descripcion": "Hazlo conmigo ahora. Escanea tu cuerpo en este segundo. Ubica el peso exacto en tu espalda. Míralo. Siente que estás aquí, vivo."},
        {"id": 2, "titulo": "Paso 2: Conciencia de base", "descripcion": "Siente tu silla ahora. Nota cómo sostiene tu peso gratis. El piso está firme. No sostengas el mundo tú solo en este minuto. Déjate caer."},
        {"id": 3, "titulo": "Paso 3: Bloqueo de pantalla", "descripcion": "Dale la vuelta a tu teléfono sobre la mesa ya. Mira una esquina de tu techo. Nota su color, sus líneas. Quédate ahí treinta segundos fijos."},
        {"id": 4, "titulo": "Paso 4: Descarga del pecho", "descripcion": "Imagina que dejas caer una mochila pesada llena de deudas y estrés ahora. Siente tus hombros libres. Se caen de golpe. El peso ya no está."},
        {"id": 5, "titulo": "Paso 5: Activación de vida", "descripcion": "Busca un vaso de agua ahora mismo. Dale un trago muy pequeño. Siente el líquido frío bajando por tu garganta. Te limpia por dentro. Es la vida."},
        {"id": 6, "titulo": "Paso 6: Romper el cortisol", "descripcion": "Aprieta tus dos puños con toda tu fuerza ahora. Siente la rabia acumulada. Mantén tres segundos. Ahora abre las manos de golpe. Suéltalo todo."},
        {"id": 7, "titulo": "Paso 7: Conexión externa", "descripcion": "Camina hacia la ventana o puerta más cercana ahora. Ábrela. Deja que el aire te golpee la cara en este instante. Siente el viento exterior."},
        {"id": 8, "titulo": "Paso 8: Reclamo del motor", "descripcion": "Gira tus muñecas y tus tobillos despacio ahora. Siente tus articulaciones. Tu cuerpo es tuyo, no del sistema. Tú gobiernas este motor físico."},
        {"id": 9, "titulo": "Paso 9: Anclaje del presente", "descripcion": "Cierra los ojos conmigo ahora. Di una sola cosa buena que tienes hoy en voz alta. Tu salud, tus manos, tu vida. Dilo con fuerza. Quédate con eso."},
        {"id": 10, "titulo": "Paso 10: Orden de control", "descripcion": "Alinea tres objetos de tu mesa perfectamente ahora. Poner orden fuera ayuda a poner orden dentro. Hazlo ya."},
        {"id": 11, "titulo": "Paso 11: Cable a tierra", "descripcion": "Quítate los zapatos ahora. Apoya las plantas de tus pies firmemente en el piso. Siente el frío del suelo. Conéctate."},
        {"id": 12, "titulo": "Paso 12: Flecha al cielo", "descripcion": "Estira tus brazos hacia arriba con fuerza en este segundo. Imagina que tocas el techo. Mantén la tensión. Suelta de golpe."},
        {"id": 13, "titulo": "Paso 13: Foco en lo ignorado", "descripcion": "Mira a tu alrededor. Elige una tarea mínima que estabas ignorando en tu cuarto. Hazla ahora mismo. Termínala ya."},
        {"id": 14, "titulo": "Paso 14: Eje biológico", "descripcion": "Endereza tu espalda en este instante. Imagina que un hilo invisible tira de tu cabeza hacia arriba. Respira hondo."},
        {"id": 15, "titulo": "Paso 15: Impacto térmico", "descripcion": "Toca una pared o una superficie de metal fría ahora mismo. Siente la temperatura real con tus dedos. Quédate ahí."},
        {"id": 16, "titulo": "Paso 16: Ventilación limpia", "descripcion": "Abre la puerta principal de tu casa ahora. Deja que el aire ruede y cambie el ambiente de tu sala. Huele el cambio."},
        {"id": 17, "titulo": "Paso 17: Descarga sacudida", "descripcion": "Párate y sacude tus manos y tus piernas con fuerza ahora. Como si te quitaras agua de encima. Hazlo por diez segundos."},
        {"id": 18, "titulo": "Paso 18: Foco de horizonte", "descripcion": "Mira por tu ventana ahora. Enfoca tus ojos en el objeto más lejano que alcances a ver en la calle. No mires nada cerca."},
        {"id": 19, "titulo": "Paso 19: Regreso a la raíz", "descripcion": "Cierra los ojos conmigo ahora. Trae a tu mente un recuerdo feliz de cuando eras un niño de ocho años. Siente esa risa."},
        {"id": 20, "titulo": "Paso 20: Hackeo de dopamina", "descripcion": "Dibuja una sonrisa grande en tu cara ahora por quince segundos, aunque no quieras. Obliga a tu cerebro a cambiar su energía ya."},
        {"id": 21, "titulo": "Paso 21: Veredicto de gratitud", "descripcion": "Cierra tus ojos en este instante. Di en voz alta una sola cosa buena que te pasó en la semana. Tu vida, tus manos. Dilo fuerte ya."},
        {"id": 22, "titulo": "Paso 22: Apagón sensorial", "descripcion": "Cierra tus ojos ahora. Cúbrelos suavemente con las palmas de tus manos templadas por un minuto. Siente la oscuridad absoluta."},
        {"id": 23, "titulo": "Paso 23: Sensor de pulso", "descripcion": "Coloca tu mano derecha sobre tu pecho en este segundo. Siente tus latidos en silencio. Estás aquí, estás al mando hoy."},
        {"id": 24, "titulo": "Paso 24: Desbloqueo cervical", "descripcion": "Mueve tu cabeza haciendo círculos muy lentos ahora. Siente cómo se destraba tu cuello del peso diario de las pantallas."},
        {"id": 25, "titulo": "Paso 25: Transferencia térmica", "descripcion": "Frota tus manos con fuerza ahora mismo hasta sentir calor real. Colócalas sobre tus hombros cansados. Siente el alivio ya."},
        {"id": 26, "titulo": "Paso 26: Sonido periférico", "descripcion": "Presta atención al ruido más lejano que ocurra fuera de tu edificio ahora mismo. Identifícalo en silencio."},
        {"id": 27, "titulo": "Paso 27: Balanceo mecánico", "descripcion": "Inclina tu columna suavemente de izquierda a derecha. Siente la elasticidad de tus costillas ahora."},
        {"id": 28, "titulo": "Paso 28: Foco transparente", "descripcion": "Mira fijamente un vaso o una botella transparente por sesenta segundos fijos. No desvíes la mirada."},
        {"id": 29, "titulo": "Paso 29: Descompresión facial", "descripcion": "Abre tu boca lo más grande que puedas y mueve tu mandíbula de lado a lado. Suelta el estrés retenido."},
        {"id": 30, "titulo": "Paso 30: Marcha ralentizada", "descripcion": "Camina cinco pasos dentro de tu espacio de la forma más lenta posible. Siente cada milímetro del movimiento."},
        {"id": 31, "titulo": "Paso 31: Presión digital", "descripcion": "Presiona suavemente tus sienes con las yemas de tus dedos haciendo círculos lentos por treinta segundos."},
        {"id": 32, "titulo": "Paso 32: Captura de oxígeno", "descripcion": "Toma aire profundo notando cómo se expande tu abdomen. Retén dos segundos y exhala despacio."},
        {"id": 33, "titulo": "Paso 33: Apertura torácica", "descripcion": "Lleva tus codos hacia atrás con fuerza e intenta que tus omóplatos se toquen. Abre tu pecho ahora."},
        {"id": 34, "titulo": "Paso 34: Abandono de carga", "descripcion": "Suelta toda la fuerza de tus piernas. Deja que el piso absorba toda la resistencia de tu peso gratis."},
        {"id": 35, "titulo": "Paso 35: Conteo de aislamiento", "descripcion": "Cuenta de forma regresiva en tu mente del treinta al uno despacio. Apaga el ruido de la sala."},
        {"id": 36, "titulo": "Paso 36: Textura real", "descripcion": "Pasa la palma de tu mano sobre tu ropa o cortina. Concéntrate puramente en el roce del tejido."},
        {"id": 37, "titulo": "Paso 37: Expansión falángica", "descripcion": "Abre tus manos separando los dedos lo más posible con rigidez por cinco segundos. Suelta de golpe."},
        {"id": 38, "titulo": "Paso 38: Murmullo biológico", "descripcion": "Tápate los oídos con tus dedos y escucha el sonido interno de tu respiración por veinte segundos."},
        {"id": 39, "titulo": "Paso 39: Foco milimétrico", "descripcion": "Elige un tornillo, marca o punto mínimo de la pared. Clava tus ojos ahí sin parpadear un momento."},
        {"id": 40, "titulo": "Paso 40: Péndulo suelto", "descripcion": "Deja tus brazos completamente muertos a los lados y balancéalos como un péndulo flojo."},
        {"id": 41, "titulo": "Paso 41: Registro dérmico", "descripcion": "Siente la temperatura exacta del aire del cuarto golpeando la piel de tus manos ahora mismo."},
        {"id": 42, "titulo": "Paso 42: Expulsión zombi", "descripcion": "Inhala inflando el pecho al máximo. Suelta el aire con un suspiro fuerte por la boca liberando la rutina."},
        {"id": 43, "titulo": "Paso 43: Caída de hombros", "descripcion": "Lleva tus hombros hasta tus orejas con fuerza. Sostén la tensión. Déjalos caer flojos de un solo golpe."},
        {"id": 44, "titulo": "Paso 44: Interregno de paz", "descripcion": "Busca el segundo de silencio absoluto que ocurre exactamente cuando terminas de exhalar el aire."},
        {"id": 45, "titulo": "Paso 45: Extensión cervical", "descripcion": "Mira hacia el techo estirando tu garganta al máximo sin mover tu espalda. Quédate ahí cinco segundos."},
        {"id": 46, "titulo": "Paso 46: Conciencia de apoyo", "descripcion": "Nota el contacto firme de tus muslos contra el asiento. Registra la estabilidad del mueble en este instante."},
        {"id": 47, "titulo": "Paso 47: Puños de choque", "descripcion": "Cierra tus puños apretando con fuerza máxima sintiendo la rigidez de tus antebrazos. Abre y relaja ya."},
        {"id": 48, "titulo": "Paso 48: Limpieza de espacio", "descripcion": "Imagina que con cada bocanada de aire sacas una preocupación burocrática fuera de tus paredes."},
        {"id": 49, "titulo": "Paso 49: Anclaje de palmas", "descripcion": "Coloca tus dos palmas planas sobre tu mesa. Empuja suavemente hacia abajo notando la solidez del material."},
        {"id": 50, "titulo": "Paso 50: Presencia soberana", "descripcion": "Regresa tu atención a este segundo exacto. Tu mente está despierta, estás a safe y recuperaste el mando."}
    ],
    
    "SALIR": {
        "agotado": [
            {"titulo": "Usa la sombra del árbol grande", "porque": "Tu mente está frita por el derroche de luz artificial y pantallas.", "que_hacer": "Hazlo ya. Camina hacia el árbol más grande de ese parque. Toca su corteza con tu mano ahora. Siente la textura fría. Quédate bajo su sombra densa mirando el aire.", "donde": "Parque público con árboles grandes.", "gps": "parks+with+shade+"},
            {"titulo": "Usa el horizonte del muelle", "porque": "Tu visión está encerrada en paredes pequeñas y biles.", "que_hacer": "Párate al final del muelle o punto alto ahora. Clava tu mirada en la línea donde se une el cielo con el agua. Quédate ahí sin moverte. Recupera el asombro.", "donde": "Muelle, mirador o orilla de lago pública.", "gps": "waterfront+viewpoints+"}
        ],
        "estresado": [
            {"titulo": "Usa la resistencia de la colina", "porque": "El estrés te tiene los hombros y el pecho trabados.", "que_hacer": "Encuentra la rampa, escalera o cuesta de esa calle o parque ahora. Súbela a paso firme sintiendo el esfuerzo. Usa la gravedad del planeta para soltar el cortisol.", "donde": "Calle elevada, escalera pública o rampa.", "gps": "public+stairs+and+ramps+"},
            {"titulo": "Usa el circuito de la acera lineal", "porque": "Tu cerebro está dando vueltas en círculos de ansiedad financiera.", "que_hacer": "Pisa la acera lineal de esa avenida pública ahora. Camina recto diez minutos seguidos sin mirar el teléfono. Siente el golpe firme de tus pies contra el concreto.", "donde": "Acera peatonal o parque lineal continuo.", "gps": "linear+parks+and+walkways+"}
        ],
        "aburrido": [
            {"titulo": "Usa los colores de los murales", "porque": "Vives en un piloto automático gris que te duerme la dopamina.", "que_hacer": "Párate frente a los dibujos de colores de esa pared urbana ahora. Busca tres detalles pequeños que nadie mira. Encuentra el asombro en lo insignificante.", "donde": "Calle con murales o distrito de diseño urbano.", "gps": "street+art+murales+"},
            {"titulo": "Usa los aromas del mercado abierto", "porque": "Has perdido la calidez de la espontaneidad humana por el confort.", "que_hacer": "Camina entre la multitud de ese mercado al aire libre ahora. Huele las frutas frescas, mira los objetos raros. Toca un producto gratis. Conecta ya.", "donde": "Mercado de pulgas, feria comunitaria o farmers market.", "gps": "farmers+markets+and+flea+markets+"}
        ]
    }
}

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    opcion_usuario = str(payload.get("modo", "")).strip().upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
    mente = str(payload.get("mente", "agotado")).lower()
    budget = str(payload.get("budget", "0"))
    perfil = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).strip().lower()   
    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"
    palabras_veteranos = ["veterano", "veteranos", "ejercito", "fuerzas+armadas", "irak", "trauma", "post_trauma"]
    palabras_gobierno = ["gobierno", "federal", "estatal", "oficina", "burocracia", "empleado+publico"]
    palabras_ancianos = ["anciano", "ancianos", "adulto+mayor", "abuelo", "abuela", "viejo", "vejez", "edad", "senior"]
    palabras_directivos = ["jefe", "jefes", "director", "directivo", "gerente", "ceo", "ejecutivo", "manager", "dueño", "corporativo"]
    palabras_lesionados = ["lesionado", "lesionada", "lesion", "lesión", "herido", "herida", "accidente", "accidentado", "compensacion", "workcomp", "dolor+espalda"]
    palabras_discapacitados = ["discapacidad", "discapacitado", "discapacitada", "silla", "ruedas", "limitado", "limitada", "paralisis", "parálisis", "ciego", "sordo", "accesible"]

    recordatorios_comunes = [
        "Sigue el pulso azul ahora. Estás conmigo.",
        "No mires tus biles. Respira ya.",
        "Mantén el ritmo ahora. Estás ganando control.",
        "Siente el peso fuera de tus hombros en este segundo.",
        "Te estoy acompañando. No estás solo. Hazlo conmigo.",
        "Siente el aire limpiando tu pecho ahora mismo.",
        "El piloto automático está apagado. Continúa.",
        "Quédate en este instante. El presente es tuyo."
    ]

    recordatorios_veteranos = [
        "Soldado, la guerra terminó. Estás en casa y estás a salvo conmigo ahora. Respira.",
        "Siente tus pies firmes en el suelo de tu país. El peligro ya pasó. Mantén el pulso.",
        "No estás solo en la trinchera mental. Tu batallón de armas está contigo in este segundo.",
        "Suelta la guardia ahora. Escucha mi voz. Recupera el control de tu mente ya.",
        "El trauma no es dueño de tu vida. Tú mandas en este motor físico hoy. Continúa.",
        "Siente el oxígeno entrando a tu pecho. Eres fuerte, sobreviviste. Camina hacia la luz."
    ]

    recordatorios_gobierno = [
        "Apaga la burocracia en este segundo. Tu mente no le pertenece al estado. Respira.",
        "Suelta la presión del sistema ahora. Eres un ser humano libre fuera de esa oficina.",
        "El papeleo y las llamadas pueden esperar. Quédate en este instante de poder.",
        "Siente cómo tus costillas se expanden limpiando el cortisol acumulado hoy.",
        "No tienes que sostener el peso de la administración tú solo. Suelta los hombros ya.",
        "Recupera tu autonomía activa en este minuto. Tu salud mental es lo único que importa."
    ]

    recordatorios_ancianos = [
        "Estás seguro conmigo en esta sala ahora. Siente la paz de tus años. Respira despacio.",
        "Tu historia tiene un valor inmenso. No estás solo en este segundo. Sigue el pulso azul.",
        "Siente el calor de tus manos ahora. Tu cuerpo está vivo y en calma en este instante.",
        "Suelta la prisa del mundo exterior. Quédate en este minuto conmigo. Lo estás haciendo bien.",
        "Tu presencia es un regalo hoy. Siente el aire llenando tus pulmones con suavidad."
    ]

    recordatorios_directivos = [
        "Suelta el control en este segundo. Nadie te está evaluando ahora. Apaga tu mente. Respira.",
        "Ya no tienes que decidir nada en este minuto. Yo tengo el mando. Déjate guiar ya.",
        "El peso de la compañía no está en tus hombros en esta sala. El suelo te sostiene gratis.",
        "Siente el aire limpiando tu cabeza. Olvida los números, las metas y las juntas ahora.",
        "Respira despacio. Saca la urgencia de tus pulmones. Estás a salvo del teléfono hoy.",
        "Tú eres más que tu rango o tu empresa. Recupera tu presencia humana en este instante."
    ]

    recordatorios_lesionados = [
        "Tu cuerpo está sanando en este segundo. Suelta el rencor contra el trabajo. Respira ya.",
        "El accidente quedó atrás. Siente tu pulso in este instante de calma. Hazlo conmigo.",
        "No te apresures. Tu única labor hoy es recuperar tu motor físico en esta sala.",
        "Siente el aire entrando suavemente. Dale descanso a la zona herida ahora mismo.",
        "La presión de las cuentas no va a acelerar tu salud. Suelta la prisa. Quédate aquí.",
        "Te estoy acompañando en este proceso. Tu fuerza biológica es real. Mantén el ritmo azul."
    ]

    recordatorios_discapacitados = [
        "Tu mente no tiene límites físicos. Eres el soberano de tus pensamientos hoy. Respira.",
        "Siente la estabilidad de tu soporte ahora. El presente te rodea en este segundo fijos.",
        "No mires las barreras de la calle. Mira el Sendero Luminoso de tu mente ahora mismo.",
        "Siente el viento entrando por tus pulmones. Tu energía es libre en esta sala conmigo.",
        "Estoy al lado tuyo. Tomo el mando de tu descompresión sensorial en este instante.",
        "Tu conciencia está despierta y activa. Gobiernas tu respiración con el pulso azul ya."
    ]

    recordatorios_personalizados = [
        "Inicia tu protocolo personalizado. Tu caso es único. Escucha mi dirección ahora.",
        "Rompemos tu piloto automático de forma específica en este segundo. Sigue el pulso.",
        "No permitas que tu mente ruede por los mismos carriles aburridos. Despierta ya.",
        "Tomo el mando absoluto de tus decisiones en este instante porque lo necesitas.",
        "Tu agobio existencial se detiene en este rincón del tiempo. Quédate conmigo hoy.",
        "Siente el oxígeno limpiando los nudos más profundos de tu pecho ahora mismo.",
        "Estás seguro, estás en el sendero luminoso. Avanza conmigo paso a paso ya."
    ]
       if  opcion_usuario == "CASA":
       elif any(p in desahogo for p in palabras_veteranos + palabras_gobierno + palabras_ancianos + palabras_directivos + palabras_lesionados + palabras_discapacitados) or perfil in ["accesible", "familia"] or (desahogo and len(desahogo) > 5):

            if any(v in desahogo for v in palabras_veteranos):
                audios_choque = recordatorios_veteranos
                tipo_protocolo_master = "CLINICO_INTENSIVO_50_VET"
                catalogo_enviar = BASE_MISIONES["CASA"]

            elif any(g in desahogo for g in palabras_gobierno):
                audios_choque = recordatorios_gobierno
                tipo_protocolo_master = "CLINICO_INTENSIVO_50_GOB"
                catalogo_enviar = BASE_MISIONES["CASA"]

            elif any(d in desahogo for d in palabras_directivos):
                audios_choque = recordatorios_directivos
                tipo_protocolo_master = "CLINICO_EJECUTIVO_30"
                catalogo_enviar = list(BASE_MISIONES["CASA"])[:30]

                for m in catalogo_enviar:
                    m["titulo"] = m["titulo"].replace("Foco", "Suelte").replace("Orden", "Desconexión")

            elif any(l in desahogo for l in palabras_lesionados):
                audios_choque = recordatorios_lesionados
                tipo_protocolo_master = "CLINICO_LESIONADOS_30"
                catalogo_enviar = list(BASE_MISIONES["CASA"])[:30]

                for m in catalogo_enviar:
                    m["titulo"] = m["titulo"].replace("Aprieta", "Siente").replace("Sacudida", "Estiramiento suave")

            elif any(x in desahogo for x in palabras_discapacitados) or perfil == "accessible":
                audios_choque = recordatorios_discapacitados
                tipo_protocolo_master = "CLINICO_DISCAPACIDAD_30"
                catalogo_enviar = list(BASE_MISIONES["CASA"])[:30]

                for m in catalogo_enviar:
                    m["titulo"] = m["titulo"].replace("Párate", "Siéntate recto").replace("Camina", "Respira en tu sitio")

            else:
                audios_choque = recordatorios_personalizados
                tipo_protocolo_master = "CLINICO_PERSONALIZADO_50"
                catalogo_enviar = BASE_MISIONES["CASA"]

            return JSONResponse({
                "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
                "tipo_protocolo": tipo_protocolo_master,
                "misiones": catalogo_enviar,
                "recordatorios_voz_choque": audios_choque
            })

        else:
            misiones_comunes = list(BASE_MISIONES["CASA"])
            random.shuffle(misiones_comunes)

            return JSONResponse({
                "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
                "tipo_protocolo": "COMUN_RAPIDO",
                "misiones": misiones_comunes[:3],
                "recordatorios_voz_choque": recordatorios_comunes
            })

    else:
        # APRENDIZAJE INTELIGENTE DE COMPORTAMIENTO
        if desahogo and desahogo not in HISTORIAL_IDEAS_NUEVAS:
            palabras_existentes = set(" ".join(HISTORIAL_IDEAS_NUEVAS).split())
            palabras_nuevas = set(desahogo.split())

            if not palabras_nuevas.issubset(palabras_existentes):
                HISTORIAL_IDEAS_NUEVAS.append(desahogo)

        if len(HISTORIAL_IDEAS_NUEVAS) > 1000:
            HISTORIAL_IDEAS_NUEVAS.pop(0)

        # Configuración de respuesta económica y acompañamiento
        precio_real = (
            "GASTO: Cero dólares. La libertad mental hoy es completamente gratis."
            if budget == "0"
            else "GASTO: Rango bajo y controlado. Un intercambio justo."
        )

        quienes_van = (
            "ACOMPAÑAMIENTO: Vas solo contigo mismo a romper tus cadenas hoy."
            if perfil == "solo"
            else "ACOMPAÑAMIENTO: Entorno apto para guiar y proteger a tus niños y familia."
            if perfil == "familia"
            else "ACOMPAÑAMIENTO: Sendero adaptado con accesibilidad física total garantizada."
        )

        # Selección de misión base
        info = random.choice(BASE_MISIONES["SALIR"]["aburrido"])

        if mente in BASE_MISIONES["SALIR"]:
            info = random.choice(BASE_MISIONES["SALIR"][mente])

        gps_query = info["gps"]
        donde_base = info["donde"]

        titulo_accion = "REGRESO A LA PRESENCIA ABSOLUTA"

        entorno_texto = (
            "Infraestructura natural pública de USA, aire, nubes, agua, tierra y viento."
        )

guia_masticada = f"""VEREDICTO: {info['titulo']}.
EL MOTIVO: Aunque lo tengas todo materialmente, estás atrapado en el piloto automático gris de la rutina diaria.
ACCIÓN OBLIGATORIA: Camina hacia este punto ahora. No mires tu pantalla. Siente el oxígeno, el viento y la tierra bajo tus pies ya.
EL TIEMPO: En este mismo instante. Tu desahogo es ahora.
EL PROPÓSITO: Romper los barrotes de tu mente y recordar quién eres fuera del sistema urbano.
{quienes_van} {precio_real}"""

        # Intervenciones críticas
        if any(p in desahogo for p in ["hospital", "clinica", "clínica", "enfermo", "dolor", "medico", "médico", "seguro", "salud", "pastillas", "remedio"]):
            gps_query = "community+health+centers+free+clinics"
            entorno_texto = "Red de clínicas comunitarias y centros de atención médica preventiva de USA."
            titulo_accion = "INTERVENCIÓN MÉDICA Y ESCUDO DE SALUD BIOLÓGICA"

            guia_masticada = f"VEREDICTO: Protección inmediata de tu templo físico. POR QUÉ: No puedes sanar tu mente si descuidas tu cuerpo. El dolor te tiene paralizado. QUÉ HACER: Acude ahora mismo por la mañana a este centro comunitario. Solicita revisión gratis. PARA QUÉ: Tomar el control absoluto de tu salud sin gastar un centavo hoy. HAZLO CONMIGO. {quienes_van}"

        if any(p in desahogo for p in ["casa", "alquilar", "alquiler", "renta", "rentar", "hogar", "apartamento", "mudanza", "zillow", "realtor"]):
            gps_query = "homes+for+rent"
            entorno_texto = "Infraestructura habitacional e inmobiliaria masiva de USA (Zillow / Realtor)."
            titulo_accion = "LOCALIZACIÓN DE TU NUEVO ESPACIO VITAL"

            guia_masticada = f"VEREDICTO: Mudanza y cambio de entorno. POR QUÉ: Tu mente está atrapada en el agobio de tu espacio actual. ACCIÓN OBLIGATORIA: Explora viviendas disponibles en tu zona. PARA QUÉ: Romper el letargo y encaminarte hacia tu nuevo hogar. {quienes_van} {precio_real}"

        if any(p in desahogo for p in ["escribir", "hablar", "pareja", "amigo", "amigos", "aislado", "solo", "gente", "facebook", "whatsapp", "instagram", "social"]):
            gps_query = "community+centers+social+clubs"
            entorno_texto = "Ecosistema de interacción social y comunicación directa."

            titulo_accion = "ROMPER EL AISLAMIENTO INDIVIDUAL"

            guia_masticada = f"VEREDICTO: Conexión humana inmediata. POR QUÉ: Eres prisionero del aislamiento digital. QUÉ HACER: Únete o interactúa con una comunidad. PARA QUÉ: Reconectar con la sociedad. {quienes_van} {precio_real}"

        if any(p in desahogo for p in ["comprar", "bici", "bicicleta", "ropa", "comida", "walmart", "amazon", "tienda"]):
            plataforma_minorista = random.choice(["walmart", "ross+dress+for+less", "dds+discounts", "burlington"])

            gps_query = f"{plataforma_minorista}+store"
            entorno_texto = "Tiendas minoristas y mercados de descuento."

            titulo_accion = f"HACKEO DE ABASTO MASIVO EN {plataforma_minorista.upper()}"

            guia_masticada = f"VEREDICTO: Intervención comercial. QUÉ HACER: Explora opciones de compra ahora. PARA QUÉ: Activar dopamina y romper rutina. {quienes_van} {precio_real}"

        if any(p in desahogo for p in ["trabajo", "empleo", "deudas", "biles", "bills", "miseria", "explotacion"]):
            gps_query = "agencias+de+empleo+staffing+agencies"
            entorno_texto = "Centros de contratación laboral inmediata."

            titulo_accion = "ESCUDO DE AUTONOMÍA FINANCIERA"

            guia_masticada = f"VEREDICTO: Reorientación laboral. QUÉ HACER: Acude a agencias de empleo. PARA QUÉ: Recuperar estabilidad financiera. {quienes_van} {precio_real}"
                    {"id": 25, "titulo": "Paso 25: Transferencia térmica", "descripcion": "Frota tus manos con fuerza ahora mismo hasta sentir calor real. Colócalas sobre tus hombros cansados. Siente el alivio ya."},
        {"id": 26, "titulo": "Paso 26: Sonido periférico", "descripcion": "Presta atención al ruido más lejano que ocurra fuera de tu edificio ahora mismo. Identifícalo en silencio."},
        {"id": 27, "titulo": "Paso 27: Balanceo mecánico", "descripcion": "Inclina tu columna suavemente de izquierda a derecha. Siente la elasticidad de tus costillas ahora."},
        {"id": 28, "titulo": "Paso 28: Foco transparente", "descripcion": "Mira fijamente un vaso o una botella transparente por sesenta segundos fijos. No desvíes la mirada."},
        {"id": 29, "titulo": "Paso 29: Descompresión facial", "descripcion": "Abre tu boca lo más grande que puedas y mueve tu mandíbula de lado a lado. Suelta el estrés retenido."},
        {"id": 30, "titulo": "Paso 30: Marcha ralentizada", "descripcion": "Camina cinco pasos dentro de tu espacio de la forma más lenta posible. Siente cada milímetro del movimiento."},
        {"id": 31, "titulo": "Paso 31: Presión digital", "descripcion": "Presiona suavemente tus sienes con las yemas de tus dedos haciendo círculos lentos por treinta segundos."},
        {"id": 32, "titulo": "Paso 32: Captura de oxígeno", "descripcion": "Toma aire profundo notando cómo se expande tu abdomen. Retén dos segundos y exhala despacio."},
        {"id": 33, "titulo": "Paso 33: Apertura torácica", "descripcion": "Lleva tus codos hacia atrás con fuerza e intenta que tus omóplatos se toquen. Abre tu pecho ahora."},
        {"id": 34, "titulo": "Paso 34: Abandono de carga", "descripcion": "Suelta toda la fuerza de tus piernas. Deja que el piso absorba toda la resistencia de tu peso gratis."},
        {"id": 35, "titulo": "Paso 35: Conteo de aislamiento", "descripcion": "Cuenta de forma regresiva en tu mente del treinta al uno despacio. Apaga el ruido de la sala."},
        {"id": 36, "titulo": "Paso 36: Textura real", "descripcion": "Pasa la palma de tu mano sobre tu ropa o cortina. Concéntrate puramente en el roce del tejido."},
        {"id": 37, "titulo": "Paso 37: Expansión falángica", "descripcion": "Abre tus manos separando los dedos lo más posible con rigidez por cinco segundos. Suelta de golpe."},
        {"id": 38, "titulo": "Paso 38: Murmullo biológico", "descripcion": "Tápate los oídos con tus dedos y escucha el sonido interno de tu respiración por veinte segundos."},
        {"id": 39, "titulo": "Paso 39: Foco milimétrico", "descripcion": "Elige un tornillo, marca o punto mínimo de la pared. Clava tus ojos ahí sin parpadear un momento."},
        {"id": 40, "titulo": "Paso 40: Péndulo suelto", "descripcion": "Deja tus brazos completamente muertos a los lados y balancéalos como un péndulo flojo."},
        {"id": 41, "titulo": "Paso 41: Registro dérmico", "descripcion": "Siente la temperatura exacta del aire del cuarto golpeando la piel de tus manos ahora mismo."},
        {"id": 42, "titulo": "Paso 42: Expulsión zombi", "descripcion": "Inhala inflando el pecho al máximo. Suelta el aire con un suspiro fuerte por la boca liberando la rutina."},
        {"id": 43, "titulo": "Paso 43: Caída de hombros", "descripcion": "Lleva tus hombros hasta tus orejas con fuerza. Sostén la tensión. Déjalos caer flojos de un solo golpe."},
        {"id": 44, "titulo": "Paso 44: Interregno de paz", "descripcion": "Busca el segundo de silencio absoluto que ocurre exactamente cuando terminas de exhalar el aire."},
        {"id": 45, "titulo": "Paso 45: Extensión cervical", "descripcion": "Mira hacia el techo estirando tu garganta al máximo sin mover tu espalda. Quédate ahí cinco segundos."},
        {"id": 46, "titulo": "Paso 46: Conciencia de apoyo", "descripcion": "Nota el contacto firme de tus muslos contra el asiento. Registra la estabilidad del mueble en este instante."},
        {"id": 47, "titulo": "Paso 47: Puños de choque", "descripcion": "Cierra tus puños apretando con fuerza máxima sintiendo la rigidez de tus antebrazos. Abre y relaja ya."},
        {"id": 48, "titulo": "Paso 48: Limpieza de espacio", "descripcion": "Imagina que con cada bocanada de aire sacas una preocupación fuera de tus paredes."},
        {"id": 49, "titulo": "Paso 49: Anclaje de palmas", "descripcion": "Coloca tus dos palmas planas sobre tu mesa. Empuja suavemente hacia abajo notando la solidez del material."},
        {"id": 50, "titulo": "Paso 50: Presencia soberana", "descripcion": "Regresa tu atención a este segundo exacto. Tu mente está despierta, estás a salvo y recuperaste el mando."}
    ]
}
"SALIR": {
    "agotado": [
        {
            "titulo": "Usa la sombra del árbol grande",
            "porque": "Tu mente está frita por el derroche de luz artificial y pantallas.",
            "que_hacer": "Hazlo ya. Camina hacia el árbol más grande de ese parque. Toca su corteza con tu mano ahora. Siente la textura fría. Quédate bajo su sombra densa.",
            "donde": "Parque público con árboles grandes.",
            "gps": "parks+with+shade+"
        },
        {
            "titulo": "Usa el horizonte del muelle",
            "porque": "Tu visión está encerrada en paredes pequeñas.",
            "que_hacer": "Párate al final del muelle o punto alto. Mira la línea del horizonte sin moverte. Recupera el asombro.",
            "donde": "Muelle o mirador público.",
            "gps": "waterfront+viewpoints+"
        }
    ],
    "estresado": [
        {
            "titulo": "Usa la resistencia de la colina",
            "porque": "El estrés te tiene el cuerpo rígido.",
            "que_hacer": "Sube una rampa o cuesta caminando firme. Usa el esfuerzo físico para liberar tensión.",
            "donde": "Escaleras o colina pública.",
            "gps": "public+stairs+and+ramps+"
        },
        {
            "titulo": "Usa la acera lineal",
            "porque": "Tu mente gira en bucles de ansiedad.",
            "que_hacer": "Camina recto 10 minutos sin mirar el teléfono.",
            "donde": "Acera o parque lineal.",
            "gps": "linear+parks+and+walkways+"
        }
    ],
    "aburrido": [
        {
            "titulo": "Usa los murales urbanos",
            "porque": "Tu dopamina está apagada por rutina.",
            "que_hacer": "Observa detalles pequeños en el arte urbano.",
            "donde": "Calles con murales.",
            "gps": "street+art+murales+"
        },
        {
            "titulo": "Usa el mercado abierto",
            "porque": "Falta estímulo humano real.",
            "que_hacer": "Camina entre personas, huele, observa y toca productos.",
            "donde": "Feria o farmers market.",
            "gps": "farmers+markets+and+flea+markets+"
        }
    ]
}
    # ================================
    # CASOS ESPECIALES AVANZADOS (CAPA FINAL DE CONTROL)
    # ================================

    if any(p in desahogo for p in ["viajar", "hotel", "vacaciones", "airbnb", "booking"]):
        gps_query = "hotels+and+travel+destinations"
        entorno_texto = "Red global de hospedaje y turismo."
        titulo_accion = "ESCAPE DE MOVILIDAD GLOBAL"
        guia_masticada = f"VEREDICTO: Activación de viaje. POR QUÉ: Necesitas romper el entorno actual. QUÉ HACER: Explora opciones de viaje ahora. {quienes_van} {precio_real}"

    if any(p in desahogo for p in ["naturaleza", "playa", "mar", "río", "bosque"]):
        gps_query = "beaches+parks+nature+trails"
        entorno_texto = "Espacios naturales abiertos."
        titulo_accion = "RECONEXIÓN NATURAL DIRECTA"
        guia_masticada = f"VEREDICTO: Contacto con naturaleza. POR QUÉ: Tu sistema nervioso necesita descompresión. QUÉ HACER: Ve a un entorno natural ahora mismo. {quienes_van} {precio_real}"

    if any(p in desahogo for p in ["gym", "ejercicio", "fitness", "correr", "entrenar"]):
        gps_query = "gyms+fitness+centers+parks+running+trails"
        entorno_texto = "Infraestructura de actividad física."
        titulo_accion = "ACTIVACIÓN BIOMECÁNICA"
        guia_masticada = f"VEREDICTO: Activación física inmediata. POR QUÉ: Tu cuerpo necesita descarga de energía. QUÉ HACER: Muévete ahora mismo. {quienes_van} {precio_real}"

    if any(p in desahogo for p in ["comida", "hambre", "restaurante", "pizza", "taco", "sushi"]):
        gps_query = "restaurants+food+near+me"
        entorno_texto = "Ecosistema gastronómico local."
        titulo_accion = "REABASTECIMIENTO SENSORIAL"
        guia_masticada = f"VEREDICTO: Alimentación inmediata. POR QUÉ: Tu cuerpo necesita energía real. QUÉ HACER: Ve a comer ahora. {quienes_van} {precio_real}"


    # ================================
    # NORMALIZACIÓN FINAL DE GPS
    # ================================

    gps_query = gps_query.replace(" ", "+")

    link_google_maps_vivo = (
        "https://www.google.com/maps/search/?api=1&query="
        + gps_query
        + "+"
        + anclaje_geografico.replace(" ", "+")
    )

    link_hoteles_fijo = "https://www.google.com/maps/search/hotels+near+me"
    link_parques_fijo = "https://www.google.com/maps/search/parks+near+me"


    # ================================
    # RESPUESTA FINAL CONSOLIDADA
    # ================================

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_titulo": titulo_accion,
        "destino_entorno": entorno_texto,
        "destino_instruccion": guia_masticada.strip(),
        "destino_coordenadas_gps": link_google_maps_vivo,
        "modo": opcion_usuario,
        "perfil": perfil,
        "estado": estado,
        "zip": zip_code,
        "region": region,
        "mente": mente,
        "budget": budget,
        "alternativas_contingencia": [
            {
                "titulo": "HACKEO COMPLEMENTARIO EN LÍNEA (TIENDAS)",
                "entorno": "Plataformas globales de consumo.",
                "gps": "https://amazon.com"
            },
            {
                "titulo": "ESCAPES DE HOSPEDAJE (HOTELES/SPAS)",
                "entorno": "Red hotelera global.",
                "gps": link_hoteles_fijo
            },
            {
                "titulo": "REFUGIOS NATURALES",
                "entorno": "Espacios públicos naturales.",
                "gps": link_parques_fijo
            }
        ]
    })
# ================================
# SISTEMA DE ARRANQUE FINAL (PRODUCCIÓN)
# ================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))

    # ================================
    # VALIDACIÓN DE ENTORNO
    # ================================
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"

    print("===================================")
    print("OPEN THAN GO SYSTEM - ENGINE ONLINE")
    print("PORT:", port)
    print("DEBUG:", debug_mode)
    print("STATUS: ACTIVE")
    print("===================================")

    # ================================
    # PROTECCIÓN BÁSICA DE ARRANQUE
    # ================================
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=debug_mode
        )
    except Exception as e:
        print("ERROR CRÍTICO EN SERVIDOR:", str(e))

        # fallback de seguridad mínimo
        try:
            uvicorn.run(
                app,
                host="127.0.0.1",
                port=port,
                log_level="error"
            )
        except Exception as e2:
            print("FALLO TOTAL DEL SISTEMA:", str(e2))

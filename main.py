# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.3.5.0
# Company: May Roga LLC
# File: main.py
# PARTE 1 DE 3: Inicialización de Red y Misiones de Casa (1 a 18)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Catálogo Maestro del Despertador Humano: Acciones Cortas Directas e Inmediatas
BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Hazlo conmigo ahora. Escanea tu cuerpo en este segundo. Ubica el peso exacto en tu espalda. Míralo. Siente que estás aquí, vivo.", "para_que": "Para recuperar tu control."},
        {"id": 2, "titulo": "Desconexión de biles", "descripcion": "Siente tu silla ahora. Nota cómo sostiene tu peso gratis. El piso está firme. No sostengas el mundo tú solo en este minuto. Déjate caer.", "para_que": "Para recordarte que el suelo está firme."},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Dale la vuelta a tu teléfono sobre la mesa ya. Mira una esquina de tu techo. Nota su color, sus líneas. Quédate ahí treinta segundos fijos.", "para_que": "Para romper el bucle visual zombi."},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Imagina que dejas caer una mochila pesada llena de deudas y estrés ahora. Siente tus hombros libres. Se caen de golpe. El peso ya no está.", "para_que": "Para limpiar tu pecho de inmediato."},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Busca un vaso de agua ahora mismo. Dale un trago muy pequeño. Siente el líquido frío bajando por tu garganta. Te limpia por dentro. Es la vida.", "para_que": "Para despertar tus sentidos dormidos."},
        {"id": 6, "titulo": "Liberación de nudos", "descripcion": "Aprieta tus dos puños con toda tu fuerza ahora. Siente la rabia acumulada. Mantén tres segundos. Ahora abre las manos de golpe. Suéltalo todo.", "para_que": "Para soltar el estrés acumulado ya."},
        {"id": 7, "titulo": "El aire de la calle", "descripcion": "Camina hacia la ventana o puerta más cercana ahora. Ábrela. Deja que el aire te golpee la cara en este instante. Siente el viento exterior.", "para_que": "Para recordarte que hay vida fuera."},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira tus muñecas y tus tobillos despacio ahora. Siente tus articulaciones. Tu cuerpo es tuyo, no del sistema. Tú gobiernas este motor físico.", "para_que": "Para recuperar tu autonomía activa ya."},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos conmigo ahora. Di una sola cosa buena que tienes hoy en voz alta. Tu salud, tus manos, tu vida. Dilo con fuerza. Quédate con eso.", "para_que": "Para encender tu chispa oculta ahora."},
        {"id": 10, "titulo": "Orden de tu espacio", "descripcion": "Alinea tres objetos de tu mesa perfectamente ahora. Pon orden fuera para poner orden dentro. Hazlo ya.", "para_que": "Para calmar el caos en tu mente."},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate los zapatos ahora. Apoya las plantas de tus pies firmemente en el piso. Siente el frío del suelo. Conéctate.", "para_que": "Para bajarte de la nube de la ansiedad."},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Estira tus brazos hacia arriba con fuerza en este segundo. Imagina que tocas el techo. Mantén la tensión. Suelta de golpe.", "para_que": "Para liberar la espalda trabada."},
        {"id": 13, "titulo": "Foco en lo olvidado", "descripcion": "Mira a tu alrededor. Elige una tarea mínima que estabas ignorando en tu cuarto. Hazla ahora mismo. Termínala ya.", "para_que": "Para ganarle a la pereza de la rutina."},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza tu espalda en este instante. Imagina que un hilo invisible tira de tu cabeza hacia arriba. Respira hondo.", "para_que": "Para activar tu alerta biológica hoy."},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una pared o una superficie de metal fría ahora mismo. Siente la temperatura real con tus dedos. Quédate ahí.", "para_que": "Para aterrizar tus pensamientos."},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la puerta principal de tu casa ahora. Deja que el aire ruede y cambie el ambiente de tu sala. Huele el cambio.", "para_que": "Para sacar el encierro gris de tu día."},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude tus manos y tus piernas con fuerza ahora. Como si te quitaras agua de encima. Hazlo por diez segundos.", "para_que": "Para romper el zombi que llevas dentro."},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira por tu ventana ahora. Enfoca tus ojos en el objeto más lejano que alcances a ver en la calle. No mires nada cerca.", "para_que": "Para descansar tu enfoque visual."},
# PARTE 2 DE 3: Continuación del catálogo de CASA (19 a 50) y misiones de SALIR
        {"id": 19, "titulo": "Paso 19: Recordar la infancia", "descripcion": "Cierra los ojos y recuerda un juego o un momento feliz de tu niñez."},
        {"id": 20, "titulo": "Paso 20: Sonrisa forzada", "descripcion": "Dibuja una sonrisa en tu cara por 15 segundos. Tu cerebro cambiará su química."},
        {"id": 21, "titulo": "Paso 21: Agradecimiento final", "descripcion": "Cierra los ojos y agradece una sola cosa buena que te haya pasado en esta semana."},
        {"id": 22, "titulo": "Paso 22: Relaja los ojos", "descripcion": "Cierra los ojos y tápalos suavemente con las palmas de tus manos templadas por un minuto."},
        {"id": 23, "titulo": "Paso 23: Ritmo cardíaco", "descripcion": "Coloca tu mano derecha en tu pecho y siente los latidos de tu corazón en silencio."},
        {"id": 24, "titulo": "Paso 24: Suelta el cuello", "descripcion": "Mueve tu cabeza en círculos muy lentos para liberar la tensión acumulada al mirar pantallas."},
        {"id": 25, "titulo": "Paso 25: Ejercicio de palmas", "descripcion": "Frota tus manos con fuerza hasta sentir calor y luego colócalas sobre tus hombros."},
        {"id": 26, "titulo": "Paso 26: Sonidos lejanos", "descripcion": "Trata de identificar el sonido más lejano que ocurra fuera de tu casa ahora mismo."},
        {"id": 27, "titulo": "Paso 27: Estiramiento lateral", "descripcion": "Inclina tu cuerpo suavemente hacia un lado y luego hacia el otro de forma fluida."},
        {"id": 28, "titulo": "Paso 28: El vaso vacío", "descripcion": "Mira un vaso vacío y concéntrate en su forma por un minuto entero sin pensar en biles."},
        {"id": 29, "titulo": "Paso 29: Suelta la mandíbula", "descripcion": "Abre la boca grande y mueve la mandíbula de lado a lado para soltar el estrés."},
        {"id": 30, "titulo": "Paso 30: Pasos lentos", "descripcion": "Camina diez pasos dentro de tu habitación de la forma más lenta que te sea posible."},
        {"id": 31, "titulo": "Paso 31: Masaje suave", "descripcion": "Usa las yemas de tus dedos para dar un suave masaje circular en tus sienes."},
        {"id": 32, "titulo": "Paso 32: Conciencia del aire", "descripcion": "Siente cómo entra el aire frío por tu nariz y cómo sale aire más cálido."},
        {"id": 33, "titulo": "Paso 33: Espalda firme", "descripcion": "Siéntate derecho y empuja tus omóplatos hacia atrás para abrir tu pecho."},
        {"id": 34, "titulo": "Paso 34: Apoyo total", "descripcion": "Siente cómo tu silla y el suelo sostienen todo tu peso sin que hagas esfuerzo."},
        {"id": 35, "titulo": "Paso 35: Cuenta regresiva", "descripcion": "Cuenta hacia atrás del veinte al uno despacio en tu mente para calmar el ruido."},
        {"id": 36, "titulo": "Paso 36: Toca tu entorno", "descripcion": "Busca un objeto de madera o tela y pasa tus dedos notando su textura real."},
        {"id": 37, "titulo": "Paso 37: Estira los dedos", "descripcion": "Abre tus manos separando los dedos lo más que puedas por cinco segundos y suelta."},
        {"id": 38, "titulo": "Paso 38: Sonidos internos", "descripcion": "Presta atención al sonido de tu propia respiración sin forzarla ni cambiarla."},
        {"id": 39, "titulo": "Paso 39: Mirada fija", "descripcion": "Elige un punto pequeño en la pared y míralo fijamente sin parpadear un momento."},
        {"id": 40, "titulo": "Paso 40: Suelta los brazos", "descripcion": "Deja colgar tus brazos a los lados de tu cuerpo y sacúdelos con suavidad."},
        {"id": 41, "titulo": "Paso 41: Conciencia de ropa", "descripcion": "Nota el contacto y el peso de la ropa sobre tu piel por treinta segundos."},
        {"id": 42, "titulo": "Paso 42: Aire profundo", "descripcion": "Toma aire inflando tu vientre, retenlo tres segundos y déjalo salir muy lento."},
        {"id": 43, "titulo": "Paso 43: Rotación de hombros", "descripcion": "Lleva tus hombros hacia tus orejas y luego déjalos caer de golpe para soltar la rutina."},
        {"id": 44, "titulo": "Paso 44: Escucha el silencio", "descripcion": "Busca el espacio de silencio que queda justo entre una respiración y la siguiente."},
        {"id": 45, "titulo": "Paso 45: Mirada al techo", "descripcion": "Mira hacia el techo y estira tu cuello suavemente sin mover tus hombros."},
        {"id": 46, "titulo": "Paso 46: Siente la base", "descripcion": "Siente el contacto firme de tus piernas con la silla y concéntrate en esa firmeza."},
        {"id": 47, "titulo": "Paso 47: Puños firmes", "descripcion": "Aprieta tus manos haciendo puños con fuerza por tres segundos y luego ábrelas."},
        {"id": 48, "titulo": "Paso 48: Limpieza mental", "descripcion": "Imagina que cada exhalación saca una preocupación aburrida fuera de tu habitación."},
        {"id": 49, "titulo": "Paso 49: Tocar la mesa", "descripcion": "Coloca ambas palmas sobre tu mesa o escritorio y nota la estabilidad del mueble."},
        {"id": 50, "titulo": "Paso 50: Presencia absoluta", "descripcion": "Regresa tu atención a este instante. Estás seguro, estás en casa y tienes el control."}
    ],
    "SALIR": {
        "agotado": [
            {"titulo": "Usa la sombra del árbol grande", "porque": "Tu mente está frita por el derroche de luz artificial y pantallas.", "que_hacer": "Hazlo ya. Camina hacia el árbol más grande de ese parque. Toca su corteza con tu mano ahora. Siente la textura fría. Quédate bajo su sombra densa.", "donde": "Parque público con árboles grandes.", "gps": "parks+with+shade+"},
            {"titulo": "Usa el horizonte del muelle", "porque": "Tu visión está encerrada en paredes pequeñas y biles.", "que_hacer": "Párate al final del muelle o punto alto ahora. Clava tu mirada en la línea donde se une el cielo con el agua. Quédate ahí sin moverte. Recupera el asombro.", "donde": "Muelle, mirador o orilla de lago pública.", "gps": "waterfront+viewpoints+"}
        ],
        "estresado": [
            {"titulo": "Usa la resistencia de la colina", "porque": "El estrés te tiene los hombros y el pecho trabados.", "que_hacer": "Encuentra la rampa, escalera o cuesta de esa calle o parque ahora. Súbela a paso firme sintiendo el esfuerzo. Usa la gravedad del planeta para soltar el cortisol.", "donde": "Calle elevada, escalera pública o rampa.", "gps": "public+stairs+and+ramps+"},
            {"titulo": "Usa el circuito de la acera lineal", "porque": "Tu cerebro está dando vueltas en círculos de ansiedad financiera.", "que_hacer": "Pisa la acera lineal de esa avenida pública ahora. Camina recto diez minutos seguidos sin mirar el teléfono. Siente el golpe firme de tus pies contra el concreto.", "donde": "Acera peatonal o parque lineal continuo.", "gps": "linear+parks+and+walkways+"}
        ],
        "aburrido": [
            {"titulo": "Usa los colores de los murales", "porque": "Vives en un piloto automático gris que te duerme la dopamina.", "que_hacer": "Párate frente a los dibujos de colores de esa pared urbana ahora. Busca tres detalles pequeños que nadie mira. Encuentra el asombro en lo insignificante.", "donde": "Calle con murales o distrito de diseño urbano.", "gps": "street+art+murals+"},
            {"titulo": "Usa los aromas del mercado abierto", "porque": "Has perdido la calidez de la espontaneidad humana por el confort.", "que_hacer": "Camina entre la multitud de ese mercado al aire libre ahora. Huele las frutas frescas, mira los objetos raros. Toca un producto gratis. Conecta ya.", "donde": "Mercado de pulgas, feria comunitaria o farmers market.", "gps": "farmers+markets+and+flea+markets+"}
        ]
    }
}
# PARTE 3 DE 3: Lógica de API, Filtros Elásticos y Enlace Satelital Universal

@app.get("/")
async def index():
    return FileResponse('static/session.html')

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
    desahogo = str(payload.get("desahogo", "")).lower()
   
    if opcion_usuario == "CASA":
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": BASE_MISIONES["CASA"]
        })
   
    else:
        info = random.choice(BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"]))
       
        # Filtro de precio real en palabras cortas de acción
        precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if budget == "0" else "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if budget == "1" else "GASTO: Libre. El dinero es tu herramienta de escape hoy."
       
        # Filtro de acompañantes reales
        quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if perfil == "solo" else "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia." if perfil == "familia" else "ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad."

        # FILTRO DE SUPERVIVENCIA LABORAL Y BIENESTAR FINANCIERO
        palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion"]
        if any(p in desahogo for p in palabras_criticas):
            gps_query = "agencias+de+empleo+staffings+corporations"
            donde_base = "Oficinas de contratación y staffings corporativos en tu zona."
           
            guia_masticada = f"""
            DESTINO: Oficinas de empleo inmediato.
            POR QUÉ: Tu mente está bloqueada por la parálisis de las deudas y los biles.
            QUÉ HACER: Entra ya con tu identificación en mano. Habla directo con el counter.
            CUÁNDO: Ahora mismo por la mañana. Es prioridad de vida.
            PARA QUÉ: Para ganarle al agobio del dinero y tomar el control de tu economía hoy.
            {quienes_van}
            {precio_real}
            """
        else:
            # INTERVENCIÓN DE ARQUITECTURA DE ENTORNO ORDINARIO (Hackear parques, playas, murales o calles)
            if budget == "0":
                gps_query = "free+public+parks+and+beaches"
            elif budget == "1":
                gps_query = "low+cost+coffee+shops+and+local+markets"
            else:
                gps_query = info["gps"]
           
            donde_base = info["donde"]
           
            guia_masticada = f"""
            DESTINO: {info['titulo']}.
            POR QUÉ: {info['porque']}
            QUÉ HACER: {info['que_hacer']}
            CUÁNDO: Ahora mismo. Levántate de la silla ya.
            PARA QUÉ: Para romper el zombi urbano y recordar que la vida es más que pagar cuentas.
            {quienes_van}
            {precio_real}
            """

        # Adaptabilidad del Perfil Biopsicosocial sin exclusión social
        if perfil == "accesible":
            gps_query = "wheelchair+accessible+" + gps_query
        elif perfil == "family":
            gps_query = "family+friendly+" + gps_query

        # FÓRMULA GEOGRÁFICA UNIVERSAL FIJA: Usa el ZIP si existe, si no toma la combinación del cajón
        anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"
       
        # RECTIFICACIÓN MAESTRA DE VARIABLES UNIFICADAS:
        link_google_maps_vivo = f"https://www.google.com/maps/search/?api=1&query={gps_query}+in+{anclaje_geografico}".replace(" ", "+")
       
        # Estructura de salida blindada sincronizada al 100% con tu engine.js
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
            "destino_titulo": info["titulo"].upper(),
            "destino_entorno": donde_base,
            "destino_instruccion": guia_masticada.strip(),
            "destino_coordenadas_gps": link_google_maps_vivo
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py
# PARTE 1 DE 3

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

# Catálogo Maestro del Despertador Humano (Misiones Directas y Sencillas)
BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Paso 1: Encuentra tu tensión", "descripcion": "Busca el lugar de tu cuerpo donde sientes más peso o cansancio ahora mismo."},
        {"id": 2, "titulo": "Paso 2: Respira despacio", "descripcion": "Toma aire por la nariz lentamente, aguanta un momento y suéltalo por la boca."},
        {"id": 3, "titulo": "Paso 3: Suelta el teléfono", "descripcion": "Deja tu celular boca abajo sobre la mesa. Mira tres objetos en tu habitación durante un minuto."},
        {"id": 4, "titulo": "Paso 4: Adiós al peso", "descripcion": "Imagina que dejas caer al suelo una mochila muy pesada llena de cuentas y biles. Siente tus hombros libres."},
        {"id": 5, "titulo": "Paso 5: Bebe agua", "descripcion": "Bebe un vaso de agua muy despacio. Siente cómo limpia tu cuerpo. Piensa en algo bueno de tu día."},
        {"id": 6, "titulo": "Paso 6: Escaneo muscular", "descripcion": "Localiza el punto exacto donde sientes más nudos. Aprieta ese músculo 5 segundos y suéltalo."},
        {"id": 7, "titulo": "Paso 7: El inventario", "descripcion": "Escribe en un papel tres cosas que hoy te pesan. Arruga ese papel con fuerza y descártalo."},
        {"id": 8, "titulo": "Paso 8: Pausa total", "descripcion": "Detente totalmente. No hagas nada ni pienses en nada por 60 segundos."},
        {"id": 9, "titulo": "Paso 9: Escucha el entorno", "descripcion": "Cierra los ojos. Escucha tres sonidos diferentes, desde el más lejano al más cercano."},
        {"id": 10, "titulo": "Paso 10: Orden físico", "descripcion": "Alinea tres objetos de tu mesa perfectamente. Poner orden fuera ayuda a poner orden dentro."},
        {"id": 11, "titulo": "Paso 11: Pies en la tierra", "descripcion": "Apoya las plantas de tus pies firmemente en el suelo. Siente el peso de la gravedad."},
        {"id": 12, "titulo": "Paso 12: Estiramiento libre", "descripcion": "Estira tus brazos hacia arriba con fuerza como si quisieras tocar el techo y suéltalos."},
        {"id": 13, "titulo": "Paso 13: Foco mínimo", "descripcion": "Elige una tarea pequeña de tu casa que estabas ignorando y termínala ahora mismo."},
        {"id": 14, "titulo": "Paso 14: Postura recta", "descripcion": "Endereza tu columna. Imagina que un hilo invisible tira de tu cabeza hacia el cielo."},
        {"id": 15, "titulo": "Paso 15: Sentido del tacto", "descripcion": "Toca una superficie fría, como una pared o una mesa de metal. Nota su temperatura."},
        {"id": 16, "titulo": "Paso 16: Aire nuevo", "descripcion": "Abre una ventana de tu cuarto. Deja que el aire de la calle ruede y renueve tu ambiente."},
        {"id": 17, "titulo": "Paso 17: Rotación somática", "descripcion": "Gira tus muñecas y tus tobillos diez veces en círculos hacia cada dirección."},
        {"id": 18, "titulo": "Paso 18: Desconexión visual", "descripcion": "Mira por la ventana hacia el punto más lejano que alcances a ver durante dos minutos."}

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
            {"titulo": "Un paseo en el parque", "porque": "Tu mente está cansada de mirar pantallas todo el día.", "que_hacer": "QUÉ: Camina despacio rodeado de árboles verdes. CÓMO: Mira el movimiento de las hojas. CUÁNDO: Por la tarde. PARA QUÉ: Sentirte libre y en paz.", "donde": "Un parque verde con caminos llanos.", "gps": "public+parks+near+"},
            {"titulo": "Mira el agua", "porque": "El sonido y el movimiento del agua calman tus nervios de forma natural.", "que_hacer": "QUÉ: Siéntate cerca del agua a mirar el paisaje. CÓMO: Escucha el sonido del viento. CUÁNDO: Al atardecer. PARA QUÉ: Resetear tu cabeza.", "donde": "Una playa o un lago cercano.", "gps": "lakes+and+beaches+near+"}
        ],
        "estresado": [
            {"titulo": "Camina rápido", "porque": "Necesitas quemar la mala energía acumulada por la rutina.", "que_hacer": "QUÉ: Camina a paso firme sin detenerte. CÓMO: Mueve tus brazos con ritmo. CUÁNDO: En cualquier momento del día. PARA QUÉ: Soltar la rabia y el estrés.", "donde": "Una pista pública de caminar.", "gps": "walking+paths+near+"},
            {"titulo": "Mueve tu cuerpo", "porque": "El estrés traba los músculos de tu espalda y hombros.", "que_hacer": "QUÉ: Estira tus brazos hacia el cielo con fuerza. CÓMO: Gira tus hombros despacio. CUÁNDO: Al salir. PARA QUÉ: Sentirte liviano y activo.", "donde": "Un parque abierto con espacio peatonal.", "gps": "linear+parks+near+"}
        ],
        "aburrido": [
            {"titulo": "Camino de arte", "porque": "Hacer siempre lo mismo apaga tus ganas de vivir.", "que_hacer": "QUÉ: Visita un lugar con pinturas en las paredes o murales de colores. CÓMO: Mira los detalles de las calles. CUÁNDO: Fin de semana. PARA QUÉ: Despertar tu curiosidad.", "donde": "Una zona de la ciudad con murales y gente.", "gps": "street+art+murales+near+"},
            {"titulo": "El mercado local", "porque": "Necesitas ver caras nuevas, olores diferentes y colores vivos.", "que_hacer": "QUÉ: Camina entre los puestos de frutas y ropa. CÓMO: Mira las cosas raras que venden. CUÁNDO: Por la mañana. PARA QUÉ: Romper la rutina aburrida.", "donde": "Un mercado abierto o feria del barrio.", "gps": "farmers+market+near+"}
        ]
    }
}

# PARTE 3 DE 3: Rutas de control, Filtros Dinámicos de Supervivencia y Encendido del Servidor

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    
    # Captura limpia y unificada para sincronizar con tu KERNEL JS 3.2.0
    modo = str(payload.get("modo", "SALIR")).upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
    mente = str(payload.get("mente", "agotado")).lower()
    budget = str(payload.get("budget", "0"))
    perfil = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    
    # MODO CASA: El KERNEL recibirá el catálogo completo y aplicará el filtro local anti-repetición
    if modo == "CASA":
        return JSONResponse({"modo": "CASA", "misiones": BASE_MISIONES["CASA"]})
    
    # MODO SALIR: El despertador calcula la ruta exacta en cualquiera de los 50 estados de USA
    else:
        info = random.choice(BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"]))
        
        # FILTRO DE SUPERVIVENCIA FINANCIERA: Si el cliente escribe sobre deudas o biles, el mapa cambia a ayuda real
        palabras_urgentes = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion"]
        if any(p in desahogo for p in palabras_urgentes):
            gps_query = "agencias+de+empleo+staffings+corporations"
            que_hacer_base = "QUÉ: Buscar oficinas de contratación rápida. CÓMO: Entra con tu identificación en la mano. CUÁNDO: Por la mañana temprano. PARA QUÉ: Conseguir ingresos y ganarle al agobio del dinero."
            donde_base = "Agencias de trabajo y empleo inmediato en tu zona."
        else:
            # Filtro elástico por presupuesto (Austeridad creativa vs Gustazos)
            if budget == "0":
                gps_query = "free+public+parks+and+beaches"
            elif budget == "1":
                gps_query = "low+cost+coffee+shops+and+local+markets"
            else:
                gps_query = info["gps"]
            
            que_hacer_base = info["que_hacer"]
            donde_base = info["donde"]

        # Adaptabilidad del Perfil Biopsicosocial sin exclusión social
        msg_adicional = ""
        if perfil == "accesible":
            msg_adicional = " (Camino plano, muy fácil de caminar para personas mayores o con movilidad limitada)."
            gps_query = "wheelchair+accessible+" + gps_query
        elif perfil == "familia":
            msg_adicional = " (Lugar seguro y divertido para ir con los niños)."
            gps_query = "family+friendly+" + gps_query

        # FÓRMULA GEOGRÁFICA UNIVERSAL: Usa el ZIP si el usuario lo pone, sino usa la combinación Región + Estado
        anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"
        link_maps = f"https://google.com{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        
        return JSONResponse({
            "modo": "SALIR",
            "titulo": info["titulo"].upper(),
            "porque": info["porque"],
            "que_hacer": que_hacer_base + msg_adicional,
            "donde": donde_base,
            "gps": link_maps
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

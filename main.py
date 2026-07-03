from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base de datos de alta disponibilidad
BASE_MISIONES = {
    "CASA": [
        {"titulo": "Fase 1: Reconocimiento", "descripcion": "Identifica tu tensión actual sin juzgarla."},
        {"titulo": "Fase 2: Anclaje", "descripcion": "Inhala en 4 tiempos, mantén en 2, exhala en 6."},
        {"titulo": "Fase 3: Reset", "descripcion": "Suelta el control. Deja que el sistema te guíe el resto del tiempo."},
        {"titulo": "Fase 1: Escaneo", "descripcion": "Localiza el punto exacto donde sientes más tensión."},
        {"titulo": "Fase 2: Liberación", "descripcion": "Contrae ese músculo con fuerza 5 segundos y suéltalo."},
        {"titulo": "Fase 3: Presencia", "descripcion": "Observa un solo objeto. Nota sus detalles y texturas."},
        {"titulo": "Fase 1: Inventario", "descripcion": "Escribe en un papel 3 cosas que hoy te pesan."},
        {"titulo": "Fase 2: Acción", "descripcion": "Arruga ese papel con fuerza y descártalo."},
        {"titulo": "Fase 3: Inicio", "descripcion": "Bebe un vaso de agua sintiendo el recorrido."},
        {"titulo": "Fase 1: Pausa", "descripcion": "Detente totalmente. No hagas nada por 60 segundos."},
        {"titulo": "Fase 2: Sonido", "descripcion": "Escucha 3 sonidos, del más lejano al más cercano."},
        {"titulo": "Fase 3: Orden", "descripcion": "Alinea 3 objetos en tu espacio físico perfectamente."},
        {"titulo": "Fase 1: Conexión", "descripcion": "Apoya las plantas de tus pies firmemente."},
        {"titulo": "Fase 2: Expansión", "descripcion": "Estira tus brazos hacia arriba sin forzar."},
        {"titulo": "Fase 3: Foco", "descripcion": "Elige una tarea mínima que ignoraste y termínala."},
        {"titulo": "Fase 1: Postura", "descripcion": "Endereza tu columna. Imagina un hilo tirando de tu coronilla."},
        {"titulo": "Fase 2: Contacto", "descripcion": "Toca una superficie fría (mesa o pared) y siente su temperatura."},
        {"titulo": "Fase 3: Ventilación", "descripcion": "Abre una ventana. Deja que el aire nuevo renueve el ambiente."},
        {"titulo": "Fase 1: Desbloqueo", "descripcion": "Gira tus muñecas y tobillos 10 veces en cada dirección."},
        {"titulo": "Fase 2: Desapego", "descripcion": "Deja el teléfono boca abajo por 3 minutos. Solo observa."},
        {"titulo": "Fase 3: Cierre", "descripcion": "Cierra los ojos y agradece una sola cosa que lograste hoy."}
    ],
    "SALIR": {
        "agotado": [
            {"titulo": "Refugio Natural", "porque": "Tu sistema necesita reducir la sobreestimulación.", "que_hacer": "Camina sin rumbo en zona verde.", "donde": "Parque cercano.", "gps": "nature+parks+near+"},
            {"titulo": "Mirador de Horizonte", "porque": "Necesitas relajar tu vista y perspectiva.", "que_hacer": "Mira hacia la línea del horizonte.", "donde": "Punto alto o muelle.", "gps": "viewpoint+near+"},
            {"titulo": "Sombra Profunda", "porque": "El exceso de luz agota tu mente.", "que_hacer": "Siéntate bajo el árbol más grande.", "donde": "Área boscosa pública.", "gps": "public+parks+shade"},
            {"titulo": "Fluidez de Agua", "porque": "El agua en movimiento calma el sistema nervioso.", "que_hacer": "Observa el flujo del agua.", "donde": "Lago o canal cercano.", "gps": "water+front+park"},
            {"titulo": "Silencio Absoluto", "porque": "Necesitas aislarte del ruido urbano.", "que_hacer": "Busca un rincón sin gente.", "donde": "Zona de reserva natural.", "gps": "nature+reserve"},
            {"titulo": "Brisa Marina", "porque": "El aire salino y el sonido del mar resetean la fatiga mental.", "que_hacer": "Camina por la orilla y siente la brisa en tu cara.", "donde": "Playa pública o malecón.", "gps": "beach+near+"},
            {"titulo": "Jardín Zen", "porque": "La geometría de la naturaleza organizada calma el caos interior.", "que_hacer": "Camina lentamente observando los detalles de las plantas.", "donde": "Jardín botánico o parque japonés.", "gps": "botanical+garden+near+"},
            {"titulo": "Refugio bajo las nubes", "porque": "Observar el cielo cambia la perspectiva del tamaño de tus problemas.", "que_hacer": "Acuéstate sobre el césped y mira hacia arriba 10 minutos.", "donde": "Campo abierto o pradera.", "gps": "open+field+park"},
            {"titulo": "Bosque de Sombras", "porque": "La luz filtrada por árboles regula la temperatura corporal y mental.", "que_hacer": "Camina bajo la sombra densa.", "donde": "Sendero arbolado.", "gps": "shaded+walking+trail"},
            {"titulo": "Observatorio de Aves", "porque": "Enfocarse en movimiento lento externo calma el pulso.", "que_hacer": "Siéntate y observa aves sin moverte.", "donde": "Refugio de vida silvestre.", "gps": "wildlife+refuge+near+"},
            {"titulo": "Zona de Viento", "porque": "El movimiento del aire dispersa la carga estática mental.", "que_hacer": "Busca un espacio abierto con brisa.", "donde": "Campo o colina abierta.", "gps": "windy+open+space"},
            {"titulo": "Paso de Piedra", "porque": "Sentir texturas naturales aterriza el sistema nervioso.", "que_hacer": "Camina sobre un sendero de grava o piedra.", "donde": "Parque con senderos de piedra.", "gps": "stone+path+park"},
            {"titulo": "Refugio de Tarde", "porque": "La luz del atardecer avisa a tu cerebro el final del ciclo de alerta.", "que_hacer": "Observa la transición de luz al atardecer.", "donde": "Punto de puesta de sol.", "gps": "sunset+viewpoint"}
        ],
        "estresado": [
            {"titulo": "Zona de Descarga", "porque": "Necesitas metabolizar el cortisol.", "que_hacer": "Caminata a ritmo acelerado.", "donde": "Pista pública.", "gps": "recreation+centers+near+"},
            {"titulo": "Ritmo Firme", "porque": "La actividad rítmica reduce la ansiedad.", "que_hacer": "Camina 10 minutos sin parar.", "donde": "Pista de atletismo.", "gps": "running+track+near+"},
            {"titulo": "Extensión Física", "porque": "Necesitas liberar tensión muscular.", "que_hacer": "Ocupa tu espacio estirando brazos.", "donde": "Parque abierto.", "gps": "open+field+park"},
            {"titulo": "Resistencia de Pendiente", "porque": "El esfuerzo físico cambia tu química.", "que_hacer": "Sube escaleras o cuestas.", "donde": "Área deportiva elevada.", "gps": "stairs+public+workout"},
            {"titulo": "Descarga de Tensión", "porque": "Tus músculos necesitan alivio.", "que_hacer": "Estira contra una superficie estable.", "donde": "Instalación recreativa.", "gps": "outdoor+gym+near+"},
            {"titulo": "Senderismo de Foco", "porque": "El terreno irregular obliga a tu mente a estar presente.", "que_hacer": "Camina por un sendero con piedras o raíces.", "donde": "Sendero natural o forestal.", "gps": "hiking+trails+near+"},
            {"titulo": "Carga de Peso Propio", "porque": "La tensión requiere una liberación de fuerza física.", "que_hacer": "Haz ejercicios de calistenia usando barras.", "donde": "Parque con zona de barras.", "gps": "outdoor+gym+near+"},
            {"titulo": "Circuito de Movilidad", "porque": "Desbloquea las articulaciones donde se guarda el estrés.", "que_hacer": "Camina activando el movimiento de tus hombros.", "donde": "Parque lineal o camino peatonal.", "gps": "linear+park+near+"},
            {"titulo": "Escalera de Desahogo", "porque": "El esfuerzo vertical corta el bucle de pensamientos repetitivos.", "que_hacer": "Sube y baja una escalinata de parque.", "donde": "Escaleras públicas.", "gps": "staircase+workout"},
            {"titulo": "Carrera de Aislamiento", "porque": "El aislamiento físico permite el desahogo sin testigos.", "que_hacer": "Corre en un tramo solitario.", "donde": "Zona deportiva de bajo tráfico.", "gps": "running+path+quiet"},
            {"titulo": "Circuito de Estiramiento", "porque": "Mantener posiciones de estiramiento alarga la fibra muscular.", "que_hacer": "Sigue una rutina de estiramiento en el césped.", "donde": "Césped de parque abierto.", "gps": "public+park+green+space"},
            {"titulo": "Boxeo de Sombra", "porque": "El movimiento explosivo y corto libera ira contenida.", "que_hacer": "Ejecuta movimientos de boxeo al aire.", "donde": "Área deportiva abierta.", "gps": "open+recreation+area"},
            {"titulo": "Caminata de Peso", "porque": "Caminar con una mochila ligera ayuda a centrar tu gravedad.", "que_hacer": "Camina con paso constante y pesado.", "donde": "Sendero pavimentado.", "gps": "paved+walking+path"}
        ],
        "aburrido": [
            {"titulo": "Distrito de Estímulo", "porque": "La monotonía bloquea tu dopamina.", "que_hacer": "Visita zona de arte y gente.", "donde": "Centro histórico.", "gps": "arts+and+entertainment+near+"},
            {"titulo": "Exploración de Color", "porque": "Necesitas impacto visual nuevo.", "que_hacer": "Busca murales y arte urbano.", "donde": "Distrito de diseño o murales.", "gps": "street+art+near+"},
            {"titulo": "Cine Urbano", "porque": "Necesitas observar movimiento ajeno.", "que_hacer": "Observa el flujo público.", "donde": "Plaza principal.", "gps": "public+square+near+"},
            {"titulo": "Cambio de Escena", "porque": "El entorno conocido es un ancla.", "que_hacer": "Entra en una tienda extraña.", "donde": "Centro comercial local.", "gps": "shopping+center+near+"},
            {"titulo": "Análisis Arquitectónico", "porque": "Cambiar el foco visual despierta curiosidad.", "que_hacer": "Mira la forma de edificios.", "donde": "Distrito histórico.", "gps": "historical+buildings+near+"},
            {"titulo": "Mercado de Sabores", "porque": "La novedad sensorial despierta el interés por el entorno.", "que_hacer": "Huele los productos y observa los colores de los puestos.", "donde": "Mercado local o feria.", "gps": "farmers+market+near+"},
            {"titulo": "Ruta de Librería", "porque": "Las historias ajenas expanden tu mundo interno.", "que_hacer": "Entra, toca los libros y elige uno al azar.", "donde": "Librería de usados o pública.", "gps": "bookstore+near+"},
            {"titulo": "Exploración de Contrastes", "porque": "El cambio de zona urbana activa tu atención plena.", "que_hacer": "Cruza de un barrio residencial a uno comercial.", "donde": "Zona de transición urbana.", "gps": "city+center+near+"},
            {"titulo": "Galería de Ventanales", "porque": "Observar reflejos y espacios altera tu percepción.", "que_hacer": "Camina frente a edificios con grandes vidrieras.", "donde": "Distrito financiero.", "gps": "financial+district+architecture"},
            {"titulo": "Paseo de Fuentes", "porque": "El sonido y movimiento de fuentes rompe la quietud aburrida.", "que_hacer": "Camina junto a fuentes públicas.", "donde": "Plaza con fuentes.", "gps": "public+fountain+plaza"},
            {"titulo": "Ruta de Cafés", "porque": "El aroma a café y el movimiento humano activan sentidos.", "que_hacer": "Observa el menú en tres cafeterías distintas.", "donde": "Zona comercial.", "gps": "coffee+shops+near+"},
            {"titulo": "Museo de Calle", "porque": "La historia expuesta en placas cambia tu foco temporal.", "que_hacer": "Lee las placas conmemorativas del barrio.", "donde": "Zona histórica.", "gps": "historical+markers+near+"},
            {"titulo": "Búsqueda de Detalles", "porque": "Obligar a tu ojo a buscar detalles pequeños elimina el aburrimiento.", "que_hacer": "Busca una puerta de color específico.", "donde": "Calle residencial.", "gps": "residential+street+walking"}
        ]
    }
}

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    
    contexto = {
        "modo": payload.get("modo"),
        "zip": payload.get("zip", "33101"),
        "mente": payload.get("mente"),
        "budget": payload.get("budget"),
        "perfil": payload.get("perfil")
    }

    if contexto["modo"] == "CASA":
        return JSONResponse({"modo": "CASA", "misiones": BASE_MISIONES["CASA"]})
    
    else:
        info = random.choice(BASE_MISIONES["SALIR"].get(contexto["mente"], BASE_MISIONES["SALIR"]["aburrido"]))
        
        msg_adicional = ""
        if contexto["perfil"] == "accesible":
            msg_adicional = " (Ruta con prioridad de accesibilidad)."
        elif contexto["perfil"] == "familia":
            msg_adicional = " (Entorno apto para menores)."

        return JSONResponse({
            "modo": "SALIR",
            "titulo": info["titulo"],
            "porque": info["porque"],
            "que_hacer": info["que_hacer"] + msg_adicional,
            "donde": info["donde"],
            "gps": f"https://www.google.com/maps/search/?api=1&query={info['gps'].replace('+', ' ')}+in+zip+{contexto['zip']}"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

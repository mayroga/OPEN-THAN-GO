# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 5 (NÚCLEO Y RETOS DOMÉSTICOS CORREGIDOS)

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

# CATÁLOGO MAESTRO EXPANDIDO DE 48 ENTORNOS CON PUNTUACIÓN DE 19 NECESIDADES HUMANAS
BASE_MISIONES = {
    
    "CASA": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo."},
        {"id": 2, "titulo": "Desconexión de biles", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer."},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle."},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Deja caer la mochila de deudas. Siente tus hombros libres. Ya no está."},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando."},
        {"id": 6, "titulo": "Liberación de nudos", "descripcion": "Aprieta los puños 3 segundos. Abre de golpe. Suéltalo todo."},
        {"id": 7, "titulo": "El aire de la calle", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior."},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor."},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte."},
        {"id": 10, "titulo": "Orden de tu espacio", "descripcion": "Alinea tres objetos de tu mesa. Orden fuera es orden dentro."},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate."},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe."},
        {"id": 13, "titulo": "Foco en lo olvidado", "descripcion": "Elige una tarea mínima que ignorabas. Hazla ahora. Termínala."},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira."},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza."},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la puerta principal. Deja que el aire ruede. Huele el cambio."},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos."},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque."},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez."},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora."},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana."},
        {"id": 22, "titulo": "Relaja ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad."},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor."},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla."},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros."},
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa."},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado."},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto."},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la mouth, mueve mandíbula a los lados."},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto."},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos."},
        {"id": 32, "conciencia": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir."},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho."},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total."},
        {"id": 35, "cuenta": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido."},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela."},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta."},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces."},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear."},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente."},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel."},
        {"id": 42, "aire": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento."},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe."},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones."},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros."},
        {"id": 46, "siente": "Siente base", "descripcion": "Contacto firme de piernas con silla."},
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido."},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti."},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la estabilidad."},
        {"id": 50, "presencia": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control."}
    ],

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 2 DE 4 (CATÁLOGO TRIDIMENSIONAL RAMIFICADO DE CAMPO)

    "SALIR": {
        "agotado": [
            # 1 a 4. Matriz Tridimensional de Contracorriente y Calma
            {
                "titulo": "Sombra de árbol",
                "porque": "Tu mente merece expandirse y conectar con la vibración silenciosa de la naturaleza.",
                "que_hacer": "Busca un árbol grande en un parque abierto. Toca su madera y descansa bajo su sombra fresca.",
                "donde": "Un parque verde nacional o jardín del condado.",
                "gps": "public+parks+with+shade",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 100, "silencio": 80, "agua": 10, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 20, "comunidad": 20, "aprendizaje": 30, "juego": 30, "contemplacion": 95, "trabajo": 0, "descanso": 90, "organizacion": 10, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 95},
                # LAS 3 VARIACIONES ASIMÉTRICAS INTEGRADAS POR ENTORNO
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+parks+with+shade"
            },
            {
                "titulo": "Orilla de playa",
                "porque": "El oleaje infinito limpia el agobio y te sintoniza con la inmensidad del mundo exterior.",
                "que_hacer": "Camina descalzo sobre la arena mojada. Deja que las olas toquen tus pies y mira el horizonte lejano.",
                "donde": "Playa pública local o muelle costero.",
                "gps": "public+beaches",
                "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 60, "agua": 100, "sol": 95, "sombra": 10, "aire_fresco": 100, "creatividad": 40, "comunidad": 40, "aprendizaje": 10, "juego": 60, "contemplacion": 90, "trabajo": 0, "descanso": 80, "organizacion": 0, "alimentacion": 10, "musica": 20, "risa": 50, "esperanza": 100},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+beaches"
            },
            {
                "titulo": "Paseo del Mall",
                "porque": "A veces rodearte de luces, vitrinas llenas, gente moviéndose y música activa renueva tu energía urbana de inmediato.",
                "que_hacer": "Camina por los pasillos iluminados del mall. Entra a ver las novedades u objetos interesantes y disfruta del entorno.",
                "donde": "Centro comercial o Shopping Mall de tu zona.",
                "gps": "shopping+mall",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 70, "comunidad": 90, "aprendizaje": 20, "juego": 70, "contemplacion": 50, "trabajo": 0, "descanso": 50, "organizacion": 40, "alimentacion": 60, "musica": 60, "risa": 50, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "shopping+mall"
            },
            {
                "titulo": "Estímulo del Sabor",
                "porque": "Disfrutar de un buen platillo en un entorno vibrante despierta tus ganas de celebrar el éxito de la abundancia.",
                "que_hacer": "Pide una mesa cerca del movimiento. Ordena algo totalmente nuevo, escucha la música de fondo y disfruta de los sabores.",
                "donde": "Restaurante con terraza o música en vivo de tu condado.",
                "gps": "vibrant+restaurant+with+music",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 20, "agua": 0, "sol": 40, "sombra": 80, "aire_fresco": 70, "creatividad": 50, "comunidad": 95, "aprendizaje": 30, "juego": 50, "contemplacion": 60, "trabajo": 0, "descanso": 80, "organizacion": 20, "alimentacion": 100, "musica": 80, "risa": 70, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "restaurant+with+outdoor+seating"
            },
            # 5 a 8. Extensiones de Calma y Estímulo de Enfoque
            {
                "titulo": "Rincón del Enfoque",
                "porque": "El olor a café mezclado con miles de portadas de libros te da una sensación de posibilidades infinitas y buen camino.",
                "que_hacer": "Pide una bebida a tu gusto. Hojea una revista de viajes, arquitectura o negocios en una mesa cómoda.",
                "donde": "Cafetería dentro de una gran librería.",
                "gps": "bookstore+cafe",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 0, "silencio": 70, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 40, "creatividad": 75, "comunidad": 60, "aprendizaje": 90, "juego": 30, "contemplacion": 85, "trabajo": 0, "descanso": 90, "organizacion": 50, "alimentacion": 80, "musica": 40, "risa": 30, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "bookstore+cafe"
            },
            {
                "titulo": "Inercia de la Caza",
                "porque": "Buscar ofertas, ver marcas de diseñadores y tocar texturas de ropa nueva activa la ilusión de renovar tu prosperidad.",
                "que_hacer": "Recorre los pasillos de liquidaciones de ropa u objetos. Disfruta del ritmo rápido de la tienda.",
                "donde": "Gran tienda de saldos u outlet del condado.",
                "gps": "department+store+outlet",
                "vector_necesidades": {"movimiento": 55, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 60, "comunidad": 80, "aprendizaje": 20, "juego": 60, "contemplacion": 40, "trabajo": 0, "descanso": 40, "organizacion": 60, "alimentacion": 10, "musica": 50, "risa": 40, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "department+store+outlet"
            },
            {
                "titulo": "Línea de la Opulencia",
                "porque": "Ver la ingeniería de los grandes botes y yates amarrados te conecta inconscientemente con el flujo de la riqueza.",
                "que_hacer": "Camina por las pasarelas de madera de la marina. Escucha el tintineo del viento en los mástiles.",
                "donde": "Puerto deportivo o marina pública de alta categoría.",
                "gps": "luxury+marina+boat+dock",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 70, "silencio": 60, "agua": 100, "sol": 85, "sombra": 20, "aire_fresco": 100, "creatividad": 40, "comunidad": 60, "aprendizaje": 30, "juego": 50, "contemplacion": 90, "trabajo": 0, "descanso": 70, "organizacion": 40, "alimentacion": 30, "musica": 20, "risa": 40, "esperanza": 100},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "luxury+marina+boat+dock"
            },
            {
                "titulo": "Inyección de Estatus",
                "porque": "Los espacios monumentales, fuentes internas y mármoles te imbuyen de un sentimiento de éxito y buen camino inmediato.",
                "que_hacer": "Entra con paso firme y disfruta de la elegancia del lobby. Toma asiento y mira el flujo de personas sofisticadas.",
                "donde": "Lobby de un hotel de lujo.",
                "gps": "5+star+hotel+lobby",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 75, "agua": 20, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 60, "comunidad": 50, "aprendizaje": 20, "juego": 10, "contemplacion": 80, "trabajo": 0, "descanso": 90, "organizacion": 70, "alimentacion": 40, "musica": 30, "risa": 20, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "5+star+hotel+lobby"
            }
        ],
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 3 DE 4 (ACTIVOS TRIDIMENSIONALES: ESTRESADO Y ABURRIDO)

        "estresado": [
            # 9 a 12. Estímulos de Alta Inercia, Kinéticos y Motores
            {
                "titulo": "Caminata en subida",
                "porque": "Tu cuerpo acumuló un exceso de energía kinética que necesita ser liberado con fuerza.",
                "que_hacer": "Busca una rampa, gradería o escalera pública. Sube a paso firme usando la fuerza de tus piernas para quemar el estrés.",
                "donde": "Una escalera o gradería pública abierta.",
                "gps": "public+stairs",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "trabajo": 0, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 80},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+stairs"
            },
            {
                "titulo": "Inercia de Alta Gama",
                "porque": "Para mentes dinámicas, rodearte de caballos de fuerza y ver diseños de vanguardia enciende tu ambición y prosperidad.",
                "que_hacer": "Entra a la sala de exhibición de autos exóticos. Examina las líneas de los motores y absorbe la vibración del éxito material.",
                "donde": "Concesionario de vehículos exóticos o deportivos de tu zona.",
                "gps": "luxury+car+dealership",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 85, "comunidad": 50, "aprendizaje": 60, "juego": 70, "contemplacion": 75, "trabajo": 0, "descanso": 40, "organizacion": 80, "alimentacion": 0, "musica": 20, "risa": 40, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "luxury+car+dealership"
            },
            {
                "titulo": "Pista del Viento",
                "porque": "El espacio masivo, el asfalto plano y el vacío te dan una pista libre para respirar y estirar el cuerpo de forma expansiva.",
                "que_hacer": "Sube al último piso del parqueo. Camina de extremo a extremo sintiendo el viento y mirando la silueta urbana.",
                "donde": "El piso superior de un parqueo elevado público.",
                "gps": "open+roof+parking+lot",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 10, "silencio": 60, "agua": 0, "sol": 90, "sombra": 10, "aire_fresco": 90, "creatividad": 20, "comunidad": 10, "aprendizaje": 10, "juego": 30, "contemplacion": 70, "trabajo": 0, "descanso": 30, "organizacion": 20, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 75},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "open+parking+lot"
            },
            {
                "titulo": "Pausa Nutricia Elevada",
                "porque": "Disfrutar de un buen aroma rodeado de una atmósfera abierta bajo el sol disuelve de inmediato las quejas rutinarias.",
                "que_hacer": "Siéntate en la barra de la terraza exterior. Pide un aperitivo simple, disfruta la música lounge y mira los colores de la ciudad.",
                "donde": "Restaurante con rooftop o terraza abierta elevada de tu zona.",
                "gps": "restaurant+with+rooftop+or+outdoor+seating",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 70, "sombra": 70, "aire_fresco": 90, "creatividad": 45, "comunidad": 90, "aprendizaje": 30, "juego": 40, "contemplacion": 75, "trabajo": 0, "descanso": 80, "organizacion": 40, "alimentacion": 100, "musica": 60, "risa": 60, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "restaurant+with+outdoor+seating"
            }
        ],
        
        "aburrido": [
            # 13 a 16. Activos de Choque Dinámico, Colores y Catarsis Social
            {
                "titulo": "Laberinto de orden",
                "porque": "Explorar simulaciones de apartamentos y hogares ideales le da una estructura y balance lógico a tu mente en crisis.",
                "que_hacer": "Camina siguiendo la ruta marcada en el suelo. Observa la organización extrema de los espacios mínimos y los colores modernos.",
                "donde": "Establecimiento masivo de diseño, muebles o decoración.",
                "gps": "furniture+store+ikea",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 90, "comunidad": 65, "aprendizaje": 60, "juego": 50, "contemplacion": 75, "trabajo": 0, "descanso": 40, "organizacion": 100, "alimentacion": 30, "musica": 20, "risa": 40, "esperanza": 80},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "furniture+store+ikea"
            },
            {
                "titulo": "Pulso rítmico nocturno",
                "porque": "Romper el confinamiento estático de casa requiere a veces sumergirte de golpe en el movimiento y ritmo de la noche.",
                "que_hacer": "Entra a la zona de la barra exterior. Escucha las frecuencias graves del bajo, mira las luces cambiar y disfruta el ambiente.",
                "donde": "Lounge de música o club nocturno local de moda.",
                "gps": "music+lounge+bar",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 80, "contemplacion": 65, "trabajo": 0, "descanso": 50, "organizacion": 20, "alimentacion": 70, "musica": 100, "risa": 70, "esperanza": 80},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "music+lounge+bar"
            },
            {
                "titulo": "Catarsis Coreográfica",
                "porque": "La música alta y el baile forzan a tus pensamientos rápidos a apagarse de inmediato, liberando alma y cuerpo.",
                "que_hacer": "Quédate cerca de la pista peatonal observando el balanceo coordinado de las parejas. Disfruta de la risa y soltura del lugar.",
                "donde": "Discoteca urbana o salón de baile activo.",
                "gps": "dance+club+or+latin+lounge",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 0, "silencio": 0, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 70, "comunidad": 95, "aprendizaje": 20, "juego": 95, "contemplacion": 40, "trabajo": 0, "descanso": 10, "organizacion": 10, "alimentacion": 60, "musica": 100, "risa": 80, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "dance+club"
            },
            {
                "titulo": "Escala de Suministro Industrial",
                "porque": "Ver montañas interminables de productos apilados y el movimiento masivo de personas distrae tu rutina al 100%.",
                "que_hacer": "Recorre los pasillos centrales de extremo a extremo. Observa el volumen gigante de la cadena de distribución americana.",
                "donde": "Almacén mayorista o distribuidora industrial de tu zona.",
                "gps": "wholesale+store+costco+or+sams",
                "vector_necesidades": {"movimiento": 55, "naturaleza": 0, "silencio": 15, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 45, "creatividad": 20, "comunidad": 85, "aprendizaje": 40, "juego": 35, "contemplacion": 50, "trabajo": 0, "descanso": 30, "organizacion": 95, "alimentacion": 90, "musica": 10, "risa": 30, "esperanza": 75},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "wholesale+store+costco"
            }
        ]
    }
}

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# File: main.py - SECCIÓN FINAL (ENDPOINTS Y PROCESAMIENTO INTEGRADO)

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
    lang = str(payload.get("lang", "es")).lower()
    
    perfil_local = payload.get("perfil_local", {})

    # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA ORIGINAL INTACTO)
    if opcion_usuario == "CASA":
        misiones = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        random.shuffle(misiones)
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})

    # 2. ACCIÓN DE CAMPO (MODO SALIR CON MOTOR DE SELECCIÓN ANTI-REPETICIÓN)
    opciones_salir = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
    random.shuffle(opciones_salir)
    
    if len(opciones_salir) >= 2:
        mejor_score = -1
        info = opciones_salir[0]
        
        for opc in opciones_salir:
            vector_lugar = opc.get("vector_necesidades", {})
            score_coincidencia = 0
            for necesidad, peso_usuario in perfil_local.items():
                if isinstance(peso_usuario, (int, float)):
                    ruido_variancia = random.uniform(0.85, 1.15)
                    peso_base_lugar = vector_lugar.get(necesidad, 50)
                    score_coincidencia += (peso_base_lugar * ruido_variancia) * peso_usuario
                
            if score_coincidencia > mejor_score:
                mejor_score = score_coincidencia
                info = opc
    else:
        info = random.choice(opciones_salir)

    # =========================================================================
    # 📌 ¡AQUÍ VA EL CÓDIGO NUEVO! (SANEADO, INTERNO E INVISIBLE AL USUARIO)
    # =========================================================================
    budget_str = str(budget).strip()
    
    if budget_str == "0":
        precio_real = "Austeridad creativa para proteger tu mente hoy."
        gps_query_default = "public+parks+with+shade+or+public+beaches+or+historical+monument+plaza"
    elif budget_str == "1":
        precio_real = "Un gustazo mínimo para romper la rutina."
        gps_query_default = "bookstore+cafe+or+department+store+outlet+or+wholesale+store+costco+or+cheap+motel"
    elif budget_str == "2":
        precio_real = "El entorno es tu herramienta de escape hoy."
        gps_query_default = "shopping+mall+or+go+kart+racing+or+restaurant+with+rooftop+or+amusement+park"
    else:
        precio_real = "Flujo de abundancia activa. Date un lujo merecido hoy."
        gps_query_default = "luxury+marina+boat+dock+or+5+star+hotel+lobby+or+luxury+car+dealership+or+musical+instruments+store"

    perfil_str = str(perfil).strip().lower()
    quienes_van = "Vas solo contigo mismo a recuperar tu centro."
    tratamiento_especial = ""

    if "adulto" in perfil_str or "mayor" in perfil_str or "senior" in perfil_str or perfil_str == "accessible":
        quienes_van = "Ruta plana con acceso total por comodidad física y cuidado de tu edad."
        tratamiento_especial = "Desplázate a ritmo lento. Este entorno cuenta con áreas sombreadas y descansos confortables para proteger tu cuerpo hoy."
    elif "veterano" in perfil_str or "veteran" in perfil_str:
        quienes_van = "Entorno honorable seleccionado para tu descanso interior."
        tratamiento_especial = "Este espacio está seleccionado por su estabilidad y respeto. Un territorio seguro para recuperar la calma que tu mente merece."
    elif "gobierno" in perfil_str or "admin" in perfil_str or "corporativo" in perfil_str or "trabajador" in perfil_str:
        quienes_van = "Desconexión radical del tiempo institucional."
        tratamiento_especial = "Estás fuera del horario del sistema. Queda estrictamente bienvenido el descanso; tu mente está libre de reportes y pantallas durante los próximos 60 minutos."
    elif "familia" in perfil_str or "hijos" in perfil_str or "family" in perfil_str:
        quienes_van = "Entorno apto para el desahogo de tus niños y seres queridos."

    palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "gastar", "compras"]

    if any(p in desahogo for p in palabras_criticas) or opcion_usuario == "MANDO_LIBRE":
        canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])

        if canal_multimedia == "SPOTIFY":
            titulo_ganador = "RESET AUDITIVO" if lang == "es" else "AUDIO RESET"
            donde_base = "Zona Libre de Consumo y Frecuencias Altas" if lang == "es" else "Store-Free High Frequency Zone"
            guia_masticada = "DESTINO: Conexión Acústica.\nQUÉ HACER: Escucha los sonidos naturales en silencio absoluto.\nPARA QUÉ: Detener la prisa de la mente, enfriar el impulso de la rutina y sintonizar con tu prosperidad interior." if lang == "es" else "TARGET: Audio Connection.\nWHAT TO DO: Listen to nature sounds in complete silence.\nWHY: Stop the rush of the mind, cool down routine impulses, and tune into inner prosperity."
            link_base = info.get("variante_spotify", "https://spotify.com")
            gps_query = ""
        elif canal_multimedia == "YOUTUBE":
            titulo_ganador = "REINICIO VISUAL" if lang == "es" else "VISUAL SHOCK"
            donde_base = "Frecuencia de Abundancia y Alivio" if lang == "es" else "Abundance & Relief Frequency"
            guia_masticada = "DESTINO: Sesión de Enfoque.\nQUÉ HACER: Pon el video en pantalla completa con audífonos.\nPARA QUÉ: Desacelerar los pensamientos rápidos y reprogramar tu cerebro hacia caminos de prosperidad y balance." if lang == "es" else "TARGET: Focus Session.\nWHAT TO DO: Play the video in full screen with headphones.\nWHY: Slow down racing thoughts and reprogram your brain towards paths of prosperity and balance."
            link_base = info.get("variante_youtube", "https://youtube.com")
            gps_query = ""
        else:
            link_base = "https://google.com"
            gps_query = gps_query_default
            
            if budget_str == "0":
                titulo_ganador = "EXPLORACIÓN DE AUSENCIA" if lang == "es" else "EXPLORATION OF ABSENCE"
                donde_base = "Espacio Peatonal Abierto, Playa Pública o Parque Verde Nacional" if lang == "es" else "Public Open Space, Beach or National Park"
                guia_masticada = f"DESTINO: Un entorno natural o plaza al aire libre.\nQUÉ HACER: Camina despacio registrando el viento, el cielo y el flujo del entorno.\nPARA QUÉ: Romper la hipnosis del encierro, relajar el cuerpo y conectar con la libertad del espacio abierto.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}" if lang == "es" else f"TARGET: Free Nature Trail, Public Plaza or Open Beach.\nWHAT TO DO: Walk slowly registering the wind, the sky, and the natural flow.\nWHY: Break the indoor hypnosis, relax your body, and connect with open freedom.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}"
                
            elif budget_str == "1":
                titulo_ganador = "INERCIA DE ABASTECIMIENTO" if lang == "es" else "SMART URBAN INERTIA"
                donde_base = "Grandes Almacenes de Suministros, Cafeterías de Libros o Tiendas de Saldo Cotidiano" if lang == "es" else "Department Outlets, Bookstores or Distribution Centers"
                guia_masticada = f"DESTINO: Un centro de distribución o rincón de diseño urbano.\nQU¿É HACER: Recorre los pasillos masivos, hojea portadas o busca novedades cotidianas con soltura.\nPARA QUÉ: Activar la mente a través de la exploración de objetos, oler el dinamismo del día y sacudirte la monotonía.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}" if lang == "es" else f"TARGET: Smart Department Outlets or Used Bookstores.\nWHAT TO DO: Walk through massive aisles, browse book covers, or look for daily items with ease.\nWHY: Activate your mind through object exploration, feel the day's energy, and shake off monotony.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}"
                
            elif budget_str == "2":
                titulo_ganador = "ESTÍMULO Y REGENERACIÓN URBANA" if lang == "es" else "URBAN REGENERATION STIMULUS"
                donde_base = "Grandes Centros Comerciales, Terrazas Elevadas, Cines o Centros de Recreación" if lang == "es" else "Vibrant Shopping Malls, Rooftops, Movie Theaters or Recreation Loops"
                guia_masticada = f"DESTINO: Un entorno comercial o recreativo activo.\nQUÉ HACER: Entra a los pasillos confortables, sube a una terraza a pie o sigue la inercia circular de la pista.\nPARA QUÉ: Rodearte de estímulos visuales, flujos sociales grandes y recuperar la soltura de tu día libre.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}" if lang == "es" else f"TARGET: Vibrant Shopping Mall, Rooftop or Recreation Center.\nWHAT TO DO: Walk through comfortable aisles, visit an open terrace, or track the track's circular loop.\nWHY: Surround yourself with visual stimulus, massive social flows, and regain the ease of your day.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}"
            gps_query = info.get("variante_maps", "shopping+mall+or+go+kart+racing+or+restaurant+with+rooftop")
        else:
            titulo_ganador = "NÚCLEO DE LA PROSPERIDAD" if lang == "es" else "CORE OF PROSPERITY"
            donde_base = "Muelles y Marinas de Yates, Vestíbulos Elegantes o Salas de Exhibición Premium" if lang == "es" else "Yacht Marinas, Premium Lobbies or Showrooms"
            guia_masticada = f"DESTINO: Un entorno de alta infraestructura y diseño urbano.\nQUÉ HACER: Camina por las pasarelas de madera entre mástiles, siéntate en los sofás amplios o admira la ingeniería de vanguardia.\nPARA QUÉ: Elevar tu sintonía subiendo el nivel de tu entorno visual, rompiendo la parálisis mental y fluyendo con el éxito material.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}" if lang == "es" else f"TARGET: High-End Yacht Marina, Premium Hotel Lobby, or Showroom.\nWHAT TO DO: Walk the wooden docks, take a seat on wide sofas, or inspect cutting-edge engineering.\nWHY: Elevate your vibration by upgrading your visual environment level, breaking mental freeze, and flowing with material success.\n\nACOMPAÑAMIENTO: {quienes_van}\nGASTO: {precio_real}"
            gps_query = "luxury+marina+boat+dock+or+5+star+hotel+lobby+or+luxury+car+dealership+or+musical+instruments+store"
    # =========================================================================
    # 📌 CONTINÚA TU CÓDIGO VIEJO DE TRADUCCIONES AUTOMÁTICAS Y ARRANQUE UVICORN
    # =========================================================================
    
    else:
        link_base = "https://google.com"
        gps_query = info["gps"]
        donde_base = info["donde"]

        if lang == "en":
            traducciones_guia = {
                "Sombra de árbol": "TARGET: Tree Shade.\nWHAT TO DO: Touch the bark. Stay under its fresh shade.\nWHY: Your eyes need a rest from screen lights.",
                "Orilla de playa": "TARGET: Beach Shore.\nWHAT TO DO: Walk barefoot on wet sand. Let waves touch your feet.\nWHY: Ocean waves clear background noise from your mind.",
                "Paseo del Mall": "TARGET: Shopping Mall Walk.\nWHAT TO DO: Walk through the corridors. Explore what is new and enjoy the lively atmosphere.\nWHY: Surrounding yourself with lights and social dynamic boosts your urban energy.",
                "Estímulo del Sabor": "TARGET: Flavor Stimulus.\nWHAT TO DO: Order something new, listen to background music and enjoy.\nWHY: Great food in a vibrant environment sparks life's abundance."
            }
            guia_masticada = traducciones_guia.get(info["titulo"], f"TARGET: {info['donde']}.\nWHAT TO DO: {info['que_hacer']}\nWHY: {info['porque']}\n{quienes_van}\n{precio_real}")
            titulo_ganador = info["titulo"].upper()
        else:
            guia_masticada = f"DESTINO: {info['titulo']}.\nPOR QUÉ: {info['porque']}\nQUÉ HACER: {info['que_hacer']}\nCUÁNDO: Ahora mismo. Levántate de la silla ya.\nPARA QUÉ: Romper el zombi urbano y recordar el valor de tu tranquilidad.\n{quienes_van}\n{precio_real}"
            titulo_ganador = info["titulo"].upper()

    if perfil == "accesible":
        gps_query = "wheelchair+accessible+" + gps_query
    elif perfil == "family":
        gps_query = "family+friendly+" + gps_query

    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"

    if gps_query:
        if link_base.startswith("http"):
            link_google_maps_vivo = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        else:
            link_google_maps_vivo = link_base.replace(" ", "+")
    else:
        link_google_maps_vivo = link_base.replace(" ", "+")

    if tratamiento_especial:
        guia_masticada += f"\n\n{tratamiento_especial}"

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_titulo": titulo_ganador,
        "destino_entorno": donde_base,
        "destino_instruccion": guia_masticada.strip(),
        "destino_coordenadas_gps": link_google_maps_vivo,
        "token_entorno": info["titulo"] if "titulo" in info else "general"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 6 (NÚCLEO Y RETOS DOMÉSTICOS)

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

# CATÁLOGO MAESTRO MULTIDIMENSIONAL DE LIBERACIÓN BIOPSICOSOCIAL
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
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu weight total."},
        {"id": 35, "cuenta": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido."},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela."},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta."},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces."},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear."},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente."},
        {"id": 41, "contacto": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel."},
        {"id": 42, "aire": "Aire profundo", "descripcion": "Infla viento, retén 3 segundos, suelta lento."},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe."},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones."},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros."},
        {"id": 46, "siente": "Siente base", "descripcion": "Contacto firme de piernas con silla."},
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido."},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti."},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la estabilidad."},
        {"id": 50, "presencia": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control."}
    ],
    "SALIR": {
        "agotado": [
            # 1. Parques Públicos (Naturaleza/Sombra)
            {
                "titulo": "Sombra de árbol",
                "porque": "Tu mente merece expandirse y conectar con la vibración silenciosa de la naturaleza.",
                "que_hacer": "Busca un árbol grande en un parque abierto. Toca su madera y descansa bajo su sombra fresca.",
                "donde": "Un parque verde nacional o jardín del condado.",
                "gps": "public+parks+with+shade",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 100, "silencio": 80, "agua": 10, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 20, "comunidad": 20, "aprendizaje": 30, "juego": 30, "contemplacion": 95, "trabajo": 0, "descanso": 90, "organizacion": 10, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+parks+with+shade"
            },
            # 2. Playas de Costo Cero
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
            # 3. Muelles y Malecones
            {
                "titulo": "Paseo del muelle",
                "porque": "Mirar el océano lejano le devuelve la claridad, la grandeza y la perspectiva a tus planes.",
                "que_hacer": "Camina hasta el extremo del muelle. Siente la brisa marina y quédate contemplando el mar un minuto.",
                "donde": "Muelle o malecón público.",
                "gps": "public+fishing+pier",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 90, "silencio": 50, "agua": 100, "sol": 80, "sombra": 20, "aire_fresco": 100, "creatividad": 30, "comunidad": 50, "aprendizaje": 20, "juego": 40, "contemplacion": 95, "trabajo": 0, "descanso": 70, "organizacion": 10, "alimentacion": 20, "musica": 10, "risa": 40, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+fishing+pier"
            },
            # 4. Grandes Centros Comerciales (Atracción y Consumo Abundante)
            {
                "titulo": "Paseo del Mall",
                "porque": "A veces rodearte de luces, vitrinas llenas, gente moviéndose y música activa renueva tu energía urbana de inmediato.",
                "que_hacer": "Camina por los pasillos iluminados del mall. Entra a ver las novedades u objetos interesantes y disfruta de la variedad del entorno.",
                "donde": "Centro comercial o Shopping Mall de tu zona.",
                "gps": "shopping+mall",
                "vector_necesidades": {"movimiento": 60, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 70, "comunidad": 90, "aprendizaje": 20, "juego": 70, "contemplacion": 50, "trabajo": 0, "descanso": 50, "organizacion": 40, "alimentacion": 60, "musica": 60, "risa": 50, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "shopping+mall"
            },
            # 5. Senderos de Bosque Sombreados
            {
                "titulo": "Senda forestal",
                "porque": "El oxígeno puro de los árboles limpia la pesadez del pecho y resetea tus ideas.",
                "que_hacer": "Sigue los senderos marcados. Escucha el susurro de las ramas y respira hondo la frescura del bosque.",
                "donde": "Sendero natural boscoso.",
                "gps": "nature+trails+forest",
                "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 85, "agua": 20, "sol": 30, "sombra": 95, "aire_fresco": 100, "creatividad": 20, "comunidad": 10, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "trabajo": 0, "descanso": 60, "organizacion": 10, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "nature+trails+forest"
            },
            # 6. Restaurantes Temáticos con Música (Comida, Risa y Vida)
            {
                "titulo": "Estímulo del Sabor",
                "porque": "Disfrutar de un buen platillo en un entorno vibrante despierta tus ganas de celebrar el éxito de la abundancia.",
                "que_hacer": "Pide una mesa cerca del movement. Ordena algo nuevo, escucha la música de fondo y disfruta de los sabores.",
                "donde": "Restaurante con terraza o música en vivo de tu condado.",
                "gps": "vibrant+restaurant+with+music",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 20, "agua": 0, "sol": 40, "sombra": 80, "aire_fresco": 70, "creatividad": 50, "comunidad": 95, "aprendizaje": 30, "juego": 50, "contemplacion": 60, "trabajo": 0, "descanso": 80, "organizacion": 20, "alimentacion": 100, "musica": 80, "risa": 70, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "vibrant+restaurant+with+music"
            },
            # 7. Miradores Elevados de la Ciudad
            {
                "titulo": "Punto de altura",
                "porque": "Ver las luces y los rascacielos desde arriba te da perspectiva y expande tus metas de prosperidad.",
                "que_hacer": "Sube hasta la colina o mirador. Contempla la extensión de la arquitectura en silencio absoluto.",
                "donde": "Mirador o colina pública panorámica.",
                "gps": "scenic+overlook",
                "vector_necesidades": {"movimiento": 65, "naturaleza": 80, "silencio": 75, "agua": 20, "sol": 80, "sombra": 10, "aire_fresco": 95, "creatividad": 50, "comunidad": 40, "aprendizaje": 30, "juego": 20, "contemplacion": 100, "trabajo": 0, "descanso": 60, "organizacion": 0, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "scenic+overlook"
            },
            # 8. Tiendas de Entretenimiento y Videojuegos (Arcades / Best Buy)
            {
                "titulo": "Descarga Tecnológica",
                "porque": "Interactuar con pantallas gigantes, colores de neón y sonidos dinámicos saca a tu mente de cualquier parálisis.",
                "que_hacer": "Camina explorando las novedades tecnológicas o juega una partida rápida. Deja que los estímulos visuales te activen.",
                "donde": "Centro de entretenimiento, arcade o gran tienda tecnológica.",
                "gps": "amusement+arcade+or+electronics+store",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 15, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 80, "comunidad": 70, "aprendizaje": 60, "juego": 100, "contemplacion": 40, "trabajo": 10, "descanso": 40, "organizacion": 50, "alimentacion": 10, "musica": 60, "risa": 70, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "amusement+arcade"
            },
            # 9. Cafeterías de Libros Animadas (Barnes & Noble)
            {
                "titulo": "Rincón del Enfoque",
                "porque": "El olor a café mezclado con miles de portadas de libros te da una sensación de posibilidades infinitas y buen camino.",
                "que_hacer": "Pide una bebida a tu gusto. Hojea una revista de viajes, autos o negocios en una mesa cómoda.",
                "donde": "Cafetería dentro de una gran librería.",
                "gps": "bookstore+cafe",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 0, "silencio": 70, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 40, "creatividad": 75, "comunidad": 60, "aprendizaje": 90, "juego": 30, "contemplacion": 85, "trabajo": 20, "descanso": 90, "organizacion": 50, "alimentacion": 80, "musica": 40, "risa": 30, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "bookstore+cafe"
            },
            # 10. Viveros y Tiendas de Plantas Gigantes
            {
                "titulo": "Bocanada verde",
                "porque": "Ver la abundancia natural nacer y multiplicarse te alinea directamente con la prosperidad.",
                "que_hacer": "Camina entre flores, palmeras y brotes. Toca la frescura de las hojas y nota la riqueza del entorno.",
                "donde": "Invernadero o gran tienda de jardinería.",
                "gps": "plant+nursery",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 60, "sombra": 70, "aire_fresco": 80, "creatividad": 65, "comunidad": 40, "aprendizaje": 60, "juego": 30, "contemplacion": 85, "trabajo": 0, "descanso": 75, "organizacion": 40, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "plant+nursery"
            },
            # 11. Grandes Outlets o Centros de Descuento (Ross / Marshalls)
            {
                "titulo": "Inercia de la Caza",
                "porque": "Buscar ofertas, ver marcas de diseñadores y tocar texturas de ropa nueva activa la ilusión de renovar tu estatus de prosperidad.",
                "que_hacer": "Recorre los pasillos de liquidaciones de ropa u objetos. Disfruta del ritmo rápido de la tienda.",
                "donde": "Gran tienda de saldos u outlet del condado.",
                "gps": "department+store+outlet",
                "vector_necesidades": {"movimiento": 55, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 60, "comunidad": 80, "aprendizaje": 20, "juego": 60, "contemplacion": 40, "trabajo": 30, "descanso": 40, "organizacion": 60, "alimentacion": 10, "musica": 50, "risa": 40, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "department+store+outlet"
            },
            # 12. Distritos de Galerías de Arte Urbanas
            {
                "titulo": "Espejo Creativo",
                "porque": "Observar los diseños, colores y formas vanguardistas expande tu visión y enriquece tu mente libre.",
                "que_hacer": "Camina por la zona de galerías. Contempla las exposiciones y nota la riqueza del pensamiento artístico.",
                "donde": "Distrito de galerías o centro cultural urbano.",
                "gps": "art+galleries+district",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 85, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 100, "comunidad": 40, "aprendizaje": 85, "juego": 20, "contemplacion": 95, "trabajo": 10, "descanso": 60, "organizacion": 30, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "art+galleries+district"
            },
            # 13. Zonas de Yates y Marinas de Lujo
            {
                "titulo": "Línea de la Opulencia",
                "porque": "Ver la ingeniería de los grandes botes y yates amarrados te conecta inconscientemente con el flujo de la riqueza.",
                "que_hacer": "Camina por las pasarelas de madera de la marina. Escucha el tintineo del viento en los mástiles.",
                "donde": "Puerto deportivo o marina pública de alta categoría.",
                "gps": "luxury+marina+boat+dock",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 70, "silencio": 60, "agua": 100, "sol": 85, "sombra": 20, "aire_fresco": 100, "creatividad": 40, "comunidad": 60, "aprendizaje": 30, "juego": 50, "contemplacion": 90, "trabajo": 10, "descanso": 70, "organizacion": 40, "alimentacion": 30, "musica": 20, "risa": 40, "esperanza": 100},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "luxury+marina+boat+dock"
            },
            # 14. Vestíbulos de Hoteles de 5 Estrellas (Estilo Las Vegas / Miami)
            {
                "titulo": "Inyección de Estatus",
                "porque": "Los espacios monumentales, fuentes internas y mármoles te imbuyen de un sentimiento de éxito y buen camino inmediato.",
                "que_hacer": "Entra con paso firme y disfruta de la elegancia del lobby. Toma asiento y mira el flujo de personas sofisticadas.",
                "donde": "Lobby de un hotel de lujo.",
                "gps": "5+star+hotel+lobby",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 75, "agua": 20, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 60, "comunidad": 50, "aprendizaje": 20, "juego": 10, "contemplacion": 80, "trabajo": 20, "descanso": 90, "organizacion": 70, "alimentacion": 40, "musica": 30, "risa": 20, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "5+star+hotel+lobby"
            },
            # 15. Mercados Gastronómicos Abiertos (Food Halls / Time Out)
            {
                "titulo": "Pulso del Sabor Urbano",
                "porque": "Oler decenas de cocinas internacionales mezcladas con risas y charlas rompe cualquier aislamiento de forma dinámica.",
                "que_hacer": "Recorre las barras de comida. Disfruta de la variedad de platos visuales, colores y la vibración social del lugar.",
                "donde": "Food Hall gourmet o mercado gastronómico de moda.",
                "gps": "food+hall+market",
                "vector_necesidades": {"movimiento": 55, "naturaleza": 30, "silencio": 20, "agua": 0, "sol": 60, "sombra": 60, "aire_fresco": 80, "creatividad": 50, "comunidad": 95, "aprendizaje": 60, "juego": 40, "contemplacion": 60, "trabajo": 30, "descanso": 40, "organizacion": 30, "alimentacion": 100, "musica": 50, "risa": 60, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "food+hall+market"
            },
            # 16. Centros de Estética, Barberías o Spas Premium
            {
                "titulo": "Inversión en Ti",
                "porque": "Dedicarse tiempo a la apariencia física enciende tu autoestima y te recuerda la prosperidad de tu cuerpo.",
                "que_hacer": "Entra a revisar el menú de masajes, cortes o tratamientos. Disfruta de la atención impecable del personal.",
                "donde": "Spa urbano, salón o barbería de alta gama.",
                "gps": "luxury+spa+or+barbershop",
                "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 80, "agua": 40, "sol": 0, "sombra": 100, "aire_fresco": 60, "creatividad": 40, "comunidad": 60, "aprendizaje": 40, "juego": 10, "contemplacion": 80, "trabajo": 0, "descanso": 100, "organizacion": 60, "alimentacion": 20, "musica": 40, "risa": 30, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "luxury+spa+or+barbershop"
            }
        ],
        "estresado": [
            # 17. Graderías y Escaleras Públicas Grandes (Movimiento)
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
            # 18. Parqueos Elevados y Miradores de Cemento
            {
                "titulo": "Pista del Viento",
                "porque": "El espacio masivo, el asfalto plano y el vacío te dan una pista libre para respirar y estirar el cuerpo de forma expansiva.",
                "que_hacer": "Sube al último piso del parqueo. Camina de extremo a extremo sintiendo el viento y mirando la silueta urbana.",
                "donde": "El piso superior de un parqueo elevado público.",
                "gps": "open+roof+parking+lot",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 10, "silencio": 60, "agua": 0, "sol": 90, "sombra": 10, "aire_fresco": 90, "creatividad": 20, "comunidad": 10, "aprendizaje": 10, "juego": 30, "contemplacion": 70, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 75},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "open+parking+lot"
            },
            # 19. Concesionarios de Autos Exóticos y Lujo (Tesla / Porsche / Ferrari)
            {
                "titulo": "Inercia de Alta Gama",
                "porque": "Para mentes dinámicas, rodearte de caballos de fuerza y ver diseños de vanguardia enciende tu ambición y prosperidad.",
                "que_hacer": "Entra a la sala de exhibición de autos exóticos. Examina las líneas de los motores y absorbe la vibración del éxito material.",
                "donde": "Concesionario de vehículos exóticos o deportivos de tu zona.",
                "gps": "luxury+car+dealership",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 85, "comunidad": 50, "aprendizaje": 60, "juego": 70, "contemplacion": 75, "trabajo": 30, "descanso": 40, "organizacion": 80, "alimentacion": 0, "musica": 20, "risa": 40, "esperanza": 95},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "luxury+car+dealership"
            },
            # 20. Complejos y Estadios Deportivos Públicos (Canchas de Béisbol / Fútbol)
            {
                "titulo": "Pulso de la Competencia",
                "porque": "El olor a césped cortado, las luces de los estadios y ver la fuerza de un juego en vivo te saca de tus pensamientos fijos.",
                "que_hacer": "Busca un lugar en la banca lateral de la cancha. Sigue la pelota con tus ojos y contágiate de la energía del equipo.",
                "donde": "Estadio público, complejo deportivo o jaulas de bateo.",
                "gps": "public+sports+complex+or+batting+cages",
                "vector_necesidades": {"movimiento": 100, "naturaleza": 40, "silencio": 20, "agua": 0, "sol": 80, "sombra": 10, "aire_fresco": 90, "creatividad": 20, "comunidad": 85, "aprendizaje": 30, "juego": 95, "contemplacion": 50, "trabajo": 10, "descanso": 15, "organizacion": 30, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+sports+complex"
            },
            # 21. Puentes Peatonales Grandes e Interestatales
            {
                "titulo": "Cruce del Flujo Masivo",
                "porque": "Caminar sobre la velocidad de miles de autos te ayuda a entender que tus problemas se desplazan rápido.",
                "que_hacer": "Cruza la pasarela peatonal del puente. Mira los vehículos pasar a toda velocidad debajo de ti y siente la inercia.",
                "donde": "Puente peatonal elevado o pasarela sobre la autopista.",
                "gps": "pedestrian+overpass+bridge",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 20, "agua": 20, "sol": 80, "sombra": 10, "aire_fresco": 95, "creatividad": 30, "comunidad": 40, "aprendizaje": 10, "juego": 20, "contemplacion": 85, "trabajo": 0, "descanso": 40, "organizacion": 0, "alimentacion": 0, "musica": 10, "risa": 20, "esperanza": 80},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "pedestrian+overpass+bridge"
            },
            # 22. Pistas de Karts y Deportes de Motor (Go-Karts)
            {
                "titulo": "Adrenalina y Control",
                "porque": "El rugido de los motores, el olor a llanta quemada y la velocidad pura obligan a tu cerebro a apagar de golpe cualquier agobio.",
                "que_hacer": "Acércate a la barandilla de la pista de karts. Siente la vibración del suelo y observa las curvas cerradas y los adelantamientos.",
                "donde": "Pista de karts o centro de carreras indoor/outdoor.",
                "gps": "go+kart+racing",
                "vector_necesidades": {"movimiento": 90, "naturaleza": 0, "silencio": 0, "agua": 0, "sol": 60, "sombra": 40, "aire_fresco": 80, "creatividad": 40, "comunidad": 75, "aprendizaje": 30, "juego": 100, "contemplacion": 40, "trabajo": 0, "descanso": 10, "organizacion": 40, "alimentacion": 20, "musica": 50, "risa": 80, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "go+kart+racing"
            },
            # 23. Zonas de Skateparks y Parques de Acción Urbana
            {
                "titulo": "Impacto Dinámico Urbano",
                "porque": "La cultura callejera, la música hip-hop y el riesgo controlado de los trucos inyectan juventud y vitalidad a tu día.",
                "que_hacer": "Quédate cerca de las rampas observando las acrobacias en patineta o bicicleta. Absorbe la soltura y audacia del entorno.",
                "donde": "Skatepark público activo de tu zona.",
                "gps": "public+skatepark",
                "vector_necesidades": {"movimiento": 75, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 85, "sombra": 15, "aire_fresco": 85, "creatividad": 70, "comunidad": 80, "aprendizaje": 40, "juego": 95, "contemplacion": 50, "trabajo": 0, "descanso": 20, "organizacion": 10, "alimentacion": 0, "musica": 60, "risa": 60, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "public+skatepark"
            },
            # 24. Grandes Tiendas de Deportes y Outdoor (Bass Pro Shops / REI)
            {
                "titulo": "Santuario de la Expedición",
                "porque": "Explorar barcos en exhibición, acuarios gigantes y equipo de aventura activa tu deseo de explorar el mundo salvaje.",
                "que_hacer": "Camina por la sección de barcos o pesca de la megatienda. Toca las texturas, mira los diseños y planifica tu próximo escape.",
                "donde": "Megatienda de deportes de aventura u outdoor.",
                "gps": "bass+pro+shops+or+rei+store",
                "vector_necesidades": {"movimiento": 55, "naturaleza": 40, "silencio": 20, "agua": 30, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 80, "comunidad": 65, "aprendizaje": 60, "juego": 85, "contemplacion": 70, "trabajo": 10, "descanso": 50, "organizacion": 60, "alimentacion": 10, "musica": 20, "risa": 40, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "bass+pro+shops"
            },
            # 25. Grandes Terminales y Estaciones de Tránsito Activas
            {
                "titulo": "Inercia del Viajero",
                "porque": "El movimiento constante de maletas, autobuses y personas abordando le recuerda a tu mente que las fronteras se pueden cruzar.",
                "que_hacer": "Párate en la zona segura de la plataforma de autobuses o trenes. Siente la vibración del motor y mira los destinos impresos en las pantallas.",
                "donde": "Estación de tránsito o terminal central de autobuses.",
                "gps": "transit+station+or+bus+terminal",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 10, "silencio": 20, "agua": 0, "sol": 60, "sombra": 40, "aire_fresco": 75, "creatividad": 30, "comunidad": 70, "aprendizaje": 50, "juego": 30, "contemplacion": 80, "trabajo": 20, "descanso": 30, "organizacion": 85, "alimentacion": 10, "musica": 10, "risa": 20, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "transit+station"
            },
            # 41. Teatros de Cine Independientes o Clásicos (Arte Alternativo)
            {
                "titulo": "Ventana de la Ficción",
                "porque": "El cine independiente te sumerge en narrativas ingeniosas, alejándote del bombardeo comercial masivo.",
                "que_hacer": "Ingresa al vestíbulo clásico de la sala. Mira los afiches antiguos y absorbe el ambiente artístico.",
                "donde": "Teatro de cine independiente, alternativo o clásico local.",
                "gps": "independent+movie+theater",
                "vector_necesidades": {"movimiento": 15, "naturaleza": 0, "silencio": 70, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 95, "comunidad": 65, "aprendizaje": 80, "juego": 40, "contemplacion": 90, "trabajo": 10, "descanso": 85, "organizacion": 40, "alimentacion": 40, "musica": 30, "risa": 50, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "independent+movie+theater"
            },
            # 42. Clubes de Ajedrez Públicos o Mesas Recreativas de Parques
            {
                "titulo": "Contacto de Estrategia Humana",
                "porque": "Ver mentes concentradas calculando jugadas en silencio te obliga a desacelerar los pensamientos rápidos.",
                "que_hacer": "Párate cerca de una mesa de juego. Analiza en silencio el orden de las piezas de madera.",
                "donde": "Club de recreación, centro comunitario o parque de mesas públicos.",
                "gps": "community+center+or+chess+club",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 65, "agua": 0, "sol": 30, "sombra": 90, "aire_fresco": 60, "creatividad": 60, "comunidad": 100, "aprendizaje": 85, "juego": 90, "contemplacion": 80, "trabajo": 20, "descanso": 70, "organizacion": 60, "alimentacion": 10, "musica": 10, "risa": 40, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "community+center"
            },
            # 43. Pistas de Patinaje sobre Hielo o Ruedas (Rollerskating)
            {
                "titulo": "Deslizamiento y Equilibrio Sincrónico",
                "porque": "La inercia de los giros circulares y el movimiento fluido forzan a tu mente a coordinar el ritmo físico.",
                "que_hacer": "Toma un asiento en las gradas laterales. Sigue el movimiento de los patinadores y déjate llevar.",
                "donde": "Pista de patinaje del condado indoor/outdoor.",
                "gps": "skating+rink",
                "vector_necesidades": {"movimiento": 80, "naturaleza": 10, "silencio": 20, "agua": 20, "sol": 20, "sombra": 90, "aire_fresco": 75, "creatividad": 30, "comunidad": 80, "aprendizaje": 30, "juego": 95, "contemplacion": 60, "trabajo": 0, "descanso": 40, "organizacion": 30, "alimentacion": 20, "musica": 60, "risa": 70, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "skating+rink"
            },
            # 44. Monumentos Históricos, Plazas Conmemorativas o Memoriales
            {
                "titulo": "Eje del Tiempo Humano",
                "porque": "Pisar el centro de un gran acontecimiento histórico te recuerda que tu agobio actual es un fragmento mínimo.",
                "que_hacer": "Camina rodeando el monumento central. Lee la inscripción grabada en la piedra.",
                "donde": "Plaza histórica, memorial del condado o parque monumental.",
                "gps": "historical+monument+plaza",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 30, "silencio": 65, "agua": 20, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 40, "comunidad": 60, "aprendizaje": 80, "juego": 10, "contemplacion": 95, "trabajo": 0, "descanso": 50, "organizacion": 40, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "historical+monument+plaza"
            },
            # 45. Pasarelas y Miradores sobre Autopistas Interestatales (Freeways)
            {
                "titulo": "Inercia de la Masa en Movimiento",
                "porque": "Ver la velocidad y el destello de miles de luces de freeways marchándose saca a tu cerebro de su inercia estática.",
                "que_hacer": "Quédate en la pasarela peatonal segura mirando el flujo masivo de autos desplazarse hacia el horizonte.",
                "donde": "Punto peatonal elevado o pasarela sobre la autopista interestatal.",
                "gps": "highway+overpass+walkway",
                "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 60, "sombra": 20, "aire_fresco": 80, "creatividad": 10, "comunidad": 40, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "trabajo": 30, "descanso": 30, "organizacion": 80, "alimentacion": 0, "musica": 10, "risa": 15, "esperanza": 75},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "highway+overpass+walkway"
            },
            # 46. Terminales Ferroviarias o de Autobuses Interurbanos (Greyhound)
            {
                "titulo": "Frontera de Asfalto Peatonal",
                "porque": "El ambiente del viajero rudo de carretera te obliga a despertar de golpe tu instinto y vitalidad biopsicosocial.",
                "que_hacer": "Camina por las aceras públicas exteriores observando los equipajes y los rumbos de salida.",
                "donde": "Terminal central de autobuses interurbanos o estación de tránsito.",
                "gps": "bus+terminal+station",
                "vector_necesidades": {"movimiento": 50, "naturaleza": 5, "silencio": 15, "agua": 0, "sol": 65, "sombra": 35, "aire_fresco": 70, "creatividad": 20, "comunidad": 75, "aprendizaje": 40, "juego": 20, "contemplacion": 75, "trabajo": 30, "descanso": 20, "organizacion": 70, "alimentacion": 30, "musica": 10, "risa": 20, "esperanza": 80},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "bus+terminal+station"
            },
            # 47. Megatiendas de Instrumentos Musicales (Guitar Center)
            {
                "titulo": "Frecuencia Acústica Instrumental",
                "porque": "Tocar cuerdas de madera o teclas físicas de pianos desactiva la inercia monótona de las aplicaciones digitales.",
                "que_hacer": "Entra a la sección de teclados o guitarras acústicas. Pasa tus dedos suavemente sobre las teclas libres.",
                "donde": "Gran tienda o almacén de instrumentos musicales de tu condado.",
                "gps": "musical+instruments+store",
                "vector_necesidades": {"movimiento": 20, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 100, "comunidad": 60, "aprendizaje": 75, "juego": 80, "contemplacion": 80, "trabajo": 20, "descanso": 60, "organizacion": 45, "alimentacion": 0, "musica": 100, "risa": 40, "esperanza": 90},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "musical+instruments+store"
            },
            # 48. Almacenes de Antigüedades, Libros de Viejo o Tiendas Vintage
            {
                "titulo": "Túnel de la Permanencia",
                "porque": "Tocar portadas de viejo e inspeccionar reliquias te reconecta con el sentido del tiempo y borra la prisa.",
                "que_hacer": "Examina los estantes del fondo. Busca un tomo o reliquia del siglo pasado y léelo un minuto en silencio.",
                "donde": "Librería de viejo, almacén vintage o anticuario local.",
                "gps": "antique+store+or+used+bookstore",
                "vector_necesidades": {"movimiento": 30, "naturaleza": 0, "silencio": 85, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 85, "comunidad": 40, "aprendizaje": 90, "juego": 50, "contemplacion": 95, "trabajo": 10, "descanso": 75, "organizacion": 50, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 85},
                "variante_spotify": "https://spotify.com",
                "variante_youtube": "https://youtube.com",
                "variante_maps": "antique+store+or+used+bookstore"
            }
        ]
    }
}
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN FINAL DE CONTROL INTEGRAL COMPACTO

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
    budget = str(payload.get("budget", "0")).strip()
    perfil = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    lang = str(payload.get("lang", "es")).lower()
    perfil_local = payload.get("perfil_local", {})

    # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA ORIGINAL INTACTO)
    if opcion_usuario == "CASA":
        misiones = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        random.shuffle(misiones)
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})

    # 2. ACCIÓN DE CAMPO (MODO SALIR CON MOTOR VECTORIAL CWRE ANTI-REPETICIÓN)
    opciones_salir = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
    random.shuffle(opciones_salir)
    
    if len(opciones_salir) >= 2:
        mejor_score = -1
        info = opciones_salir
        for opc in opciones_salir:
            vector_lugar = opc.get("vector_necesidades", {})
            score_coincidencia = 0
            for necesidad, peso_usuario in perfil_local.items():
                if isinstance(peso_usuario, (int, float)):
                    ruido_variancia = random.uniform(0.85, 1.15)
                    score_coincidencia += (vector_lugar.get(necesidad, 50) * ruido_variancia) * peso_usuario
            if score_coincidencia > mejor_score:
                mejor_score = score_coincidencia
                info = opc
    else:
        info = random.choice(opciones_salir)

    # 3. SEGMENTACIÓN DE PRESUPUESTO SILENCIOSA E INVISIBLE (INTERNAL MATRICES)
    if budget == "0":
        precio_real = "Austeridad creativa para proteger tu mente hoy."
        gps_fallback = "public+parks+with+shade+or+public+beaches"
    elif budget == "1": # Max $100: Ross, Burlington, Costco, Walmart, Book Cafes
        precio_real = "Un gustazo mínimo para romper la rutina."
        gps_fallback = "department+store+outlet+or+wholesale+store+costco+or+bookstore+cafe"
    elif budget == "2": # Malls, Recreation, Roofs
        precio_real = "El entorno es tu herramienta de escape hoy."
        gps_fallback = "shopping+mall+or+go+kart+racing+or+restaurant+with+rooftop"
    else: # Premium Abundance Showrooms, Luxury Marinas, 5-Star Lobbies
        precio_real = "Flujo de abundancia activa. Date un lujo merecido hoy."
        gps_fallback = "luxury+marina+or+5+star+hotel+lobby+or+luxury+car+dealership"

    # 4. TRATAMIENTO DE PERFIL ACCESIBLE Y SENSITIVO (USA SPECIAL POLICIES)
    quienes_van = "Vas solo contigo mismo a recuperar tu centro."
    tratamiento_especial = ""
    
    if "adulto" in perfil or "mayor" in perfil or "senior" in perfil or perfil == "accessible":
        quienes_van = "Ruta plana con acceso total por comodidad física y cuidado de tu edad."
        tratamiento_especial = "Desplázate a ritmo lento. Este entorno cuenta con áreas sombreadas y descansos confortables para proteger tu cuerpo hoy."
    elif "veterano" in perfil or "veteran" in perfil:
        quienes_van = "Entorno honorable seleccionado para tu descanso interior."
        tratamiento_especial = "Este espacio está seleccionado por su estabilidad y respeto. Un territorio seguro para recuperar la calma que tu mente merece."
    elif "gobierno" in perfil or "admin" in perfil or "corporativo" in perfil or "trabajador" in perfil:
        quienes_van = "Desconexión radical del tiempo institucional."
        tratamiento_especial = "Estás fuera del horario del sistema. Queda estrictamente bienvenido el descanso; tu mente está libre de reportes y pantallas por los próximos 60 minutos."
    elif "familia" in perfil or "hijos" in perfil or "family" in perfil:
        quienes_van = "Entorno apto para el desahogo de tus niños y seres queridos."

    # 5. EL INTERCEPTOR TRIDIMENSIONAL 3X1 DE CONTROL FINANCIERO Y MANDO LIBRE
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
            link_base = "https://www.google.com/maps/search/?api=1&query="
            gps_query = gps_fallback
            if budget == "0":
                titulo_ganador = (
                    "EXPLORACIÓN DE AUSENCIA" if lang == "es" else "EXPLORATION OF ABSENCE"
                )
                donde_base = (
                    "Espacio Peatonal Abierto, Playa Pública o Parque Verde Nacional"
                    if lang == "es" else "Public Open Space, Beach or National Park"
                )
                guia_masticada = (
                    (
                        f"DESTINO: Un entorno natural o plaza al aire libre.\n"
                        f"QUÉ HACER: Camina despacio registrando el viento, el cielo y el flujo del entorno.\n"
                        f"PARA QUÉ: Romper la hipnosis del encierro, relajar el cuerpo y conectar con la libertad del espacio abierto.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    ) if lang == "es" else (
                        f"TARGET: Free Nature Trail, Public Plaza or Open Beach.\n"
                        f"WHAT TO DO: Walk slowly registering the wind, the sky, and the natural flow.\n"
                        f"WHY: Break the indoor hypnosis, relax your body, and connect with open freedom.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    )
                )
            elif budget == "1":
                titulo_ganador = (
                    "INERCIA DE ABASTECIMIENTO" if lang == "es" else "SMART URBAN INERTIA"
                )
                donde_base = (
                    "Grandes Almacenes de Suministros, Cafeterías de Libros o Tiendas de Saldo Cotidiano"
                    if lang == "es" else "Department Outlets, Bookstores or Distribution Centers"
                )
                guia_masticada = (
                    (
                        f"DESTINO: Un centro de distribución o rincón de diseño urbano.\n"
                        f"QUÉ HACER: Recorre los pasillos masivos, hojea portadas o busca novedades cotidianas con soltura.\n"
                        f"PARA QUÉ: Activar la mente a través de la exploración de objetos, oler el dinamismo del día y sacudirte la monotonía.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    ) if lang == "es" else (
                        f"TARGET: Smart Department Outlets or Used Bookstores.\n"
                        f"WHAT TO DO: Walk through massive aisles, browse book covers, or look for daily items with ease.\n"
                        f"WHY: Activate your mind through object exploration, feel the day's energy, and shake off monotony.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    )
                )
            elif budget == "2":
                titulo_ganador = (
                    "ESTÍMULO Y REGENERACIÓN URBANA" if lang == "es" else "URBAN REGENERATION STIMULUS"
                )
                donde_base = (
                    "Grandes Centros Comerciales, Terrazas Elevadas, Cines o Centros de Recreación"
                    if lang == "es" else "Vibrant Shopping Malls, Rooftops, Movie Theaters or Recreation Loops"
                )
                guia_masticada = (
                    (
                        f"DESTINO: Un entorno comercial o recreativo activo.\n"
                        f"QUÉ HACER: Entra a los pasillos confortables, sube a una terraza a pie o sigue la inercia circular de la pista.\n"
                        f"PARA QUÉ: Rodearte de estímulos visuales, flujos sociales grandes y recuperar la soltura de tu día libre.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    ) if lang == "es" else (
                        f"TARGET: Vibrant Shopping Mall, Rooftop or Recreation Center.\n"
                        f"WHAT TO DO: Walk through comfortable aisles, visit an open terrace, or track the track's circular loop.\n"
                        f"WHY: Surround yourself with visual stimulus, massive social flows, and regain the ease of your day.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    )
                )
                gps_query = info.get(
                    "variante_maps", "shopping+mall+or+go+kart+racing+or+restaurant+with+rooftop"
                )
            else:
                titulo_ganador = (
                    "NÚCLEO DE LA PROSPERIDAD" if lang == "es" else "CORE OF PROSPERITY"
                )
                donde_base = (
                    "Muelles y Marinas de Yates, Vestíbulos Elegantes o Salas de Exhibición Premium"
                    if lang == "es" else "Yacht Marinas, Premium Lobbies or Showrooms"
                )
                guia_masticada = (
                    (
                        f"DESTINO: Un activo urbano de alto estatus sin límites de gasto.\n"
                        f"QUÉ HACER: Camina por las pasarelas de madera entre mástiles, siéntate en los sofás amplios o admira la ingeniería de vanguardia.\n"
                        f"PARA QUÉ: Elevar tu sintonía subiendo el nivel de tu entorno visual, rompiendo la parálisis mental y fluyendo con el éxito material.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    ) if lang == "es" else (
                        f"TARGET: High-End Yacht Marina, Premium Hotel Lobby, or Showroom.\n"
                        f"WHAT TO DO: Walk the wooden docks, take a seat on wide sofas, or inspect cutting-edge engineering.\n"
                        f"WHY: Elevate your vibration by upgrading your visual environment level, breaking mental freeze, and flowing with material success.\n\n"
                        f"ACOMPAÑAMIENTO: {quienes_van}\n"
                        f"GASTO: {precio_real}"
                    )
                )
                gps_query = info.get(
                    "variante_maps", "luxury+marina+or+5+star+hotel+lobby+or+luxury+car+dealership"
                )

    # 6. ENTORNO ORDINARIO LIBRE DE INTERCEPCIÓN
    else:
        link_base = "https://www.google.com/maps/search/?api=1&query="
        ggps_query = info.get("gps", "")
        donde_base = info["donde"]
        titulo_ganador = info["titulo"].upper()
        
        if lang == "en":
            traducciones_guia = {
                "Sombra de árbol": "TARGET: Tree Shade.\nWHAT TO DO: Touch the bark. Stay under its fresh shade.\nWHY: Your eyes need a rest from screen lights.",
                "Orilla de playa": "TARGET: Beach Shore.\nWHAT TO DO: Walk barefoot on wet sand. Let waves touch your feet.\nWHY: Ocean waves clear background noise from your mind.",
                "Paseo del Mall": "TARGET: Shopping Mall Walk.\nWHAT TO DO: Walk through the corridors. Explore what is new and enjoy the lively atmosphere.\nWHY: Surrounding yourself with lights and social dynamic boosts your urban energy.",
                "Estímulo del Sabor": "TARGET: Flavor Stimulus.\nWHAT TO DO: Order something new, listen to background music and enjoy.\nWHY: Great food in a vibrant environment sparks life's abundance."
            }
            guia_masticada = traducciones_guia.get(info["titulo"], f"TARGET: {info['donde']}.\nWHAT TO DO: {info['que_hacer']}\nWHY: {info['porque']}\n{quienes_van}\n{precio_real}")
        else:
            guia_masticada = f"DESTINO: {info['titulo']}.\nPOR QUÉ: {info['porque']}\nQUÉ HACER: {info['que_hacer']}\nCUÁNDO: Ahora mismo. Levántate de la silla ya.\nPARA QUÉ: Romper el zombi urbano y recordar el valor de tu tranquilidad.\n{quienes_van}\n{precio_real}"

    # 7. ADAPTABILIDAD GEOGRÁFICA UNIVERSAL FIJA Y SALIDA DE CONTROL
    if perfil == "accesible":
        gps_query = "wheelchair+accessible+" + gps_query
    elif perfil == "family":
        gps_query = "family+friendly+" + gps_query

    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"
    
    if gps_query:
        link_google_maps_vivo = f"https://google.com{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
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

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 5 (NÚCLEO Y RETOS DOMÉSTICOS)

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
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros."}
    ],

        "CASA_EXTRA": [
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

    
        # ENLACE SOLDADO: Se cierra la estructura interna y se abre el diccionario de campo multidimensional
    "SALIR": {
        "agotado": [
            # 1. Parques Públicos (Naturaleza/Sombra)
            {"titulo": "Sombra de árbol", "porque": "Tu mente merece expandirse y conectar con la vibración silenciosa de la naturaleza.", "que_hacer": "Busca un árbol grande en un parque abierto. Toca su madera y descansa bajo su sombra fresca.", "donde": "Un parque verde nacional.", "gps": "public+parks+with+shade", "vector_necesidades": {"movimiento": 50, "naturaleza": 100, "silencio": 80, "agua": 10, "sol": 40, "sombra": 100, "aire_fresco": 100, "creatividad": 20, "comunidad": 20, "aprendizaje": 30, "juego": 30, "contemplacion": 95, "trabajo": 0, "descanso": 90, "organizacion": 10, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 95}},
            # 2. Playas de Costo Cero
            {"titulo": "Orilla de playa", "porque": "El oleaje infinito limpia el agobio y te sintoniza con la inmensidad del mundo exterior.", "que_hacer": "Camina descalzo sobre la arena mojada. Deja que las olas toquen tus pies y mira el horizonte lejano.", "donde": "Playa pública local.", "gps": "public+beaches", "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 60, "agua": 100, "sol": 95, "sombra": 10, "aire_fresco": 100, "creatividad": 40, "comunidad": 40, "aprendizaje": 10, "juego": 60, "contemplacion": 90, "trabajo": 0, "descanso": 80, "organizacion": 0, "alimentacion": 10, "musica": 20, "risa": 50, "esperanza": 100}},
            # 3. Muelles y Malecones
            {"titulo": "Paseo del muelle", "porque": "Mirar el océano lejano le devuelve la claridad, la grandeza y la perspectiva a tus planes.", "que_hacer": "Camina hasta el extremo del muelle. Siente la brisa marina y quédate contemplando el mar un minuto.", "donde": "Muelle o malecón público.", "gps": "public+fishing+pier", "vector_necesidades": {"movimiento": 60, "naturaleza": 90, "silencio": 50, "agua": 100, "sol": 80, "sombra": 20, "aire_fresco": 100, "creatividad": 30, "comunidad": 50, "aprendizaje": 20, "juego": 40, "contemplacion": 95, "trabajo": 0, "descanso": 70, "organizacion": 10, "alimentacion": 20, "musica": 10, "risa": 40, "esperanza": 95}},
            # 4. Grandes Centros Comerciales (Atracción, Colores y Consumo)
            {"titulo": "Paseo del Mall", "porque": "A veces rodearte de luces, vitrinas llenas, gente moviéndose y música activa renueva tu energía urbana.", "que_hacer": "Camina por los pasillos iluminados del mall. Entra a ver las novedades u objetos interesantes y disfruta de la variedad del entorno.", "donde": "Centro comercial o Shopping Mall de tu zona.", "gps": "shopping+mall", "vector_necesidades": {"movimiento": 60, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 70, "comunidad": 90, "aprendizaje": 20, "juego": 70, "contemplacion": 50, "trabajo": 10, "descanso": 50, "organizacion": 40, "alimentacion": 60, "musica": 60, "risa": 50, "esperanza": 95}},
            # 5. Senderos de Bosque Sombreados
            {"titulo": "Senda forestal", "porque": "El oxígeno puro de los árboles limpia la pesadez del pecho y resetea tus ideas.", "que_hacer": "Sigue los senderos marcados. Escucha el susurro de las ramas y respira hondo la frescura del bosque.", "donde": "Sendero natural boscoso.", "gps": "nature+trails+forest", "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 85, "agua": 20, "sol": 30, "sombra": 95, "aire_fresco": 100, "creatividad": 20, "comunidad": 10, "aprendizaje": 40, "juego": 30, "contemplacion": 90, "trabajo": 0, "descanso": 60, "organizacion": 10, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 90}},
            # 6. Restaurantes Temáticos con Música (Comida, Risa y Vida)
            {"titulo": "Estímulo del Sabor", "porque": "Disfrutar de un buen platillo en un entorno vibrante despierta tus ganas de celebrar el éxito de la abundancia.", "que_hacer": "Pide una mesa cerca del movimiento. Ordena algo nuevo, escucha la música de fondo y disfruta de los sabores.", "donde": "Restaurante con terraza o música en vivo.", "gps": "vibrant+restaurant+with+music", "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 20, "agua": 0, "sol": 40, "sombra": 80, "aire_fresco": 70, "creatividad": 50, "comunidad": 95, "aprendizaje": 30, "juego": 50, "contemplacion": 60, "trabajo": 0, "descanso": 80, "organizacion": 20, "alimentacion": 100, "musica": 80, "risa": 70, "esperanza": 95}},
            # 7. Miradores Elevados de la Ciudad
            {"titulo": "Punto de altura", "porque": "Ver las luces y los rascacielos desde arriba te da perspectiva y expande tus metas de prosperidad.", "que_hacer": "Sube hasta la colina o mirador. Contempla la extensión de la arquitectura en silencio absoluto.", "donde": "Mirador o colina pública panorámica.", "gps": "scenic+overlook", "vector_necesidades": {"movimiento": 65, "naturaleza": 80, "silencio": 75, "agua": 20, "sol": 80, "sombra": 10, "aire_fresco": 95, "creatividad": 50, "comunidad": 40, "aprendizaje": 30, "juego": 20, "contemplacion": 100, "trabajo": 0, "descanso": 60, "organizacion": 0, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 95}},
            # 8. Tiendas de Entretenimiento y Videojuegos (Arcades / Best Buy)
            {"titulo": "Descarga Tecnológica", "porque": "Interactuar con pantallas gigantes, colores de neón y sonidos dinámicos saca a tu mente de cualquier parálisis.", "que_hacer": "Camina explorando las novedades tecnológicas o juega una partida rápida. Deja que los estímulos visuales te activen.", "donde": "Centro de entretenimiento, arcade o gran tienda tecnológica.", "gps": "amusement+arcade+or+electronics+store", "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 15, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 80, "comunidad": 70, "aprendizaje": 60, "juego": 100, "contemplacion": 40, "trabajo": 10, "descanso": 40, "organizacion": 50, "alimentacion": 10, "musica": 60, "risa": 70, "esperanza": 90}},
            # 9. Cafeterías de Libros Animadas (Barnes & Noble)
            {"titulo": "Rincón del Enfoque", "porque": "El olor a café mezclado con miles de portadas de libros te da una sensación de posibilidades infinitas y buen camino.", "que_hacer": "Pide una bebida a tu gusto. Hojea una revista de viajes, autos o negocios en una mesa cómoda.", "donde": "Cafetería dentro de una gran librería.", "gps": "bookstore+cafe", "vector_necesidades": {"movimiento": 10, "naturaleza": 0, "silencio": 70, "agua": 0, "sol": 10, "sombra": 100, "aire_fresco": 40, "creatividad": 75, "comunidad": 60, "aprendizaje": 90, "juego": 30, "contemplacion": 85, "trabajo": 20, "descanso": 90, "organizacion": 50, "alimentacion": 80, "musica": 40, "risa": 30, "esperanza": 95}},
            # 10. Viveros y Tiendas de Plantas Gigantes
            {"titulo": "Bocanada verde", "porque": "Ver la abundancia natural nacer y multiplicarse te alinea directamente con la prosperidad.", "que_hacer": "Camina entre flores, palmeras y brotes. Toca la frescura de las hojas y nota la riqueza del entorno.", "donde": "Invernadero o gran tienda de jardinería.", "gps": "plant+nursery", "vector_necesidades": {"movimiento": 30, "naturaleza": 90, "silencio": 70, "agua": 20, "sol": 60, "sombra": 70, "aire_fresco": 80, "creatividad": 65, "comunidad": 40, "aprendizaje": 60, "juego": 30, "contemplacion": 85, "trabajo": 0, "descanso": 75, "organizacion": 40, "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 95}},
            # 11. Grandes Outlets o Centros de Descuento (Ross / Marshalls)
            {"titulo": "Inercia de la Caza", "porque": "Buscar ofertas, ver marcas de diseñadores y tocar texturas de ropa nueva activa la ilusión de renovar tu estatus de prosperidad.", "que_hacer": "Recorre los pasillos de liquidaciones de ropa u objetos. Disfruta del ritmo rápido de la tienda.", "donde": "Gran tienda de saldos u outlet del condado.", "gps": "department+store+outlet", "vector_necesidades": {"movimiento": 55, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 60, "comunidad": 80, "aprendizaje": 20, "juego": 60, "contemplacion": 40, "trabajo": 30, "descanso": 40, "organizacion": 60, "alimentacion": 10, "musica": 50, "risa": 40, "esperanza": 95}},
            # 12. Distritos de Galerías de Arte Urbanas
            {"titulo": "Espejo Creativo", "porque": "Observar los diseños, colores y formas vanguardistas expande tu visión y enriquece tu mente libre.", "que_hacer": "Camina por la zona de galerías. Contempla las exposiciones y nota la riqueza del pensamiento artístico.", "donde": "Distrito de galerías o centro cultural urbano.", "gps": "art+galleries+district", "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 85, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 100, "comunidad": 40, "aprendizaje": 85, "juego": 20, "contemplacion": 95, "trabajo": 10, "descanso": 60, "organizacion": 30, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 95}},
            # 13. Zonas de Yates y Marinas de Lujo
            {"titulo": "Línea de la Opulencia", "porque": "Ver la ingeniería de los grandes botes y yates amarrados te conecta inconscientemente con el flujo de la riqueza.", "que_hacer": "Camina por las pasarelas de madera de la marina. Escucha el tintineo del viento en los mástiles.", "donde": "Puerto deportivo o marina pública de alta categoría.", "gps": "luxury+marina+boat+dock", "vector_necesidades": {"movimiento": 50, "naturaleza": 70, "silencio": 60, "agua": 100, "sol": 85, "sombra": 20, "aire_fresco": 100, "creatividad": 40, "comunidad": 60, "aprendizaje": 30, "juego": 50, "contemplacion": 90, "trabajo": 10, "descanso": 70, "organizacion": 40, "alimentacion": 30, "musica": 20, "risa": 40, "esperanza": 100}},
            # 14. Vestíbulos de Hoteles de 5 Estrellas (Estilo Las Vegas / Miami)
            {"titulo": "Inyección de Estatus", "porque": "Los espacios monumentales, fuentes internas y mármoles te imbuyen de un sentimiento de éxito y buen camino inmediato.", "que_hacer": "Entra con paso firme y disfruta de la elegancia del lobby. Toma asiento y mira el flujo de personas sofisticadas.", "donde": "Lobby de un hotel de lujo.", "gps": "5+star+hotel+lobby", "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 75, "agua": 20, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 60, "comunidad": 50, "aprendizaje": 20, "juego": 10, "contemplacion": 80, "trabajo": 20, "descanso": 90, "organizacion": 70, "alimentacion": 40, "musica": 30, "risa": 20, "esperanza": 95}},
            # 15. Mercados Gastronómicos Abiertos (Food Halls / Time Out)
            {"titulo": "Pulso del Sabor Urbano", "porque": "Oler decenas de cocinas internacionales mezcladas con risas y charlas rompe cualquier aislamiento de forma dinámica.", "que_hacer": "Recorre las barras de comida. Disfruta de la variedad de platos visuales, colores y la vibración social del lugar.", "donde": "Food Hall gourmet o mercado gastronómico de moda.", "gps": "food+hall+market", "vector_necesidades": {"movimiento": 55, "naturaleza": 30, "silencio": 20, "agua": 0, "sol": 60, "sombra": 60, "aire_fresco": 80, "creatividad": 50, "comunidad": 95, "aprendizaje": 60, "juego": 40, "contemplacion": 60, "trabajo": 30, "descanso": 40, "organizacion": 30, "alimentacion": 100, "musica": 50, "risa": 60, "esperanza": 95}},
            # 16. Centros de Estética, Barberías o Spas Premium
            {"titulo": "Inversión en Ti", "porque": "Dedicarse tiempo a la apariencia física enciende tu autoestima y te recuerda la prosperidad de tu cuerpo.", "que_hacer": "Entra a revisar el menú de masajes, cortes o tratamientos. Disfruta de la atención impecable del personal.", "donde": "Spa urbano, salón o barbería de alta gama.", "gps": "luxury+spa+or+barbershop", "vector_necesidades": {"movimiento": 10, "naturaleza": 10, "silencio": 80, "agua": 40, "sol": 0, "sombra": 100, "aire_fresco": 60, "creatividad": 40, "comunidad": 60, "aprendizaje": 40, "juego": 10, "contemplacion": 80, "trabajo": 0, "descanso": 100, "organizacion": 60, "alimentacion": 20, "musica": 40, "risa": 30, "esperanza": 95}}
        ],

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 3 DE 5 (ACTIVOS DE CAMPO MULTIDIMENSIONALES: ESTRESADO)
        "estresado": [
            # 17. Graderías y Escaleras Públicas Grandes (Movimiento)
            {"titulo": "Caminata en subida", "porque": "Tu cuerpo acumuló un exceso de energía kinética que necesita ser liberado con fuerza.", "que_hacer": "Busca una rampa, gradería o escalera pública. Sube a paso firme usando la fuerza de tus piernas para quemar el estrés.", "donde": "Una escalera o gradería pública abierta.", "gps": "public+stairs", "vector_necesidades": {"movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70, "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10, "juego": 20, "contemplacion": 60, "trabajo": 0, "descanso": 10, "organizacion": 30, "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 80}},
            # 18. Parqueos Elevados y Miradores de Cemento
            {"titulo": "Pista del Viento", "porque": "El espacio masivo, el asfalto plano y el vacío te dan una pista libre para respirar y estirar el cuerpo.", "que_hacer": "Sube al último piso del parqueo. Camina de extremo a extremo sintiendo el viento y mirando los autos pasar abajo.", "donde": "El piso superior de un parqueo evasivo público.", "gps": "open+roof+parking+lot", "vector_necesidades": {"movimiento": 90, "naturaleza": 10, "silencio": 60, "agua": 0, "sol": 90, "sombra": 10, "aire_fresco": 90, "creatividad": 20, "comunidad": 10, "aprendizaje": 10, "juego": 30, "contemplacion": 70, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 75}},
            # 19. Concesionarios de Autos Exóticos y Lujo (Tesla / Porsche / Ferrari)
            {"titulo": "Inercia de Alta Gama", "porque": "Para mentes dinámicas, rodearte de caballos de fuerza, oler el cuero nuevo y ver el diseño aerodinámico enciende la ambición.", "que_hacer": "Entra a la sala de exhibición de autos exóticos. Examina las líneas de los motores y absorbe la vibración del éxito material.", "donde": "Concesionario de vehículos exóticos o deportivos de tu zona.", "gps": "luxury+car+dealership", "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 85, "comunidad": 50, "aprendizaje": 60, "juego": 70, "contemplacion": 75, "trabajo": 30, "descanso": 40, "organizacion": 80, "alimentacion": 0, "musica": 20, "risa": 40, "esperanza": 95}},
            # 20. Complejos y Estadios Deportivos Públicos (Canchas de Béisbol / Fútbol)
            {"titulo": "Pulso de la Competencia", "porque": "El olor a césped cortado, las luces de los estadios y ver la fuerza de un juego en vivo te saca de tus pensamientos fijos.", "que_hacer": "Busca un lugar en la banca lateral de la cancha. Sigue la pelota con tus ojos y contágiate de la energía del equipo.", "donde": "Estadio público, complejo deportivo o jaulas de bateo.", "gps": "public+sports+complex+or+batting+cages", "vector_necesidades": {"movimiento": 100, "naturaleza": 40, "silencio": 20, "agua": 0, "sol": 80, "sombra": 10, "aire_fresco": 90, "creatividad": 20, "comunidad": 85, "aprendizaje": 30, "juego": 95, "contemplacion": 50, "trabajo": 10, "descanso": 15, "organizacion": 30, "alimentacion": 10, "musica": 40, "risa": 60, "esperanza": 90}},
            # 21. Puentes Peatonales Grandes e Interestatales
            {"titulo": "Cruce del Flujo Masivo", "porque": "Caminar sobre la velocidad de miles de autos te ayuda a entender que tus problemas se desplazan rápido.", "que_hacer": "Cruza la pasarela peatonal del puente. Mira los vehículos pasar a toda velocidad debajo de ti y siente la inercia.", "donde": "Puente peatonal elevado o pasarela sobre la autopista.", "gps": "pedestrian+overpass+bridge", "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 20, "agua": 20, "sol": 80, "sombra": 10, "aire_fresco": 95, "creatividad": 30, "comunidad": 40, "aprendizaje": 10, "juego": 20, "contemplacion": 85, "trabajo": 0, "descanso": 40, "organizacion": 0, "alimentacion": 0, "musica": 10, "risa": 20, "esperanza": 80}},
            # 22. Pistas de Karts y Deportes de Motor (Go-Karts)
            {"titulo": "Adrenalina y Control", "porque": "El rugido de los motores, el olor a llanta quemada y la velocidad pura obligan a tu cerebro a apagar de golpe cualquier agobio.", "que_hacer": "Acércate a la barandilla de la pista de karts. Siente la vibración del suelo y observa las curvas cerradas y los adelantamientos.", "donde": "Pista de karts o centro de carreras indoor/outdoor.", "gps": "go+kart+racing", "vector_necesidades": {"movimiento": 90, "naturaleza": 0, "silencio": 0, "agua": 0, "sol": 60, "sombra": 40, "aire_fresco": 80, "creatividad": 40, "comunidad": 75, "aprendizaje": 30, "juego": 100, "contemplacion": 40, "trabajo": 0, "descanso": 10, "organizacion": 40, "alimentacion": 20, "musica": 50, "risa": 80, "esperanza": 85}},
            # 23. Zonas de Skateparks y Parques de Acción Urbana
            {"titulo": "Impacto Dinámico Urbano", "porque": "La cultura callejera, la música hip-hop y el riesgo controlado de los trucos inyectan juventud y vitalidad a tu día.", "que_hacer": "Quédate cerca de las rampas observando las acrobacias en patineta o bicicleta. Absorbe la soltura y audacia del entorno.", "donde": "Skatepark público activo de tu zona.", "gps": "public+skatepark", "vector_necesidades": {"movimiento": 75, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 85, "sombra": 15, "aire_fresco": 85, "creatividad": 70, "comunidad": 80, "aprendizaje": 40, "juego": 95, "contemplacion": 50, "trabajo": 0, "descanso": 20, "organizacion": 10, "alimentacion": 0, "musica": 60, "risa": 60, "esperanza": 85}},
            # 24. Grandes Tiendas de Deportes y Outdoor (Bass Pro Shops / REI)
            {"titulo": "Santuario de la Expedición", "porque": "Explorar barcos en exhibición, acuarios gigantes y equipo de aventura activa tu deseo de explorar el mundo salvaje.", "que_hacer": "Camina por la sección de barcos o pesca de la megatienda. Toca las texturas, mira los diseños y planifica tu próximo escape.", "donde": "Megatienda de deportes de aventura u outdoor.", "gps": "bass+pro+shops+or+rei+store", "vector_necesidades": {"movimiento": 55, "naturaleza": 40, "silencio": 20, "agua": 30, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 80, "comunidad": 65, "aprendizaje": 60, "juego": 85, "contemplacion": 70, "trabajo": 10, "descanso": 50, "organizacion": 60, "alimentacion": 10, "musica": 20, "risa": 40, "esperanza": 90}},
            # 25. Grandes Terminales y Estaciones de Tránsito Activas
            {"titulo": "Inercia del Viajero", "porque": "El movimiento constante de maletas, autobuses y personas abordando le recuerda a tu mente que las fronteras se pueden cruzar.", "que_hacer": "Párate en la zona segura de la plataforma de autobuses o trenes. Siente la vibración del motor y mira los destinos impresos en las pantallas.", "donde": "Estación de tránsito o terminal central de autobuses.", "gps": "transit+station+or+bus+terminal", "vector_necesidades": {"movimiento": 50, "naturaleza": 10, "silencio": 20, "agua": 0, "sol": 60, "sombra": 40, "aire_fresco": 75, "creatividad": 30, "comunidad": 70, "aprendizaje": 50, "juego": 30, "contemplacion": 80, "trabajo": 20, "descanso": 30, "organizacion": 85, "alimentacion": 10, "musica": 10, "risa": 20, "esperanza": 85}},
            # 26. Senderos Geológicos y Parques de Rocas Escénicas
            {"titulo": "Anclaje Mineral Extremo", "porque": "Tocar formaciones rocosas milenarias destruye instantáneamente cualquier cortocircuito digital.", "que_hacer": "Busca una gran muralla de piedra o roca en el sendero. Apoya ambas palmas con firma y absorbe la solidez y estabilidad mineral.", "donde": "Parque geológico, cantera pública o sendero rocoso.", "gps": "state+park+trails+rocks", "vector_necesidades": {"movimiento": 90, "naturaleza": 100, "silencio": 85, "agua": 10, "sol": 60, "sombra": 50, "aire_fresco": 100, "creatividad": 20, "comunidad": 10, "aprendizaje": 40, "juego": 40, "contemplacion": 95, "trabajo": 0, "descanso": 50, "organizacion": 10, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 85}},
            # 27. Clínicas de Estética y Diseño Dental Premium (Smile Centers)
            {"titulo": "Foco en la Sonrisa", "porque": "Ver la transformación cosmética y el cuidado del rostro enciende tu deseo inconsciente de mostrar una expression de triunfo.", "que_hacer": "Camina por la zona de recepción o infórmate sobre blanqueamientos express. Siente la pulcritud y el orden higiénico del lugar.", "donde": "Clínica dental cosmética o centro estético moderno.", "gps": "cosmetic+dental+clinic+or+smile+center", "vector_necesidades": {"movimiento": 20, "naturaleza": 0, "silencio": 80, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 30, "comunidad": 40, "aprendizaje": 60, "juego": 10, "contemplacion": 70, "trabajo": 10, "descanso": 60, "organizacion": 95, "alimentacion": 0, "musica": 20, "risa": 30, "esperanza": 90}},
            # 28. Miradores y Parques de Observación de Aeropuertos
            {"titulo": "Vector de Despegue", "porque": "Mirar la masa de un avión pesado romper la gravedad y elevarse hacia las nubes reprograma de golpe tus límites.", "que_hacer": "Párate en la zona de observación exterior pública. Mira fijamente la trayectoria de un despegue y siente el rugido sónico del aire.", "donde": "Parque de observación de aeronaves colindante al aeropuerto.", "gps": "airport+viewing+area+or+aviation+park", "vector_necesidades": {"movimiento": 40, "naturaleza": 30, "silencio": 10, "agua": 0, "sol": 80, "sombra": 10, "aire_fresco": 90, "creatividad": 40, "comunidad": 60, "aprendizaje": 40, "juego": 30, "contemplacion": 95, "trabajo": 20, "descanso": 40, "organizacion": 70, "alimentacion": 20, "musica": 10, "risa": 30, "esperanza": 95}},
            # 29. Canchas Públicas de Tenis, Racketball o Pickleball
            {"titulo": "Impacto y Reflejos Veloces", "porque": "El sonido seco del impacto de la bola contra la raqueta absorbe al 100% el foco de tu atención visual.", "que_hacer": "Quédate en la grada lateral siguiendo la trayectoria de la pelota con tus ojos a velocidad rápida. Disfruta de la inercia del juego.", "donde": "Cancha pública deportiva del parque de tu condado.", "gps": "public+pickleball+or+tennis+courts", "vector_necesidades": {"movimiento": 85, "naturaleza": 40, "silencio": 30, "agua": 0, "sol": 85, "sombra": 15, "aire_fresco": 90, "creatividad": 20, "comunidad": 70, "aprendizaje": 30, "juego": 95, "contemplacion": 50, "trabajo": 0, "descanso": 30, "organizacion": 30, "alimentacion": 0, "musica": 10, "risa": 50, "esperanza": 80}},
            # 30. Tiendas Megastore de Herramientas y Diseño (Home Depot / Lowe's)
            {"titulo": "Orden e Ingeniería Estructural", "porque": "Caminar entre pasillos de maderas masivas, bloques de piedra, herramientas y planos le devuelve el balance lógico a tu mente.", "que_hacer": "Recorre el pasillo de materiales pesados y construcción. Mira la solidez de las estructuras físicas y nota la capacidad de crear.", "donde": "Establecimiento industrial de construcción de tu zona.", "gps": "hardware+megastore", "vector_necesidades": {"movimiento": 50, "naturaleza": 10, "silencio": 20, "agua": 0, "sol": 20, "sombra": 100, "aire_fresco": 50, "creatividad": 85, "comunidad": 60, "aprendizaje": 70, "juego": 40, "contemplacion": 65, "trabajo": 40, "descanso": 20, "organizacion": 95, "alimentacion": 0, "musica": 10, "risa": 25, "esperanza": 85}},
            # 31. Terrazas y Rooftops de Restaurantes con Vistas Libres
            {"titulo": "Pausa Nutricia Elevada", "porque": "Disfrutar de un buen aroma rodeado de una atmósfera abierta bajo el sol disuelve de inmediato el agobio familiar.", "que_hacer": "Siéntate en la barra de la terraza exterior. Pide un aperitivo simple, disfruta la música lounge y mira los colores de la ciudad.", "donde": "Restaurante con rooftop o terraza abierta elevada.", "gps": "restaurant+with+rooftop+or+outdoor+seating", "vector_necesidades": {"movimiento": 10, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 70, "sombra": 70, "aire_fresco": 90, "creatividad": 45, "comunidad": 90, "aprendizaje": 30, "juego": 40, "contemplacion": 75, "trabajo": 10, "descanso": 80, "organizacion": 40, "alimentacion": 100, "musica": 60, "risa": 60, "esperanza": 90}},
            # 32. Hospitales y Centros Médicos Grandes (Zonas de Fuentes y Jardines)
            {"titulo": "Reflexión Vital Profunda", "porque": "Ver la seriedad de la arquitectura médica y la fragilidad real de la vida te ayuda a poner tus quejas en la escala correcta.", "que_hacer": "Camina por el jardín exterior o la plaza de la gran fuente médica. Siente la quietud y la estabilidad de las estructuras limpias.", "donde": "Jardín exterior público de un gran complejo hospitalario.", "gps": "hospital+public+plaza+or+gardens", "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "silencio": 90, "agua": 30, "sol": 50, "sombra": 70, "aire_fresco": 80, "creatividad": 10, "comunidad": 50, "aprendizaje": 60, "juego": 0, "contemplacion": 100, "trabajo": 10, "descanso": 70, "organizacion": 80, "alimentacion": 10, "musica": 0, "risa": 10, "esperanza": 95}}
        ],

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 4 DE 5 (ACTIVOS DE CAMPO MULTIDIMENSIONALES: ABURRIDO)

        "aburrido": [
            # 33. Calles con Murales (Creatividad Urbana)
            {"titulo": "Paseo de colores", "porque": "Estás repitiendo los mismos días y necesitas inyectar imágenes e ideas totalmente nuevas a tus ojos hoy.", "que_hacer": "Camina despacio observando la acera de enfrente. Encuentra dibujos gigantes pintados con aerosol en los bloques de tu zona.", "donde": "Calle decorada con murales de arte urbano.", "gps": "street+art", "vector_necesidades": {"movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80, "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "trabajo": 10, "descanso": 30, "organizacion": 20, "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95}},
            # 34. Tiendas IKEA o Centros de Arquitectura y Diseño Interior
            {"titulo": "Laberinto de orden", "porque": "Explorar simulaciones de apartamentos y hogares ideales le da una estructura y balance lógico a tu mente en crisis.", "que_hacer": "Camina siguiendo la ruta marcada en el suelo. Observa la organización extrema de los espacios mínimos y los colores modernos.", "donde": "Establecimiento masivo de diseño, muebles o decoración.", "gps": "furniture+store+ikea", "vector_necesidades": {"movimiento": 60, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 90, "comunidad": 65, "aprendizaje": 60, "juego": 50, "contemplacion": 75, "trabajo": 20, "descanso": 40, "organizacion": 100, "alimentacion": 30, "musica": 20, "risa": 40, "esperanza": 80}},
            # 35. Clubes Nocturnos y Lounges Musicales (Atmósfera Social Activa)
            {"titulo": "Pulso rítmico nocturno", "porque": "Romper el confinamiento estático de casa requiere a veces sumergirte de golpe en el movimiento de la noche.", "que_hacer": "Entra a la zona de la barra exterior. Escucha las frecuencias graves del bajo, mira las luces cambiar y disfruta el ambiente.", "donde": "Lounge de música o club nocturno local de moda.", "gps": "music+lounge+bar", "vector_necesidades": {"movimiento": 40, "naturaleza": 0, "silencio": 10, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 60, "comunidad": 90, "aprendizaje": 10, "juego": 80, "contemplacion": 65, "trabajo": 0, "descanso": 50, "organizacion": 20, "alimentacion": 70, "musica": 100, "risa": 70, "esperanza": 80}},
            # 36. Discotecas de Música Latina o Centros de Baile Urbano
            {"titulo": "Catarsis Coreográfica", "porque": "Tu cerebro está dándole vueltas a las preocupaciones rutinarias. La música alta y el baile forzan a tus pensamientos a apagarse de inmediato.", "que_hacer": "Quédate cerca de la pista peatonal observando el balanceo coordinado de las parejas. Disfruta de la risa y soltura del lugar.", "donde": "Discoteca urbana o salón de baile activo.", "gps": "dance+club+or+latin+lounge", "vector_necesidades": {"movimiento": 90, "naturaleza": 0, "silencio": 0, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 40, "creatividad": 70, "comunidad": 95, "aprendizaje": 20, "juego": 95, "contemplacion": 40, "trabajo": 0, "descanso": 10, "organizacion": 10, "alimentacion": 60, "musica": 100, "risa": 80, "esperanza": 85}},
            # 37. Parques de Atracciones, Ferias Locales o Grandes Arcades (Adrenalina)
            {"titulo": "Estímulo de Choque Máximo", "porque": "Los gritos de emoción, las luces mecánicas y los giros rápidos le inyectan dopamina fresca y vitalidad a tu cuerpo.", "que_hacer": "Recorre las avenidas centrales de la feria o parque. Mira los puestos de luces, los retos físicos y contágiate del juego.", "donde": "Feria del condado, parque de atracciones o gran arcade público.", "gps": "amusement+park+or+arcade", "vector_necesidades": {"movimiento": 75, "naturaleza": 20, "silencio": 5, "agua": 10, "sol": 70, "sombra": 30, "aire_fresco": 85, "creatividad": 50, "comunidad": 90, "aprendizaje": 15, "juego": 100, "contemplacion": 40, "trabajo": 0, "descanso": 20, "organizacion": 20, "alimentacion": 80, "musica": 70, "risa": 90, "esperanza": 90}},
            # 38. Mercados de Pulgas Grandes (Flea Markets / Coleccionismo)
            {"titulo": "Cazador de Reliquias", "porque": "Examinar antigüedades u objetos extraños del pasado despierta la curiosidad, la ilusión y la nostalgia sana de tu mente.", "que_hacer": "Camina despacio revisando los artículos sobre las mesas de los vendedores. Intenta encontrar tres objetos que usabas en tu niñez.", "donde": "Flea market de fin de semana o almacén vintage masivo.", "gps": "flea+market", "vector_necesidades": {"movimiento": 60, "naturaleza": 20, "silencio": 20, "agua": 0, "sol": 80, "sombra": 40, "aire_fresco": 90, "creatividad": 80, "comunidad": 90, "aprendizaje": 70, "juego": 60, "contemplacion": 75, "trabajo": 20, "descanso": 40, "organizacion": 25, "alimentacion": 50, "musica": 20, "risa": 50, "esperanza": 85}},
            # 39. Tiendas Megastore Costco, Sam's o Mayoristas Industriales
            {"titulo": "Escala de Suministro Industrial", "porque": "Ver montañas interminables de paletas gigantes, productos apilados y movimiento masivo de personas distrae tu rutina.", "que_hacer": "Recorre los pasillos de comida o electrónica de extremo a extremo. Observa el volumen de la cadena de distribución americana.", "donde": "Almacén mayorista o distribuidora industrial de tu zona.", "gps": "wholesale+store+costco+or+sams", "vector_necesidades": {"movimiento": 55, "naturaleza": 0, "silencio": 15, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 45, "creatividad": 20, "comunidad": 85, "aprendizaje": 40, "juego": 35, "contemplacion": 50, "trabajo": 40, "descanso": 30, "organizacion": 95, "alimentacion": 90, "musica": 10, "risa": 30, "esperanza": 75}},
            # 40. Marinas Públicas y Clubes de Yates
            {"titulo": "Línea de Flotación Marina", "porque": "Observar los veleros, las cubiertas pulidas y el agua en movimiento te regala una bocanada instantánea de aire libre y libertad.", "que_hacer": "Camina por los muelles de madera de la marina pública. Mira cómo los botes se balancean suavemente y respira la frescura marina.", "donde": "Puerto de botes o marina pública de su condado.", "gps": "marina+boat+dock", "vector_necesidades": {"movimiento": 50, "naturaleza": 85, "silencio": 65, "agua": 100, "sol": 85, "sombra": 20, "aire_fresco": 100, "creatividad": 40, "comunidad": 60, "aprendizaje": 30, "juego": 50, "contemplacion": 90, "trabajo": 10, "descanso": 70, "organizacion": 40, "alimentacion": 30, "musica": 20, "risa": 40, "esperanza": 90}},
            # 41. Teatros de Cine Independientes o Clásicos (Arte Alternativo)
            {"titulo": "Ventana de la Ficción", "porque": "El cine independiente te sumerge en narrativas ingeniosas, alejándote del bombardeo comercial masivo del sistema.", "que_hacer": "Ingresa al vestíbulo clásico de la sala. Mira los afiches antiguos, examina la cartelera física y absorbe el ambiente artístico.", "donde": "Teatro de cine independiente, alternativo o clásico local.", "gps": "independent+movie+theater", "vector_necesidades": {"movimiento": 15, "naturaleza": 0, "silencio": 70, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 95, "comunidad": 65, "aprendizaje": 80, "juego": 40, "contemplacion": 90, "trabajo": 10, "descanso": 85, "organizacion": 40, "alimentacion": 40, "musica": 30, "risa": 50, "esperanza": 85}},
            # 42. Clubes de Ajedrez Públicos o Mesas Recreativas de Parques
            {"titulo": "Contacto de Estrategia Humana", "porque": "Ver mentes concentradas calculando jugadas en silencio te obliga a desacelerar la velocidad de tus pensamientos.", "que_hacer": "Párate cerca de una mesa de juego. Analiza en silencio el orden de las piezas de madera y nota la capacidad de enfocar la mente.", "donde": "Club de recreación, centro comunitario o parque de mesas públicos.", "gps": "community+center+or+chess+club", "vector_necesidades": {"movimiento": 20, "naturaleza": 10, "silencio": 65, "agua": 0, "sol": 30, "sombra": 90, "aire_fresco": 60, "creatividad": 60, "comunidad": 100, "aprendizaje": 85, "juego": 90, "contemplacion": 80, "trabajo": 20, "descanso": 70, "organizacion": 60, "alimentacion": 10, "musica": 10, "risa": 40, "esperanza": 90}},
            # 43. Pistas de Patinaje sobre Hielo o Ruedas (Rollerskating)
            {"titulo": "Deslizamiento y Equilibrio Sincrónico", "porque": "La inercia de los giros circulares y el movimiento fluido forzan a tu mente a coordinar el ritmo físico y corporal.", "que_hacer": "Toma un asiento en las gradas laterales. Sigue el movimiento de los patinadores, escucha el ritmo musical y déjate llevar.", "donde": "Pista de patinaje del condado indoor/outdoor.", "gps": "skating+rink", "vector_necesidades": {"movimiento": 80, "naturaleza": 10, "silencio": 20, "agua": 20, "sol": 20, "sombra": 90, "aire_fresco": 75, "creatividad": 30, "comunidad": 80, "aprendizaje": 30, "juego": 95, "contemplacion": 60, "trabajo": 0, "descanso": 40, "organizacion": 30, "alimentacion": 20, "musica": 60, "risa": 70, "esperanza": 85}},
            # 44. Monumentos Históricos, Plazas Conmemorativas o Memoriales
            {"titulo": "Eje del Tiempo Humano", "porque": "Pisar el centro de un gran acontecimiento histórico te recuerda que tu agobio actual es solo un fragmento mínimo.", "que_hacer": "Camina rodeando la estatua o muro conmemorativo central. Lee la inscripción grabada en la piedra y asimila el respeto del lugar.", "donde": "Plaza histórica, memorial del condado o parque monumental.", "gps": "historical+monument+plaza", "vector_necesidades": {"movimiento": 50, "naturaleza": 30, "silencio": 65, "agua": 20, "sol": 80, "sombra": 30, "aire_fresco": 90, "creatividad": 40, "comunidad": 60, "aprendizaje": 80, "juego": 10, "contemplacion": 95, "trabajo": 0, "descanso": 50, "organizacion": 40, "alimentacion": 0, "musica": 0, "risa": 20, "esperanza": 90}},
            # 45. Pasarelas y Miradores sobre Autopistas Interestatales (Freeways)
            {"titulo": "Inercia de la Masa en Movimiento", "porque": "Ver la velocidad y el destello de miles de luces de freeways marchándose saca a tu cerebro de su inercia estática.", "que_hacer": "Quédate en la pasarela peatonal segura mirando el flujo masivo de autos desplazarse hacia el horizonte. Siente la fuerza del motor urbano.", "donde": "Punto peatonal elevado o pasarela sobre la autopista interestatal.", "gps": "highway+overpass+walkway", "vector_necesidades": {"movimiento": 40, "naturaleza": 10, "silencio": 10, "agua": 0, "sol": 60, "sombra": 20, "aire_fresco": 80, "creatividad": 10, "comunidad": 40, "aprendizaje": 20, "juego": 20, "contemplacion": 90, "trabajo": 30, "descanso": 30, "organizacion": 80, "alimentacion": 0, "musica": 10, "risa": 15, "esperanza": 75}},
            # 46. Terminales Ferroviarias o de Autobuses Interurbanos (Greyhound)
            {"titulo": "Frontera de Asfalto Peatonal", "porque": "El ambiente del viajero rudo de carretera te obliga a despertar de golpe tu instinto y vitalidad biopsicosocial.", "que_hacer": "Camina por las aceras públicas exteriores observando los equipajes, los saludos de reencuentro y los rumbos de salida.", "donde": "Terminal central de autobuses interurbanos o estación de tránsito.", "gps": "bus+terminal+station", "vector_necesidades": {"movimiento": 50, "naturaleza": 5, "silencio": 15, "agua": 0, "sol": 65, "sombra": 35, "aire_fresco": 70, "creatividad": 20, "comunidad": 75, "aprendizaje": 40, "juego": 20, "contemplacion": 75, "trabajo": 30, "descanso": 20, "organizacion": 70, "alimentacion": 30, "musica": 10, "risa": 20, "esperanza": 80}},
            # 47. Megatiendas de Instrumentos Musicales (Guitar Center)
            {"titulo": "Frecuencia Acústica Instrumental", "porque": "Tocar cuerdas de madera o teclas físicas de pianos desactiva la inercia monótona de las aplicaciones de tu smartphone.", "que_hacer": "Entra a la sección de teclados o guitarras acústicas. Pasa tus dedos suavemente sobre las teclas libres, escucha la acústica y crea sonido.", "donde": "Gran tienda o almacén de instrumentos musicales de tu condado.", "gps": "musical+instruments+store", "vector_necesidades": {"movimiento": 20, "naturaleza": 0, "silencio": 30, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 100, "comunidad": 60, "aprendizaje": 75, "juego": 80, "contemplacion": 80, "trabajo": 20, "descanso": 60, "organizacion": 45, "alimentacion": 0, "musica": 100, "risa": 40, "esperanza": 90}},
            # 48. Almacenes de Antigüedades, Libros de Viejo o Tiendas Vintage
            {"titulo": "Túnel de la Permanencia", "porque": "Tocar portadas de papel amarillento e inspeccionar reliquias te reconecta con el sentido del tiempo y borra la prisa.", "que_hacer": "Examina los estantes del fondo de la librería de viejo. Busca un tomo o reliquia del siglo pasado, huele el papel y léelo un minuto en silencio.", "donde": "Librería de viejo, almacén vintage o anticuario local.", "gps": "antique+store+or+used+bookstore", "vector_necesidades": {"movimiento": 30, "naturaleza": 0, "silencio": 85, "agua": 0, "sol": 0, "sombra": 100, "aire_fresco": 50, "creatividad": 85, "comunidad": 40, "aprendizaje": 90, "juego": 50, "contemplacion": 95, "trabajo": 10, "descanso": 75, "organizacion": 50, "alimentacion": 0, "musica": 0, "risa": 30, "esperanza": 85}}
        ]
    }
}

# RECURSOS DE INFRAESTRUCTURA TRILLONARIA SELECCIONADOS EN MEMORIA
BIG_TECH_RESOURCES = {
    "spotify_audio": "https://spotify.com",
    "youtube_audio": "https://youtube.com",
    "staffing_agencies": "staffing+agencies"
}

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 5 DE 5 (ENDPOINTS E INICIALIZACIÓN DE PROCESAMIENTO)

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
    
    # Captura las métricas de clics acumuladas localmente en engine.js para las 19 necesidades
    perfil_local = payload.get("perfil_local", {})

    # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA ORIGINAL INTACTO)
    if opcion_usuario == "CASA":
        misiones = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        random.shuffle(misiones)  # Evita la monotonía barajando los retos locales
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})

    # 2. ACCIÓN DE CAMPO (MODO SALIR CON MOTOR DE SELECCIÓN ANTI-REPETICIÓN Y RUIDO VECTORIAL)
    opciones_salir = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
    
    # ANTI-MONOTONÍA SHUFFLER: Pre-scrambles the list order to break perfect tie scores
    random.shuffle(opciones_salir)
    
    # LÓGICA CWRE INTEGRADA REPARADA: Ponderación con varianza dinámica para evitar bucles repetitivos
    if len(opciones_salir) >= 2:
        mejor_score = -1
        info = opciones_salir[0]
        
        for opc in opciones_salir:
            vector_lugar = opc.get("vector_necesidades", {})
            score_coincidencia = 0
            
            # Suma los pesos del historial interno del usuario contra la puntuación del entorno
            for necesidad, peso_usuario in perfil_local.items():
                if isinstance(peso_usuario, (int, float)):
                    # INYECCIÓN DE VARIANZA DE CHOQUE: Rompe monopolios vectoriales planos (ej: Playa)
                    ruido_variancia = random.uniform(0.85, 1.15)
                    peso_base_lugar = vector_lugar.get(necesidad, 50)
                    score_coincidencia += (peso_base_lugar * ruido_variancia) * peso_usuario
                    
            if score_coincidencia > mejor_score:
                mejor_score = score_coincidencia
                info = opc
    else:
        info = random.choice(opciones_salir)

    # Filtro de precio real en palabras cortas de acción y acompañantes
    precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if budget == "0" else "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if budget == "1" else "GASTO: Libre. El dinero es tu herramienta de escape hoy."
    quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if perfil == "solo" else "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia." if perfil == "familia" else "ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad."

    # FILTRO DE SUPERVIVENCIA LABORAL Y BIENESTAR FINANCIERO INTERCEPTOR SANEADO
    palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero"]

    if any(p in desahogo for p in palabras_criticas):
        # LÓGICA DE RAMIFICACIÓN TRIDIMENSIONAL SANEADA (CERO AGENCIAS DE TRABAJO)
        if "amazon" in desahogo:
            canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])
        else:
            canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 5 DE 5 (PARTE B: CIERRE, TRADUCCIONES Y UVICORN)

    else:
        # Rutas bilingües de campo ordinarias libres de deudas
        link_base = "https://google.com"
        gps_query = info["gps"]
        donde_base = info["donde"]

        if lang == "en":
            traducciones_guia = {
                "Sombra de árbol": "TARGET: Tree Shade.\nWHAT TO DO: Touch the bark. Stay under its fresh shade.\nWHY: Your eyes need a rest from screen lights.",
                "Caminata en subida": "TARGET: Public Stairs.\nWHAT TO DO: Walk up firmly using your strength.\nWHY: Release the physical stress from your body.",
                "Paseo de colores": "TARGET: Street Art.\nWHAT TO DO: Look at murals in silence. Find hidden details.\nWHY: Break your daily routine with something new."
            }
            guia_masticada = traducciones_guia.get(info["titulo"], f"TARGET: {info['donde']}.\nWHAT TO DO: {info['que_hacer']}\nWHY: {info['porque']}\n{quienes_van}\n{precio_real}")
            titulo_ganador = info["titulo"].upper()
        else:
            guia_masticada = f"DESTINO: {info['titulo']}.\nPOR QUÉ: {info['porque']}\nQUÉ HACER: {info['que_hacer']}\nCUÁNDO: Ahora mismo. Levántate de la silla ya.\nPARA QUÉ: Para romper el zombi urbano y recordar que la vida es más que pagar cuentas.\n{quienes_van}\n{precio_real}"
            titulo_ganador = info["titulo"].upper()

    # Adaptabilidad del Perfil Biopsicosocial sin exclusión social
    if perfil == "accesible":
        gps_query = "wheelchair+accessible+" + gps_query
    elif perfil == "family":
        gps_query = "family+friendly+" + gps_query

    # FÓRMULA GEOGRÁFICA UNIVERSAL FIJA ORIGINAL RESTAURADA SIN RECORTE NI ALTERACIONES
    anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"

    if gps_query:
        if link_base.startswith("http"):
            link_google_maps_vivo = f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        else:
            link_google_maps_vivo = link_base.replace(" ", "+")
    else:
        link_google_maps_vivo = link_base.replace(" ", "+")

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

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
        # CORREGIDO: Se restauró la clave "descripcion" perdida
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

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 2 DE 5 (PARTE A: ACTIVOS AGOTADO)

    "SALIR": {
        "agotado": [
    # 1. Parques Públicos (Naturaleza/Sombra)
    {"titulo": "Sombra de árbol", "porque": "Tu mente necesita descansar de las luces de la pantalla.", "que_hacer": "Busca un árbol grande. Toca su madera y quédate bajo su sombra fresca.", "donde": "Un parque verde nacional.", "gps": "public+parks+with+shade", "vector_necesidades": {"actividad_fisica": 30, "entorno_verde": 100, "presencia_agua": 0, "aislamiento": 80, "paz_sensorial": 90, "exposicion_sol": 20}},
    # 2. Playas de Costo Cero
    {"titulo": "Orilla de playa", "porque": "El sonido del agua borra el ruido repetitivo de tus pensamientos.", "que_hacer": "Camina descalzo sobre la arena mojada. Deja que las olas toquen tus pies.", "donde": "Playa pública local.", "gps": "public+beaches", "vector_necesidades": {"actividad_fisica": 60, "entorno_verde": 40, "presencia_agua": 100, "aislamiento": 30, "paz_sensorial": 70, "exposicion_sol": 95}},
    # 3. Muelles y Malecones
    {"titulo": "Paseo del muelle", "porque": "Mirar el horizonte lejano le devuelve la perspectiva a tu mente cansada.", "que_hacer": "Camina hasta el extremo del muelle. Quédate mirando el mar fijamente un minuto.", "donde": "Muelle o malecón público.", "gps": "public+fishing+pier", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 10, "presencia_agua": 100, "aislamiento": 40, "paz_sensorial": 60, "exposicion_sol": 80}},
    # 4. Jardines Botánicos Tranquilos
    {"titulo": "Senda botánica", "porque": "La variedad de formas y colores naturales despierta tus sentidos dormidos.", "que_hacer": "Camina despacio observando las texturas de las hojas sin usar tu teléfono.", "donde": "Jardín botánico o invernadero.", "gps": "botanical+gardens", "vector_necesidades": {"actividad_fisica": 40, "entorno_verde": 100, "presencia_agua": 20, "aislamiento": 60, "paz_sensorial": 80, "exposicion_sol": 50}},
    # 5. Senderos de Bosque Sombreados
    {"titulo": "Senda forestal", "porque": "El aire puro de los árboles limpia el agobio acumulado en tu pecho.", "que_hacer": "Camina siguiendo los senderos marcados. Escucha el sonido de tus pasos en la tierra.", "donde": "Sendero natural boscoso.", "gps": "nature+trails+forest", "vector_necesidades": {"actividad_fisica": 85, "entorno_verde": 100, "presencia_agua": 10, "aislamiento": 90, "paz_sensorial": 85, "exposicion_sol": 25}},
    # 6. Lagos y Lagunas Locales
    {"titulo": "Espejo de agua", "porque": "El agua en calma refleja la paz que necesitas recuperar por dentro.", "que_hacer": "Siéntate cerca de la orilla. Observa las ondas que genera el viento en la superficie.", "donde": "Lago o laguna pública.", "gps": "public+lakes+parks", "vector_necesidades": {"actividad_fisica": 20, "entorno_verde": 80, "presencia_agua": 90, "aislamiento": 70, "paz_sensorial": 95, "exposicion_sol": 60}},
    # 7. Miradores Elevados
    {"titulo": "Punto de altura", "porque": "Ver la ciudad desde arriba reduce el tamaño de tus problemas diarios.", "que_hacer": "Sube hasta el mirador. Contempla la extensión del territorio en silencio absoluto.", "donde": "Mirador o colina pública.", "gps": "scenic+overlook", "vector_necesidades": {"actividad_fisica": 70, "entorno_verde": 50, "presencia_agua": 0, "aislamiento": 60, "paz_sensorial": 80, "exposicion_sol": 85}},
    # 8. Refugios de Aves y Humedales
    {"titulo": "Sinfonía natural", "porque": "El canto de los animales silvestres rompe tu parálisis mental de inmediato.", "que_hacer": "Quédate quieto en una estación de observación. Intenta identificar tres sonidos diferentes.", "donde": "Reserva de aves o humedal.", "gps": "wildlife+refuge+wetlands", "vector_necesidades": {"actividad_fisica": 30, "entorno_verde": 90, "presencia_agua": 70, "aislamiento": 85, "paz_sensorial": 75, "exposicion_sol": 40}},
    # 9. Cafeterías de Libros Tranquilas
    {"titulo": "Rincón de lectura", "porque": "El olor a café y el silencio te desconectan del ritmo zombi de la calle.", "que_hacer": "Pide una bebida simple. Lee un capítulo de un libro físico sin mirar notificaciones.", "donde": "Cafetería de libros o librería local.", "gps": "bookstore+cafe", "vector_necesidades": {"actividad_fisica": 10, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 50, "paz_sensorial": 75, "exposicion_sol": 10}},
    # 10. Viveros y Tiendas de Plantas
    {"titulo": "Bocanada verde", "porque": "Rodearte de vida vegetal en crecimiento renueva tus motivos interiores.", "que_hacer": "Camina entre los pasillos de plantas. Toca la textura de las hojas y huele la tierra mojada.", "donde": "Invernadero o tienda de jardinería.", "gps": "plant+nursery", "vector_necesidades": {"actividad_fisica": 30, "entorno_verde": 90, "presencia_agua": 20, "aislamiento": 60, "paz_sensorial": 80, "exposicion_sol": 60}},
    # 11. Bibliotecas Públicas Antiguas
    {"titulo": "Santuario del saber", "porque": "El silencio absoluto de la historia calma la velocidad de tus pensamientos.", "que_hacer": "Busca una mesa de madera al fondo. Quédate de cinco minutos asimilando la quietud de la sala.", "donde": "Biblioteca pública del condado.", "gps": "public+library", "vector_necesidades": {"actividad_fisica": 10, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 70, "paz_sensorial": 100, "exposicion_sol": 0}},
    # 12. Museos de Arte Locales Gratis
    {"titulo": "Espejo creativo", "porque": "Observar la creatividad de otros rompe tu estancamiento mental rutinario.", "que_hacer": "Párate frente a una pintura grande. Intenta descubrir tres detalles ocultos en los trazos.", "donde": "Museo de arte o centro cultural.", "gps": "art+museum", "vector_necesidades": {"actividad_fisica": 40, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 60, "paz_sensorial": 85, "exposicion_sol": 0}},
    # 13. Iglesia o Templos Históricos
    {"titulo": "Refugio del alma", "porque": "La arquitectura sagrada y el vacío detienen el agobio financiero del día.", "que_hacer": "Entra despacio y siéntate al fondo. Respira el aire templado y quédate en contemplación.", "donde": "Iglesia o capilla histórica abierta.", "gps": "historical+church", "vector_necesidades": {"actividad_fisica": 10, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 70, "paz_sensorial": 95, "exposicion_sol": 0}},
    # 14. Vestíbulos de Hoteles de Lujo Tranquilos
    {"titulo": "Pausa de diseño", "porque": "Los espacios amplios y bien ordenados le dan estructura a tu caos interior.", "que_hacer": "Siéntate en uno de los sillones del lobby. Observa los arreglos y el flujo ordenado de personas.", "donde": "Lobby de un hotel de alta categoría.", "gps": "luxury+hotel+lobby", "vector_necesidades": {"actividad_fisica": 10, "entorno_verde": 10, "presencia_agua": 20, "aislamiento": 50, "paz_sensorial": 75, "exposicion_sol": 0}},
    # 15. Mercados Agrícolas de Fin de Weekend
    {"titulo": "Pulso comunitario", "porque": "Ver los frutos directos de la tierra te reconecta con la abundancia real.", "que_hacer": "Recorre los puestos de comida fresca. Observa los colores y habla ligeramente con un productor.", "donde": "Farmers market local.", "gps": "farmers+market", "vector_necesidades": {"actividad_fisica": 55, "entorno_verde": 50, "presencia_agua": 0, "aislamiento": 5, "paz_sensorial": 20, "exposicion_sol": 80}},
    # 16. Clínicas de Bienestar Somático u Holístico
    {"titulo": "Anclaje corporal", "porque": "Tu mente ignora tu cuerpo y necesitas registrar tu salud física ya.", "que_hacer": "Camina hacia la recepción o quédate en la sala de descanso asimilando los aromas relajantes.", "donde": "Centro holístico o spa urbano.", "gps": "wellness+center", "vector_necesidades": {"actividad_fisica": 10, "entorno_verde": 20, "presencia_agua": 30, "aislamiento": 60, "paz_sensorial": 90, "exposicion_sol": 10}}
],

# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 3 DE 5 (PARTE A: ACTIVOS ESTRESADO)

       "estresado": [
    # 17. Escaleras Públicas Grandes (Movimiento)
    {"titulo": "Caminata en subida", "porque": "Tu cuerpo acumuló cansancio muscular y necesitas soltarlo con fuerza.", "que_hacer": "Busca una rampa o escalera pública. Sube a paso firme usando la energía de tus piernas.", "donde": "Una escalera o gradería pública.", "gps": "public+stairs", "vector_necesidades": {"actividad_fisica": 100, "entorno_verde": 30, "presencia_agua": 10, "aislamiento": 70, "paz_sensorial": 50, "exposicion_sol": 70}},
    # 18. Parqueos Vacíos y Terrenos Abiertos
    {"titulo": "Espacio despejado", "porque": "El cemento amplio y el vacío te dan pista libre para estirar el cuerpo.", "que_hacer": "Camina en línea recta de extremo a extremo del parqueo. Siente el viento golpeándote.", "donde": "Un parqueo elevado o zona abierta.", "gps": "open+parking+lot", "vector_necesidades": {"actividad_fisica": 90, "entorno_verde": 10, "presencia_agua": 0, "aislamiento": 90, "paz_sensorial": 60, "exposicion_sol": 90}},
    # 19. Senderos de Montaña con Pendiente
    {"titulo": "Ruta de esfuerzo", "porque": "Conquistar una pendiente física obliga a tu cerebro a apagar los biles.", "que_hacer": "Camina hacia arriba manteniendo un ritmo respiratorio controlado. No te detengas.", "donde": "Sendero público con elevación.", "gps": "hiking+trails+elevation", "vector_necesidades": {"actividad_fisica": 100, "entorno_verde": 95, "presencia_agua": 10, "aislamiento": 80, "paz_sensorial": 75, "exposicion_sol": 75}},
    # 20. Gimnasios Públicos o Pistas de Atletismo
    {"titulo": "Quema de tensión", "porque": "El estrés es energía estancada que necesita salir mediante el sudor.", "que_hacer": "Da una vuelta completa a la pista a paso rápido. Siente tus músculos activarse.", "donde": "Cancha pública o pista de atletismo.", "gps": "public+athletic+track", "vector_necesidades": {"actividad_fisica": 100, "entorno_verde": 20, "presencia_agua": 0, "aislamiento": 40, "paz_sensorial": 30, "exposicion_sol": 80}},
    # 21. Puentes Peatonales Grandes
    {"titulo": "Cruce del flujo", "porque": "Caminar sobre el movimiento te ayuda a entender que todo fluye y cambia.", "que_hacer": "Cruza el puente a pie. Mira los autos o el agua pasar debajo de ti.", "donde": "Puente peatonal o pasarela escénica.", "gps": "pedestrian+bridge", "vector_necesidades": {"actividad_fisica": 80, "entorno_verde": 40, "presencia_agua": 40, "aislamiento": 60, "paz_sensorial": 40, "exposicion_sol": 80}},
    # 22. Campos de Ciclismo o Senderos de Ruedas
    {"titulo": "Velocidad motriz", "porque": "El movimiento rápido desplaza los pensamientos fijos de deudas.", "que_hacer": "Camina con paso ágil por la zona peatonal lateral. Observa la inercia del lugar.", "donde": "Pista pública de bicicletas o sendero plano.", "gps": "bike+path+park", "vector_necesidades": {"actividad_fisica": 95, "entorno_verde": 60, "presencia_agua": 10, "aislamiento": 50, "paz_sensorial": 50, "exposicion_sol": 80}},
    # 23. Zonas de Skateparks Públicos
    {"titulo": "Impacto dynamic", "porque": "El dinamismo juvenil y el riesgo controlado inyectan vitalidad a tu mente.", "que_hacer": "Quédate cerca de las barandillas observando las acrobacias y los saltos mecánicos.", "donde": "Skatepark público de la ciudad.", "gps": "public+skatepark", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 10, "presencia_agua": 0, "aislamiento": 25, "paz_sensorial": 10, "exposicion_sol": 85}},
    # 24. Escalinatas de Edificios de Gobierno o Tribunales
    {"titulo": "Firmeza estructural", "porque": "El peso y la escala de la piedra monumental calman el pánico al mañana.", "que_hacer": "Sube los peldaños solemnemente. Siéntate en la parte alta y mira la plaza de frente.", "donde": "Escaleras de la corte o ayuntamiento.", "gps": "city+hall+steps", "vector_necesidades": {"actividad_fisica": 60, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 50, "paz_sensorial": 60, "exposicion_sol": 70}},
    # 25. Muelles de Carga o Estaciones de Tren Abiertas
    {"titulo": "Inercia de escape", "porque": "Ver la logística de las grandes máquinas le recuerda al cerebro que los viajes existen.", "que_hacer": "Párate de forma segura en la zona peatonal de la estación. Siente la vibración del metal.", "donde": "Estación de tránsito o tren local.", "gps": "train+station+platform", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 10, "presencia_agua": 0, "aislamiento": 30, "paz_sensorial": 20, "exposicion_sol": 60}},
    # 26. Senderos de Parques Nacionales con Rocas
    {"titulo": "Anclaje mineral", "porque": "Tocar materiales macizos y duros destruye de golpe el zombi digital.", "que_hacer": "Busca una formación rocosa grande. Apoya ambas palmas de tus manos firmemente en la piedra.", "donde": "Parque geológico o sendero rocoso.", "gps": "state+park+trails+rock", "vector_necesidades": {"actividad_fisica": 90, "entorno_verde": 100, "presencia_agua": 10, "aislamiento": 90, "paz_sensorial": 85, "exposicion_sol": 60}},
    # 27. Clínicas Dentales o de Salud Corporativa Abiertas
    {"titulo": "Foco preventivo", "porque": "Huir de las responsabilidades del cuerpo drena tu energía biopsicosocial hoy.", "que_hacer": "Camina por el área de recepción o infórmate sobre revisiones básicas. Encara tu cuidado.", "donde": "Centro médico o dental del condado.", "gps": "dental+clinic", "vector_necesidades": {"actividad_fisica": 20, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 60, "paz_sensorial": 80, "exposicion_sol": 0}},
    # 28. Entornos de Aeropuertos (Miradores Exteriores)
    {"titulo": "Vector de despegue", "porque": "Mirar las nubes y los aviones partir te saca del encierro mental de la rutina.", "que_hacer": "Párate en la zona pública de observación exterior. Mira fijamente un despegue hacia el cielo.", "donde": "Mirador de aviones o parque colindante.", "gps": "airport+viewing+area", "vector_necesidades": {"actividad_fisica": 40, "entorno_verde": 30, "presencia_agua": 0, "aislamiento": 40, "paz_sensorial": 15, "exposicion_sol": 80}},
    # 29. Canchas Públicas de Tenis o Pickleball
    {"titulo": "Impacto y reflejos", "porque": "El sonido seco de la bola golpeando la raqueta borra el caos de tus biles.", "que_hacer": "Quédate en la banca lateral mirando la velocidad del juego. Sigue la pelota con tus ojos.", "donde": "Cancha pública de tenis del parque.", "gps": "public+tennis+courts", "vector_necesidades": {"actividad_fisica": 85, "entorno_verde": 40, "presencia_agua": 0, "aislamiento": 30, "paz_sensorial": 30, "exposicion_sol": 85}},
    # 30. Tiendas Home Depot o de Herramientas Grandes
    {"titulo": "Orden constructivo", "porque": "Rodearte de maderas, bloques y planos le da balance lógico a tu mente.", "que_hacer": "Recorre el pasillo de materiales pesados. Mira la solidez de las estructuras físicas.", "donde": "Establecimiento de construcción de tu zona.", "gps": "hardware+store", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 10, "presencia_agua": 0, "aislamiento": 40, "paz_sensorial": 20, "exposicion_sol": 20}},
    # 31. Restaurantes Abiertos con Terrazas de Madera
    {"titulo": "Pausa nutricia", "porque": "Comer algo ligero rodeado de actividad social ligera rompe el aislamiento.", "que_hacer": "Siéntate al aire libre en la barra exterior. Pide un aperitivo simple y mira el entorno.", "donde": "Restaurante local con terraza.", "gps": "restaurant+with+outdoor+seating", "vector_necesidades": {"actividad_fisica": 10, "entorno_verde": 20, "presencia_agua": 10, "aislamiento": 10, "paz_sensorial": 40, "exposicion_sol": 60}},
    # 32. Hospitales del Condado (Zonas de Jardines de Descanso)
    {"titulo": "Reflexión vital", "porque": "Ver la fragilidad real de la vida apaga tus quejas monótonas de inmediato.", "que_hacer": "Camina por las áreas verdes de descanso exteriores. Siente el silencio del respeto y respira.", "donde": "Jardín exterior de un centro médico.", "gps": "hospital+public+gardens", "vector_necesidades": {"actividad_fisica": 30, "entorno_verde": 60, "presencia_agua": 10, "aislamiento": 50, "paz_sensorial": 90, "exposicion_sol": 50}}
],
 
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 4 DE 5 (PARTE A: ACTIVOS ABURRIDO)

        "aburrido": [
    # 33. Calles con Murales (Creatividad)
    {"titulo": "Paseo de colores", "porque": "Estás repitiendo los mismos días y necesitas inyectar imágenes nuevas a tus ojos.", "que_hacer": "Camina despacio por la acera. Encuentra dibujos gigantes pintados en los bloques de tu zona.", "donde": "Calle decorada con arte urbano.", "gps": "street+art", "vector_necesidades": {"actividad_fisica": 80, "entorno_verde": 20, "presencia_agua": 10, "aislamiento": 40, "paz_sensorial": 40, "exposicion_sol": 80}},
    # 34. Tiendas IKEA o Centros de Diseño Interior
    {"titulo": "Laberinto de orden", "porque": "Explorar simulaciones de hogares ideales ordena los nudos de tu cerebro en crisis.", "que_hacer": "Camina siguiendo las flechas del piso. Observa la organización extrema de los espacios mínimos.", "donde": "Establecimiento de diseño o muebles.", "gps": "furniture+store+ikea", "vector_necesidades": {"actividad_fisica": 60, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 35, "paz_sensorial": 35, "exposicion_sol": 0}},
    # 35. Clubes Nocturnos y Lounges Musicales (Zonas de Barra)
    {"titulo": "Pulso rítmico nocturno", "porque": "Romper el confinamiento estático de casa requiere sumergirte en el ritmo social.", "que_hacer": "Entra a la zona de la barra exterior. Escucha las vibraciones del bajo y mira las luces cambiar.", "donde": "Lounge musical o club nocturno local.", "gps": "music+lounge+bar", "vector_necesidades": {"actividad_fisica": 40, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 10, "paz_sensorial": 10, "exposicion_sol": 0}},
    # 36. Discotecas de Música Latina o Baile Urbano
    {"titulo": "Catarsis coreográfica", "porque": "Tu mente está atrapada en sus pensamientos rápidos y el baile rompe esa inercia hoy.", "que_hacer": "Quédate cerca de la pista peatonal observando el movement coordinado de las parejas.", "donde": "Discoteca o club de baile.", "gps": "dance+club", "vector_necesidades": {"actividad_fisica": 90, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 5, "paz_sensorial": 5, "exposicion_sol": 0}},
    # 37. Parques de Atracciones o Ferias Locales
    {"titulo": "Estímulo de choque", "porque": "Los gritos de emoción y los giros mecánicos despiertan tu adrenalina dormida.", "que_hacer": "Recorre los pasillos centrales de la feria. Observa los juegos de luces y los puestos mecánicos.", "donde": "Feria, parque de diversiones o arcade público.", "gps": "amusement+park", "vector_necesidades": {"actividad_fisica": 75, "entorno_verde": 20, "presencia_agua": 10, "aislamiento": 10, "paz_sensorial": 5, "exposicion_sol": 70}},
    # 38. Mercados de Pulgas Grandes (Flea Markets)
    {"titulo": "Cazador de antigüedades", "porque": "Buscar objetos raros del pasado estimula la curiosidad e ilusión de tu mente.", "que_hacer": "Camina examinando los objetos olvidados en las mesas. Encuentra tres cosas que usabas de niño.", "donde": "Flea market de fin de semana.", "gps": "flea+market", "vector_necesidades": {"actividad_fisica": 60, "entorno_verde": 20, "presencia_agua": 0, "aislamiento": 10, "paz_sensorial": 20, "exposicion_sol": 80}},
    # 39. Tiendas Costco o Centros de Distribución Mayorista
    {"titulo": "Escala industrial", "porque": "Ver las montañas de cajas y paletas gigantes distrae tu parálisis mental rutinaria.", "que_hacer": "Recorre el pasillo central de extremo a extremo. Observa el volumen de la cadena de suministro.", "donde": "Almacén mayorista de tu ciudad.", "gps": "wholesale+store+costco", "vector_necesidades": {"actividad_fisica": 55, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 15, "paz_sensorial": 15, "exposicion_sol": 0}},
    # 40. Zonas de Puertos Deportivos o Marinas
    {"titulo": "Línea de flotación", "porque": "Ver los yates y botes amarrados te inyecta de golpe sensación de aire libre.", "que_hacer": "Camina por las pasarelas de madera de la marina. Observa el balanceo de los mástiles.", "donde": "Puerto deportivo o marina pública.", "gps": "marina+boat+dock", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 85, "presencia_agua": 100, "aislamiento": 40, "paz_sensorial": 65, "exposicion_sol": 85}},
    # 41. Teatros o Cines Independientes Locales
    {"titulo": "Ventana de ficción", "porque": "El cine alternativo te saca de tu encierro y te muestra realidades distintas hoy.", "que_hacer": "Acércate a la cartelera física exterior o entra al vestíbulo a observar los afiches de las funciones.", "donde": "Teatro de la comunidad o cine clásico.", "gps": "independent+movie+theater", "vector_necesidades": {"actividad_fisica": 15, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 35, "paz_sensorial": 70, "exposicion_sol": 0}},
    # 42. Centros Comunitarios o Clubes de Ajedrez Públicos
    {"titulo": "Contacto estratégico", "porque": "Ver mentes concentradas en un juego de mesa rompe tu bucle digital individual.", "que_hacer": "Quédate un minuto de pie observando una partida en curso. Analiza el orden de las piezas.", "donde": "Centro comunitario o club de recreación.", "gps": "community+center", "vector_necesidades": {"actividad_fisica": 20, "entorno_verde": 10, "presencia_agua": 0, "aislamiento": 0, "paz_sensorial": 65, "exposicion_sol": 30}},
    # 43. Pistas Públicas de Patinaje sobre Hielo o Ruedas
    {"titulo": "Equilibrio fluido", "porque": "El deslizamiento continuo obliga al cuerpo a concentrar el enfoque biopsicosocial.", "que_hacer": "Siéntate en las gradas peatonales mirando la inercia circular de los patinadores.", "donde": "Pista de patinaje del condado.", "gps": "skating+rink", "vector_necesidades": {"actividad_fisica": 80, "entorno_verde": 10, "presencia_agua": 20, "aislamiento": 20, "paz_sensorial": 20, "exposicion_sol": 20}},
    # 44. Monumentos Históricos o Plazas Conmemorativas
    {"titulo": "Eje del tiempo", "porque": "Pisar el centro de la historia te recuerda que tu crisis de hoy es solo un milisegundo.", "que_hacer": "Camina rodeando la estatua o monumento central. Lee la placa grabada con los ojos cerrados.", "donde": "Plaza histórica o memorial público.", "gps": "historical+monument+plaza", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 30, "presencia_agua": 20, "aislamiento": 40, "paz_sensorial": 65, "exposicion_sol": 80}},
    # 45. Miradores de Puentes de Autopistas Interestatales
    {"titulo": "Inercia de la masa", "porque": "Ver la velocidad de miles de autos marchándose saca a tu cerebro de su parálisis estática.", "que_hacer": "Quédate en la pasarela peatonal segura mirando el flujo masivo de luces de la autopista.", "donde": "Punto elevado sobre la autopista o freeway.", "gps": "highway+overpass+walkway", "vector_necesidades": {"actividad_fisica": 40, "entorno_verde": 10, "presencia_agua": 0, "aislamiento": 60, "paz_sensorial": 10, "exposicion_sol": 60}},
    # 46. Zonas Exteriores de Grandes Terminales de Autobuses o Greyhound
    {"titulo": "Frontera de asfalto", "porque": "El ambiente del viajero rudo de carretera te obliga a despertar tu instinto de supervivencia.", "que_hacer": "Camina por las aceras públicas aledañas observando los equipajes y los rumbos de salida.", "donde": "Terminal de autobuses interurbanos.", "gps": "bus+terminal", "vector_necesidades": {"actividad_fisica": 50, "entorno_verde": 5, "presencia_agua": 0, "aislamiento": 25, "paz_sensorial": 15, "exposicion_sol": 65}},
    # 47. Tiendas de Instrumentos Musicales Grandes
    {"titulo": "Frecuencia acústica libre", "porque": "Tocar cuerdas o teclas físicas desactiva de golpe tus quejas mentales de pantalla.", "que_hacer": "Entra a la sección de guitarras o pianos. Pasa tus dedos suavemente sobre las cuerdas libres.", "donde": "Establecimiento musical de tu condado.", "gps": "musical+instruments+store", "vector_necesidades": {"actividad_fisica": 20, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 40, "paz_sensorial": 30, "exposicion_sol": 0}},
    # 48. Tiendas de Antigüedades o Librerías de Viejo
    {"titulo": "Túnel del tiempo", "porque": "Tocar el papel amarillento e inspeccionar reliquias te reconecta con el sentido de la permanencia.", "que_hacer": "Examina los estantes del fondo. Busca un tomo o un objeto del siglo pasado y estúdialo en silencio.", "donde": "Librería de viejo o almacén vintage.", "gps": "antique+store", "vector_necesidades": {"actividad_fisica": 30, "entorno_verde": 0, "presencia_agua": 0, "aislamiento": 60, "paz_sensorial": 85, "exposicion_sol": 0}}
]
}
}
# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.6.5.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 5 DE 5 (ENDPOINTS, INTERCEPTOR Y ARRANQUE)

# Recursos de infraestructura trillonaria secuestrados para romper la monotonía
BIG_TECH_RESOURCES = {
    "spotify_audio": "https://spotify.com",
    "youtube_audio": "https://youtube.com",
    "staffing_agencies": "staffing+agencies"
}

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

    # Filtro de precio real en palabras cortas de acción
    precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if budget == "0" else "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if budget == "1" else "GASTO: Libre. El dinero es tu herramienta de escape hoy."
    
    # Filtro de acompañantes reales
    quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if perfil == "solo" else "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia." if perfil == "familia" else "ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad."

    # FILTRO DE SUPERVIVENCIA LABORAL Y BIENESTAR FINANCIERO INTERCEPTOR
    palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero"]

    if any(p in desahogo for p in palabras_criticas):
        # LÓGICA DE RAMIFICACIÓN TRIDIMENSIONAL INTEGRADA (3 OPCIONES PARA AMAZON)
        # Forzamos al parásito a barajar entre Spotify, YouTube o Google Maps usando tus mismas variables fijas
        if "amazon" in desahogo:
            canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])
        else:
            canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])

        if canal_multimedia == "SPOTIFY":
            titulo_ganador = "RESET AUDITIVO" if lang == "es" else "AUDIO RESET"
            donde_base = "Zona Libre de Consumo" if lang == "es" else "Store-Free Zone"
            guia_masticada = "DESTINO: Spotify Gratis.\nQUÉ HACER: Escucha los sonidos naturales en silencio.\nPARA QUÉ: Detener el impulso de gastar dinero en cosas innecesarias hoy." if lang == "es" else "TARGET: Free Spotify.\nWHAT TO DO: Listen to nature sounds in silence.\nWHY: Stop the urge to buy unnecessary items today."
            link_base = BIG_TECH_RESOURCES["spotify_audio"]
            gps_query = ""
        elif canal_multimedia == "YOUTUBE":
            titulo_ganador = "REINICIO VISUAL" if lang == "es" else "VISUAL SHOCK"
            donde_base = "Frecuencia de Alivio" if lang == "es" else "Relief Frequency"
            guia_masticada = "DESTINO: Video en YouTube.\nQUÉ HACER: Pon el video en pantalla completa.\nPARA QUÉ: Calmar los pensamientos rápidos del día." if lang == "es" else "TARGET: YouTube Video.\nWHAT TO DO: Play the video in full screen.\nWHY: Calm your racing thoughts right now."
            link_base = BIG_TECH_RESOURCES["youtube_audio"]
            gps_query = ""
        else:
            # Si el azar tira MAPS, evalúa de forma inteligente si viene de Amazon o de una deba general
            if "amazon" in desahogo:
                titulo_ganador = "EXPLORACIÓN DE AUSENCIA" if lang == "es" else "EXPLORATION OF ABSENCE"
                donde_base = "Mercado Local Abierto" if lang == "es" else "Local Open Market"
                guia_masticada = f"DESTINO: Mercado agrícola o de pulgas local.\nQUÉ HACER: Camina y observa personas reales sin comprar nada.\nPARA QUÉ: Romper el bucle de la pantalla digital.\n{quienes_van}\n{precio_real}" if lang == "es" else f"TARGET: Local Farmers or Flea Market.\nWHAT TO DO: Walk and observe real people without buying anything.\nWHY: Break the digital screen loop.\n{quienes_van}\n{precio_real}"
                link_base = "https://www.google.com/maps/search/?api=1&query="
                gps_query = "farmers+market"
            else:
                titulo_ganador = "ACTIVACIÓN LABORAL" if lang == "es" else "ECONOMIC ACTION"
                donde_base = "Oficinas de contratación y staffings corporativos en tu zona." if lang == "es" else "Employment Agency"
                guia_masticada = f"DESTINO: Oficinas de empleo inmediato.\nQUÉ HACER: Entra ya con tu identificación en mano.\nPARA QUÉ: Para ganarle al agobio del dinero y tomar el control de tu economía hoy.\n{quienes_van}\n{precio_real}" if lang == "es" else f"TARGET: Google Maps.\nWHAT TO DO: Go out straight with your physical ID.\nWHY: Look for a quick job and get cash now.\n{quienes_van}\n{precio_real}"
                link_base = "https://www.google.com/maps/search/?api=1&query="
                gps_query = BIG_TECH_RESOURCES["staffing_agencies"]
    else:
        # Rutas bilingües de campo ordinarias libres de deudas
        link_base = "https://www.google.com/maps/search/?api=1&query="
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

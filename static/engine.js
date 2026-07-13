const DRIVER_MATRIX = {
  Aburrido: {
    CASA: {
      Gratis: [
        { name: "YouTube Entertainment", url: "https://youtube.com" },
        { name: "TikTok Trends", url: "https://tiktok.com" },
        { name: "Twitch Live", url: "https://twitch.tv" },
        { name: "Internet Archive Games", url: "https://archive.org" },
        { name: "Wikipedia Random", url: "https://wikipedia.org" }
      ],
      Bajo: [
        { name: "Netflix", url: "https://netflix.com" },
        { name: "Disney Plus", url: "https://disneyplus.com" },
        { name: "Spotify Podcasts", url: "https://spotify.com" },
        { name: "Hulu", url: "https://hulu.com" },
        { name: "Amazon Prime Video", url: "https://amazon.com" },
        { name: "Audible Audiobooks", url: "https://audible.com" },
        { name: "Duolingo Learning", url: "https://duolingo.com" },
        { name: "Apple Music", url: "https://apple.com" }
      ],
      Gasto: [
        { name: "Amazon Retail Hobbies", url: "https://amazon.com" },
        { name: "Etsy Artisan", url: "https://etsy.com" },
        { name: "Best Buy Electronics", url: "https://bestbuy.com" },
        { name: "Target Trends", url: "https://target.com" },
        { name: "eBay Auctions", url: "https://ebay.com" },
        { name: "Poshmark Fashion", url: "https://poshmark.com" },
        { name: "StockX Hypebeast", url: "https://stockx.com" },
        { name: "Newegg Gaming PC", url: "https://newegg.com" },
        { name: "Reverb Instruments", url: "https://reverb.com" },
        { name: "Chewy Pet Luxury", url: "https://chewy.com" },
        { name: "Wayfair Decor", url: "https://wayfair.com" },
        { name: "Home Depot Tools", url: "https://homedepot.com" },
        { name: "Lowe's Hardware", url: "https://lowes.com" },
        { name: "Macy's Department", url: "https://macys.com" },
        { name: "Costco Wholesale", url: "https://costco.com" }
      ]
    },
    Mente: {
      Gratis: [
        { name: "AllTrails Local Hiking", url: "https://alltrails.com{{ZIP}}" },
        { name: "National Park Service State", url: "https://nps.gov{{STATE}}/index.htm" },
        { name: "State Parks National Portal", url: "https://stateparks.org" },
        { name: "Smithsonian Museums", url: "https://si.edu" },
        { name: "MuseumFinder Local Database", url: "https://museumsusa.org{{ZIP}}%2c1" },
        { name: "Surfline Live Beach Cameras", url: "https://surfline.com{{ZIP}}" },
        { name: "Recreation gov Public Lands", url: "https://recreation.gov{{ZIP}}" }
      ],
      Bajo: [
        { name: "AMC Theatres Showtimes", url: "https://amctheatres.com{{ZIP}}" },
        { name: "Regal Cinemas Tickets", url: "https://regalcinemas.com{{ZIP}}" },
        { name: "Cinemark Theatres Matrix", url: "https://cinemark.com{{ZIP}}" },
        { name: "Planet Fitness Local Gym", url: "https://planetfitness.com{{ZIP}}" },
        { name: "YMCA Regional Centers", url: "https://ymca.org{{ZIP}}" },
        { name: "KOA Campgrounds Map", url: "https://koa.com" },
        { name: "Broadway local listings", url: "https://broadway.com" }
      ],
      Gasto: [
        { name: "Ticketmaster Live Shows", url: "https://ticketmaster.com{{STATE}}&postalCode={{ZIP}}" },
        { name: "StubHub Last Minute Events", url: "https://stubhub.com{{ZIP}}" },
        { name: "Dave & Buster's Arcade Night", url: "https://daveandbusters.com" },
        { name: "Topgolf Entertainment Hub", url: "https://topgolf.com" },
        { name: "Resident Advisor Electronic Clubs", url: "https://residentadvisor.net{{CITY}}" },
        { name: "Yelp Nightlife Top Spots", url: "https://yelp.com{{ZIP}}" }
      ]
    }
  },
  Agotado: {
    CASA: {
      Gratis: [
        { name: "YouTube Nature Relax", url: "https://youtube.com" },
        { name: "Calm Ambient Sessions", url: "https://youtube.com" }
      ],
      Bajo: [
        { name: "HelloFresh Delivery Box", url: "https://hellofresh.com" },
        { name: "Thrive Market Organics", url: "https://thrivemarket.com" }
      ],
      Gasto: [
        { name: "DoorDash Local Restaurants", url: "https://doordash.com" },
        { name: "Uber Eats Instant Delivery", url: "https://ubereats.com" },
        { name: "Instacart Supermarket Dissector", url: "https://instacart.com" },
        { name: "McDonald's Digital Order", url: "https://mcdonalds.com" },
        { name: "Starbucks Rapid Pickup", url: "https://starbucks.com" },
        { name: "Domino's Tracker Delivery", url: "https://dominos.com" },
        { name: "Grubhub City Delivery", url: "https://grubhub.com" },
        { name: "Subway App Order", url: "https://subway.com" },
        { name: "Chipotle Digital Assembly", url: "https://chipotle.com" },
        { name: "Kroger Home Delivery Network", url: "https://kroger.com" },
        { name: "Shipt Target Ecosystem", url: "https://shipt.com" },
        { name: "Pizza Hut Delivery Network", url: "https://pizzahut.com" },
        { name: "KFC Online Delivery", url: "https://kfc.com" },
        { name: "Burger King Mobile System", url: "https://bk.com" },
        { name: "Dunkin Donuts Pickup", url: "https://dunkindonuts.com" }
      ]
    },
    Mente: {
      Gratis: [
        { name: "Google Maps Silent Parks", url: "https://google.com+{{ZIP}}" }
      ],
      Bajo: [
        { name: "Olive Garden Comfort Food", url: "https://olivegarden.com" },
        { name: "Applebee's Neighborhood Grill", url: "https://applebees.com" },
        { name: "Buffalo Wild Wings Center", url: "https://buffalowildwings.com" },
        { name: "The Cheesecake Factory Mass Menu", url: "https://thecheesecakefactory.com" },
        { name: "Taco Bell Drive Thru Finder", url: "https://tacobell.com" },
        { name: "Papa Johns Local Pizza", url: "https://papajohns.com" }
      ],
      Gasto: [
        { name: "OpenTable Regional Reservations", url: "https://opentable.com{{ZIP}}" },
        { name: "Resy High End Dining Gastronomy", url: "https://resy.com{{CITY}}" },
        { name: "Uber Black Ride", url: "https://uber.com" },
        { name: "Lyft Lux Ride", url: "https://lyft.com" }
      ]
    }
  },
  Estresado: {
    CASA: {
      Gratis: [
        { name: "HRSA Federal Free Clinics", url: "https://hrsa.gov" },
        { name: "Credit Karma Financial Exposure", url: "https://creditkarma.com" },
        { name: "Experian Credit Bureau Audit", url: "https://experian.com" },
        { name: "Credit Sesame Monitoring", url: "https://creditsesame.com" }
      ],
      Bajo: [
        { name: "BetterHelp Online Therapy", url: "https://betterhelp.com" },
        { name: "Talkspace Clinical Psychiatry", url: "https://talkspace.com" },
        { name: "Sesame Care No Insurance Cash Doctor", url: "https://sesamecare.com" },
        { name: "GoodRx Prescription Discounter", url: "https://goodrx.com" },
        { name: "SingleCare Medical Vouchers", url: "https://singlecare.com" },
        { name: "Chime Mobile Banking Fees Zero", url: "https://chime.com" },
        { name: "Venmo Social Financial Link", url: "https://venmo.com" },
        { name: "Cash App Instataneous Processing", url: "https://cash.app" },
        { name: "Acorns Micro Savings Engine", url: "https://acorns.com" },
        { name: "Ally Bank High Yield Portal", url: "https://ally.com" },
        { name: "SoFi Financial Suites", url: "https://sofi.com" }
      ],
      Gasto: [
        { name: "Zocdoc Instant Doctor Booking", url: "https://zocdoc.com{{ZIP}}" },
        { name: "CVS MinuteClinic Urgent Finder", url: "https://cvs.com{{ZIP}}" },
        { name: "Walgreens Pharmacy Network", url: "https://walgreens.com" },
        { name: "Chase Corporate Portals", url: "chase.com" },
        { name: "Bank of America Network", url: "bankofamerica.com" },
        { name: "PayPal Mass Transactions", url: "paypal.com" },
        { name: "Wells Fargo Retail Banking", url: "wellsfargo.com" },
        { name: "Citibank Global Banking", url: "citibank.com" }
      ]
    },
    Mente: {
      Gratis: [
        { name: "AllTrails Stress Relief Trails", url: "alltrails.com{{ZIP}}&diff=easy" }
      ],
      Bajo: [
        { name: "Zillow Housing Market Rentals", url: "zillow.com{{ZIP}}_rb/" },
        { name: "Apartments com Residential Search", url: "apartments.com{{CITY}}-{{STATE}}/" },
        { name: "Realtor com Regional Listings", url: "realtor.com{{ZIP}}" },
        { name: "Trulia Real Estate Engine", url: "trulia.com" },
        { name: "Redfin Home Database", url: "redfin.com" },
        { name: "Instawork Day Shift Staffing", url: "instawork.com" },
        { name: "Wonolo Instant Labor Dispatch", url: "wonolo.com" },
        { name: "TaskRabbit Freelance Handyman", url: "taskrabbit.com" },
        { name: "Indeed Job Database", url: "indeed.com" },
        { name: "ZipRecruiter Rapid Application", url: "ziprecruiter.com" },
        { name: "LinkedIn Professional Systems", url: "linkedin.com" },
        { name: "Fiverr Freelance Output", url: "fiverr.com" },
        { name: "Upwork Global Contracting", url: "upwork.com" },
        { name: "ShiftSmart Hourly Operations", url: "shiftsmart.com" }
      ],
      Gasto: [
        { name: "U-Haul Logistics Relocation", url: "uhaul.com{{STATE}}/{{ZIP}}/" },
        { name: "PODS Containerized Moving", url: "pods.com" },
        { name: "Airbnb Instant Escape", url: "airbnb.com{{CITY}}/homes" },
        { name: "Booking com Global Accommodations", url: "booking.com{{CITY}}" },
        { name: "Expedia Metasearch Travel", url: "expedia.com" },
        { name: "Delta Air Lines Routes", url: "delta.com" },
        { name: "American Airlines Network", url: "aa.com" },
        { name: "United Airlines Operations", url: "united.com" },
        { name: "Southwest Airlines Low Cost", url: "southwest.com" },
        { name: "JetBlue Airways", url: "jetblue.com" },
        { name: "Royal Caribbean International Cruise", url: "royalcaribbean.com" },
        { name: "Carnival Cruise Line Fun Ships", url: "carnival.com" },
        { name: "Norwegian Cruise Line Logistics", url: "ncl.com" },
        { name: "Amtrak Rail Network US", url: "amtrak.com" },
        { name: "Greyhound Intercity Bus lines", url: "greyhound.com" }
      ]
    }
  },
  Cansado: {
    CASA: {
      Gratis: [
        { name: "YouTube Somatic Rest Meditation", url: "youtube.com" }
      ],
      Bajo: [
        { name: "Chewy Rapid Pet Consumables", url: "chewy.com" }
      ],
      Gasto: [
        { name: "Walmart Grocery Logistics", url: "walmart.com" },
        { name: "Amazon Fresh Instant Food", url: "amazon.com" }
      ]
    },
    Mente: {
      Gratis: [
        { name: "Google Maps Silent Zones", url: "google.com+{{ZIP}}" }
      ],
      Bajo: [
        { name: "YMCA Spa and Pool Access", url: "ymca.org" }
      ],
      Gasto: [
        { name: "Uber Comfort Transit", url: "uber.com" },
        { name: "Lyft Personal Transport", url: "lyft.com" }
      ]
    }
  },
  Ansioso: {
    CASA: {
      Gratis: [
        { name: "HRSA Community Clinical Support", url: "hrsa.gov" },
        { name: "Remitly Global Remittance Systems", url: "remitly.com" },
        { name: "Western Union International", url: "westernunion.com" }
      ],
      Bajo: [
        { name: "GoodRx Medication Shield", url: "goodrx.com" },
        { name: "BetterHelp Clinical Support", url: "betterhelp.com" },
        { name: "Wise Multi Currency Ledger", url: "https://wise.com" },
        { name: "Intermex Remittance Network", url: "intermexonline.com" }
      ],
      Gasto: [
        { name: "Zocdoc Psychiatry Direct Booking", url: "zocdoc.com" },
        { name: "Teladoc Video Medicine Platform", url: "teladoc.com" },
        { name: "Amwell Emergency Telehealth", url: "amwell.com" }
      ]
    },
    Mente: {
      Gratis: [
        { name: "AllTrails Breathing Walks", url: "alltrails.com" }
      ],
      Bajo: [
        { name: "Indeed Job Acceleration Protocol", url: "indeed.com" },
        { name: "ZipRecruiter Rapid Matrix Apply", url: "ziprecruiter.com" }
      ],
      Gasto: [
        { name: "Booking com Absolute Remote Insulation", url: "booking.com" },
        { name: "TripAdvisor Excursion Filters", url: "tripadvisor.com" },
        { name: "Hopper Predictive Travel Flights", url: "hopper.com" }
      ]
    }
  }
};
const INFANT_LEVEL_ANTIDOTE_PHRASES = ["Baja tus hombros ahora mismo. Todo va a estar bien.","No tienes que arreglar todo tu mundo en este minuto.","Tú eres más importante que cualquier tarea o dinero.","Toma aire con fuerza. Suelta el ruido de la calle.","Tus pies están en el suelo. El suelo te sostiene. Estás a salvo.","El dinero viene y va, pero tu sonrisa se cuida.","No pienses en mañana. Piensa en el aire que entra a tu cuerpo.","Estás haciendo un buen trabajo hoy. Date un abrazo.","Ningún papel o pantalla te dice cuánto vales. Vales mucho.","Deja que los problemas se queden afuera un ratito.","Hacer lo mismo siempre aburre. Vamos a ver algo nuevo.","Tu mente quiere jugar hoy. Vamos a buscar un camino diferente.","Estás a un solo botón de ver un lugar hermoso.","Si cambias lo que miras, cambia cómo te sientes hoy.","No naciste solo para trabajar. Naciste para explorar el mapa.","Vamos a enseñarle a tu cerebro una idea que no conoce.","Caminar por otra calle puede alegrar todo tu día.","La rutina es una caja cerrada. Abre la puerta hoy.","Tu cuerpo no es un juguete con pilas infinitas. Descansa.","Estar cansado está bien. Es la forma en que tu cuerpo pide paz.","Hoy dejamos que las tiendas grandes se muevan por ti.","Apaga las luces de tu cabeza un momento. El mundo espera.","No hacer nada productivo hoy también es ganar un premio.","Cierra los ojos tres segundos. Siente tu corazón latir.","Si estás muy cansado, para. Las soluciones vienen después.","Tu energía es un tesoro. No la gastes en tener miedo.","Suelta el control. Deja que el día ruede solo por un rato."];

// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.0.1
// Company: May Roga LLC
// File: static/engine.js (Frontend Logic)

class AntiStressAudioBroker {
constructor() {
this.intervalId = null;
this.pool = [...INFANT_LEVEL_ANTIDOTE_PHRASES];
this.history = JSON.parse(localStorage.getItem('otg_audio_history')) || [];
}
comenzarTerapiaAuditiva() {
if (this.intervalId) clearInterval(this.intervalId);
this.emitirFraseLimpia();
this.intervalId = setInterval(() => {
this.emitirFraseLimpia();
}, 15000);
}
cancelarTerapiaAuditiva() {
if (this.intervalId) {
clearInterval(this.intervalId);
this.intervalId = null;
}
window.speechSynthesis.cancel();
}
emitirFraseLimpia() {
let limpias = this.pool.filter(frase => !this.history.includes(frase));
if (limpias.length === 0) {
this.history = [];
localStorage.removeItem('otg_audio_history');
limpias = [...this.pool];
}
const seleccionada = limpias[Math.floor(Math.random() * limpias.length)];
this.history.push(seleccionada);
localStorage.setItem('otg_audio_history', JSON.stringify(this.history));
window.speechSynthesis.cancel();
const enunciado = new SpeechSynthesisUtterance(seleccionada);
enunciado.lang = document.documentElement.lang === 'en' ? 'en-US' : 'es-US';
enunciado.rate = 0.82;
enunciado.pitch = 1.0;
window.speechSynthesis.speak(enunciado);
}}
const motorAudioOTG = new AntiStressAudioBroker();

function calcularEstadoPorPostal(zip) {
const digitosBase = parseInt(zip.substring(0, 2));
if (digitosBase >= 10 && digitosBase <= 14) return "NY";
if (digitosBase >= 32 && digitosBase <= 34) return "FL";
if (digitosBase >= 90 && digitosBase <= 96) return "CA";
if (digitosBase >= 60 && digitosBase <= 62) return "IL";
if (digitosBase >= 70 && digitosBase <= 89) return "TX";
const primerNumero = zip.charAt(0);
const mapaNacional = { "0": "NJ", "1": "PA", "2": "VA", "3": "GA", "4": "OH", "5": "IA", "6": "MO", "7": "LA", "8": "CO", "9": "WA" };
return mapaNacional[primerNumero] || "NY";
}
function calcularCiudadPorPostal(zip) {
if (zip.startsWith("331")) return "miami";
if (zip.startsWith("100")) return "newyork";
if (zip.startsWith("900")) return "losangeles";
if (zip.startsWith("606")) return "chicago";
return "default";}

const KERNEL = {
    timerInaccion: null,
    timerClinico: null,
    temporizadorCascada: null,
    temporizadorCierre: null,
    salidaSugeridaTimeoutId: null,
    timeLeft: 600,
    timeLeftCierre: 60,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",
   
    // Propiedades para la captura de control corporativo
    corporateSelectedEmotion: "",
    corporateSelectedEnvironment: "",
    corporateSelectedBudget: "",
    corporateSelectedZip: "",

    contadorToques: 0,
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5],
   
    historialSalir: [],
    historialCasa: [],
    historialPreguntas: [],
    historialRetosSecuencias: [],

    lastDecayTimestamp: null,
    sessionSeed: null,

    MAX_HISTORY_SALIR: 5,
    MAX_HISTORY_CASA: 8,
    MAX_HISTORY_ORACULO: 12,
    MAX_HISTORY_RETOS_SECUENCIAS: 3,
    DECAY_PER_DAY: 0.985,

    conteoInaccion: 0,
    indicePreguntaCascada: 0,

    DEFAULT_NECESSITY_PROFILE: {
        "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
        "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
        "juego": 50, "contemplacion": 50, "descanso": 50, "organizacion": 50,
        "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
        "indicador_ansiedad": 0
    },
   
    CATALOGO_PREGUNTAS_ES: [
        // Bloque 1: El Bucle Digital Urbano (Redes, Contenido y Consumo)
        "¿Abres redes sociales por inercia, comparando tu día con imágenes idealizadas?",
        "¿Te pierdes en contenido de video que olvidas en pocos segundos, buscando llenar un vacío?",
        "¿Usas música para ahogar el ruido mental y la inquietud de tu día a día?",
        "¿Sientes que lo digital te desconectó de la capacidad de observar el mundo real en calma?",

        // Bloque 2: Evasión y Rutina Física (Comida, Descanso y Movimiento)
        "¿Inviertes mucho en experiencias pasajeras buscando una satisfacción que se desvanece rápido?",
        "¿Te refugias en espacios ajenos huyendo de situaciones que te acompañan a todas partes?",
        "¿Conduces sin destino solo para escapar del encierro en tu propio entorno?",
        "¿Mantienes hábitos por costumbre, sintiendo que te anestesian de tu realidad?",
        "¿Te cuesta romper tu rutina por miedo a la incomodidad o el esfuerzo físico?",
        "¿Tu cuerpo te pide actividad, pero eliges la comodidad estática del sofá?",

        // Bloque 3: Distracción Nocturna y Aislamiento Social
        "¿Buscas ambientes ruidosos para silenciar los pensamientos que te inquietan?",
        "¿Bailas rodeado de gente, sintiendo a la vez una profunda soledad interior?",
        "¿Asistes a eventos sociales por compromiso, anhelando volver a tu propio espacio?",
        "¿Necesitas estímulos externos para sobrellevar conversaciones monótonas?",
        "¿Aceptas la compañía, pero te escudas detrás de tu dispositivo móvil?",
        "¿Proyectas una imagen de perfección social para ocultar tu verdadero sentir?",

        // Bloque 4: Entorno Familiar y Distancia Emocional
        "¿Existen roces constantes con tus seres queridos que impiden la armonía en casa?",
        "¿Sientes desinterés o apatía ante reuniones familiares inevitables?",
        "¿Compartes techo, pero la distancia emocional te hace sentir como extraños?",
        "¿La visita de un familiar te genera tensión en vez de verdadera paz y conexión?",
        "¿La añoranza por los que están lejos te paraliza y te impide vivir tu presente?",
        "¿Sientes que las interacciones diarias están creando silencios en tus relaciones?",

        // Bloque 5: Evasión por Viajes y Fugas de la Realidad
        "¿Subestimas lo que tienes cerca, soñando con escapes lejanos que te son inalcanzables?",
        "¿Deseas una huida total para que el cambio de escenario resuelva tus crisis internas?",
        "¿Crees que la solución a tu insatisfacción es un cambio radical de ubicación?",
        "¿Planeas grandes gastos en ocio que podrían comprometer tu calma futura?",
        "¿Buscas imágenes de paisajes distantes porque perdiste la capacidad de asombrarte con tu propio cielo?",
        "¿Te sientes atado a tu lugar y asumes que la libertad requiere de un boleto a otro sitio?",

        // Bloque 6: Vulnerabilidad Corporal y Sensaciones
        "¿Aplazas tu bienestar físico por miedo a los costos o las complicaciones?",
        "¿Sientes molestias en el cuerpo causadas por la acumulación de tensión diaria?",
        "¿Sientes opresión en el pecho por la prisa del entorno y la incertidumbre del futuro?",
        "¿Has olvidado el consuelo de una respiración profunda, libre de cualquier preocupación?",

        // Bloque 7: El Espejismo Material y Vacío Existencial
        "¿Buscas la tranquilidad en un entorno natural, pero tu mente sigue en el bucle de las preocupaciones?",
        "¿Tienes comodidades, pero una insatisfacción crónica te consume por dentro?",
        "¿Crees que la adquisición de bienes te dará un sentido de pertenencia o identidad?",
        "¿Te paraliza la idea de dejar la seguridad de lo conocido, por miedo a un paso incierto?",
        "¿Te comparas con las posesiones y el estilo de vida de los demás?",

        // Bloque 8: El Despertar Maestro (Quiebre y Mando Absoluto)
        "¿Tu mente se convirtió en tu mayor prisión en este momento?",
        "¿Quieres ayudar a tu familia a estar mejor pero te paraliza no saber cómo empezar?",
        "¿Estás cansado de repetir patrones que consumen tu libertad y energía?",
        "¿Sientes que estás perdiendo tus mejores años esperando un milagro que no va a llegar?",
        "¿Te cuesta creer que exista un espacio gratis en tu zona capaz de devolverte la esperanza?",
        "¿Estás listo para obedecer al mando, soltar tus indecisiones y salir de tu encierro mental hoy?"
    ],
    CATALOGO_PREGUNTAS_EN: [
        // Block 1: The Urban Digital Loop (Social Media, Content, and Consumption)
        "Do you open social media out of inertia, comparing your day to idealized images?",
        "Do you get lost in video content that you forget in a few seconds, trying to fill a void?",
        "Do you use music to drown out mental noise and daily restlessness?",
        "Do you feel like technology disconnected you from the ability to calmly observe the real world?",

        // Block 2: Escape Consumption and Physical Routine (Food, Rest, and Movement)
        "Do you overspend on fleeting experiences looking for satisfaction that quickly fades?",
        "Do you take refuge in external spaces fleeing situations that accompany you everywhere?",
        "Do you drive aimlessly just to escape being cooped up in your own environment?",
        "Do you maintain habits out of custom, feeling that they numb you to your reality?",
        "Are you afraid to break your routine for fear of discomfort or physical effort?",
        "Does your body crave activity, but you choose the static comfort of the couch?",

        // Block 3: Nightly Distraction and Social Isolation
        "Do you seek noisy environments to silence the thoughts that trouble you?",
        "Do you dance surrounded by people, while feeling a deep inner loneliness?",
        "Do you attend social events out of obligation, wishing to return to your own space?",
        "Do you need external stimuli to endure monotonous conversations?",
        "Do you accept company but shield yourself behind your mobile device?",
        "Do you project an image of social perfection to hide your true feelings?",

        // Block 4: Family Environment and Emotional Distance
        "Do you constantly argue with your loved ones over differences that prevent harmony at home?",
        "Do you live under the same roof with your family but emotional distance makes you feel like strangers?",
        "Does a family visit generate tension instead of true peace and connection?",
        "Does longing for those far away paralyze you and prevent you to live your present?",
        "Do you feel that daily interactions are creating silences in your relationships?",

        // Block 5: Travel Evasion and Escapes from Reality
        "Do you underestimate what's near you, dreaming of distant escapes that are unattainable?",
        "Do you wish for a total escape so that a change of scenery resolves your internal crises?",
        "Do you believe that the solution to your dissatisfaction is a radical change of location?",
        "Do you plan large expenses on leisure that could compromise your future calm?",
        "Do you search for images of distant landscapes because you've lost the ability to be amazed by your own sky?",
        "Do you feel tied to your place and assume that freedom requires a ticket to another location?",

        // Block 6: Bodily Vulnerability and Sensations
        "Do you postpone your physical well-being for fear of costs or complications?",
        "Do you feel physical discomfort caused by the accumulation of daily tension?",
        "Do you feel tightness in your chest from the rush of your environment and the uncertainty of the future?",
        "Have you forgotten the comfort of a deep breath, free from any worry?",

        // Block 7: The Material Mirage and Existential Void
        "Do you seek tranquility in a natural environment, but your mind remains in the loop of worries?",
        "Do you have comforts but a chronic dissatisfaction consumes you within?",
        "Do you believe that acquiring property will give you a sense of belonging or identity?",
        "Does the idea of leaving the security of the known paralyze you, for fear of an uncertain step?",
        "Do you secretly compare yourself to the status and possessions of others?",

        // Block 8: The Master Awakening (Breakthrough and Absolute Command)
        "Has your mind become your biggest prison right now?",
        "Do you want to help your family be better but are paralyzed by not knowing how to start?",
        "Are you tired of repeating patterns that consume your freedom and energy?",
        "Do you feel like you are losing your best years waiting for a miracle that won't come?",
        "Is it hard for you to believe there's a free space in your area capable of restoring your hope?",
        "Are you ready to obey the command, let go of your indecisions, and break free from your mental imprisonment today?"
    ],

    AUDIOS_SECUENCIALES_CASA_ES: [
        "Sigue el pulso en tu pantalla. Concéntrate. Estás conmigo hoy.",
        "Suelta los hombros despacio. Deja caer todo el peso físico y mental de tu día.",
        "No pienses en pendientes ahora. No mires tu lista mental. Respira ya.",
        "Mantén el ritmo constante. Siente el aire fresco limpiando tu pecho.",
        "Te estoy acompañando en silencio. No estás solo en esta habitación.",
        "Siente tus pies firmes apoyados en el suelo. La tierra te sostiene gratis.",
        "El piloto automático está apagado en este segundo. Continúa así.",
        "Quédate justo en este instante. El pasado ya pasó, el presente es tuyo.",
        "Suelta la mandíbula ahora. Libera esa carga que aprietas sin darte cuenta.",
        "Tu mente está despertando poco a poco. Estás ganando control real.",
        "Eres mucho más grande que tus preocupaciones. Respira hondo y despacio.",
        "Rompe el bucle que el ruido externo quiere que seas. Quédate en la sala conmigo.",
        "Escucha mi voz. Nota cómo tu respiración se vuelve más profunda y limpia.",
        "Tus ojos están descansando finalmente de las luces artificiales de la pantalla.",
        "Siente los latidos de tu pecho. Es tu motor vivo latiendo para ti.",
        "Siente el peso fuera de tu espalda. Imagina que dejas caer el cansancio.",
        "No dejes que los pensamientos rápidos te saquen de este momento de paz.",
        "Abandona la prisa de la ciudad hoy. Aquí el tiempo es tuyo.",
        "Tu calma regresará, pero este segundo de paz no se repite.",
        "Siente cómo tus pulmones se llenan de fuerza con cada ciclo de aire azul.",
        "Tu familia necesita que estés fuerte por dentro. Recupérate ahora.",
        "Estás borrando el ruido del día. Quédate en la sala respirando conmigo.",
        "La rutina diaria se ha roto. Tú gobiernas tus decisiones en este instante.",
        "El suelo está firme debajo tuyo. Siente la estabilidad de la tierra.",
        "Tu pecho está libre de agobios ahora. Expulsa todo lo malo de golpe.",
        "Estás recuperando tu centro biopsicosocial. Sigue la luz del círculo.",
        "Tu mente es fuerte. Has domado el miedo a las presiones de hoy.",
        "Faltan pocos segundos para el reinicio definitivo. Siente la esperanza.",
        "Estás completamente a salvo aquí. Quédate en paz absoluta en este segundo."
    ],
    AUDIOS_SECUENCIALES_CASA_EN: [
        "Follow the pulse on your screen. Concentrate. You are with me today.",
        "Slowly relax your shoulders. Let all the physical and mental weight of your day fall away.",
        "Don't think about pending tasks now. Don't look at your mental list. Breathe now.",
        "Maintain a constant rhythm. Feel the fresh air cleansing your chest.",
        "I am accompanying you in silence. You are not alone in this room.",
        "Feel your feet firmly on the ground. The earth supports you for free.",
        "The autopilot is off this second. Keep going.",
        "Stay right in this instant. The past is gone, the present is yours.",
        "Release your jaw now. Let go of that tension you hold without realizing.",
        "Your mind is slowly awakening. You are gaining real control.",
        "You are much bigger than your worries. Breathe deeply and slowly.",
        "Break the loop the external noise wants you to be. Stay in the room with me.",
        "Listen to my voice. Notice how your breathing becomes deeper and cleaner.",
        "Your eyes are finally resting from the artificial lights of the screen.",
        "Feel your heartbeat. It's your living engine beating for you.",
        "Feel the weight off your back. Imagine shaking off tiredness.",
        "Don't let racing thoughts take you out of this peaceful moment.",
        "Abandon the city's rush today. Here, time is yours.",
        "Your calm will return, but this second of peace will not repeat.",
        "Feel your lungs fill with strength with each cycle of blue air.",
        "Your family needs you to be strong inside. Recover now.",
        "You are erasing the day's noise. Stay in the room breathing with me.",
        "The daily routine is broken. You govern your decisions at this instant.",
        "The ground is firm beneath you. Feel the stability of the earth.",
        "Your chest is free from worries now. Expel all negativity at once.",
        "You are regaining your biopsychosocial center. Follow the light of the circle.",
        "Your mind is strong. You have tamed the fear of today's pressures.",
        "Only a few seconds left for the definitive reset. Feel the hope.",
        "You are completely safe here. Remain in absolute peace this second."
    ],

    // NUEVO CATÁLOGO DE RETOS DE CIERRE (Microacciones de Recuperación Mental)
    CATALOGO_RETOS_ES: [
        {"id": 201, "titulo": "EL RETO DE LA SUSCRIPCIÓN OLVIDADA", "descripcion": "Abre tu correo o tu aplicación bancaria. Busca 'Subscription', 'Invoice' o 'Payment' y cancela una sola suscripción que ya no utilices. Recuperar el control también es ahorrar.", "img": "gratitude.svg"},
        {"id": 202, "titulo": "EL RETO DE LOS TRES GASTOS", "descripcion": "Abre una nota en tu teléfono y escribe únicamente los tres gastos inevitables de esta semana. No pienses en todo el mes. Solo en esta semana.", "img": "words.svg"},
        {"id": 203, "titulo": "EL RETO DEL ORDEN DIGITAL", "descripcion": "Borra veinte capturas de pantalla, archivos o documentos que ya no necesites. El orden digital también reduce la carga mental.", "img": "observe.svg"},
        {"id": 204, "titulo": "EL RETO DEL SILENCIO", "descripcion": "Silencia durante una hora las aplicaciones que más ansiedad te generan. Tu atención también necesita descansar.", "img": "silence.svg"},
        {"id": 205, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Escribe tres cosas que hoy tienes y que hace algunos años deseabas. Tu mente necesita recordar que también has avanzado.", "img": "gratitude.svg"},
        {"id": 206, "titulo": "EL RETO DEL AGUA", "descripcion": "Levántate despacio, bebe un vaso completo de agua y vuelve respirando con calma.", "img": "stretch.svg"},
        {"id": 207, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre una ventana durante dos minutos y observa el cielo sin mirar el teléfono.", "img": "nature_sound.svg"},
        {"id": 208, "titulo": "EL RETO DEL ORDEN", "descripcion": "Guarda únicamente cinco objetos que estén fuera de lugar. Cinco son suficientes por hoy.", "img": "observe.svg"},
        {"id": 209, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Realiza cinco respiraciones profundas siguiendo un ritmo lento. No tienes que hacer nada más.", "img": "square_breath.svg"},
        {"id": 210, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "Durante dos minutos mira un punto lejano para permitir que tus ojos descansen de la pantalla.", "img": "nature_sound.svg"},
    ],
    CATALOGO_RETOS_EN: [
        {"id": 201, "titulo": "THE FORGOTTEN SUBSCRIPTION CHALLENGE", "descripcion": "Open your email or banking app. Search for 'Subscription', 'Invoice', or 'Payment' and cancel a single subscription you no longer use. Regaining control is also saving.", "img": "gratitude.svg"},
        {"id": 202, "titulo": "THE THREE EXPENSES CHALLENGE", "descripcion": "Open a note on your phone and write down only the three unavoidable expenses for this week. Don't think about the whole month. Just this week.", "img": "words.svg"},
        {"id": 203, "titulo": "THE DIGITAL ORDER CHALLENGE", "descripcion": "Delete twenty screenshots, files, or documents you no longer need. Digital order also reduces mental load.", "img": "observe.svg"},
        {"id": 204, "titulo": "THE SILENCE CHALLENGE", "descripcion": "Silence the apps that generate the most anxiety for an hour. Your attention also needs rest.", "img": "silence.svg"},
        {"id": 205, "titulo": "THE GRATITUDE CHALLENGE", "descripcion": "Write down three things you have today that you wished for a few years ago. Your mind needs to remember that you have also made progress.", "img": "gratitude.svg"},
        {"id": 206, "titulo": "THE WATER CHALLENGE", "descripcion": "Slowly stand up, drink a full glass of water, and return, breathing calmly.", "img": "stretch.svg"},
        {"id": 207, "titulo": "THE WINDOW CHALLENGE", "descripcion": "Open a window for two minutes and observe the sky without looking at your phone.", "img": "nature_sound.svg"},
        {"id": 208, "titulo": "THE ORDER CHALLENGE", "descripcion": "Put away only five objects that are out of place. Five are enough for today.", "img": "observe.svg"},
        {"id": 209, "titulo": "THE BREATHING CHALLENGE", "descripcion": "Take five deep breaths following a slow rhythm. You don't have to do anything else.", "img": "square_breath.svg"},
        {"id": 210, "titulo": "THE VISUAL REST CHALLENGE", "descripcion": "For two minutes, look at a distant point to allow your eyes to rest from the screen.", "img": "nature_sound.svg"},
    ],

    /**
     * Retrieves or initializes the user's dynamic profile from localStorage.
     * Ensures all 19 needs are present with default values if missing.
     * Applies gradual daily reduction (decay) towards base values.
     * @returns {Object} The user's dynamic profile.
     */
    obtenerPerfilLocal() {
        let perfilRaw = localStorage.getItem("otg_perfil_dinamico");
        let perfil = {};

        if (!perfilRaw) {
            perfil = { ...this.DEFAULT_NECESSITY_PROFILE };
        } else {
            try {
                perfil = JSON.parse(perfilRaw);
                for (const need in this.DEFAULT_NECESSITY_PROFILE) {
                    if (!(need in perfil)) {
                        perfil[need] = this.DEFAULT_NECESSITY_PROFILE[need];
                    }
                }
            } catch (e) {
                console.error("Error parsing otg_perfil_dinamico from localStorage, resetting.", e);
                perfil = { ...this.DEFAULT_NECESSITY_PROFILE };
            }
        }

        const now = Date.now();
        let lastDecayTimestamp = parseInt(localStorage.getItem("otg_last_decay") || now);
        this.sessionSeed = localStorage.getItem("otg_session_seed") || Math.random().toString(36).substring(2, 15);

        const daysPassed = (now - lastDecayTimestamp) / (1000 * 60 * 60 * 24);

        if (daysPassed >= 1) {
            const newPerfil = {};
            const base = 50;
            for (const necesidad in perfil) {
                if (necesidad === "indicador_ansiedad") {
                    newPerfil[necesidad] = Math.max(0, perfil[necesidad] - (daysPassed * 2));
                    continue;
                }
                const valor = perfil[necesidad];
                let diferencia = valor - base;
                diferencia *= (this.DECAY_PER_DAY ** daysPassed);
                newPerfil[necesidad] = Math.round((base + diferencia) * 100) / 100;
            }
            perfil = newPerfil;
            lastDecayTimestamp = now;
        }

        perfil.fecha = new Date(now).toISOString().split('T')[0];
        perfil.timestamp = now;

        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        localStorage.setItem("otg_last_decay", lastDecayTimestamp.toString());
        localStorage.setItem("otg_session_seed", this.sessionSeed);

        return perfil;
    },

    /** Initializes the KERNEL on DOMContentLoaded. */
    init() {
        const storedLang = localStorage.getItem("otg_language");
        if (storedLang) {
            this.idiomaActual = storedLang;
        } else {
            localStorage.setItem("otg_language", this.idiomaActual);
        }
        try {
            this.historialSalir = JSON.parse(localStorage.getItem("otg_historial_salir") || "[]");
            this.historialCasa = JSON.parse(localStorage.getItem("otg_historial_casa") || "[]");
            this.historialPreguntas = JSON.parse(localStorage.getItem("otg_historial_oraculo") || "[]");
            this.historialRetosSecuencias = JSON.parse(localStorage.getItem("otg_historial_retos_secuencias") || "[]");
        } catch (e) {
            console.error("Error parsing history from localStorage, resetting specific histories.", e);
            this.historialSalir = [];
            this.historialCasa = [];
            this.historialPreguntas = [];
            this.historialRetosSecuencias = [];
            localStorage.removeItem("otg_historial_salir");
            localStorage.removeItem("otg_historial_casa");
            localStorage.removeItem("otg_historial_oraculo");
            localStorage.removeItem("otg_historial_retos_secuencias");
        }
        this.obtenerPerfilLocal();

        const zipInput = document.getElementById('inp-zip');
        if (zipInput) {
            zipInput.addEventListener('input', () => this.validarZip());
            this.validarZip();
        }
    },

    /** Starts the initial welcome sequence after user interaction. */
    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
       
        this.cambiarIdioma(this.idiomaActual);
       
        const saludos_es = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Escucha mis preguntas en pantalla.",
            "ópen dán go está activo. Concéntrate un momento. Mira las opciones en tu pantalla ya.",
            "Entraste a ópen dán go. Rompamos tu piloto automático ahora mismo. Toca lo que sientes hoy."
        ];
        const saludos_en = [
            "Welcome to open than go. Your smart escape. Listen to my questions on screen.",
            "open than go is active. Focus for a moment. Look at the options on your screen now.",
            "You entered open than go. Let's break your autopilot right now. Tap what you feel today."
        ];
        const saludos = this.idiomaActual === 'es' ? saludos_es : saludos_en;
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
       
        this.inyectarBloquePreguntas();
        this.iniciarMonitoreoInaccion();
       
        this.activarBotonMandoLibreInicial();
    },

    /**
     * Injects a block of 6 questions into the UI, ensuring they are distinct and not recent.
     */
    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo');
        if (!grid) return;
       
        clearInterval(this.temporizadorCascada);
        grid.innerHTML = "";
        this.indicePreguntaCascada = 0;
       
        const catalogo = this.idiomaActual === 'es' ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
        let preguntasYaVistasRecientemente = new Set(this.historialPreguntas);

        let unseenIndices = [];
        for (let i = 0; i < catalogo.length; i++) {
            if (!preguntasYaVistasRecientemente.has(i)) {
                unseenIndices.push(i);
            }
        }

        if (unseenIndices.length < 6) {
            console.warn("Not enough unseen questions. Resetting Oracle history.");
            this.historialPreguntas = [];
            localStorage.removeItem("otg_historial_oraculo");
            unseenIndices = Array.from({length: catalogo.length}, (_, i) => i);
        }
       
        for (let i = unseenIndices.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [unseenIndices[i], unseenIndices[j]] = [unseenIndices[j], unseenIndices[i]];
        }

        let preguntasSeleccionadasIndices = [];
        let blocksUsedInCurrentSelection = new Set();
       
        for (let i = 0; i < 6; i++) {
            if (unseenIndices.length === 0) break;

            let candidateIndex = -1;
            for (let j = 0; j < unseenIndices.length; j++) {
                const currentIdx = unseenIndices[j];
                const currentBlock = Math.floor(currentIdx / 6);
                if (!blocksUsedInCurrentSelection.has(currentBlock)) {
                    candidateIndex = j;
                    blocksUsedInCurrentSelection.add(currentBlock);
                    break;
                }
            }

            if (candidateIndex === -1) {
                candidateIndex = 0;
                const currentBlock = Math.floor(unseenIndices[candidateIndex] / 6);
                blocksUsedInCurrentSelection.add(currentBlock);
            }
           
            const selectedIndex = unseenIndices.splice(candidateIndex, 1)[0];
            preguntasSeleccionadasIndices.push(selectedIndex);
           
            this.historialPreguntas.push(selectedIndex);
        }
        this.historialPreguntas = this.historialPreguntas.slice(-this.MAX_HISTORY_ORACULO);
        localStorage.setItem("otg_historial_oraculo", JSON.stringify(this.historialPreguntas));

        preguntasSeleccionadasIndices.forEach((questionIdx, i) => {
            let preguntaTexto = catalogo[questionIdx];
            if (!preguntaTexto) return;

            let btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.id = `btn-pregunta-${i}`;
            btn.innerText = `${i + 1}. ${preguntaTexto}`;
            btn.onclick = () => this.reaccionarPreguntaSeleccionada(preguntaTexto);
            grid.appendChild(btn);
        });

        this.iniciarEfectoCascada();
    },

    /** Initiates the fading cascade effect for questions. */
    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
       
        const totalButtons = document.querySelectorAll('.btn-pregunta-crisis').length;
        if (totalButtons === 0) {
            this.liberarCajonEscrituraLibre();
            return;
        }

        this.temporizadorCascada = setInterval(() => {
            let botonParaEliminar = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
           
            if (botonParaEliminar) {
                botonParaEliminar.classList.add('fade-out');
               
                let siguienteIdx = this.indicePreguntaCascada + 1;
                let siguienteBoton = document.getElementById(`btn-pregunta-${siguienteIdx}`);
                if (siguienteBoton) {
                    let textoLimpio = siguienteBoton.innerText.substring(3);
                    this.hablar(textoLimpio);
                }
                this.indicePreguntaCascada++;
            } else {
                clearInterval(this.temporizadorCascada);
                this.liberarCajonEscrituraLibre();
            }
        }, 8000);
    },

    /** Activates the free writing input field and button from start. */
    activarBotonMandoLibreInicial() {
        const textarea = document.getElementById('inp-text-libre');
        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');
        const zipInput = document.getElementById('inp-zip');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "¿Qué te tiene atrapado hoy?" : "What has you trapped today?";
            instruccion.style.color = "var(--accent)";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#666";

        if (btnLibre) {
            const isZipInvalid = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();
            const isTextareaEmpty = textarea.value.trim().length <= 3;

            if (isZipInvalid || isTextareaEmpty) {
                btnLibre.style.background = "#111";
                btnLibre.style.color = "#555";
                btnLibre.style.borderColor = "#222";
                btnLibre.disabled = true;
            } else {
                btnLibre.style.background = "var(--green-action)";
                btnLibre.style.color = "#fff";
                btnLibre.style.borderColor = "var(--green-action)";
                btnLibre.disabled = false;
            }

            btnLibre.onclick = () => {
                let textoEscrito = textarea.value.trim();
                const isZipInvalidOnSubmit = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();

                if (isZipInvalidOnSubmit) {
                    this.hablar(this.idiomaActual === 'es' ? "Por favor, introduce un código postal válido." : "Please enter a valid ZIP code.");
                    zipInput.focus();
                    return;
                }
                if (textoEscrito.length > 3) {
                    this.reaccionarPreguntaSeleccionada(textoEscrito);
                } else {
                    this.hablar(this.idiomaActual === 'es' ? "Escribe tu problema en el cuadro antes de activar el mando." : "Write your problem in the box before activating control.");
                }
            };
        }
        if (textarea) {
            textarea.removeEventListener('input', this.textareaInputHandler);
            this.textareaInputHandler = () => {
                const isZipInvalid = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();
               
                if (textarea.value.trim().length > 3 && !isZipInvalid) {
                    if (btnLibre) {
                        btnLibre.style.background = "var(--green-action)";
                        btnLibre.style.color = "#fff";
                        btnLibre.style.borderColor = "var(--green-action)";
                        btnLibre.disabled = false;
                    }
                } else {
                    if (btnLibre) {
                        btnLibre.style.background = "#111";
                        btnLibre.style.color = "#555";
                        btnLibre.style.borderColor = "#222";
                        btnLibre.disabled = true;
                    }
                }
                this.validarZip();
            };
            textarea.addEventListener('input', this.textareaInputHandler);
        }
        this.validarZip();
    },

    /** Validates ZIP input and controls button state */
    validarZip() {
        const zipInput = document.getElementById('inp-zip');
        const btnActivarLibre = document.getElementById('btn-activar-libre');
        const textarea = document.getElementById('inp-text-libre');

        if (!zipInput || !btnActivarLibre || !textarea) return;

        const zipValue = zipInput.value.trim();
        const isValidZip = zipInput.checkValidity();
        const hasTextareaContent = textarea.value.trim().length > 3;

        if (zipValue.length > 0 && !isValidZip) {
            zipInput.style.borderColor = "var(--accent)";
            btnActivarLibre.disabled = true;
            btnActivarLibre.style.background = "#111";
            btnActivarLibre.style.color = "#555";
            btnActivarLibre.style.borderColor = "#222";
        } else {
            zipInput.style.borderColor = "#222";
            if (hasTextareaContent) {
                btnActivarLibre.disabled = false;
                btnActivarLibre.style.background = "var(--green-action)";
                btnActivarLibre.style.color = "#fff";
                btnActivarLibre.style.borderColor = "var(--green-action)";
            } else {
                btnActivarLibre.disabled = true;
                btnActivarLibre.style.background = "#111";
                btnActivarLibre.style.color = "#555";
                btnActivarLibre.style.borderColor = "#222";
            }
        }
    },

    /** Activates the free writing input field and visually indicates readiness. */
    liberarCajonEscrituraLibre() {
        const textarea = document.getElementById('inp-text-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "Mando libre listo. Cuéntame qué te pasa." : "Free control ready. Tell me what is happening.";
            instruccion.style.color = "var(--green-action)";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#fff";
        if (textarea) textarea.focus();
        this.validarZip();
    },

    /**
     * Monitors user inaction and advances question blocks or pauses.
     */
    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion);
        this.conteoInaccion = 0;
        this.timerInaccion = setInterval(() => {
            this.conteoInaccion++;
            if (this.conteoInaccion === 3 || this.conteoInaccion === 6) {
                clearInterval(this.temporizadorCascada);
                this.inyectarBloquePreguntas();
                this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
            } else if (this.conteoInaccion >= 9) {
                clearInterval(this.timerInaccion);
                clearInterval(this.temporizadorCascada);
                this.hablar(this.idiomaActual === 'es' ? "Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando." : "Apologies. I will give you time. I know your mind is tired. I will be waiting here.");
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) {
                    instruccion.innerText = this.idiomaActual === 'es' ? "Tomando un respiro. Toca cuando estés listo..." : "Taking a breath. Tap when you are ready...";
                    instruccion.style.color = "#666";
                }
            }
        }, 8000);
    },

    /**
     * Handles user selecting a question or entering free text.
     */
    reaccionarPreguntaSeleccionada(textoPregunta) {
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
       
        document.getElementById('inp-text-libre').value = textoPregunta;
        this.ejecutar();
    },

    /**
     * Converts text to speech using browser's SpeechSynthesis API.
     * Checks for API support and uses a fixed Spanish voice for consistency as per instructions.
     * @param {string} texto - The text to speak.
     */
    hablar(texto) {
        if (!('speechSynthesis' in window)) {
            console.warn("Speech Synthesis API not supported in this browser.");
            return;
        }
        if (!texto) return;
        window.speechSynthesis.cancel();
        let fx = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO").replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(fx);
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 1.20;
        window.speechSynthesis.speak(msg);
    },

    /**
     * Changes the application's language and updates UI elements.
     * @param {string} lang - The target language ('es' or 'en').
     */
    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        localStorage.setItem("otg_language", lang);
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');
       
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español.", budget0: "Gratis", budget1: "Bajo", budget2: "Abierto", solo: "Solo", familia: "Familia", accesible: "Accesible", menteAburrido: "Aburrido", menteAgotado: "Agotado", menteEstresado: "Estresado", menteCansado: "Cansado", menteAnsioso: "Ansioso", modoSalir: "SALIR", modoCasa: "CASA", recomenzar: "RECOMENZAR EXPERIENCIA", puertaAbierta: "La puerta está abierta. ¿Continuamos?" },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English.", budget0: "Free", budget1: "Low", budget2: "Open", solo: "Alone", familia: "Family", accesible: "Accessible", menteAburrido: "Bored", menteAgotado: "Exhausted", menteEstresado: "Stressed", menteCansado: "Tired", menteAnsioso: "Anxious", modoSalir: "OUT", modoCasa: "HOME", recomenzar: "RESTART EXPERIENCE", puertaAbierta: "The door is open. Shall we continue?" }
        }[lang];
       
        document.getElementById('html-title').innerText = t.title;
        document.getElementById('txt-app-title').innerText = t.title;
        document.getElementById('lbl-zip').innerText = t.zip;
        document.getElementById('lbl-oraculo-instruccion').innerText = t.instruccion;
        document.getElementById('lbl-desahogo').innerText = t.desahogo;
        document.getElementById('inp-text-libre').placeholder = t.placeholder;
        document.getElementById('btn-activar-libre').innerText = t.btn;
        document.getElementById('opt-budget-0').innerText = t.budget0;
        document.getElementById('opt-budget-1').innerText = t.budget1;
        document.getElementById('opt-budget-2').innerText = t.budget2;
        document.getElementById('opt-perfil-solo').innerText = t.solo;
        document.getElementById('opt-perfil-familia').innerText = t.familia;
        document.getElementById('opt-perfil-accesible').innerText = t.accesible;
        document.getElementById('opt-mente-aburrido').innerText = t.menteAburrido;
        document.getElementById('opt-mente-agotado').innerText = t.menteAgotado;
        document.getElementById('opt-mente-estresado').innerText = t.menteEstresado;
        document.getElementById('opt-mente-cansado').innerText = t.menteCansado;
        document.getElementById('opt-mente-ansioso').innerText = t.menteAnsioso;
        document.querySelector('#modo-selector option[value="SALIR"]').innerText = t.modoSalir;
        document.querySelector('#modo-selector option[value="CASA"]').innerText = t.modoCasa;
       
        const cierreLogo = document.getElementById('cierre-logo');
        if (cierreLogo) cierreLogo.innerText = t.title;
        const cierreBoton = document.getElementById('btn-recomenzar-experiencia');
        if (cierreBoton) cierreBoton.innerText = t.recomenzar;
        const cierreMensajeFinal = document.getElementById('cierre-mensaje-final');
        if (cierreMensajeFinal) cierreMensajeFinal.innerText = t.puertaAbierta;


        this.hablar(t.alert);
        this.inyectarBloquePreguntas();
        this.activarBotonMandoLibreInicial();
    },

    /**
     * Executes the main logic to fetch recommendations from the backend.
     */
    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();
        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }

        const modoActual = document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR";
        const zipInput = document.getElementById('inp-zip');
        const desahogoInput = document.getElementById('inp-text-libre');

        // Capture corporate redirection criteria from active selectors
        const zipIngresadoValue = zipInput ? zipInput.value.trim() : "";
        const emocionRawValue = document.getElementById('mente-selector')?.value || "aburrido";
        const entornoRawValue = document.getElementById('modo-selector')?.value || "SALIR";
        const presupuestoRawValue = document.getElementById('budget-selector')?.value || "0";

        // Map values to DRIVER_MATRIX keys
        this.corporateSelectedEmotion = emocionRawValue.charAt(0).toUpperCase() + emocionRawValue.slice(1); // e.g., "aburrido" -> "Aburrido"
        this.corporateSelectedEnvironment = entornoRawValue === "CASA" ? "CASA" : "Mente"; // Map 'SALIR' to 'Mente' for DRIVER_MATRIX
        this.corporateSelectedBudget = { "0": "Gratis", "1": "Bajo", "2": "Gasto" }[presupuestoRawValue];
        this.corporateSelectedZip = zipIngresadoValue || "10001"; // Default ZIP

        if (zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity()) {
            alert(this.idiomaActual === 'es' ? "Error: Código Postal inválido. Por favor, corrígelo." : "Error: Invalid ZIP Code. Please correct it.");
            this.isLocked = false;
            zipInput.focus();
            return;
        }

        const payload = {
            zip: zipInput ? zipInput.value.trim() : "",
            modo: modoActual,
            desahogo: desahogoInput ? desahogoInput.value.trim() : "",
            lang: this.idiomaActual,
            mente: document.getElementById('mente-selector') ? document.getElementById('mente-selector').value : "aburrido",
            budget: document.getElementById('budget-selector') ? document.getElementById('budget-selector').value : "0",
            perfil: document.getElementById('perfil-selector') ? document.getElementById('perfil-selector').value : "solo",
            perfil_local: this.obtenerPerfilLocal(),
        };

        if (modoActual === "CASA") {
            payload.historial_casa = this.historialCasa;
        } else {
            payload.historial_salir = this.historialSalir;
        }

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('pantalla-cierre').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem;'>${this.idiomaActual === 'es' ? 'CONECTANDO...' : 'CONNECTING...'}</h2></div>`;
        container.classList.remove('hidden');

        try {
            const r = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await r.json();

            if (data.error) {
                alert(data.error);
                document.getElementById('wrapper-form').classList.remove('hidden');
                container.classList.add('hidden');
                this.isLocked = false;
                this.validarZip();
                return;
            }

            this.datosLugarGlobal = data;
            this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER;
            this.indiceMision = 0;
           
            if (this.tipoEscapeGlobal === "ACCION_CAMPO" && data.historial_salir_actualizado) {
                this.historialSalir = data.historial_salir_actualizado;
                localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
            }
            else if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA" && data.historial_casa_actualizado) {
                this.historialCasa = data.historial_casa_actualizado;
                localStorage.setItem("otg_historial_casa", JSON.stringify(this.historialCasa));
            }


            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                this.pasosMisiones = data.misiones; // Now data.misiones will be 1 for forced or 3 for normal CASA
            } else {
                this.pasosMisiones = [];
            }
            this.procesarFlujoSecuencial(container);
        } catch (error) {
            console.error("Fetch error:", error);
            alert(this.idiomaActual === 'es' ? "Error de conexión con el servidor. Por favor, inténtalo de nuevo." : "Connection error with the server. Please try again.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
            this.validarZip();
        }
    },

    /**
     * Processes the sequential flow based on the recommendation type.
     */
    procesarFlujoSecuencial(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL EXTERNO YA", fieldAction: "Acción de Campo", internalMission: "Misión Interna", doItNow: "HAZLO AHORA", suggestedEscape: "Escape sugerido" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN EXTERNAL CHANNEL NOW", fieldAction: "Field Action", internalMission: "Internal Mission", doItNow: "DO IT NOW", suggestedEscape: "Suggested escape" }
        }[this.idiomaActual];

        // Handles external "Field Action" recommendations
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            if (this.datosLugarGlobal) {
                let textoFormateado = this.datosLugarGlobal.destino_instruccion.replace(/\n/g, '<br>');
                container.innerHTML = `
                <div class="mision-card">
                    <small>${t.fieldAction}</small>
                    <h2>${this.datosLugarGlobal.destino_titulo}</h2>
                    <div class="instruccion-text">${textoFormateado}</div>
                    <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; font-size:0.9rem;" disabled>35s ${t.listen}</button>
                    <button id="btn-gps-action" class="hidden" style="width:100%; background:var(--secondary); color:#fff; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; cursor:pointer; font-size:0.95rem; letter-spacing:0.5px;">${t.launch}</button>
                </div>`;

                let speechText = this.datosLugarGlobal.destino_titulo + ". " + this.datosLugarGlobal.destino_instruccion;
                this.hablar(speechText);
               
                let retencion = 35;
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');
               
                this.timerClinico = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s ${t.listen}`;
                    if (retencion <= 0) {
                        clearInterval(this.timerClinico);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
                            btnGps.onclick = () => {
                                try {
                                    let perfil = KERNEL.obtenerPerfilLocal();
                                    const selectedVector = KERNEL.datosLugarGlobal.vector_entorno_seleccionado;
                                   
                                    for (const need in selectedVector) {
                                        if (need !== "indicador_ansiedad" && perfil[need] !== undefined) {
                                            perfil[need] = Math.min(perfil[need] + (selectedVector[need] * 0.1), 100);
                                        }
                                    }
                                    perfil["indicador_ansiedad"] = Math.max(0, perfil["indicador_ansiedad"] - 10);
                                    localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                                } catch (e) {
                                    console.error("Error updating local profile after action:", e);
                                }
                                window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank');
                                KERNEL.reiniciarExperiencia();
                            };
                        }
                    }
                }, 1000);
                return;
            }
        }

        // Handles internal "Domestic Intervention" missions
        if (this.indiceMision >= this.pasosMisiones.length) {
            this.iniciarRelojClinicoCasa(container, t);
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];
       
        container.innerHTML = `
        <div class="mision-card">
            <small>${t.internalMission}</small>
            <h3>${paso.titulo}</h3>
            <p>${paso.descripcion}</p>
            <button id="btn-next" style="width:100%; background:var(--green-action); color:#fff; padding:16px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; border:none; margin-top:15px; font-size:0.95rem;">${t.doItNow}</button>
        </div>`;

        this.hablar(paso.titulo + " . " + paso.descripcion);
        document.getElementById('btn-next').onclick = () => {
            try {
                let perfil = this.obtenerPerfilLocal();
                const missionVector = paso.vector_necesidades || this.DEFAULT_NECESSITY_PROFILE;
                for (const need in missionVector) {
                    if (need !== "indicador_ansiedad" && perfil[need] !== undefined) {
                        perfil[need] = Math.min(perfil[need] + (missionVector[need] * 0.05), 100);
                    }
                }
                perfil["indicador_ansiedad"] = Math.max(0, perfil["indicador_ansiedad"] - 5);
                localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
            } catch (e) {
                console.error("Error updating local profile after CASA mission:", e);
            }
            this.avanzarPaso();
        };
    },

    /** Starts the 10-minute clinical breathing timer for CASA mode. */
    iniciarRelojClinicoCasa(container, t) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();
       
        let msg = this.idiomaActual === 'es' ? "Iniciamos diez minutos de limpieza mental profunda. Respira." : "Starting ten minutes of deep mental clearing. Breathe.";
        this.hablar(msg);
       
        container.innerHTML = `
        <div style="text-align:center; width:100%;">
            <div id="breath-circle" style="cursor:pointer;" title="${this.idiomaActual === 'es' ? 'Toca para enfocar tu mente' : 'Tap to focus your mind'}"></div>
            <div id="timer">10:00</div>
            <p id="txt-pulmon">INHALA / INHALE</p>
            <div id="salida-sugerida" class="hidden" style="margin-top: 30px; padding: 15px; border: 1px dashed #444; border-radius: 8px; font-size: 0.9rem; color: #888;">
                <p style="margin:0;">${t.suggestedEscape}: <a href="#" id="link-salida-sugerida" style="color: var(--accent); text-decoration: none; font-weight: bold;">Cargando...</a></p>
            </div>
        </div>`;

        this.timeLeft = 600;
        this.contadorToques = 0;

        const circleElement = document.getElementById('breath-circle');
        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');
        const salidaSugeridaDiv = document.getElementById('salida-sugerida');
        const linkSalidaSugerida = document.getElementById('link-salida-sugerida');

        const AUDIOS_SECUENCIALES_CASA = this.idiomaActual === 'es' ? this.AUDIOS_SECUENCIALES_CASA_ES : this.AUDIOS_SECUENCIALES_CASA_EN;

        if (circleElement) {
            circleElement.onclick = () => {
                if (this.contadorToques < this.secuenciaAdelantos.length) {
                    let adelantoSegundos = this.secuenciaAdelantos[this.contadorToques];
                    this.timeLeft = Math.max(this.timeLeft - adelantoSegundos, 0);
                    this.contadorToques++;
                    try {
                        let perfil = this.obtenerPerfilLocal();
                        perfil["indicador_ansiedad"] = Math.min((perfil["indicador_ansiedad"] || 0) + 5, 100);
                        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                    } catch (e) {
                        console.error("Error updating anxiety indicator:", e);
                    }
                    let m = Math.floor(this.timeLeft / 60);
                    let s = this.timeLeft % 60;
                    if (timerDiv) {
                        timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
                    }
                }
            };
        }

        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }

        this.salidaSugeridaTimeoutId = setTimeout(async () => {
            try {
                const r = await fetch("/api/mando-integral", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        modo: "SALIR",
                        lang: this.idiomaActual,
                        mente: "agotado",
                        budget: "0",
                        perfil: "solo",
                        desahogo: "",
                        zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
                        perfil_local: this.obtenerPerfilLocal(),
                        historial_salir: this.historialSalir
                    })
                });
                const data = await r.json();
               
                if (data.DIRECCIONAMIENTO_MASTER === "ACCION_CAMPO" && linkSalidaSugerida && salidaSugeridaDiv) {
                    if (data.historial_salir_actualizado) {
                        this.historialSalir = data.historial_salir_actualizado;
                        localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
                    }

                    linkSalidaSugerida.innerText = data.destino_titulo;
                    linkSalidaSugerida.href = data.destino_coordenadas_gps;
                    salidaSugeridaDiv.classList.remove('hidden');
                    this.hablar(this.idiomaActual === 'es' ? `Considera también: ${data.destino_titulo}` : `Also consider: ${data.destino_titulo_en || data.destino_titulo}`);
                }
            } catch (e) {
                console.error("Error fetching SALIR suggestion in CASA mode:", e);
            } finally {
                this.salidaSugeridaTimeoutId = null;
            }
        }, 180000);

        this.timerClinico = setInterval(() => {
            if (this.timeLeft > 0) this.timeLeft--;

            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
           
            if (pulmonDiv) {
                let ciclo = this.timeLeft % 8;
                if (ciclo >= 4) {
                    pulmonDiv.innerText = t.inspira.toUpperCase();
                    pulmonDiv.style.color = "var(--cyan-inhale)";
                } else {
                    pulmonDiv.innerText = t.expira.toUpperCase();
                    pulmonDiv.style.color = "var(--accent)";
                }
            }

            if (this.timeLeft < 600 && (600 - this.timeLeft) % 20 === 0 && (600 - this.timeLeft) !== 0) {
                let pasoAudioIdx = Math.floor((600 - this.timeLeft) / 20) - 1;
                if (pasoAudioIdx >= 0 && pasoAudioIdx < AUDIOS_SECUENCIALES_CASA.length) {
                    let recordatorioTexto = AUDIOS_SECUENCIALES_CASA[pasoAudioIdx];
                    if (recordatorioTexto) {
                        this.hablar(recordatorioTexto);
                    }
                }
            }

            if (this.timeLeft <= 0) {
                clearInterval(this.timerClinico);
                clearTimeout(this.salidaSugeridaTimeoutId);
                this.salidaSugeridaTimeoutId = null;
                window.speechSynthesis.cancel();
                if (circleElement) {
                    circleElement.style.animation = "none";
                    circleElement.style.transform = "scale(1)";
                }
                this.iniciarRetoCierre60Segundos();
            }
        }, 1000);
    },

    /** Advances to the next internal mission step. */
    avanzarPaso() {
        this.indiceMision++;
        const container = document.getElementById('wrapper-interactive');
        this.procesarFlujoSecuencial(container);
    },

    /**
     * Initiates the 60-second closing challenge phase.
     */
    iniciarRetoCierre60Segundos() {
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCierre);
        window.speechSynthesis.cancel();

        const t = {
            es: { logo: "OPEN THAN GO", cierreMensaje: "Gracias por tu presencia.", recomenzar: "RECOMENZAR EXPERIENCIA", puertaAbierta: "La puerta está abierta. ¿Continuamos?", retoInicial: "Prepárate para un reto combinado en 3, 2, 1..." },
            en: { logo: "OPEN THAN GO", cierreMensaje: "Thank you for your presence.", recomenzar: "RESTART EXPERIENCE", puertaAbierta: "The door is open. Shall we continue?", retoInicial: "Get ready for a combined challenge in 3, 2, 1..." }
        }[this.idiomaActual];

        const container = document.getElementById('wrapper-interactive');
        const cierrePantalla = document.getElementById('pantalla-cierre');
        const retoTitulo = document.getElementById('reto-titulo');
        const retoDescripcion = document.getElementById('reto-descripcion');
        const retoImg = document.getElementById('reto-img');
        const cierreTimer = document.getElementById('cierre-timer');
        const btnRecomenzar = document.getElementById('btn-recomenzar-experiencia');
        const cierreMensajeFinal = document.getElementById('cierre-mensaje-final');

        container.classList.add('hidden');
        cierrePantalla.classList.remove('hidden');
       
        cierreMensajeFinal.classList.add('hidden');
        btnRecomenzar.classList.add('hidden');
        btnRecomenzar.disabled = true;

        this.timeLeftCierre = 60;

        const catalogoRetos = this.idiomaActual === 'es' ? this.CATALOGO_RETOS_ES : this.CATALOGO_RETOS_EN;
       
        let secuenciaRetos = [];
        let numRetos = 3;
       
        let candidateSequenceIds;
        let sequenceString;
        let maxAttempts = 10;

        while(maxAttempts > 0) {
            secuenciaRetos = [];
            let tempRetos = [...catalogoRetos];
            for (let i = tempRetos.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [tempRetos[i], tempRetos[j]] = [tempRetos[j], tempRetos[i]];
            }

            for (let i = 0; i < numRetos; i++) {
                if (tempRetos.length === 0) break;
                secuenciaRetos.push(tempRetos.shift());
            }
           
            candidateSequenceIds = secuenciaRetos.map(r => r.id).sort((a, b) => a - b).join('-');
           
            if (!this.historialRetosSecuencias.includes(candidateSequenceIds)) {
                sequenceString = candidateSequenceIds;
                break;
            }
            maxAttempts--;
            if (maxAttempts === 0) {
                console.warn("Could not find a unique challenge sequence after multiple attempts, reusing one.");
                sequenceString = candidateSequenceIds;
            }
        }
       
        if (sequenceString) {
            this.historialRetosSecuencias.push(sequenceString);
            this.historialRetosSecuencias = this.historialRetosSecuencias.slice(-this.MAX_HISTORY_RETOS_SECUENCIAS);
            localStorage.setItem("otg_historial_retos_secuencias", JSON.stringify(this.historialRetosSecuencias));
        }

        let currentRetoIndex = 0;
        const displayNextReto = () => {
            if (currentRetoIndex < secuenciaRetos.length) {
                const reto = secuenciaRetos[currentRetoIndex];
                if (retoTitulo) retoTitulo.innerText = reto.titulo;
                if (retoDescripcion) retoDescripcion.innerText = reto.descripcion;
                if (retoImg) retoImg.src = `/static/${reto.img}`;
                this.hablar(reto.descripcion);
                currentRetoIndex++;
            }
        };

        this.hablar(t.retoInicial);
        setTimeout(() => {
            displayNextReto();
            this.temporizadorCierre = setInterval(() => {
                this.timeLeftCierre--;
                if (cierreTimer) cierreTimer.innerText = this.timeLeftCierre.toString().padStart(2, '0');

                if (this.timeLeftCierre > 0 && currentRetoIndex < numRetos && (this.timeLeftCierre % Math.floor(60 / numRetos) === 0)) {
                    displayNextReto();
                }

                if (this.timeLeftCierre <= 0) {
                    clearInterval(this.temporizadorCierre);
                    window.speechSynthesis.cancel();
                    if (retoTitulo) retoTitulo.innerText = "";
                    if (retoDescripcion) retoDescripcion.innerText = "";
                    if (retoImg) retoImg.src = "";
                   
                    // --- INJECTED CORPORATE REDIRECTION LOGIC ---
                    const zipIngresado = this.corporateSelectedZip;
                    const emocionActiva = this.corporateSelectedEmotion;
                    const entornoActivo = this.corporateSelectedEnvironment;
                    const presupuestoActivo = this.corporateSelectedBudget;

                    // Ensure default values in case of null/undefined from selectors, or mapping issues
                    const defaultEmocion = "Estresado";
                    const defaultEntorno = "CASA";
                    const defaultPresupuesto = "Gratis";
                    
                    const actualEmocion = DRIVER_MATRIX[emocionActiva] ? emocionActiva : defaultEmocion;
                    const actualEntorno = DRIVER_MATRIX[actualEmocion]?.[entornoActivo] ? entornoActivo : defaultEntorno;
                    const actualPresupuesto = DRIVER_MATRIX[actualEmocion]?.[actualEntorno]?.[presupuestoActivo] ? presupuestoActivo : defaultPresupuesto;
                    
                    const grupoEmpresas = DRIVER_MATRIX[actualEmocion][actualEntorno][actualPresupuesto];
                    const destinoElegido = grupoEmpresas[Math.floor(Math.random() * grupoEmpresas.length)];
                    
                    const estadoTraducido = calcularEstadoPorPostal(zipIngresado);
                    const ciudadTraducida = calcularCiudadPorPostal(zipIngresado);
                    
                    let urlResultado = destinoElegido.url
                        .replace(/{{ZIP}}/g, zipIngresado)
                        .replace(/{{STATE}}/g, estadoTraducido)
                        .replace(/{{CITY}}/g, ciudadTraducida);
                    
                    window.open(urlResultado, '_blank', 'noopener,noreferrer');
                    // Activa las microfrases robóticas continuas cada 15 segundos
                    motorAudioOTG.comenzarTerapiaAuditiva();
                    // --- END INJECTED CORPORATE REDIRECTION LOGIC ---

                    cierreTimer.classList.add('hidden');
                    cierreMensajeFinal.classList.remove('hidden');
                    btnRecomenzar.classList.remove('hidden');
                    btnRecomenzar.disabled = false;
                    // Delay speaking the final message to let audio therapy start without immediate interruption
                    setTimeout(() => {
                        this.hablar(t.puertaAbierta);
                    }, 1000);
                }
            }, 1000);
        }, 5000);

        btnRecomenzar.onclick = () => {
            this.reiniciarExperiencia();
        };
    },

    /**
     * Resets the UI to the initial form state without clearing persistent data.
     */
    reiniciarExperiencia() {
        clearInterval(this.timerInaccion);
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.temporizadorCierre);
        window.speechSynthesis.cancel();
        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }

        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        this.contadorToques = 0;

        document.getElementById('pantalla-cierre').classList.add('hidden');
        document.getElementById('wrapper-interactive').classList.add('hidden');
        document.getElementById('wrapper-form').classList.remove('hidden');
       
        document.getElementById('inp-text-libre').value = "";
        this.inyectarBloquePreguntas();
        this.activarBotonMandoLibreInicial();
       
        const saludos_es = ["Bienvenido de nuevo. Tu escape inteligente. Escucha mis preguntas en pantalla.", "Ópen Dán Go activo. Toca lo que sientes hoy para continuar."];
        const saludos_en = ["Welcome back. Your smart escape. Listen to my questions on screen.", "Open Than Go active. Tap what you feel today to continue."];
        const saludos = this.idiomaActual === 'es' ? saludos_es : saludos_en;
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
    },

    /**
     * Clears ALL session data and reloads the application.
     */
    destruirYReiniciar() {
        // Por último, localiza el evento de clic de tu botón 'SALIR' (btnSalirApp) e inserta la línea 'motorAudioOTG.cancelarTerapiaAuditiva();'
        motorAudioOTG.cancelarTerapiaAuditiva();
        
        clearInterval(this.timerInaccion);
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.temporizadorCierre);
        window.speechSynthesis.cancel();
        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }

        localStorage.clear();

        this.historialSalir = [];
        this.historialCasa = [];
        this.historialPreguntas = [];
        this.historialRetosSecuencias = [];
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        this.contadorToques = 0;

        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());

window.KERNEL = KERNEL;

// VARIABLES GLOBALES DE CONFIGURACIÓN Y CONTROL DE ESTADOS
let configuracion = {
    idioma: 'es',
    puedes_salir: true,
    bolsillo: 'cero'
};

// DICCIONARIO BILINGÜE PARA TRADUCCIÓN COMPLETA DE LA INTERFAZ
const textos = {
    es: {
        subtitle: "Tu botón de escape inmediato para romper la monotonía urbana.",
        lblState: "Estado / State:",
        lblZip: "ZIP Code (5 dígitos):",
        lblPocket: "¿Cuál es tu presupuesto real para hoy?",
        pocketCero: "GASTO $0 HOY",
        pocketMod: "MODERADO",
        pocketLibre: "PRESUPUESTO LIBRE",
        lblMode: "¿Puedes o quieres salir de casa hoy?",
        btnOut: "🟢 SÍ, NECESITO SALIR",
        btnIn: "🏠 NO, ME QUEDO EN CASA",
        lblText: "Desahógate aquí (Escribe libremente lo que traigas en la mente):",
        placeholder: "Escribe si estás cansado de la rutina, preocupado por biles o el trabajo, solo, o con niños aburridos...",
        btnSubmit: "SÁCAME DE LA MONOTONÍA",
        alertZip: "Por favor, ingresa un código postal (ZIP Code) válido de 5 dígitos.",
        alertError: "Ocurrió un inconveniente al conectar con el servidor de OPEN THAN GO. Inténtalo de nuevo.",
        btnMaps: "🗺️ ABRIR RUTA EN MI MAPA GRATIS"
    },
    en: {
        subtitle: "Your instant escape button to break free from urban monotony.",
        lblState: "State / Estado:",
        lblZip: "ZIP Code (5 digits):",
        lblPocket: "What is your real budget for today?",
        pocketCero: "$0 SPENDING TODAY",
        pocketMod: "MODERATE",
        pocketLibre: "OPEN BUDGET",
        lblMode: "Can you or do you want to leave the house today?",
        btnOut: "🟢 YES, I NEED TO GO OUT",
        btnIn: "🏠 NO, I'M STAYING HOME",
        lblText: "Vent here (Write freely whatever is on your mind):",
        placeholder: "Write if you are tired of the routine, worried about bills or work, alone, or with bored kids...",
        btnSubmit: "BREAK THE MONOTONY",
        alertZip: "Please enter a valid 5-digit ZIP Code.",
        alertError: "An issue occurred while connecting to the OPEN THAN GO server. Please try again.",
        btnMaps: "🗺️ OPEN ROUTE IN MY MAP FOR FREE"
    }
};

// CONTROLA EL INTERCAMBIO DE IDIOMA EN LA PANTALLA
function cambiarIdioma(nuevoIdioma) {
    configuracion.idioma = nuevoIdioma;
    
    // Cambiar estado activo visual de los botones de idioma
    document.getElementById('lang-es').classList.toggle('active', nuevoIdioma === 'es');
    document.getElementById('lang-en').classList.toggle('active', nuevoIdioma === 'en');
    
    // Inyección de textos traducidos de forma masiva
    const t = textos[nuevoIdioma];
    document.getElementById('txt-subtitle').innerText = t.subtitle;
    document.getElementById('lbl-state').innerText = t.lblState;
    document.getElementById('lbl-zip').innerText = t.lblZip;
    document.getElementById('lbl-pocket').innerText = t.lblPocket;
    document.getElementById('pocket-cero').innerText = t.pocketCero;
    document.getElementById('pocket-mod').innerText = t.pocketMod;
    document.getElementById('pocket-libre').innerText = t.pocketLibre;
    document.getElementById('lbl-mode').innerText = t.lblMode;
    document.getElementById('mode-out').innerText = t.btnOut;
    document.getElementById('mode-in').innerText = t.btnIn;
    document.getElementById('lbl-text').innerText = t.lblText;
    document.getElementById('inp-text').placeholder = t.placeholder;
    document.getElementById('btn-submit').innerText = t.btnSubmit;
    document.getElementById('res-maps').innerText = t.btnMaps;
    
    // Ocultar resultados previos para evitar discrepancias de traducción
    document.getElementById('result-box').style.display = 'none';
}

// ASIGNA EL PRESUPUESTO REAL SELECCIONADO (Cero, Moderado, Libre)
function setBolsillo(tipoBolsillo) {
    configuracion.bolsillo = tipoBolsillo;
    
    document.getElementById('pocket-cero').classList.toggle('active', tipoBolsillo === 'cero');
    document.getElementById('pocket-mod').classList.toggle('active', tipoBolsillo === 'moderado');
    document.getElementById('pocket-libre').classList.toggle('active', tipoBolsillo === 'libre');
}

// ASIGNA SI EL USUARIO TIENE CAPACIDAD DE SALIR O SE QUEDA EN CASA
function setModalidad(salir) {
    configuracion.puedes_salir = salir;
    document.getElementById('mode-out').classList.toggle('active', salir);
    document.getElementById('mode-in').classList.toggle('active', !salir);
    
    // Atenuar o iluminar el campo de código postal de acuerdo con la necesidad geográfica
    const campoZip = document.getElementById('inp-zip');
    if (!salir) {
        campoZip.style.opacity = '0.4';
        campoZip.disabled = true;
    } else {
        campoZip.style.opacity = '1';
        campoZip.disabled = false;
    }
}

// CONECTA LA INTERFAZ CON EL SERVIDOR PYTHON EN RENDER EN SEGUNDO PLANO
function ejecutarEscape() {
    const estado = document.getElementById('inp-state').value;
    const zip = document.getElementById('inp-zip').value.trim();
    const textoLibre = document.getElementById('inp-text').value.trim();
    const t = textos[configuracion.idioma];

    // Validación obligatoria del ZIP Code solo si requiere geolocalización exterior
    if (configuracion.puedes_salir && (zip.length !== 5 || isNaN(zip))) {
        alert(t.alertZip);
        return;
    }

    // Estructuración del paquete JSON definitivo
    const payload = {
        puedes_salir: configuracion.puedes_salir,
        idioma: configuracion.idioma,
        zip_code: zip,
        estado: estado,
        bolsillo: configuracion.bolsillo,
        texto_libre: textoLibre
    };

    // Envío asíncrono asumiendo el control de las peticiones concurrentes
    fetch('/diagnostico-kamizen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) throw new Error('Error de comunicación con Render');
        return response.json();
    })
    .then(data => {
        // Carga de la respuesta sorpresa en la tarjeta mística
        document.getElementById('res-title').innerText = data.titulo;
        document.getElementById('res-location').innerText = data.lugar;
        document.getElementById('res-steps').innerText = data.instrucciones;

        const btnMaps = document.getElementById('res-maps');
        
        // DEEP LINKING GRATUITO: Activa el enlace solo si se requiere ruta física
        if (data.modalidad === 'outdoor' && data.url_maps) {
            btnMaps.href = data.url_maps;
            btnMaps.style.display = 'block';
        } else {
            btnMaps.style.display = 'none';
        }

        // Mostrar la tarjeta y generar el desplazamiento suave de pantalla
        const resultBox = document.getElementById('result-box');
        resultBox.style.display = 'block';
        resultBox.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        console.error('Error del sistema:', error);
        alert(t.alertError);
    });
}

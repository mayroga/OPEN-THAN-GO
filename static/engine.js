// VARIABLES GLOBALES DE CONTROL
let configuracion = {
    idioma: 'es',
    puedes_salir: true
};

// DICCIONARIO BILINGÜE OBLIGATORIO PARA LA INTERFAZ
const textos = {
    es: {
        subtitle: "Tu botón de escape inmediato para romper la monotonía urbana.",
        lblState: "Estado / State:",
        lblZip: "ZIP Code (5 dígitos):",
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

// FUNCIÓN PARA INTERCAMBIAR EL IDIOMA DE LA PANTALLA
function cambiarIdioma(nuevoIdioma) {
    configuracion.idioma = nuevoIdioma;
    
    // Actualizar estados visuales de los botones de idioma
    document.getElementById('lang-es').classList.toggle('active', nuevoIdioma === 'es');
    document.getElementById('lang-en').classList.toggle('active', nuevoIdioma === 'en');
    
    // Traducir todos los elementos de la interfaz en tiempo real
    const t = textos[nuevoIdioma];
    document.getElementById('txt-subtitle').innerText = t.subtitle;
    document.getElementById('lbl-state').innerText = t.lblState;
    document.getElementById('lbl-zip').innerText = t.lblZip;
    document.getElementById('lbl-mode').innerText = t.lblMode;
    document.getElementById('mode-out').innerText = t.btnOut;
    document.getElementById('mode-in').innerText = t.btnIn;
    document.getElementById('lbl-text').innerText = t.lblText;
    document.getElementById('inp-text').placeholder = t.placeholder;
    document.getElementById('btn-submit').innerText = t.btnSubmit;
    document.getElementById('res-maps').innerText = t.btnMaps;
    
    // Limpiar caja de resultados si cambia el idioma para evitar textos cruzados
    document.getElementById('result-box').style.display = 'none';
}

// FUNCIÓN PARA SELECCIONAR SI SE QUEDA EN CASA O SALE
function setModalidad(salir) {
    configuracion.puedes_salir = salir;
    document.getElementById('mode-out').classList.toggle('active', salir);
    document.getElementById('mode-in').classList.toggle('active', !salir);
    
    // Si decide quedarse en casa, el ZIP code no es obligatorio visualmente
    if (!salir) {
        document.getElementById('inp-zip').style.opacity = '0.5';
    } else {
        document.getElementById('inp-zip').style.opacity = '1';
    }
}

// FUNCIÓN PRINCIPAL: ENVÍA LOS DATOS A PYTHON EN RENDER
function ejecutarEscape() {
    const estado = document.getElementById('inp-state').value;
    const zip = document.getElementById('inp-zip').value.trim();
    const textoLibre = document.getElementById('inp-text').value.trim();
    const t = textos[configuracion.idioma];

    // Validación estricta del ZIP Code solo si el usuario seleccionó que quiere salir
    if (configuracion.puedes_salir && (zip.length !== 5 || isNaN(zip))) {
        alert(t.alertZip);
        return;
    }

    // Preparar el paquete de datos estructurado
    const payload = {
        puedes_salir: configuracion.puedes_salir,
        idioma: configuracion.idioma,
        zip_code: zip,
        estado: estado,
        texto_libre: textoLibre
    };

    // Petición POST asíncrona hacia el Backend en Render
    fetch('/diagnostico-kamizen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
    })
    .then(data => {
        // Inyectar los datos de la sorpresa en la tarjeta mística
        document.getElementById('res-title').innerText = data.titulo;
        document.getElementById('res-location').innerText = data.lugar;
        document.getElementById('res-steps').innerText = data.instrucciones;

        const btnMaps = document.getElementById('res-maps');
        
        // DEEP LINKING GRATUITO: Activar mapa solo si es modalidad exterior
        if (data.modalidad === 'outdoor' && data.url_maps) {
            btnMaps.href = data.url_maps;
            btnMaps.style.display = 'block';
        } else {
            btnMaps.style.display = 'none';
        }

        // Mostrar la tarjeta y hacer scroll suave hacia abajo
        const resultBox = document.getElementById('result-box');
        resultBox.style.display = 'block';
        resultBox.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        console.error('Error:', error);
        alert(t.alertError);
    });
}

let configuracion = { 
    idioma: 'es', 
    puedes_salir: true, 
    bolsillo: 'cero' 
};
let comandosMision = [];
let indiceActual = 0;
let intervaloRespiracion = null;
let cuentaRegresiva = null;

const textos = {
    es: {
        subtitle: "Tu botón de escape inmediato para romper la monotonía urbana.",
        lblState: "Estado / State:", 
        lblZip: "ZIP Code (5 dígitos):", 
        lblPocket: "¿Cuál es tu presupuesto real para hoy?",
        pocketCero: "GASTO $0 HOY", 
        pocketMod: "MODERADO", 
        pocketLibre: "LIBRE",
        lblMode: "¿Puedes o quieres salir de casa hoy?", 
        btnOut: "🟢 SÍ, SALIR", 
        btnIn: "🏠 EN CASA",
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
        pocketCero: "$0 SPENDING", 
        pocketMod: "MODERATE", 
        pocketLibre: "FREE BUDGET",
        lblMode: "Can you or do you want to leave the house today?", 
        btnOut: "🟢 YES, GO OUT", 
        btnIn: "🏠 STAY HOME",
        lblText: "Vent here (Write freely whatever is on your mind):",
        placeholder: "Write if you are tired of the routine, worried about bills or work, alone, or with bored kids...",
        btnSubmit: "BREAK THE MONOTONY", 
        alertZip: "Please enter a valid 5-digit ZIP Code.",
        alertError: "An issue occurred while connecting to the OPEN THAN GO server. Please try again.",
        btnMaps: "🗺️ OPEN ROUTE IN MY MAP FOR FREE"
    }
};

function cambiarIdioma(nuevoIdioma) {
    configuracion.idioma = nuevoIdioma;
    document.getElementById('lang-es').classList.toggle('active', nuevoIdioma === 'es');
    document.getElementById('lang-en').classList.toggle('active', nuevoIdioma === 'en');
    
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
    document.getElementById('result-box').style.display = 'none';
}

function setBolsillo(tipoBolsillo) {
    configuracion.bolsillo = tipoBolsillo;
    document.getElementById('pocket-cero').classList.toggle('active', tipoBolsillo === 'cero');
    document.getElementById('pocket-mod').classList.toggle('active', tipoBolsillo === 'moderado');
    document.getElementById('pocket-libre').classList.toggle('active', tipoBolsillo === 'libre');
}

function setModalidad(salir) {
    configuracion.puedes_salir = salir;
    document.getElementById('mode-out').classList.toggle('active', salir);
    document.getElementById('mode-in').classList.toggle('active', !salir);
    
    const campoZip = document.getElementById('inp-zip');
    if (!salir) {
        campoZip.style.opacity = '0.4';
        campoZip.disabled = true;
    } else {
        campoZip.style.opacity = '1';
        campoZip.disabled = false;
    }
}

function ejecutarEscape() {
    const estado = document.getElementById('inp-state').value;
    const zip = document.getElementById('inp-zip').value.trim();
    const textoLibre = document.getElementById('inp-text').value.trim();
    const t = textos[configuracion.idioma];

    if (configuracion.puedes_salir && (zip.length !== 5 || isNaN(zip))) {
        alert(t.alertZip);
        return;
    }

    const payload = {
        puedes_salir: configuracion.puedes_salir,
        idioma: configuracion.idioma,
        zip_code: zip,
        estado: estado,
        bolsillo: configuracion.bolsillo,
        texto_libre: textoLibre
    };

    fetch('/diagnostico-kamizen', {
        method: 'POST',
        headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // Ocultamos el formulario inicial y encendemos el panel interactivo
        document.getElementById('wrapper-form').style.display = 'none';
        const panelInteractivo = document.getElementById('wrapper-interactive');
        panelInteractivo.style.display = 'block';

        document.getElementById('interactive-title').innerText = data.titulo;
        document.getElementById('interactive-location').innerText = data.lugar;

        // Almacenamos los comandos estructurados de los JSON
        comandosMision = data.bloques_interactivos || [];
        indiceActual = 0;

        // Configuramos la acción final del mapa si la modalidad es calle
        const btnMaps = document.getElementById('btn-maps-action');
        if (data.modalidad === 'outdoor' && data.url_maps) {
            btnMaps.href = data.url_maps;
            btnMaps.style.display = 'block';
        } else {
            btnMaps.style.display = 'none';
        }

        // Iniciamos la ejecución paso a paso en el celular
        procesarComando();
    })
    .catch(error => {
        console.error('Error detectado:', error);
        alert(t.alertError);
    });
}

// MOTOR DE FLUJO SECUENCIAL INTERACTIVO
function procesarComando() {
    // Apagar todos los cronómetros y ciclos anteriores de inmediato
    clearInterval(intervaloRespiracion);
    clearInterval(cuentaRegresiva);

    const cajaContenedora = document.getElementById('step-content');
    const btnSiguiente = document.getElementById('btn-next');
    
    cajaContenedora.innerHTML = "";
    btnSiguiente.style.display = 'none';

    // Verificación de fin de curso
    if (indiceActual >= comandosMision.length) {
        cajaContenedora.innerHTML = `<div class='screen-story' style='text-align:center; font-weight:bold;'>¡Misión Completada con Éxito! Disfruta tu bienestar. / Mission Accomplished!</div>`;
        return;
    }

    const c = comandosMision[indiceActual];

    // ACCIÓN 1: Textos fijos, Historias o Conclusiones (v, h, story, c)
    if (c.t === 'v' || c.t === 'h' || c.story || c.t === 'c') {
        let mensaje = c.tx || c.story || c.c || "";
        cajaContenedora.innerHTML = `<div class='screen-story'>${mensaje}</div>`;
        btnSiguiente.style.display = 'block';
    }

    // ACCIÓN 2: Círculo Respiratorio Azul Animado (breath_auto)
    else if (c.t === 'breath_auto') {
        cajaContenedora.innerHTML = `
            <div class='screen-story'><b>${c.tx}</b><br><small style='color:var(--secondary);'>${c.inf || ''}</small></div>
            <div class='wrapper-circle'>
                <div id='circle-azul' class='breath-circle'>INHALA</div>
            </div>
            <div id='timer-breath' class='timer-display'>${c.d}s</div>
        `;

        let segundos = c.d;
        const circulo = document.getElementById('circle-azul');
        const contador = document.getElementById('timer-breath');
        
        let modoExpansion = true;
        circulo.classList.add('expand');
        circulo.innerText = configuracion.idioma === 'es' ? "INHALA" : "BREATHE IN";

        // Ciclo somático cada 4 segundos exactos
        intervaloRespiracion = setInterval(() => {
            modoExpansion = !modoExpansion;
            if (modoExpansion) {
                circulo.className = 'breath-circle expand';
                circulo.innerText = configuracion.idioma === 'es' ? "INHALA" : "BREATHE IN";
            } else {
                circulo.className = 'breath-circle contract';
                circulo.innerText = configuracion.idioma === 'es' ? "EXHALA" : "BREATHE OUT";
            }
        }, 4000);

        cuentaRegresiva = setInterval(() => {
            segundos--;
            contador.innerText = `${segundos}s`;
            if (segundos <= 0) {
                clearInterval(intervaloRespiracion);
                clearInterval(cuentaRegresiva);
                btnSiguiente.style.display = 'block';
            }
        }, 1000);
    }

    // ACCIÓN 3: Retos de Entrenamiento Mental en Silencio (sil)
    else if (c.t === 'sil') {
        cajaContenedora.innerHTML = `
            <div class='screen-story'><b>${c.tx}</b><br><small style='color:var(--accent);'>${c.inf || ''}</small></div>
            <div id='timer-silence' class='timer-display' style='color:var(--accent);'>${c.d}s</div>
        `;

        let segundos = c.d;
        const contador = document.getElementById('timer-silence');

        cuentaRegresiva = setInterval(() => {
            segundos--;
            contador.innerText = `${segundos}s`;
            if (segundos <= 0) {
                clearInterval(cuentaRegresiva);
                btnSiguiente.style.display = 'block';
            }
        }, 1000);
    }


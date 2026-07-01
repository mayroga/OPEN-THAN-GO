let configuracion = {
    idioma: 'es',
    puedes_salir: true,
    bolsillo: 'cero'
};
let comandosMision = [];
let indiceActual = 0;
let intervaloRespiracion = null;
let cuentaRegresiva = null;

// ... (El objeto 'textos' se mantiene igual)

function cambiarIdioma(nuevoIdioma) {
    configuracion.idioma = nuevoIdioma;
    // ... (Tu lógica de cambio de idioma)
}

// ... (Funciones cambiarBolsillo y cambiarModalidad igual)

function solicitarEscape() {
    // ... (Tu lógica de fetch y manejo de datos)
}

// ÚNICA DEFINICIÓN DE LA FUNCIÓN PROCESARCOMANDO
function procesarComando() {
    clearInterval(intervaloRespiracion);
    clearInterval(cuentaRegresiva);
    const cajaContenedora = document.getElementById('step-content');
    const btnSiguiente = document.getElementById('btn-next');
   
    cajaContenedora.innerHTML = "";
    btnSiguiente.style.display = 'none';

    if (indiceActual >= comandosMision.length) {
        cajaContenedora.innerHTML = `<div class='screen-story' style='text-align:center; font-weight:bold;'>¡Misión Completada! / Mission Accomplished!</div>`;
        return;
    }

    const c = comandosMision[indiceActual];

    // Lógica para tipos de pantalla
    if (c.t === 'v' || c.t === 'h' || c.story || c.t === 'c') {
        cajaContenedora.innerHTML = `<div class='screen-story'>${c.tx || c.story || c.c || ""}</div>`;
        btnSiguiente.style.display = 'block';
    }
    else if (c.t === 'breath_auto') {
        cajaContenedora.innerHTML = `<div class='screen-story'><b>${c.tx}</b></div><div class='wrapper-circle'><div id='circle-azul' class='breath-circle'>INHALA</div></div><div id='timer-breath' class='timer-display'>${c.d}s</div>`;
        // ... (Aquí va tu lógica de intervalos de respiración)
    }
    else if (c.t === 'sil') {
        cajaContenedora.innerHTML = `<div class='screen-story'><b>${c.tx}</b></div><div id='timer-silence' class='timer-display'>${c.d}s</div>`;
        // ... (Aquí va tu lógica de intervalos de silencio)
    }
    else if (c.t === 'd') {
        let opcionesHtml = "";
        c.op.forEach((opcion, idx) => {
            opcionesHtml += `<button class='btn-option-interactive' onclick='validarRespuesta(${idx}, ${c.c}, "${c.ex[idx].replace(/"/g, '&quot;')}")'>${opcion}</button>`;
        });
        cajaContenedora.innerHTML = `<div class='screen-title'>${c.q}</div><div class='options-list'>${opcionesHtml}</div><div id='box-explicacion' class='explanation-box'></div>`;
    }
    else {
        indiceActual++;
        procesarComando();
    }
}

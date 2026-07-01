let estado = {
    datos: null,
    indice: 0,
    bloque: 0,
    ejecutando: false,
    timerSesion: null,
    tiempoRestante: 600, // 10 minutos exactos
    intervalo: null,
    respiracion: null,
    usados: new Set()
};

const ui = {
    titulo: document.getElementById("titulo"),
    subtitulo: document.getElementById("subtitulo"),
    contenedor: document.getElementById("contenedor"),
    circulo: document.getElementById("circulo"),
    timer: document.getElementById("timer")
};

//
// ===============================
// INICIO DE SESION
// ===============================
//
function iniciarSesion(datos) {
    estado.datos = datos;
    estado.indice = 0;
    estado.bloque = 0;
    estado.usados.clear();

    iniciarTimerGlobal();
    ejecutarSiguienteBloque();
}

//
// ===============================
// TIMER GLOBAL 10 MINUTOS
// ===============================
//
function iniciarTimerGlobal() {
    clearInterval(estado.timerSesion);

    estado.tiempoRestante = 600;

    estado.timerSesion = setInterval(() => {
        estado.tiempoRestante--;

        actualizarTimerUI();

        if (estado.tiempoRestante <= 0) {
            finalizarSesion();
        }
    }, 1000);
}

function actualizarTimerUI() {
    const min = Math.floor(estado.tiempoRestante / 60);
    const sec = estado.tiempoRestante % 60;

    ui.timer.innerText = `${min}:${sec < 10 ? "0" : ""}${sec}`;
}

function finalizarSesion() {
    clearInterval(estado.timerSesion);
    clearInterval(estado.intervalo);
    cancelarRespiracion();

    ui.contenedor.innerHTML = `
        <div class="end-screen">
            <h2>Sesión completada</h2>
            <button onclick="reiniciarSesion()">Reiniciar</button>
        </div>
    `;
}

function reiniciarSesion() {
    location.reload();
}

//
// ===============================
// LOOP PRINCIPAL DE BLOQUES
// ===============================
//
function ejecutarSiguienteBloque() {
    if (!estado.datos) return;

    const bloques = estado.datos.bloques_interactivos;

    if (estado.bloque >= bloques.length) {
        estado.indice++;
        estado.bloque = 0;

        if (estado.indice >= bloques.length) {
            estado.indice = 0;
        }
    }

    const bloque = bloques[estado.bloque];
    estado.bloque++;

    procesarBloque(bloque);
}

//
// ===============================
// MOTOR DE BLOQUES
// ===============================
//
function procesarBloque(bloque) {

    switch (bloque.t) {

        case "v":
            mostrarTitulo(bloque.tx);
            setTimeout(ejecutarSiguienteBloque, 2000);
            break;

        case "h":
            mostrarSubtitulo(bloque.tx);
            setTimeout(ejecutarSiguienteBloque, 4000);
            break;

        case "story":
            mostrarTexto(bloque);
            setTimeout(ejecutarSiguienteBloque, 6000);
            break;

        case "breath_auto":
            iniciarRespiracion(bloque.d);
            setTimeout(() => {
                cancelarRespiracion();
                ejecutarSiguienteBloque();
            }, bloque.d * 1000);
            break;

        case "d":
            mostrarDecision(bloque);
            break;

        case "r":
            mostrarRecompensa(bloque);
            setTimeout(ejecutarSiguienteBloque, 2000);
            break;

        case "c":
            mostrarConfirmacion(bloque);
            setTimeout(ejecutarSiguienteBloque, 2000);
            break;

        case "sil":
            iniciarSilencio(bloque);
            break;

        default:
            ejecutarSiguienteBloque();
    }
}

//
// ===============================
// UI HELPERS
// ===============================
//
function mostrarTitulo(texto) {
    ui.titulo.innerText = texto;
}

function mostrarSubtitulo(texto) {
    ui.subtitulo.innerText = texto;
}

function mostrarTexto(bloque) {
    ui.contenedor.innerHTML = `<p>${bloque.tx || ""}</p>`;
}

//
// ===============================
// RESPIRACION REAL ANIMADA
// ===============================
//
function iniciarRespiracion(duracion) {
    let expandiendo = true;
    let escala = 1;

    clearInterval(estado.intervalo);

    estado.intervalo = setInterval(() => {

        if (expandiendo) {
            escala += 0.01;
            if (escala >= 1.4) expandiendo = false;
        } else {
            escala -= 0.01;
            if (escala <= 1) expandiendo = true;
        }

        ui.circulo.style.transform = `scale(${escala})`;

    }, 16); // ~60fps
}

function cancelarRespiracion() {
    clearInterval(estado.intervalo);
    ui.circulo.style.transform = "scale(1)";
}

//
// ===============================
// DECISIONES
// ===============================
//
function mostrarDecision(bloque) {
    let html = `<h3>${bloque.q}</h3>`;

    bloque.op.forEach((op, index) => {
        html += `<button onclick="responder(${index}, ${bloque.c})">${op}</button>`;
    });

    ui.contenedor.innerHTML = html;
}

function responder(index, correcta) {

    if (index === correcta) {
        ui.contenedor.innerHTML += `<p>✔ Correcto</p>`;
    } else {
        ui.contenedor.innerHTML += `<p>✖ Ajuste necesario</p>`;
    }

    setTimeout(ejecutarSiguienteBloque, 1500);
}

//
// ===============================
// SILENCIO CRONOMETRADO
// ===============================
//
function iniciarSilencio(bloque) {

    let tiempo = bloque.d;
    ui.contenedor.innerHTML = `<h3>Silencio activo</h3><div id="silencioTimer">${tiempo}</div>`;

    const intervalo = setInterval(() => {

        tiempo--;
        document.getElementById("silencioTimer").innerText = tiempo;

        if (tiempo <= 0) {
            clearInterval(intervalo);
            ejecutarSiguienteBloque();
        }

    }, 1000);
}

//
// ===============================
// RECOMPENSAS / CONFIRMACION
// ===============================
//
function mostrarRecompensa(bloque) {
    ui.contenedor.innerHTML = `<p>${bloque.tx}</p>`;
}

function mostrarConfirmacion(bloque) {
    ui.contenedor.innerHTML = `<p>${bloque.tx}</p>`;
}

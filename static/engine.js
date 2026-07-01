let estado = {
    datos: null,
    bloque: 0,
    ejecutando: false,

    timerSesion: null,
    tiempoRestante: 600,

    intervaloRespiracion: null,
    watchdog: null,

    ultimoTick: Date.now()
};


// ===============================
// INICIO SEGURO
// ===============================
function iniciarSesion(datos) {

    if (!datos || !Array.isArray(datos.bloques_interactivos)) {
        console.error("❌ Datos inválidos del backend");
        return;
    }

    estado.datos = datos;
    estado.bloque = 0;

    iniciarTimerGlobal();
    iniciarWatchdog();
    ejecutarSiguienteBloque();
}


// ===============================
// WATCHDOG (ANTI FREEZE)
// ===============================
function iniciarWatchdog() {

    clearInterval(estado.watchdog);

    estado.watchdog = setInterval(() => {

        const ahora = Date.now();
        const diff = ahora - estado.ultimoTick;

        // si no hay actividad en 8 segundos → recuperación
        if (diff > 8000) {
            console.warn("⚠️ Freeze detectado → recuperando loop");
            ejecutarSiguienteBloque();
        }

    }, 3000);
}


// ===============================
// TIMER GLOBAL 10 MIN
// ===============================
function iniciarTimerGlobal() {

    clearInterval(estado.timerSesion);

    estado.tiempoRestante = 600;

    estado.timerSesion = setInterval(() => {

        estado.tiempoRestante--;
        actualizarTimer();

        if (estado.tiempoRestante <= 0) {
            finalizarSesion();
        }

    }, 1000);
}

function actualizarTimer() {
    const el = document.getElementById("timer");
    if (!el) return;

    const m = Math.floor(estado.tiempoRestante / 60);
    const s = estado.tiempoRestante % 60;

    el.innerText = `${m}:${s < 10 ? "0" : ""}${s}`;
}


// ===============================
// LOOP PRINCIPAL SEGURO
// ===============================
function ejecutarSiguienteBloque() {

    estado.ultimoTick = Date.now();

    if (!estado.datos || !estado.datos.bloques_interactivos) {
        console.error("❌ Sin datos");
        return;
    }

    const bloques = estado.datos.bloques_interactivos;

    // si índice fuera de rango → reset seguro
    if (estado.bloque >= bloques.length) {
        estado.bloque = 0;
    }

    const bloque = bloques[estado.bloque];
    estado.bloque++;

    procesarBloqueSeguro(bloque);
}


// ===============================
// MOTOR ROBUSTO
// ===============================
function procesarBloqueSeguro(bloque) {

    estado.ultimoTick = Date.now();

    // 🛡 VALIDACIÓN CRÍTICA
    if (!bloque || typeof bloque !== "object" || !bloque.t) {
        console.warn("⚠️ Bloque inválido, saltando...");
        setTimeout(ejecutarSiguienteBloque, 200);
        return;
    }

    try {

        switch (bloque.t) {

            case "v":
                renderTitulo(bloque.tx);
                delay(1500);
                break;

            case "h":
                renderSubtitulo(bloque.tx);
                delay(2500);
                break;

            case "story":
                renderTexto(bloque.tx);
                delay(4000);
                break;

            case "breath_auto":
                iniciarRespiracion(bloque.d || 20);
                setTimeout(() => {
                    detenerRespiracion();
                    ejecutarSiguienteBloque();
                }, (bloque.d || 20) * 1000);
                break;

            case "d":
                renderDecision(bloque);
                break;

            case "r":
                renderSimple(bloque.tx);
                delay(1500);
                break;

            case "c":
                renderSimple(bloque.tx);
                delay(1500);
                break;

            case "sil":
                iniciarSilencioSeguro(bloque.d || 30);
                break;

            default:
                console.warn("⚠️ Tipo desconocido:", bloque.t);
                delay(500);
        }

    } catch (e) {
        console.error("🔥 Error en bloque:", e);
        delay(300);
    }
}


// ===============================
// SAFE DELAY
// ===============================
function delay(ms) {
    setTimeout(() => {
        ejecutarSiguienteBloque();
    }, ms);
}


// ===============================
// RESPIRACION SEGURA (ANTI FREEZE)
// ===============================
function iniciarRespiracion(duracion) {

    detenerRespiracion();

    const circulo = document.getElementById("circulo");
    if (!circulo) return;

    let scale = 1;
    let up = true;

    estado.intervaloRespiracion = setInterval(() => {

        if (!circulo) return;

        if (up) {
            scale += 0.02;
            if (scale >= 1.35) up = false;
        } else {
            scale -= 0.02;
            if (scale <= 1) up = true;
        }

        circulo.style.transform = `scale(${scale})`;

    }, 16);
}

function detenerRespiracion() {
    clearInterval(estado.intervaloRespiracion);

    const circulo = document.getElementById("circulo");
    if (circulo) circulo.style.transform = "scale(1)";
}


// ===============================
// SILENCIO SEGURO
// ===============================
function iniciarSilencioSeguro(segundos) {

    const cont = document.getElementById("contenedor");
    if (!cont) return;

    let t = segundos;

    cont.innerHTML = `<h3>Silencio activo</h3><h2 id="silencio">${t}</h2>`;

    const intv = setInterval(() => {

        t--;
        const el = document.getElementById("silencio");

        if (el) el.innerText = t;

        if (t <= 0) {
            clearInterval(intv);
            ejecutarSiguienteBloque();
        }

    }, 1000);
}


// ===============================
// RENDER BÁSICO SEGURO
// ===============================
function renderTitulo(t) {
    const el = document.getElementById("titulo");
    if (el) el.innerText = t || "";
}

function renderSubtitulo(t) {
    const el = document.getElementById("subtitulo");
    if (el) el.innerText = t || "";
}

function renderTexto(t) {
    const el = document.getElementById("contenedor");
    if (el) el.innerHTML = `<p>${t || ""}</p>`;
}

function renderSimple(t) {
    renderTexto(t);
}


// ===============================
// DECISIONES SEGURAS
// ===============================
function renderDecision(b) {

    const cont = document.getElementById("contenedor");
    if (!cont) return;

    let html = `<h3>${b.q || ""}</h3>`;

    (b.op || []).forEach((op, i) => {
        html += `<button onclick="resolverDecision(${i}, ${b.c})">${op}</button>`;
    });

    cont.innerHTML = html;
}

function resolverDecision(i, correcta) {

    const cont = document.getElementById("contenedor");

    if (i === correcta) {
        cont.innerHTML += `<p>✔</p>`;
    } else {
        cont.innerHTML += `<p>✖</p>`;
    }

    setTimeout(ejecutarSiguienteBloque, 1200);
}


// ===============================
// FINALIZACION SEGURA
// ===============================
function finalizarSesion() {

    clearInterval(estado.timerSesion);
    clearInterval(estado.watchdog);

    detenerRespiracion();

    const cont = document.getElementById("contenedor");

    if (cont) {
        cont.innerHTML = `
            <div>
                <h2>Sesión completada</h2>
                <button onclick="location.reload()">Reiniciar</button>
            </div>
        `;
    }
}

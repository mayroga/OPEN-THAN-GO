// OPEN THAN GO SYSTEM - Frontend Engine v3 (OPTIMIZED + ENHANCED)
// Company: May Roga LLC

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";
let intervaloRespiracion = null;
let timerCasa = null;

// ------------------------------
// UTILS (FAST + SAFE)
// ------------------------------
const $ = (id) => document.getElementById(id);

const speak = (text) => {
    try {
        if (!("speechSynthesis" in window)) return;
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
        u.rate = 1;
        window.speechSynthesis.speak(u);
    } catch (e) {}
};

const show = (id, mode = "block") => {
    const el = $(id);
    if (el) el.style.display = mode;
};

const hide = (id) => {
    const el = $(id);
    if (el) el.style.display = "none";
};

// ------------------------------
// TRADUCCIONES
// ------------------------------
const t = {
    es: {
        inhale: "Inhala",
        exhale: "Exhala",
        continue: "CONTINUAR",
        finish: "FINALIZAR",
        restart: "REINICIAR",
        exit: "SALIR",
        loading: "Calculando...",
        intro_q1: "¿Qué necesitas ahora mismo?",
        intro_q2: "¿Quieres calma, energía o desconexión?",
        intro_q3: "¿Nivel de estrés (1-10)?"
    },
    en: {
        inhale: "Inhale",
        exhale: "Exhale",
        continue: "CONTINUE",
        finish: "FINISH",
        restart: "RESTART",
        exit: "EXIT",
        loading: "Calculating...",
        intro_q1: "What do you need right now?",
        intro_q2: "Calm, energy or disconnection?",
        intro_q3: "Stress level (1-10)?"
    }
};

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const btn = $("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// ------------------------------
// IDIOMA
// ------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;
}

// ------------------------------
// PRESUPUESTO
// ------------------------------
function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;
}

// ------------------------------
// MODALIDAD
// ------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;
}

// ------------------------------
// ZIP PRIORITY FIX (STATE CONSISTENCY)
// ------------------------------
function resolverUbicacion() {
    const zip = $("inp-zip")?.value?.trim();
    const state = $("inp-state")?.value?.trim();
    const region = $("inp-region")?.value?.trim();

    // ZIP always wins
    if (zip) return { zip_code: zip, region: "", estado: state };

    return { zip_code: "", region, estado: state };
}

// ------------------------------
// INTRO QUESTIONS (NEW FEATURE)
// ------------------------------
function mostrarIntroPreguntas() {
    return new Promise((resolve) => {
        const cont = $("step-content");
        if (!cont) return resolve();

        let i = 0;
        const qs = [
            t[idiomaActual].intro_q1,
            t[idiomaActual].intro_q2,
            t[idiomaActual].intro_q3
        ];

        cont.innerHTML = `<h3>${qs[i]}</h3><input id="intro_input" style="width:100%;padding:10px;margin-top:10px;">`;

        const next = document.createElement("button");
        next.innerText = "OK";
        next.style.width = "100%";
        next.onclick = () => {
            i++;
            const val = $("intro_input")?.value || "";
            if (i >= qs.length) return resolve(val);
            cont.innerHTML = `<h3>${qs[i]}</h3><input id="intro_input" style="width:100%;padding:10px;margin-top:10px;">`;
            cont.appendChild(next);
        };

        cont.appendChild(next);
    });
}

// ------------------------------
// MAIN CALL
// ------------------------------
async function solicitarEscape() {

    // INTRO FLOW (lightweight, non-blocking UX)
    await mostrarIntroPreguntas();

    const loc = resolverUbicacion();

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: loc.zip_code,
        estado: loc.estado,
        region: loc.region,
        desahogo: $("inp-text")?.value || ""
    };

    hide("wrapper-form");
    show("wrapper-loader", "flex");
    hide("wrapper-interactive");

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || data.status !== "success") throw new Error();

        setTimeout(() => {
            hide("wrapper-loader");
            show("wrapper-interactive");

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || "";

            indicePasoActual = 0;

            procesarPaso();
        }, 600);

    } catch (e) {
        hide("wrapper-loader");
        show("wrapper-form");
    }
}

// ------------------------------
// BREATHING CIRCLE (24–26s, SMOOTH)
// ------------------------------
function breathingCycle(duration = 25000) {
    const circle = $("breathingCircle");
    if (!circle) return;

    let start = Date.now();

    intervaloRespiracion = setInterval(() => {
        let t = (Date.now() - start) / duration;

        let scale = 1 + Math.sin(t * Math.PI * 2) * 0.3;

        circle.style.transform = `scale(${scale})`;
        circle.style.background = `rgba(120,200,255,${0.4 + scale / 3})`;

        if (t >= 1) {
            clearInterval(intervaloRespiracion);
        }
    }, 50);
}

// ------------------------------
// TIMER CASA (10 MIN)
// ------------------------------
function startCasaTimer() {
    let time = 600;
    const cont = $("step-content");

    timerCasa = setInterval(() => {
        let min = Math.floor(time / 60);
        let sec = time % 60;

        if (cont) {
            cont.innerHTML = `<h2>${min}:${sec.toString().padStart(2, "0")}</h2>`;
        }

        if (time <= 0) {
            clearInterval(timerCasa);
            endScreen();
        }

        time--;
    }, 1000);
}

// ------------------------------
// END SCREEN
// ------------------------------
function endScreen() {
    const cont = $("step-content");
    if (!cont) return;

    cont.innerHTML = `
        <h2>${tipoEscapeGlobal === "Casa" ? "Sesión finalizada" : "Experiencia completada"}</h2>
        <button onclick="location.reload()">${t[idiomaActual].restart}</button>
        <button onclick="window.close?.()">${t[idiomaActual].exit}</button>
    `;
}

// ------------------------------
// ENGINE FLOW
// ------------------------------
function procesarPaso() {

    clearInterval(intervaloRespiracion);
    window.speechSynthesis.cancel();

    const cont = $("step-content");
    const btn = $("btn-next");
    const map = $("btn-maps-action");

    if (!cont) return;

    if (indicePasoActual >= pasosMisionGlobal.length) {

        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal?.gps_link) {
            map.href = datosLugarGlobal.gps_link;
            show("btn-maps-action");
        } else {
            endScreen();
        }
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    const nextStep = () => {
        indicePasoActual++;
        procesarPaso();
    };

    if (btn) {
        btn.onclick = nextStep;
        btn.innerText = t[idiomaActual].continue;
        show("btn-next");
    }

    // STORY
    if (paso.story) {
        cont.innerHTML = `<div>${paso.story[idiomaActual] || ""}</div>`;
        speak(paso.story[idiomaActual] || "");
        return;
    }

    // BREATHING STEP
    if (paso.t === "breath_auto") {
        cont.innerHTML = `
            <h2>${t[idiomaActual].inhale} / ${t[idiomaActual].exhale}</h2>
            <div id="breathingCircle"></div>
        `;
        breathingCycle(25000);
        speak("Respiración guiada");
        return;
    }

    // SILENCE CHALLENGE
    if (paso.t === "silence") {
        cont.innerHTML = `<h2>🤫 00:10</h2>`;
        let s = 10;

        const int = setInterval(() => {
            cont.innerHTML = `<h2>🤫 00:${s.toString().padStart(2,"0")}</h2>`;
            s--;
            if (s < 0) {
                clearInterval(int);
                nextStep();
            }
        }, 1000);

        return;
    }

    // DEFAULT TEXT
    cont.innerHTML = `<h3>${paso.tx?.[idiomaActual] || ""}</h3>`;
    speak(paso.tx?.[idiomaActual] || "");
}

// ------------------------------
// EXPORT GLOBAL
// ------------------------------
window.OPEN_THAN_GO = {
    solicitarEscape,
    cambiarIdioma,
    cambiarBolsillo,
    cambiarModalidad
};

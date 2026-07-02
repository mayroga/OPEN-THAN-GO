// OPEN THAN GO SYSTEM - Frontend Engine v4 FINAL (FIXED + BIOPSYCHOSOCIAL FLOW)
// Company: May Roga LLC

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

// ------------------------------
// SAFE GET
// ------------------------------
function get(id) {
    return document.getElementById(id);
}

// ------------------------------
// GLOBAL TITLE (STATE AWARE)
// ------------------------------
function setTitle(type, emotion = "neutral") {
    const el = get("interactive-title");
    if (!el) return;

    if (tipoEscapeGlobal === "Casa") {
        el.innerText = "OPEN ◯ THAN GO";
        return;
    }

    const map = {
        stress: "OPEN ◉ THAN GO",
        monotony: "OPEN — THAN GO",
        low: "OPEN ○ THAN GO",
        neutral: "OPEN ◎ THAN GO"
    };

    el.innerText = map[emotion] || map.neutral;
}

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const btn = get("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// ------------------------------
// MODES
// ------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;

    get("m-salir")?.classList.toggle("active", esSalir);
    get("m-casa")?.classList.toggle("active", !esSalir);

    setTitle(esSalir ? "Salida" : "Casa");
}

// ------------------------------
// BUDGET
// ------------------------------
function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        const el = get(`b-${v}`);
        if (el) el.classList.toggle("active", v === opcion);
    });
}

// ------------------------------
// LANGUAGE
// ------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;

    get("lang-es")?.classList.toggle("active", lang === "es");
    get("lang-en")?.classList.toggle("active", lang === "en");
}

// ------------------------------
// MAIN REQUEST
// ------------------------------
async function solicitarEscape() {

    const estadoRaw = (get("inp-state")?.value || "FL").toUpperCase();
    const zip = (get("inp-zip")?.value || "").trim();

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: zip,
        estado: estadoRaw,
        region: get("inp-region")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";
    get("wrapper-interactive").style.display = "none";

    try {

        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        get("wrapper-loader").style.display = "none";
        get("wrapper-interactive").style.display = "block";

        pasosMisionGlobal = data.mision?.b || [];
        datosLugarGlobal = data.lugar || null;
        tipoEscapeGlobal = data.tipo || "Salida";

        indicePasoActual = 0;

        setTitle(
            data.tipo,
            detectEmotion(payload.desahogo)
        );

        render();

    } catch (e) {
        console.error(e);
        alert("Error de conexión");
        get("wrapper-form").style.display = "block";
    }
}

// ------------------------------
// EMOTION ENGINE (BIOSOCIAL SIGNAL)
// ------------------------------
function detectEmotion(text = "") {
    text = text.toLowerCase();

    if (text.includes("estres") || text.includes("trabajo") || text.includes("biles")) {
        return "stress";
    }

    if (text.includes("aburrido") || text.includes("rutina") || text.includes("siempre lo mismo")) {
        return "monotony";
    }

    if (text.includes("cansado") || text.includes("sin energia") || text.includes("agotado")) {
        return "low";
    }

    return "neutral";
}

// ------------------------------
// CORE RENDER ENGINE (CRITICAL FIX)
// ------------------------------
function render() {

    const cont = get("step-content");

    if (indicePasoActual >= pasosMisionGlobal.length) {

        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {

            get("btn-maps-action").style.display = "block";
            get("btn-maps-action").href = datosLugarGlobal.gps_link || "#";

            cont.innerHTML = `
                <div class="fade">
                    <h3>Tu destino</h3>
                    <p><strong>${datosLugarGlobal.name}</strong></p>
                    <p>${datosLugarGlobal.address}</p>
                </div>
            `;
        } else {
            cont.innerHTML = `<h3>Sesión completada</h3>`;
        }

        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    if (!paso) return;

    // ------------------------------
    // BIOPSYCHOSOCIAL INTERPRETER
    // ------------------------------
    let output = "";

    switch (paso.t) {

        case "v":
            output = `<h2>${t(paso.tx)}</h2>`;
            break;

        case "h":
            output = `<h4>${t(paso.tx)}</h4>`;
            break;

        case "story":
            output = `<p class="story">${t(paso.story)}</p>`;
            break;

        case "breath_auto":
            iniciarRespiracion(paso.d || 10);
            return;

        case "d":
            renderDecision(paso);
            return;

        case "r":
            output = `<div class="reward">${t(paso.tx)} ${paso.p || ""}</div>`;
            break;

        case "c":
            output = `<div class="affirmation">"${t(paso.tx)}"</div>`;
            break;

        case "sil":
            iniciarSilencio(paso);
            return;

        default:
            output = `<div>${t(paso.tx || paso)}</div>`;
    }

    cont.innerHTML = `<div class="fade">${output}</div>`;

    speak(output);

    get("btn-next").style.display = "block";
    get("btn-next").onclick = () => {
        indicePasoActual++;
        render();
    };
}

// ------------------------------
// SPEECH SAFE
// ------------------------------
function speak(text) {
    if (!("speechSynthesis" in window)) return;

    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(stripHtml(text));
    speechSynthesis.speak(u);
}

// ------------------------------
// DECISION ENGINE (CRITICAL PSYCHOLOGICAL FLOW)
// ------------------------------
function renderDecision(paso) {

    const cont = get("step-content");

    cont.innerHTML = `
        <div class="decision-box">
            <h3>${t(paso.q)}</h3>
            ${paso.op.map((o, i) => `
                <button onclick="resolveDecision(${i}, ${paso.c})">
                    ${t(o)}
                </button>
            `).join("")}
        </div>
    `;
}

// ------------------------------
// DECISION RESOLUTION (COGNITIVE IMPACT)
// ------------------------------
function resolveDecision(i, correct) {

    const paso = pasosMisionGlobal[indicePasoActual];
    const exp = paso.ex?.[i];

    const cont = get("step-content");

    cont.innerHTML = `
        <div class="fade">
            ${t(exp || "Procesando experiencia...")}
        </div>
    `;

    speak(t(exp));

    setTimeout(() => {
        indicePasoActual++;
        render();
    }, 3500);
}

// ------------------------------
// SILENCE MODULE (BIO RESET)
// ------------------------------
function iniciarSilencio(paso) {

    const cont = get("step-content");

    let t = paso.d || 30;

    cont.innerHTML = `
        <div class="silence">
            <p>${t(paso.tx)}</p>
            <h2 id="sil-count">${t}</h2>
        </div>
    `;

    const interval = setInterval(() => {

        t--;
        const el = document.getElementById("sil-count");
        if (el) el.innerText = t;

        if (t <= 0) {
            clearInterval(interval);
            indicePasoActual++;
            render();
        }

    }, 1000);
}

// ------------------------------
// BREATHING (UNCHANGED CORE)
// ------------------------------
function iniciarRespiracion(segundos) {

    const cont = get("step-content");
    let s = segundos;

    cont.innerHTML = `
        <div class="breath-ui">
            <h2>Respira</h2>
            <div id="breathTime"></div>
        </div>
    `;

    const interval = setInterval(() => {

        get("breathTime").innerText = s + "s";
        s--;

        if (s <= 0) {
            clearInterval(interval);
            indicePasoActual++;
            render();
        }

    }, 1000);
}

// ------------------------------
// UTILS
// ------------------------------
function stripHtml(html) {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.innerText;
}

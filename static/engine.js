// OPEN THAN GO SYSTEM - Frontend Engine v4 FINAL
// Company: May Roga LLC

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoPaso = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

let intervaloRespiracion = null;
let intervaloTimer = null;
let tiempoRestante = 0;

// ------------------------------
// SAFE GET
// ------------------------------
function get(id) {
    return document.getElementById(id);
}

// ------------------------------
// VOZ GUIADA (CONTROL SIMPLE)
// ------------------------------
function hablar(texto) {
    if (!("speechSynthesis" in window)) return;
    if (!texto) return;

    const u = new SpeechSynthesisUtterance(texto);
    const voces = speechSynthesis.getVoices();

    let v =
        voces.find(x => x.lang === (idiomaActual === "es" ? "es-ES" : "en-US")) ||
        voces.find(x => x.lang?.startsWith(idiomaActual)) ||
        voces[0];

    u.voice = v;
    u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;
    u.pitch = 1;

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}

// ------------------------------
// TEXT SAFE
// ------------------------------
function t(x) {
    if (!x) return "";
    if (typeof x === "string") return x;
    return x[idiomaActual] || x.es || x.en || "";
}

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    get("btn-start")?.addEventListener("click", solicitarEscape);
});

// ------------------------------
// MODE
// ------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;
    get("m-salir")?.classList.toggle("active", esSalir);
    get("m-casa")?.classList.toggle("active", !esSalir);
}

// ------------------------------
// BUDGET
// ------------------------------
function cambiarBolsillo(v) {
    presupuestoActual = v;
    ["cero","minimo","moderado","libre"].forEach(b=>{
        get(`b-${b}`)?.classList.toggle("active", b===v);
    });
}

// ------------------------------
// LANGUAGE
// ------------------------------
function cambiarIdioma(l) {
    idiomaActual = l;
    get("lang-es")?.classList.toggle("active", l==="es");
    get("lang-en")?.classList.toggle("active", l==="en");
}

// ------------------------------
// MAIN REQUEST
// ------------------------------
async function solicitarEscape() {

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: get("inp-zip")?.value || "",
        estado: get("inp-state")?.value || "",
        region: get("inp-region")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "block";
    get("wrapper-interactive").style.display = "none";

    try {
        const r = await fetch("/api/open-than-go", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(payload)
        });

        const data = await r.json();

        if (!data || data.status !== "success") throw new Error("backend fail");

        setTimeout(() => {

            get("wrapper-loader").style.display = "none";
            get("wrapper-interactive").style.display = "block";

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || data.mode || "";

            indicePasoPaso = 0;

            iniciarFlujo();

        }, 400);

    } catch (e) {
        console.log(e);
        alert("Error conexión");
        location.reload();
    }
}

// ------------------------------
// FLOW ENGINE
// ------------------------------
function iniciarFlujo() {

    clearInterval(intervaloRespiracion);
    clearInterval(intervaloTimer);
    speechSynthesis.cancel();

    const cont = get("step-content");
    const nextBtn = ensureNext();
    const mapBtn = ensureMap();

    if (indicePasoPaso >= pasosMisionGlobal.length) {

        if (tipoEscapeGlobal === "Salida") {
            mapBtn.style.display = "block";
            mapBtn.href = datosLugarGlobal?.gps_link || "#";
            return;
        }

        nextBtn.style.display = "block";
        nextBtn.innerText = "FINALIZAR";
        nextBtn.onclick = () => location.reload();
        return;
    }

    const paso = pasosMisionGlobal[indicePasoPaso];

    nextBtn.onclick = () => {
        indicePasoPaso++;
        iniciarFlujo();
    };

    // ---------------- BREATH ----------------
    if (paso.t === "breath_auto") {
        iniciarRespiracion(paso.d || 10);
        return;
    }

    // ---------------- TIMER CASA ----------------
    if (tipoEscapeGlobal === "Casa") {
        iniciarTimer(600);
    }

    const contenido = paso.tx || paso.story || paso;

    cont.innerHTML = `
        <div class="card-box fade">
            ${t(contenido)}
        </div>
    `;

    hablar(t(contenido));

    nextBtn.style.display = "block";
}

// ------------------------------
// BREATHING GUIDED
// ------------------------------
function iniciarRespiracion(seg) {

    const cont = get("step-content");
    cont.innerHTML = `
        <div class="card center">
            <div id="breathCircle"></div>
            <h2 id="breathText">Inhala</h2>
            <div id="breathTime"></div>
        </div>
    `;

    let t = seg;
    let grow = true;
    let r = 40;

    intervaloRespiracion = setInterval(() => {

        const circle = get("breathCircle");

        r += grow ? 2 : -2;

        if (r > 75) grow = false;
        if (r < 40) grow = true;

        circle.style.transform = `scale(${r/50})`;

        get("breathText").innerText = grow ? "Inhala" : "Exhala";
        get("breathTime").innerText = t + "s";

        t--;

        if (t <= 0) {
            clearInterval(intervaloRespiracion);
            indicePasoPaso++;
            iniciarFlujo();
        }

    }, 1000);
}

// ------------------------------
// TIMER CASA
// ------------------------------
function iniciarTimer(seg) {

    const cont = get("step-content");
    let t = seg;

    cont.innerHTML = `<div id="timer"></div>`;

    intervaloTimer = setInterval(() => {

        const m = Math.floor(t / 60);
        const s = t % 60;

        get("timer").innerText = `${m}:${s.toString().padStart(2,"0")}`;

        t--;

        if (t <= 0) {
            clearInterval(intervaloTimer);
            get("step-content").innerHTML = "<h2>Sesión completada</h2>";
        }

    }, 1000);
}

// ------------------------------
// BUTTONS SAFE
// ------------------------------
function ensureNext() {
    let b = get("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        get("wrapper-interactive").appendChild(b);
    }
    b.style.display = "none";
    b.innerText = "CONTINUAR";
    return b;
}

function ensureMap() {
    let b = get("btn-maps-action");
    if (!b) {
        b = document.createElement("a");
        b.id = "btn-maps-action";
        b.className = "btn-maps-route";
        b.target = "_blank";
        get("wrapper-interactive").appendChild(b);
    }
    b.style.display = "none";
    b.innerText = "ABRIR MAPA";
    return b;
}

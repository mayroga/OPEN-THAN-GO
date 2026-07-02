// ======================================================
// OPEN THAN GO PRO ENGINE v3 (OPTIMIZED)
// May Roga LLC
// Lightweight + Fast + Synced + Stable
// ======================================================

let idiomaActual = 'es';
let presupuestoActual = 'cero';
let modalidadSalir = true;

let pasos = [];
let index = 0;
let lugar = null;
let tipo = "";

let breathingTimer = null;
let stepTimer = null;

// ------------------------------
// SAFE DOM
// ------------------------------
const $ = (id) => document.getElementById(id);

// ------------------------------
// SPEECH (CLEAN QUEUE)
// ------------------------------
function speak(text) {
    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    u.lang = idiomaActual === 'es' ? 'es-ES' : 'en-US';
    u.rate = 0.95;
    u.pitch = 0.9;

    speechSynthesis.speak(u);
}

// ------------------------------
// LANGUAGE
// ------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;

    $("lang-es")?.classList.toggle("active", lang === "es");
    $("lang-en")?.classList.toggle("active", lang === "en");
}

// ------------------------------
// POCKET
// ------------------------------
function cambiarBolsillo(p) {
    presupuestoActual = p;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        $("b-" + v)?.classList.toggle("active", v === p);
    });
}

// ------------------------------
// MODE
// ------------------------------
function cambiarModalidad(isOut) {
    modalidadSalir = isOut;

    $("m-salir")?.classList.toggle("active", isOut);
    $("m-casa")?.classList.toggle("active", !isOut);
}

// ------------------------------
// MAIN REQUEST
// ------------------------------
async function solicitarEscape() {

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        budget_level: presupuestoActual,
        zip_code: $("inp-zip")?.value || "",
        estado: $("inp-state")?.value || "",
        region: $("inp-region")?.value || "",
        desahogo: $("inp-text")?.value || ""
    };

    // UI SWITCH FAST
    $("wrapper-form").style.display = "none";
    $("wrapper-loader").style.display = "block";
    $("wrapper-interactive").style.display = "none";

    try {
        const r = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await r.json();

        if (!r.ok || data.status !== "success") throw new Error("backend");

        setTimeout(() => {

            $("wrapper-loader").style.display = "none";
            $("wrapper-interactive").style.display = "block";

            pasos = data.mision?.b || [];
            lugar = data.lugar || null;
            tipo = data.tipo || "";

            index = 0;

            renderStep();

        }, 400); // 🔥 faster UX

    } catch (e) {
        console.error(e);

        $("wrapper-loader").style.display = "none";
        $("wrapper-form").style.display = "block";
    }
}

// ------------------------------
// CLEAN RENDER ENGINE
// ------------------------------
function renderStep() {

    clearInterval(breathingTimer);
    window.speechSynthesis.cancel();

    const box = $("step-content");
    if (!box) return;

    const btn = ensureNext();
    const map = ensureMap();

    // END
    if (index >= pasos.length) {

        box.innerHTML = "";

        if (tipo === "Salida" && lugar?.gps_link) {
            map.href = lugar.gps_link;
            map.style.display = "block";
            btn.style.display = "none";
        } else {
            btn.innerText = "FINALIZAR";
            btn.style.display = "block";
            btn.onclick = () => location.reload();
        }

        return;
    }

    const p = pasos[index];

    btn.onclick = () => {
        index++;
        renderStep();
    };

    // -------------------------
    // STORY (FAST PATH)
    // -------------------------
    if (p.story) {
        const t = p.story[idiomaActual] || "";
        box.innerHTML = `<div>${t}</div>`;
        speak(t);
        btn.style.display = "block";
        return;
    }

    // -------------------------
    // TEXT STEP
    // -------------------------
    if (p.t === "v" || p.t === "h") {
        const t = p.tx?.[idiomaActual] || "";
        box.innerHTML = `<h3>${t}</h3>`;
        speak(t);
        btn.style.display = "block";
        return;
    }

    // -------------------------
    // BREATHING (OPTIMIZED SINGLE TIMER)
    // -------------------------
    if (p.t === "breath_auto") {

        let t = p.d || 10;
        let inhale = true;

        box.innerHTML = `<h2>${inhale ? "Inhala" : "Exhala"}</h2><div>${t}</div>`;
        speak(inhale ? "Inhala" : "Exhala");

        breathingTimer = setInterval(() => {

            t--;
            inhale = !inhale;

            box.innerHTML = `<h2>${inhale ? "Inhala" : "Exhala"}</h2><div>${t}</div>`;

            if (t % 2 === 0) speak(inhale ? "Inhala" : "Exhala");

            if (t <= 0) {
                clearInterval(breathingTimer);
                index++;
                renderStep();
            }

        }, 1000);

        return;
    }

    // -------------------------
    // DEFAULT SKIP SAFE
    // -------------------------
    index++;
    renderStep();
}

// ------------------------------
// BUTTON FACTORY (NO DUPLICATES)
// ------------------------------
function ensureNext() {
    let b = $("btn-next");

    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        $("wrapper-interactive").appendChild(b);
    }

    b.style.display = "none";
    b.innerText = "CONTINUAR";

    return b;
}

function ensureMap() {
    let b = $("btn-maps-action");

    if (!b) {
        b = document.createElement("a");
        b.id = "btn-maps-action";
        b.className = "btn-maps-route";
        b.target = "_blank";
        $("wrapper-interactive").appendChild(b);
    }

    b.style.display = "none";
    b.innerText = "MAPA";

    return b;
}

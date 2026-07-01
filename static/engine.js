// ===============================
// SAFE LOOP ENGINE v3 CLIENT
// OPEN THAN GO - MAY ROGA LLC
// ===============================

let currentBlocks = [];
let currentStep = 0;
let engineState = null;

let timer = null;
let sessionSeconds = 600; // 10 minutes
let remaining = sessionSeconds;

let breathingInterval = null;
let isRunning = false;

// ===============================
// INIT REQUEST
// ===============================
async function solicitarEscape() {

    const payload = {
        estado: document.getElementById("inp-state").value,
        zip_code: document.getElementById("inp-zip").value,
        bolsillo: selectedPocket,
        texto_libre: document.getElementById("inp-text").value,
        puedes_salir: selectedMode,
        idioma: currentLang
    };

    const res = await fetch("/safe-loop-engine", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!data.blocks) {
        alert("No data received");
        return;
    }

    startEngine(data);
}


// ===============================
// START ENGINE
// ===============================
function startEngine(data) {

    currentBlocks = data.blocks || [];
    currentStep = 0;
    engineState = data.engine || {};

    isRunning = true;

    document.getElementById("wrapper-form").style.display = "none";
    document.getElementById("wrapper-interactive").style.display = "block";

    document.getElementById("interactive-title").innerText = data.title || "OPEN THAN GO";

    if (data.location) {
        document.getElementById("interactive-location").innerText = data.location;
    }

    if (data.map_url) {
        const mapBtn = document.getElementById("btn-maps-action");
        mapBtn.style.display = "block";
        mapBtn.href = data.map_url;
    }

    startLoop();
    startBreathing();
    startTimer();
    renderStep();
}


// ===============================
// LOOP CONTROL
// ===============================
function startLoop() {
    renderStep();
}

function renderStep() {

    if (!isRunning) return;

    const container = document.getElementById("step-content");
    const btnNext = document.getElementById("btn-next");

    const block = currentBlocks[currentStep];

    if (!block) {
        finishSession();
        return;
    }

    container.innerHTML = "";

    // TEXT BLOCK
    if (block.tx) {
        const div = document.createElement("div");
        div.className = "screen-story";
        div.innerText = block.tx;
        container.appendChild(div);

        speak(block.tx);
    }

    // QUESTION BLOCK
    if (block.t === "d") {
        const q = document.createElement("div");
        q.className = "screen-story";
        q.innerText = block.q;
        container.appendChild(q);

        block.op.forEach((opt, index) => {
            const btn = document.createElement("button");
            btn.className = "btn-choice";
            btn.innerText = opt;

            btn.onclick = () => selectOption(index);

            container.appendChild(btn);
        });
    }

    btnNext.style.display = "block";
}


// ===============================
// NEXT STEP
// ===============================
function siguienteComando() {

    if (!isRunning) return;

    currentStep++;

    if (currentStep >= currentBlocks.length) {
        finishSession();
        return;
    }

    renderStep();
}


// ===============================
// OPTION SELECT (NO FREEZE)
// ===============================
function selectOption(index) {

    const block = currentBlocks[currentStep];

    if (!block || !block.op) return;

    const selected = block.op[index];

    speak(selected);

    setTimeout(() => {
        siguienteComando();
    }, 800);
}


// ===============================
// TIMER 10 MINUTES SAFE LOOP
// ===============================
function startTimer() {

    remaining = sessionSeconds;

    timer = setInterval(() => {

        remaining--;

        if (remaining <= 0) {
            finishSession();
        }

    }, 1000);
}


// ===============================
// BREATHING ANIMATION (FIXED)
// ===============================
function startBreathing() {

    const circle = document.querySelector(".breath-circle");

    if (!circle) return;

    let inhale = true;

    breathingInterval = setInterval(() => {

        if (!isRunning) return;

        if (inhale) {
            circle.style.transform = "scale(1.6)";
            circle.innerText = "INHALE";
        } else {
            circle.style.transform = "scale(1.0)";
            circle.innerText = "EXHALE";
        }

        inhale = !inhale;

    }, 3000);
}


// ===============================
// VOICE ENGINE (TTS)
// ===============================
function speak(text) {

    if (!text) return;

    try {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = currentLang === "es" ? "es-ES" : "en-US";
        msg.rate = 1;

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    } catch (e) {
        console.log("Voice error", e);
    }
}


// ===============================
// FINISH SESSION SAFE RESET
// ===============================
function finishSession() {

    isRunning = false;

    clearInterval(timer);
    clearInterval(breathingInterval);

    document.getElementById("step-content").innerHTML = `
        <div class="screen-story">
            Sesión completada. Puedes reiniciar el ciclo.
        </div>
    `;

    const btn = document.getElementById("btn-next");
    btn.innerText = "REINICIAR";
    btn.onclick = () => location.reload();
}


// ===============================
// GLOBAL CONTROL FLAGS
// ===============================
let selectedPocket = "cero";
let selectedMode = true;
let currentLang = "es";

function cambiarIdioma(lang) {
    currentLang = lang;
}

function cambiarBolsillo(v) {
    selectedPocket = v;
}

function cambiarModalidad(v) {
    selectedMode = v;
}

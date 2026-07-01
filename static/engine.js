// ===============================
// SAFE LOOP ENGINE v5 TOTAL FIX
// ONE BRAIN ONLY - CLIENT CONTROLLED
// ===============================

let state = {
    lang: "es",
    stepIndex: 0,
    bloques: [],
    modalidad: "outdoor",
    voice: null,
    speaking: false,
    breathingInterval: null,
    silenceTimer: null,
    silenceActive: false,
    countdown: 0,
    loopStart: 0,
    loopDuration: 600000, // 10 min exact
    usedIndexes: new Set(),
    breathingState: 0
};

// ===============================
// INIT VOICE
// ===============================
function initVoice(lang) {
    const voices = speechSynthesis.getVoices();
    state.voice = voices.find(v => v.lang.includes(lang)) || voices[0];
}

// ===============================
// TEXT SPEAK
// ===============================
function speak(text) {
    if (!text) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = state.lang;
    u.voice = state.voice;
    state.speaking = true;
    u.onend = () => state.speaking = false;
    window.speechSynthesis.speak(u);
}

// ===============================
// LOAD SESSION
// ===============================
async function solicitarEscape() {

    const payload = {
        estado: document.getElementById("inp-state").value,
        zip_code: document.getElementById("inp-zip").value,
        bolsillo: getBolsillo(),
        puedes_salir: getModalidad(),
        texto_libre: document.getElementById("inp-text").value,
        idioma: state.lang
    };

    const res = await fetch("/diagnostico-kamizen", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    state.bloques = data.bloques_interactivos || [];
    state.modalidad = data.modalidad;

    document.getElementById("wrapper-form").style.display = "none";
    document.getElementById("wrapper-interactive").style.display = "block";

    document.getElementById("interactive-title").innerText = data.titulo;

    if (data.lugar) {
        document.getElementById("interactive-location").innerText = data.lugar;
    }

    if (data.url_maps) {
        const mapBtn = document.getElementById("btn-maps-action");
        mapBtn.href = data.url_maps;
        mapBtn.style.display = "block";
    }

    state.loopStart = Date.now();
    startLoop();
    renderStep();
}

// ===============================
// LOOP CONTROL 10 MIN EXACT
// ===============================
function startLoop() {
    clearInterval(state.silenceTimer);

    setTimeout(() => {
        endLoop();
    }, state.loopDuration);
}

// ===============================
function endLoop() {
    speak("Ejercicio terminado. Puedes reiniciar cuando quieras.");
    resetEngine();
}

// ===============================
function resetEngine() {
    state.stepIndex = 0;
    state.usedIndexes.clear();
    state.breathingState = 0;
}

// ===============================
// STEP RENDER
// ===============================
function renderStep() {

    if (!state.bloques.length) return;

    let block = getNextBlock();

    if (!block) {
        endLoop();
        return;
    }

    showBlock(block);
}

// ===============================
// SECUENCIA SIN REPETICIÓN
// ===============================
function getNextBlock() {

    if (state.usedIndexes.size >= state.bloques.length) {
        state.usedIndexes.clear();
    }

    let available = state.bloques
        .map((_, i) => i)
        .filter(i => !state.usedIndexes.has(i));

    let idx = available[Math.floor(Math.random() * available.length)];

    state.usedIndexes.add(idx);
    state.stepIndex = idx;

    return state.bloques[idx];
}

// ===============================
// SHOW BLOCK
// ===============================
function showBlock(block) {

    const container = document.getElementById("step-content");
    container.innerHTML = "";

    if (block.tx) {
        speak(typeof block.tx === "string" ? block.tx : block.tx.es || block.tx.en);
    }

    // TEXT
    if (block.tx) {
        const div = document.createElement("div");
        div.innerText = typeof block.tx === "string" ? block.tx : (block.tx.es || block.tx.en);
        container.appendChild(div);
    }

    // QUESTION
    if (block.q) {
        const q = document.createElement("h3");
        q.innerText = block.q.es || block.q.en;
        container.appendChild(q);
    }

    // OPTIONS
    if (block.op) {
        block.op.forEach((o, i) => {
            const b = document.createElement("button");
            b.innerText = o.es || o.en || o;
            b.onclick = () => handleOption(i, block);
            container.appendChild(b);
        });
    }

    // BREATHING FIX ANIMATED
    if (block.t === "breath_auto") {
        startBreathing(block.d || 20);
    }

    // SILENCE TIMER FIX
    if (block.t === "sil") {
        startSilence(block.d || 30);
    }

    document.getElementById("btn-next").style.display = "block";
}

// ===============================
// OPTION HANDLER
// ===============================
function handleOption(i, block) {
    speak("Continuando");

    renderStep();
}

// ===============================
// BREATHING FIX ANIMATED
// ===============================
function startBreathing(seconds) {

    const circle = document.createElement("div");
    circle.className = "breath-circle";

    const wrapper = document.querySelector(".wrapper-circle") || document.getElementById("step-content");
    wrapper.appendChild(circle);

    let inhale = true;
    let t = 0;

    clearInterval(state.breathingInterval);

    state.breathingInterval = setInterval(() => {

        t++;

        if (inhale) {
            circle.style.transform = "scale(1.6)";
            circle.innerText = "IN";
        } else {
            circle.style.transform = "scale(1)";
            circle.innerText = "OUT";
        }

        inhale = !inhale;

        if (t >= seconds * 2) {
            clearInterval(state.breathingInterval);
        }

    }, 1000);
}

// ===============================
// SILENCE TIMER FIX
// ===============================
function startSilence(seconds) {

    state.silenceActive = true;
    state.countdown = seconds;

    const container = document.getElementById("step-content");

    const timer = document.createElement("div");
    timer.id = "silence-timer";
    container.appendChild(timer);

    clearInterval(state.silenceTimer);

    state.silenceTimer = setInterval(() => {

        state.countdown--;

        timer.innerText = "Silencio: " + state.countdown + "s";

        if (state.countdown <= 0) {
            clearInterval(state.silenceTimer);
            state.silenceActive = false;
            renderStep();
        }

    }, 1000);
}

// ===============================
// UI HELPERS
// ===============================
function cambiarIdioma(l) {
    state.lang = l;
    document.getElementById("lang-es").classList.toggle("active", l === "es");
    document.getElementById("lang-en").classList.toggle("active", l === "en");
}

function cambiarBolsillo(v) {
    window._bolsillo = v;
}

function getBolsillo() {
    return window._bolsillo || "cero";
}

function cambiarModalidad(v) {
    window._modalidad = v;
}

function getModalidad() {
    return window._modalidad ?? true;
}

// ===============================
// NEXT STEP
// ===============================
function siguienteComando() {
    renderStep();
}

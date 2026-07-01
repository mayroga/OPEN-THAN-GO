/* =========================================================
   OPEN THAN GO ENGINE vFINAL CLEAN
   SINGLE BRAIN + LINEAR FLOW 1 → 27
   NO FREEZE + NO DOUBLE CONTROL
========================================================= */

const state = {
    missions: [],
    stories: [],
    i: 0,              // mission index (strict)
    b: 0,              // block index
    lang: "en",
    running: false,
    speaking: false,
    timer: null,
    tLeft: 0,
    breathTimer: null
};

/* =========================
   INIT
========================= */
window.addEventListener("load", async () => {
    await boot();
    intro();
});

async function boot() {
    const [s, m] = await Promise.all([
        fetch("/api/stories").then(r => r.json()),
        fetch("/api/missions").then(r => r.json())
    ]);

    state.stories = (s.stories || []).sort((a,b)=>a.id-b.id);
    state.missions = (m.missions || []).sort((a,b)=>a.id-b.id);

    state.running = true;
}

/* =========================
   INTRO
========================= */
function intro() {
    document.getElementById("app").innerHTML = `
        <div class="card center">
            <h1>OPEN THAN GO</h1>
            <p>Linear Emotional System</p>
            <button onclick="start()">START</button>
        </div>
    `;
}

function start() {
    state.i = 0;
    state.b = 0;
    render();
}

/* =========================
   LANGUAGE
========================= */
function setLang(l) {
    state.lang = l;
    render();
}

/* =========================
   SAFE TEXT
========================= */
function T(obj) {
    if (!obj) return "";
    if (typeof obj === "string") return obj;
    return obj[state.lang] || obj.en || "";
}

/* =========================
   MAIN RENDER (SINGLE LOOP ONLY)
========================= */
function render() {
    if (!state.running) return;

    const app = document.getElementById("app");

    const mission = state.missions[state.i];
    if (!mission) return reset();

    const block = mission.b[state.b];

    let html = `
        <div class="topbar">
            <button onclick="setLang('en')">EN</button>
            <button onclick="setLang('es')">ES</button>
            <button onclick="back()">BACK</button>
        </div>
    `;

    if (!block) {
        nextMission();
        return;
    }

    /* =========================
       BLOCK TYPES
    ========================= */

    if (block.t === "v") {
        html += `<div class="card"><h2>${T(block.tx)}</h2></div>`;
        speak(T(block.tx), nextBlock);
    }

    if (block.t === "h") {
        html += `<div class="card"><h3>${T(block.tx)}</h3></div>`;
        speak(T(block.tx), nextBlock);
    }

    if (block.story) {
        html += `<div class="card"><p>${T(block.story)}</p></div>`;
        speak(T(block.story), nextBlock);
    }

    if (block.t === "breath_auto" || block.t === "br") {
        html += breathUI(block);
        startBreath(block.d || 25);
        speak(T(block.tx), () => {});
    }

    if (block.t === "d") {
        html += `<div class="card"><h3>${T(block.q)}</h3>`;
        block.op.forEach((o, idx) => {
            html += `
                <div class="answer" onclick="answer(${idx}, ${block.c}, ${encodeURIComponent(JSON.stringify(block.ex))})">
                    ${T(o)}
                </div>`;
        });
        html += `</div>`;
    }

    if (block.t === "r") {
        html += `<div class="card center">+${block.p} XP</div>`;
        speak(T(block.tx), nextBlock);
    }

    if (block.t === "c") {
        html += `<div class="card">${T(block.tx)}</div>`;
        speak(T(block.tx), nextBlock);
    }

    if (block.t === "sil") {
        html += breathUI(block);
        startTimer(block.d || 30, nextBlock);
        speak(T(block.tx), () => {});
    }

    app.innerHTML = html;
}

/* =========================
   SAFE SPEECH (NO FREEZE)
========================= */
function speak(text, cb) {
    if (!text) return cb && cb();

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;

    u.onend = () => cb && cb();
    window.speechSynthesis.speak(u);
}

/* =========================
   LINEAR NAVIGATION ONLY
========================= */
function nextBlock() {
    state.b++;
    render();
}

function nextMission() {
    state.i++;
    state.b = 0;

    if (state.i >= state.missions.length) {
        state.i = 0;
    }
    render();
}

function back() {
    window.speechSynthesis.cancel();

    if (state.b > 0) state.b--;
    else if (state.i > 0) {
        state.i--;
        state.b = 0;
    }

    render();
}

function reset() {
    state.i = 0;
    state.b = 0;
    render();
}

/* =========================
   ANSWERS (NO FREEZE)
========================= */
function answer(i, correct, ex) {
    const exp = JSON.parse(decodeURIComponent(ex));

    const ok = i === correct;

    const box = document.createElement("div");
    box.className = "card";
    box.innerHTML = `
        <h3 style="color:${ok ? "lime" : "red"}">
            ${ok ? "GOOD" : "TRY AGAIN"}
        </h3>
        <p>${T(exp[i])}</p>
        <button onclick="nextBlock()">CONTINUE</button>
    `;

    document.getElementById("app").appendChild(box);

    speak(T(exp[i]), () => {});
}

/* =========================
   TIMER REAL (NON-BLOCKING)
========================= */
function startTimer(sec, cb) {
    clearInterval(state.timer);
    state.tLeft = sec;

    state.timer = setInterval(() => {
        state.tLeft--;
        if (state.tLeft <= 0) {
            clearInterval(state.timer);
            cb && cb();
        }
    }, 1000);
}

/* =========================
   BREATH (REAL NATURAL LOOP)
========================= */
function breathUI(block) {
    return `
        <div class="card center">
            <div id="breath" class="breath"></div>
            <p>${T(block.tx)}</p>
        </div>
    `;
}

function startBreath(sec) {
    clearInterval(state.breathTimer);

    let inhale = true;
    const el = document.getElementById("breath");

    if (!el) return;

    state.breathTimer = setInterval(() => {
        inhale = !inhale;
        el.style.transform = inhale ? "scale(1.4)" : "scale(0.9)";
        el.style.transition = "3s ease-in-out";
    }, 3000);

    setTimeout(() => clearInterval(state.breathTimer), sec * 1000);
}

let state = {
    missions: [],
    i: 0,
    b: 0,
    lang: "es",
    timer: null,
    timeLeft: 600,
    running: false,
    locked: false
};

window.onload = async () => {
    await boot();
};

async function boot() {
    const res = await fetch("/api/missions");
    const data = await res.json();

    state.missions = data.missions || [];
    startSession();
}

function startSession() {
    state.i = 0;
    state.b = 0;
    state.timeLeft = 600;
    state.running = true;

    startGlobalTimer();
    render();
}

/* ================= TIMER 10 MIN ================= */
function startGlobalTimer() {
    clearInterval(state.timer);

    state.timer = setInterval(() => {
        state.timeLeft--;

        if (state.timeLeft <= 0) {
            endSession();
        }
    }, 1000);
}

function endSession() {
    clearInterval(state.timer);
    speechSynthesis.cancel();

    document.getElementById("app").innerHTML =
        `<div class="card">
            <h2>SESSION COMPLETE</h2>
            <button onclick="location.reload()">RESTART</button>
        </div>`;
}

/* ================= FLOW CONTROL ================= */
function next() {
    if (state.locked) return;

    const m = state.missions[state.i];
    if (!m) return endSession();

    state.b++;

    if (state.b >= m.b.length) {
        state.i++;
        state.b = 0;

        if (state.i >= state.missions.length) {
            state.i = 0; // LOOP 1-21
        }
    }

    render();
}

function back() {
    if (state.locked) return;

    if (state.b > 0) {
        state.b--;
    } else if (state.i > 0) {
        state.i--;
        state.b = state.missions[state.i].b.length - 1;
    }

    render();
}

/* ================= RENDER ENGINE ================= */
function render() {
    const app = document.getElementById("app");
    const m = state.missions[state.i];
    if (!m) return;

    const b = m.b[state.b];
    if (!b) return next();

    let html = `<div class="card">`;

    /* HEADER */
    html += `
        <div style="display:flex;gap:10px;margin-bottom:10px;">
            <button onclick="back()">BACK</button>
            <button onclick="next()">CONTINUE</button>
        </div>
    `;

    /* ================= BLOCK TYPES ================= */

    // TITLE / HEADER
    if (b.t === "v" || b.t === "h") {
        html += `<h2>${b.tx?.[state.lang] || ""}</h2>`;
        speak(b.tx?.[state.lang]);
    }

    // STORY
    if (b.story) {
        html += `<p>${b.story?.[state.lang]}</p>`;
        speak(b.story?.[state.lang]);
    }

    // BREATH (REAL VISUAL LOOP)
    if (b.t === "breath_auto") {
        html += `
            <div class="breath-circle" id="breath">BREATH</div>
            <p>${b.tx?.[state.lang] || ""}</p>
        `;
        startBreath(b.d || 25);
        speak(b.tx?.[state.lang]);
    }

    // SILENCE TIMER BLOCK
    if (b.t === "sil") {
        html += `<h3>${b.tx?.[state.lang]}</h3>`;
        startSilence(b.d || 30);
        speak(b.tx?.[state.lang]);
    }

    // QUESTION BLOCK
    if (b.t === "d") {
        html += `<h3>${b.q?.[state.lang]}</h3>`;

        b.op.forEach((o, i) => {
            html += `
                <div class="answer" onclick="answer(${i}, ${b.c})">
                    ${o[state.lang] || o}
                </div>
            `;
        });
    }

    // REWARD
    if (b.t === "r") {
        html += `<h2>${b.tx}</h2>`;
        speak("Reward earned");
    }

    // CONFIRMATION
    if (b.t === "c") {
        html += `<p>${b.tx?.[state.lang]}</p>`;
        speak(b.tx?.[state.lang]);
    }

    html += `</div>`;

    app.innerHTML = html;
}

/* ================= ANSWER ================= */
function answer(i, correct) {
    if (i === correct) {
        speak("Correct");
    } else {
        speak("Incorrect");
    }

    setTimeout(next, 800);
}

/* ================= BREATH SYSTEM ================= */
function startBreath(seconds) {
    const el = document.getElementById("breath");
    if (!el) return;

    let inhale = true;

    const interval = setInterval(() => {
        if (!el) return clearInterval(interval);

        el.style.transition = "all 4s ease";
        el.style.transform = inhale ? "scale(1.4)" : "scale(0.8)";
        el.innerText = inhale ? "INHALE" : "EXHALE";

        inhale = !inhale;
    }, 4000);

    setTimeout(() => clearInterval(interval), seconds * 1000);
}

/* ================= SILENCE TIMER ================= */
function startSilence(seconds) {
    setTimeout(() => {
        speak("Silence complete");
    }, seconds * 1000);
}

/* ================= SPEECH ================= */
function speak(text) {
    if (!text) return;

    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);

    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;

    speechSynthesis.speak(u);
}

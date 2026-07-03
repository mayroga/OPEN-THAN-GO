// =====================================
// OPEN THAN GO SYSTEM
// Frontend Engine Unified v5
// Company: May Roga LLC
// =====================================

let appState = {
    mode: "salir",
    emotion: "neutral",
    missions: [],
    currentMission: null,
    currentBlock: 0,
    selectedPlace: null,
    places: [],
    timer: null,
    timeLeft: 0,
    sessionStarted: false,
    speechLocked: false
};

// =====================================
// SAFE GET
// =====================================

function get(id){
    return document.getElementById(id);
}

// =====================================
// VOICE ENGINE
// =====================================

function speak(text, callback=null){

    if(!window.speechSynthesis){
        if(callback) callback();
        return;
    }

    speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 0.92;
    speech.pitch = 0.85;

    const voices = speechSynthesis.getVoices();

    const male =
        voices.find(v =>
            v.lang.startsWith("en") &&
            (
                v.name.includes("David") ||
                v.name.includes("Guy") ||
                v.name.includes("Male")
            )
        );

    if(male){
        speech.voice = male;
    }

    speech.onend = () => {
        if(callback) callback();
    };

    speechSynthesis.speak(speech);
}

// =====================================
// TITLE ENGINE
// =====================================

function setTitle(){

    const el = get("interactive-title");

    if(!el) return;

    if(appState.mode==="casa"){
        el.innerText = "OPEN ◯ THAN GO";
        return;
    }

    switch(appState.emotion){

        case "OUT_STRUCTURE":
            el.innerText = "OPEN ◉ THAN GO";
            break;

        case "OUT_EXPLORATION":
            el.innerText = "OPEN — THAN GO";
            break;

        case "OUT_SLOW":
            el.innerText = "OPEN ○ THAN GO";
            break;

        default:
            el.innerText = "OPEN ◎ THAN GO";
    }
}

// =====================================
// MODE
// =====================================

function setMode(mode){

    appState.mode = mode;

    setTitle();

    const badge = get("mode-badge");

    if(!badge) return;

    if(mode==="casa"){
        badge.innerText =
            "Modo: Casa";
    }
    else{
        badge.innerText =
            "Modo: Salir";
    }
}

// =====================================
// START
// =====================================

async function startOpenThanGo(){

    get("form").style.display = "none";
    get("loader").style.display = "block";

    const payload = {
        decision: appState.mode,
        estado: get("inp-state").value,
        zip_code: get("inp-zip").value,
        budget_level: get("inp-budget").value,
        desahogo: get("inp-text").value
    };

    const res =
        await fetch(
            "/api/open-than-go",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify(payload)
            }
        );

    const data = await res.json();

    get("loader").style.display = "none";

    appState.emotion =
        data.emotion || "neutral";

    appState.places =
        data.recommendations || [];

    appState.currentMission =
        data.mision || null;

    setTitle();

    if(appState.mode==="salir"){
        renderPlaces(data);
    }
    else{
        startHomeSession(data);
    }
}

// =====================================
// PLACE ENGINE
// =====================================

function renderPlaces(data){

    const result =
        get("result");

    let html = "";

    let places =
        data.recommendations || [];

    if(places.length===0){
        result.innerHTML =
            "<div class='card'>No places available.</div>";
        return;
    }

    const suggested =
        Math.floor(
            Math.random() *
            places.length
        );

    appState.selectedPlace =
        places[suggested];

    html += `
        <div class="card">
            <h2>
                Tu opciones de hoy
            </h2>
        </div>
    `;

    places.forEach((p,index)=>{

        const recommended =
            index===suggested;

        html += `
            <div class="place-card">

                ${
                    recommended
                    ?
                    `<div>
                        ⭐ Recomendado para hoy
                     </div>`
                    :
                    ""
                }

                <h3>${p.name}</h3>

                <p>
                    💵 ${p.cost}
                </p>

                <p>
                    ${p.why}
                </p>

                <a
                    class="btn"
                    href="${p.gps_link}"
                    target="_blank">

                    IR AQUÍ

                </a>

            </div>
        `;
    });

    result.innerHTML = html;

    speak(
        "Your options are ready. One destination has been specially selected for today."
    );
}

// =====================================
// CASA MODE
// =====================================

function startHomeSession(data){

    const result =
        get("result");

    result.innerHTML = `
        <div class="card center">

            <h2>
                OPEN ◯ THAN GO
            </h2>

            <div
                class="breath-circle"
                id="breathCircle">

                <span id="breathLabel">
                    READY
                </span>

            </div>

            <h1 id="timerDisplay">
                10:00
            </h1>

        </div>
    `;

    speak(
        "Find a comfortable place. Follow the circle."
    );

    startCountdown(
        600,
        finishHomeSession
    );

    startGuidedBreathing();
}

// =====================================
// TIMER
// =====================================

function startCountdown(seconds, callback){

    clearInterval(
        appState.timer
    );

    appState.timeLeft =
        seconds;

    appState.timer =
        setInterval(()=>{

            appState.timeLeft--;

            const m =
                Math.floor(
                    appState.timeLeft/60
                );

            const s =
                appState.timeLeft%60;

            const display =
                get("timerDisplay");

            if(display){
                display.innerText =
                    `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
            }

            if(appState.timeLeft<=0){

                clearInterval(
                    appState.timer
                );

                if(callback){
                    callback();
                }
            }

        },1000);
}

// =====================================
// BREATH
// =====================================

function startGuidedBreathing(){

    const circle =
        get("breathCircle");

    const label =
        get("breathLabel");

    if(!circle || !label)
        return;

    let inhale = true;

    function step(){

        label.innerText =
            inhale
            ? "INHALE"
            : "EXHALE";

        circle.style.transform =
            inhale
            ? "scale(1.35)"
            : "scale(0.85)";

        inhale = !inhale;
    }

    step();

    setInterval(()=>{
        if(appState.timeLeft<=0)
            return;

        step();
    },4000);
}

// =====================================
// FINISH
// =====================================

function finishHomeSession(){

    speechSynthesis.cancel();

    get("result").innerHTML = `
        <div class="card center">

            <h2>
                OPEN THAN GO
            </h2>

            <p>
                Session completed.
            </p>

            <button
                onclick="location.reload()">

                CONTINUE

            </button>

        </div>
    `;

    speak(
        "Session completed. Have a good day."
    );
}

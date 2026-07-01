const state = { lang: 'es', salir: true };

function renderForm() {
    document.getElementById('app').innerHTML = `
        <div class="lang-bar">
            <button class="btn-lang ${state.lang==='es'?'active':''}" onclick="setLang('es')">ES</button>
            <button class="btn-lang ${state.lang==='en'?'active':''}" onclick="setLang('en')">EN</button>
        </div>
        <div class="header-app">
            <h1>OPEN THAN GO</h1>
            <p>Tu escape emocional inteligente</p>
        </div>
        <div class="form-group">
            <label>Estado</label>
            <select id="inp-state"><option>Florida</option><option>Texas</option><option>California</option></select>
        </div>
        <div class="form-group">
            <label>ZIP Code</label><input id="inp-zip" placeholder="Ej: 33101">
        </div>
        <div class="form-group">
            <label>Presupuesto</label>
            <div class="btn-grid-3">
                <button class="btn-choice active">$0</button><button class="btn-choice">Medio</button><button class="btn-choice">Libre</button>
            </div>
        </div>
        <div class="form-group">
            <label>¿Salir o casa?</label>
            <div class="btn-grid-2">
                <button class="btn-choice ${state.salir?'active':''}" onclick="setSalir(true)">Salir</button>
                <button class="btn-choice ${!state.salir?'active':''}" onclick="setSalir(false)">Casa</button>
            </div>
        </div>
        <div class="form-group">
            <label>Desahogo</label><textarea id="inp-text" placeholder="Escribe cómo te sientes..."></textarea>
        </div>
        <button class="btn-trigger" onclick="ejecutarProtocolo()">GENERAR ESCAPE</button>
    `;
}

function setLang(l) { state.lang = l; renderForm(); }
function setSalir(s) { state.salir = s; renderForm(); }

async function ejecutarProtocolo() {
    const res = await fetch(`/api/get-protocol?salir=${state.salir}`);
    const data = await res.json();
    
    let html = `<h2>Tu Protocolo de Activación</h2>`;
    if (data.modo === 'casa') {
        html += `<p>Fase 1: ${data.protocolos[0].nombre} (${data.protocolos[0].accion})</p>
                 <p>Fase 2: ${data.protocolos[1].nombre} (${data.protocolos[1].accion})</p>`;
    } else {
        html += `<p>Misión: ${data.protocolo.nombre} <br> Acción: ${data.protocolo.accion}</p>`;
    }
    html += `<button class="btn-trigger" onclick="renderForm()">NUEVA MISIÓN</button>`;
    document.getElementById('app').innerHTML = html;
}

renderForm();

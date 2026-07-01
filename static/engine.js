// Open Than Go Engine - UX Dinámica y Manejo de Bloques de Misiones

async function ejecutarOpenThanGo() {
    // 1. Capturar Variables Básicas de la Interfaz
    const decision = document.querySelector('input[name="destino_inicial"]:checked')?.value; // "casa" o "salir"
    const current_lang = document.getElementById("select-lang").value || "es";
    
    // Contenedores de Pantalla
    const pantallaCarga = document.getElementById("loader-pantalla");
    const contenedorResultado = document.getElementById("contenedor-prescripcion");
    
    pantallaCarga.style.display = "flex";
    contenedorResultado.style.display = "none";

    let payload = { decision: decision, lang: current_lang };

    // Si decide salir, agregamos los filtros geográficos y económicos
    if (decision === "salir") {
        payload.zip_code = document.getElementById("input-zip").value;
        payload.estado = document.getElementById("select-estado").value;
        payload.region = document.getElementById("select-region").value;
        payload.budget_level = document.querySelector('input[name="pocket_match"]:checked')?.value; // "cero", "moderado", "libre"
    }

    try {
        const respuesta = await fetch('/api/open-than-go', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await respuesta.json();

        setTimeout(() => {
            pantallaCarga.style.display = "none";
            
            if (data.status === "success") {
                renderizarEstructuraMision(data, current_lang);
                contenedorResultado.style.display = "block";
                contenedorResultado.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert(data.message);
            }
        }, 1500); // 1.5 segundos para bajar la ansiedad del usuario

    } catch (error) {
        pantallaCarga.style.display = "none";
        console.error("Error en Open Than Go System:", error);
    }
}

function renderizarEstructuraMision(data, lang) {
    // Renderizar Ubicación (Solo si es una salida exterior)
    const areaLugar = document.getElementById("modulo-lugar");
    if (data.tipo === "Salida") {
        areaLugar.innerHTML = `
            <div class="card-lugar">
                <h3>📍 Tu Destino de Cambio: ${data.lugar.name}</h3>
                <p><strong>Ubicación:</strong> ${data.lugar.address} (${data.lugar.region})</p>
                <button onclick="window.open('${data.lugar.gps_link}', '_blank')" class="btn-gps">Abrir GPS Gratis</button>
            </div>
        `;
        areaLugar.style.display = "block";
    } else {
        areaLugar.style.display = "none";
    }

    // Procesar e Inyectar los Bloques Internos (b) de la Misión de manera Humana
    const pasos = data.mision.b;
    let htmlPasos = "";

    pasos.forEach(paso => {
        if (paso.story) {
            htmlPasos += `<div class="bloque-historia"><p>${paso.story[lang]}</p></div>`;
        }
        if (paso.t === "breath_auto") {
            htmlPasos += `
                <div class="bloque-respiracion">
                    <span class="cronometro">⏱️ ${paso.d}s</span>
                    <p><strong>${paso.tx[lang]}</strong></p>
                    <small>${paso.inf[lang]}</small>
                </div>
            `;
        }
        if (paso.t === "d") {
            // El Cuestionario de Opción Múltiple (Terapia de Decisión Conductual)
            let opcionesHtml = "";
            paso.op.forEach((opcion, index) => {
                opcionesHtml += `
                    <button class="btn-opcion" onclick="validarRespuestaMision(${index}, ${paso.c}, '${paso.ex[index][lang]}')">
                        ${opcion[lang]}
                    </button>
                `;
            });
            htmlPasos += `
                <div class="bloque-decision">
                    <h4>🤔 Desafío Mental:</h4>
                    <p class="pregunta">${paso.q[lang]}</p>
                    <div class="contenedor-opciones">${opcionesHtml}</div>
                    <div id="feedback-decision" class="feedback-oculto"></div>
                </div>
            `;
        }
        if (paso.t === "c") {
            htmlPasos += `<div class="bloque-compromiso"><blockquote>"${paso.tx[lang]}"</blockquote></div>`;
        }
        if (paso.t === "sil") {
            htmlPasos += `
                <div class="bloque-ejercicio-final">
                    <h4>⚡ Ejercicio Práctico en el Sitio (${paso.d} segundos):</h4>
                    <p>${paso.tx[lang]}</p>
                    <small>💡 Beneficio: ${paso.inf[lang]}</small>
                </div>
            `;
        }
    });

    document.getElementById("area-pasos-mision").innerHTML = htmlPasos;
}

function validarRespuestaMision(seleccionado, correcto, explicacion) {
    const feedbackDiv = document.getElementById("feedback-decision");
    feedbackDiv.className = "feedback-visible";
    
    if (seleccionado === correcto) {
        feedbackDiv.innerHTML = `<p class="txt-correcto"><strong>¡Excelente elección!</strong> <br>${explicacion}</p>`;
    } else {
        feedbackDiv.innerHTML = `<p class="txt-incorrecto"><strong>Analiza esto:</strong> <br>${explicacion}</p>`;
    }
}

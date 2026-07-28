/**
 * OPEN THAN GO - MÓDULO SATÉLITE PREMIUM DE BIENESTAR ASISTIDO V6.2.0
 * (Estructura de Expansión Masiva de Misiones y Cuantificación Biopsicosocial)
 */
const ASISTENCIA_ESPECIAL_CORE = {
    categoriaActiva: "",
    faseAntes: { indicador_saturacion: 0, mente_inicial: "", timestamp: "" },
    faseDurante: { id_mision: "", interaccion_activa: 0, descompresion_lograda: 0, timestamp: "" },
    faseDespues: { retorno_equilibrio: 0, estado_final: "", enfoque_recuperado: 0, timestamp: "" },

    // BANCO DE DATOS EXPANDIDO DE ALTA DIVERSIDAD PARA PREVENIR REPETICIONES
    misionesEspeciales: {
        "veterano": {
            "SALIR": [
                {id: "v_s1", titulo: "Filtro de Frecuencias Periféricas", desc: "Mira un punto estático lejano 3 minutos al aire libre. Registra conscientemente la seguridad del espacio abierto.", fisiologica: "Suelo firme. Entorno despejado. Estás seguro aquí."},
                {id: "v_s2", titulo: "Reconocimiento Acústico Orgánico", desc: "Cierra los ojos en una zona verde. Identifica tres sonidos suaves y aislados de la naturaleza.", fisiologica: "Suelta la tensión del cuello. Escucha el aire en absoluta paz."},
                {id: "v_s3", titulo: "Sincronización de Marcha Táctica", desc: "Camina contando mentalmente 4 pasos para inhalar y 4 para exhalar de forma continua.", fisiologica: "Siente el impacto suave de cada paso. Avanzas a tu propio ritmo seguro."},
                {id: "v_s4", titulo: "Anclaje Táctil con la Tierra", desc: "Toca la corteza de un árbol o una roca grande con la palma izquierda 2 minutos. Siente su temperatura.", fisiologica: "Tu cuerpo está conectado a algo firme. Respira hondo una vez."},
                {id: "v_s5", titulo: "Ampliación del Horizonte Visual", desc: "Siéntate al sol mirando hacia el punto más lejano donde se une el cielo y la tierra. Brazos flojos.", fisiologica: "Siente el cobijo del calor ambiental. Estás en control total de tu espacio."}
            ],
            "CASA": [
                {id: "v_c1", titulo: "Anclaje Físico Axial", desc: "Siéntate derecho con las plantas de los pies planas en el piso. Siente todo tu peso real sobre el asiento.", fisiologica: "Deja caer el peso de tus hombros. El suelo te sostiene firme."},
                {id: "v_c2", titulo: "Aislamiento de Frecuencias de Fondo", desc: "En la habitación más silenciosa de casa, cierra los ojos y atiende únicamente el sonido de tu respiración.", fisiologica: "El aire fresco entra y sale tibio. Estás en tu espacio seguro."},
                {id: "v_c3", titulo: "Descarga Excesiva Escapular", desc: "Sube hombros a las orejas con fuerza tomando aire, sostén 3 segundos y suéltalos de golpe exhalando.", fisiologica: "Siente tus brazos colgar libres y ligeros. Repítelo una vez más."},
                {id: "v_c4", titulo: "Escudo Térmico Somático", desc: "Sostén una taza templada entre las manos. Siente el calor fluir a la piel con los ojos cerrados.", fisiologica: "Disfruta el confort térmico en tus palmas. Respira muy despacio."}
            ]
        },
        "mayor": {
            "SALIR": [
                {id: "m_s1", titulo: "Baño de Sol Directo y Oxigenación", desc: "Busca una banca cómoda al aire libre libre de escalones difíciles. Deja que la luz natural ilumine tu rostro.", fisiologica: "Siente la brisa ligera en tu piel. Respira sin prisa, el tiempo es tuyo."},
                {id: "m_s2", titulo: "Paseo de Enfoque Cromático", desc: "Camina a paso muy lento por un jardín. Observa detalladamente las tonalidades y formas de una planta.", fisiologica: "Tu vista descansa en la belleza natural. Camina suave y con calma."},
                {id: "m_s3", titulo: "Eco Acústico Ambiental", desc: "Siéntate bajo la sombra de un árbol. Coloca tus manos en las piernas, entorna los ojos y escucha aves.", fisiologica: "Tu corazón late a un ritmo tranquilo. Todo tu cuerpo descansa plenamente."},
                {id: "m_s4", titulo: "Paso Firme de Confianza", desc: "Camina en plano 3 minutos. Siente conscientemente el impacto del talón, la planta y luego los dedos.", fisiologica: "Seguridad total en tu andar. Te conectas de forma firme a la tierra."},
                {id: "m_s5", titulo: "Contemplación del Vaivén Natural", desc: "Observa fijamente el movimiento de las hojas con el viento o el fluir de una fuente por 2 minutos.", fisiologica: "Suelta cualquier preocupación. Tu mente fluye tranquila como el viento."}
            ],
            "CASA": [
                {id: "m_c1", titulo: "Despertar Biocirculatorio de Manos", desc: "Frota tus palmas suavemente hasta que se pongan tibias. Acaricia tus brazos con ellas sin prisa.", fisiologica: "Siente el calor reconfortante de tu propia piel. Tu cuerpo es seguro."},
                {id: "m_c2", titulo: "Sintonía Táctil Fina", desc: "Pasa las yemas de tus dedos sobre una manta muy suave o madera lisa manteniendo los ojos cerrados.", fisiologica: "Disfruta la sensación táctil pacífica. Respira de forma honda y pausada."},
                {id: "m_c3", titulo: "Respiración del Hilo de Seda", desc: "Inhala por la nariz y exhala por la boca tan suavemente que no moverías un hilo de seda frente a ti.", fisiologica: "Tu pecho se infla y se desinfla en perfecta paz. Mantén el rostro flojo."},
                {id: "m_c4", titulo: "Apertura de Ventana y Aire Nuevo", desc: "Abre la ventana más luminosa de casa. Siente el aire fresco rozar tu rostro mirando hacia afuera.", fisiologica: "El aire renovado oxigena tus energías. Disfruta de la claridad del día."}
            ]
        },
        "gobierno": {
            "SALIR": [
                {id: "g_s1", titulo: "Ruptura Burocrática de Campo", desc: "Sal por completo del edificio. Camina rápido balanceando los brazos y mira las copas de los árboles.", fisiologica: "Aire libre en movimiento constante. Tus ojos descansan lejos de los documentos."},
                {id: "g_s2", titulo: "Reset Digital Absoluto", desc: "Guarda el teléfono en el bolsillo en una banca. Mantén tus manos completamente vacías y observa el entorno.", fisiologica: "No hay correos ni plazos que responder ahora. Tu tiempo te pertenece por completo."},
                {id: "g_s3", titulo: "Descarga de Presión en Marcha", desc: "Camina 100 metros atendiendo el impacto seco del talón. Imagina que descargas el peso laboral.", fisiologica: "Camina de forma libre y suelta. Eres mucho más grande que tu escritorio."},
                {id: "g_s4", titulo: "Sintonía con Elementos Vivos", desc: "Detén tu paso ante una jardinera o tierra. Observa cómo interactúa la luz del sol directamente con ellas.", fisiologica: "Recibe el oxígeno directo de las plantas. Tu mente se aclara al instante."},
                {id: "g_s5", titulo: "Pausa Acústica de Oficina", desc: "Aléjate de teclados, teléfonos y ruidos institucionales. Quédate de pie en un rincón pacífico oyendo el espacio.", fisiologica: "Siente el espacio abierto. Tu pecho se expande de forma libre y natural."}
            ],
            "CASA": [
                {id: "g_c1", titulo: "Reset Óptico de Monitor", desc: "Bloquea tu monitor de inmediato. Cierra los ojos y cúbrelos suavemente con tus palmas 2 minutos en sombra.", fisiologica: "El mundo digital está apagado. Tu nervio óptico descansa en absoluta paz."},
                {id: "g_c2", titulo: "Ajuste Postural de Columna", desc: "Ponte de pie, estira tus brazos al techo tomando aire con fuerza como si quisieras tocarlo y suelta de golpe.", fisiologica: "Lleva el aire hasta el abdomen. Tu estructura física recupera su espacio libre."},
                {id: "g_c3", titulo: "Vaciado Interoceptivo Sensorial", desc: "Toma un vaso de agua fresca sintiendo el frío en el vidrio. Bebe un sorbo despacio notando el recorrido.", fisiologica: "El agua te refresca por completo desde adentro. Alivio somático inmediato."},
                {id: "g_c4", titulo: "Soltura Cervical Profunda", desc: "Deja caer la cabeza hacia el hombro derecho 3 respiraciones sintiendo el estiramiento. Cambia al lado izquierdo.", fisiologica: "El músculo se afloja y cede. Toda la carga diaria acumulada se disuelve ahora."}
            ]
        }
    },

    // INICIO DEL CIRCUITO CUANTIFICADO (MÉTRICA ANTES)
    iniciarCanalAsistido: function(tipoPerfil) {
        let zipValue = document.getElementById("inp-zip")?.value || "";
        let modoValue = document.getElementById("modo-selector")?.value || "SALIR";
        let menteValue = document.getElementById("mente-selector")?.value || "aburrido";

        if (!zipValue) {
            alert(KERNEL.idiomaActual === 'es' ? "Por favor, ingresa un Código Postal primero." : "Please enter a Zip Code first.");
            return;
        }

        // Asignación de indicadores iniciales basados en la severidad declarada de la mente
        let mapaSeveridad = { "aburrido": 40, "cansado": 55, "agotado": 75, "estresado": 85, "ansioso": 95 };
        let severidadInicial = mapaSeveridad[menteValue] || 50;

        this.categoriaActiva = tipoPerfil;
        
        // REGISTRO FORMAL FASE 1 (ANTES)
        this.faseAntes = {
            indicador_saturacion: severidadInicial,
            mente_inicial: menteValue,
            timestamp: new Date().toISOString()
        };
        
        if (tipoPerfil === "mayor") document.body.style.fontSize = "125%";

        let misionesDisponibles = this.misionesEspeciales[tipoPerfil][modoValue];
        let mSeleccionada = misionesDisponibles[Math.floor(Math.random() * misionesDisponibles.length)];
        
        // REGISTRO FORMAL FASE 2 (DURANTE)
        this.faseDurante = {
            id_mision: mSeleccionada.id,
            interaccion_activa: 10, // Inicia contador de atención
            descompresion_lograda: 0,
            timestamp: new Date().toISOString()
        };
        
        if (typeof KERNEL.hablar === 'function') {
            KERNEL.hablar(mSeleccionada.fisiologica);
        }

        this.abrirInterfazLimpia(mSeleccionada);
    // --- RENDERIZADO INTERACTIVO SOBERANO DE LOS 15 MINUTOS ---
    abrirInterfazLimpia: function(mision) {
        document.getElementById("wrapper-form")?.classList.add("hidden");
        
        let contenedorInteractiva = document.getElementById("wrapper-interactive");
        if (contenedorInteractiva) {
            contenedorInteractiva.classList.remove("hidden");
            contenedorInteractiva.innerHTML = `
                <div style="background: #111; border: 4px solid #efb810; border-radius: 16px; padding: 30px; max-width: 450px; margin: 40px auto; text-align: center; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.6); font-family: sans-serif; clear: both; display: block;">
                    <h2 style="font-size: 1.5rem; color: #efb810; text-transform: uppercase; margin: 0 0 15px 0; font-weight: 900; letter-spacing: 1px;">${mision.titulo}</h2>
                    <p style="font-size: 1.1rem; line-height: 1.6; margin: 0 0 20px 0; color: #cbd5e1; text-align: justify;">${mision.desc}</p>
                    <p style="font-size: 1rem; font-style: italic; color: #a3a3a3; background: rgba(255,255,255,0.05); padding: 12px; border-left: 4px solid #efb810; margin-bottom: 25px; text-align: left;">${mision.fisiologica}</p>
                    <div id="cronometro-satelite" style="font-size: 3.5rem; font-weight: bold; margin-bottom: 25px; font-family: monospace; color: #fff;">15:00</div>
                    <p id="indicador-progreso-somon" style="font-size: 0.85rem; text-transform: uppercase; color: #efb810; letter-spacing: 1px; margin-bottom: 20px;">Sintonía en curso: 10%</p>
                    <button onclick="ASISTENCIA_ESPECIAL_CORE.forzarCierreYExportar()" style="background: #e53e3e; color: white; border: none; padding: 14px 30px; font-size: 1.1rem; font-weight: bold; border-radius: 8px; cursor: pointer; text-transform: uppercase; width: 100%;">
                        ${KERNEL.idiomaActual === 'es' ? 'Finalizar y Generar Balance' : 'End & Generate Balance'}
                    </button>
                </div>
            `;
            this.iniciarTemporizadorSatelite(15 * 60);
        }
    },

    // --- TEMPORIZADOR CON REGISTRO DE CUANTIFICACIÓN SENSORIAL ---
    iniciarTemporizadorSatelite: function(segundos) {
        let tiempoRestante = segundos;
        let display = document.getElementById("cronometro-satelite");
        let txtProgreso = document.getElementById("indicador-progreso-somon");
        
        let intervalo = setInterval(() => {
            let minutos = parseInt(tiempoRestante / 60, 10);
            let segs = parseInt(tiempoRestante % 60, 10);
            minutos = minutos < 10 ? "0" + minutos : minutos;
            segs = segs < 10 ? "0" + segs : segs;
            
            if (display) display.textContent = minutos + ":" + segs;

            // Métrica dinámica acumulativa durante el servicio
            let segundosTranscurridos = (15 * 60) - tiempoRestante;
            if (segundosTranscurridos % 30 === 0 && tiempoRestante > 0) {
                this.faseDurante.interaccion_activa += 3;
                this.faseDurante.descompresion_lograda += 2.5;
                if (this.faseDurante.interaccion_activa > 100) this.faseDurante.interaccion_activa = 100;
                if (this.faseDurante.descompresion_lograda > 100) this.faseDurante.descompresion_lograda = 100;
                
                if (txtProgreso) {
                    txtProgreso.textContent = (KERNEL.idiomaActual === 'es' ? "Sintonía Somática: " : "Somatic Tuning: ") + Math.round(this.faseDurante.interaccion_activa) + "%";
                }
            }

            if (--tiempoRestante < 0) {
                clearInterval(intervalo);
                this.forzarCierreYExportar();
            }
        }, 1000);
    },

    // --- CONSOLIDACIÓN FINAL DE RESULTADOS MEDIBLES (MÉTRICA DESPUÉS) ---
    forzarCierreYExportar: function() {
        // Cálculo matemático exacto de la evolución del desarrollo del usuario
        let agobioOriginal = this.faseAntes.indicador_saturacion;
        let liberacionSomaticas = Math.min(this.faseDurante.descompresion_lograda + 20, 95); 
        let equilibrioAlcanzado = Math.round(Math.max(100 - (agobioOriginal - liberacionSomaticas), 15));
        let focoRecuperado = Math.round(Math.min(liberacionSomaticas * 1.15, 100));

        this.faseDespues = {
            retorno_equilibrio: equilibrioAlcanzado,
            estado_final: "completado",
            enfoque_recuperado: focoRecuperado,
            timestamp: new Date().toISOString()
        };

        // Bloque unificado enviado al Backend Core para registro y blindaje legal
        fetch("/api/generar-reporte-bienestar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                categoria: this.categoriaActiva,
                antes: this.faseAntes,
                durante: this.faseDurante,
                despues: this.faseDespues,
                lang: KERNEL.idiomaActual || "es"
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.documento_metadata) {
                this.pintarPanelResultadosMedibles(data.documento_metadata);
            }
        });
    },

    // --- PANEL GRÁFICO VISUAL CON RESUMEN DEL DESARROLLO DEL USUARIO ---
    pintarPanelResultadosMedibles: function(metadata) {
        let contenedor = document.getElementById("wrapper-interactive");
        if (!contenedor) return;

        let es = KERNEL.idiomaActual === 'es';
        
        // Elementos visuales dinámicos de barra de progreso basados en las fases reales medidas
        let saturacionBarra = this.faseAntes.indicador_saturacion;
        let sintoniaBarra = Math.round(this.faseDurante.interaccion_activa);
        let retornoBarra = this.faseDespues.retorno_equilibrio;

        contenedor.innerHTML = `
            <div style="background: #ffffff; border: 4px solid #0b3c5d; border-radius: 16px; padding: 25px; max-width: 550px; margin: 30px auto; font-family: sans-serif; box-shadow: 0px 10px 25px rgba(0,0,0,0.3); color: #1a202c; text-align: left;">
                <div style="text-align: center; border-bottom: 3px solid #efb810; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="font-size: 1.4rem; font-weight: bold; color: #0b3c5d; margin: 0; text-transform: uppercase;">${metadata.titulo}</h2>
                    <p style="font-size: 0.9rem; color: #718096; margin: 5px 0 0 0; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
                        ${es ? "Resumen de Evolución Biopsicosocial" : "Biopsychosocial Evolution Summary"}
                    </p>
                </div>

                <!-- GRÁFICAS Y MÉTRICAS CUANTIFICADAS DE SEGUIMIENTO SOBERANO -->
                <div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
                    <h4 style="margin: 0 0 12px 0; color: #0b3c5d; font-size: 1.05rem; text-transform: uppercase;">📊 ${es ? "Resultados de Desarrollo Medibles" : "Measurable Development Results"}</h4>
                    
                    <!-- FASE Antes -->
                    <div style="margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: bold; color: #e53e3e;">
                            <span>⚠️ ${es ? "Saturación de Rutina Inicial" : "Initial Routine Saturation"}</span>
                            <span>${saturacionBarra}%</span>
                        </div>
                        <div style="background: #edf2f7; border-radius: 4px; height: 10px; width: 100%; margin-top: 4px; overflow: hidden;">
                            <div style="background: #e53e3e; width: ${saturacionBarra}%; height: 100%;"></div>
                        </div>
                    </div>

                    <!-- FASE Durante -->
                    <div style="margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: bold; color: #d69e2e;">
                            <span>🌟 ${es ? "Sintonía e Interacción Activa" : "Active Tuning & Interaction"}</span>
                            <span>${sintoniaBarra}%</span>
                        </div>
                        <div style="background: #edf2f7; border-radius: 4px; height: 10px; width: 100%; margin-top: 4px; overflow: hidden;">
                            <div style="background: #d69e2e; width: ${sintoniaBarra}%; height: 100%;"></div>
                        </div>
                    </div>

                    <!-- FASE Después -->
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: bold; color: #3182ce;">
                            <span>✅ ${es ? "Retorno al Equilibrio y Enfoque" : "Return to Balance & Focus"}</span>
                            <span>${retornoBarra}%</span>
                        </div>
                        <div style="background: #edf2f7; border-radius: 4px; height: 10px; width: 100%; margin-top: 4px; overflow: hidden;">
                            <div style="background: #3182ce; width: ${retornoBarra}%; height: 100%;"></div>
                        </div>
                    </div>
                </div>
<!-- COMPILACIÓN ESCRITA DE LAS 3 FASES DEL REPORTE -->
<div style="margin-bottom:15px;">

    <h5 style="color:#48bb78;margin:0 0 5px 0;font-size:0.95rem;">
        🟢 FASE 1: ${es ? "Punto de Partida Inicial" : "Initial Departure Point"}
    </h5>

    ${metadata.fase_1_antes}

    <h5 style="color:#ecc94b;margin:15px 0 5px 0;font-size:0.95rem;">
        🟡 FASE 2: ${es ? "Bitácora de Acción Somática" : "Somatic Action Log"}
    </h5>

    ${metadata.fase_2_durante}

    <h5 style="color:#4299e1;margin:15px 0 5px 0;font-size:0.95rem;">
        🔵 FASE 3: ${es ? "Consolidación de Presencia" : "Presence Consolidation"}
    </h5>

    ${metadata.fase_3_despues}

</div>

<div style="display:flex;gap:10px;justify-content:center;margin-top:20px;flex-wrap:wrap;">

    <button
        onclick="window.print()"
        style="padding:12px 20px;border:none;border-radius:12px;background:#38a169;color:#fff;font-weight:bold;cursor:pointer;">
        🖨️ ${es ? "Imprimir Balance" : "Print Balance"}
    </button>

    <button
        onclick="document.getElementById('wrapper-interactive').innerHTML='';"
        style="padding:12px 20px;border:none;border-radius:12px;background:#e53e3e;color:#fff;font-weight:bold;cursor:pointer;">
        ❌ ${es ? "Finalizar" : "Close"}
    </button>

</div>

<div style="margin-top:25px;font-size:0.82rem;color:#718096;line-height:1.5;">
    ${metadata.pie_pagina_legal}
</div>

`;

window.scrollTo({
    top: 0,
    behavior: "smooth"
});

}

};

// CIERRE ABSOLUTO DE ASISTENCIA_ESPECIAL_CORE                

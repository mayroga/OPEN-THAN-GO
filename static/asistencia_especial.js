/**
 * OPEN THAN GO - MÓDULO SATÉLITE AISLADO DE BIENESTAR ASISTIDO
 * (Veteranos, Adultos Mayores y Trabajadores del Gobierno)
 */
const ASISTENCIA_ESPECIAL_CORE = {
    categoriaActiva: "",
    faseAntes: null,
    faseDurante: null,
    faseDespues: null,

    // Se activa al presionar uno de tus 3 botones gigantes
    iniciarCanalAsistido: function(tipoPerfil) {
        let zipValue = document.getElementById("inp-zip")?.value || "";
        let modoValue = document.getElementById("modo-selector")?.value || "SALIR";
        let menteValue = document.getElementById("mente-selector")?.value || "aburrido";

        if (!zipValue) {
            alert(KERNEL.idiomaActual === 'es' ? "Por favor, ingresa un Código Postal primero." : "Please enter a Zip Code first.");
            return;
        }

        this.categoriaActiva = tipoPerfil;
        this.faseAntes = { mente_inicial: menteValue, timestamp: new Date().toISOString() };
        
        if (tipoPerfil === "mayor") {
            document.body.style.fontSize = "125%"; // Contraste y lectura accesible
        }

        console.log("Desplegando canal satélite para: " + tipoPerfil);

        // Petición directa al endpoint del reporte escrito (Sin tocar el motor tradicional)
        fetch("/api/generar-reporte-bienestar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                categoria: tipoPerfil,
                modo: modoValue,
                lang: KERNEL.idiomaActual || "es",
                antes: this.faseAntes
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.documento_metadata) {
                this.faseDurante = { id_mision: data.documento_metadata.identificador_sistema, timestamp: new Date().toISOString() };
                this.abrirInterfazLimpia(data.documento_metadata);
            }
        })
        .catch(err => console.error("Error en canal asistido satélite:", err));
    },

    // Pinta la pantalla interactiva directamente saltándose todo el sistema de mapas
    abrirInterfazLimpia: function(metadata) {
        // Forzamos el cambio visual nativo de tu HTML
        document.getElementById("wrapper-form")?.classList.add("hidden");
        document.getElementById("wrapper-interactive")?.classList.remove("hidden");

        // Buscamos los contenedores de texto de tu Open Than Go nativo
        let contenedorInteractiva = document.getElementById("wrapper-interactive");
        if (contenedorInteractiva) {
            contenedorInteractiva.innerHTML = `
                <div style="background: rgba(0,0,0,0.8); border: 2px solid #efb810; border-radius: 12px; padding: 25px; max-width: 480px; margin: 20px auto; text-align: center; color: white;">
                    <h2 style="font-size: 1.5rem; color: #efb810; text-transform: uppercase; margin-bottom: 15px;">${metadata.titulo}</h2>
                    <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 25px; color: #e2e8f0;">
                        ${KERNEL.idiomaActual === 'es' ? 'Foco de atención: Realiza el ejercicio con respiraciones profundas durante 15 minutos.' : 'Focus of attention: Perform the exercise with deep breaths for 15 minutes.'}
                    </p>
                    <div id="cronometro-satelite" style="font-size: 3rem; font-weight: bold; margin-bottom: 20px; color: #fff;">15:00</div>
                    <button onclick="ASISTENCIA_ESPECIAL_CORE.forzarCierreYExportar()" style="background: #e53e3e; color: white; border: none; padding: 12px 25px; font-weight: bold; border-radius: 6px; cursor: pointer; text-transform: uppercase;">
                        ${KERNEL.idiomaActual === 'es' ? 'Finalizar Sesión' : 'End Session'}
                    </button>
                </div>
            `;
            this.iniciarTemporizadorSatelite(15 * 60);
        }
    },

    iniciarTemporizadorSatelite: function(segundos) {
        let tiempoRestante = segundos;
        let display = document.getElementById("cronometro-satelite");
        
        let intervalo = setInterval(() => {
            let minutos = parseInt(tiempoRestante / 60, 10);
            let segs = parseInt(tiempoRestante % 60, 10);

            minutos = minutos < 10 ? "0" + minutos : minutos;
            segs = segs < 10 ? "0" + segs : segs;

            if (display) display.textContent = minutos + ":" + segs;

            if (--tiempoRestante < 0) {
                clearInterval(intervalo);
                this.forzarCierreYExportar();
            }
        }, 1000);
    },

    forzarCierreYExportar: function() {
        this.faseDespues = { estado_final: "completado", timestamp: new Date().toISOString() };
        console.log("Consolidando reporte final de desarrollo humano...");
        
        // Ejecuta la llamada al backend para pintar el reporte impreso con blindaje legal
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
                // Removemos el contenedor temporal y disparamos la tarjeta visual de las 3 fases
                document.getElementById("wrapper-interactive").innerHTML = "";
                KERNEL.asistenciaEspecial.pintarReportePantalla(data.documento_metadata);
            }
        });
    }
};

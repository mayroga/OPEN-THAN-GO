// OPEN THAN GO SYSTEM - Kernel Safety Guard V1.0
// Company: May Roga LLC
// File: static/kernel-safety.js
// Protección contra congelamientos, ciclos y errores de arranque

(function(){

    console.log("🛡️ OPEN THAN GO Safety Guard activo");

    // Captura errores globales sin romper la pantalla
    window.addEventListener("error",(event)=>{

        console.error(
            "🔥 Error capturado:",
            event.message,
            "Archivo:",
            event.filename,
            "Línea:",
            event.lineno
        );

    });


    // Captura errores de promesas
    window.addEventListener("unhandledrejection",(event)=>{

        console.error(
            "🔥 Promesa rota:",
            event.reason
        );

    });


    // Control de SpeechSynthesis para evitar acumulación de voces
    const vozOriginal=window.speechSynthesis;

    if(vozOriginal){

        let ultimoHabla=0;

        const hablarSeguro=vozOriginal.speak.bind(vozOriginal);

        vozOriginal.speak=function(msg){

            const ahora=Date.now();

            if(ahora-ultimoHabla<300){
                console.warn("⚠️ Voz bloqueada por exceso");
                return;
            }

            ultimoHabla=ahora;

            hablarSeguro(msg);

        };

    }


    // Detector de múltiples intervalos activos
    let intervalosActivos=0;

    const intervaloOriginal=window.setInterval;

    window.setInterval=function(fn,tiempo){

        intervalosActivos++;

        if(intervalosActivos>20){

            console.warn(
                "⚠️ Muchos intervalos activos:",
                intervalosActivos
            );

        }

        return intervaloOriginal(fn,tiempo);

    };


    const clearOriginal=window.clearInterval;

    window.clearInterval=function(id){

        if(intervalosActivos>0){
            intervalosActivos--;
        }

        return clearOriginal(id);

    };


    // Espera a que KERNEL exista
    window.addEventListener("load",()=>{

        setTimeout(()=>{

            console.log("🔎 Revisando Kernel...");

            if(typeof KERNEL==="undefined"){

                console.error(
                    "❌ KERNEL no fue creado. Revisar llaves o sintaxis en engine.js"
                );

                return;
            }


            console.log("✅ KERNEL detectado");


            const obligatorias=[
                "init",
                "hablar",
                "despacharOraculo",
                "inyectarBloquePreguntas",
                "destruirYReiniciar"
            ];


            obligatorias.forEach(funcion=>{

                if(typeof KERNEL[funcion]!=="function"){

                    console.error(
                        "❌ Falta función:",
                        funcion
                    );

                }else{

                    console.log(
                        "✅ OK:",
                        funcion
                    );

                }

            });


            // Limpieza preventiva de estados dañados
            try{

                if(localStorage.getItem("otg_bloque_secuencial")===null){

                    localStorage.setItem(
                        "otg_bloque_secuencial",
                        "0"
                    );

                }

            }catch(e){

                console.error(
                    "Error localStorage:",
                    e
                );

            }


        },1000);

    });


})();

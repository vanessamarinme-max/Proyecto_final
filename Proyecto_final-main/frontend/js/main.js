/**
 * Archivo de Funcionalidades Principales - Huellitas de Amor
 * Autor: Refugio Huellitas de Amor
 */

// URL base de tu backend (Flask / Servidor)
const API_URL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
    console.log("Huellitas de Amor: Script JS cargado correctamente.");

    saludarVisitante();
    configurarValidacionFormularios();
    configurarEnlacesWhatsApp();
    configurarAutenticacionAdmin();
    configurarTogglePassword();
    configurarFormularioAdopcion();
    configurarFormularioAdminPerrito();
    configurarFormularioAdminProducto();
    
    // Cargar catálogos dinámicamente si estamos en las páginas públicas
    cargarPerritosCatalogo();
    cargarProductosTienda();
});

/**
 * Muestra un mensaje en consola según la hora del día
 */
function saludarVisitante() {
    const hora = new Date().getHours();
    let saludo = "¡Bienvenido a Huellitas de Amor!";

    if (hora < 12) {
        saludo = "¡Buenos días! Gracias por visitar Huellitas de Amor.";
    } else if (hora < 18) {
        saludo = "¡Buenas tardes! Explora nuestros peluditos en adopción.";
    } else {
        saludo = "¡Buenas noches! Gracias por apoyar nuestro refugio.";
    }

    console.log(saludo);
}

/**
 * Valida el inicio de sesión conectándose con el backend mediante correo y contraseña
 */
function configurarAutenticacionAdmin() {
    const formLogin = document.querySelector("#form-login-admin");

    if (formLogin) {
        formLogin.addEventListener("submit", async function(evento) {
            evento.preventDefault(); 
            evento.stopPropagation();

            const correoIngresado = document.querySelector("#usuario").value.trim();
            const passwordIngresada = document.querySelector("#password").value.trim();

            try {
                // Petición POST al backend para validar las credenciales exactas
                const respuesta = await fetch(`${API_URL}/api/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        correo: correoIngresado,
                        password: passwordIngresada
                    })
                });

                const resultado = await respuesta.json();

                if (respuesta.ok) {
                    alert("¡Inicio de sesión exitoso! Redirigiendo al panel de administración...");
                    window.location.href = "dashboard-admin.html";
                } else {
                    alert("Acceso denegado: " + (resultado.error || "Credenciales incorrectas."));
                    document.querySelector("#password").value = "";
                    document.querySelector("#password").focus();
                }
            } catch (error) {
                console.error("Error al conectar con el servidor:", error);
                alert("No se pudo conectar con el servidor backend. Asegúrate de que el servidor esté encendido.");
            }
        });
    }
}

/**
 * Valida los campos requeridos en los demás formularios generales antes de enviarlos
 */
function configurarValidacionFormularios() {
    const formularios = document.querySelectorAll("form:not(#form-login-admin):not([action='adopcion.html']):not(.form-admin)");

    formularios.forEach((form) => {
        form.addEventListener("submit", async (evento) => {
            const inputsRequeridos = form.querySelectorAll("[required]");
            let formularioValido = true;

            inputsRequeridos.forEach((input) => {
                if (!input.value.trim()) {
                    formularioValido = false;
                    input.style.borderColor = "#D90429"; // Alerta visual en rojo
                } else {
                    input.style.borderColor = "#5B6470"; // Color normal
                }
            });

            if (!formularioValido) {
                evento.preventDefault();
                alert("Por favor, completa todos los campos requeridos antes de continuar.");
            }
        });
    });
}

/**
 * Captura los datos del formulario de adopción y los envía a MongoDB
 */
function configurarFormularioAdopcion() {
    const formAdopcion = document.querySelector("form[action='adopcion.html']");

    if (formAdopcion) {
        formAdopcion.addEventListener("submit", async function(evento) {
            evento.preventDefault();

            const datosAdopcion = {
                nombre: document.querySelector("#nombre").value.trim(),
                documento: document.querySelector("#documento").value.trim(),
                correo: document.querySelector("#correo").value.trim(),
                celular: document.querySelector("#celular").value.trim(),
                fecha: document.querySelector("#fecha").value,
                tamano: document.querySelector("input[name='tamano']:checked")?.value || "",
                tipo_vivienda: document.querySelector("#tipo_vivienda").value,
                cantidad_mascotas: document.querySelector("#cantidad_mascotas").value,
                programa: document.querySelector("#programa").value,
                comentarios: document.querySelector("#comentarios").value.trim()
            };

            try {
                const respuesta = await fetch(`${API_URL}/api/solicitudesAdopcion`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosAdopcion)
                });

                const resultado = await respuesta.json();

                if (respuesta.ok) {
                    alert("¡Solicitud de adopción guardada con éxito en la base de datos!");
                    formAdopcion.reset();
                } else {
                    alert("Error al guardar: " + (resultado.error || "Revisa los datos."));
                }
            } catch (error) {
                console.error("Error de red:", error);
                alert("No se pudo conectar con el servidor backend.");
            }
        });
    }
}

/**
 * Registra un nuevo perrito desde el Panel Admin y lo guarda en MongoDB (colección 'perros')
 * Soporta tanto si el formulario usa id="form-perrito" como si usa action="perritos.html"
 */
function configurarFormularioAdminPerrito() {
    const formPerrito = document.querySelector("#form-perrito") || document.querySelector("form[action='perritos.html']");

    if (formPerrito) {
        formPerrito.addEventListener("submit", async function(evento) {
            evento.preventDefault();

            const datosPerrito = {
                nombre: document.querySelector("#nombre_perrito").value.trim(),
                edad: document.querySelector("#edad_perrito").value.trim(),
                sexo: document.querySelector("#sexo_perrito").value,
                tamano: document.querySelector("#tamano_perrito").value,
                descripcion: document.querySelector("#descripcion_perrito").value.trim(),
                estado: "En adopción"
            };

            try {
                const respuesta = await fetch(`${API_URL}/api/perros`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosPerrito)
                });

                const resultado = await respuesta.json();

                if (respuesta.ok) {
                    alert("¡Perrito registrado y guardado en MongoDB con éxito!");
                    formPerrito.reset();
                } else {
                    alert("Error al registrar perrito: " + (resultado.error || ""));
                }
            } catch (error) {
                console.error("Error de red:", error);
                alert("No se pudo conectar con el servidor backend.");
            }
        });
    }
}

/**
 * Registra un nuevo producto desde el Panel Admin y lo guarda en MongoDB (colección 'tienda')
 * Soporta tanto si el formulario usa id="form-producto" como si usa action="tienda.html"
 */
function configurarFormularioAdminProducto() {
    const formProducto = document.querySelector("#form-producto") || document.querySelector("form[action='tienda.html']");

    if (formProducto) {
        formProducto.addEventListener("submit", async function(evento) {
            evento.preventDefault();

            const datosProducto = {
                nombre: document.querySelector("#nombre_producto").value.trim(),
                categoria: document.querySelector("#categoria_producto").value,
                precio: Number(document.querySelector("#precio_producto").value),
                stock: Number(document.querySelector("#stock_producto").value),
                descripcion: document.querySelector("#descripcion_producto").value.trim()
            };

            try {
                // Modificado para guardar en la colección 'tienda'
                const respuesta = await fetch(`${API_URL}/api/tienda`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosProducto)
                });

                const resultado = await respuesta.json();

                if (respuesta.ok) {
                    alert("¡Producto registrado y guardado en la colección 'tienda' con éxito!");
                    formProducto.reset();
                } else {
                    alert("Error al registrar producto: " + (resultado.error || ""));
                }
            } catch (error) {
                console.error("Error de red:", error);
                alert("No se pudo conectar con el servidor backend.");
            }
        });
    }
}

/**
 * Consulta los perritos guardados en MongoDB y los dibuja en perritos.html
 */
async function cargarPerritosCatalogo() {
    const contenedor = document.querySelector("#contenedor-perritos");
    
    if (!contenedor) return;

    try {
        const respuesta = await fetch(`${API_URL}/api/perros`);
        const perritos = await respuesta.json();

        if (perritos.length === 0) return;

        contenedor.innerHTML = "";

        perritos.forEach(perro => {
            const article = document.createElement("article");
            article.className = "tarjeta-perrito";

            article.innerHTML = `
                <span class="etiqueta-estado">${perro.estado || "En adopción"}</span>
                <img src="../img/perrito-max.jpg" alt="${perro.nombre}" width="350">
                
                <h3>${perro.nombre}</h3>
                
                <ul class="datos-perrito">
                    <li><strong>Especie:</strong> Canino</li>
                    <li><strong>Edad:</strong> ${perro.edad}</li>
                    <li><strong>Tamaño:</strong> ${perro.tamano}</li>
                    <li><strong>Sexo:</strong> ${perro.sexo}</li>
                </ul>

                <p>${perro.descripcion}</p>

                <p><a href="adopcion.html" class="btn-cta">Quiero adoptar a ${perro.nombre}</a></p>
            `;

            contenedor.appendChild(article);
        });
    } catch (error) {
        console.error("Error al cargar perritos:", error);
    }
}

/**
 * Consulta los productos guardados en la colección 'tienda' y los dibuja en tienda.html
 */
async function cargarProductosTienda() {
    const contenedor = document.querySelector("#contenedor-tienda");
    
    if (!contenedor) return;

    try {
        // Consultamos a la colección 'tienda'
        const respuesta = await fetch(`${API_URL}/api/tienda`);
        const productos = await respuesta.json();

        if (productos.length === 0) return;

        contenedor.innerHTML = "";

        productos.forEach(prod => {
            const article = document.createElement("article");
            article.className = "tarjeta-servicio";

            const mensajeWS = encodeURIComponent(`Hola, quiero comprar el producto: ${prod.nombre}`);

            article.innerHTML = `
                <span class="etiqueta-nuevo">${prod.categoria}</span>
                <img src="../img/kit-aseo.jpg" alt="${prod.nombre}" width="350">
                
                <h3>${prod.nombre}</h3>

                <ul>
                    <li><strong>Categoría:</strong> ${prod.categoria}</li>
                    <li><strong>Precio:</strong> $${Number(prod.precio).toLocaleString()} COP</li>
                    <li><strong>Disponibles:</strong> ${prod.stock} unidades</li>
                </ul>

                <p>${prod.descripcion}</p>

                <p>
                    <a href="https://wa.me/573114231400?text=${mensajeWS}" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       class="btn-cta">Comprar por WhatsApp</a>
                </p>
            `;

            contenedor.appendChild(article);
        });
    } catch (error) {
        console.error("Error al cargar productos de la tienda:", error);
    }
}

/**
 * Muestra u oculta la contraseña al presionar el botón del icono de ojo
 */
function configurarTogglePassword() {
    const btnToggle = document.querySelector("#btn-toggle-password");
    const inputPassword = document.querySelector("#password");

    if (btnToggle && inputPassword) {
        btnToggle.addEventListener("click", () => {
            const esPassword = inputPassword.type === "password";
            
            inputPassword.type = esPassword ? "text" : "password";
            btnToggle.textContent = esPassword ? "🙈" : "👁️";
            btnToggle.setAttribute("aria-label", esPassword ? "Ocultar contraseña" : "Mostrar contraseña");
        });
    }
}

/**
 * Registra interacciones con los enlaces de WhatsApp
 */
function configurarEnlacesWhatsApp() {
    const botonesWhatsApp = document.querySelectorAll('a[href*="wa.me"]');

    botonesWhatsApp.forEach((boton) => {
        boton.addEventListener("click", () => {
            console.log("Redirigiendo a la línea de atención de WhatsApp de Huellitas de Amor...");
        });
    });
}

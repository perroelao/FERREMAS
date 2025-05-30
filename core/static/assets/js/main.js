// Espera a que todo el contenido del DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- Script para el menú móvil ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            // Alterna la clase 'hidden' para mostrar/ocultar el menú
            // Tailwind CSS usa la clase 'hidden' para display: none;
            mobileMenu.classList.toggle('hidden');

            // Opcional: Cambiar el ícono del botón (hamburguesa/cruz)
            // Esto requeriría dos SVGs o cambiar la ruta del SVG
            // Ejemplo simple:
            // if (mobileMenu.classList.contains('hidden')) {
            //     mobileMenuButton.innerHTML = '<svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>';
            // } else {
            //     mobileMenuButton.innerHTML = '<svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
            // }
        });
    } else {
        console.warn("No se encontraron los elementos del menú móvil (botón o menú).");
    }

    // --- Script para el año actual en el footer ---
    const currentYearElement = document.getElementById('currentYear');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    } else {
        console.warn("No se encontró el elemento para el año actual en el footer.");
    }

    // --- Simulación de "Añadir al Carrito" ---
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartCountElement = document.querySelector('.cart-count'); // Asegúrate que este selector sea único y correcto
    let cartItemCount = 0; // Podrías inicializar esto desde localStorage si guardas el carrito

    // Función para actualizar el contador visual del carrito
    function updateCartCountVisual() {
        if (cartCountElement) {
            cartCountElement.textContent = cartItemCount;
            if (cartItemCount > 0) {
                cartCountElement.classList.remove('hidden'); // Mostrar si tiene items
            } else {
                // Opcional: ocultar si está vacío, dependiendo del diseño
                // cartCountElement.classList.add('hidden');
            }
        }
    }

    // Inicializar el contador visual del carrito
    updateCartCountVisual();

    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Prevenir comportamiento por defecto si el botón está dentro de un <a>
            cartItemCount++;
            updateCartCountVisual();

            // Aquí añadirías la lógica real para agregar el producto al carrito:
            // 1. Obtener información del producto (ID, nombre, precio)
            //    Podrías usar atributos data-* en el botón o en el product-card
            //    const productId = button.closest('.product-card').dataset.productId;
            // 2. Guardar en localStorage, sessionStorage o enviar a un backend
            // 3. Mostrar una notificación/feedback al usuario

            // Simulación de feedback
            const productName = button.closest('.product-card')?.querySelector('h3')?.textContent || 'Producto';
            showTemporaryMessage(`${productName} añadido al carrito`, button);

            console.log(`Producto añadido. Total items: ${cartItemCount}`);
        });
    });

    // Función para mostrar un mensaje temporal cerca del botón
    function showTemporaryMessage(message, targetElement) {
        let messageElement = document.getElementById('cart-action-message');
        if (!messageElement) {
            messageElement = document.createElement('div');
            messageElement.id = 'cart-action-message';
            // Estilos básicos para el mensaje (puedes mejorarlos con CSS)
            messageElement.style.position = 'fixed';
            messageElement.style.bottom = '20px';
            messageElement.style.left = '50%';
            messageElement.style.transform = 'translateX(-50%)';
            messageElement.style.padding = '10px 20px';
            messageElement.style.backgroundColor = '#28a745'; // Verde éxito
            messageElement.style.color = 'white';
            messageElement.style.borderRadius = '5px';
            messageElement.style.zIndex = '1000';
            messageElement.style.opacity = '0';
            messageElement.style.transition = 'opacity 0.5s ease-in-out';
            document.body.appendChild(messageElement);
        }

        messageElement.textContent = message;
        messageElement.style.opacity = '1'; // Mostrar mensaje

        // Ocultar mensaje después de unos segundos
        setTimeout(() => {
            messageElement.style.opacity = '0';
        }, 3000); // 3 segundos
    }


    // --- Opcional: Smooth scroll para anclas (si las usas) ---
    // document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    //     anchor.addEventListener('click', function (e) {
    //         e.preventDefault();
    //         const targetId = this.getAttribute('href');
    //         const targetElement = document.querySelector(targetId);
    //         if (targetElement) {
    //             targetElement.scrollIntoView({
    //                 behavior: 'smooth'
    //             });
    //         }
    //     });
    // });

    // --- Opcional: Lazy loading para imágenes (mejora el rendimiento) ---
    // const lazyImages = document.querySelectorAll('img[data-src]');
    // const lazyImageObserver = new IntersectionObserver((entries, observer) => {
    //     entries.forEach(entry => {
    //         if (entry.isIntersecting) {
    //             const lazyImage = entry.target;
    //             lazyImage.src = lazyImage.dataset.src;
    //             lazyImage.removeAttribute('data-src'); // Para no volver a cargarla
    //             observer.unobserve(lazyImage);
    //         }
    //     });
    // });
    // lazyImages.forEach(lazyImage => {
    //     lazyImageObserver.observe(lazyImage);
    // });

    console.log("JavaScript de Mi Ferretería Online cargado y listo.");
});

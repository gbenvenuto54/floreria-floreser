// Activar tooltips de Bootstrap
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Smooth scrolling para enlaces de ancla
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Comportamiento de la barra de navegación al hacer scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar-main') || document.querySelector('.navbar');
    if (!navbar) return;

    if (window.scrollY > 100) {
        navbar.classList.add('shadow');
    } else {
        navbar.classList.remove('shadow');
    }
});

// Inicializar carruseles
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar carrusel de testimonios si existe
    const testimonialCarousel = document.querySelector('#testimonialCarousel');
    if (testimonialCarousel) {
        new bootstrap.Carousel(testimonialCarousel, {
            interval: 5000,
            wrap: true
        });
    }
    
    // Mostrar alertas con animación
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('show');
        }, 100);
        
        // Cerrar alertas automáticamente después de 5 segundos
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Manejo del contador del carrito
function updateCartCount() {
    // Aquí iría la lógica para actualizar el contador del carrito
    // Por ahora, lo dejamos vacío
}

// Llamar a la función cuando el documento esté listo
document.addEventListener('DOMContentLoaded', updateCartCount);
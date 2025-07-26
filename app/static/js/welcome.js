
document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.hero-slide');
    const dotsContainer = document.querySelector('.slider-dots');
    let current = 0;
    let interval;

    // Create dots
    slides.forEach((_, idx) => {
        const dot = document.createElement('div');
        dot.classList.add('slider-dot');
        if (idx === 0) dot.classList.add('active');
        dot.addEventListener('click', () => {
            goToSlide(idx);
            resetInterval();
        });
        dotsContainer.appendChild(dot);
    });
    const dots = document.querySelectorAll('.slider-dot');

    function goToSlide(idx) {
        slides[current].classList.remove('active');
        dots[current].classList.remove('active');
        current = idx;
        slides[current].classList.add('active');
        dots[current].classList.add('active');
    }

    function nextSlide() {
        goToSlide((current + 1) % slides.length);
    }

    function resetInterval() {
        clearInterval(interval);
        interval = setInterval(nextSlide, 5000);
    }

    if (slides.length > 0) {
        slides[0].classList.add('active');
        interval = setInterval(nextSlide, 5000);
    }

    const scrollIndicator = document.getElementById('scroll-indicator');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            scrollIndicator.style.opacity = '0';
        } else {
            scrollIndicator.style.opacity = '1';
        }
    });
}); 
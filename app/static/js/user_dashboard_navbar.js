document.addEventListener('DOMContentLoaded', function() {
    let lastScroll = window.scrollY;
    const navbar = document.querySelector('.navbar-welcome');
    window.addEventListener('scroll', function() {
        const currScroll = window.scrollY;
        if (currScroll > lastScroll && currScroll > 50) {
            navbar.classList.add('hide');
        } else {
            navbar.classList.remove('hide');
        }
        lastScroll = currScroll;
    });
}); 
// Mobile Menu Functionality
function toggleMobileMenu() {
    const navbarLinks = document.querySelector('.navbar-links');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    if (navbarLinks && toggle) {
        navbarLinks.classList.toggle('active');
        toggle.classList.toggle('active');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const navbarLinks = document.querySelector('.navbar-links');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    if (navbarLinks && toggle && !navbarLinks.contains(event.target) && !toggle.contains(event.target)) {
        navbarLinks.classList.remove('active');
        toggle.classList.remove('active');
    }
});

// Close mobile menu when clicking on a link
document.addEventListener('click', function(event) {
    if (event.target.tagName === 'A' && event.target.closest('.navbar-links')) {
        const navbarLinks = document.querySelector('.navbar-links');
        const toggle = document.querySelector('.mobile-menu-toggle');
        
        if (navbarLinks && toggle) {
            navbarLinks.classList.remove('active');
            toggle.classList.remove('active');
        }
    }
});

// Add mobile menu toggle button to navbar if it doesn't exist
document.addEventListener('DOMContentLoaded', function() {
    const navbarContainer = document.querySelector('.navbar-container');
    const existingToggle = document.querySelector('.mobile-menu-toggle');
    
    if (navbarContainer && !existingToggle) {
        const toggleButton = document.createElement('button');
        toggleButton.className = 'mobile-menu-toggle';
        toggleButton.onclick = toggleMobileMenu;
        toggleButton.innerHTML = `
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        `;
        
        // Insert the toggle button before the navbar-links
        const navbarLinks = navbarContainer.querySelector('.navbar-links');
        if (navbarLinks) {
            navbarContainer.insertBefore(toggleButton, navbarLinks);
        } else {
            navbarContainer.appendChild(toggleButton);
        }
    }
});

// Add animation classes to elements when they come into view
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate
    const animateElements = document.querySelectorAll('.card, .feature-card, .destination-card, .tour-card, .contact-card, .faq-item, .stat-item');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    addScrollAnimations();
});

// Add staggered animations to lists
function addStaggeredAnimations() {
    const staggerElements = document.querySelectorAll('.features-grid, .destinations-grid, .tours-grid, .contact-cards-container, .faq-grid, .stats-section');
    
    staggerElements.forEach(container => {
        if (container) {
            container.classList.add('animate-stagger');
        }
    });
}

// Initialize staggered animations
document.addEventListener('DOMContentLoaded', function() {
    addStaggeredAnimations();
});

// Add hover animations to interactive elements
function addHoverAnimations() {
    const hoverElements = document.querySelectorAll('.card, .feature-card, .destination-card, .tour-card, .contact-card, .btn');
    
    hoverElements.forEach(el => {
        if (el.classList.contains('card') || el.classList.contains('feature-card') || 
            el.classList.contains('destination-card') || el.classList.contains('tour-card') || 
            el.classList.contains('contact-card')) {
            el.classList.add('hover-lift');
        }
        
        if (el.classList.contains('btn')) {
            el.classList.add('hover-scale');
        }
    });
}

// Initialize hover animations
document.addEventListener('DOMContentLoaded', function() {
    addHoverAnimations();
}); 
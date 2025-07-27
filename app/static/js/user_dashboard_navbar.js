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

// Profile Dropdown JavaScript
function toggleProfileDropdown() {
    const dropdown = document.querySelector('.user-profile-dropdown');
    dropdown.classList.toggle('active');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.user-profile-dropdown');
    const profileButton = document.querySelector('.user-profile');
    
    if (!dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});

// Close dropdown when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const dropdown = document.querySelector('.user-profile-dropdown');
        dropdown.classList.remove('active');
    }
}); 
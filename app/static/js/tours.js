// Tours page functionality
function updateWishlistBadge() {
  fetch('/tours/wishlist/count')
    .then(res => res.json())
    .then(data => {
      document.querySelectorAll('.wishlist-badge').forEach(badge => {
        badge.textContent = data.wishlist_count;
      });
    });
}

function setWishlistButtonState(tourId) {
  const btn = document.getElementById('wishlist-toggle-btn');
  if (!btn) return;
  let inWishlist = false;
  if (window.isLoggedIn) {
    fetch(`/tours/wishlist/count`) // Not ideal, but for demo, check if count > 0 and update on click
      .then(() => {
        // For a real app, fetch the user's wishlist and check if tourId is in it
        // For now, just toggle on click
      });
  } else {
    const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
    inWishlist = wishlist.includes(String(tourId));
  }
  if (inWishlist) {
    btn.classList.remove('btn-wishlist-add');
    btn.classList.add('btn-wishlist-remove');
    btn.innerHTML = '<i class="fas fa-heart"></i> Remove from Wishlist';
  } else {
    btn.classList.remove('btn-wishlist-remove');
    btn.classList.add('btn-wishlist-add');
    btn.innerHTML = '<i class="fas fa-heart"></i> Add to Wishlist';
  }
}

function toggleWishlist(tourId) {
  if (window.isLoggedIn) {
    const btn = document.querySelector('.tour-wishlist-btn[data-tour-id="' + tourId + '"]');
    const isActive = btn && btn.classList.contains('active');
    const url = isActive ? `/tours/wishlist/remove/${tourId}` : `/tours/wishlist/add/${tourId}`;
    fetch(url, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        updateWishlistBadge();
        // Toggle the button state and icon
        if (btn) {
          btn.classList.toggle('active', !isActive);
          const icon = btn.querySelector('i');
          if (icon) {
            if (!isActive) {
              icon.classList.remove('far');
              icon.classList.add('fas');
            } else {
              icon.classList.remove('fas');
              icon.classList.add('far');
            }
          }
        }
      })
      .catch(error => {
        alert('Could not update wishlist. Please try again.');
        console.error(error);
      });
  } else {
    let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
    tourId = String(tourId);
    let inWishlist = wishlist.includes(tourId);
    if (inWishlist) {
      wishlist = wishlist.filter(id => id !== tourId);
    } else {
      wishlist.push(tourId);
    }
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    updateWishlistBadge();
    // Toggle the button state and icon
    const btn = document.getElementById('wishlist-toggle-btn') || document.querySelector('.tour-wishlist-btn[data-tour-id="' + tourId + '"]');
    if (btn) {
      btn.classList.toggle('active', !inWishlist);
      const icon = btn.querySelector('i');
      if (icon) {
        if (!inWishlist) {
          icon.classList.remove('far');
          icon.classList.add('fas');
        } else {
          icon.classList.remove('fas');
          icon.classList.add('far');
        }
      }
    }
  }
}

function setTourCardWishlistState() {
  document.querySelectorAll('.tour-wishlist-btn').forEach(btn => {
    const tourId = btn.dataset.tourId;
    let inWishlist = false;
    if (window.isLoggedIn) {
      // For logged-in users, rely on the backend-rendered .active class
      inWishlist = btn.classList.contains('active');
    } else {
      const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
      inWishlist = wishlist.includes(String(tourId));
    }
    if (inWishlist) {
      btn.classList.add('active');
      btn.querySelector('i').classList.remove('far');
      btn.querySelector('i').classList.add('fas');
    } else {
      btn.classList.remove('active');
      btn.querySelector('i').classList.remove('fas');
      btn.querySelector('i').classList.add('far');
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  updateWishlistBadge();
  setTourCardWishlistState();
  const btn = document.getElementById('wishlist-toggle-btn');
  if (btn) {
    const tourId = btn.dataset.tourId;
    setWishlistButtonState(tourId);
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      toggleWishlist(tourId);
    });
  }
  // Attach to all wishlist buttons on tour cards
  document.querySelectorAll('.tour-wishlist-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const tourId = this.dataset.tourId;
      if (window.isLoggedIn) {
        const isActive = this.classList.contains('active');
        const url = isActive ? `/tours/wishlist/remove/${tourId}` : `/tours/wishlist/add/${tourId}`;
        fetch(url, { method: 'POST' })
          .then(res => res.json())
          .then(data => {
            updateWishlistBadge();
            // Only toggle state after server confirms
            this.classList.toggle('active', !isActive);
            const icon = this.querySelector('i');
            if (icon) {
              if (!isActive) {
                icon.classList.remove('far');
                icon.classList.add('fas');
              } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
              }
            }
          });
      } else {
        let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
        let inWishlist = wishlist.includes(String(tourId));
        if (inWishlist) {
          wishlist = wishlist.filter(id => id !== String(tourId));
        } else {
          wishlist.push(String(tourId));
        }
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        updateWishlistBadge();
        // Toggle state visually
        this.classList.toggle('active', !inWishlist);
        const icon = this.querySelector('i');
        if (icon) {
          if (!inWishlist) {
            icon.classList.remove('far');
            icon.classList.add('fas');
          } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
          }
        }
      }
    });
  });
    // Get DOM elements
    const searchForm = document.querySelector('.search-filter-bar');
    const searchInput = document.querySelector('.search-input input');
    const categoryDropdown = document.querySelector('select[name="category"]');
    const durationDropdown = document.querySelector('select[name="duration"]');
    const applyFiltersBtn = document.querySelector('.apply-filters-btn');
    const tourCards = document.querySelectorAll('.tour-card');

    // Auto-submit form when dropdowns change (optional)
    if (categoryDropdown) {
        categoryDropdown.addEventListener('change', function() {
            // Uncomment the line below if you want auto-submit on dropdown change
            // searchForm.submit();
        });
    }

    if (durationDropdown) {
        durationDropdown.addEventListener('change', function() {
            // Uncomment the line below if you want auto-submit on dropdown change
            // searchForm.submit();
        });
    }

    // Apply filters button with visual feedback
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function(e) {
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }

    // Wishlist functionality
    tourCards.forEach(card => {
        const wishlistBtn = card.querySelector('.tour-wishlist');
        if (wishlistBtn) {
            wishlistBtn.addEventListener('click', function() {
                const heartIcon = this.querySelector('i');
                if (heartIcon.classList.contains('far')) {
                    heartIcon.classList.remove('far');
                    heartIcon.classList.add('fas');
                    // Add to wishlist logic here
                } else {
                    heartIcon.classList.remove('fas');
                    heartIcon.classList.add('far');
                    // Remove from wishlist logic here
                }
            });
        }
    });

    // Wishlist page: Remove from wishlist (AJAX, no redirect)
    document.querySelectorAll('.wishlist-remove-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const tourId = this.dataset.tourId;
        fetch(`/tours/wishlist/remove/${tourId}`, { method: 'POST' })
          .then(res => res.json())
          .then(data => {
            updateWishlistBadge();
            // Set heart to empty before removing card
            const icon = this.querySelector('i');
            if (icon) {
              icon.classList.remove('fas');
              icon.classList.add('far');
            }
            // Remove the card from the DOM
            const card = this.closest('.wishlist-tour-card');
            if (card) card.remove();
            // If no more cards, show the empty state
            if (document.querySelectorAll('.wishlist-tour-card').length === 0) {
              document.querySelector('.wishlist-tours-list').innerHTML =
                `<div class="wishlist-empty">
                  <div class="wishlist-empty-icon"><i class="fas fa-heart"></i></div>
                  <h2>Your wishlist is empty</h2>
                  <p>Start exploring our amazing tours and save your favorites for later!</p>
                  <a href="/tours" class="btn btn-book-now"><i class="fas fa-search"></i> Browse Tours</a>
                </div>`;
            }
          });
      });
    });

    // Attach to all wishlist buttons (tours page and detail page)
    document.querySelectorAll('.tour-wishlist-btn, #wishlist-toggle-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const tourId = this.dataset.tourId;
        const isActive = this.classList.contains('active') || this.classList.contains('btn-wishlist-remove');
        const url = isActive ? `/tours/wishlist/remove/${tourId}` : `/tours/wishlist/add/${tourId}`;
        fetch(url, { method: 'POST' })
          .then(res => res.json())
          .then(data => {
            updateWishlistBadge();
            // Toggle state after server confirms (no reload)
            this.classList.toggle('active', !isActive);
            this.classList.toggle('btn-wishlist-remove', !isActive);
            this.classList.toggle('btn-wishlist-add', isActive);
            const icon = this.querySelector('i');
            if (icon) {
              if (!isActive) {
                icon.classList.remove('far');
                icon.classList.add('fas');
              } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
              }
            }
            // If on detail page, update button text
            if (this.id === 'wishlist-toggle-btn') {
              this.innerHTML = `<i class="${!isActive ? 'fas' : 'far'} fa-heart"></i> ${!isActive ? 'Remove from Wishlist' : 'Add to Wishlist'}`;
            }
          });
      });
    });

    // Responsive behavior
    function handleResponsive() {
        const searchFilterBar = document.querySelector('.search-filter-bar');
        
        if (window.innerWidth <= 768) {
            searchFilterBar.style.flexDirection = 'column';
            searchFilterBar.style.gap = '12px';
        } else {
            searchFilterBar.style.flexDirection = 'row';
            searchFilterBar.style.gap = '16px';
        }
    }

    // Initialize responsive behavior
    handleResponsive();
    window.addEventListener('resize', handleResponsive);

    // Add smooth transitions to tour cards
    tourCards.forEach(card => {
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    });

    // Search input with debouncing (optional)
    let searchTimeout;
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Uncomment the line below if you want auto-search
                // searchForm.submit();
            }, 500);
        });
    }
}); 
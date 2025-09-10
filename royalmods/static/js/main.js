// Main JavaScript for RoyalMods

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Image carousel functionality
    setupImageCarousels();
    
    // Theme toggle functionality
    setupThemeToggle();
});

function initializeTheme() {
    const body = document.getElementById('body');
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme) {
        body.className = savedTheme;
    } else {
        // Default to dark mode
        body.className = 'dark-mode';
        localStorage.setItem('theme', 'dark-mode');
    }
    
    updateToggleButton();
}

function setupThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const body = document.getElementById('body');
            const isDarkMode = body.classList.contains('dark-mode');
            
            if (isDarkMode) {
                body.className = 'light-mode';
                localStorage.setItem('theme', 'light-mode');
            } else {
                body.className = 'dark-mode';
                localStorage.setItem('theme', 'dark-mode');
            }
            
            updateToggleButton();
        });
    }
}

function updateToggleButton() {
    const toggleBtn = document.getElementById('theme-toggle');
    const body = document.getElementById('body');
    
    if (toggleBtn) {
        const icon = toggleBtn.querySelector('.toggle-icon');
        const text = toggleBtn.querySelector('.toggle-text');
        const isDarkMode = body.classList.contains('dark-mode');
        
        if (isDarkMode) {
            icon.textContent = '☀️';
            text.textContent = 'Light Mode';
        } else {
            icon.textContent = '🌙';
            text.textContent = 'Dark Mode';
        }
    }
}

function setupImageCarousels() {
    const modCards = document.querySelectorAll('.mod-card');
    
    modCards.forEach(function(card) {
        const mainImage = card.querySelector('.mod-main-image');
        const thumbnails = card.querySelectorAll('.mod-thumbnail');
        
        if (mainImage && thumbnails.length > 0) {
            let currentIndex = 0;
            const images = [mainImage.src, ...Array.from(thumbnails).map(thumb => thumb.src)];
            
            // Click on main image to go to next
            mainImage.addEventListener('click', function() {
                currentIndex = (currentIndex + 1) % images.length;
                mainImage.src = images[currentIndex];
            });
            
            // Click on thumbnails to swap
            thumbnails.forEach(function(thumbnail, index) {
                thumbnail.addEventListener('click', function() {
                    const oldSrc = mainImage.src;
                    mainImage.src = thumbnail.src;
                    thumbnail.src = oldSrc;
                });
            });
        }
    });
}

// Helper function for image swapping (used in templates)
function swapImage(thumbnail, newSrc) {
    const mainImage = thumbnail.closest('.mod-card').querySelector('.mod-main-image');
    if (mainImage) {
        const oldSrc = mainImage.src;
        mainImage.src = newSrc;
        thumbnail.src = oldSrc;
    }
}
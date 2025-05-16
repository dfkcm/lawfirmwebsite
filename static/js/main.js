document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                }
            }
        });
    });
    
    // Refresh captcha
    const refreshCaptcha = document.querySelector('.refresh-captcha');
    const captchaImage = document.querySelector('.captcha-image');
    
    if (refreshCaptcha && captchaImage) {
        refreshCaptcha.addEventListener('click', function() {
            captchaImage.src = '/captcha?' + new Date().getTime();
        });
    }
    
    // Article search form submit
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchQuery = document.getElementById('searchQuery').value;
            const categorySelect = document.getElementById('categorySelect');
            const category = categorySelect ? categorySelect.value : '';
            
            let url = '/makaleler?';
            if (searchQuery) {
                url += 'search=' + encodeURIComponent(searchQuery);
            }
            
            if (category) {
                url += (searchQuery ? '&' : '') + 'category=' + encodeURIComponent(category);
            }
            
            window.location.href = url;
        });
    }
    
    // Category select change
    const categorySelect = document.getElementById('categorySelect');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const searchQuery = document.getElementById('searchQuery').value;
            const category = this.value;
            
            let url = '/makaleler?';
            if (category) {
                url += 'category=' + encodeURIComponent(category);
            }
            
            if (searchQuery) {
                url += (category ? '&' : '') + 'search=' + encodeURIComponent(searchQuery);
            }
            
            window.location.href = url;
        });
    }
    
    // Auto hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 5000);
    }
});

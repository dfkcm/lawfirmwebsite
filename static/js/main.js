document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const body = document.body;
    
    if (navToggle) {
        navToggle.addEventListener('click', function(e) {
            e.preventDefault();
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Menü açıkken sayfanın kaydırılmasını engelle
            if (navMenu.classList.contains('active')) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = '';
            }
        });

        // Menü dışına tıklandığında menüyü kapat
        document.addEventListener('click', function(e) {
            if (navMenu.classList.contains('active') && 
                !navMenu.contains(e.target) && 
                !navToggle.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.style.overflow = '';
            }
        });

        // ESC tuşuna basıldığında menüyü kapat
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.style.overflow = '';
            }
        });

        // Menü linklerine tıklandığında menüyü kapat
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.style.overflow = '';
            });
        });
    }
    
    // Sayfa geçişleri için AJAX
    function initializePageTransitions() {
        const mainContent = document.querySelector('.main-content');
        const navLinks = document.querySelectorAll('.nav-link');
        let currentPath = window.location.pathname;

        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetPath = this.getAttribute('href');
                
                // Aynı sayfaya tıklanırsa işlemi iptal et
                if (targetPath === currentPath) return;

                // Preloader'ı göster
                const preloader = document.createElement('div');
                preloader.id = 'preloader';
                preloader.innerHTML = `
                    <div class="loader-logo">
                        <img src="/static/img/new-logo.png" alt="Logo">
                    </div>
                `;
                document.body.appendChild(preloader);

                // İçeriği gizle
                mainContent.style.opacity = '0';

                // AJAX isteği
                fetch(targetPath)
                    .then(response => response.text())
                    .then(html => {
                        // Yeni HTML'i parse et
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newContent = doc.querySelector('.main-content').innerHTML;
                        
                        // URL'i güncelle
                        window.history.pushState({}, '', targetPath);
                        currentPath = targetPath;
                        
                        // Başlığı güncelle
                        document.title = doc.title;

                        // Mobil menüyü kapat
                        if (navMenu.classList.contains('active')) {
                            navMenu.classList.remove('active');
                        }

                        // İçeriği güncelle ve göster
                        setTimeout(() => {
                            mainContent.innerHTML = newContent;
                            
                            // AOS'u yeniden başlat ve zorla güncelle
                            if (typeof AOS !== 'undefined') {
                                AOS.init({ once: false });
                                AOS.refreshHard();
                            }

                            // Preloader'ı kaldır
                            preloader.classList.add('fade-out');
                            setTimeout(() => {
                                mainContent.style.opacity = '1';
                                preloader.addEventListener('transitionend', function() {
                                    preloader.remove();
                                });
                            }, 300);
                        }, 200);
                    })
                    .catch(error => {
                        console.error('Sayfa yüklenirken hata:', error);
                        window.location.href = targetPath;
                    });
            });
        });

        // Tarayıcının geri/ileri butonları için
        window.addEventListener('popstate', function() {
            window.location.reload();
        });
    }

    // Sayfa geçiş sistemini başlat
    initializePageTransitions();
    
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

    // Hero down arrow scroll
    const heroDownArrow = document.getElementById('heroDownArrow');
    const cardsSection = document.querySelector('.cards-section');
    if (heroDownArrow && cardsSection) {
        heroDownArrow.addEventListener('click', function() {
            cardsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    // Harita linki için cihaz kontrolü
    const mapsLink = document.querySelector('.maps-link');
    if (mapsLink) {
        mapsLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            // iOS cihaz kontrolü
            const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
            
            if (isIOS) {
                // iOS için Apple Maps
                window.open(this.getAttribute('data-apple-maps'), '_blank');
            } else {
                // Diğer cihazlar için Google Maps
                window.open(this.getAttribute('href'), '_blank');
            }
        });
    }

    // İletişim kutuları için tıklama işlevleri
    const contactItems = document.querySelectorAll('.contact-item');
    contactItems.forEach(item => {
        item.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            const googleMaps = this.getAttribute('data-google-maps');
            const appleMaps = this.getAttribute('data-apple-maps');
            
            if (action) {
                // Telefon veya e-posta için
                window.location.href = action;
            } else if (googleMaps && appleMaps) {
                // Harita için
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
                window.open(isIOS ? appleMaps : googleMaps, '_blank');
            }
        });
    });
});
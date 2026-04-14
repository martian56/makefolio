(function () {
    var html = document.documentElement;
    var themeToggle = document.getElementById('theme-toggle');
    var mobileMenuBtn = document.getElementById('mobile-menu-btn');
    var navbar = document.querySelector('.navbar');

    // --- Theme ---
    var saved = localStorage.getItem('theme') || html.getAttribute('data-theme') || 'light';
    applyTheme(saved);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('theme', next);
        });
    }

    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        if (!themeToggle) return;
        var sun = themeToggle.querySelector('.icon-sun');
        var moon = themeToggle.querySelector('.icon-moon');
        if (sun && moon) {
            sun.style.display = theme === 'dark' ? 'block' : 'none';
            moon.style.display = theme === 'dark' ? 'none' : 'block';
        }
    }

    // --- Mobile Menu ---
    if (mobileMenuBtn && navbar) {
        mobileMenuBtn.addEventListener('click', function () {
            navbar.classList.toggle('nav-open');
            var expanded = navbar.classList.contains('nav-open');
            mobileMenuBtn.setAttribute('aria-expanded', expanded);
        });

        document.querySelectorAll('.nav-links a').forEach(function (link) {
            link.addEventListener('click', function () {
                navbar.classList.remove('nav-open');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // --- Scroll Reveal ---
    var reveals = document.querySelectorAll('.reveal');
    if (reveals.length && 'IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

        reveals.forEach(function (el) { observer.observe(el); });
    } else {
        reveals.forEach(function (el) { el.classList.add('revealed'); });
    }

    // --- Skill Bar Animation ---
    var skillBars = document.querySelectorAll('.skill-progress');
    if (skillBars.length && 'IntersectionObserver' in window) {
        var skillObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    var bar = entry.target;
                    bar.style.width = bar.getAttribute('data-level') + '%';
                    skillObserver.unobserve(bar);
                }
            });
        }, { threshold: 0.2 });

        skillBars.forEach(function (bar) { skillObserver.observe(bar); });
    } else {
        skillBars.forEach(function (bar) {
            bar.style.width = bar.getAttribute('data-level') + '%';
        });
    }

    // --- Stat Counter Animation ---
    var statValues = document.querySelectorAll('.stat-value[data-count]');
    if (statValues.length && 'IntersectionObserver' in window) {
        var countObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    countObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statValues.forEach(function (el) { countObserver.observe(el); });
    }

    function animateCount(el) {
        var target = parseInt(el.getAttribute('data-count'), 10);
        var suffix = el.getAttribute('data-suffix') || '';
        var duration = 1200;
        var start = 0;
        var startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            var current = Math.floor(eased * (target - start) + start);
            el.textContent = current + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    }

    // --- Smooth Scroll ---
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var href = this.getAttribute('href');
            if (href === '#' || href === '#top') return;
            var target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // --- Navbar shadow on scroll ---
    var scrolled = false;
    window.addEventListener('scroll', function () {
        if (window.scrollY > 10 && !scrolled) {
            navbar.style.boxShadow = 'var(--shadow-md)';
            scrolled = true;
        } else if (window.scrollY <= 10 && scrolled) {
            navbar.style.boxShadow = 'none';
            scrolled = false;
        }
    }, { passive: true });
})();

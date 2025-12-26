(function() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Get saved theme or default
    const savedTheme = localStorage.getItem('theme') || html.getAttribute('data-theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateIcon(savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
    });
    
    function updateIcon(theme) {
        const icon = themeToggle.querySelector('.theme-icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '#top') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const offset = 80; // Account for fixed navbar
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
})();


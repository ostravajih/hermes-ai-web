// Language switching — no auto-redirect (handled server-side by Nginx)
// Only the manual switcher uses JavaScript for page reload
(function() {
    const LANG_KEY = 'hermes_lang';
    const path = window.location.pathname;
    const isEnPath = path.startsWith('/en/');

    window.switchLang = function(lang) {
        // Save preference as cookie (for Nginx) AND localStorage (for JS)
        localStorage.setItem(LANG_KEY, lang);
        document.cookie = LANG_KEY + "=" + lang + ";path=/;max-age=31536000;SameSite=Lax";
        
        let target;
        if (lang === 'en' && !isEnPath) {
            target = path === '/' ? '/en/' : '/en' + path;
        } else if (lang === 'cs' && isEnPath) {
            target = path.replace(/^\/en/, '') || '/';
        }
        if (target && target !== path) {
            window.location.href = target;
        }
    };

    // Mobile: clone lang/theme buttons into the nav menu
    document.addEventListener('DOMContentLoaded', function() {
        const navLinks = document.getElementById('navLinks');
        if (!navLinks) return;

        const langBtn = document.querySelector('.lang-switch');
        const themeBtn = document.querySelector('.theme-toggle');

        if (langBtn || themeBtn) {
            const extras = document.createElement('li');
            extras.className = 'mobile-extras';
            extras.style.listStyle = 'none';
            
            if (langBtn) {
                const langClone = langBtn.cloneNode(true);
                langClone.style.display = 'inline-flex';
                extras.appendChild(langClone);
            }
            if (themeBtn) {
                const themeClone = themeBtn.cloneNode(true);
                themeClone.style.display = 'inline-flex';
                extras.appendChild(themeClone);
            }
            
            navLinks.appendChild(extras);
        }
    });
})();

// Theme toggle
function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('themeIcon');
    const label = document.getElementById('themeLabel');
    const isDark = html.getAttribute('data-theme') === 'dark';

    if (isDark) {
        html.removeAttribute('data-theme');
        if (icon) icon.textContent = '🌙';
        if (label) label.textContent = document.documentElement.lang === 'cs' ? 'Tmavý' : 'Dark';
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-theme', 'dark');
        if (icon) icon.textContent = '☀️';
        if (label) label.textContent = document.documentElement.lang === 'cs' ? 'Světlý' : 'Light';
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme
(function() {
    const saved = localStorage.getItem('theme');
    const icon = document.getElementById('themeIcon');
    const label = document.getElementById('themeLabel');
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (icon) icon.textContent = '☀️';
        if (label) label.textContent = document.documentElement.lang === 'cs' ? 'Světlý' : 'Light';
    }
})();

// Close mobile menu on link click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            const navLinks = document.getElementById('navLinks');
            if (navLinks) navLinks.classList.remove('open');
        });
    });
});

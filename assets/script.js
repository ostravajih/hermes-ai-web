// Language detection and switching
(function() {
    const LANG_KEY = 'hermes_lang';
    const path = window.location.pathname;
    const isEnPath = path.startsWith('/en/');

    let storedLang = localStorage.getItem(LANG_KEY);

    if (!storedLang) {
        // First visit: detect from browser
        const browserLang = (navigator.language || '').split('-')[0];
        storedLang = (browserLang === 'cs' || browserLang === 'sk') ? 'cs' : 'en';
        localStorage.setItem(LANG_KEY, storedLang);
    }

    // Redirect if on wrong language version
    const needsEnPath = storedLang === 'en';
    if (needsEnPath !== isEnPath) {
        let target;
        if (needsEnPath) {
            target = path === '/' ? '/en/' : '/en' + path;
        } else {
            target = path.replace(/^\/en/, '') || '/';
        }
        window.location.replace(target);
        return;
    }

    // Language switcher function
    window.switchLang = function(lang) {
        localStorage.setItem(LANG_KEY, lang);
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

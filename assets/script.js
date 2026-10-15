// Language switching — no auto-redirect (handled server-side by Nginx)
// Only the manual switcher uses JavaScript for page reload
(function() {
    const LANG_KEY = 'hermes_lang';

    // Stránky, které mají v každém jazyce jinou adresu (ostatní jsou jen /en + cesta)
    const STRANKY_CS_EN = {
        '/instalace/': '/en/installation/',
        '/hosting/': '/en/hosting/',
        '/skills/': '/en/skills/',
        '/faq/': '/en/faq/',
        '/blog/': '/en/blog/',
        '/co-je-hermes/': '/en/what-is-hermes/',
        '/funkce/': '/en/features/',
        '/komunita/': '/en/community/'
    };
    // Články mají v každém jazyce vlastní adresu (název se překládá)
    const CLANKY_CS_EN = {
    'ai-agent-na-vps-contabo': 'ai-agent-on-vps-contabo',
    'bezpecnost-hermes-agent': 'hermes-agent-security',
    'hermes-agent-aktualizace-2026': 'hermes-agent-updates-2026',
    'hermes-agent-cron-planovac': 'hermes-agent-cron-scheduler',
    'hermes-agent-docker': 'hermes-agent-docker',
    'hermes-agent-google-gemini': 'hermes-agent-google-gemini',
    'hermes-agent-macos': 'hermes-agent-macos',
    'hermes-agent-mcp-integration': 'hermes-agent-mcp-integration',
    'hermes-agent-multi-platform': 'hermes-agent-multi-platform',
    'hermes-agent-nous-portal': 'hermes-agent-nous-portal',
    'hermes-agent-ollama-lokalni-llm': 'hermes-agent-ollama-local-llm',
    'hermes-agent-open-source': 'hermes-agent-open-source',
    'hermes-agent-openrouter': 'hermes-agent-openrouter',
    'hermes-agent-profily': 'hermes-agent-profiles',
    'hermes-agent-raspberry-pi': 'hermes-agent-raspberry-pi',
    'hermes-agent-soul-md': 'hermes-agent-soul-md',
    'hermes-agent-ssh-vps': 'hermes-agent-ssh-vps',
    'hermes-agent-system-admin': 'hermes-agent-system-admin',
    'hermes-agent-voice-mode': 'hermes-agent-voice-mode',
    'hermes-agent-vs-claude-code': 'hermes-agent-vs-claude-code',
    'hermes-agent-vs-codex': 'hermes-agent-vs-codex',
    'hermes-agent-vs-openclaw': 'hermes-agent-vs-openclaw',
    'hermes-agent-windows-wsl2': 'hermes-agent-windows-wsl2',
    'hermes-webui-pruvodce': 'hermes-webui-guide',
    'instalace-hermes-agent-ubuntu': 'install-hermes-agent-ubuntu',
    'jak-pouzivat-hermes-skills': 'how-to-use-hermes-skills',
    'telegram-bot-hermes-agent': 'telegram-bot-hermes-agent'
    };
    const STRANKY_EN_CS = {};
    Object.keys(STRANKY_CS_EN).forEach(k => { STRANKY_EN_CS[STRANKY_CS_EN[k]] = k; });
    const CLANKY_EN_CS = {};
    Object.keys(CLANKY_CS_EN).forEach(k => { CLANKY_EN_CS[CLANKY_CS_EN[k]] = k; });

    // Wiki má v každém jazyce vlastní adresu (název se překládá).
    // Sem se dopisuje každá nová stránka wiki, aby přepínač jazyka trefil protějšek.
    const WIKI_CS_EN = {
        '/wiki/': '/en/wiki/',
        '/wiki/zaciname/instalace/': '/en/wiki/getting-started/installation/'
    };
    const WIKI_EN_CS = {};
    Object.keys(WIKI_CS_EN).forEach(k => { WIKI_EN_CS[WIKI_CS_EN[k]] = k; });

    function cilovaAdresa(lang) {
        const cesta = window.location.pathname;
        const clanek = cesta.match(/^\/(?:en\/)?blog\/clanek\/([^/]+)\//);
        if (clanek) {
            const slug = clanek[1];
            if (lang === 'en') return CLANKY_CS_EN[slug] ? '/en/blog/clanek/' + CLANKY_CS_EN[slug] + '/' : '/en/blog/';
            return CLANKY_EN_CS[slug] ? '/blog/clanek/' + CLANKY_EN_CS[slug] + '/' : '/blog/';
        }
        if (lang === 'en') {
            if (WIKI_CS_EN[cesta]) return WIKI_CS_EN[cesta];
            // stránka wiki bez přeloženého protějšku → aspoň rozcestník wiki
            if (cesta.indexOf('/wiki/') === 0) return '/en/wiki/';
            return STRANKY_CS_EN[cesta] || (cesta === '/' ? '/en/' : '/en' + cesta);
        }
        if (WIKI_EN_CS[cesta]) return WIKI_EN_CS[cesta];
        if (cesta.indexOf('/en/wiki/') === 0) return '/wiki/';
        return STRANKY_EN_CS[cesta] || cesta.replace(/^\/en/, '') || '/';
    }

    window.switchLang = function(lang) {
        // Save preference as cookie (for Nginx) AND localStorage (for JS)
        localStorage.setItem(LANG_KEY, lang);
        document.cookie = LANG_KEY + "=" + lang + ";path=/;max-age=31536000;SameSite=Lax";
        const cesta = window.location.pathname;
        const target = cilovaAdresa(lang);
        if (target && target !== cesta) {
            window.location.href = target;
        } else {
            // Úvodní stránka je pro oba jazyky stejná adresa (jazyk se vybírá na serveru),
            // takže se stačí znovu načíst — cookie už je nastavená.
            window.location.reload();
        }
    };

    // Mobile: klon přepínače jazyka do mobilního menu.
    // (Přepínač světlého/tmavého režimu byl 15. 10. 2026 zrušen — web je vždy tmavý.)
    document.addEventListener('DOMContentLoaded', function() {
        const navLinks = document.getElementById('navLinks');
        if (!navLinks) return;

        const langBtn = document.querySelector('.lang-switch');

        if (langBtn) {
            const extras = document.createElement('li');
            extras.className = 'mobile-extras';
            extras.style.listStyle = 'none';

            const langClone = langBtn.cloneNode(true);
            langClone.style.display = 'inline-flex';
            extras.appendChild(langClone);

            navLinks.appendChild(extras);
        }
    });
})();

// Close mobile menu on link click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            const navLinks = document.getElementById('navLinks');
            if (navLinks) navLinks.classList.remove('open');
        });
    });

    // WebMCP: handle find_hermes_guide tool navigation
    var guideForm = document.querySelector('form[toolname="find_hermes_guide"]');
    if (guideForm) {
        guideForm.addEventListener('submit', function(e) {
            var select = this.querySelector('select[name="guide_type"]');
            if (select && select.value) {
                window.location.href = select.value;
            }
            e.preventDefault();
        });
    }
});

// WebMCP event listeners
window.addEventListener('toolactivated', function(e) {
    console.log('WebMCP tool activated:', e.toolName);
    var guideForm = document.querySelector('form[toolname="find_hermes_guide"]');
    if (guideForm && e.toolName === 'find_hermes_guide') {
        var select = guideForm.querySelector('select[name="guide_type"]');
        if (select && select.value) {
            window.location.href = select.value;
        }
    }
});
window.addEventListener('toolcancel', function(e) {
    console.log('WebMCP tool cancelled:', e.toolName);
});

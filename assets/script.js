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
        "/wiki/": "/en/wiki/",
        "/wiki/zaciname/instalace/": "/en/wiki/getting-started/installation/",
        "/wiki/zaciname/vyber-modelu/": "/en/wiki/getting-started/choosing-a-model/",
        "/wiki/zaciname/prvni-chat/": "/en/wiki/getting-started/first-chat/",
        "/wiki/zaciname/telegram-a-discord/": "/en/wiki/getting-started/telegram-and-discord/",
        "/wiki/zaciname/skilly/": "/en/wiki/getting-started/skills/",
        "/wiki/zaciname/pamet/": "/en/wiki/getting-started/memory/",
        "/wiki/zaciname/pravidelne-ulohy/": "/en/wiki/getting-started/scheduled-tasks/",
        "/wiki/zaciname/mcp-nastroje/": "/en/wiki/getting-started/mcp-tools/",
        "/wiki/zaciname/bezpecnost/": "/en/wiki/getting-started/security/",
        "/wiki/zaciname/kdyz-se-neco-pokazi/": "/en/wiki/getting-started/troubleshooting/",
        "/wiki/zaciname/caste-dotazy/": "/en/wiki/getting-started/faq/",
        "/wiki/zaciname/slovnicek/": "/en/wiki/getting-started/glossary/",
        "/wiki/funkce/nastroje/": "/en/wiki/features/tools/",
        "/wiki/funkce/profily/": "/en/wiki/features/profiles/",
        "/wiki/funkce/desktop/": "/en/wiki/features/desktop/",
        "/wiki/funkce/tui/": "/en/wiki/features/tui/",
        "/wiki/funkce/sezeni/": "/en/wiki/features/sessions/",
        "/wiki/funkce/podagenti/": "/en/wiki/features/subagents/",
        "/wiki/funkce/hlas/": "/en/wiki/features/voice/",
        "/wiki/funkce/email-kalendar/": "/en/wiki/features/email-and-calendar/",
        "/wiki/funkce/lokalni-modely/": "/en/wiki/features/local-models/",
        "/wiki/funkce/kontrolni-body/": "/en/wiki/features/checkpoints/",
        "/wiki/funkce/spousteni-prikazu/": "/en/wiki/features/command-execution/",
        "/wiki/funkce/kontextove-soubory/": "/en/wiki/features/context-files/",
        "/wiki/funkce/zalohy-a-obnova/": "/en/wiki/features/backups-and-restore/",
        "/wiki/funkce/pluginy/": "/en/wiki/features/plugins/",
        "/wiki/funkce/kurator-skills/": "/en/wiki/features/skill-curator/",
        "/wiki/funkce/import-z-jinych-agentu/": "/en/wiki/features/import-from-other-agents/",
        "/wiki/funkce/webhooky/": "/en/wiki/features/webhooks/",
        "/wiki/funkce/monitoring/": "/en/wiki/features/monitoring/",
        "/wiki/integrace/telegram/": "/en/wiki/integrations/telegram/",
        "/wiki/integrace/discord/": "/en/wiki/integrations/discord/",
        "/wiki/integrace/whatsapp/": "/en/wiki/integrations/whatsapp/",
        "/wiki/integrace/sms/": "/en/wiki/integrations/sms/",
        "/wiki/integrace/google-workspace/": "/en/wiki/integrations/google-workspace/",
        "/wiki/integrace/github/": "/en/wiki/integrations/github/",
        "/wiki/integrace/spravci-hesel/": "/en/wiki/integrations/password-managers/",
        "/wiki/integrace/hosting-a-domeny/": "/en/wiki/integrations/hosting-and-domains/",
        "/wiki/integrace/vlastni-aplikace-mcp/": "/en/wiki/integrations/your-app-via-mcp/",
    };
    const WIKI_EN_CS = {};
    Object.keys(WIKI_CS_EN).forEach(k => { WIKI_EN_CS[WIKI_CS_EN[k]] = k; });

    // Protějšek stránky v druhém jazyce je v hlavičce jako hreflang — je to jediné
    // místo, které zná skutečné adresy (blog má /blog/stranka/2/, anglicky
    // /en/blog/page/2/; články a wiki mají přeložené názvy). Přepínač ho proto
    // bere odsud a tabulky níž slouží jen jako záloha pro stránky bez hreflang.
    function zHreflangu(lang) {
        const link = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
        if (!link) return null;
        const cil = link.getAttribute('href');
        if (!cil) return null;
        try {
            const u = new URL(cil, window.location.origin);
            if (u.origin !== window.location.origin) return null;
            return u.pathname;
        } catch (e) { return null; }
    }

    function cilovaAdresa(lang) {
        const presna = zHreflangu(lang);
        if (presna) return presna;
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

    window.__hermesCilovaAdresa = cilovaAdresa;   // pro ověření, že přepínač míří správně

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

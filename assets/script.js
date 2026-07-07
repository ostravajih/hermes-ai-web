        // Theme toggle
        function toggleTheme() {
            const html = document.documentElement;
            const icon = document.getElementById('themeIcon');
            const label = document.getElementById('themeLabel');
            const isDark = html.getAttribute('data-theme') === 'dark';
            
            if (isDark) {
                html.removeAttribute('data-theme');
                icon.textContent = '🌙';
                label.textContent = 'Tmavý';
                localStorage.setItem('theme', 'light');
            } else {
                html.setAttribute('data-theme', 'dark');
                icon.textContent = '☀️';
                label.textContent = 'Světlý';
                localStorage.setItem('theme', 'dark');
            }
        }

        // Load saved theme
        (function() {
            const saved = localStorage.getItem('theme');
            if (saved === 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
                document.getElementById('themeIcon').textContent = '☀️';
                document.getElementById('themeLabel').textContent = 'Světlý';
            }
        })();

        // Close mobile menu on link click
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                document.getElementById('navLinks').classList.remove('open');
            });
        });

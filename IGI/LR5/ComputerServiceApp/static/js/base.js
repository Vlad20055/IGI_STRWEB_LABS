document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeText = document.querySelector('.theme-text');
    
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        if (themeToggle) themeToggle.checked = true;
        if (themeText) themeText.textContent = 'Светлая тема';
    } else {
        document.body.classList.remove('dark-theme');
        if (themeToggle) themeToggle.checked = false;
        if (themeText) themeText.textContent = 'Тёмная тема';
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark');
                if (themeText) themeText.textContent = 'Светлая тема';
            } else {
                document.body.classList.remove('dark-theme');
                localStorage.setItem('theme', 'light');
                if (themeText) themeText.textContent = 'Тёмная тема';
            }
        });
    }
});
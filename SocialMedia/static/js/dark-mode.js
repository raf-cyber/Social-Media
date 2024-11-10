// dark-mode.js
document.addEventListener('DOMContentLoaded', function () {
    // Check for saved theme in localStorage
    const prefersDarkMode = localStorage.getItem('theme') === 'dark';

    // Apply dark mode if the user preference is stored or system preference is dark
    if (prefersDarkMode || window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-mode');
    }

    // Select the toggle button
    const toggleButton = document.getElementById('dark-mode-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            
            // Save the theme preference to localStorage
            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                toggleButton.innerHTML = '🌞 Switch to Light Mode'; // Update button text to Light Mode
            } else {
                localStorage.setItem('theme', 'light');
                toggleButton.innerHTML = '🌙 Switch to Dark Mode'; // Update button text to Dark Mode
            }
        });
    }
});

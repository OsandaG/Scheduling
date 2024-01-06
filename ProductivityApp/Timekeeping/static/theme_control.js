document.addEventListener("DOMContentLoaded", function () {
    const darkModeToggle = document.getElementById("darkModeEnabled");

    // Check the user's preference and set dark mode if enabled
    if (localStorage.getItem("darkModeEnabled") === "true") {
        enableDarkMode();
    }

    // Toggle dark mode on checkbox change
    darkModeToggle.addEventListener("change", function () {
        if (this.checked) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    });

    function enableDarkMode() {
        document.documentElement.setAttribute("data-bs-theme", "dark");
        localStorage.setItem("darkModeEnabled", "true");
    }

    function disableDarkMode() {
        document.documentElement.setAttribute("data-bs-theme", "light");
        localStorage.setItem("darkModeEnabled", "false");
    }
});
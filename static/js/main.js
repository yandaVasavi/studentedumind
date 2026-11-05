
document.addEventListener("DOMContentLoaded", function () {

    // =================================
    // 1. DARK MODE / LIGHT MODE
    // =================================

    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");

    // Get previously saved theme
    const savedTheme = localStorage.getItem("edumind-theme");

    // Apply saved theme
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        themeIcon.textContent = "☀";
    } else {
        themeIcon.textContent = "☾";
    }

    // Change theme when button is clicked
    if (themeToggle) {
        themeToggle.addEventListener("click", function () {

            document.body.classList.toggle("dark-theme");

            if (document.body.classList.contains("dark-theme")) {

                localStorage.setItem("edumind-theme", "dark");
                themeIcon.textContent = "☀";

            } else {

                localStorage.setItem("edumind-theme", "light");
                themeIcon.textContent = "☾";

            }

        });
    }


    // =================================
    // 2. MOBILE NAVIGATION MENU
    // =================================

    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {

        menuToggle.addEventListener("click", function () {

            navLinks.classList.toggle("active");

            const isExpanded = navLinks.classList.contains("active");

            menuToggle.setAttribute("aria-expanded", isExpanded);

        });

    }

});

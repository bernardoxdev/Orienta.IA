document.querySelectorAll(".navbar .nav-link").forEach(link => {

    link.addEventListener("click", () => {

        const navbar = document.querySelector("#navbarMenu");

        if (navbar.classList.contains("show")) {
            bootstrap.Collapse
                .getOrCreateInstance(navbar)
                .hide();
        }

    });

});


const navbar = document.querySelector("#navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 30) {

        navbar.style.boxShadow =
            "0 5px 25px rgba(0, 0, 0, 0.30)";

    } else {

        navbar.style.boxShadow = "none";

    }

});
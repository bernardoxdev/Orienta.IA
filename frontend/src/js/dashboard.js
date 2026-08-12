document.addEventListener("DOMContentLoaded", () => {

    const sidebar =
        document.getElementById("sidebar");

    const mobileButton =
        document.getElementById("mobileMenuButton");


    /*
     * Menu mobile
     */

    if (mobileButton && sidebar) {

        mobileButton.addEventListener(
            "click",
            () => {

                sidebar.classList.toggle("open");

            }
        );

    }


    /*
     * Salvar projeto
     */

    document
        .querySelectorAll(".save-button")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const icon =
                        button.querySelector("i");


                    if (
                        icon.classList.contains(
                            "bi-bookmark"
                        )
                    ) {

                        icon.classList.remove(
                            "bi-bookmark"
                        );

                        icon.classList.add(
                            "bi-bookmark-fill"
                        );

                        button.style.color =
                            "var(--primary)";

                    } else {

                        icon.classList.remove(
                            "bi-bookmark-fill"
                        );

                        icon.classList.add(
                            "bi-bookmark"
                        );

                        button.style.color = "";

                    }

                }
            );

        });

});
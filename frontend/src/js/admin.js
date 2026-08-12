document.addEventListener("DOMContentLoaded", () => {

    const button =
        document.getElementById("notificationButton");

    const dropdown =
        document.getElementById("notificationDropdown");


    if (!button || !dropdown) {
        return;
    }


    /* =========================================
       ABRIR / FECHAR
    ========================================= */

    button.addEventListener("click", (event) => {

        event.stopPropagation();

        const isOpen =
            dropdown.classList.toggle("show");

        button.setAttribute(
            "aria-expanded",
            isOpen
        );

    });


    /* =========================================
       CLIQUE FORA
    ========================================= */

    document.addEventListener("click", (event) => {

        if (
            !dropdown.contains(event.target) &&
            !button.contains(event.target)
        ) {

            dropdown.classList.remove("show");

            button.setAttribute(
                "aria-expanded",
                "false"
            );

        }

    });


    /* =========================================
       MARCAR TODAS COMO LIDAS
    ========================================= */

    const markAll =
        document.getElementById(
            "markNotificationsRead"
        );


    if (markAll) {

        markAll.addEventListener(
            "click",
            async () => {

                try {

                    const response =
                        await fetch(
                            "/admin/notificacoes/marcar-lidas",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                }
                            }
                        );


                    if (!response.ok) {
                        throw new Error(
                            "Erro ao marcar notificações"
                        );
                    }


                    document
                        .querySelectorAll(
                            ".notification-item.unread"
                        )
                        .forEach(item => {

                            item.classList.remove(
                                "unread"
                            );

                            const dot =
                                item.querySelector(
                                    ".notification-unread"
                                );

                            if (dot) {
                                dot.remove();
                            }

                        });


                    const notificationDot =
                        document.querySelector(
                            ".notification-dot"
                        );


                    if (notificationDot) {
                        notificationDot.remove();
                    }


                    const headerText =
                        document.querySelector(
                            ".notification-header span"
                        );


                    if (headerText) {

                        headerText.textContent =
                            "Nenhuma nova";

                    }

                } catch (error) {

                    console.error(error);

                }

            }
        );

    }

    /*
     * =========================================
     * MENU MOBILE
     * =========================================
     */

    const sidebar =
        document.getElementById("adminSidebar");

    const mobileButton =
        document.getElementById("adminMobileButton");


    if (mobileButton && sidebar) {

        mobileButton.addEventListener(
            "click",
            () => {

                sidebar.classList.toggle("open");

            }
        );

    }


    /*
     * =========================================
     * CONFIRMAÇÃO DE EXCLUSÃO
     * =========================================
     */

    const deleteButtons =
        document.querySelectorAll(
            "[data-delete-url]"
        );


    const deleteModalElement =
        document.getElementById(
            "deleteModal"
        );


    if (
        deleteButtons.length &&
        deleteModalElement
    ) {

        const deleteModal =
            new bootstrap.Modal(
                deleteModalElement
            );


        const deleteForm =
            document.getElementById(
                "deleteForm"
            );


        const deleteName =
            document.getElementById(
                "deleteName"
            );


        deleteButtons.forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const url =
                        button.dataset.deleteUrl;

                    const name =
                        button.dataset.deleteName;


                    deleteForm.action = url;

                    deleteName.textContent =
                        name;


                    deleteModal.show();

                }
            );

        });

    }


    /*
     * =========================================
     * PESQUISA
     * =========================================
     */

    const search =
        document.getElementById(
            "globalSearch"
        );


    if (search) {

        search.addEventListener(
            "input",
            event => {

                const value =
                    event.target.value
                        .toLowerCase()
                        .trim();


                document
                    .querySelectorAll(
                        ".admin-table tbody tr"
                    )
                    .forEach(row => {

                        const text =
                            row.textContent
                                .toLowerCase();


                        row.style.display =
                            text.includes(value)
                                ? ""
                                : "none";

                    });

            }
        );

    }

});
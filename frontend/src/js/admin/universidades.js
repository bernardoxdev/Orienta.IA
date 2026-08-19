document.addEventListener("DOMContentLoaded", () => {
    // ========================================================
    // BUSCA E FILTRO
    // ========================================================
    const search = document.getElementById("universitySearch");
    const stateFilter = document.getElementById("stateFilter");
    const rows = document.querySelectorAll("#universitiesTableBody tr[data-name]");
    const count = document.getElementById("universitiesCount");

    function filterUniversities() {
        const searchValue = search.value.toLowerCase().trim();
        const stateValue = stateFilter.value;

        let visible = 0;

        rows.forEach(row => {
            const name = row.dataset.name;
            const sigla = row.dataset.sigla;
            const city = row.dataset.city;
            const state = row.dataset.state;

            const matchesSearch =
                !searchValue ||
                name.includes(searchValue) ||
                sigla.includes(searchValue) ||
                city.includes(searchValue);

            const matchesState =
                stateValue === "all" ||
                state === stateValue;

            const show = matchesSearch && matchesState;

            row.style.display = show ? "" : "none";

            if (show) {
                visible++;
            }
        });

        count.textContent =
            `${visible} universidade${visible !== 1 ? "s" : ""}`;
    }

    search.addEventListener("input", filterUniversities);
    stateFilter.addEventListener("change", filterUniversities);


    // ========================================================
    // MODAL — VISUALIZAR
    // ========================================================
    const modalVisualizar = document.getElementById("modalVisualizarUniversidade");

    if (modalVisualizar) {
        modalVisualizar.addEventListener("show.bs.modal", event => {
            const button = event.relatedTarget;

            const id = button.dataset.id;
            const nome = button.dataset.nome;
            const sigla = button.dataset.sigla;
            const cidade = button.dataset.cidade;
            const estado = button.dataset.estado;

            document.getElementById("visualizar_id").textContent =
                `#${id}`;

            document.getElementById("visualizar_nome").textContent =
                nome;

            document.getElementById("visualizar_sigla").textContent =
                sigla;

            document.getElementById("visualizar_cidade").textContent =
                cidade;

            document.getElementById("visualizar_estado").textContent =
                estado;
        });
    }


    // ========================================================
    // MODAL — EDITAR
    // ========================================================
    const modalEditar = document.getElementById("modalEditarUniversidade");

    if (modalEditar) {
        modalEditar.addEventListener("show.bs.modal", event => {
            const button = event.relatedTarget;

            const id = button.dataset.id;
            const nome = button.dataset.nome;
            const sigla = button.dataset.sigla;
            const cidade = button.dataset.cidade;
            const estado = button.dataset.estado;

            document.getElementById("editar_nome").value =
                nome;

            document.getElementById("editar_sigla").value =
                sigla;

            document.getElementById("editar_cidade").value =
                cidade;

            document.getElementById("editar_estado").value =
                estado;

            const form = document.getElementById(
                "formEditarUniversidade"
            );

            form.action =
                `/admin/universidades/${id}/editar`;
        });
    }


    // ========================================================
    // MODAL — EXCLUIR
    // ========================================================
    const deleteModalElement = document.getElementById("deleteUniversityModal");
    const deleteName = document.getElementById("deleteUniversityName");
    const deleteForm = document.getElementById("deleteUniversityForm");

    if (deleteModalElement && deleteName && deleteForm) {
        const deleteModal = new bootstrap.Modal(
            deleteModalElement
        );

        document
            .querySelectorAll("[data-delete-university]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    const name =
                        button.dataset.deleteUniversity;

                    const id =
                        button.dataset.deleteId;

                    deleteName.textContent = name;

                    deleteForm.action =
                        `/admin/universidades/${id}/excluir`;

                    deleteModal.show();
                });
            });
    }


    // ========================================================
    // NOTIFICAÇÕES
    // ========================================================
    const notificationButton = document.getElementById("notificationButton");
    const notificationDropdown = document.getElementById("notificationDropdown");
    const markNotificationsRead = document.getElementById("markNotificationsRead");

    if (notificationButton && notificationDropdown) {
        notificationButton.addEventListener(
            "click",
            event => {
                event.stopPropagation();

                const isOpen =
                    notificationDropdown.classList.contains(
                        "show"
                    );

                notificationDropdown.classList.toggle(
                    "show"
                );

                notificationButton.setAttribute(
                    "aria-expanded",
                    String(!isOpen)
                );
            }
        );

        document.addEventListener("click", event => {
            if (
                !notificationDropdown.contains(event.target) &&
                !notificationButton.contains(event.target)
            ) {
                notificationDropdown.classList.remove(
                    "show"
                );

                notificationButton.setAttribute(
                    "aria-expanded",
                    "false"
                );
            }
        });
    }


    // ========================================================
    // MARCAR NOTIFICAÇÕES COMO LIDAS
    // ========================================================
    if (markNotificationsRead) {
        markNotificationsRead.addEventListener(
            "click",
            () => {
                document
                    .querySelectorAll(
                        ".notification-item.unread"
                    )
                    .forEach(item => {
                        item.classList.remove("unread");

                        const indicator =
                            item.querySelector(
                                ".notification-unread"
                            );

                        if (indicator) {
                            indicator.remove();
                        }
                    });

                const dot = document.querySelector(
                    ".notification-dot"
                );

                if (dot) {
                    dot.remove();
                }
            }
        );
    }


    // ========================================================
    // MOBILE SIDEBAR
    // ========================================================
    const mobileButton = document.getElementById(
        "adminMobileButton"
    );

    const sidebar = document.getElementById(
        "adminSidebar"
    );

    if (
        mobileButton &&
        sidebar
    ) {
        mobileButton.addEventListener(
            "click",
            () => {
                sidebar.classList.toggle("show");
            }
        );
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const search = document.getElementById("userSearch");
    const typeFilter = document.getElementById("typeFilter");
    const statusFilter = document.getElementById("statusFilter");
    const rows = document.querySelectorAll("#usersTableBody tr[data-type]");
    const count = document.getElementById("usersCount");

    function filterUsers() {
        const searchValue = search.value.toLowerCase().trim();
        const typeValue = typeFilter.value;
        const statusValue = statusFilter.value;

        let visible = 0;

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const type = row.dataset.type;
            const status = row.dataset.status;
            const matchesSearch = !searchValue || text.includes(searchValue);
            const matchesType = typeValue === "all" || type === typeValue;
            const matchesStatus = statusValue === "all" || status === statusValue;
            const show = matchesSearch && matchesType && matchesStatus;

            row.style.display = show ? "" : "none";

            if (show) {
                visible++;
            }
        });

        count.textContent = `${visible} usuário${visible !== 1 ? "s" : ""}`;
    }

    search.addEventListener("input", filterUsers);
    typeFilter.addEventListener("change", filterUsers);
    statusFilter.addEventListener("change", filterUsers);

    const modalElement = document.getElementById("deleteUserModal");
    const modal = new bootstrap.Modal(modalElement);
    const deleteName = document.getElementById("deleteUserName");
    const deleteForm = document.getElementById("deleteUserForm");

    document.querySelectorAll("[data-delete-user]").forEach(button => {
        button.addEventListener("click", () => {
            const name = button.dataset.deleteUser;
            const id = button.dataset.deleteId;
            deleteName.textContent = name;
            deleteForm.action = `/admin/usuarios/${id}/excluir`;

            modal.show();
        });
    });

    document.querySelectorAll("[data-visualizar-user]").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.visualizarId;
            window.location.href = `/admin/usuarios/${id}/visualizar`;
        });
    });


    document.querySelectorAll("[data-editar-user]").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.editarId;
            window.location.href = `/admin/usuarios/${id}/editar`;
        });
    });


    // document.querySelectorAll("[data-message-user]").forEach(button => {
    //     button.addEventListener("click", () => {
    //         const id = button.dataset.messageId;
    //         window.location.href = `/admin/mensagens/nova/${id}`;
    //     });
    // });
});
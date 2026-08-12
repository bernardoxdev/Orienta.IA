function mostrarToast(mensagem, tipo = 'success') {
    const toastEl = document.getElementById('toastFeedback');
    const toastMessage = document.getElementById('toastMessage');

    toastMessage.textContent = mensagem;

    toastEl.classList.remove('bg-success', 'bg-danger', 'bg-primary');
    toastEl.classList.add(tipo === 'success' ? 'bg-success' : tipo === 'error' ? 'bg-danger' : 'bg-primary');

    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

document.addEventListener("DOMContentLoaded", () => {
    const roleInputs = document.querySelectorAll('input[name="tipo"]');
    const studentFields = document.getElementById("studentFields");
    const professorFields = document.getElementById("professorFields");


    function updateProfileFields() {
        const selected = document.querySelector('input[name="tipo"]:checked');

        if (!selected) {
            studentFields.style.display = "none";
            professorFields.style.display = "none";

            return;
        }

        if (selected.value === "estudante") {
            studentFields.style.display = "block";
            professorFields.style.display = "none";

            setStudentRequired(true);
            setProfessorRequired(false);
        }

        if (selected.value === "professor") {
            studentFields.style.display = "none";
            professorFields.style.display = "block";

            setStudentRequired(false);
            setProfessorRequired(true);
        }
    }

    function setStudentRequired(required) {
        const matricula = document.getElementById("matricula");

        matricula.required = required;
    }

    function setProfessorRequired(required) {
        const departamento = document.getElementById("departamento");

        departamento.required = required;
    }

    roleInputs.forEach(input => {
        input.addEventListener("change", updateProfileFields);
    });

    updateProfileFields();

    document.querySelectorAll(".password-toggle").forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.target;
            const input = document.getElementById(targetId);
            const icon = button.querySelector("i");

            if (input.type === "password") {
                input.type = "text";

                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            } else {
                input.type = "password";

                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");
            }
        });
    });

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", event => {
            const password = document.getElementById("password").value;
            const passwordConfirm = document.getElementById("password_confirm").value;

            if (password !== passwordConfirm) {
                event.preventDefault();

                mostrarToast("As senhas não coincidem.", "error");

                return;
            }


            if (password.length < 8) {
                event.preventDefault();

                mostrarToast("A senha deve ter pelo menos 8 caracteres.", "error");
            }
        });
    }
});
const tipoInputs = document.querySelectorAll(
    'input[name="tipo"]'
);

const estudanteSection =
    document.getElementById("estudanteSection");

const professorSection =
    document.getElementById("professorSection");


function atualizarTipo() {

    const tipo = document.querySelector(
        'input[name="tipo"]:checked'
    ).value;


    if (tipo === "estudante") {

        estudanteSection.classList.remove("d-none");

        professorSection.classList.add("d-none");

    }


    else {

        estudanteSection.classList.add("d-none");

        professorSection.classList.remove("d-none");

    }

}


tipoInputs.forEach(input => {

    input.addEventListener(
        "change",
        atualizarTipo
    );

});


atualizarTipo();


// =============================
// CONFIRMAÇÃO DE SENHA
// =============================

document
    .getElementById("novoUsuarioForm")
    .addEventListener("submit", function (event) {

        const senha =
            document.getElementById("senha").value;

        const confirmacao =
            document.getElementById(
                "senha_confirmacao"
            ).value;


        if (senha !== confirmacao) {

            event.preventDefault();

            alert("As senhas não coincidem.");

        }

    });
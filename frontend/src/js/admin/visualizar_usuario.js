const btnExcluir =
    document.getElementById("btnExcluir");

const modalElement =
    document.getElementById("modalExcluir");


if (btnExcluir && modalElement) {

    const modal =
        new bootstrap.Modal(modalElement);


    btnExcluir.addEventListener(
        "click",
        () => {

            modal.show();

        }
    );

}
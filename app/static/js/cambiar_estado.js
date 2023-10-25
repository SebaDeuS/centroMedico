function cambiarEstado(enlace) {
    if (enlace.textContent === "Deshabilitar") {
        enlace.textContent = "Habilitar";
        enlace.classList.remove("btn-danger");
        enlace.classList.add("btn-success");
    } else {
        enlace.textContent = "Deshabilitar";
        enlace.classList.remove("btn-success");
        enlace.classList.add("btn-danger");
    }
}

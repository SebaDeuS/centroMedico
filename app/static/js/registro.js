const form = document.getElementById("form");
const parrafo = document.getElementById("warnings");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  let warnings = "";
  let entrar = false;
  let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

  const rut = document.getElementById("rut");
  const nombre = document.getElementById("nombre");
  const email = document.getElementById("correo");
  const pass = document.getElementById("contraseña");
  const select = document.getElementById("select"); 

  if (rut.value.length >= 7 && rut.value.length <= 8) {
    console.log("Rut pulento");
  } else {
    warnings += "Rut invalido\n";
    entrar = true;
  }
  if (nombre.value.length < 3) {
    warnings += "Ingrese un nombre valido<br>";
    entrar = true;
  }
  if (!regexEmail.test(email.value)) {
    warnings += "El email no es valido<br>";
    entrar = true;
  }
  if (pass.value.length < 8) {
    warnings += "La clave no es valida<br>";
    entrar = true;
  }

  if (select.value === "Seleccione dv") {
    warnings += "Seleccione un dígito verificador<br>";
    entrar = true;
  }

  if (entrar) {
    parrafo.innerHTML = warnings;
  } else {
    var jsonData = {
      rut: rut.value,
      dv: select.value,
      nombre: nombre.value,
      correo: email.value,
      contraseña: pass.value,
    };

    var jsonString = JSON.stringify(jsonData);

    console.log(jsonString);
    alert("registro Exitoso")
  }
});

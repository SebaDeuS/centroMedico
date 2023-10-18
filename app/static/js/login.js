const form = document.getElementById("form");
const parrafo = document.getElementById("warnings");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    let warnings = "";
    let entrar = false;
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  
    const email = document.getElementById("correo");
    const pass = document.getElementById("contraseña");

  
    if (!regexEmail.test(email.value)) {
      warnings += "El email no es valido\n";
      entrar = true;
    }
    if (pass.value.length < 8) {
      warnings += "La clave no es valida\n";
      entrar = true;
    }
  
  
    if (entrar) {
      parrafo.innerHTML = warnings;
    } else {
      var jsonData = {
        correo: email.value,
        contraseña: pass.value,
      };
  
      var jsonString = JSON.stringify(jsonData);
  
      console.log(jsonString);
  
    }
  });
  
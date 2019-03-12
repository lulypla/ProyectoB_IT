function cedula(cedula) {
  let errores = [];
  if (typeof parseInt(cedula, 10) !== "integer") {
    errores.push("Cedula no es numerica");
  } else if (cedula.toString().length < 8) {
    errores.push("Largo invalido, si no es millones agregue un 0 adelante");
  }

  if (errores.length === 0) {
    return true;
  } else {
    return false;
  }
}

function iguales(arg1, arg2) {
  if (arg1 !== arg2) {
    return false;
  }
  return true;
}

function password(pass1, pass2) {
  // No se si quieres tambien alguna validacion por largo o elemntos de seguridad.
  return iguales(pass1, pass2);
}

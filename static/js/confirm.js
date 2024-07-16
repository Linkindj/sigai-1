
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('envir').addEventListener('click', function(e) {
      e.preventDefault();
      pregunta()
    });
  }); 
  function pregunta() {
    if (confirm('¿Estas seguro de enviar este registro?')) {
      document.getElementById('registro').submit();
    }
  }
  
  function pregunta() {
    if (confirm('¿Estas seguro de enviar este registro?')) {
      document.getElementById('registro_familia').submit();
    }
  }
  document.getElementById("toggleArrow").addEventListener("click", function() {
    var formulario = document.getElementById("formulario");
    formulario.classList.toggle("hidden");
    if (formulario.classList.contains("hidden")) {
        // Cambia la flecha a la derecha si el formulario está oculto
        document.getElementById("toggleArrow").innerHTML = "&#9658;";
    } else {
        // Cambia la flecha hacia abajo si el formulario está visible
        document.getElementById("toggleArrow").innerHTML = "&#9660;";
    }
});
$(document).ready(function() {
  $('#nextButton').click(function() {
      $('#module1').hide();
      $('#module2').show();
      $('#nextButton').hide();
      $('#prevButton').show();
  });

  $('#prevButton').click(function() {
      $('#module2').hide();
      $('#module1').show();
      $('#prevButton').hide();
      $('#nextButton').show();
  });
});
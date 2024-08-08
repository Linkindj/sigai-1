document.addEventListener('DOMContentLoaded', function() {
  // Función para manejar la eliminación con SweetAlert2
  const deleteLinks = document.querySelectorAll('.delete-link');
  deleteLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();  // Prevenir la acción predeterminada del enlace

      const href = this.getAttribute('href');  // Obtener la URL de eliminación

      Swal.fire({
        title: "Estás seguro de eliminarlo?",
        text: "Si eliminas este registro será de manera permanente",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText:"No",
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Si"
      }).then((result) => {
        if (result.isConfirmed) {
          // Redirigir manualmente al enlace de eliminación
          window.location.href = href;
        }
      });
    });
  });

  // Función para togglear el formulario y cambiar la flecha
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

  // Mostrar alerta de bienvenida si los parámetros están presentes
  const urlParams = new URLSearchParams(window.location.search);
  const showWelcome = urlParams.get('show_welcome');
  const username = urlParams.get('username');

  if (showWelcome && username) {
    Swal.fire({
      title: '¡Bienvenido!',
      text: `Bienvenido ${username}`,
      icon: 'success'
    });
  }
});

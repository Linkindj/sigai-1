 // Obtener el parámetro show_welcome de la URL
 const urlParams = new URLSearchParams(window.location.search);
 const showWelcome = urlParams.get('show_welcome');
 const username = urlParams.get('username');

 // Mostrar el alert si show_welcome está presente
 if (showWelcome && username) {
     Swal.fire({
         title: '¡Bienvenido!',
         text: `haz iniciado sesión como ${username}`,
         icon: 'success'
     });
 }
  const urlParams1 = new URLSearchParams(window.location.search);
  const showSave = urlParams.get('show_Save');
 
  if (showSave) {
      Swal.fire({
          title: '¡Enviado!',
          text: `Su solicitud fue enviada correctamente`,
          icon: 'success'
      });
  }

  const urlParams2 = new URLSearchParams(window.location.search);
  const showCita = urlParams.get('show_cita');
 
  if (showCita) {
      Swal.fire({
          title: '¡Enviado!',
          text: `Cita programada correctamente`,
          icon: 'success'
      });
  }


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
  const urlParams3 = new URLSearchParams(window.location.search);
  const showDelete = urlParams.get('show_Delete');
 
  if (showDelete) {
      Swal.fire({
          title: 'Eliminado',
          text: `El registro fue eliminado`,
          icon: 'success',
          confirmButtonText:'Aceptar'
      });
  }
  const urlParams4 = new URLSearchParams(window.location.search);
  const showEdit = urlParams.get('Show_Edit');
 
  if (showEdit) {
      Swal.fire({
          title: 'Guardado',
          text: `Sus datos han sido guardados con exito`,
          icon: 'success',
          confirmButtonText:'Aceptar'
      });
  }
  const urlParams5 = new URLSearchParams(window.location.search);
  const showpassFail = urlParams.get('Show_passFail');
 
  if (showpassFail) {
      Swal.fire({
          title: 'Error',
          text: `Las contraseñas ingresadas no coinciden    `,
          icon: 'error',
          confirmButtonText:'Aceptar'
      });
  }


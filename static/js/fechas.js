document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Meses van de 0 a 11
    const dd = String(today.getDate()).padStart(2, '0');

    const todayStr = `${yyyy}-${mm}-${dd}`;
    document.getElementById('fecha_sol').value = todayStr;
});

// filepath: static/js/confirmar-pedido.js
document.getElementById('metodo_pago_id').addEventListener('change', function() {
    const transferenciaDiv = document.getElementById('transferencia-info');
    if (this.value === '4') {
        transferenciaDiv.style.display = 'block';
    } else {
        transferenciaDiv.style.display = 'none';
    }
});
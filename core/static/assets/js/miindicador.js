document.getElementById('convert-to-usd').addEventListener('click', function() {
    fetch('https://mindicador.cl/api')
        .then(response => response.json())
        .then(indicadores => {
            const usdRate = indicadores.dolar.valor;
            const prices = document.querySelectorAll('.price');
            prices.forEach(priceElement => {
                const clpPrice = parseFloat(priceElement.textContent.replace('$', ''));
                const usdPrice = (clpPrice / usdRate).toFixed(2);
                priceElement.textContent = `$${usdPrice} USD`;
                priceElement.classList.remove('text-green-600');
                priceElement.classList.add('text-blue-600');
            });
        })
        .catch(error => {
            alert('No se pudo obtener el valor del dólar.');
        });
});
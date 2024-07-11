document.addEventListener('DOMContentLoaded', () => {
    // Inicializar la página con los precios en la moneda predeterminada
    actualizarPrecios();
});

function cambiarMoneda() {
    const selector = document.getElementById('currency-selector');
    monedaActual = selector.value; // Actualizar la moneda actual seleccionada
    actualizarPrecios(); // Actualizar los precios al cambiar la moneda
}

function actualizarPrecios() {
    const elementosPrecio = document.querySelectorAll('.precio');
    const elementosPrecioTotal = document.querySelectorAll('.precio-total');
    const totalPedidoElemento = document.getElementById('total-pedido');
    
    elementosPrecio.forEach(elemento => {
        const precioOriginal = parseFloat(elemento.getAttribute('data-precio-original'));
        const tasaDeCambio = monedaActual === 'CLP' ? 1 : tasasDeCambio[monedaActual];
        const precioConvertido = (precioOriginal / tasaDeCambio).toFixed(2);
        elemento.innerText = `${precioConvertido} ${monedaActual}`;
    });

    elementosPrecioTotal.forEach(elemento => {
        const precioOriginal = parseFloat(elemento.getAttribute('data-precio-original'));
        const tasaDeCambio = monedaActual === 'CLP' ? 1 : tasasDeCambio[monedaActual];
        const precioConvertido = (precioOriginal / tasaDeCambio).toFixed(2);
        elemento.innerText = `${precioConvertido} ${monedaActual}`;
    });

    if (totalPedidoElemento) {
        const totalPrecioOriginal = parseFloat(totalPedidoElemento.getAttribute('data-precio-original'));
        const totalPrecioConvertido = (totalPrecioOriginal / tasasDeCambio[monedaActual]).toFixed(2);
        totalPedidoElemento.innerText = `${totalPrecioConvertido} ${monedaActual}`;
    }
}

path('update-cart/', update_cart, name='update_cart'),


// Obtener todos los elementos "Eliminar Item" y agregar un controlador de eventos clic a cada uno
document.querySelectorAll('.remove-cart').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Evitar el comportamiento predeterminado del enlace

        // Obtener el ID del producto del atributo pid
        const productId = this.getAttribute('pid');

        // Realizar una solicitud POST al servidor para eliminar el elemento del carrito
        fetch(`/remove-from-cart?prod_id=${productId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}' // Agregar el token CSRF para protección contra falsificación de solicitudes entre sitios
            }
        })
        .then(response => {
            if (response.ok) {
                // Recargar la página después de eliminar el elemento del carrito
                window.location.reload();
            } else {
                // Manejar cualquier error que ocurra durante la solicitud
                console.error('Error al eliminar el elemento del carrito');
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    });
});


$(document).ready(function () {
    $(".minus-cart, .plus-cart").on("click", function (e) {
        e.preventDefault();
        var productId = $(this).attr("pid");
        var action = $(this).hasClass("minus-cart") ? "minus" : "plus";

        $.ajax({
            url: "/update-cart/",
            data: {
                prod_id: productId,
                action: action
            },
            type: "GET",
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    // Actualizar la cantidad en la interfaz de usuario
                    $("#cantidad").text(data.new_quantity);
                } else {
                    alert("Error: " + data.error);
                }
            }
        });
    });
});
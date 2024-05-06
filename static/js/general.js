const url_servidor= "http://127.0.0.1:5000";

function crearMensaje(titulo, mensaje, redireccion) {
    var $contenedor = $('#mensaje');
    var $overlay = $('#popup-overlay');

    var $popup = $('<div>').addClass('popup').addClass(titulo);
    var $popupTitulo = $('<h2>').text(titulo);
    var $popupMensaje = $('<p>').text(mensaje);
    var $closeButton = $('<button>').text('Cerrar').addClass('close-btn');

    $closeButton.on('click', function () {
        if (redireccion) {
            $popup.remove();
            $overlay.hide();
            window.location.href = redireccion;
        } else {
            $popup.remove();
            $overlay.hide();
        }
    });

    $popup.append($popupTitulo, $popupMensaje, $closeButton);
    $contenedor.append($popup);
    $overlay.show();
}
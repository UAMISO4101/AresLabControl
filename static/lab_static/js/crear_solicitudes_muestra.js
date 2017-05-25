function validateForm() {
    validarRequeridos(function (res) {
        if (res && validarCantidad()) {
            $("#formSolicitud").submit();
        }
    });
    return false;
}

function validarCantidad() {
    if ($("#id_cantidad").val() > parseInt($("#cantidadActual").text())) {
        $("#mensajes-error").append('<div class="alert alert-danger col-md-6"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            'La cantidad solicitada no puede ser mayor que la disponible</div>');
        return false;
    }
    if ($("#id_cantidad").val() <= 0) {
        $("#mensajes-error").append('<div class="alert alert-danger col-md-6"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            'La cantidad solicitada debe ser mayor que cero</div>');
        return false;
    }
    return true;
}

$(function () {
    $('#id_fechaInicial').datetimepicker({
        locale: 'es',
        showTodayButton: true,
        format: 'YYYY-MM-DD HH:mm',
        stepping: 30,
        minDate: new Date()
    });
});
function validateForm() {
    validarRequeridos(function (res) {
        if (res && validarFechas()) {
            $("#formSolicitud").submit();
        }
    });
    return false;
}

function validarFechas() {
    if (new Date($("#id_fechaInicial").val()) >= new Date($("#id_fechaFinal").val())) {

        $("#mensajes-error").append('<div class="alert alert-danger col-md-6"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            'La fecha inicial debe ser menor que la fecha final</div>');
        return false;
    }
    return true;
}

function iniciarFechas(defaultDateEnd, defaultDateStart, minDateEnd, minDateStart) {

    $('#id_fechaFinal').datetimepicker({
        locale: 'es',
        showTodayButton: true,
        format: 'YYYY-MM-DD HH:mm',
        stepping: 30,
        minDate: new Date(),
        defaultDate: defaultDateEnd
    });

    $('#id_fechaInicial').datetimepicker({
        locale: 'es',
        showTodayButton: true,
        format: 'YYYY-MM-DD HH:mm',
        stepping: 30,
        minDate: new Date(),
        defaultDate: defaultDateStart
    });

    if (minDateEnd != null) {
        $('#id_fechaInicial').data("DateTimePicker").options({minDate: minDateStart});
        $('#id_fechaFinal').data("DateTimePicker").options({minDate: minDateEnd});
    }

}
$('#project').change(function () {
            project_id = $(this).val();
            request_url = '/solicitarMuestra/experimentos/?project_id=' + project_id;
            $('#experiment')
                .find('option')
                .remove()
                .end()
                .append('<option value="">----------</option>')
                .val('');

            $('#protocol')
                .find('option')
                .remove()
                .end()
                .append('<option value="">----------</option>')
                .val('');

            $('#step')
                .find('option')
                .remove()
                .end()
                .append('<option value="">----------</option>')
                .val('');

            if (this.value == -1 || this.value == "") {

                return false;
            }
            $.ajax({
                type: "POST",
                url: request_url,
                data: JSON.stringify({
                    id_country: project_id
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function (data) {
                    if (data != null) {
                        $.each(data, function (key, value) {
                            $('#experiment').append($("<option/>").val(key).text(value));
                        });
                    } else {
                        console.log('error')
                    }

                },
                failure: function (errMsg) {
                    alert('Hubo un error');
                }
            });
        });
        $('#experiment').change(function () {
            experiment_id = $(this).val();
            request_url = '/solicitarMuestra/protocolos/?experiment_id=' + experiment_id;
            $('#protocol')
                .find('option')
                .remove()
                .end()
                .append('<option value="">----------</option>')
                .val('');

            $('#step')
                .find('option')
                .remove()
                .end()
                .append('<option value="">----------</option>')
                .val('');

            if (this.value == -1 || this.value == "") {
                return false;
            }
            $.ajax({
                type: "POST",
                url: request_url,
                data: JSON.stringify({
                    id_country: experiment_id
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function (data) {
                    if (data != null) {
                        $.each(data, function (key, value) {
                            $('#protocol').append($("<option/>").val(key).text(value));
                        });
                    } else {
                        console.log('error')
                    }

                },
                failure: function (errMsg) {
                    alert('Hubo un error');
                }
            });
        });
        $('#protocol').change(function () {
            protocol_id = $(this).val();
            request_url = '/solicitarMuestra/pasos/?protocol_id=' + protocol_id;
            $('#step')
                .find('option')
                .remove()
                .end()
                .append('<option value="">----------</option>')
                .val('');

            if (this.value == -1 || this.value == "") {
                return false;
            }
            $.ajax({
                type: "POST",
                url: request_url,
                data: JSON.stringify({
                    id_country: protocol_id
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function (data) {
                    if (data != null) {
                        $.each(data, function (key, value) {
                            $('#step').append($("<option/>").val(key).text(value));
                        });
                    } else {
                        console.log('error')
                    }

                },
                failure: function (errMsg) {
                    alert('Hubo un error');
                }
            });
        });


        function validateForm() {

            validarRequeridos(function (res) {
                if (res && validarCantidad()) {
                    $("#formSolicitud").submit();

                }
            });
            return false;
        };

        $(function () {
        $('#id_fechaInicial').datetimepicker({
            locale: 'es',
            showTodayButton: true,
            format: 'YYYY-MM-DD HH:mm',
            stepping: 30,
            minDate: new Date()
        });
    })
        function validarRequeridos(callback) {
            var cont = $(".requerido").length;
            $(".requerido").each(function () {

                if ($(this).val() == "") {
                    $("#mensajes-error").append('<div class="alert alert-danger col-md-6"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
                        'Los campos requeridos deben ser diligenciados</div>');
                    callback(false);
                } else {
                    cont--;
                }
                if (cont == 0) {
                    callback(true);
                }
            });

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
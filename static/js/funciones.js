$(document).ready(function () {
    $('#consultar_egresados').on('click', function () {
        $.ajax({
            url: '/consulta_egresados',
            method: 'GET',
            success: function (data) {
                $('#actualizable').html(data);

                // Inicializar DataTable si existe y lógica del modal de actualización
                if ($('#egresadostable').length && $.fn.DataTable) {
                    // Usar retrieve/destroy para evitar el warning de reinit
                    $('#egresadostable').DataTable({
                        retrieve: true,
                        destroy: true,
                        language: {
                            lengthMenu: 'MOSTRAR _MENU_ REGISTROS POR PÁGINA',
                            zeroRecords: 'NO SE ENCONTRARON RESULTADOS',
                            info: 'MOSTRANDO PÁGINA _PAGE_ DE _PAGES_',
                            infoEmpty: 'NO HAY REGISTROS DISPONIBLES',
                            infoFiltered: '(FILTRADO DE _MAX_ REGISTROS TOTALES)',
                            search: 'BUSCAR:',
                            paginate: { first: 'PRIMERO', last: 'ÚLTIMO', next: 'SIGUIENTE', previous: 'ANTERIOR' }
                        },
                        paging: true,
                        lengthChange: true,
                        searching: true,
                        ordering: true,
                        info: true,
                        autoWidth: false,
                        responsive: true,
                        lengthMenu: [[3, 5, 10], [3, 5, 10]],
                        order: [[6, 'asc'], [3, 'asc']]
                    });
                }

                inicializarModalActualizacion();
            },
            error: function (err) {
                console.log('Error al cargar los alumnos')
            }

        });

    });
    $('#estadisticas_egresados').on('click', function () {
    $.ajax({
        url: '/estadisticas_egresados',
        method: 'GET',
        success: function (data) {
            $('#actualizable').html(data);
            
            // Aquí puedes inicializar cualquier gráfico o librería que uses
            // Por ejemplo, si usas Chart.js o similares
            console.log('Estadísticas cargadas exitosamente');
        },
        error: function (err) {
            console.log('Error al cargar las estadísticas', err);
            alert('No se pudieron cargar las estadísticas');
        }
    });
});

    // Eliminación de egresados con confirmación en modal
    let eliminarContexto = { id: null, nombre: '', $btn: null };

    $(document).off('click', '.btn-eliminar').on('click', '.btn-eliminar', function (ev) {
        ev.preventDefault();
        const $btn = $(this);
        const id = $btn.attr('data-id');
        const nombre = $btn.attr('data-nombre') || '';
        if (!id) { alert('No se encontró el ID del egresado.'); return; }

        eliminarContexto = { id, nombre, $btn };
        // Mostrar modal de confirmación (Bootstrap 5)
        const nombreSpan = document.getElementById('nombreEgresadoEliminar');
        if (nombreSpan) nombreSpan.textContent = nombre;
        const modalEl = document.getElementById('modaleliminaregresado');
        if (modalEl && window.bootstrap) {
            const modal = new window.bootstrap.Modal(modalEl);
            modal.show();
        } else {
            // Si no hay modal, preguntar con confirm
            if (confirm(`¿Está seguro de borrar al egresado ${nombre}?`)) {
                ejecutarEliminacion(id, $btn);
            }
        }
    });

    // Botón confirmar en el modal
    $(document).off('click', '#confirmarEliminarEgresado').on('click', '#confirmarEliminarEgresado', async function () {
        const id = eliminarContexto.id;
        const $btn = eliminarContexto.$btn;
        if (!id || !$btn) return;
        // Cerrar modal antes de proceder
        const modalEl = document.getElementById('modaleliminaregresado');
        if (modalEl && window.bootstrap) {
            const instance = window.bootstrap.Modal.getInstance(modalEl) || new window.bootstrap.Modal(modalEl);
            instance.hide();
        }
        await ejecutarEliminacion(id, $btn);
    });

    async function ejecutarEliminacion(id, $btn) {
        try {
            $btn.prop('disabled', true).text('Borrando…');
            let resp = await fetch(`/eliminar_egresado/${id}`, {
                method: 'DELETE',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' },
                credentials: 'same-origin'
            });
            if (!resp.ok && (resp.status === 405 || resp.status === 404)) {
                resp = await fetch(`/eliminar_egresado/${id}`, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' },
                    credentials: 'same-origin'
                });
            }
            let data;
            try { data = await resp.json(); } catch (_) { data = { success: false, message: 'Respuesta no válida del servidor' }; }

            if (resp.ok && data.success) {
                // Quitar fila
                const tr = $btn.closest('tr')[0] || document.querySelector(`tr[data-row-id="${id}"]`);
                if (tr) {
                    try {
                        const $tabla = $('#egresadostable');
                        if ($tabla.length && $.fn.DataTable && $tabla.DataTable) {
                            const dt = $tabla.DataTable();
                            dt.row(tr).remove().draw(false);
                        } else {
                            tr.remove();
                        }
                    } catch (e) {
                        tr.remove();
                    }
                }
                // Mostrar modal de éxito
                const modalOkEl = document.getElementById('modalExitoEliminar');
                if (modalOkEl && window.bootstrap) {
                    const modalOk = new window.bootstrap.Modal(modalOkEl);
                    modalOk.show();
                } else {
                    alert('Usuario eliminado exitosamente');
                }
            } else {
                alert(data.message || `Error al eliminar egresado (HTTP ${resp.status})`);
                console.error('Fallo al eliminar:', { status: resp.status, data });
            }
        } catch (e) {
            console.error('Error de red al eliminar egresado:', e);
            alert('Error de red al eliminar egresado');
        } finally {
            $btn.prop('disabled', false).text('Eliminar');
        }
    }


    // Acción de guardado de actualización
    $(document).off('click', '#guardar_actualizacion').on('click', '#guardar_actualizacion', function(){
        const $btn = $(this);
        $btn.prop('disabled', true).text('Guardando...');

        const form = document.getElementById('form_actualizacion_egresado');
        if (!form) { $btn.prop('disabled', false).text('Guardar'); return; }

        const data = {
            id_egresado_ac: $('#id_egresado_ac').val(),
            nombre_egresado_ac: $('#nombre_egresado_ac').val(),
            apellido_paterno_ac: $('#apellido_paterno_ac').val(),
            apellido_materno_ac: $('#apellido_materno_ac').val(),
            matricula_ac: $('#matricula_ac').val(),
            correo_ac: $('#correo_ac').val(),
            telefono_ac: $('#telefono_ac').val(),
            generacion_ac: $('#generacion_ac').val(),
            modalidad: $('#modalidad').val(),
            estatus_titulacion_ac: $('#estatus_titulacion_ac').val(),
            estatus_laboral_ac: $('#estatus_laboral_ac').val(),
            id_carrera_ac: $('#id_carrera_ac').val(),
            id_ues_ac: $('#id_ues_ac').val(),
            id_municipio_ac: $('#id_municipio_ac').val(),
            id_localidad_ac: $('#id_localidad_ac').val(),
        };

        $.ajax({
            url: '/actualizar_egresado',
            method: 'POST',
            data: data,
            success: function (resp) {
                if (resp && resp.success) {
                    // Cerrar modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('modalactualizaregresado'));
                    if (modal) modal.hide();
                    // Notificar
                    alert('Actualización exitosa');

                    // Actualizar fila en la tabla sin recargar
                    if (resp.egresado) {
                        const eg = resp.egresado;
                        const row = buscarFilaEgresado(eg.id_egresado);
                        if (row) {
                            actualizarFilaTabla(row, eg);
                        }
                        // Actualizar el data-egresado del botón para futuras ediciones
                        const btnAct = row ? row.querySelector('.btn-actualizar') : null;
                        if (btnAct) {
                            btnAct.setAttribute('data-egresado', JSON.stringify(eg));
                        }
                    }
                } else {
                    alert((resp && resp.message) ? resp.message : 'Error al actualizar');
                }
            },
            error: function (xhr) {
                const msg = (xhr && xhr.responseJSON && xhr.responseJSON.message) ? xhr.responseJSON.message : 'Error en la solicitud';
                alert(msg);
            },
            complete: function(){
                $btn.prop('disabled', false).text('Guardar');
            }
        });
    });

    function buscarFilaEgresado(idEgresado) {
        const rows = document.querySelectorAll('#egresadostable tbody tr');
        for (const tr of rows) {
            const btn = tr.querySelector('.btn-actualizar');
            if (!btn) continue;
            const raw = btn.getAttribute('data-egresado');
            try {
                const eg = JSON.parse(raw);
                if (eg && (eg.id_egresado == idEgresado)) {
                    return tr;
                }
            } catch (e) {}
        }
        return null;
    }

    function actualizarFilaTabla(tr, eg) {
        // Asumiendo el orden de columnas actual en consulta_egresados.html
        const tds = tr.querySelectorAll('td');
        // 0 nombre, 1 ap paterno, 2 ap materno, 3 matricula, 4 correo, 5 telefono, 6 generacion, 7 modalidad, 8 foto, 9 acciones
        if (tds[0]) tds[0].textContent = eg.nombre_encargado || '';
        if (tds[1]) tds[1].textContent = eg.apellido_paterno || '';
        if (tds[2]) tds[2].textContent = eg.apellido_materno || '';
        if (tds[3]) tds[3].textContent = eg.matricula || '';
        if (tds[4]) tds[4].textContent = eg.correo || '';
        if (tds[5]) tds[5].textContent = eg.telefono || '';
        if (tds[6]) tds[6].textContent = eg.generacion || '';
        if (tds[7]) tds[7].textContent = eg.modalidad || '';
        if (tds[8]) {
            const img = tds[8].querySelector('img#foto_egresado');
            if (img) {
                if (eg.fotografia) {
                    const ruta = eg.fotografia.startsWith('uploads/') ? `/static/${eg.fotografia}` : eg.fotografia;
                    img.src = ruta;
                } else {
                    img.src = '/static/egresados/1.jpg';
                }
            }
        }
    }

    function inicializarModalActualizacion() {
        // Usar delegación de eventos en el documento para que funcione después de recargar la tabla
        $(document).off('click', '.btn-actualizar').on('click', '.btn-actualizar', function(event) {
            event.preventDefault();
            const btn = this;
            const raw = btn.getAttribute('data-egresado');
            let eg = null;
            try { eg = JSON.parse(raw); } catch (e) { console.error('JSON inválido', e); return; }

            // Cargar opciones y luego asignar valores
            Promise.all([
                cargarCarreras('#id_carrera_ac'),
                cargarUes('#id_ues_ac'),
                cargarMunicipios('#id_municipio_ac')
            ]).then(function(){
                if (eg?.id_municipio) {
                    return cargarLocalidades('#id_localidad_ac', eg.id_municipio).then(function(){ asignarValores(eg); });
                } else {
                    asignarValores(eg);
                }
            }).catch(function(){
                asignarValores(eg);
            });

            // Cambiar municipios -> recargar localidades
            $(document).off('change', '#id_municipio_ac').on('change', '#id_municipio_ac', function(){
                const idMun = $(this).val();
                cargarLocalidades('#id_localidad_ac', idMun);
            });

            function asignarValores(eg){
                function setValue(id, value) {
                    const el = document.getElementById(id);
                    if (!el) return;
                    if (['INPUT','SELECT','TEXTAREA'].includes(el.tagName)) {
                        el.value = value != null ? value : '';
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }

                setValue('id_egresado_ac', eg?.id_egresado);
                setValue('nombre_egresado_ac', eg?.nombre_encargado);
                setValue('apellido_paterno_ac', eg?.apellido_paterno);
                setValue('apellido_materno_ac', eg?.apellido_materno);
                setValue('matricula_ac', eg?.matricula);
                setValue('correo_ac', eg?.correo);
                setValue('telefono_ac', eg?.telefono);
                setValue('generacion_ac', eg?.generacion);
                setValue('modalidad', eg?.modalidad);
                setValue('estatus_titulacion_ac', eg?.estatus_titulacion);
                setValue('estatus_laboral_ac', eg?.estatus_laboral);

                setValue('id_carrera_ac', eg?.id_carrera);
                setValue('id_ues_ac', eg?.id_ues);
                setValue('id_municipio_ac', eg?.id_municipio);
                setValue('id_localidad_ac', eg?.id_localidad);

                const preview = document.getElementById('previewegr');
                if (preview) {
                    if (eg?.fotografia) {
                        const ruta = eg.fotografia.startsWith('uploads/') ? `/static/${eg.fotografia}` : eg.fotografia;
                        preview.src = ruta;
                    } else {
                        preview.src = '/static/uploads/egresados/1.jpg';
                    }
                }
            }
        });
    }

    // Utilidades para cargar selects desde endpoints
    function cargarCarreras(selector) {
        return $.get('/consulta_carrera').then(function(data){
            const $sel = $(selector);
            $sel.empty().append('<option value="">Seleccione...</option>');
            (data || []).forEach(function(item){
                $sel.append(`<option value="${item.id_carrera}">${item.nombre_carrera}</option>`);
            });
        }).catch(function(err){ console.error('Error cargando carreras', err); });
    }

    function cargarUes(selector) {
        return $.get('/consulta_ues').then(function(data){
            const $sel = $(selector);
            $sel.empty().append('<option value="">Seleccione...</option>');
            (data || []).forEach(function(item){
                $sel.append(`<option value="${item.id_ues}">${item.nombre_ues}</option>`);
            });
        }).catch(function(err){ console.error('Error cargando UES', err); });
    }

    function cargarMunicipios(selector) {
        return $.get('/consulta_municipio').then(function(data){
            const $sel = $(selector);
            $sel.empty().append('<option value="">Seleccione...</option>');
            (data || []).forEach(function(item){
                $sel.append(`<option value="${item.id_municipio}">${item.nombre_municipio}</option>`);
            });
        }).catch(function(err){ console.error('Error cargando municipios', err); });
    }

    function cargarLocalidades(selector, idMunicipio) {
        if (!idMunicipio) {
            const $sel = $(selector);
            $sel.empty().append('<option value="">Seleccione...</option>');
            return Promise.resolve();
        }
        return $.get(`/consulta_localidades/${idMunicipio}`).then(function(data){
            const $sel = $(selector);
            $sel.empty().append('<option value="">Seleccione...</option>');
            (data || []).forEach(function(item){
                $sel.append(`<option value="${item.id_localidad}">${item.nombre_localidad}</option>`);
            });
        }).catch(function(err){ console.error('Error cargando localidades', err); });
    }
});

// Array para almacenar los usuarios
let usuarios = [];

window.onload = function() {
    // Mostrar el modal de verificación de contraseña al cargar la página
    var modalVerificacion = new bootstrap.Modal(document.getElementById('modalVerificacion'));
    modalVerificacion.show();
}

// Evento para verificar la contraseña en el modal de verificación
document.getElementById('botonVerificar').addEventListener('click', function() {
    var contraseña = document.getElementById('inputContraseña').value;
    if (contraseña === "admin") {
        var modalVerificacion = bootstrap.Modal.getInstance(document.getElementById('modalVerificacion'));
        modalVerificacion.hide();
        var modalUsuarios = new bootstrap.Modal(document.getElementById('modalUsuarios'));
        modalUsuarios.show();
        mostrarUsuarios(); // Muestra los usuarios en la lista
    } else {
        alert("Contraseña incorrecta");
    }
});

// Evento para abrir el modal de confirmación de agregar usuario
document.getElementById('botonAgregarUsuarioModal').addEventListener('click', function() {
    var modalUsuarios = bootstrap.Modal.getInstance(document.getElementById('modalUsuarios'));
    modalUsuarios.hide();
    var modalConfirmacion = new bootstrap.Modal(document.getElementById('modalConfirmacion'));
    modalConfirmacion.show();
});

// Evento para confirmar la adición del usuario
document.getElementById('botonConfirmarAgregar').addEventListener('click', function() {
    var correoElectronico = document.getElementById('correoElectronico').value;
    var rolUsuario = document.getElementById('rolUsuario').value;

    if (correoElectronico) {
        usuarios.push({
            correo: correoElectronico,
            rol: rolUsuario
        });

        alert("Usuario agregado: " + correoElectronico + " como " + rolUsuario);
        var modalConfirmacion = bootstrap.Modal.getInstance(document.getElementById('modalConfirmacion'));
        modalConfirmacion.hide();

        var modalUsuarios = new bootstrap.Modal(document.getElementById('modalUsuarios'));
        modalUsuarios.show();
        mostrarUsuarios(); // Actualizar la lista de usuarios
    } else {
        alert("Por favor, completa todos los campos");
    }
});

// Función para mostrar los usuarios en la lista
function mostrarUsuarios() {
    var listaUsuariosDiv = document.getElementById('listaUsuarios');
    listaUsuariosDiv.innerHTML = '';

    usuarios.forEach(function(usuario, index) {
        var usuarioDiv = crearDivUsuario(usuario, index);
        listaUsuariosDiv.appendChild(usuarioDiv);
    });
}

// Función para crear un div de usuario
function crearDivUsuario(usuario, index) {
    var usuarioDiv = document.createElement('div');
    usuarioDiv.classList.add('d-flex', 'align-items-center', 'mb-2');

    var correoSpan = document.createElement('span');
    correoSpan.classList.add('me-2');
    correoSpan.textContent = usuario.correo;

    var selectorTipo = crearSelectorTipo(usuario.rol);

    var botonEliminar = document.createElement('button');
    botonEliminar.classList.add('btn', 'btn-danger', 'btn-sm');
    botonEliminar.textContent = 'X';
    botonEliminar.addEventListener('click', function() {
        usuarios.splice(index, 1);
        mostrarUsuarios();
    });

    usuarioDiv.appendChild(correoSpan);
    usuarioDiv.appendChild(selectorTipo);
    usuarioDiv.appendChild(botonEliminar);

    return usuarioDiv;
}

// Función para crear un selector de rol
function crearSelectorTipo(rol) {
    var selectorTipo = document.createElement('select');
    selectorTipo.classList.add('form-select', 'form-select-sm', 'me-2');

    var opcionTutor = document.createElement('option');
    opcionTutor.value = 'Tutor';
    opcionTutor.textContent = 'Tutor';
    var opcionAsistente = document.createElement('option');
    opcionAsistente.value = 'Asistente';
    opcionAsistente.textContent = 'Asistente';

    if (rol === 'Tutor') {
        opcionTutor.selected = true;
    } else {
        opcionAsistente.selected = true;
    }

    selectorTipo.appendChild(opcionTutor);
    selectorTipo.appendChild(opcionAsistente);

    return selectorTipo;
}

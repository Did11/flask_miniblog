// Función para iniciar sesión y almacenar el JWT
function login(username, password) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Hay un error en el inicio de sesión!');
        }
    })
    .then(data => {
        // Asumiendo que el token se devuelve en un campo llamado 'access_token'
        localStorage.setItem('jwt', data.access_token);
        checkAuthState(); // Actualizar el estado de autenticación
        // Redirigir al usuario a la página de inicio o donde sea necesario
        window.location.href = '/';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error en el inicio de sesión: ' + error.message);
    });
}

// Función para cerrar sesión y eliminar el JWT
function logout() {
    localStorage.removeItem('jwt');
    checkAuthState(); // Actualizar el estado de autenticación
    // Actualizar la UI o redirigir al usuario
}

// Función para incluir el JWT en las solicitudes subsiguientes
function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('jwt');
    if (token) {
        options.headers = options.headers || {};
        options.headers.Authorization = `Bearer ${token}`;
    }
    return fetch(url, options);
}

// Función para verificar el estado de autenticación y actualizar la UI
function checkAuthState() {
    const userMenu = document.getElementById('user-menu');
    const guestMenu = document.getElementById('guest-menu');
    const token = localStorage.getItem('jwt');

    if (token) {
        userMenu.style.display = 'block';
        guestMenu.style.display = 'none';
    } else {
        userMenu.style.display = 'none';
        guestMenu.style.display = 'block';
    }
}

// Evento que se dispara cuando el contenido de la página se ha cargado
document.addEventListener('DOMContentLoaded', (event) => {
    checkAuthState(); // Llama a esta función para verificar el estado de autenticación al cargar la página
});

// Asegúrate de que los IDs y eventos coincidan con tu HTML real
// Por ejemplo, si tienes un formulario de inicio de sesión con un ID 'login-form'
// y un botón de cierre de sesión con un ID 'logout-button', podrías hacer algo como esto:

// Vincular la función de inicio de sesión al formulario de inicio de sesión
const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            login(username, password);
        });
    }

// Vincular la función de cierre de sesión al botón de cierre de sesión
const logoutButton = document.getElementById('logout-button');
if (logoutButton) {
    logoutButton.addEventListener('click', function(event) {
        logout();
    });
}

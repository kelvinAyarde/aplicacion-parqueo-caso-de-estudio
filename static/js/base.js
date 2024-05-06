const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');

const darkMode = document.querySelector('.dark-mode');

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});
/*
darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
})*/

$('.sidebar a').click(function(e) {
    //e.preventDefault(); // Evita la acción predeterminada del enlace
    $('.sidebar a').removeClass('active'); // Elimina la clase 'active' de todos los elementos 'a' dentro de '.sidebar'
    $(this).addClass('active'); // Agrega la clase 'active' al elemento 'a' que se hizo clic
});

//-----------------------------

const darkModeToggle = darkMode;

// Verificar el estado actual del modo oscuro al cargar la página
window.addEventListener('load', () => {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDarkMode);
});

// Función para cambiar el estado del modo oscuro
function setDarkMode(isDarkMode) {
    document.body.classList.toggle('dark-mode-variables', isDarkMode);
    if(!isDarkMode){
        darkModeToggle.querySelector('span:nth-child(1)').classList.toggle('active');
        darkModeToggle.querySelector('span:nth-child(2)').classList.toggle('active',false);
    }else{
        darkModeToggle.querySelector('span:nth-child(2)').classList.toggle('active');
        darkModeToggle.querySelector('span:nth-child(1)').classList.toggle('active',false);
    }    
    // Guardar el estado del modo oscuro en el almacenamiento local
    localStorage.setItem('darkMode', isDarkMode);
}

// Evento de clic para alternar el modo oscuro
darkModeToggle.addEventListener('click', () => {
    const isDarkMode = document.body.classList.contains('dark-mode-variables');
    setDarkMode(!isDarkMode);
});

$('#cerrar_sesion').click(function(e) {
    localStorage.removeItem('darkMode');
});
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    if (!name || !email || !message) {
        alert('Por favor, completa todos los campos.');
        return;
    }
    alert('Formulario enviado con éxito.');
});

let currentIndex = 0;
const images = document.querySelectorAll('#carousel img');
document.getElementById('next').addEventListener('click', () => {
    images[currentIndex].classList.add('hidden');
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.remove('hidden');
});
document.getElementById('prev').addEventListener('click', () => {
    images[currentIndex].classList.add('hidden');
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    images[currentIndex].classList.remove('hidden');
});

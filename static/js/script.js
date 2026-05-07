<<<<<<< Updated upstream
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
=======
class Carousel {
    constructor(elementId) {
        this.images = document.querySelectorAll(`#${elementId} img`);
        this.currentIndex = 0;
        this.prevButton = document.getElementById('prev');
        this.nextButton = document.getElementById('next');
        this.init();
    }
    init() {
        this.nextButton.addEventListener('click', () => this.next());
        this.prevButton.addEventListener('click', () => this.prev());
    }
    next() {
        this.images[this.currentIndex].classList.add('hidden');
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.images[this.currentIndex].classList.remove('hidden');
    }
    prev() {
        this.images[this.currentIndex].classList.add('hidden');
        this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        this.images[this.currentIndex].classList.remove('hidden');
    }
}
new Carousel('carousel');
>>>>>>> Stashed changes

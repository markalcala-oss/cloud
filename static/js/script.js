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

(function () {
  function initCarousel() {
    const slide = document.getElementById('carouselSlide');
    if (!slide || slide.dataset.carouselInitialized) return;

    const images = slide.querySelectorAll('a');
    if (!images.length) return;

    let counter = Math.floor(Math.random() * images.length);
    slide.style.transform = `translateX(-${counter * 100}%)`;

    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');

    const move = (delta) => {
      counter = (counter + delta + images.length) % images.length;
      slide.style.transform = `translateX(-${counter * 100}%)`;
    };

    if (nextBtn) nextBtn.addEventListener('click', () => move(1));
    if (prevBtn) prevBtn.addEventListener('click', () => move(-1));

    slide.dataset.carouselInitialized = '1';
  }

  document.addEventListener('DOMContentLoaded', initCarousel);
  document.addEventListener('turbolinks:load', initCarousel); // if using Turbolinks
  document.addEventListener('turbo:load', initCarousel);      // if using Turbo
})();

var index = 0;

function changeSlide(slideIndex) {
  var width = document.querySelector('.articleView-slider').clientWidth;
  var slides = document.querySelector('.articleView-slides');

  if (width * slideIndex >= slides.clientWidth) {
    slideIndex = 0;
  }

  var step = width * slideIndex;

  slides.style.left = "-" + step + "px";

  // Update the index
  index = slideIndex;
}

function automaticSlide() {
  setTimeout(automaticSlide, 5000);
  changeSlide(index);
  index++;
}

automaticSlide();

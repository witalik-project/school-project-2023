var index = 0;

function changeSlide(slideIndex) {
    var width = document.querySelector('.articleView-slider').clientWidth;
    var slides = document.querySelector('.articleView-slides');
    
    if(width*slideIndex>=slides.clientWidth)
    {
      slideIndex = 0;
    }
  
    var step = width*slideIndex;
  
    slides.style.left = "-" + step + "px";

    /*console.log("slideIndex: " + slideIndex);
    console.log("width: " + width);
    console.log("slides.clientWidth: " + slides.clientWidth);*/
}

function automaticSlide() {
  setTimeout(automaticSlide, 5000);
  changeSlide(index);
  index++;
}

function manualSlide(slideIndex) {
    
  }
  
  var btn = document.querySelectorAll('.articleView-sliderNavigation button');
  
  for (var i = 0; i < btn.length; i++) {
    btn[i].addEventListener('click', function() {
      manualSlide(parseInt(btn.id));

    });
  }


automaticSlide();

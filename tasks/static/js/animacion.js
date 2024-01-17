document.addEventListener('DOMContentLoaded', function () {
  // Tu código JavaScript existente

// Selecciona todos los elementos con la clase "cabeza" en un NodeList
let elementosCabeza = document.querySelectorAll(".cabeza");

// Itera sobre cada elemento y aplica la animación cuando sea visible
elementosCabeza.forEach(function(elemento) {
  window.addEventListener('scroll', function() {
    let position1 = elemento.getBoundingClientRect().top;
    let tamPantalla = window.innerHeight / 1.2;
    if (position1 < tamPantalla) {
      elemento.style.animation = 'mover 1s ease-out';
    }
  });
});


});
// Función para mostrar toasts
const mostrarToasts = (taskTitle, taskId) => {
    var toastElement = document.querySelector(`#liveToast_${taskId}`);
    var toastTitleElement = document.querySelector(`#toastTaskTitle_${taskId}`);
  
    if (toastElement && toastTitleElement) {
      console.log("Elemento de toast encontrado.");
  
      // Actualizar contenido del Toast
      toastTitleElement.textContent = taskTitle;
  
      var toastInstance = new bootstrap.Toast(toastElement, {
        // Añadir opciones para ajustar la posición
        position: 'bottom-end',
      });
  
      console.log("funciona hasta la acción mostrar");
      toastInstance.show();
    } else {
      console.error('Toast element no encontrado. Intenta con otro selector.');
    }
  };
  
  // fetch con todos los valores
  document.querySelectorAll('.task-form').forEach(function(form) {
    form.addEventListener('submit', async function(event) {
      event.preventDefault();
  
      const formData = new FormData(event.target);
  
      try {
        const response = await fetch('/', {
          method: 'POST',
          body: formData,
        });
  
        const data = await response.json();
  
        if (data.message === 'Success') {
          const taskId = formData.get('task_id');
          const taskTitle = formData.get('task_title');
          mostrarToasts(taskTitle, taskId);
        } else {
          alert('Hubo un problema al enviar el formulario.');
        }
      } catch (error) {
        console.error('Error en la solicitud:', error);
      }
    });
  });
  // Obtener elementos del DOM
  var incrementButtons = document.querySelectorAll(".increment");
  var decrementButtons = document.querySelectorAll(".decrement");
  var quantityInputs = document.querySelectorAll(".quantity");
  var totalElement = document.querySelector("#total");
  var products = document.querySelectorAll(".productos_precio");
  var productsUnits = document.querySelectorAll(".priceUnit");
  var submitButton = document.querySelector('.btn-success');
  var form = document.querySelector('form');
  
  // Inicializar la variable totalSum en 0
  var totalSum = 0;
  
  // Desactivar el botón para evitar clics múltiples
  var isSubmitting = false;
  
  // Función para actualizar la información de un producto
  function updateProduct(index) {
      var currentQuantity = parseInt(quantityInputs[index].value);
      var productPrice = parseFloat(products[index].textContent);
      productsUnits[index].textContent = (currentQuantity * productPrice).toFixed(2);
  }
  
  // Manejar eventos de clic para botones de incremento y decremento
  function handleButtonClick(index, increment) {
      return function () {
          var currentQuantity = parseInt(quantityInputs[index].value);
          quantityInputs[index].value = increment ? currentQuantity + 1 : Math.max(currentQuantity - 1, 1);
          updateProduct(index);
          updateTotal();
      };
  }
  
  // Asignar manejadores de eventos a botones de incremento y decremento
  incrementButtons.forEach(function (button, index) {
      button.addEventListener('click', handleButtonClick(index, true));
  });
  
  decrementButtons.forEach(function (button, index) {
      button.addEventListener('click', handleButtonClick(index, false));
  });
  
  // Función para actualizar el elemento total
  function updateTotal() {
      totalSum = 0;
  
      quantityInputs.forEach(function (quantityInput, index) {
          var productPrice = parseFloat(products[index].textContent);
          totalSum += parseInt(quantityInput.value) * productPrice;
          productsUnits[index].textContent = (parseInt(quantityInput.value) * productPrice).toFixed(2);
      });
  
      if (totalElement) {
          totalElement.textContent = "Total: " + totalSum.toFixed(2);
          totalElement.setAttribute('data-total', totalSum.toFixed(2));
      }
  }
  
  // Nueva función para manejar el clic en el botón "Finalizar compra"
  function submitForm() {
      if (isSubmitting) {
          return;
      }
      isSubmitting = true;
  
      updateTotal();
      var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
      var totalValue = totalElement.getAttribute('data-total');
      var productsData = [];
  
      quantityInputs.forEach(function (quantityInput, index) {
          var targetAttribute = quantityInput.getAttribute('data-target');
          if (targetAttribute) {
              var productId = targetAttribute.split('_')[1];
              var productQuantity = parseInt(quantityInput.value);
              productsData.push({
                  id: productId,
                  quantity: productQuantity
              });
          }
      });
  
      var formData = new URLSearchParams();
      formData.append('total', totalValue);
      productsData.forEach(function (product) {
          formData.append('products[]', JSON.stringify(product));
      });
  
      fetch('/carrito/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': csrfToken
          },
          body: formData.toString()
      })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  window.location.href = '/finish_Sell/';
              } else {
                  console.error('Error:', data.error);
              }
          })
          .catch(error => {
              console.error('Error:', error);
          })
          .finally(() => {
              isSubmitting = false;
          });
  }
  
  // Asignar el manejador de eventos al formulario
  if (form) {
      form.addEventListener('submit', function (event) {
          event.preventDefault();
          submitForm();
      });
  }
  
  // Llamar a la función updateTotal para asegurarse de que el total se muestre correctamente al cargar la página
  updateTotal();
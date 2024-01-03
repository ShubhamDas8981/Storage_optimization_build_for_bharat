// Buyer Section
document.getElementById("buyerBtn").addEventListener("click", function () {
  document.querySelector('.card').style.display = 'none';
  document.querySelector('.buyer-form').style.display = 'block';
});

document.getElementById("buyerSubmitBtn").addEventListener("click", function (event) {
  event.preventDefault();

  const buyerId = document.getElementById("buyerId").value.trim();
  const buyerPass = document.getElementById("buyerPass").value.trim();
  const buyerPincode = document.getElementById("buyerPincode").value.trim();

  
  const message = document.createElement("p");
  message.textContent = "Searching for your pincode...";
  message.classList.add("searching-message");

  
  const form = document.getElementById("buyerForm");
  form.parentNode.insertBefore(message, form.nextSibling);
  setTimeout(function () {
    message.remove();
  }, 3000);
  
});

// Merchant Section
document.getElementById("merchantBtn").addEventListener("click", function () {
  document.querySelector('.card').style.display = 'none';
  document.querySelector('.merchant-form').style.display = 'block';
});

document.getElementById("submitBtn").addEventListener("click", function (event) {
  event.preventDefault();

  const pincodeCount = parseInt(document.getElementById("pincodeCount").value);
  const pincodeInputs = document.getElementById("pincodeInputs");

  pincodeInputs.innerHTML = '';


  for (let i = 1; i <= pincodeCount; i++) {
    const textarea = document.createElement("textarea");
    textarea.placeholder = `Enter Pin Code ${i}`;
    pincodeInputs.appendChild(textarea);
  }
});

document.getElementById("pincodeForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const pincodeInputs = Array.from(document.getElementById("pincodeInputs").querySelectorAll("textarea"));
  const allPincodesValid = pincodeInputs.every(textarea => textarea.value.trim().length === 6);

  if (allPincodesValid) {
    const successMessage = document.createElement("p");
    successMessage.textContent = "Pincodes successfully registered";
    successMessage.classList.add("success-message");

    
    const form = document.getElementById("pincodeForm");
    form.parentNode.insertBefore(successMessage, form.nextSibling);

    setTimeout(function () {
      successMessage.remove();
    }, 3000); 
  }
});

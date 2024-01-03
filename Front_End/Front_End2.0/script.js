document.getElementById("merchantBtn").addEventListener("click", function () {
  document.querySelector('.card').style.display = 'none';
  document.querySelector('.merchant-form').style.display = 'block';
});

document.getElementById("buyerBtn").addEventListener("click", function () {
  // Handle buyer login or redirect to the buyer page
  // You can implement this functionality similarly to the merchant button
});

document.getElementById("submitBtn").addEventListener("click", function (event) {
  event.preventDefault();

  const pincodeCount = parseInt(document.getElementById("pincodeCount").value);
  const pincodeInputs = document.getElementById("pincodeInputs");

  // Clear previous inputs
  pincodeInputs.innerHTML = '';

  // Create textarea inputs based on pincodeCount
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

    // Replace the next line with the appropriate element to display the message
    const form = document.getElementById("pincodeForm");
    form.parentNode.insertBefore(successMessage, form.nextSibling);

    setTimeout(function () {
      successMessage.remove();
    }, 3000);
  }
});


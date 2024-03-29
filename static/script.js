document.addEventListener("DOMContentLoaded", function () {
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

    const data = {
      buyerId,
      buyerPass,
      buyerPincode
    };

    fetch('/submit_buyer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Handle the response from the backend here
      displayMerchantIds(data); // Update the display with merchant IDs
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
  // Function to display merchant IDs
  function displayMerchantIds(data) {
    const merchantList = document.getElementById("merchantList");
    merchantList.innerHTML = ""; // Clear previous content
  
    if (data.merchants_found && data.merchants_found.length > 0) {
      // Show the merchant IDs section
      document.getElementById("merchantIDs").style.display = "block";
  
      data.merchants_found.forEach(merchantId => {
        const listItem = document.createElement("li");
        listItem.textContent = merchantId;
        merchantList.appendChild(listItem);
      });
    } else {
      // Hide the merchant IDs section if no merchants are found
      window.alert("No merchants avaliable for the given pincode");
      document.getElementById("merchantIDs").style.display = "none";
    }
  }
  
  // Merchant Section
  document.getElementById("merchantBtn").addEventListener("click", function () {
    document.querySelector('.card').style.display = 'none';
    document.querySelector('.merchant-form').style.display = 'block';
  });

  document.getElementById("submitBtn").addEventListener("click", function (event) {
    event.preventDefault();

    const merchantName = document.getElementById("merchantName").value.trim();
    const merchantid = document.getElementById("merchantid").value.trim();
    const merchantpass = document.getElementById("merchantpass").value.trim();
    const pincodeCount = document.getElementById("pincodeCount").value;

    const pincodeList = [];
    for (let i = 1; i <= pincodeCount; i++) {
      const pincode = document.getElementById(`pincode_${i}`).value.trim();
      pincodeList.push(pincode);
    }

    const data = {
      merchantName: merchantName,
      merchantid: merchantid,
      merchantpass: merchantpass,
      pincodeCount: parseInt(pincodeCount),
      pincodeList: pincodeList
    };

    fetch('/submit_merchant', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Handle the response from the backend here
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
  // Add the dynamic pincode input generation script here
  document.getElementById("pincodeCount").addEventListener("input", function() {
    const pincodeCount = parseInt(this.value);
    const pincodeInputs = document.getElementById("pincodeInputs");

    // Clear previous inputs
    pincodeInputs.innerHTML = "";

    // Generate new pincode input fields
    for (let i = 1; i <= pincodeCount; i++) {
        const input = document.createElement("input");
        input.type = "text";
        input.id = `pincode_${i}`;
        input.placeholder = `Enter Pin Code ${i}`;
        pincodeInputs.appendChild(input);
    }
  });
});

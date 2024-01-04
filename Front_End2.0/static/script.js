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
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });

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
      merchantName,
      merchantid,
      merchantpass,
      pincodeCount,
      pincodeList
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
});



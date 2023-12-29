function searchPincode() {
  var pincode = document.getElementById("pincode").value;
  var resultDisplay = document.getElementById("result");

  if (pincode.trim() !== "") {
    if (pincode.length === 6 && /^\d+$/.test(pincode)) {
      var result = "Searching for pin code: " + pincode;
      resultDisplay.textContent = result;
      resultDisplay.classList.add("show");
      resultDisplay.style.color = "green";
    } else {
      resultDisplay.textContent = "Please enter a valid 6-digit pincode.";
      resultDisplay.classList.add("show");
      resultDisplay.style.color = "red";
    }
  } else {
    resultDisplay.textContent = "Please enter a pincode to search.";
    resultDisplay.classList.add("show");
    resultDisplay.style.color = "red";
  }

  setTimeout(function () {
    resultDisplay.classList.remove("show");
  }, 3000);
}

document.getElementById("pincode").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    searchPincode();
  }
});

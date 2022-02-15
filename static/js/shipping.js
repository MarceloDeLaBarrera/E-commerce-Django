if (shipping == "False") {
  document.getElementById("shipping-info").innerHTML = "";
}

if (user != "AnonymousUser") {
  document.getElementById("user-info").innerHTML = "";
}

if (shipping == "False" && user != "AnonymousUser") {
  document.getElementById("form-wrapper").classList.add("hidden");
  document.getElementById("payment-info").classList.remove("hidden");
}

var form = document.getElementById("form");

form.addEventListener("submit", function (e) {
  e.preventDefault();
  console.log("Form Submited...");
  document.getElementById("form-button").classList.add("hidden");
  document.getElementById("payment-info").classList.remove("hidden");
});

document.getElementById("make-payment").addEventListener("click", function (e) {
  submitFormData();
});

function submitFormData() {
  console.log("Payment button clicked");
}

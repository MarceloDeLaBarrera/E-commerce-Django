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
csrftoken = form.getElementsByTagName("input")[0].value;
console.log("Newtoken: ", csrftoken);

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

  var userFormData = {
    name: null,
    email: null,
    total: total,
  };
  var shippingInfo = {
    address: null,
    city: null,
    state: null,
    zipcode: null,
  };

  if (shipping != "False") {
    shippingInfo.address = form.address.value;
    shippingInfo.city = form.city.value;
    shippingInfo.state = form.state.value;
    shippingInfo.zipcode = form.zipcode.value;
  }

  if (user == "AnonymousUser") {
    userFormData.name = form.name.value;
    userFormData.email = form.email.value;
  }

  var url = "/process_order/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ form: userFormData, shipping: shippingInfo }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success: ", data);
      alert("Transacción Completada");

      //Set cart to empty to clear cookies, and redirect to home page. That's because when a order is complete, we need to clean the cart.
      cart = {};
      document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
      window.location.href = home_url;
    });
}
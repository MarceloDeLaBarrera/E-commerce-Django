var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productID = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productID, "action:", action);

    console.log("User:", user);
    if (user === "AnonymousUser") {
      addCookieItem(productID, action);
    } else {
      updateUserOrder(productID, action);
    }
  });
}

function addCookieItem(productID, action) {
  console.log("Not logged in");
  if (action == "add") {
    if (cart[productID] == undefined) {
      cart[productID] = { quantity: 1 };
    } else {
      cart[productID]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productID]["quantity"] -= 1;

    if (cart[productID]["quantity"] <= 0) {
      console.log("Item should be deleted");
      delete cart[productID];
    }
  }
  //Set the cokie value, if guest reload, or leave the page, he don't lose information.
  console.log("Cart: ", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

function updateUserOrder(productID, action) {
  console.log("User is logged, sending data...");

  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productID: productID, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data: ", data);
      location.reload();
    });
}

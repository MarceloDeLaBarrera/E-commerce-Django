var info_messages = document.getElementsByClassName(
  ("alert-success", "alert-danger")
);

setTimeout(function () {
  for (var i = 0; i < info_messages.length; i++) {
    // Set display attribute as !important, neccessary when using bootstrap
    info_messages[i].setAttribute("style", "display:none !important");
  }
}, 6000);
// Timeout is 6 sec, you can change it

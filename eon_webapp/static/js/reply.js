function boxAppear(button) {
  var id = button.getAttribute("attr-id");
  var x = document.getElementById("replyBox_" + id);
  if (x.style.display === "none") {
    x.style.display = "block";
    return false;
  }
}

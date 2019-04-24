// cookie for remembering if it's mitchell/keer
// periodically update count of days since march 31st in corner
// slowly fade
// communicate with server

$(document).ready(function() {
  var canvas = new fabric.Canvas("Canvas", {
    isDrawingMode: true
  });
  canvas.freeDrawingBrush.color = "#ff0000";
  canvas.freeDrawingBrush.width = 10;

  function clearCanvas() {
    // Tell server
    canvas.clear();
  }

  $("#Clear").click(function() {
    if (confirm("Are you sure you want to erase everything?")) {
      clearCanvas();
    }
  });
  $("#Snapshot").click(function() {
    alert("Not implemented yet");
  });
  $("#History").click(function() {
    alert("Not implemented yet");
  });
  $("#SignOut").click(function() {
    $("#Canvas").fadeOut(500, function() {
      $(".center").empty();
    });
    $.removeCookie("token");
  });
});

// Constants
var UI_FADE_TIME = 500;
var TOOLBOX_SHOW_TIME = 3000;
var CANVAS_HTML = "<canvas id='Canvas' width='500' height='500'></canvas>";

// Globals
var $main = $("#Main");
var $canvasView = $("#CanvasView");
var $loginView = $("#LoginView");
var $loginForm = $("#LoginForm");
var $loginMessage = $("#LoginMessage");
var $toolbox = $("#Toolbox");
var userInfo = null;
var canvas = null;

// Makes a request to the server with a JSON body.
function request(type, path, data) {
  return $.ajax({
    type: type,
    url: window.location.protocol + "//" + window.location.host + path,
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8"
  });
}

// Attempts to log in with the remembered session.
function autoLogin() {
  return request("GET", "/api/user").done(function(response) {
    userInfo = response;
  });
}

// Clears the login data.
function logout() {
  userInfo = null;
  return request("POST", "/api/logout");
}

// Connects the canvas to the server.
function connect() {
  $canvasView.empty().hide().append(CANVAS_HTML);
  canvas = new fabric.Canvas("Canvas", {isDrawingMode: true});
  canvas.freeDrawingBrush.color = "#ff0000";
  canvas.freeDrawingBrush.width = 10;
  // connect to server and get first image
  // start main loop
  return showCanvasView();
}

// Disconnects the canvas from the server.
function disconnect() {
  return hideCanvasView().done(function() {
    $canvasView.empty();
    // stop main loop
  });
}

// Fades in the login form.
function showLoginView() {
  var $children = $loginView.children();
  $loginMessage.hide();
  // Fade in the children one by one.
  $children.hide();
  $loginView.show();
  var children = $children.toArray();
  var dfd = $.Deferred();
  function revealNext() {
    var next = children.shift();
    if (next === undefined) {
      dfd.resolve();
    } else {
      $(next).fadeIn(UI_FADE_TIME, revealNext);
    }
  }
  revealNext();
  return dfd;
}

// Fades out the login form.
function hideLoginView() {
  return $loginView.fadeOut(UI_FADE_TIME);
}

// Fades in the canvas view and toolbox.
function showCanvasView() {
  return $.when(
    $canvasView.fadeIn(UI_FADE_TIME),
    $toolbox.css({visibility: "visible", opacity: 0})
      .fadeTo(UI_FADE_TIME, 1)
      .delay(TOOLBOX_SHOW_TIME)
      .fadeTo(UI_FADE_TIME, 0, function() {
        $toolbox.css("opacity", "");
      })
  );
}

// Fades out the canvas view and toolbox.
function hideCanvasView() {
  return $.when(
    $canvasView.fadeOut(UI_FADE_TIME),
    $toolbox.fadeTo(UI_FADE_TIME, 0, function() {
      $toolbox.css("visibility", "hidden");
    })
  );
}

// Syncs the canvas with the server.
function mainLoop() {
  // TODO
}

$loginForm.submit(function() {
  // Fades in a message underneath the form.
  function show(kind, text) {
    return $loginMessage.hide().removeClass().addClass(kind).text(text)
      .fadeIn(UI_FADE_TIME).promise();
  }

  // Make sure all fields are present.
  $loginForm.find("input").removeClass("error");
  var values = {}
  var ok = true;
  $.each(["username", "password"], function(index, field) {
    var $input = $loginForm.find('input[name="' + field + '"]');
    values[field] = $input.val();
    if (!values[field]) {
      $input.addClass("error");
      if (ok) {
        show("error", "Please enter a " + field + ".");
      }
      ok = false;
    }
  });
  if (!ok) {
    return false;
  }

  // Attempt to log in to the server.
  var status = show("", "Connecting ...");
  request("POST", "/api/login", values).fail(function(xhr) {
    status.done(function() {
      if (xhr.readyState !== 4) {
        show("error", "Could not connect to sever.");
      } else if (xhr.status === 401) {
        show("error", "Wrong username or password.");
      } else {
        show("error", "Unexpected error (" + xhr.status + ").");
      }
    });
  }).done(function() {
    status.then(autoLogin).fail(function() {
      show("error", "Unexpected server error.");
    }).done(function() {
      show("success", "Success!").then(hideLoginView).done(connect);
    });
  });
  return false;
});

$("#Clear").click(function() {
  if (confirm("Are you sure you want to erase everything?")) {
    clearCanvas();
  }
  return false;
});

$("#Snapshot").click(function() {
  alert("Not implemented yet");
  return false;
});

$("#History").click(function() {
  alert("Not implemented yet");
  return false;
});

$("#SignOut").click(function() {
  logout();
  disconnect().done(showLoginView);
  return false;
});

autoLogin().done(connect).fail(showLoginView);

// Constants
var UI_FADE_TIME = 500;
var MESSAGE_SHOW_TIME = 1000;
var TOOLBAR_SHOW_TIME = 3000;
var CANVAS_HTML = "<canvas id='Canvas' width='500' height='500'></canvas>";
var TOOLS = ["Brush", "Eraser", "Text"];
var MIN_BRUSH_SIZE = 4;
var MAX_BRUSH_SIZE = 16;
var BRUSH_SIZE_INC = 2;

// Globals
var $main = $("#Main");
var $message = $("#Message");
var $canvasView = $("#CanvasView");
var $loginView = $("#LoginView");
var $loginForm = $("#LoginForm");
var $loginMessage = $("#LoginMessage");
var $toolbar = $("#Toolbar");
var userInfo = null;
var canvas = null;
var toolIndex = 0;
var brushSize = 4;

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

// Shows a message temporarily in the middle of the view.
function showMessage(message) {
  return $message.finish().hide()
    .text(message)
    .fadeTo(UI_FADE_TIME, 1)
    .delay(MESSAGE_SHOW_TIME)
    .fadeOut(UI_FADE_TIME).promise();
}

// Fades in the login form.
function showLoginView() {
  var $children = $loginView.children();
  $loginMessage.finish().hide();
  $children.finish().hide();
  $loginView.finish().show();
  // Fade in the children one by one.
  var children = $children.toArray();
  var dfd = $.Deferred();
  function revealNext() {
    var next = children.shift();
    if (next === undefined) {
      dfd.resolve();
    } else {
      $(next).fadeTo(UI_FADE_TIME, 1, revealNext);
    }
  }
  revealNext();
  return dfd;
}

// Fades out the login form.
function hideLoginView() {
  return $loginView.finish().fadeOut(UI_FADE_TIME).promise();
}

// Fades in the canvas view and toolbar.
function showCanvasView() {
  return $.when(
    $canvasView.finish().fadeTo(UI_FADE_TIME, 1),
    $toolbar.finish()
      .removeClass("transition-opacity")
      .css({visibility: "visible", opacity: 0})
      .fadeTo(UI_FADE_TIME, 1)
      .delay(TOOLBAR_SHOW_TIME)
      .promise().done(function() {
        var restore = function() {
          $toolbar.css("opacity", "").addClass("transition-opacity");
        };
        if ($("body").find("#Toolbar:hover").length) {
          restore();
        } else {
          $toolbar.fadeTo(UI_FADE_TIME, 0, restore);
        }
      })
  );
}

// Fades out the canvas view and toolbar.
function hideCanvasView() {
  return $.when(
    $canvasView.finish().fadeOut(UI_FADE_TIME),
    $toolbar.finish().removeClass("transition-opacity")
      .fadeTo(UI_FADE_TIME, 0, function() {
        $toolbar.css("visibility", "hidden");
      })
  );
}

// Connects the canvas to the server.
function connect() {
  $canvasView.empty().hide().append(CANVAS_HTML);
  canvas = new fabric.Canvas("Canvas", {isDrawingMode: true});
  canvas.freeDrawingBrush.color = "#ff0000";
  canvas.freeDrawingBrush.width = brushSize;
  // connect to server and get first image
  // start main loop
  return showCanvasView();
}

// Disconnects the canvas from the server.
function disconnect() {
  canvas = null;
  return hideCanvasView().done(function() {
    $canvasView.empty();
    // stop main loop
  });
}

// Syncs the canvas with the server.
function mainLoop() {
  // TODO
}

$loginForm.submit(function() {
  // Fades in a message underneath the form.
  function show(kind, text) {
    return $loginMessage.finish()
      .hide().removeClass().addClass(kind).text(text)
      .fadeTo(UI_FADE_TIME, 1).promise();
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
      show("success", "Success!").then(hideLoginView).done(function() {
        // Don't leave the password in the DOM.
        $loginForm.trigger("reset");
        connect();
      });
    });
  });
  return false;
});

$("#CurrentTool").click(function() {
  toolIndex = (toolIndex + 1) % TOOLS.length;
  $(this).finish().css("opacity", 0).text(TOOLS[toolIndex])
    .fadeTo(UI_FADE_TIME, 1);
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
  $.when(disconnect(), showMessage("Signing out ...")).done(showLoginView);
  return false;
});

$("body").keydown(function(event) {
  if (canvas !== null) {
    if (event.which === 219) {
      brushSize -= BRUSH_SIZE_INC;
      showMessage("dec");
    } else if (event.which == 221) {
      brushSize += BRUSH_SIZE_INC;
      showMessage("inc");
    }
    // clamp
  }
});

autoLogin().done(connect).fail(showLoginView);

// Constants
var UI_FADE_TIME = 500;
var TEXT_FADE_TIME = 200;//1000;
var CANVAS_HTML = "<canvas id='Canvas' width='500' height='500'></canvas>";

// Globals
var $main = $("#Main");
var $canvasView = $("#CanvasView");
var $loginView = $("#LoginView");
var $loginForm = $("#LoginForm");
var $loginMessage = $("#LoginMessage");
var $toolbox = $("#Toolbox");
var clientState = null;
var canvas = null;

// Makes a POST request to the given server.
function postTo(server, path, data) {
  return $.ajax({
    type: "POST",
    xhrFields: {withCredentials: true},
    url: server + path,
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8"
  });
}

// Makes a POST request to the remembered server.
function post(path, data) {
  return postTo(clientState["server"], path, data);
}

// Attempts to log in using arguments or cookies. Returns a promise.
function login(server, response) {
  var dfd = $.Deferred();
  var newLogin = server !== undefined;
  if (newLogin) {
    // Set client state from the login response.
    clientState = {
      server: server,
      color: response["color"]
    };
    // On success, we will persist the state to a cookie.
    dfd.then(function() {
      Cookies.setJSON("clientState", clientState);
    });
  } else {
    // Read the client state from the cookie.
    var cookie = Cookies.getJSON("clientState");
    if (cookie === undefined) {
      return dfd.reject().promise();
    }
    clientState = cookie;
  }
  if (clientState["server"] === undefined) {
    return dfd.reject().promise();
  }
  // Make sure authentication is working.
  post("/api/ping").done(function(data) {
    if (data == "pong") {
      dfd.resolve();
    } else {
      dfd.reject();
    }
  }).fail(function() {
    dfd.reject();
  });
  return dfd.promise();
}

// Clears all login data.
function logout() {
  Cookies.remove("clientState");
  clientState = null;
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
      $(next).fadeIn(TEXT_FADE_TIME, revealNext);
    }
  }
  revealNext();
  return dfd;
}

// Fades out the login form.
function hideLoginView() {
  if ($loginView.css("display") === "none") {
    return $.Deferred().resolve().promise();
  }
  return $loginView.fadeOut(UI_FADE_TIME);
}

// Fades in the canvas view and toolbox.
function showCanvasView() {
  if ($canvasView.css("display") === "none") {
    return $.Deferred().resolve().promise();
  }
  return $.when(
    $canvasView.fadeIn(UI_FADE_TIME),
    $toolbox.css({visibility: "visible", opacity: 0}).fadeTo(1, UI_FADE_TIME)
  );
}

// Fades out the canvas view and toolbox.
function hideCanvasView() {
  return $.when(
    $canvasView.fadeOut(UI_FADE_TIME),
    $toolbox.fadeTo(0, UI_FADE_TIME, function() {
      $toolbox.css("visibility", "hidden");
    })
  );
}

// Syncs the canvas with the server.
function mainLoop() {
  // TODO
}

// Normalizes a URL by prefixing https:// and removing trailing slashes.
function normalizeUrl(url) {
  url = url.replace(/\/+$/, "");
  if (!/^https?:\/\//i.test(url)) {
    url = "https://" + url;
  }
  return url;
}

$loginForm.submit(function() {
  function show(kind, text) {
    return $loginMessage.hide().removeClass().addClass(kind).text(text)
      .fadeIn(TEXT_FADE_TIME).promise();
  }

  // Make sure all fields are present.
  $loginForm.find("input").removeClass("error");
  var fields = ["server", "username", "password"];
  var values = {}
  var ok = true;
  $.each(fields, function(index, field) {
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

  // Attempt to connect.
  var status = show("", "Connecting ...");
  var server = normalizeUrl(values["server"]);
  postTo(server, "/api/login", {
    username: values["username"],
    password: values["password"]
  }).done(function(response) {
    status.done(function() {
      login(server, response).then(function() {
        show("success", "Success!").done(hideLoginView).done(connect);
      }).fail(function() {
        show("error", "Unexpected server error.");
      });
    });
  }).fail(function(xhr) {
    status.done(function() {
      if (xhr.readyState !== 4) {
        show("error", "Could not connect to sever.");
      } else if (xhr.status === 401) {
        show("error", "Wrong username or password.");
      } else {
        show("error", "Unexpected error (" + xhr.status + ").");
      }
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

login().done(connect).fail(showLoginView);

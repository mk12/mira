export function isDevelopment() {
  return process.env.NODE_ENV === "development";
}

export function errorStatus(error) {
  return error.response && error.response.status;
}

export function errorCode(error) {
  return error.response && error.response.data && error.response.data.code;
}

export function neutralMessage(text) {
  return { text };
}

export function successMessage(text) {
  return { text, success: true };
}

export function errorMessage(text) {
  return { text, error: true };
}

export function genericErrorMessage(error) {
  if (errorCode(error) === "login_fail") {
    return errorMessage("Wrong username or password.");
  }
  if (errorCode(error) === "username_taken") {
    return errorMessage("Username is already taken.");
  }
  if (errorStatus(error) === 429) {
    return errorMessage("Too many requests.");
  }
  if (error.code === "ECONNABORTED") {
    return errorMessage("Request timed out.");
  }
  return errorMessage("An unexpected error occurred.");
}

export function makeDataURL(data) {
  return "data:image/png;base64," + data;
}

export function extractDataURL(dataURL) {
  return dataURL.substr(dataURL.indexOf(",") + 1);
}

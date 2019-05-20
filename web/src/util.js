export function isDevelopment() {
  return process.env.NODE_ENV === "development";
}

export function errorStatus(error) {
  return error.response && error.response.status;
}

export function errorCode(error) {
  return error.response && error.response.data && error.response.data.code;
}

export function formSuccess(text) {
  return { text };
}

export function formSuccessSlot() {
  return { slot: true };
}

export function formError(text) {
  return { text, error: true };
}

export function genericFormError(error) {
  if (errorCode(error) === "login_fail") {
    return formError("Wrong username or password.");
  }
  if (errorCode(error) === "username_taken") {
    return formError("Username is already taken.");
  }
  if (errorStatus(error) === 429) {
    return formError("Too many requests.");
  }
  return formError("An unknown error occurred.");
}

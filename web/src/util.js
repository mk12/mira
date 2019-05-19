export function isDevelopment() {
  return process.env.NODE_ENV === "development";
}

export function errorStatusIs(error, status) {
  return (
    error.response !== undefined &&
    error.response.status !== undefined &&
    error.response.status === status
  );
}

export function errorCodeIs(error, code) {
  return (
    error.response !== undefined &&
    error.response.data !== undefined &&
    error.response.data.code === code
  );
}

export function formSuccess(text) {
  return { text };
}

export function formError(text) {
  return { text, error: true };
}

export function genericFormError(error) {
  if (errorCodeIs(error, "login_fail")) {
    return "Wrong username or password.";
  }
  if (errorCodeIs(error, "username_taken")) {
    return "Username is already taken.";
  }
  if (errorStatusIs(error, 429)) {
    return "Too many requests.";
  }
  return "An unknown error occurred.";
}

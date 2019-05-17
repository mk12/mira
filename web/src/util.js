export function isDevelopment() {
  return process.env.NODE_ENV === "development";
}

export function isStatus(error, status) {
  return (
    error.response !== undefined &&
    error.response.status !== undefined &&
    error.response.status === status
  );
}

export function isCode(error, code) {
  return (
    error.response !== undefined &&
    error.response.data !== undefined &&
    error.response.data.code === code
  );
}

export function errorMessage(error) {
  if (isCode(error, "login_fail")) {
    return "Wrong username or password.";
  }
  if (isCode(error, "username_taken")) {
    return "Username is already taken.";
  }
  if (isStatus(error, 429)) {
    return "Too many requests.";
  }
  return "An unknown error occurred.";
}

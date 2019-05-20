import api from "@/api";
import store from "@/store";
import { isDevelopment, errorStatus } from "@/util";

// Returns true if we are logged in.
function isLoggedIn() {
  return store.getters.isLoggedIn;
}

// Attempts to log in automatically.
async function autoLogin() {
  // In production, window.miraUsername will be set to a string or null.
  if (isDevelopment()) {
    try {
      window.miraUsername = (await api.get("check")).data.username;
    } catch (error) {
      if (errorStatus(error) === 401) {
        window.miraUsername = null;
      } else {
        throw error;
      }
    }
  }
  store.commit("login", window.miraUsername);
}

// Logs in using the given credentials.
async function login(username, password) {
  await api.post("login", { username, password });
  store.commit("login", username);
}

// Registers a new account.
async function register(username, password) {
  await api.post("register", { username, password });
}

// Changes the password on the current account and logs out.
async function changePassword(oldPassword, newPassword) {
  await api.put("change_password", {
    password: oldPassword,
    new_password: newPassword
  });
  store.commit("logout");
}

// Deletes the current account and logs out.
async function deleteAccount(password) {
  await api.delete("account", { data: { password } });
  store.commit("logout");
}

// Logs out the current user.
async function logout() {
  await api.post("logout");
  store.commit("logout");
}

export default {
  isLoggedIn,
  autoLogin,
  login,
  register,
  changePassword,
  deleteAccount,
  logout
};

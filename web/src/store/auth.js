import api from "@/api";
import { errorStatus, isDevelopment } from "@/util";

function initialState() {
  return {
    username: null
  };
}

export default {
  namespaced: true,

  state: initialState,

  getters: {
    isLoggedIn: state => !!state.username
  },

  mutations: {
    reset(state) {
      Object.assign(state, initialState());
    },

    setUser(state, username) {
      state.username = username;
    }
  },

  actions: {
    async autoLogin({ commit }) {
      // In production, the server sets window.miraUsername to a string or null.
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
      commit("setUser", window.miraUsername);
    },

    async login({ commit }, { username, password }) {
      await api.post("login", { username, password });
      commit("setUser", username);
    },

    async logout({ dispatch }, options) {
      if (!(options && options.skipServer)) {
        await api.post("logout");
      }
      await dispatch("resetAll", null, { root: true });
    }
  }
};

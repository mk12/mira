import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: null
  },

  getters: {
    isLoggedIn: state => !!state.username
  },

  mutations: {
    login(state, username) {
      state.username = username;
    },

    logout(state) {
      state.username = null;
    }
  }
});

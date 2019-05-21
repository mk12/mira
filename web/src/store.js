import Vue from "vue";
import Vuex from "vuex";

import api from "@/api";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: null,
    loaded: false,
    loadError: false,
    friendList: [],
    routerKey: 0
  },

  getters: {
    isLoggedIn(state) {
      return !!state.username;
    },

    friends(state) {
      let map = {};
      for (let f of state.friendList) {
        map[f.username] = f;
      }
      return map;
    },

    confirmedFriends(state) {
      return state.friendList.filter(f => f.state === "friend");
    },

    incomingRequests(state) {
      return state.friendList.filter(f => f.state === "incoming");
    },

    outgoingRequests(state) {
      return state.friendList.filter(f => f.state === "outgoing");
    }
  },

  mutations: {
    login(state, username) {
      state.username = username;
    },

    logout(state) {
      state.username = null;
      state.loaded = false;
      state.loadError = false;
      state.friendList = [];
    },

    loadError(state) {
      state.loadError = true;
    },

    loadSuccess(state, friends) {
      state.loaded = true;
      state.friendList = [
        {
          username: "alice",
          state: "friend",
          canvas:
            "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        },
        {
          username: "tracy",
          state: "friend",
          canvas: null
        },
        {
          username: "gladys",
          state: "friend",
          canvas: null
        },
        {
          username: "dragosword2",
          state: "outgoing",
          canvas: null
        },
        {
          username: "forgetmenot",
          state: "outgoing",
          canvas: null
        },
        {
          username: "bob",
          state: "incoming",
          canvas: null
        }
      ];
      state.friendList = friends;
    },

    reloadRoute(state) {
      state.routerKey++;
    }
  },

  actions: {
    async refresh({ commit, getters }) {
      if (!getters.isLoggedIn) {
        return;
      }
      let response;
      try {
        response = await api.get("friends_data");
      } catch (error) {
        commit("loadError");
        return;
      }
      commit("loadSuccess", response.data.friends);
    },

    async refreshPage({ commit, dispatch }) {
      await dispatch("refresh");
      commit("reloadRoute");
    }
  }
});

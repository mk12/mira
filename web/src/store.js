import Vue from "vue";
import Vuex from "vuex";

import api from "@/api";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: null,
    loading: true,
    friendList: null
  },

  getters: {
    isLoggedIn(state) {
      return !!state.username;
    },

    friends(state, username) {
      let map = {};
      for (let f of state.friendList) {
        map[f.username] = f;
      }
      return map;
    },

    incomingRequests(state) {
      return state.friendList.filter(f => f.state === "incoming");
    },

    outgoingRequests(state) {
      return state.friendList.filter(f => f.state === "outgoing");
    },

    confirmedFriends(state) {
      return state.friendList.filter(f => f.state === "friend");
    }
  },

  mutations: {
    login(state, username) {
      state.username = username;
    },

    logout(state) {
      state.username = null;
    },

    loadError(state) {
      state.loading = "error";
    },

    loadSuccess(state, friends) {
      state.loading = false;
      state.friendList = [
        {
          username: "alice",
          state: "friend",
          canvas: "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
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
          state: "incoming",
          canvas: null
        },
        {
          username: "forgetmenot",
          state: "outgoing",
          canvas: null
        },
        {
          username: "bob",
          state: "outgoing",
          canvas: null
        }
      ];
      state.friendList = friends;
    }
  },

  actions: {
    async refresh({ commit, getters }) {
      if (!getters.isLoggedIn) {
        commit("loadError");
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
    }
  }
});

import Vue from "vue";

import api from "@/api";

function initialState() {
  return {
    data: {},
    errors: {}
  };
}

function resourceKey(resource) {
  switch (resource.loader) {
    case "allFriends":
      return "friends_data";
    case "oneFriend":
      return "friends/" + encodeURIComponent(resource.username);
  }
}

export default {
  namespaced: true,

  state: initialState,

  getters: {
    status(state) {
      return function(resource) {
        let key = resourceKey(resource);
        if (state.errors[key]) {
          return "error";
        }
        if (state.data[key] === undefined) {
          return "loading";
        }
        return "loaded";
      };
    },

    friendList(state) {
      return state.data.friends_data;
    },

    friendMap(state, getters) {
      if (!getters.friendList) {
        return null;
      }
      let map = {};
      for (let friend of getters.friendList) {
        map[friend.username] = friend;
      }
      return map;
    },

    getFriend(state, getters) {
      return function(username) {
        let key = resourceKey({ loader: "oneFriend", username });
        let friend = state.data[key];
        if (friend) {
          return friend;
        }
        let map = getters.friendMap;
        if (map) {
          return map[username];
        }
        return null;
      };
    }
  },

  mutations: {
    reset(state) {
      Object.assign(state, initialState());
    },

    loadError(state, payload) {
      Vue.set(state.errors, payload.key, true);
    },

    loadSuccess(state, payload) {
      Vue.set(state.data, payload.key, payload.value);
    }
  },

  actions: {
    async load({ commit, rootGetters }, resource) {
      if (!rootGetters["auth/isLoggedIn"]) {
        return;
      }
      let key = resourceKey(resource);
      let response;
      try {
        response = await api.get(key);
      } catch (error) {
        commit("loadError", { key });
        return;
      }
      commit("loadSuccess", { key, value: response.data });
      if (resource.rerender) {
        commit("page/rerender", null, { root: true });
      }
    },

    async reload({ dispatch }, resource) {
      dispatch("load", { ...resource, rerender: true });
    }
  }
};

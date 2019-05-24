import Vue from "vue";

import api from "@/api";

function initialState() {
  return {
    data: {},
    errors: {},
    refreshKey: 0
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
    status(state, getters) {
      return function(resource) {
        if (state.errors[resourceKey(resource)]) {
          return "error";
        }
        if (getters.get(resource) !== undefined) {
          return "loaded";
        }
        return "loading";
      };
    },

    get(state, getters) {
      return function(resource) {
        let value = state.data[resourceKey(resource)];
        if (value !== undefined) {
          return value;
        }
        if (
          resource.loader === "oneFriend" &&
          getters.friendMap &&
          getters.friendMap[resource.username]
        ) {
          return getters.friendMap[resource.username];
        }
        return null;
      };
    },

    friendMap(state) {
      let friends = state.data.friends_data;
      if (!friends) {
        return null;
      }
      let map = {};
      for (let friend of friends) {
        map[friend.username] = friend;
      }
      return map;
    }
  },

  mutations: {
    reset(state) {
      Object.assign(state, initialState());
    },

    loadError(state, { key }) {
      Vue.set(state.errors, key, true);
    },

    loadSuccess(state, { key, value }) {
      Vue.set(state.data, key, value);
    },

    refresh(state) {
      state.refreshKey++;
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
      if (resource.refresh) {
        commit("refresh");
      }
    },

    async reload({ dispatch }, resource) {
      await dispatch("load", { ...resource, refresh: true });
    }
  }
};

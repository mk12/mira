import Vue from "vue";
import isEqual from "lodash.isequal";

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
    case "canvas":
      return `friends/${encodeURIComponent(resource.username)}/canvas`;
  }
}

export default {
  namespaced: true,

  state: initialState,

  getters: {
    getData(state, getters) {
      return function(resource) {
        let value = state.data[resourceKey(resource)];
        if (value !== undefined) {
          return value;
        }
        if (
          resource.loader === "oneFriend" &&
          getters.friendMap[resource.username]
        ) {
          return getters.friendMap[resource.username];
        }
        return undefined;
      };
    },

    getError(state) {
      return function(resource) {
        return state.errors[resourceKey(resource)];
      };
    },

    friendMap(state) {
      let map = {};
      let friends = state.data.friends_data;
      if (friends) {
        for (let friend of friends) {
          map[friend.username] = friend;
        }
      }
      return map;
    }
  },

  mutations: {
    reset(state) {
      Object.assign(state, initialState());
    },

    loadError(state, { key, error }) {
      Vue.set(state.errors, key, error);
    },

    loadSuccess(state, { key, value }) {
      Vue.set(state.data, key, value);
    },

    refresh(state) {
      state.refreshKey++;
    }
  },

  actions: {
    async load({ commit, getters, rootGetters }, resource) {
      if (!rootGetters["auth/isLoggedIn"]) {
        return;
      }
      let oldData = getters.getData(resource);
      let key = resourceKey(resource);
      let response;
      try {
        response = await api.get(key);
      } catch (error) {
        commit("loadError", { key, error });
        return;
      }
      commit("loadSuccess", { key, value: response.data });
      if (!isEqual(oldData, getters.getData(resource))) {
        commit("refresh");
      }
    },

    async set({ commit }, { resource, value }) {
      let key = resourceKey(resource);
      commit("loadSuccess", { key, value });
    }
  }
};

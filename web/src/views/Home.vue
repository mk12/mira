<template>
  <div class="text-page">
    <div v-if="loading" class="center-box">
      <p :class="{ 'error-message': loading === 'error' }">{{ loadingMessage }}</p>
    </div>
    <template v-else>
      <div v-if="requests.length" class="request">
        Accept <strong>{{ requests[0].username }}</strong>'s friend request?
        <button class="button button--inline" @click.prevent="acceptRequest()">
          Yes
        </button>
        <button class="button button--inline" @click.prevent="rejectRequest()">
          No
        </button>
      </div>
      <div v-if="!friends.length" class="center-box">
        <p class="friend-message">Friends will show up here!</p>
        <router-link to="/settings/add_friend">Add friends</router-link>
      </div>
      <div v-else class="friend-grid">
        <div
          v-for="friend in friends"
          :key="friend.username"
          class="friend-grid__item"
        >
          <CanvasThumbnail :username="friend.username" />
          <router-link :to="friendLink(friend)" class="friend-grid__username">{{
            friend.username
          }}</router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import CanvasThumbnail from "@/components/CanvasThumbnail.vue";

export default {
  name: "Home",

  components: {
    CanvasThumbnail
  },

  computed: {
    loadingMessage() {
      if (this.loading === "error") {
        return "An unexpected error occurred.";
      }
      return "Loading ...";
    },

    ...mapState([
      "loading"
    ]),

    ...mapGetters({
      requests: "incomingRequests"
    }),

    friends() {
      let confirmed = this.$store.getters.confirmedFriends;
      let pending = this.$store.getters.outgoingRequests;
      return confirmed.concat(pending);
    }
  },
  methods: {
    canvasLink(friend) {
      return {
        name: "canvas",
        params: { username: friend.username }
      };
    },

    friendLink(friend) {
      return {
        name: "friend",
        params: { username: friend.username }
      };
    },

    acceptRequest() {},

    rejectRequest() {}
  }
};
</script>

<style lang="scss" scoped>
.request {
  margin-bottom: 0.5em;
}

.friend-grid {
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-content: center;
  height: 100%;

  &__item {
    margin: 15px;
  }

  &__username {
    font-size: 0.8em;
  }
}

.friend-message {
  color: $disabled;
}
</style>

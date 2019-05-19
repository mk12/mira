<template>
  <div class="text-page">
    <h1>{{ title }}: {{ username }}</h1>
    <p v-if="user.state === 'friend'">
      You have been friends for {{ duration }}.
      <button
        class="button button--inline"
        @click.prevent="unfriend()"
        >Unfriend</button
      >
    </p>
    <p v-else-if="user.state === 'outgoing'">
      You sent a friend request {{ duration }} ago.
      <button
        class="button button--inline"
        @click.prevent="unfriend()">Revoke</button
      >
    </p>
    <CanvasThumbnail :username="username" />
  </div>
</template>

<script>
import api from "@/api";

import CanvasThumbnail from "@/components/CanvasThumbnail.vue";

export default {
  name: "Friend",

  props: {
    username: String
  },

  components: {
    CanvasThumbnail
  },

  data() {
    // TODO since this is route /friends/:username,
    // check if it's actually a friend! (and restrict type)
    return {
      duration: "2 days",
      canvasLink: {
        name: "canvas",
        params: { username: this.username }
      }
    };
  },

  computed: {
    title() {
      switch (this.user.state) {
        case "friend":
          return "Friend";
        case "outgoing":
          return "Pending";
        case "incoming":
          return "Deleted";
      }
    },

    user() {
      return this.$store.getters.friends[this.username];
    }
  },

  methods: {
    async unfriend() {
      await api.delete(`friends/${encodeURIComponent(this.username)}`);
    },

    async refriend() {
      await api.put(`friends/${encodeURIComponent(this.username)}`);
    }
  }
};
</script>

<style lang="scss" scoped>
.friend-canvas {
  width: 250px;
  height: 250px;
  margin: 1em auto;
}
</style>

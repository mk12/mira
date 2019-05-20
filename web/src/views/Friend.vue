<template>
  <div class="text-page">
    <LoadPage>
      <template v-if="user.state === 'friend'">
        <h1>Friend: {{ username }}</h1>
        <p>You became friends {{ relativeTime }}.</p>
        <CanvasThumbnail :username="username" class="friend-thumbnail" />
        <ActionButton :submit="unfriend" value="Unfriend" />
      </template>
      <template v-else-if="user.state === 'outgoing'">
        <h1>Pending friend: {{ username }}</h1>
        <p>You sent a friend request {{ relativeTime }}.</p>
        <ActionButton :submit="unfriend" value="Revoke request" />
      </template>
      <template v-else-if="user.state === 'incoming'">
        <h1>Friend request: {{ username }}</h1>
        <p>You received a friend request {{ relativeTime }}.</p>
        <ul class="horiz-list">
          <li class="horiz-list__item">
            <ActionButton :submit="friend" value="Accept" />
          </li>
          <li class="horiz-list__item">
            <ActionButton :submit="unfriend" value="Ignore" />
          </li>
        </ul>
      </template>
      <template v-else-if="user.state === 'none'">
        <h1>User: {{ username }}</h1>
        <p>You are not friends.</p>
        <ActionButton :submit="friend" value="Add friend" />
      </template>
    </LoadPage>
  </div>
</template>

<script>
import api from "@/api";

import { errorStatus } from "@/util";

import ActionButton from "@/components/ActionButton.vue";
import CanvasThumbnail from "@/components/CanvasThumbnail.vue";
import LoadPage from "@/components/LoadPage.vue";

export default {
  name: "Friend",

  props: {
    username: String
  },

  components: {
    ActionButton,
    CanvasThumbnail,
    LoadPage
  },

  data() {
    return {
      canvasLink: {
        name: "canvas",
        params: { username: this.username }
      }
    };
  },

  computed: {
    user() {
      return (
        this.$store.getters.friends[this.username] || {
          username: this.username,
          state: "none"
        }
      );
    },

    relativeTime() {
      return this.user.time;
    }
  },

  methods: {
    async unfriend() {
      await api.delete(`friends/${encodeURIComponent(this.username)}`);
      await this.$store.dispatch("refresh");
    },

    async friend() {
      try {
        await api.put(`friends/${encodeURIComponent(this.username)}`);
      } catch (error) {
        if (errorStatus(error) === 404) {
          this.$router.replace({ name: "404", params: { "0": this.username } });
          return;
        }
        throw error;
      }
      await this.$store.dispatch("refresh");
    }
  }
};
</script>

<style lang="scss" scoped>
/deep/ .friend-thumbnail {
  margin: 1em auto;
}
</style>

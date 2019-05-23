<template>
  <div class="text-page">
    <LoadPage :resource="initialResource" @load="onLoad">
    <div :key="key">
      <template v-if="user">
        <template v-if="user.state === 'friend'">
          <h1>Friend: {{ username }}</h1>
          <p>
            You became friends with <strong>{{ username }}</strong>
            {{ relativeTime }}.
          </p>
          <CanvasThumbnail :username="username" class="friend-thumbnail" />
          <ActionButton :submit="unfriend" value="Unfriend" />
        </template>
        <template v-else-if="user.state === 'outgoing'">
          <h1>Pending friend: {{ username }}</h1>
          <p>
            You sent a friend request to <strong>{{ username }}</strong>
            {{ relativeTime }}.
          </p>
          <ActionButton :submit="unfriend" value="Revoke request" />
        </template>
        <template v-else-if="user.state === 'incoming'">
          <h1>Friend request: {{ username }}</h1>
          <p>
            You received a friend request from <strong>{{ username }}</strong>
            {{ relativeTime }}.
          </p>
          <ul class="horiz-list">
            <li class="horiz-list__item">
              <ActionButton :submit="friend" value="Accept" />
            </li>
            <li class="horiz-list__item">
              <ActionButton :submit="unfriend" value="Ignore" />
            </li>
          </ul>
        </template>
        <template v-else-if="user.state === 'self'">
          <h1>User: {{ username }}</h1>
          <p>
            You are <strong>{{ username }}</strong>!
          </p>
        </template>
        <template v-else-if="user.state === 'stranger'">
          <h1>User: {{ username }}</h1>
          <p>
            You are not friends with <strong>{{ username }}</strong
            >.
          </p>
          <ActionButton :submit="friend" value="Add friend" />
        </template>
      </template>
    </div>
    </LoadPage>
  </div>
</template>

<script>
import { distanceInWordsToNow, parse } from "date-fns";

import api from "@/api";

import ActionButton from "@/components/ActionButton.vue";
import CanvasThumbnail from "@/components/CanvasThumbnail.vue";
import LoadPage from "@/components/LoadPage.vue";

export default {
  name: "Friend",

  components: {
    ActionButton,
    CanvasThumbnail,
    LoadPage
  },

  props: {
    username: String
  },

  created() {
    this.resource = { loader: "oneFriend", username: this.username };
  },

  data() {
    return {
      key: 0
    };
  },

  computed: {
    user() {
      return this.$store.getters["data/getFriend"](this.username);
    },

    initialResource() {
      return this.user ? null : this.resource;
    },

    relativeTime() {
      return distanceInWordsToNow(parse(this.user.time)) + " ago";
    }
  },

  methods: {
    onLoad() {
      if (!this.user) {
        this.$router.replace({ name: "404", params: { "0": this.username } });
      }
    },

    async unfriend() {
      await api.delete("friends/" + encodeURIComponent(this.username));
      await this.$store.dispatch("data/load", this.resource);
      this.key++;
      // TODO handle 500 error?
    },

    async friend() {
      await api.put("friends/" + encodeURIComponent(this.username));
      await this.$store.dispatch("data/reload", this.resource);
      // TODO handle 500 error?
    }
  }
};
</script>

<style lang="scss" scoped>
/deep/ .friend-thumbnail {
  margin: 1em auto;
}
</style>

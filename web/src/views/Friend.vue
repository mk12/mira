<template>
  <div class="text-page">
    <LoadPage
      ref="load"
      :resource="resource"
      :handleError="handleError"
      @load="onLoad"
    >
      <template v-if="user">
        <template v-if="user.state === 'friend'">
          <h1>Friend: {{ username }}</h1>
          <p>
            You became friends with <strong>{{ username }}</strong>
            {{ relativeTime }}.
          </p>
          <CanvasThumbnail :user="user" class="block block--center" />
          <ActionButton :submit="unfriend" class="block" value="Unfriend" />
        </template>
        <template v-else-if="user.state === 'outgoing'">
          <h1>Pending friend: {{ username }}</h1>
          <p>
            You sent a friend request to <strong>{{ username }}</strong>
            {{ relativeTime }}.
          </p>
          <ActionButton
            :submit="unfriend"
            class="block"
            value="Revoke request"
          />
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
            You are <strong>{{ username }}</strong
            >!
          </p>
        </template>
        <template v-else-if="user.state === 'stranger'">
          <h1>User: {{ username }}</h1>
          <p>
            You are not friends with <strong>{{ username }}</strong
            >.
          </p>
          <ActionButton :submit="friend" class="block" value="Add friend" />
        </template>
      </template>
      <StatusMessage :message="message" />
    </LoadPage>
  </div>
</template>

<script>
import { distanceInWordsToNow, parse } from "date-fns";

import api from "@/api";
import { errorStatus, genericErrorMessage } from "@/util";

import ActionButton from "@/components/ActionButton.vue";
import CanvasThumbnail from "@/components/CanvasThumbnail.vue";
import LoadPage from "@/components/LoadPage.vue";
import StatusMessage from "@/components/StatusMessage.vue";

export default {
  name: "Friend",

  components: {
    ActionButton,
    CanvasThumbnail,
    LoadPage,
    StatusMessage
  },

  props: {
    username: String
  },

  data() {
    return {
      message: null
    };
  },

  created() {
    this.resource = { loader: "oneFriend", username: this.username };
  },

  computed: {
    user() {
      return this.$store.getters["data/getData"](this.resource);
    },

    relativeTime() {
      return distanceInWordsToNow(parse(this.user.time)) + " ago";
    }
  },

  methods: {
    handleError(error) {
      return errorStatus(error) === 404;
    },

    onLoad() {
      if (!this.user) {
        this.$router.replace({ name: "404", params: { "0": this.username } });
      }
    },

    async submit(method) {
      this.message = null;
      try {
        await api.request({
          method,
          url: "friends/" + encodeURIComponent(this.username)
        });
        await this.$refs.load.reload();
      } catch (error) {
        this.message = genericErrorMessage(error);
      }
    },

    async friend() {
      await this.submit("put");
    },

    async unfriend() {
      await this.submit("delete");
    }
  }
};
</script>

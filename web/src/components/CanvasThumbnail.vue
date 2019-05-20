<template>
  <div>
    <template v-if="user.state === 'friend'">
      <router-link :to="{ name: 'canvas', params: { username } }" class="link">
        <img
          v-if="user.canvas"
          :src="'data:image/jpg;base64,' + user.canvas"
          class="thumbnail thumbnail--enabled"
        />
        <div v-else class="thumbnail thumbnail--enabled center-box">
          Draw!
        </div>
      </router-link>
    </template>
    <template v-else>
      <div class="thumbnail thumbnail--disabled center-box">
        <template v-if="user.state === 'incoming'">
          <ActionButton
            :submit="acceptRequest"
            value="Accept"
            class="button--inline thumbnail__button"
          />
          <ActionButton
            :submit="ignoreRequest"
            value="Ignore"
            class="button--inline thumbnail__button"
          />
        </template>
        <template v-else-if="user.state === 'outgoing'">
          Pending
        </template>
      </div>
    </template>
  </div>
</template>

<script>
import api from "@/api";

import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "CanvasThumbnail",

  props: {
    username: String
  },

  components: {
    ActionButton
  },

  computed: {
    user() {
      return this.$store.getters.friends[this.username];
    }
  },

  methods: {
    async acceptRequest() {
      await api.put(`friends/${this.username}`);
      await this.$store.dispatch("refresh");
    },

    async ignoreRequest() {
      await api.delete(`friends/${this.username}`);
      await this.$store.dispatch("refresh");
    }
  }
};
</script>

<style lang="scss" scoped>
.link {
  line-height: 0;
  border: none;
  display: inline-block;
}

.thumbnail {
  width: 100px;
  height: 100px;
  border: 1px solid $foreground;

  &--disabled {
    border-color: $disabled;
    color: $disabled;
  }

  &--enabled:hover {
    border-color: $action;
  }

  &__button {
    margin: 5px 0;
  }
}
</style>

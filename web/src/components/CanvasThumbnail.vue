<template>
  <div class="thumbnail-wrapper">
    <template v-if="user.state === 'friend'">
      <router-link
        :to="{ name: 'canvas', params: { username: user.username } }"
        class="link"
      >
        <img
          v-if="user.thumbnail"
          :src="thumbnailSrc"
          class="thumbnail thumbnail--enabled"
        />
        <div v-else class="thumbnail thumbnail--enabled center-box">Draw!</div>
      </router-link>
    </template>
    <template v-else>
      <div class="thumbnail thumbnail--disabled center-box">
        <template v-if="user.state === 'incoming'">
          <ActionButton
            :submit="acceptRequest"
            value="Accept"
            class="button--small thumbnail__button"
          />
          <ActionButton
            :submit="ignoreRequest"
            value="Ignore"
            class="button--small thumbnail__button"
          />
        </template>
        <template v-else-if="user.state === 'outgoing'"
          >Pending</template
        >
      </div>
    </template>
  </div>
</template>

<script>
import api from "@/api";
import { makeDataURL } from "@/util";

import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "CanvasThumbnail",

  components: {
    ActionButton
  },

  props: {
    user: Object,
    reload: Function
  },

  computed: {
    thumbnailSrc() {
      return makeDataURL(this.user.thumbnail);
    }
  },

  methods: {
    async acceptRequest() {
      await api.put("friends/" + encodeURIComponent(this.user.username));
      await this.reload();
    },

    async ignoreRequest() {
      await api.delete("friends/" + encodeURIComponent(this.user.username));
      await this.reload();
    }
  }
};
</script>

<style lang="scss" scoped>
.thumbnail-wrapper {
  line-height: 0;
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
    line-height: initial;
  }
}

.link {
  line-height: 0;
  border: none;
  display: inline-block;
}
</style>

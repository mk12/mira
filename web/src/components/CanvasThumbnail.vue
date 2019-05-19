<template>
  <div>
    <template v-if="user.state === 'friend'">
      <router-link
        :to="{ name: 'canvas', params: { username } }"
        class="link"
        >
        <img
          v-if="user.canvas"
          :src="'data:image/jpg;base64,' + user.canvas"
          class="thumbnail thumbnail--enabled" />
        <div v-else class="thumbnail thumbnail--enabled center-box">
          Draw!
        </div>
      </router-link>
    </template>
    <template v-else>
      <div class="thumbnail thumbnail--disabled center-box">
        <template v-if="user.state === 'outgoing'">Pending</template>
        <template v-else-if="user.state === 'incoming'">Requested</template>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "CanvasThumbnail",

  props: {
    username: String
  },

  computed: {
    user() {
      return this.$store.getters.friends[this.username];
    }
  },

  methods: {
  }
};
</script>

<style lang="scss" scoped>
.link {
  line-height: 0;
  display: block;
  border: none;
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
}
</style>

<template>
  <div class="loading-wrapper">
    <transition name="abrupt-fade" appear>
      <div v-if="!loaded" key="loading" class="center-box">
        <p :class="{ 'error-message': loadError }">{{ loadingMessage }}</p>
      </div>
      <div v-else key="content" class="loading-wrapper">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "LoadPage",

  computed: {
    ...mapState(["loaded", "loadError"]),

    loadingMessage() {
      return this.loadError ? "An unexpected error occurred." : "Loading ...";
    }
  }
};
</script>

<style lang="scss" scoped>
.loading-wrapper {
  height: 100%;
}
</style>

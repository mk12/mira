<template>
  <div class="full-height">
    <transition name="abrupt-fade" appear>
      <div v-if="status !== 'loaded'" key="loading" class="center-box">
        <p :class="{ 'error-message': status === 'error' }">{{ message }}</p>
      </div>
      <div v-else key="content" class="full-height">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "LoadPage",

  props: {
    resource: Object
  },

  computed: {
    status() {
      return this.resource
        ? this.$store.getters["data/status"](this.resource)
        : "loaded";
    },

    message() {
      return this.status === "error"
        ? "An unexpected error occurred."
        : "Loading ...";
    }
  },

  async created() {
    if (this.resource) {
      await this.$store.dispatch("data/load", this.resource);
    }
    this.$emit("load");
  }
};
</script>

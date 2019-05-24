<template>
  <div class="absolute-fill">
    <transition name="cross-fade" appear>
      <div v-if="status !== 'loaded'" :key="message" class="center-box">
        <p :class="{ 'error-message': status === 'error' }">{{ message }}</p>
      </div>
      <div v-else :key="refreshKey" class="absolute-fill">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "LoadPage",

  props: {
    resource: Object
  },

  data() {
    return {
      contentKey: 0
    };
  },

  computed: {
    ...mapState("data", ["refreshKey"]),

    status() {
      return this.$store.getters["data/status"](this.resource);
    },

    message() {
      return this.status === "error"
        ? "An unexpected error occurred."
        : "Loading ...";
    }
  },

  methods: {
    async reload() {
      await this.$store.dispatch("data/reload", this.resource);
      if (this.status === "loaded") {
        this.$emit("load");
      }
    }
  },

  async created() {
    await this.$store.dispatch("data/load", this.resource);
    if (this.status === "loaded") {
      this.$emit("load");
    }
  }
};
</script>

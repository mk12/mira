<template>
  <div class="absolute-fill">
    <transition name="cross-fade" appear>
      <StatusMessage v-if="!loaded" :message="message" class="center-box" />
      <div v-else :key="refreshKey" class="absolute-fill">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState } from "vuex";

import { genericErrorMessage, neutralMessage } from "@/util";

import StatusMessage from "@/components/StatusMessage.vue";

export default {
  name: "LoadPage",

  components: {
    StatusMessage
  },

  props: {
    resource: Object,
    handleError: {
      type: Function,
      default: () => false
    }
  },

  data() {
    return {
      contentKey: 0
    };
  },

  computed: {
    ...mapState("data", ["refreshKey"]),

    error() {
      return this.$store.getters["data/getError"](this.resource);
    },

    loaded() {
      if (this.error && this.handleError(this.error)) {
        return true;
      }
      return !!this.$store.getters["data/getData"](this.resource);
    },

    message() {
      return this.error
        ? genericErrorMessage(this.error)
        : neutralMessage("Loading ...");
    }
  },

  methods: {
    async reload() {
      await this.$store.dispatch("data/load", this.resource);
      if (this.loaded) {
        this.$emit("load");
      }
    }
  },

  async created() {
    await this.reload();
  }
};
</script>

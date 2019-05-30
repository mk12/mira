<template>
  <div class="absolute-fill">
    <transition name="cross-fade" appear>
      <StatusMessage
        v-if="!loaded"
        key="message"
        :message="message"
        class="center-box"
      />
      <div v-else :key="refresh ? refreshKey : 'content'" class="absolute-fill">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState } from "vuex";

import { LOAD_REFRESH_TIME } from "@/constants";
import { genericErrorMessage, neutralMessage } from "@/util";

import StatusMessage from "@/components/StatusMessage.vue";

export default {
  name: "LoadPage",

  components: {
    StatusMessage
  },

  props: {
    resource: Object,
    refresh: {
      type: Boolean,
      default: true
    },
    period: {
      type: Number,
      default: LOAD_REFRESH_TIME
    },
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
      return this.$store.getters["data/getData"](this.resource) !== undefined;
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
    },

    onFocus() {
      clearInterval(this.interval);
      this.interval = setInterval(this.reload, this.period);
      this.reload();
    },

    onBlur() {
      clearInterval(this.interval);
    }
  },

  async created() {
    if (this.loaded) {
      this.$emit("load");
      if (!this.refresh) {
        return;
      }
    }
    await this.reload();
    if (this.refresh && this.period > 0) {
      this.interval = setInterval(this.reload, this.period);
      window.addEventListener("focus", this.onFocus);
      window.addEventListener("blur", this.onBlur);
    }
  },

  beforeDestroy() {
    clearInterval(this.interval);
    window.removeEventListener("focus", this.onFocus);
    window.removeEventListener("blur", this.onBlur);
  }
};
</script>

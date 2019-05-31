<template>
  <LoadPage
    :resource="resource"
    :refresh="false"
    :handleError="handleError"
    @load="onLoad"
  >
    <div class="top-banner">
      <router-link
        class="subtle-link"
        :to="{ name: 'friend', params: { username } }"
        >{{ username }}</router-link
      >
    </div>
    <transition name="cross-fade">
      <img
        v-if="backgroundSrc"
        :key="backgroundSrc"
        ref="background"
        :width="appSize"
        :height="appSize"
        :src="backgroundSrc"
        class="canvas-layer"
        style="z-index: 0;"
      />
    </transition>
    <transition name="fade-out">
      <canvas
        v-show="showAlt"
        ref="altCanvas"
        :width="appSize"
        :height="appSize"
        class="canvas-layer"
        style="z-index: 1;"
      />
    </transition>
    <canvas
      ref="canvas"
      :width="appSize"
      :height="appSize"
      class="canvas-layer"
      style="z-index: 2;"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @mousemove="onMouseMove"
      @touchstart.prevent="onMouseDown"
      @touchend.prevent="onMouseUp"
      @touchmove.prevent="onMouseMove"
    ></canvas>
    <ColorPicker
      class="color-picker"
      @changeColor="onChangeColor"
      @changeBrushSize="onChangeBrushSize"
    />
  </LoadPage>
</template>

<script>
import api from "@/api";
import { APP_SIZE, IDLE_SYNC_TIME, PERIODIC_SYNC_TIME } from "@/constants";
import { errorStatus, extractDataURL, makeDataURL } from "@/util";

import ColorPicker from "@/components/ColorPicker.vue";
import LoadPage from "@/components/LoadPage.vue";

export default {
  name: "Canvas",

  components: {
    ColorPicker,
    LoadPage
  },

  props: {
    username: String
  },

  created() {
    this.resource = { loader: "canvas", username: this.username };
    this.appSize = APP_SIZE;
    this.mouseDown = false;
    this.lastPosition = {};
    this.color = null;
    this.lineWidth = null;
    this.idleTimeout = null;
    this.syncTimeout = null;
    this.pendingSyncs = 0;
    this.changeVersion = 0;
    this.syncVersion = 0;
  },

  async beforeRouteLeave(to, from, next) {
    if (
      this.changeVersion > this.syncVersion &&
      this.$store.getters["auth/isLoggedIn"]
    ) {
      await this.sync();
    }
    next();
  },

  async beforeDestroy() {
    this.clearTimeouts();
    window.removeEventListener("focus", this.onFocus);
    window.removeEventListener("blur", this.onBlur);
  },

  data() {
    return {
      showAlt: false
    };
  },

  computed: {
    backgroundSrc() {
      let data = this.$store.getters["data/getData"](this.resource);
      return data ? makeDataURL(data) : null;
    }
  },

  methods: {
    handleError(error) {
      return errorStatus(error) === 404;
    },

    async onLoad() {
      if (this.$store.getters["data/getError"](this.resource)) {
        this.$router.replace({ name: "404", params: { "0": "canvas" } });
        return;
      }
      await this.$nextTick();
      this.canvas = this.$refs.canvas;
      this.context = this.canvas.getContext("2d");
      this.altCanvas = this.$refs.altCanvas;
      this.altContext = this.altCanvas.getContext("2d");
      window.addEventListener("focus", this.sync);
      window.addEventListener("blur", this.clearTimeouts);
      await this.sync();
    },

    onChangeColor(color) {
      this.color = color.rgba.toRgbString();
    },

    onChangeBrushSize(size) {
      this.lineWidth = size;
    },

    clearTimeouts() {
      clearTimeout(this.idleTimeout);
      clearTimeout(this.syncTimeout);
    },

    startIdleTimeout() {
      this.clearTimeouts();
      this.idleTimeout = setTimeout(this.sync, IDLE_SYNC_TIME);
    },

    async sync() {
      if (this.pendingSyncs > 1 || this.mouseDown) {
        return;
      }
      this.pendingSyncs++;
      let dataURL = this.canvas.toDataURL("image/png");
      this.altContext.clearRect(
        0,
        0,
        this.altCanvas.width,
        this.altCanvas.height
      );
      let version = this.changeVersion;
      this.altContext.drawImage(this.canvas, 0, 0);
      this.showAlt = true;
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      let data = extractDataURL(dataURL);
      let response = await api.post(
        `friends/${encodeURIComponent(this.username)}/sync`,
        { data }
      );
      await this.$store.dispatch("data/set", {
        resource: this.resource,
        value: response.data
      });
      this.showAlt = false;
      this.syncVersion = version;
      this.pendingSyncs--;
      this.syncTimeout = setTimeout(this.sync, PERIODIC_SYNC_TIME);
    },

    currentPosition(event) {
      let canvas = this.canvas;
      let rect = canvas.getBoundingClientRect();
      let x, y;
      if (event.changedTouches === undefined) {
        x = event.clientX;
        y = event.clientY;
      } else {
        x = event.changedTouches[event.changedTouches.length - 1].clientX;
        y = event.changedTouches[event.changedTouches.length - 1].clientY;
      }
      return {
        x: parseInt(x - rect.left - canvas.clientLeft),
        y: parseInt(y - rect.top - canvas.clientTop)
      };
    },

    onMouseDown(event) {
      this.mouseDown = true;
      this.changeVersion++;
      this.lastPosition = this.currentPosition(event);
    },

    onMouseUp() {
      this.mouseDown = false;
      this.changeVersion++;
      this.startIdleTimeout();
    },

    onMouseMove(event) {
      if (!this.mouseDown) {
        return;
      }
      let position = this.currentPosition(event);
      let ctx = this.context;
      ctx.beginPath();
      ctx.globalCompositeOperation = "source-over";
      ctx.strokeStyle = this.color;
      ctx.lineWidth = this.lineWidth;
      ctx.lineJoin = "round";
      ctx.lineCap = "round";
      ctx.moveTo(this.lastPosition.x, this.lastPosition.y);
      ctx.lineTo(position.x, position.y);
      ctx.stroke();
      this.lastPosition = position;
    }
  }
};
</script>

<style lang="scss" scoped>
.top-banner {
  position: absolute;
  top: -50px;
  left: 0;
  right: 0;
  text-align: center;
}

.canvas-layer {
  position: absolute;
  width: $app-size;
  height: $app-size;
}

.color-picker {
  position: fixed;
  z-index: 3;
  top: 10px;
  right: 10px;
}
</style>

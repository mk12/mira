<template>
  <LoadPage>
    <canvas
      ref="canvas"
      :width="appSize"
      :height="appSize"
      class="canvas"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @mousemove="onMouseMove"
    ></canvas>
  </LoadPage>
</template>

<script>
import { APP_SIZE, IDLE_SYNC_TIME, PERIODIC_SYNC_TIME } from "@/constants";

import LoadPage from "@/components/LoadPage.vue";

export default {
  name: "Canvas",

  components: {
    LoadPage
  },

  props: {
    username: String
  },

  created() {
    this.appSize = APP_SIZE;
    this.mouseDown = false;
    this.lastPosition = {};
    this.idleTimeout = null;
    this.syncTimeout = null;
  },

  mounted() {
    this.canvas = this.$refs.canvas;
    this.context = this.$refs.canvas.getContext("2d");
  },

  beforeDestroy() {
    // consider vue-timers
    this.clearTimeouts();
  },

  methods: {
    clearTimeouts() {
      clearTimeout(this.idleTimeout);
      clearTimeout(this.syncTimeout);
    },

    resetIdleTimeout() {
      this.clearTimeouts();
      this.idleTimeout = setTimeout(this.sync, IDLE_SYNC_TIME);
    },

    sync() {
      this.syncTimeout = setTimeout(this.sync, PERIODIC_SYNC_TIME);
    },

    currentPosition(event) {
      let canvas = this.canvas;
      let rect = canvas.getBoundingClientRect();
      return {
        x: parseInt(event.clientX - rect.left - canvas.clientLeft),
        y: parseInt(event.clientY - rect.top - canvas.clientTop)
      };
    },

    onMouseDown(event) {
      this.mouseDown = true;
      this.lastPosition = this.currentPosition(event);
    },

    onMouseUp() {
      this.mouseDown = false;
    },

    onMouseMove(event) {
      if (!this.mouseDown) {
        return;
      }
      let position = this.currentPosition(event);
      let ctx = this.context;
      ctx.beginPath();
      ctx.globalCompositeOperation = "source-over";
      ctx.strokeStyle = "black";
      ctx.lineWidth = 3;
      ctx.moveTo(this.lastPosition.x, this.lastPosition.y);
      ctx.lineTo(position.x, position.y);
      ctx.lineJoin = "round";
      ctx.lineCap = "round";
      ctx.stroke();
      this.lastPosition = position;
      this.resetIdleTimeout();
    }
  }
};
</script>

<style lang="scss" scoped>
.canvas {
  width: $app-size;
  height: $app-size;
}
</style>

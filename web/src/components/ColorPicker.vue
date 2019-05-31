<!--
  Modified from https://github.com/caohenghu/vue-colorpicker
  MIT Licensed
  Original author: caohenghu
-->
<template>
  <div class="hu-overall">
    <div>
      <div
        :style="{ background: rgba.toRgbaString() }"
        class="hu-hidden-color"
        @mousedown="toggle()"
      />
    </div>
    <div v-if="!hidden" class="hu-color-picker" :style="{ width: totalWidth + 'px' }">
      <div class="color-set">
        <div ref="size" class="size" @mousedown="selectSize">
          <canvas ref="canvasSize"/>
          <div :style="slideSizeStyle" class="slide"/>
        </div>
        <div ref="saturation" class="saturation" @mousedown="selectSaturation">
          <canvas ref="canvasSaturation"/>
          <div :style="slideSaturationStyle" class="slide"/>
        </div>
        <div ref="hue" class="hue" @mousedown="selectHue">
          <canvas ref="canvasHue"/>
          <div :style="slideHueStyle" class="slide"/>
        </div>
      </div>
      <div :style="{ height: selectedColorHeight + 'px' }" class="color-show">
        <div class="show-circle">
          <div :style="circleStyle" class="color"/>
        </div>
        <div class="show">
          <div :style="{ background: rgba.toRgbaString() }" class="color"/>
        </div>
      </div>
      <ul class="colors">
        <li v-for="item in colorsDefault" :key="item" class="item" @click="selectColor(item)">
          <div :style="{ background: item }" class="color"/>
        </li>
      </ul>
      <ul v-if="colorsHistory.length" class="colors history">
        <li v-for="item in colorsHistory" :key="item" class="item" @click="selectColor(item)">
          <div :style="{ background: item }" class="color"/>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {
  DEFAULT_BRUSH_COLOR,
  DEFAULT_BRUSH_SIZE,
  MIN_BRUSH_SIZE,
  MAX_BRUSH_SIZE
} from "@/constants";

export default {
  props: {
    color: {
      type: String,
      default: DEFAULT_BRUSH_COLOR
    },
    colorsDefault: {
      type: Array,
      default: () => [
        "#000000",
        "#FF1900",
        "#F47365",
        "#FFB243",
        "#FFE623",
        "#6EFF2A",
        "#1BC7B1",
        "#00BEFF",
        "#2E81FF",
        "#5D61FF",
        "#FF89CF",
        "#FC3CAD",
        "#BF3DCE",
        "#8E00A7",
        "#A0522D",
        "#7D7D7D"
      ]
    },
    historyKey: {
      type: String,
      default: "vue-colorpicker-history"
    }
  },
  data() {
    let history = JSON.parse(localStorage.getItem(this.historyKey)) || {};
    return {
      hidden: true,
      slideSaturationStyle: {},
      slideHueStyle: {},
      slideSizeStyle: {},
      r: 0,
      g: 0,
      b: 0,
      a: 1,
      h: 0,
      s: 0,
      v: 0,
      brushSize: history.size || DEFAULT_BRUSH_SIZE,
      colorsHistory: history.colors || [],
      colorSelected: ""
    };
  },
  computed: {
    totalWidth() {
      return this.hueHeight + (this.hueWidth + 8) * 2;
    },
    rgba() {
      return {
        r: this.r,
        g: this.g,
        b: this.b,
        a: this.a,
        toRgbString: () => `rgb(${[this.r, this.g, this.b].join(",")})`,
        toRgbaStringShort: () =>
          `${[this.r, this.g, this.b, this.a].join(",")}`,
        toRgbaString: () => `rgba(${this.rgba.toRgbaStringShort()})`,
        toHexString: () => this.rgb2hex(this.rgba, true)
      };
    },
    hsv() {
      return {
        h: this.h,
        s: this.s,
        v: this.v
      };
    },
    circleStyle() {
      const size = this.brushSize + 2;
      return {
        background: this.rgba.toRgbaString(),
        width: size + "px",
        height: size + "px"
      };
    }
  },
  watch: {
    rgba: {
      immediate: true,
      handler() {
        this.$emit("changeColor", {
          rgba: this.rgba,
          hsv: this.hsv
        });
      }
    },
    brushSize: {
      immediate: true,
      handler() {
        this.$emit("changeBrushSize", this.brushSize);
      }
    }
  },
  created() {
    this.hueWidth = 15;
    this.hueHeight = 152;
    this.sizeWidth = 15;
    this.sizeHeight = 152;
    this.selectedColorHeight = 30;

    if (this.colorsHistory) {
      this.setColorValue(this.colorsHistory[0]);
    } else {
      this.setColorValue(this.color);
    }
    this.setColorPos();
    this.setSizePos();
  },
  destroyed() {
    this.setcolorsHistory(this.colorSelected);
  },
  methods: {
    async toggle() {
      if (this.hidden) {
        this.hidden = false;
        await this.$nextTick();
        this.renderHue(this.$refs.canvasHue, this.hueWidth, this.hueHeight);
        this.renderSize(this.$refs.canvasSize, this.sizeWidth, this.sizeHeight);
        this.renderSaturation(
          this.$refs.canvasSaturation,
          this.hueCornerRgbaString(),
          this.hueHeight
        );
      } else {
        this.hidden = true;
        this.setcolorsHistory(this.colorSelected);
      }
    },
    inputColor(e) {
      this.setColorValue(e.target.value);
      this.setColorPos();
      this.renderSaturation(
        this.$refs.canvasSaturation,
        this.hueCornerRgbaString(),
        this.hueHeight
      );
      this.colorSelected = this.rgba.toRgbaString();
    },
    setcolorsHistory(color) {
      if (color) {
        const colors = this.colorsHistory;
        const index = colors.indexOf(color);
        if (index >= 0) {
          colors.splice(index, 1);
        }
        if (colors.length >= 7) {
          colors.length = 7;
        }
        colors.unshift(color);
        this.colorsHistory = colors;
      }
      let history = {
        colors: this.colorsHistory,
        size: this.brushSize
      };
      localStorage.setItem(this.historyKey, JSON.stringify(history));
    },
    setColorValue(color) {
      let rgba = { r: 0, g: 0, b: 0, a: 1 };
      if (/#/.test(color)) {
        rgba = this.hex2rgba(color);
      } else if (/rgb/.test(color)) {
        rgba = this.rgb2rgba(color);
      } else if (Object.prototype.toString.call(color) === "[object Object]") {
        rgba = color;
      }
      const { r, g, b, a } = rgba;
      this.r = r;
      this.g = g;
      this.b = b;
      this.a = a || a === 0 ? a : 1;
      const { h, s, v } = this.rgb2hsv(this.rgba);
      this.h = h;
      this.s = s;
      this.v = v;
    },
    setColorPos() {
      this.slideSaturationStyle = {
        left: this.s * this.hueHeight - 5 + "px",
        top: (1 - this.v) * this.hueHeight - 5 + "px"
      };
      this.slideHueStyle = {
        top: (1 - this.h / 360) * this.hueHeight - 2 + "px"
      };
    },
    setSizePos() {
      const range = MAX_BRUSH_SIZE - MIN_BRUSH_SIZE;
      this.slideSizeStyle = {
        top:
          (1 - (this.brushSize - MIN_BRUSH_SIZE) / range) * this.sizeHeight -
          2 +
          "px"
      };
    },
    selectColor(color) {
      this.setColorValue(color);
      this.setColorPos();
      this.renderSaturation(
        this.$refs.canvasSaturation,
        this.hueCornerRgbaString(),
        this.hueHeight
      );
      this.colorSelected = this.rgba.toRgbaString();
    },
    selectSaturation(e) {
      e.preventDefault();
      e.stopPropagation();
      const {
        top: saturationTop,
        left: saturationLeft
      } = this.$refs.saturation.getBoundingClientRect();
      const ctx = e.target.getContext("2d");

      const mousemove = e => {
        let x = e.clientX - saturationLeft;
        let y = e.clientY - saturationTop;

        if (x < 0) {
          x = 0;
        }
        if (y < 0) {
          y = 0;
        }
        if (x > this.hueHeight) {
          x = this.hueHeight;
        }
        if (y > this.hueHeight) {
          y = this.hueHeight;
        }

        this.slideSaturationStyle = {
          left: x - 5 + "px",
          top: y - 5 + "px"
        };
        const imgData = ctx.getImageData(
          Math.min(x, this.hueHeight - 1),
          Math.min(y, this.hueHeight - 1),
          1,
          1
        );
        const [r, g, b] = imgData.data;
        this.setColorValue({ r, g, b });
      };

      mousemove(e);

      const mouseup = () => {
        document.removeEventListener("mousemove", mousemove);
        document.removeEventListener("mouseup", mouseup);
        this.colorSelected = this.rgba.toRgbaString();
      };

      document.addEventListener("mousemove", mousemove);
      document.addEventListener("mouseup", mouseup);
    },
    selectHue(e) {
      e.preventDefault();
      e.stopPropagation();
      const { top: hueTop } = this.$refs.hue.getBoundingClientRect();
      const ctx = e.target.getContext("2d");

      const mousemove = e => {
        let y = e.clientY - hueTop;

        if (y < 0) {
          y = 0;
        }
        if (y > this.hueHeight) {
          y = this.hueHeight;
        }

        this.slideHueStyle = {
          top: y - 2 + "px"
        };
        const imgData = ctx.getImageData(
          0,
          Math.min(y, this.hueHeight - 1),
          1,
          1
        );
        const [r, g, b] = imgData.data;
        const { h } = this.rgb2hsv({ r, g, b });
        const color = this.hsv2rgb({ h, s: this.s, v: this.v });
        this.setColorValue(color);
        this.renderSaturation(
          this.$refs.canvasSaturation,
          this.hueCornerRgbaString(),
          this.hueHeight
        );
        this.colorSelected = this.rgba.toRgbaString();
      };

      mousemove(e);

      const mouseup = () => {
        document.removeEventListener("mousemove", mousemove);
        document.removeEventListener("mouseup", mouseup);
      };

      document.addEventListener("mousemove", mousemove);
      document.addEventListener("mouseup", mouseup);
    },
    selectSize(e) {
      e.preventDefault();
      e.stopPropagation();
      const { top: sizeTop } = this.$refs.size.getBoundingClientRect();

      const mousemove = e => {
        let y = e.clientY - sizeTop;

        if (y < 0) {
          y = 0;
        }
        if (y > this.sizeHeight) {
          y = this.sizeHeight;
        }

        this.slideSizeStyle = {
          top: y - 2 + "px"
        };
        const min = MIN_BRUSH_SIZE;
        const max = MAX_BRUSH_SIZE;
        this.brushSize = Math.max(
          min,
          Math.min(max, (1 - y / this.sizeHeight) * (max - min) + min)
        );
      };

      mousemove(e);

      const mouseup = () => {
        document.removeEventListener("mousemove", mousemove);
        document.removeEventListener("mouseup", mouseup);
      };

      document.addEventListener("mousemove", mousemove);
      document.addEventListener("mouseup", mouseup);
    },
    renderSaturation(canvas, color, size) {
      const ctx = canvas.getContext("2d");
      canvas.width = size;
      canvas.height = size;

      ctx.fillStyle = color;
      ctx.fillRect(0, 0, size, size);

      this.createLinearGradient(
        "l",
        ctx,
        size,
        size,
        "#FFFFFF",
        "rgba(255,255,255,0)"
      );
      this.createLinearGradient(
        "p",
        ctx,
        size,
        size,
        "rgba(0,0,0,0)",
        "#000000"
      );
    },
    renderHue(canvas, width, height) {
      const ctx = canvas.getContext("2d");
      canvas.width = width;
      canvas.height = height;

      const gradient = ctx.createLinearGradient(0, 0, 0, height);
      gradient.addColorStop(0, "#FF0000");
      gradient.addColorStop(0.17 * 1, "#FF00FF");
      gradient.addColorStop(0.17 * 2, "#0000FF");
      gradient.addColorStop(0.17 * 3, "#00FFFF");
      gradient.addColorStop(0.17 * 4, "#00FF00");
      gradient.addColorStop(0.17 * 5, "#FFFF00");
      gradient.addColorStop(1, "#FF0000");
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, width, height);
    },
    renderSize(canvas, width, height) {
      const ctx = canvas.getContext("2d");
      canvas.width = width;
      canvas.height = height;

      ctx.beginPath();
      ctx.strokeStyle = "#999999";
      ctx.lineCap = "round";
      ctx.moveTo(width / 2, 2);
      ctx.lineTo(width / 2, height - 2);
      ctx.stroke();
    },
    createLinearGradient(direction, ctx, width, height, color1, color2) {
      const isL = direction === "l";
      const gradient = ctx.createLinearGradient(
        0,
        0,
        isL ? width : 0,
        isL ? 0 : height
      );
      gradient.addColorStop(0.01, color1);
      gradient.addColorStop(0.99, color2);
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, width, height);
    },
    rgb2hex({ r, g, b }, toUpper) {
      const change = val => ("0" + Number(val).toString(16)).slice(-2);
      const color = `#${change(r)}${change(g)}${change(b)}`;
      return toUpper ? color.toUpperCase() : color;
    },
    hex2rgba(hex) {
      hex = hex.slice(1);
      const change = val => parseInt(val, 16) || 0;
      return {
        r: change(hex.slice(0, 2)),
        g: change(hex.slice(2, 4)),
        b: change(hex.slice(4, 6)),
        a: 1
      };
    },
    rgb2rgba(rgba) {
      if (typeof rgba === "string") {
        rgba = (/rgba?\((.*?)\)/.exec(rgba) || ["", "0,0,0,1"])[1].split(",");
        return {
          r: Number(rgba[0]) || 0,
          g: Number(rgba[1]) || 0,
          b: Number(rgba[2]) || 0,
          a: Number(rgba[3] ? rgba[3] : 1)
        };
      } else {
        return rgba;
      }
    },
    rgb2hsv({ r, g, b }) {
      r = r / 255;
      g = g / 255;
      b = b / 255;
      const max = Math.max(r, g, b);
      const min = Math.min(r, g, b);
      const delta = max - min;
      let h = 0;
      if (max === min) {
        h = 0;
      } else if (max === r) {
        if (g >= b) {
          h = (60 * (g - b)) / delta;
        } else {
          h = (60 * (g - b)) / delta + 360;
        }
      } else if (max === g) {
        h = (60 * (b - r)) / delta + 120;
      } else if (max === b) {
        h = (60 * (r - g)) / delta + 240;
      }
      h = Math.floor(h);
      let s = parseFloat((max === 0 ? 0 : 1 - min / max).toFixed(2));
      let v = parseFloat(max.toFixed(2));
      return { h, s, v };
    },
    hsv2rgb({ h, s, v }) {
      // https://stackoverflow.com/a/17243070
      let r, g, b, i, f, p, q, t;
      i = Math.floor(h / 60);
      f = h / 60 - i;
      p = v * (1 - s);
      q = v * (1 - f * s);
      t = v * (1 - (1 - f) * s);
      switch (i % 6) {
        case 0:
          (r = v), (g = t), (b = p);
          break;
        case 1:
          (r = q), (g = v), (b = p);
          break;
        case 2:
          (r = p), (g = v), (b = t);
          break;
        case 3:
          (r = p), (g = q), (b = v);
          break;
        case 4:
          (r = t), (g = p), (b = v);
          break;
        case 5:
          (r = v), (g = p), (b = q);
          break;
      }
      return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
      };
    },
    hueCornerRgbaString() {
      let { r, g, b } = this.hsv2rgb({ h: this.h, s: 1, v: 1 });
      return `rgb(${[r, g, b].join(",")})`;
    }
  }
};
</script>

<style lang="scss">
.hu-overall {
  text-align: right;
}
.hu-hidden-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  box-sizing: border-box;
  box-shadow: 0 0 16px 0 rgba(0, 0, 0, 0.2);
  vertical-align: top;
  display: inline-block;
  transition: all 0.1s;
  cursor: pointer;
  &:hover {
    transform: scale(1.4);
  }
}
.hu-color-picker {
  padding: 10px;
  background: $backdrop;
  border-radius: 4px;
  box-shadow: 0 0 16px 0 rgba(0, 0, 0, 0.2);
  z-index: 1;
  &.light {
    background: #f7f8f9;
    .colors.history {
      border-top: 1px solid #eee;
    }
  }
  canvas {
    vertical-align: top;
  }
  .color-set {
    display: flex;
    .size {
      position: relative;
      cursor: pointer;
      .slide {
        position: absolute;
        left: 0;
        top: 100px;
        width: 100%;
        height: 4px;
        background: #fff;
        box-shadow: 0 0 1px 0 rgba(0, 0, 0, 0.3);
        pointer-events: none;
      }
    }
    .saturation {
      position: relative;
      cursor: pointer;
      margin-left: 8px;
      .slide {
        position: absolute;
        left: 100px;
        top: 0;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        border: 1px solid #fff;
        box-shadow: 0 0 1px 1px rgba(0, 0, 0, 0.3);
        pointer-events: none;
      }
    }
    .hue {
      position: relative;
      margin-left: 8px;
      cursor: pointer;
      .slide {
        position: absolute;
        left: 0;
        top: 100px;
        width: 100%;
        height: 4px;
        background: #fff;
        box-shadow: 0 0 1px 0 rgba(0, 0, 0, 0.3);
        pointer-events: none;
      }
    }
  }
  .color-show {
    margin-top: 8px;
    display: flex;
    .show-circle {
      width: 15px;
      margin-right: 8px;
      position: relative;
      .color {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        right: 0;
        margin: auto;
        clip-path: circle();
      }
    }
    .show {
      position: relative;
      flex: 1;
      .color {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
      }
    }
  }
  .colors {
    padding: 0;
    margin: 0;
    &.history {
      margin-top: 10px;
      border-top: 1px solid $disabled;
    }
    .item {
      position: relative;
      width: 16px;
      height: 16px;
      margin: 10px 0 0 10px;
      border-radius: 3px;
      box-sizing: border-box;
      vertical-align: top;
      display: inline-block;
      transition: all 0.1s;
      cursor: pointer;
      &:nth-child(8n + 1) {
        margin-left: 0;
      }
      &:hover {
        transform: scale(1.4);
      }
      .color {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        border-radius: 3px;
      }
    }
  }
}
</style>

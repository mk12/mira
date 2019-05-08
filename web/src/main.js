// These must be imported first for the correct CSS order.
import "@/assets/reset.scss";
import "@/assets/global.scss";

import Vue from "vue";
import App from "@/App.vue";
import router from "@/router";

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");

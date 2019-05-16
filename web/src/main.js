// These must be imported first for the correct CSS order.
import "@/assets/reset.scss";
import "@/assets/global.scss";

import App from "@/App.vue";
import Vue from "vue";
import router from "@/router";
import store from "@/store";

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");

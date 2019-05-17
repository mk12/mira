// These must be imported first for the correct CSS order.
import "@/assets/reset.scss";
import "@/assets/global.scss";

import Vue from "vue";

import auth from "@/auth";
import router from "@/router";
import store from "@/store";

import App from "@/App.vue";

function main() {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount("#app");
}

auth.autoLogin().finally(main);

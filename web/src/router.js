import Vue from "vue";
import Router from "vue-router";

import Home from "@/views/Home.vue";
import LogIn from "@/views/LogIn.vue";
import NotFound from "@/views/NotFound.vue";
import SignUp from "@/views/SignUp.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    // {
    //   path: "/about",
    //   name: "about",
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () =>
    //     import(/* webpackChunkName: "about" */ "@/views/About.vue")
    // },
    {
      path: "/signup",
      name: "signup",
      component: SignUp,
      props: true
    },
    {
      path: "/login",
      name: "login",
      component: LogIn,
      props: true
    },
    {
      path: "*",
      name: "404",
      component: NotFound
    }
  ]
});

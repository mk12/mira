import Vue from "vue";
import Router from "vue-router";

import auth from "@/auth";

import Index from "@/views/Index.vue";
import LogIn from "@/views/LogIn.vue";
import NotFound from "@/views/NotFound.vue";
import Settings from "@/views/Settings.vue";
import SignUp from "@/views/SignUp.vue";

Vue.use(Router);

let router = new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "index",
      component: Index
    },
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
      path: "/settings",
      name: "settings",
      component: Settings,
      meta: { loginRequired: true }
    },
    // {
    //   path: "/friends",
    //   name: "friends",
    //   component: Friends,
    //   meta: { loginRequired: true },
    //   children: [
    //     {
    //       path: ":username",
    //       name: "friend",
    //       component: Friend,
    //       meta: { loginRequired: true },
    //       children: [
    //         {
    //           path: "canvas",
    //           name: "canvas",
    //           component: Canvas,
    //           meta: { loginRequired: true }
    //         }
    //       ]
    //     }
    //   ]
    // },
    {
      path: "*",
      name: "404",
      component: NotFound
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (
    to.matched.some(record => record.meta.loginRequired) && !auth.isLoggedIn()
  ) {
    next({
      path: "/login",
      query: { redirect: to.fullPath }
    });
  } else {
    next();
  }
});

export default router;

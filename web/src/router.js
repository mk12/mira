import Vue from "vue";
import Router from "vue-router";

import auth from "@/auth";
import store from "@/store";

import AddFriend from "@/views/AddFriend.vue";
import Canvas from "@/views/Canvas.vue";
import ChangePassword from "@/views/ChangePassword.vue";
import DeleteAccount from "@/views/DeleteAccount.vue";
import Friend from "@/views/Friend.vue";
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
      component: Index,
      meta: { dataRequired: true }
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
    {
      path: "/settings/add_friend",
      name: "add_friend",
      component: AddFriend,
      meta: { loginRequired: true }
    },
    {
      path: "/settings/change_password",
      name: "change_password",
      component: ChangePassword,
      meta: { loginRequired: true }
    },
    {
      path: "/settings/delete_account",
      name: "delete_account",
      component: DeleteAccount,
      meta: { loginRequired: true }
    },
    {
      path: "/friends/:username",
      name: "friend",
      component: Friend,
      meta: { loginRequired: true, dataRequired: true },
      props: true
    },
    {
      path: "/friends/:username/canvas",
      name: "canvas",
      component: Canvas,
      meta: { loginRequired: true },
      props: true
    },
    {
      path: "*",
      name: "404",
      component: NotFound
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (
    to.matched.some(record => record.meta.loginRequired) &&
    !auth.isLoggedIn()
  ) {
    next({
      path: "/login",
      query: { redirect: to.fullPath }
    });
  } else {
    next();
  }
});

router.afterEach(to => {
  if (to.matched.some(record => record.meta.dataRequired)) {
    store.dispatch("refresh");
  }
});

export default router;

<template>
  <div class="wrapper">
    <div class="container">
      <transition name="cross-fade">
        <router-view :key="routerKey" class="container__content" />
      </transition>
      <nav class="container__navigation">
        <ul class="nav-list">
          <li class="nav-list__item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <template v-if="isLoggedIn()">
            <li class="nav-list__item">
              <router-link to="/settings" class="nav-link"
                >Settings</router-link
              >
            </li>
            <li class="nav-list__item">
              <a href="#" class="nav-link" @click.prevent="logout">Log out</a>
            </li>
          </template>
          <template v-else>
            <li class="nav-list__item">
              <router-link to="/signup" class="nav-link">Sign up</router-link>
            </li>
            <li class="nav-list__item">
              <router-link to="/login" class="nav-link">Log in</router-link>
            </li>
          </template>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import auth from "@/auth";

export default {
  name: "App",

  computed: {
    ...mapState([
      "routerKey"
    ])
  },

  methods: {
    isLoggedIn() {
      return auth.isLoggedIn();
    },

    async logout() {
      await auth.logout();
      this.$router.push("/");
    }
  }
};
</script>

<style lang="scss">
.wrapper {
  min-width: 100%;
  min-height: 100%;
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: $backdrop;
}

.container {
  margin: 50px;
  padding: 0;
  background: $background;
  border-image: asset("border.png") #{214} / #{103px} / #{14px} round;
  width: $app-size;
  height: $app-size;
  min-height: $app-size;
  position: relative;

  &__content {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
  }

  &__navigation {
    position: absolute;
    bottom: -55px;
    left: 0px;
    right: 0px;
  }
}

.nav-list {
  margin: 0;
  padding: 0;
  text-align: center;

  &__item {
    display: inline-block;
    margin: 15px;
  }
}

.nav-link {
  color: $subtle;
  border: 0;

  &:hover {
    border: 0;
  }
}

.router-link-exact-active {
  color: $action;
  cursor: default;
  pointer-events: none;
}
</style>

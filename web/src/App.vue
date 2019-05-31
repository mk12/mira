<template>
  <div class="wrapper">
    <div class="container">
      <transition name="cross-fade">
        <router-view class="absolute-fill" />
      </transition>
      <nav class="container__navigation">
        <ul class="nav-list">
          <li class="nav-list__item">
            <router-link to="/" class="subtle-link">Home</router-link>
          </li>
          <template v-if="isLoggedIn">
            <li class="nav-list__item">
              <router-link to="/settings" class="subtle-link"
                >Settings</router-link
              >
            </li>
            <li class="nav-list__item">
              <a href="#" class="subtle-link" @click.prevent="logout"
                >Log out</a
              >
            </li>
          </template>
          <template v-else>
            <li class="nav-list__item">
              <router-link to="/signup" class="subtle-link"
                >Sign up</router-link
              >
            </li>
            <li class="nav-list__item">
              <router-link to="/login" class="subtle-link">Log in</router-link>
            </li>
          </template>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "App",

  computed: {
    ...mapGetters("auth", ["isLoggedIn"])
  },

  methods: {
    async logout() {
      await this.$store.dispatch("auth/logout");
      this.$router.push("/");
    }
  }
};
</script>

<style lang="scss" scoped>
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
  border-style: solid;
  border-image: asset("border.png") #{214} / #{103px} / #{14px} round;
  width: $app-size;
  height: $app-size;
  min-height: $app-size;
  position: relative;

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

.router-link-exact-active {
  color: $action;
  cursor: default;
  pointer-events: none;
}
</style>

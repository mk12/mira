<template>
  <div class="absolute-fill">
    <transition name="cross-fade">
      <div v-if="showLogout" key="logout" class="text-page">
        <h1>Logout required</h1>
        <p>
          You are already logged in as <strong>{{ username }}</strong
          >.
        </p>
        <p>To view this page, you must log out.</p>
        <ul class="vert-list">
          <li class="vert-list__item">
            <ActionButton :submit="logout" value="Log out" />
          </li>
          <li class="vert-list__item">
            <router-link to="/">Go to homepage</router-link>
          </li>
        </ul>
      </div>
      <div v-else key="content" class="absolute-fill">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "LogoutRequired",

  components: {
    ActionButton
  },

  data() {
    return {
      showLogout: true
    };
  },

  computed: {
    ...mapGetters("auth", ["isLoggedIn"]),
    ...mapState("auth", ["username"])
  },

  methods: {
    ...mapActions("auth", ["logout"])
  },

  watch: {
    isLoggedIn: {
      immediate: true,
      handler(loggedInNow) {
        this.showLogout = this.showLogout && loggedInNow;
      }
    }
  }
};
</script>

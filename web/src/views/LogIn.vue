<template>
  <div v-if="isLoggedIn" class="text-page">
    <!-- FIXME SHOWS UP WHEN FADING OUT AFTER LOGIN :( -->
    <p>
      You are already logged in as <strong>{{ username }}</strong
      >!
    </p>
    <ActionButton :submit="logout" value="Log out" />
  </div>
  <BasicForm
    v-else
    title="Log in"
    action="Log in"
    v-bind="{ fields, submit, prefill }"
  >
    <template #instructions
      >Please enter your username and password.</template
    >
    <template #extra="{ form }">
      <router-link :to="signupRoute(form)"
        >Want to create an account?</router-link
      >
    </template>
  </BasicForm>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import { genericErrorMessage } from "@/util";

import ActionButton from "@/components/ActionButton.vue";
import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "LogIn",

  components: {
    ActionButton,
    BasicForm
  },

  props: {
    prefill: Object
  },

  created() {
    this.fields = [
      {
        id: "username",
        type: "text",
        label: "Username",
        placeholder: "Enter username",
        required: "Please enter a username."
      },
      {
        id: "password",
        type: "password",
        label: "Password",
        placeholder: "Enter password",
        required: "Please enter a password."
      }
    ];
  },

  computed: {
    ...mapGetters("auth", ["isLoggedIn"]),
    ...mapState("auth", ["username"])
  },

  methods: {
    ...mapActions("auth", ["logout"]),

    signupRoute(form) {
      return {
        name: "signup",
        params: { prefill: form },
        query: this.$route.query
      };
    },

    async submit(form) {
      try {
        await this.$store.dispatch("auth/login", {
          username: form.username.value,
          password: form.password.value
        });
      } catch (error) {
        return genericErrorMessage(error);
      }
      this.$router.push(this.$route.query.redirect || "/");
    }
  }
};
</script>

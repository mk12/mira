<template>
  <LogoutRequired>
    <BasicForm
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
  </LogoutRequired>
</template>

<script>
import { genericErrorMessage } from "@/util";

import BasicForm from "@/components/BasicForm.vue";
import LogoutRequired from "@/components/LogoutRequired.vue";

export default {
  name: "LogIn",

  components: {
    BasicForm,
    LogoutRequired
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

  methods: {
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
      await this.$nextTick();
      this.$router.push(this.$route.query.redirect || "/");
    }
  }
};
</script>

<template>
  <BasicForm
    title="Log in"
    action="Log in"
    v-bind="{ fields, submit, prefill }"
  >
    <template #instructions>
      Please enter your username and password.
    </template>
    <template #extra="{ form }">
      <router-link :to="signupRoute(form)"
        >Want to create an account?</router-link
      >
    </template>
  </BasicForm>
</template>

<script>
import auth from "@/auth";
import { genericFormError } from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "LogIn",

  components: {
    BasicForm
  },

  props: {
    prefill: Object
  },

  data() {
    return {
      fields: [
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
      ]
    };
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
        await auth.login(form.username.value, form.password.value);
      } catch (error) {
        return genericFormError(error);
      }
      this.$router.push(this.$route.query.redirect || "/");
    }
  }
};
</script>

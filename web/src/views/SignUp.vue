<template>
  <BasicForm
    title="Sign up"
    action="Register"
    v-bind="{ fields, validate, submit, prefill }"
  >
    <template #instructions>
      Please choose a username and password.
    </template>
    <template #extra="{ form }">
      <router-link :to="loginRoute(form)"
        >Already have an account?</router-link
      >
    </template>
  </BasicForm>
</template>

<script>
import api from "@/api";
import { MIN_PASSWORD_LENGTH } from "@/constants.js";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "SignUp",

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
          placeholder: "Choose a username",
          required: "Please choose a username"
        },
        {
          id: "password",
          type: "password",
          label: "Password",
          placeholder: "Choose a password",
          required: "Please choose a password"
        },
        {
          id: "passwordConfirm",
          type: "password",
          label: "Confirm",
          placeholder: "Confirm password",
          required: "Please confirm password"
        }
      ]
    };
  },

  methods: {
    loginRoute(form) {
      return {
        name: "login",
        params: {prefill: form}
      };
    },

    validate(form) {
      if (form.password.value !== form.passwordConfirm.value) {
        form.password.error = true;
        form.passwordConfirm.error = true;
        return "Passwords do not match.";
      }
      if (form.password.value.length < MIN_PASSWORD_LENGTH) {
        form.password.error = true;
        form.passwordConfirm.error = true;
        return `Password must be at least ${MIN_PASSWORD_LENGTH} characters.`;
      }
    },

    async submit(form) {
      let credentials = {
        username: form.username.value,
        password: form.password.value
      };
      try {
        await api.post("register", credentials);
        await api.post("login", credentials);
        this.$router.push({ name: "home" });
      } catch (error) {
        if (error.response.data.code === "username_taken") {
          form.username.error = true;
          return "Username is already taken.";
        }
        return "An unknown error occurred.";
      }
    }
  }
};
</script>

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
import api from "@/api";

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
          required: "Please enter a username"
        },
        {
          id: "password",
          type: "password",
          label: "Password",
          placeholder: "Enter password",
          required: "Please enter a password"
        }
      ]
    };
  },

  methods: {
    signupRoute(form) {
      return {
        name: "signup",
        params: {prefill: form}
      };
    },

    async submit(form) {
      let credentials = {
        username: form.username.value,
        password: form.password.value
      };
      try {
        await api.post("login", credentials);
        this.$store.commit("login", credentials.username);
        this.$router.push({name: "index"});
        return "foo";
      } catch (error) {
        if (error.response.data.code === "login_fail") {
          return "Wrong username or password.";
        }
        return "An unknown error occurred.";
      }
    }
  }
};
</script>

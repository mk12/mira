<template>
  <BasicForm
    title="Delete account"
    action="Delete my account"
    v-bind="{ fields, submit }"
  >
    <template #instructions
      >Please confirm your password.</template
    >
  </BasicForm>
</template>

<script>
import api from "@/api";
import { errorMessage, errorStatus, genericErrorMessage } from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "DeleteAccount",

  components: {
    BasicForm
  },

  created() {
    this.fields = [
      {
        id: "password",
        type: "password",
        label: "Password",
        placeholder: "Enter password",
        required: "Please enter your password."
      }
    ];
  },

  methods: {
    async submit(form) {
      try {
        await api.delete("account", {
          data: { password: form.password.value }
        });
        await this.$store.dispatch("auth/logout", { skipServer: true });
      } catch (error) {
        switch (errorStatus(error)) {
          case 401:
            return errorMessage("Invalid password.");
          default:
            return genericErrorMessage(error);
        }
      }
      this.$router.push(this.$route.query.redirect || "/");
    }
  }
};
</script>

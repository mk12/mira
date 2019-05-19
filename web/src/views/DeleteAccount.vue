<template>
  <BasicForm
    title="Delete account"
    action="Delete my account"
    v-bind="{ fields, submit }"
  >
    <template #instructions>
      Please confirm your password.
    </template>
  </BasicForm>
</template>

<script>
import auth from "@/auth";
import { errorStatusIs, formError, genericFormError } from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "DeleteAccount",

  components: {
    BasicForm
  },

  data() {
    return {
      fields: [
        {
          id: "password",
          type: "password",
          label: "Password",
          placeholder: "Enter password",
          required: "Please enter your password."
        }
      ]
    };
  },

  methods: {
    async submit(form) {
      try {
        await auth.deleteAccount(form.password.value);
      } catch (error) {
        if (errorStatusIs(error, 401)) {
          return formError("Invalid password.");
        }
        return genericFormError(error);
      }
      this.$router.push(this.$route.query.redirect || "/");
    }
  }
};
</script>

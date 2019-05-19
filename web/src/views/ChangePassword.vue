<template>
  <BasicForm
    title="Change password"
    action="Change"
    v-bind="{ fields, validate, submit }"
  >
    <template #instructions>
      Please confirm your current password and choose a new password.
    </template>
  </BasicForm>
</template>

<script>
import auth from "@/auth";
import { MIN_PASSWORD_LENGTH } from "@/constants";
import { errorStatusIs, formError, genericFormError } from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "ChangePassword",

  components: {
    BasicForm
  },

  data() {
    return {
      fields: [
        {
          id: "oldPassword",
          type: "password",
          label: "Old password",
          placeholder: "Enter old password",
          required: "Please enter your old password."
        },
        {
          id: "newPassword",
          type: "password",
          label: "New password",
          placeholder: "Enter new password",
          required: "Please choose a new password."
        }
      ]
    };
  },

  methods: {
    validate(form) {
      if (form.oldPassword.value === form.newPassword.value) {
        form.newPassword.error = true;
        return "New password must be different.";
      }
      if (form.newPassword.value.length < MIN_PASSWORD_LENGTH) {
        form.newPassword.error = true;
        return `New password must be at least ${MIN_PASSWORD_LENGTH} characters.`;
      }
    },

    async submit(form) {
      try {
        await auth.changePassword(
          form.oldPassword.value,
          form.newPassword.value
        );
      } catch (error) {
        if (errorStatusIs(error, 401)) {
          return formError("Invalid password.");
        }
        return genericFormError(error);
      }
      this.$router.push(this.$route.query.redirect || "/login");
    }
  }
};
</script>

<style lang="scss" scoped>
/deep/ .label {
  width: 120px;
}
</style>

<template>
  <BasicForm
    title="Change password"
    action="Change"
    v-bind="{ fields, validate, submit }"
  >
    <template #instructions
      >Please confirm your current password and choose a new password.</template
    >
  </BasicForm>
</template>

<script>
import api from "@/api";
import { MIN_PASSWORD_LENGTH } from "@/constants";
import { errorStatus, formError, genericFormError } from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "ChangePassword",

  components: {
    BasicForm
  },

  created() {
    this.fields = [
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
    ];
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
        await api.put("change_password", {
          password: form.oldPassword.value,
          new_password: form.newPassword.value
        });
        await this.$store.dispatch("auth/logout", { skipServer: true });
      } catch (error) {
        switch (errorStatus(error)) {
          case 401:
            return formError("Invalid password.");
          default:
            return genericFormError(error);
        }
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

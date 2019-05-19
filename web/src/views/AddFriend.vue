<template>
  <BasicForm title="Add friend" action="Add friend" v-bind="{ fields, submit }">
    <template #instructions>
      Enter the username of the friend you wish to add.
    </template>
  </BasicForm>
</template>

<script>
import api from "@/api";
import { errorCodeIs, formError, formSuccess, genericFormError } from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "AddFriend",

  components: {
    BasicForm
  },

  data() {
    return {
      fields: [
        {
          id: "username",
          type: "text",
          label: "Username",
          placeholder: "Enter friend's username",
          required: "Please enter a username."
        }
      ]
    };
  },

  methods: {
    async submit(form) {
      let username = form.username.value;
      try {
        let response = await api.put(`friends/${encodeURIComponent(username)}`);
        if (response.data.code === "accept") {
          return formSuccess(`Became friends with ${username}.`);
        }
        return formSuccess(`Sent friend request to ${username}.`);
      } catch (error) {
        if (errorCodeIs(error, "unknown_user")) {
          return formError("There is no one with that username.");
        }
        if (errorCodeIs(error, "self")) {
          return formError("You cannot add yourself as a friend.");
        }
        if (errorCodeIs(error, "maximum")) {
          return formError("You already have the maximum number of friends.");
        }
        return genericFormError(error);
      }
    }
  }
};
</script>

<template>
  <BasicForm title="Add friend" action="Add friend" v-bind="{ fields, submit }">
    <template #instructions
      >Enter the username of the friend you wish to add.</template
    >
    <template #message
      >{{ message }}
      <router-link :to="{ name: 'friend', params: { username } }">{{
        username
      }}</router-link
      >.
    </template>
  </BasicForm>
</template>

<script>
import api from "@/api";
import {
  errorCode,
  errorMessage,
  genericErrorMessage,
  successMessage
} from "@/util";

import BasicForm from "@/components/BasicForm.vue";

export default {
  name: "AddFriend",

  components: {
    BasicForm
  },

  created() {
    this.fields = [
      {
        id: "username",
        type: "text",
        label: "Username",
        placeholder: "Enter friend's username",
        required: "Please enter a username."
      }
    ];
  },

  data() {
    return {
      message: null,
      username: null
    };
  },

  methods: {
    async submit(form) {
      let username = form.username.value;
      let response;
      try {
        response = await api.put("friends/" + encodeURIComponent(username));
      } catch (error) {
        switch (errorCode(error)) {
          case "unknown_user":
            return errorMessage("There is no one with that username.");
          case "self":
            return errorMessage("You cannot add yourself as a friend.");
          case "maximum":
            return errorMessage(
              "You already have the maximum number of friends."
            );
          default:
            return genericErrorMessage(error);
        }
      }

      this.username = username;
      switch (response.data.code) {
        case "accept":
          this.message = "Became friends with";
          return successMessage();
        case "request":
          this.message = "Sent friend request to";
          return successMessage();
        case "no_op_accept":
          this.message = "Already friends with";
          return successMessage();
        case "no_op_request":
          this.message = "Already sent friend request to";
          return successMessage();
        default:
          return errorMessage("Unexpected server response.");
      }
    }
  }
};
</script>

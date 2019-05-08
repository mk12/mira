<template>
  <AccountForm
    title="Sign up"
    instructions="Please choose a username and password."
    alternateView="login"
    alternateLabel="Already have an account?"
    submitLabel="Create"
    confirm
    :prefill="prefill"
    @submit="submit"
  />
</template>

<script>
import api from "@/api";

import AccountForm from "@/components/AccountForm.vue";

export default {
  name: "SignUp",
  props: {
    prefill: Object
  },
  components: {
    AccountForm
  },
  methods: {
    submit(credentials) {
      // disable button
      // show registering
      // show result
      // re-enable button slash possibly redirect
      api
        .post("register", credentials)
        .then(response => {
          alert(response.data);
        })
        .catch(err => {
          // handle 429
          alert(err);
        });
    }
  }
};
</script>

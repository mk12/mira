<template>
  <AccountForm
    title="Log in"
    instructions="Please enter your username and password."
    alternateView="signup"
    alternateLabel="Want to create an account?"
    submitLabel="Log in"
    :prefill="prefill"
    @submit="submit"
  />
</template>

<script>
import AccountForm from "@/components/AccountForm.vue";

export default {
  name: "LogIn",
  props: {
    prefill: Object
  },
  components: {
    AccountForm
  },
  methods: {
    submit(input) {
      alert(process.env.NODE_ENV);
    }
  }
};
</script>

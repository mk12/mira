<template>
  <button class="button" :disabled="submitting" @click.prevent="click()">
    {{ buttonLabel }}
  </button>
</template>

<script>
export default {
  name: "SubmitButton",

  props: {
    value: String,
    submit: Function
  },

  data() {
    return {
      submitting: false
    };
  },

  computed: {
    buttonLabel() {
      return this.submitting ? "..." : this.value;
    }
  },

  methods: {
    async click() {
      this.submitting = true;
      try {
        await this.submit();
      } finally {
        this.submitting = false;
      }
    }
  }
};
</script>

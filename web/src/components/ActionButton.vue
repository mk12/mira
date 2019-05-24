<template>
  <button
    type="button"
    class="button"
    :disabled="submitting"
    @click.prevent="click"
  >
    <div v-if="submitting" class="button__loader"></div>
    <span
      class="button__text"
      :class="{ 'button__text--submitting': submitting }"
      >{{ value }}</span
    >
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

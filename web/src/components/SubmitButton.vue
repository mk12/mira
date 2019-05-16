<template>
  <input
    type="submit"
    class="button"
    :value="currentValue"
    :disabled="submitting"
  />
</template>

<script>
export default {
  name: "SubmitButton",
  props: {
    value: String,
    submitting: Boolean
  },
  computed: {
    currentValue() {
      return this.submitting ? ". . ." : this.value;
    }
  }
};
</script>

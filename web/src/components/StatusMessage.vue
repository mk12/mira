<template>
  <transition name="abrupt-fade" appear>
    <p v-if="message" :key="messageKey" :class="messageClass">
      <template v-if="message.text === undefined">
        <slot />
      </template>
      <template v-else>{{ message.text }}</template>
    </p>
  </transition>
</template>

<script>
export default {
  name: "StatusMessage",

  props: {
    message: Object
  },

  data() {
    return {
      messageKey: 0
    };
  },

  watch: {
    message: function() {
      this.messageKey++;
    }
  },

  computed: {
    messageClass() {
      return {
        "success-message": this.message.success,
        "error-message": this.message.error
      };
    }
  }
};
</script>

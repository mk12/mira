<template>
  <div class="text-page">
    <h1>{{ title }}</h1>
    <p><slot name="instructions" /></p>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <div v-for="field in fields" :key="field.id" class="form-group__item">
          <label :for="field.id" class="label">{{ field.label }}</label>
          <input
            :id="field.id"
            v-model="form[field.id].value"
            :type="field.type"
            class="text-input"
            :class="{ 'text-input--error': form[field.id].error }"
            :placeholder="field.placeholder"
            autocorrect="off"
            autocapitalize="none"
          />
        </div>
      </div>

      <div class="form-group">
        <div class="form-group__item">
          <button class="button" :disabled="submitting">
            <div v-if="submitting" class="button__loader"></div>
            <span
              class="button__text"
              :class="{ 'button__text--submitting': submitting }"
              >{{ action }}</span
            >
          </button>
        </div>
        <div v-if="!!this.$scopedSlots.extra" class="form-group__item">
          <slot name="extra" :form="form" />
        </div>
      </div>
      <StatusMessage :message="message">
        <slot name="message" />
      </StatusMessage>
    </form>
  </div>
</template>

<script>
import { errorMessage } from "@/util";

import StatusMessage from "@/components/StatusMessage.vue";

export default {
  name: "BasicForm",

  components: {
    StatusMessage
  },

  props: {
    title: String,
    action: String,
    fields: Array,
    validate: {
      type: Function,
      default: () => {}
    },
    submit: Function,
    prefill: {
      type: Object,
      default: () => ({})
    }
  },

  data() {
    let form = {};
    for (let field of this.fields) {
      let input = this.prefill[field.id];
      form[field.id] = {
        value: input ? input.value : "",
        error: false
      };
    }
    return {
      form,
      message: null,
      messageKey: 0,
      submitting: false
    };
  },

  methods: {
    validateForm() {
      let error = null;
      for (let field of this.fields) {
        let input = this.form[field.id];
        input.error = field.required && !input.value;
        if (input.error) {
          error = error || field.required;
        }
      }
      error = error || this.validate(this.form);
      this.message = error ? errorMessage(error) : null;
      return !error;
    },

    async submitForm() {
      if (this.validateForm()) {
        this.submitting = true;
        try {
          let result = await this.submit(this.form);
          if (result) {
            this.message = result;
          }
        } finally {
          this.submitting = false;
        }
      }
    }
  }
};
</script>

<template>
  <div class="text-page">
    <h1>{{ title }}</h1>
    <p><slot name="instructions" /></p>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <div
          v-for="field in fields"
          :key="field.id"
          class="form-group__item"
        >
          <label :for="field.id" class="label">{{ field.label }}</label>
          <input
            :id="field.id"
            v-model="form[field.id].value"
            :type="field.type"
            class="text-input"
            :class="{ 'text-input--error': form[field.id].error }"
            :placeholder="field.placeholder"
          />
        </div>
      </div>

      <div class="form-group">
        <div class="form-group__item">
          <input
            type="submit"
            class="button"
            :value="submitValue"
            :disabled="submitting"
          />
        </div>
        <div v-if="!!this.$scopedSlots.extra" class="form-group__item">
          <slot name="extra" :form="form" />
        </div>
      </div>
      <div v-if="errorMessage" class="form-group">
        <div class="form-group__item">
          <p class="error-message">{{ errorMessage }}</p>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "BasicForm",

  props: {
    title: String,
    action: String,
    fields: Array,
    validate: {
      type: Function,
      default: () => {}
    },
    submit: {
      type: Function,
      default: () => Promise.resolve()
    },
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
      }
    }
    return {
      form,
      errorMessage: null,
      submitting: false
    };
  },

  computed: {
    submitValue() {
      return this.submitting ? "..." : this.action;
    }
  },

  methods: {
    validateForm() {
      this.errorMessage = null;
      for (let field of this.fields) {
        let input = this.form[field.id];
        input.error = field.required && !input.value;
        if (input.error) {
          this.errorMessage = this.errorMessage || field.required;
        }
      }
      this.errorMessage = this.errorMessage || this.validate(this.form);
      return !this.errorMessage;
    },

    async submitForm() {
      if (this.validateForm()) {
        this.submitting = true;
        try {
          let result = await this.submit(this.form);
          if (result) {
            this.errorMessage = result;
          }
        } finally {
          this.submitting = false;
        }
      }
    }
  }
};
</script>

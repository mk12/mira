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
      <transition name="abrupt-fade" appear>
        <div v-if="message" :key="messageKey" class="form-group">
          <div class="form-group__item">
            <p :class="messageClass">
              <template v-if="message.slot">
                <slot name="message" />
              </template>
              <template v-else>
                {{ message.text }}
              </template>
            </p>
          </div>
        </div>
      </transition>
    </form>
  </div>
</template>

<script>
import { formError } from "@/util";

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
      };
    }
    return {
      form,
      message: null,
      messageKey: 0,
      submitting: false
    };
  },

  computed: {
    messageClass() {
      return {
        "success-message": !this.message.error,
        "error-message": this.message.error
      };
    }
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
      this.message = error ? formError(error) : null;
      this.messageKey++;
      return !error;
    },

    async submitForm() {
      if (this.validateForm()) {
        this.submitting = true;
        try {
          let result = await this.submit(this.form);
          if (result) {
            this.message = result;
            this.messageKey++;
          }
        } finally {
          this.submitting = false;
        }
      }
    }
  }
};
</script>

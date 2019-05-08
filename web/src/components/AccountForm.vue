<template>
  <div class="text-page">
    <h1>{{ title }}</h1>
    <p>{{ instructions }}</p>
    <form @submit.prevent="submit">
      <div class="form-group">
        <div class="form-group__item">
          <label for="username" class="label">Username</label>
          <input
            id="username"
            v-model.trim="username"
            type="text"
            class="text-input"
            :class="{ 'text-input--error': error.username }"
            placeholder="Enter username"
          />
        </div>
        <div class="form-group__item">
          <label for="password" class="label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="text-input"
            :class="{ 'text-input--error': error.password }"
            placeholder="Enter password"
          />
        </div>
        <div v-if="confirm" class="form-group__item">
          <label for="password-confirm" class="label">Confirm</label>
          <input
            id="password-confirm"
            v-model="passwordConfirm"
            class="text-input"
            :class="{ 'text-input--error': error.passwordConfirm }"
            type="password"
            placeholder="Confirm password"
          />
        </div>
      </div>
      <div class="form-group">
        <div class="form-group__item">
          <input
            type="submit"
            class="button"
            :value="submitLabel"
            :disabled="!submitEnabled"
          />
        </div>
        <div class="form-group__item">
          <router-link :to="alternateLocation">{{
            alternateLabel
          }}</router-link>
        </div>
      </div>
      <div class="form-group">
        <div class="form-group__item">
          <p class="error-message">{{ error.message }}</p>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { MIN_PASSWORD_LENGTH } from "@/constants.js";

export default {
  name: "AccountForm",
  props: {
    title: String,
    instructions: String,
    alternateView: String,
    alternateLabel: String,
    submitLabel: String,
    confirm: Boolean,
    prefill: {
      type: Object,
      default: () => ({})
    }
  },

  data() {
    return {
      username: this.prefill.username,
      password: this.prefill.password,
      passwordConfirm: "",
      error: {},
      submitEnabled: true
    };
  },

  computed: {
    fields() {
      let list = ["username", "password"];
      if (this.confirm) {
        list.push("passwordConfirm");
      }
      return list;
    },

    alternateLocation() {
      return {
        name: this.alternateView,
        params: {
          prefill: {
            username: this.username,
            password: this.password
          }
        }
      };
    }
  },

  methods: {
    validate() {
      let err = {};
      for (let field of this.fields) {
        if (!this[field]) {
          err[field] = true;
        }
      }
      if (!this.username) {
        err.message = "Please enter a username.";
      } else if (!this.password) {
        err.message = "Please enter a password.";
      } else if (this.confirm && !this.passwordConfirm) {
        err.message = "Please confirm your password.";
      } else if (this.confirm && this.password !== this.passwordConfirm) {
        err.password = true;
        err.passwordConfirm = true;
        err.message = "Passwords do not match.";
      } else if (this.confirm && this.password.length < MIN_PASSWORD_LENGTH) {
        err.password = true;
        err.passwordConfirm = true;
        err.message = `Password must be at least ${MIN_PASSWORD_LENGTH} characters.`;
      }
      this.error = err;
      return err.message === undefined;
    },

    submit() {
      if (this.validate()) {
        this.$emit("submit", {
          username: this.username,
          password: this.password
        });
      }
    }
  }
};
</script>

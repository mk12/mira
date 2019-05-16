<template>
  <div class="text-page">
    <h1>Mira</h1>
    <ul class="button-list">
      <li class="button-list__item">
        <button @click="logout()" class="button">Log out</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Home",
  methods: {
    logout() {
      this.$store.commit("logout");
    }
  }
};
</script>

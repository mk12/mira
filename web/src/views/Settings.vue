<template>
  <div class="text-page">
    <h1>Settings</h1>
    <p>
      You are currently logged in as <strong>{{ username }}</strong
      >.
    </p>
    <ul class="vert-list">
      <li class="vert-list__item">
        <router-link to="/settings/add_friend">Add friends</router-link>
      </li>
      <li class="vert-list__item">
        <router-link to="/settings/change_password"
          >Change password</router-link
        >
      </li>
      <li class="vert-list__item">
        <router-link to="/settings/delete_account">Delete account</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Settings",

  computed: {
    ...mapState(["username"])
  }
};
</script>

<template>
  <div class="text-page">
    <h1>Settings</h1>
    <p>Here are the settings you can manage:</p>
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
export default {
  name: "Settings"
};
</script>

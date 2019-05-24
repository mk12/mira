<template>
  <!-- FIXME SHOWS UP WHEN FADING OUT AFTER LOGIN :( -->
  <!-- make non-reactive? -->
  <div class="full-height">
    <div v-if="isLoggedIn" key="logout" class="text-page">
      <p>
        You are already logged in as <strong>{{ username }}</strong
        >!
      </p>
      <ActionButton :submit="logout" value="Log out" />
    </div>
    <div v-else key="content" class="full-height">
      <slot />
    </div>
  </div>
</template>

<template>
  <div class="text-page">
    <h1>Welcome to Mira</h1>
    <p>Mira is a fun and simple communication app.</p>
    <ul class="bullets">
      <li class="bullets__item">Share messages or doodles with a friend.</li>
      <li class="bullets__item">Drawings slowly fade away over 24 hours.</li>
      <li class="bullets__item">No notifications. Just check when you want.</li>
    </ul>
    <p>
      Sound good? Start using it today
      <img
        src="@/assets/smile.svg"
        width="16"
        height="16"
        style="vertical-align: -6%;"
      />
    </p>
    <ul class="horiz-list">
      <li class="horiz-list__item">
        <router-link to="/signup" tag="button" class="button"
          >Sign up</router-link
        >
      </li>
      <li class="horiz-list__item">
        <router-link to="/login" tag="button" class="button"
          >Log in</router-link
        >
      </li>
    </ul>
  </div>
</template>

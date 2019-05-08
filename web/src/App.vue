<template>
  <div class="wrapper">
    <div class="container">
      <!-- <div class="banner"> -->
      <!--   <router-link to="/" class="banner__link">M</router-link> -->
      <!-- </div> -->
      <router-view class="container__content" />
    </div>
  </div>
</template>

<style lang="scss">
.wrapper {
  min-width: 100%;
  min-height: 100%;
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: $backdrop;
}

.banner {
  position: relative;
  top: -40px;
  text-align: center;
}

.banner__link {
  border: none;
  text-align: center;
}

.container {
  margin: 50px;
  padding: 0;
  background: $background;
  border-image: asset("border.png") #{214} / #{103px} / #{14px} round;
  width: $app-size;
  height: $app-size;
  min-height: $app-size;
  position: relative;

  &__content {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
  }
}
</style>

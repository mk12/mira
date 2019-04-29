<template>
  <div class="wrapper">
    <div class="container">
      <router-view />
    </div>
    <div class="toolbar">
      <router-view name="toolbar" />
    </div>
  </div>
</template>

<style lang="scss">
.wrapper {
  min-width: 100%;
  min-height: 100vh;
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: $light-blue;
}

.container {
  margin: 50px;
  padding: 0;
  background: $light-yellow;
  border-image: asset("border.png") #{214} / #{103px} / #{14px} round;
  width: $app-size;
  height: $app-size;
  min-height: $app-size;
  position: relative;
}

.toolbar {
  display: flex;
  justify-content: center;
  opacity: 0;
  text-align: center;
}

.toolbar--permanent,
.toolbar:hover {
  opacity: 1;
}

.toolbar--transition {
  /* https://stackoverflow.com/questions/9245030 */
  transition: opacity 0.5s cubic-bezier(0.02, 0.01, 0.47, 1);
}

.toolbar__link {
  padding: 0 20px;
}
</style>

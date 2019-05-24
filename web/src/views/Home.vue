<template>
  <div class="text-page">
    <LoadPage ref="load" :resource="resource">
      <template v-if="friends">
        <div v-if="!friends.length" class="center-box">
          <p class="friend-message">Friends will show up here!</p>
          <router-link to="/settings/add_friend">Add friends</router-link>
        </div>
        <div v-else class="friend-grid">
          <div
            v-for="friend in friends"
            :key="friend.username"
            class="friend-grid__item"
          >
            <CanvasThumbnail :username="friend.username" :reload="reload" />
            <router-link
              :to="{ name: 'friend', params: { username: friend.username } }"
              class="small"
              >{{ friend.username }}</router-link
            >
          </div>
        </div>
      </template>
    </LoadPage>
  </div>
</template>

<script>
import { MAX_FRIENDS } from "@/constants";

import CanvasThumbnail from "@/components/CanvasThumbnail.vue";
import LoadPage from "@/components/LoadPage.vue";

export default {
  name: "Home",

  components: {
    CanvasThumbnail,
    LoadPage
  },

  created() {
    this.resource = { loader: "allFriends" };
  },

  computed: {
    friends() {
      let friends = this.$store.getters["data/get"](this.resource);
      return friends ? friends.slice(0, MAX_FRIENDS) : null;
    }
  },

  methods: {
    async reload() {
      await this.$refs.load.reload();
    }
  }
};
</script>

<style lang="scss" scoped>
/deep/ .friend-grid {
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-items: center;
  align-content: center;
  height: 100%;

  &__item {
    margin: 15px;
    flex-basis: fit-content;
  }
}

/deep/ .friend-message {
  color: $disabled;
}
</style>

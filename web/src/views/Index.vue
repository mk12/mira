<script>
import auth from "@/auth";

import Home from "@/views/Home.vue";
import Welcome from "@/views/Welcome.vue";

export default {
  name: "Index",
  functional: true,
  render(h, ctx) {
    let component = auth.isLoggedIn() ? Home : Welcome;
    return h(component, ctx.data, ctx.children);
  }
};
</script>

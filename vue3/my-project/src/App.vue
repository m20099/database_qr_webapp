<template>
  <v-app>
    <Header />
    <div class="content">
      <router-view />
    </div>
    <bottom-nav />
  </v-app>
</template>

<script>
import Header from './components/Header.vue';
import BottomNav from './components/BottomNav.vue';

export default {
  components: {
    Header,
    BottomNav,
  },
};
</script>

<style>
body {
  background-color: #FBFEFF;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.content {
  margin-top: 63px;
  padding-bottom: 56px;
}

</style>

<template>
  <div id="app">
    <Header />
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/Header.vue';

export default {
  components: {
    Header,
  },
};
</script>

<style>
body {
  background-color: #FBFEFF;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>

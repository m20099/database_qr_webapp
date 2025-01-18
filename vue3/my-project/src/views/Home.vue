<template>
  <v-container fluid class="home-container">
        <v-row
          class="hero-section"
          justify="center"
          align="center"
        >
          <v-col cols="12" md="6" class="text-center">
            <h1 class="text-h4 font-weight-bold mb-4">
              QRコードを利用した<br />支出履歴管理システム
            </h1>
            <p class="text-subtitle-1">
              レシート情報が格納されたQRコードを<br />読み取るだけで簡単に支出を記録
            </p>
          </v-col>
        </v-row>
    </v-container>

</template>

<script>
export default {
  name: "HomePage",
  computed: {
    bottomNavHeight() {
      return window.innerWidth < 960 ? 56 : 0;
    },
  },
};
</script>

<style scoped>
.home-container {
  position: fixed;
  top: -75px;
  bottom: calc(env(bottom-nav-height, 0px));
  left: 0;
  right: 0;
  background: linear-gradient(90deg, #0b3a63, #135389, #0b3a63);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
}

.hero-section {
  text-align: center;
  padding: 40px, 10%;
}

</style>
<template>
  <v-container fluid class="home-container">
    <v-carousel cycle height="400" class="custom-carousel" :show-arrows="false">
      <v-carousel-item>
        <v-row
          class="hero-section"
          justify="center"
          align="center"
          style="min-height: 400px;"
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
      </v-carousel-item>

      <v-carousel-item>
        <v-row
          class="page-section"
          justify="center"
          align="center"
          style="background: linear-gradient(90deg, #0b3a63, #135389, #0b3a63); min-height: 400px;"
        >
        </v-row>
      </v-carousel-item>


      <v-carousel-item>
        <v-row
          class="page-section"
          justify="center"
          align="center"
          style="background: linear-gradient(90deg, #0b3a63, #135389, #0b3a63); min-height: 400px;"
        >
        </v-row>
      </v-carousel-item>
    </v-carousel>
    <v-container class="how-to-use">
      <v-row>
        <v-col cols="12" class="text-center mb-6">
          <h2 class="text-h4 font-weight-bold">How to Use</h2>
          <p class="text-subtitle-1">
            未定
          </p>
        </v-col>
      </v-row>
  </v-container>
    </v-container>

</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      carouselItems: [
        { src: "/images/slide1.jpg" },
        { src: "/images/slide2.jpg" },
      ],
    };
  },
};
</script>

<style scoped>
.home-container {
  font-family: 'Roboto', sans-serif;
  padding: 0;
}

.hero-section {
  padding: 40px 10%;
  background: linear-gradient(90deg, #0b3a63, #135389, #0b3a63);
  color: white;
  box-sizing: border-box;
}

.hero-actions .v-btn {
  font-size: 1em;
}

/* 高さ調整 */
.custom-carousel .v-carousel-item {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* メディアクエリ */
@media (max-width: 768px) {
  .hero-section {
    padding: 20px;
  }
}
</style>

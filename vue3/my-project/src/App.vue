<template>
  <div id="app">
    <h2>QR Web App Demo</h2>
    <div class="qr-container">
      <QRCodeGenerator />
      <QRCodeScanner />
    </div>
  </div>
</template>

<script>
import QRCodeGenerator from './components/QRCodeGenerator.vue';
import QRCodeScanner from './components/QRCodeScanner.vue'

export default {
  components: {
    QRCodeGenerator,
    QRCodeScanner
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 20px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

.qr-container {
  display: flex;
  gap: 20px; /* コンポーネント間のスペース */
}

</style>

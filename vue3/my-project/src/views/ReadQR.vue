<template>
  <div class="userhome-container">
    <h1>QR Code Scanner</h1>

    <div class="qrcode-wrapper">
      <qrcode-stream @detect="onDetect" @init="onInit" class="qrcode-stream"></qrcode-stream>
      <div class="guideline"><div></div></div>
    </div>

    <div v-if="decodedText" class="decoded-result">
      <p>読み取り結果:</p>
      <p class="result">{{ decodedText }}</p>
    </div>
  </div>
</template>

<script>
import { QrcodeStream } from 'vue-qrcode-reader'

export default {
  name: 'ReadQR',
  components: {
    QrcodeStream
  },
  data() {
    return {
      decodedText: null,
    }
  },
  methods: {
    onDetect(detectedCodes) {
      console.log('デコード結果:', detectedCodes);
      if (detectedCodes.length > 0) {
        this.decodedText = detectedCodes[0].rawValue;
      }
    },
    onInit(promise) {
      promise
        .then(() => {
          console.log("カメラが正常に初期化されました");
        })
        .catch(error => {
          console.error("カメラの初期化に失敗しました:", error);
        });
    }
  }
}
</script>

<style scoped>
.userhome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  font-size: 2em;
  color: #333;
  margin-bottom: 20px;
}

.qrcode-wrapper {
  width: 250px;
  height: 250px;
  position: relative;
  border: 2px solid transparent;
  overflow: hidden;
}

.guideline {
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  bottom: 15px;
  pointer-events: none;
}

.guideline::before,
.guideline::after,
.guideline div::before,
.guideline div::after {
  content: "";
  position: absolute;
  width: 30px;
  height: 30px;
  border: 4px solid #ffffff;
  border-radius: 10%;
}

.guideline::before {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.guideline::after {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.guideline div::before {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

.guideline div::after {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}


.qrcode-stream {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.decoded-result {
  margin-top: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.result {
  font-size: 1.2em;
  color: #333;
  font-weight: bold;
  word-break: break-all;
}
</style>

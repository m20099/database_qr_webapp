<template>
  <div class="userhome-container">
    <h1>QR Code Scanner</h1>

    <!-- QRコードリーダー -->
    <div class="qrcode-wrapper">
      <qrcode-stream @detect="onDetect" @init="onInit" class="qrcode-stream"></qrcode-stream>
    </div>

    <!-- 読み取り結果表示 -->
    <div v-if="decodedText" class="decoded-result">
      <p>読み取り結果:</p>
      <p class="result">{{ decodedText }}</p>
    </div>
    <div v-else>
      <p>QRコードをスキャン</p>
    </div>
  </div>
</template>

<script>
import { QrcodeStream } from 'vue-qrcode-reader'

export default {
  name: 'UserHome',
  components: {
    QrcodeStream
  },
  data() {
    return {
      decodedText: null,  // 初期値をnull
    }
  },
  methods: {
    // QRコードのデコード結果を受け取る
    onDetect(detectedCodes) {
      console.log('デコード結果:', detectedCodes);
      if (detectedCodes.length > 0) {
        this.decodedText = detectedCodes[0].rawValue;
      }
    },
    // 初期化完了後の処理
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
  width: 150px;
  height: 150px;
  overflow: hidden;
  position: relative;
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

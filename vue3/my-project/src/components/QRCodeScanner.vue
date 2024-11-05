<template>
  <div>
    <h3>Scanner</h3>    
    <div class="qr-code-scanner">
      <qrcode-stream class="camera-view" @detect="onDetect" @init="onInit"></qrcode-stream>
    </div>
    <div v-if="qrCodeData" class="result">
      <h3>Scan result:</h3>
      <p>{{ qrCodeData }}</p>
    </div>
  </div>
</template>

<script>
import { QrcodeStream } from "vue-qrcode-reader";

export default {
  components: {
    QrcodeStream,
  },
  data() {
    return {
      qrCodeData: null,
    };
  },
  methods: {
    async onDetect(result) {
      console.log('Decoded QR code:', result);
      this.qrCodeData = result[0].rawValue;

      fetch('http://localhost:5000/api/qr-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code_content: this.qrCodeData }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => console.log("QR data sent successfully:", data.message))
      .catch(error => {
        console.error("Error sending QR code data:", error);
        alert("QRコードのデータ送信に失敗しました。");
      });
    },
    onInit(promise) {
      promise.then(() => {
        console.log('Camera initialized successfully');
      }).catch(error => {
        console.error('Camera initialization error:', error);
        alert('カメラが利用できません。');
      });
    }
  }
};
</script>

<style scoped>
.qr-code-scanner {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 200px;
  height: 200px;
}
.result {
  width:200px;
}
</style>

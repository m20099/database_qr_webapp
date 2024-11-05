<template>
  <div class="qr-generator">
    <h3>QR Code Generator</h3>
    <input v-model="text" placeholder="Enter text" /><br>

    <label>
      Size:
      <input type="number" v-model.number="size" placeholder="Enter size" min="100" max="1000" />
    </label><br>

    <label>
      Error Correction Level:
      <select v-model="errorCorrectionLevel">
        <option value="L">Low (L)</option>
        <option value="M">Medium (M)</option>
        <option value="Q">Quartile (Q)</option>
        <option value="H">High (H)</option>
      </select>
    </label><br>

    <label>
      Color:
      <input type="color" v-model="color" />
    </label><br>

    <button @click="generateQRCode">Generate</button>
    
    <div v-if="qrCodeDataUrl" class="qr-code">
      <img :src="qrCodeDataUrl" alt="QR Code" />
    </div>
  </div>
</template>

<script>
import QRCode from 'qrcode';

export default {
  data() {
    return {
      text: '',
      size: 200,  // デフォルトのサイズ
      errorCorrectionLevel: 'M',  // デフォルトのエラー補正レベル
      color: '#000000',  // デフォルトのQRコード色
      qrCodeDataUrl: null
    };
  },
  methods: {
    async generateQRCode() {
      try {
        // QRコード生成のオプション
        const options = {
          width: this.size,
          errorCorrectionLevel: this.errorCorrectionLevel,
          color: {
            dark: this.color,
            light: '#FFFFFF' // 背景色（白色）
          }
        };

        // QRコードをBase64のDataURLとして生成
        this.qrCodeDataUrl = await QRCode.toDataURL(this.text, options);
      } catch (error) {
        console.error('Failed to generate QR code:', error);
      }
    }
  }
};
</script>

<style scoped>
.qr-generator {
  display: flex;
  flex-direction: column;
  align-items: center;
}

input, select {
  padding: 8px;
  margin-bottom: 10px;
  width: 80%;
  max-width: 300px;
  font-size: 16px;
}

button {
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
}

.qr-code {
  margin-top: 20px;
}
</style>

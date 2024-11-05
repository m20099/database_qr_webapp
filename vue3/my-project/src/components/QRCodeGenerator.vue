<template>
  <div>
    <h3>Generator</h3>
    <input v-model="text" placeholder="Enter text" /><br>
    <button @click="generateQRCode">Generate</button>
    <div v-if="qrCodeDataUrl">
      <img :src="qrCodeDataUrl" alt="QR Code" />
    </div>
  </div>
</template>

<script>
import QRCode from 'qrcode'

export default {
  data() {
    return {
      text: '',
      qrCodeDataUrl: null
    }
  },
  methods: {
    async generateQRCode() {
      try {
        this.qrCodeDataUrl = await QRCode.toDataURL(this.text)
      } catch (error) {
        console.error('Failed to generate QR code:', error)
      }
    }
  }
}
</script>

<style scoped>
.qr-generator {
  display: flex;
  flex-direction: column;
  align-items: center;
}

input {
  padding: 8px;
  margin-bottom: 10px;
  width: 80%;
  max-width: 300px;
  max-height: 15px;
  font-size: 16px;
}
</style>

<template>
  <div class="store-home-container">
    <h2 class="page-title">QR Code Generator</h2>

    <div class="content-container">
      <div class="form-container">
        <!-- 店名 -->
        <div class="form-group">
          <label for="store-name">店名</label>
          <input type="text" id="store-name" v-model="storeName" placeholder="店名を入力" />
        </div>

        <!-- 場所 -->
        <div class="form-group">
          <label for="store-location">場所</label>
          <input type="text" id="store-location" v-model="storeLocation" placeholder="場所を入力" />
        </div>

        <!-- 自由記述欄 -->
        <div class="form-group">
          <label for="store-description">自由記述欄</label>
          <textarea id="store-description" v-model="storeDescription" placeholder="適当な情報を入力、検討中"></textarea>
        </div>

        <!-- QRコード生成・クリアボタン -->
        <div class="button-group">
          <button @click="clearInput" class="clear-button">CLEAR</button>
          <button @click="generateQRCode">GENERATE</button>
        </div>

        <p v-if="errorMessage" class="form-error-message">※Please fill in the required fields.</p>
      </div>

      <!-- QRコード表示エリア -->
      <div class="qr-code-container">
        <div class="qr-code-display">
          <div v-if="qrCodeDataUrl">
            <img :src="qrCodeDataUrl" alt="Generated QR Code" />
          </div>
          <div v-else class="qr-placeholder">ここにQRコードが表示</div>
        </div>

        <!-- QRコード保存ボタン -->
        <div class="button-group">
            <button @click="saveQRCodeAsPng" :disabled="!qrCodeDataUrl">DL as PNG</button>
            <button @click="saveQRCodeAsJpeg" :disabled="!qrCodeDataUrl">DL as JPG</button>
            <button @click="saveToDatabase" :disabled="!qrCodeDataUrl || isLoading">
                <span v-if="isLoading" class="spinner"></span>
                <span v-else>SAVE</span>
            </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'StoreHome',
  data() {
    return {
      storeName: '',
      storeLocation: '',
      storeDescription: '',
      qrCodeDataUrl: null,
      errorMessage: false,
      isLoading: false,
    };
  },
  methods: {
    async generateQRCode() {
      if (!this.storeName || !this.storeLocation || !this.storeDescription) {
        this.errorMessage = true;
        return;
      }

      this.errorMessage = false;
      const data = {
        storeName: this.storeName,
        storeLocation: this.storeLocation,
        storeDescription: this.storeDescription
      };

      try {
        this.qrCodeDataUrl = await QRCode.toDataURL(JSON.stringify(data));
        console.log('QRコード生成:', this.qrCodeDataUrl);
      } catch (error) {
        console.error('QRコード生成エラー:', error);
      }
    },

    clearInput() {
      this.storeName = '';
      this.storeLocation = '';
      this.storeDescription = '';
      this.qrCodeDataUrl = null;
      this.errorMessage = false;
    },

    saveQRCodeAsPng() {
      this.saveQRCode('png');
    },

    saveQRCodeAsJpeg() {
      this.saveQRCode('jpeg');
    },

    saveQRCode(format) {
      const link = document.createElement('a');
      link.href = this.qrCodeDataUrl.replace('image/png', `image/${format}`);
      link.download = `qr_code.${format}`;
      link.click();
    },

    async saveToDatabase() {
      const confirmation = confirm('保存しますか？');
      if (!confirmation) {
        return;
      }
      this.isLoading = true;
      const data = {
        storeName: this.storeName,
        storeLocation: this.storeLocation,
        storeDescription: this.storeDescription,
      };

      fetch('http://localhost:5000/api/qr-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      setTimeout(() => {
        this.isLoading = false;
      }, 500);
      console.log('データベースに保存');
    },
  }
};

</script>

<style scoped>
.store-home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.page-title {
  font-size: 24px;
  color: #30343A;
  margin-bottom: 20px;
  text-align: center;
}

.content-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1000px;
  box-sizing: border-box;
}


.form-container, .qr-code-container {
  width: 48%;
  padding: 20px 30px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
  height: 100%;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ddd;
  margin-bottom: 15px;
  box-sizing: border-box;
}

textarea {
  height: 120px;
  resize: none;
}

.button-group {
  height: 50px;
  display: flex;
  gap: 10px;
  justify-content: space-between;
  margin-top: auto;
}

button {
  width: 48%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.clear-button {
  background-color: #6c757d;
  color: white;
}

.clear-button:hover {
  background-color: #5a6268;
}


button:not(.clear-button) {
  background-color: #135389;
  color: white;
}

button:not(.clear-button):hover {
  background-color: #1d7ed1;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.input-error {
  border: 2px solid red;
}

.form-error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

.qr-code-display {
  width: 100%;
  max-width: 420px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #ddd;
  margin-top: 16px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
}

.qr-placeholder {
  color: #aaa;
  font-size: 14px;
}

.qr-code-display img {
  max-width: 100%;
  max-height: 100%;
}
</style>

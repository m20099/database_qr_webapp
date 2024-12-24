<template>
  <div class="userhome-container">
    <h1>QR Code Scanner</h1>

    <div class="qrcode-wrapper">
      <qrcode-stream @detect="onDetect" @init="onInit" class="qrcode-stream"></qrcode-stream>
      <div class="guideline"><div></div></div>
    </div>

  <div v-if="decodedData" class="decoded-data">
      <h2>デコードされた内容</h2>
      <p><strong>ストアID:</strong> {{ decodedData.storeId }}</p>
      <p><strong>購入日時:</strong> {{ decodedData.purchaseDate }}</p>
      <h3>商品リスト</h3>
      <ul>
        <li v-for="item in decodedData.items" :key="item.id">
          商品ID: {{ item.id }} / 数量: {{ item.quantity }}
        </li>
      </ul>
    </div>

    <div v-else-if="decodedText" class="decoded-error">
      <p>QRコードのデコードに失敗しました。</p>
    </div>
    </div>
</template>

<script>
import { QrcodeStream } from 'vue-qrcode-reader'
import pako from "pako";
import axios from "axios";

export default {
  name: 'ReadQR',
  components: {
    QrcodeStream
  },
  data() {
    return {
      decodedText: null,
      decodedData: null,
      user: null,
    }
  },

  methods: {

    async onInit(promise) {
        try {
            await promise;
            console.log("カメラが正常に初期化されました");
        } catch (error) {
            console.error("カメラの初期化に失敗しました:", error);
        }
    },

    async onDetect(detectedCodes) {
      if (detectedCodes.length > 0) {
        this.decodedText = detectedCodes[0].rawValue;
        await this.decodeQRCode(this.decodedText);
      }
    },

    async decodeQRCode(base64Data) {
      try {
        const compressedData = Uint8Array.from(atob(base64Data), c => c.charCodeAt(0));
        const decompressedData = pako.inflate(compressedData, { to: "string" });
        const parsedData = JSON.parse(decompressedData);

        if (parsedData.storeId && parsedData.purchaseDate && Array.isArray(parsedData.items)) {
          this.decodedData = parsedData;

          console.log("Decoded QR Code Data:", {
            store_id: this.decodedData.storeId,
            purchase_date: this.decodedData.purchaseDate,
            items: this.decodedData.items,
          });

          console.log("デコード完了、データ送信を開始します...");
          await this.sendDataToDatabase(this.decodedData);
        } else {
          throw new Error('データ形式が不正です');
        }

      } catch (error) {
        console.error('デコードエラー:', error);
        this.decodedData = null;
        alert('QRコードのデコードに失敗しました。');
      }
    },

    async sendDataToDatabase(data) {
    try {
        const userId = localStorage.getItem("user");
        if (!userId) {
        throw new Error("ユーザー情報が見つかりません");
        }

        const payload = {
            user_id: userId,
            store_id: data.storeId,
            purchase_date: data.purchaseDate,
            items: data.items.map(item => ({
                item_id: item.id,
                quantity: item.quantity,
            }))
        };

        console.log("送信データ:", JSON.stringify(payload, null, 2)); // 確認用ログ

        const response = await axios.post('http://localhost:5000/api/purchases', payload);

        console.log("レスポンス内容:", response);

        if (response.status === 201) {
        alert("購入データが正常に登録されました！");
        } else {
        throw new Error("サーバーエラーが発生しました");
        }
    } catch (error) {
        console.error("データ送信エラー:", error);
        alert("購入データの登録に失敗しました！");
    }
    }
  },
};
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
  width: 100vw;
  height: 80vh;
  max-width: 300px;
  max-height: 300px;
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
  border-radius: 5%;
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

.decoded-item {
  background: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.result {
  font-size: 1.2em;
  color: #333;
  font-weight: bold;
  word-break: break-all;
}
</style>

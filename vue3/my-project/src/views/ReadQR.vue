<template>
  <v-container class="userhome-container">
    <v-row justify="center">
      <v-col cols="12" md="8" class="text-center">
        <h1>QR Code Scanner</h1>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="6">
        <div class="qrcode-wrapper">
          <qrcode-stream @detect="onDetect" @init="onInit" class="qrcode-stream"></qrcode-stream>
          <div class="guideline"><div></div></div>
        </div>
      </v-col>
    </v-row>

    <v-row justify="center" v-if="decodedData">
      <v-col cols="12" md="8">
        <v-card class="pa-4" outlined>
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-center">Result<br />ストアID：{{ decodedData.storeId }}<br />購入日時：{{ decodedData.purchaseDate }}</span>
          </v-card-title>
          <v-card-text style="max-height: 300px; overflow-y: auto;">
            <v-list v-if="decodedData.items.length">
              <v-list-item v-for="item in decodedData.items" :key="item.item_name" class="mb-2" >
                <template v-slot:prepend>
                  <v-avatar size="40" :style="{ border: '1px solid #135389' }">
                    <v-icon color="#135389" size="24">mdi-cube</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-content>
                  <v-list-item-title class="text-h6">
                    {{ item.item_name }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-2 text-gray">
                    価格: ¥{{ item.price.toLocaleString() }} / 数量: {{ item.quantity }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" v-else-if="decodedText">
      <v-col cols="12" md="6">
        <v-alert type="error" outlined>
          QRコードのデコードに失敗しました。
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { ref } from 'vue';
import { QrcodeStream } from 'vue-qrcode-reader';
import pako from "pako";
import axios from "axios";

export default {
  name: 'ReadQR',
  components: {
    QrcodeStream
  },
    setup() {
        const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
        const decodedText = ref(null);
        const decodedData = ref(null);
        const user = ref(null);

        const onInit = async (promise) => {
            try {
                await promise;
                console.log("カメラが正常に初期化されました");
            } catch (error) {
                console.error("カメラの初期化に失敗しました:", error);
            }
        };

        const onDetect = async (detectedCodes) => {
            if (detectedCodes.length > 0) {
                decodedText.value = detectedCodes[0].rawValue;
                await decodeQRCode(decodedText.value);
            }
        };

        const decodeQRCode = async (base64Data) => {
        try {
            const compressedData = Uint8Array.from(atob(base64Data), c => c.charCodeAt(0));
            const decompressedData = pako.inflate(compressedData, { to: "string" });
            const parsedData = JSON.parse(decompressedData);

            if (Array.isArray(parsedData) && parsedData.length === 3 && Array.isArray(parsedData[2])) {
            const [storeId, purchaseDate, items] = parsedData;
            decodedData.value = {
              storeId,
              purchaseDate,
              items: items.map(item => ({
                item_name: item[0],
                price: item[1],
                quantity: item[2]
              }))
            };

            console.log("Decoded QR Code Data:", {
                store_id: decodedData.value.storeId,
                purchase_date: decodedData.value.purchaseDate,
                items: decodedData.value.items,
            });

            console.log("デコード完了、データ送信を開始します...");
            await sendDataToDatabase(decodedData.value);
            } else {
            throw new Error('データ形式が不正です');
            }
        } catch (error) {
            console.error('デコードエラー:', error);
            decodedData.value = null;
            alert('QRコードのデコードに失敗しました。');
        }
        };

        const sendDataToDatabase = async (data) => {
        try {
            const userId = localStorage.getItem("user");
            if (!userId) {
            throw new Error("ユーザー情報が見つかりません");
            }

            const payload = {
            user_id: userId,
            store_id: data.storeId,
            purchase_date: data.purchaseDate,
            items: data.items
            };

            console.log("送信データ:", JSON.stringify(payload, null, 2));

            const response = await axios.post(`${API_BASE_URL}/api/purchases`, payload);

            console.log("レスポンス内容:", response);

            if (response.status === 201) {
            alert("購入データが正常に登録されました！");
            } else {
            throw new Error("サーバーエラーが発生しました");
            }
        } catch (error) {
            console.error("データ送信エラー:", error);
            if (error.response && error.response.status === 400) {
                alert("このデータはすでに登録されています！");
            } else {
                alert("購入データの登録に失敗しました！");
            }
        }
        };

    return {
      decodedText,
      decodedData,
      user,
      onInit,
      onDetect,
      decodeQRCode
    };
  },
};
</script>

<style scoped>
.userhome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

h1 {
  font-size: 2em;
  color: #333;
}

.v-card {
  max-width: 500px;
  margin: auto;
  box-shadow: none !important;
  border: 1.0px solid #a4a4a4;
  border-radius: 16px;
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

</style>

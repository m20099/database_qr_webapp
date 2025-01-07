<template>
  <v-container class="narrow-container">
    <v-row justify="center" class="pa-0">
      <v-col cols="12" class="text-center">
        <h1>Receipt Simulator</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card outlined class="pa-4 mb-6">
          <v-tabs v-model="tab" align-tabs="center" class="tab-btn-group">
            <v-tab :value="1">Item</v-tab>
            <v-tab :value="2">Store</v-tab>
          </v-tabs>

          <v-tabs-window v-model="tab">
            <v-tabs-window-item :value="1">
              <v-card-text>
                <v-form @submit.prevent="submitForm">
                  <v-text-field v-model="item_name" label="商品名" outlined required></v-text-field>
                  <v-text-field v-model.number="price" label="金額" type="number" outlined required></v-text-field>
                  <v-row class="d-flex align-center">
                    <v-col cols="6">
                      <v-btn class="btn-group" type="submit" block>
                        Register
                      </v-btn>
                    </v-col>
                    <v-col cols="6">
                      <v-btn class="btn-group" @click="importCSV" :disabled="!csvFile" block>
                        IMPORT
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
                <v-divider class="my-4"></v-divider>
                <v-file-input v-model="csvFile" label="CSVファイルをインポート" accept=".csv" outlined dense></v-file-input>
              </v-card-text>
            </v-tabs-window-item>

            <v-tabs-window-item :value="2">
              <v-card-text>
                <v-form @submit.prevent="submitStoreForm">
                  <v-text-field v-model="store_name" label="店舗名" outlined required></v-text-field>
                  <v-text-field disabled style="opacity: 0;"></v-text-field>
                  <v-row class="d-flex align-center">
                    <v-col cols="6">
                      <v-btn class="btn-group" type="submit" block>
                        Register
                      </v-btn>
                    </v-col>
                    <v-col cols="6">
                      <v-btn class="btn-group" @click="importStoreCSV" :disabled="!storeCSVFile" block>
                        IMPORT
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
                <v-divider class="my-4"></v-divider>
                <v-file-input v-model="storeCSVFile" label="店舗CSVファイルをインポート" accept=".csv" outlined dense></v-file-input>
              </v-card-text>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card>

        <v-card outlined class="pa-4 mb-6" style="height: 500px">
          <v-tabs v-model="listTab" align-tabs="center" class="tab-btn-group">
            <v-tab :value="1">Item List</v-tab>
            <v-tab :value="2">Store List</v-tab>
          </v-tabs>

          <v-tabs-window v-model="listTab">
            <v-tabs-window-item :value="1">
              <v-card-title class="d-flex justify-space-between align-center">
                <span class="text-center">商品一覧</span>
                <v-btn icon class="btn-group" @click="fetchItems">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </v-card-title>
              <v-card-text style="max-height: 300px; overflow-y: auto;">
                <v-list v-if="items.length">
                  <v-list-item v-for="item in items" :key="item.id" class="mb-2">
                    <template v-slot:prepend>
                      <v-avatar size="40" :style="{ border: '1px solid #135389' }">
                        <v-icon color="#135389" size="24">mdi-cube</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-content>
                      <v-list-item-title class="text-h6">{{ item.item_name }}</v-list-item-title>
                      <v-list-item-subtitle class="text-body-2 text-gray">
                        価格: ¥{{ item.price.toLocaleString() }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                    <template v-slot:append>
                      <v-btn icon @click="deleteItem(item.id)" elevation="0">
                        <v-icon color="red">mdi-delete</v-icon>
                      </v-btn>
                    </template>
                  </v-list-item>
                </v-list>
                <v-alert v-else type="info" color="blue lighten-3" border="left" border-color="blue">
                  登録された商品がありません。
                </v-alert>
              </v-card-text>
            </v-tabs-window-item>

            <v-tabs-window-item :value="2">
              <v-card-title class="d-flex justify-space-between align-center">
                <span class="text-center">店舗一覧</span>
                <v-btn icon class="btn-group" @click="fetchStores">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </v-card-title>
              <v-card-text style="max-height: 300px; overflow-y: auto;">
                <v-list v-if="stores.length">
                  <v-list-item v-for="store in stores" :key="store.id" class="mb-2">
                    <template v-slot:prepend>
                      <v-avatar size="40" :style="{ border: '1px solid #135389' }">
                        <v-icon color="#135389" size="24">mdi-store</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-content>
                      <v-list-item-title class="text-h6">{{ store.store_name }}</v-list-item-title>
                    </v-list-item-content>
                    <template v-slot:append>
                      <v-btn icon @click="deleteStore(store.id)" elevation="0">
                        <v-icon color="red">mdi-delete</v-icon>
                      </v-btn>
                    </template>
                  </v-list-item>
                </v-list>
                <v-alert v-else type="info" color="blue lighten-3" border="left" border-color="blue">
                  登録された店舗がありません。
                </v-alert>
              </v-card-text>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card outlined class="pa-4 mb-6">
          <v-card-title class="text-center">QR Code Generator</v-card-title>
          <v-card-text class="text-body-1">
            <v-row class="pa-0" justify="space-between">
              <v-col cols="4">
                <v-text-field v-model.number="itemCount" label="商品数" type="number" min="1" outlined dense required></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-text-field v-model.number="minQuantity" label="最小数量" type="number" min="1" outlined dense required></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-text-field v-model.number="maxQuantity" label="最大数量" type="number" :min="minQuantity" outlined dense required></v-text-field>
              </v-col>
            </v-row>

            <v-radio-group v-model="useCurrentTime" inline color="#135389">
              <v-radio label="Current Time" :value="true"></v-radio>
              <v-radio label="Custom Date" :value="false" style="padding-left:15px"></v-radio>
            </v-radio-group>
            <v-text-field v-model="manualDate" label="購入日時 (YYYY-MM-DD HH:mm)" outlined dense :disabled="useCurrentTime"></v-text-field>

            <v-btn class="btn-group" @click="generateQRCode" block>GENERATE</v-btn>
          <div v-if="qrCodeData" class="text-center mt-4">
            <p><strong>Result</strong></p>
            <img :src="qrCodeData" alt="QR Code" />
          </div>
          <div v-else-if="qrCodeData === null">
            <p class="text-center text-error">QRコードが生成されませんでした。</p>
          </div>

          <v-alert v-if="selectedItems" type="info" class="mt-4" color="#135389">
            <div>
              <p>ストアID: {{ selectedItems[0] }}</p>
              <p>購入日時: {{ selectedItems[1] }}</p>
              <div v-for="(item, index) in selectedItems[2]" :key="index">
                <p>商品名: {{ item[0] }} 単価: {{ item[1] }} 量: {{ item[2] }}</p>
              </div>
            </div>
          </v-alert>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
  <v-dialog v-model="showDialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5">インポート確認</v-card-title>
      <v-card-text>
        <v-list dense>
          <v-list-item v-for="(item, index) in importedItems" :key="index">
            <v-list-item-content>
              商品名: {{ item.item_name }} / 金額: ¥{{ item.price }}
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="showDialog = false">キャンセル</v-btn>
        <v-btn color="primary" text @click="confirmImport">登録する</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="showStoreDialog" max-width="600px">
    <v-card>
      <v-card-title>店舗インポート確認</v-card-title>
      <v-card-text>
        <p>以下の店舗を登録しますか？</p>
        <v-list dense>
          <v-list-item v-for="(store, index) in importedStores" :key="index">
            <v-list-item-content>
              <v-list-item-title>{{ store.store_name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" text @click="showStoreDialog = false">キャンセル</v-btn>
        <v-btn color="green" text @click="confirmStoreImport">確認</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</v-container>
</template>

<script>
import axios from "axios";
import QRCode from "qrcode";
import pako from "pako";

export default {
  name: 'ReceiptSimulator',
  data() {
    return {
      tab: 1,
      listTab: 1,
      item_name: "",
      price: null,
      items: [],
      csvFile: null,
      showDialog: false,
      importedItems: [],
      qrCodeData: "",
      selectedItem: null,
      store_name: "",
      stores: [],
      storeCSVFile: null,
      importedStores: [],
      showStoreDialog: false,
      itemCount: 1,
      minQuantity: 1,
      maxQuantity: 5,
      useCurrentTime: true,
      manualDate: '',
    };
  },
  methods: {
    async submitForm() {
      if (this.item_name && this.price) {
        const payload = { item_name: this.item_name, price: this.price };
        try {
          const response = await axios.post('http://localhost:5000/api/itemregister', payload);
          if (response.status === 201) {
            alert("商品が正常に登録されました。");
            this.item_name = "";
            this.price = null;
          } else {
            alert("登録に失敗しました。もう一度お試しください。");
          }
        } catch (error) {
          console.error("エラーが発生しました:", error);
          alert(error.response ? `エラー: ${error.response.data.message || "登録に失敗しました。"}` : "ネットワークエラーが発生しました。サーバーを確認してください。");
        }
      } else {
        alert("商品名と金額を入力してください。");
      }
    },

    async importCSV() {
      if (!this.csvFile) return;
      const reader = new FileReader();

      reader.onload = (e) => {
        const csvContent = e.target.result;
        const rows = csvContent.split("\n").filter((row) => row.trim() !== "");
        const items = rows.map((row) => {
          const [item_name, price] = row.split(",");
          return { item_name: item_name.trim(), price: parseFloat(price) };
        });

        this.importedItems = items;
        this.showDialog = true;
      };

      reader.onerror = () => {
        alert("CSVファイルの読み込みに失敗しました。");
      };

      reader.readAsText(this.csvFile);
    },

    async confirmImport() {
      try {
        for (const item of this.importedItems) {
          const payload = { item_name: item.item_name, price: item.price };
          await axios.post("http://localhost:5000/api/itemregister", payload);
        }
        alert("商品が正常に登録されました。");
      } catch (error) {
        console.error("登録中にエラーが発生しました:", error);
        alert("商品登録に失敗しました。");
      } finally {
        this.showDialog = false;
        this.csvFile = null;
      }
    },

    async submitStoreForm() {
      if (this.store_name) {
        const payload = { store_name: this.store_name };
        try {
          const response = await axios.post("http://localhost:5000/api/storeregister", payload);
          if (response.status === 201) {
            alert("店舗が正常に登録されました。");
            this.store_name = ""; 
          } else {
            alert("登録に失敗しました。もう一度お試しください。");
          }
        } catch (error) {
          console.error("エラーが発生しました:", error);
          alert(
            error.response
              ? `エラー: ${error.response.data.message || "登録に失敗しました。"}`
              : "ネットワークエラーが発生しました。サーバーを確認してください。"
          );
        }
      } else {
        alert("店舗名を入力してください。");
      }
    },

    async importStoreCSV() {
    if (!this.storeCSVFile) return;
    const reader = new FileReader();

    reader.onload = (e) => {
        const csvContent = e.target.result;
        const rows = csvContent.split("\n").filter((row) => row.trim() !== "");
        const stores = rows.map((row) => {
        const [store_name] = row.split(",");
        return { store_name: store_name.trim() };
        });

        this.importedStores = stores;
        this.showStoreDialog = true;
    };

    reader.onerror = () => {
        alert("CSVファイルの読み込みに失敗しました。");
    };
        reader.readAsText(this.storeCSVFile);
    },

    async confirmStoreImport() {
    try {
        for (const store of this.importedStores) {
        const payload = { store_name: store.store_name };
        await axios.post("http://localhost:5000/api/storeregister", payload);
        }
        alert("店舗が正常に登録されました。");
    } catch (error) {
        console.error("登録中にエラーが発生しました:", error);
        alert("店舗登録に失敗しました。");
    } finally {
        this.showStoreDialog = false;
        this.storeCSVFile = null;
    }
    },


    async fetchItems() {
      try {
        const response = await axios.get("http://localhost:5000/api/view-items");
        this.items = response.data;
      } catch (error) {
        console.error("商品情報の取得に失敗しました:", error);
      }
    },

    async fetchStores() {
      try {
        const response = await axios.get("http://localhost:5000/api/view-stores");
        this.stores = response.data;
      } catch (error) {
        console.error("店舗情報の取得に失敗しました:", error);
      }
    },

    async generateQRCode() {
      if (!this.items.length) {
        alert("登録された商品がありません。QRコードを生成できません。");
        return;
      }

      if (this.itemCount < 1 || this.minQuantity < 1 || this.maxQuantity < this.minQuantity) {
        alert("商品数は1以上、最小数量と最大数量は適切な範囲を指定してください。");
        return;
      }

        const randomStoreIndex = Math.floor(Math.random() * this.stores.length);
        const randomStore = this.stores[randomStoreIndex];
        const storeId = randomStore.id;
        const selectedItems = [];
        const availableItems = [...this.items];

        let purchaseDate;
        if (this.useCurrentTime) {
            purchaseDate = this.formatDate(new Date());
        } else if (this.manualDate) {
            purchaseDate = this.manualDate;
        } else {
            alert('購入日時を入力してください。');
            return;
        }

        for (let i = 0; i < this.itemCount; i++) {
            if (!availableItems.length) break;
            const randomIndex = Math.floor(Math.random() * availableItems.length);
            const selectedItem = availableItems.splice(randomIndex, 1)[0];
            const randomQuantity = Math.floor(Math.random() * (this.maxQuantity - this.minQuantity + 1)) + this.minQuantity;
            selectedItems.push([selectedItem.item_name, selectedItem.price, randomQuantity]);
        }

      const qrData = [storeId, purchaseDate, selectedItems];

      try {
        const jsonString = JSON.stringify(qrData);
        const compressedData = pako.deflate(jsonString, { level: 7 });
        const base64Data = btoa(String.fromCharCode(...compressedData));

        this.qrCodeData = await QRCode.toDataURL(base64Data, {
          errorCorrectionLevel: 'L',
          width: 200,
          margin: 2,
        });
      } catch (error) {
        console.error('QRコード生成エラー:', error);
        alert("QRコードの生成に失敗しました。");
      }
        console.log("生成されたQRコードデータ:", qrData);
      this.selectedItems = qrData;
    },

    async deleteItem(itemId) {
        if (confirm("この商品を削除しますか？")) {
        try {
            const response = await axios.put(`http://localhost:5000/api/delete-item/${itemId}`);
            if (response.status === 200) {
            alert("商品が削除されました。");
            this.fetchItems();
            }
        } catch (error) {
            console.error("削除中にエラーが発生しました:", error);
            alert("商品を削除できませんでした。");
        }
        }
    },

    async deleteStore(storeId) {
        if (confirm("この店舗を削除しますか？")) {
        try {
            const response = await axios.put(`http://localhost:5000/api/delete-store/${storeId}`);
            if (response.status === 200) {
            alert("店舗が削除されました。");
            this.fetchStores();
            }
        } catch (error) {
            console.error("削除中にエラーが発生しました:", error);
            alert("店舗を削除できませんでした。");
        }
        }
    },

    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
    },

  mounted() {
    this.fetchItems();
    this.fetchStores();
  },
};
</script>

<style scoped>
.narrow-container {
  max-width: 1000px;
  margin: 0 auto;
}

.v-card {
  max-width: 500px;
  margin: auto;
  box-shadow: none !important;
  border: 1.25px solid #a4a4a4;
  border-radius: 16px;
}

.btn-group {
    background-color: #135389;
    color: white;
}

.tab-btn-group {
    color: #135389;
}
</style>
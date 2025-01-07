<template>
  <v-container fluid>
    <v-row no-gutters>
      <!-- 右側カラム: 購入履歴一覧 -->
      <v-col cols="12" md="4" class="history-column">
        <v-card height="100%" class="scrollable-card">
          <v-card-title>購入履歴</v-card-title>
          <v-list dense>
            <v-list-item
              v-for="receipt in sortedReceipts" 
              :key="receipt.id"
              @click="selectReceipt(receipt)"
              :class="{'selected-receipt': selectedReceipt && selectedReceipt.id === receipt.id}"
            >
              <v-list-item-content>
                <v-list-item-title>{{ formatDate(receipt.purchase_date) }}</v-list-item-title>
                <v-list-item-subtitle>{{ receipt.store_name }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- 左側カラム: 詳細表示 -->
      <v-col cols="12" md="8" class="detail-column">
        <v-card height="100%" class="scrollable-card">
          <v-card-title>購入詳細</v-card-title>
          <v-divider></v-divider>
          <div v-if="selectedReceipt" class="receipt-detail">
            <div class="receipt-header">
              <div class="receipt-date">日付: {{ formatDate(selectedReceipt.purchase_date) }}</div>
              <div class="receipt-store">店舗: {{ selectedReceipt.store_name }}</div>
            </div>
            <v-divider></v-divider>
            <v-list>
              <v-list-item v-for="item in selectedReceipt.items" :key="item.id">
                <v-list-item-content>
                  <v-list-item-title>{{ item.item_name }} × {{ item.quantity }}</v-list-item-title>
                  <v-list-item-subtitle>単価: ¥{{ item.price.toLocaleString() }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <div class="receipt-footer">
              <div class="total">合計: ¥{{ calculateTotal(selectedReceipt.items).toLocaleString() }}</div>
            </div>
          </div>
          <v-alert v-else type="info" class="ma-4">
            購入履歴を選択してください。
          </v-alert>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'ReceiptList',
  setup() {
    const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
    const receipts = ref([]);
    const selectedReceipt = ref(null);

    const sortedReceipts = computed(() => {
      return receipts.value.slice().sort((a, b) => new Date(b.purchase_date) - new Date(a.purchase_date));
    });

    const fetchReceipts = async () => {
      const userId = localStorage.getItem('user');
      if (!userId) {
        console.error('ユーザー情報が見つかりません。');
        return;
      }

      try {
        const response = await axios.get(`${API_BASE_URL}/api/receipts`, {
          params: { user_id: userId },
        });

        receipts.value = response.data.map((receipt, index) => ({
          id: index,
          store_name: receipt.store_name,
          purchase_date: receipt.purchase_date,
          items: receipt.items.map((item, idx) => ({
            id: idx,
            item_name: item.item_name,
            price: item.price,
            quantity: item.quantity,
          })),
        }));
      } catch (error) {
        console.error('データ取得中にエラーが発生しました。', error);
      }
    };

    const formatDate = (date) => {
      const d = new Date(date);
      return `${d.getFullYear()}/${('0' + (d.getMonth() + 1)).slice(-2)}/${('0' + d.getDate()).slice(-2)}`;
    };

    const selectReceipt = (receipt) => {
      selectedReceipt.value = receipt;
    };

    const calculateTotal = (items) => {
      return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    };

    onMounted(() => {
      fetchReceipts();
    });

    return {
      receipts,
      selectedReceipt,
      sortedReceipts,
      fetchReceipts,
      formatDate,
      selectReceipt,
      calculateTotal,
    };
  },
};
</script>



<style scoped>
.selected-receipt {
  background-color: #e3f2fd;
  border-left: 4px solid #1976d2;
}

.v-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.v-row {
  flex-grow: 1;
  overflow: hidden;
}

.scrollable-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scrollable-card .v-list {
  overflow-y: auto;
  max-height: calc(100vh - 150px);
}

.history-column {
  max-height: 100%;
  flex: 0 0 35%;
}

.detail-column {
  max-height: 100%;
  flex: 0 0 65%;
}

.receipt-detail {
  padding: 16px;
}

.receipt-header, .receipt-footer {
  padding: 8px 0;
}

.receipt-footer {
  font-weight: bold;
}

@media (max-width: 960px) {
  .history-column {
    flex: 0 0 40%;
  }
  .detail-column {
    flex: 0 0 60%;
  }
}
</style>

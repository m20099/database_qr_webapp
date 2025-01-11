<template>
  <v-container class="user-settings">
    <h1>Settings</h1>

    <v-row justify="center">
      <v-col cols="12" md="8" sm="10">
        <v-card outlined elevation="0">
          <v-list class="mb-4">
            <v-subheader class="subheader">
                <v-icon class="subheader-icon" color="#135389">mdi-account-box</v-icon>
                アカウント設定
            </v-subheader>
            <v-list-item link>
              <div class="d-flex justify-space-between align-center w-100">
                <span>ユーザ名</span>
                <div class="d-flex align-center">
                  <span>{{ userName }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link>
              <div class="d-flex justify-space-between align-center w-100">
                <span>メールアドレス</span>
                <div class="d-flex align-center">
                  <span>{{ userEmail }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link>
              <div class="d-flex justify-space-between align-center w-100">
                <span>パスワード</span>
                <div class="d-flex align-center">
                  <span>●●●●●●●●</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link @click="showLogoutDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span class="text-red">ログアウト</span>
                <v-icon color="red" class="ml-2">mdi-logout</v-icon>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link @click="showDeleteDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span class="text-red">アカウントを削除</span>
                <v-icon color="red" class="ml-2">mdi-delete</v-icon>
              </div>
            </v-list-item>
            <v-divider></v-divider>
          </v-list>

          <v-list class="mb-4">
            <v-subheader class="subheader">
                <v-icon class="subheader-icon" color="#135389">mdi-cash-multiple</v-icon>
                支出管理設定
            </v-subheader>
            <v-list-item link>
              <div class="d-flex justify-space-between align-center w-100">
                <span>1日あたりの支出上限</span>
                <div class="d-flex align-center">
                  <span>{{ currentMaxValue }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link>
              <div class="d-flex justify-space-between align-center w-100">
                <span>月間支出上限</span>
                <div class="d-flex align-center">
                  <span></span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
          </v-list>
          <v-list>
            <v-subheader class="subheader">
                <v-icon class="subheader-icon" color="#135389">mdi-palette</v-icon>
                表示設定
            </v-subheader>
            <v-list-item link>
              <div class="d-flex justify-space-between align-center w-100">
                <span>ダークテーマ</span>
                <div class="d-flex align-center">
                  <span></span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showLogoutDialog" max-width="400">
      <v-card class="pa-2">
        <v-card-title class="d-flex align-center">
          <v-icon color="red" style="padding-right:12px">mdi-logout</v-icon>
          <span class="font-weight-bold">LOG OUT</span>
        </v-card-title>
        <v-card-text>
          ログアウトしますか？
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text class="font-weight-bold" @click="showLogoutDialog = false">Cancel</v-btn>
          <v-btn color="red" text class="font-weight-bold" @click="handleLogout">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card class="pa-2">
        <v-card-title class="d-flex align-center">
          <v-icon color="red" style="padding-right:12px">mdi-delete</v-icon>
          <span class="text-red font-weight-bold">DELETE ACCOUNT</span>
        </v-card-title>
        <v-card-text>
          アカウントを削除すると復元できません。<br />本当に削除しますか？
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text class="font-weight-bold" @click="showDeleteDialog = false">CANCEL</v-btn>
          <v-btn color="red" text class="font-weight-bold" @click="showSecondDeleteDialog = true; showDeleteDialog = false; deleteClickCount = 0">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showSecondDeleteDialog" max-width="400">
        <v-card class="pa-2">
            <v-card-title class="d-flex align-center">
                <v-icon color="red" style="padding-right:12px">mdi-alert</v-icon>
                <span class="text-red font-weight-bold">CONFIRM DELETE</span>
            </v-card-title>
                <v-card-text>
                    本当にアカウントを削除しますか？<br />この操作は取り消せません。
                          <br /><br />
                <span v-if="deleteClickCount < 5">
                    削除を確定するには、<br />あと <strong>{{ 5 - deleteClickCount }}</strong> 回クリックしてください。
                </span>
                </v-card-text>
            <v-card-actions class="justify-end">
            <v-btn text class="font-weight-bold" @click="showSecondDeleteDialog = false; deleteClickCount = 0">CANCEL</v-btn>
      <v-btn 
        :disabled="deleteClickCount >= 5" 
        color="red" 
        text 
        class="font-weight-bold" 
        @click="handleDeleteClick">
        {{ deleteClickCount < 5 ? `DELETE (${5 - deleteClickCount})` : 'DELETING...' }}
      </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

  </v-container>
</template>



<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
    name: "UserSettings",
    setup() {
        const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;

        const userName = ref("");
        const userEmail = ref("");
        const userCreatedAt = ref("");
        const userMaxValue = ref(null);
        const currentMaxValue = ref(0);
        const userId = JSON.parse(localStorage.getItem("user"));

        const activeTab = ref(1);

        const showLogoutDialog = ref(false);
        const showDeleteDialog = ref(false);
        const showSecondDeleteDialog = ref(false);
        const deleteClickCount = ref(0);

        const fetchUserSettings = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/api/setting/${userId}`);
                if (response.status === 200) {
                    const data = response.data;

                    userName.value = data.username;
                    userEmail.value = data.email;
                    userCreatedAt.value = data.created_at;
                    userMaxValue.value = data.budget_limit || null;
                    currentMaxValue.value = data.budget_limit || 10000;
                }
            } catch (error) {
                console.error("設定取得エラー：", error);
            }
        };

        const handleLogout = () => {
            localStorage.removeItem("token");
            localStorage.removeItem("tokenExpiry");
            localStorage.removeItem("user");
            alert("ログアウトしました！");
            window.location.reload();
        };

        const deleteAccount = async () => {
            try {
                await axios.delete(`${API_BASE_URL}/api/user/${userId}`);
                localStorage.clear();
                alert("アカウントを削除しました。");
                window.location.reload();
            } catch (error) {
                console.error("アカウント削除エラー:", error);
                alert("アカウントの削除に失敗しました。");
            }
        };

        const handleDeleteClick = async () => {
            if (deleteClickCount.value < 4) {
                deleteClickCount.value++;
            } else {
                deleteClickCount.value++;
                await deleteAccount();
            }
        };

        onMounted(() => {
            fetchUserSettings();
        });

        return {
            userName,
            userEmail,
            userCreatedAt,
            userMaxValue,
            currentMaxValue,
            activeTab,
            handleLogout,
            showLogoutDialog,
            deleteAccount,
            showDeleteDialog,
            showSecondDeleteDialog,
            deleteClickCount,
            handleDeleteClick,
        };
    },
}
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.subheader {
  margin-top: 16px;
  margin-bottom: 8px;
  font-size: 1.0rem;
  font-weight: bold;
  color: #000000;
}
.subheader-icon {
  margin-bottom: 2px;
  margin-right: 5px;
  font-size: 1.5rem;
}
</style>
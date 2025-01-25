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
            <v-list-item link @click="showEditNameDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span>ユーザ名</span>
                <div class="d-flex align-center">
                  <span>{{ userName }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link @click="showEditEmailDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span>メールアドレス</span>
                <div class="d-flex align-center">
                  <span>{{ userEmail }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link @click="showEditPasswordDialog = true">
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
            <v-list-item link @click="showEditDayMaxDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span>1日あたりの支出上限</span>
                <div class="d-flex align-center">
                  <span>{{ currentDayMaxValue }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link @click="showEditMonthMaxDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span>月間支出上限</span>
                <div class="d-flex align-center">
                  <span>{{ currentMonthMaxValue }}</span>
                  <v-icon color="grey" class="ml-2">mdi-chevron-right</v-icon>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item link @click="showResetDialog = true">
              <div class="d-flex justify-space-between align-center w-100">
                <span class="text-red">初期設定に戻す</span>
                <v-icon color="red" class="ml-2">mdi-restore</v-icon>
              </div>
            </v-list-item>
            <v-divider></v-divider>
          </v-list>

          <!-- <v-list>
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

          </v-list> -->
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showLogoutDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title class="d-flex align-center">
          <v-icon color="red" class="dialog-icon">mdi-logout</v-icon>
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
      <v-card class="pa-3">
        <v-card-title class="d-flex align-center">
          <v-icon color="red" class="dialog-icon">mdi-delete</v-icon>
          <span class="text-red font-weight-bold">DELETE ACCOUNT</span>
        </v-card-title>
        <v-card-text>
          アカウントを削除しますか？
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text class="font-weight-bold" @click="showDeleteDialog = false">CANCEL</v-btn>
          <v-btn color="red" text class="font-weight-bold" @click="showSecondDeleteDialog = true; showDeleteDialog = false; deleteClickCount = 0">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showSecondDeleteDialog" max-width="400">
        <v-card class="pa-3">
            <v-card-title class="d-flex align-center">
                <v-icon color="red" class="dialog-icon">mdi-alert</v-icon>
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

    <v-dialog v-model="showEditNameDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title>
          <v-icon color="#135389" class="dialog-icon">mdi-account-edit</v-icon>
          ユーザ名を変更
        </v-card-title>
        <v-card-text>
          <v-text-field label="New UserName" v-model="newUserName" outlined dense required hint="6〜30文字の半角英数字のみ使用可能" :error-messages="errors.username" @input="clearError('username')"/>
        </v-card-text>
        <v-card-actions>
          <v-btn text class="font-weight-bold" @click="resetDialog('username'); showEditNameDialog = false">CANCEL</v-btn>
          <v-btn color="#135389" text class="font-weight-bold" @click="handleSaveUserName">SAVE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showEditEmailDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title>
          <v-icon color="#135389" class="dialog-icon">mdi-email-edit</v-icon>
          メールアドレスを変更
        </v-card-title>
        <v-card-text>
          <v-text-field label="New Email" v-model="newUserEmail" outlined dense required :error-messages="errors.email" @input="clearError('email')"/>
        </v-card-text>
        <v-card-actions>
          <v-btn text class="font-weight-bold" @click="resetDialog('email'); showEditEmailDialog = false">CANCEL</v-btn>
          <v-btn color="#135389" text class="font-weight-bold" @click="handleSaveUserEmail">SAVE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showEditPasswordDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title>
          <v-icon color="#135389" class="dialog-icon">mdi-lock-reset</v-icon>
          パスワードを変更
        </v-card-title>
        <v-card-text>
          <v-text-field label="Current Password" v-model="currentPassword" :type="showCurrentPassword ? 'text' : 'password'" outlined dense required :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'" @click:append-inner="toggleCurrentPasswordVisibility" :error-messages="errors.currentPassword" @input="clearError('currentPassword')"/>
          <v-text-field label="New Password" v-model="newPassword" :type="showNewPassword ? 'text' : 'password'" outlined dense required :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'" @click:append-inner="toggleNewPasswordVisibility" hint="8文字以上の半角英数字,(- .)のみ使用可能" :error-messages="errors.newPassword" @input="clearError('newPassword')"/>
          <v-text-field label="Retype New Password" v-model="confirmNewPassword" :type="showConfirmPassword ? 'text' : 'password'" outlined dense required :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'" @click:append-inner="toggleConfirmPasswordVisibility" :error-messages="errors.confirmNewPassword" @input="clearError('confirmNewPassword')"/>
        </v-card-text>
        <v-card-actions>
          <v-btn text class="font-weight-bold" @click="resetDialog('password'); showEditPasswordDialog = false">CANCEL</v-btn>
          <v-btn color="#135389" text class="font-weight-bold" @click="handleSavePassword">SAVE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showEditDayMaxDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title>
          <v-icon color="#135389" class="dialog-icon">mdi-calendar-today</v-icon>
          1日の支出上限を設定
        </v-card-title>
        <v-card-text>
          <v-text-field label="1日の支出上限金額" type="number" v-model="newDailyMax" outlined dense required hint="半角英数字で入力"/>
        </v-card-text>
        <v-card-actions>
          <v-btn text class="font-weight-bold" @click="resetDialog('daymax'); showEditDayMaxDialog = false">CANCEL</v-btn>
          <v-btn color="#135389" text class="font-weight-bold" @click="handleSaveDaylyMax">SAVE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showEditMonthMaxDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title>
          <v-icon color="#135389" class="dialog-icon">mdi-calendar-today</v-icon>
          1ヵ月の支出上限を設定
        </v-card-title>
        <v-card-text>
          <v-text-field label="1ヵ月の支出上限金額" type="number" v-model="newMonthlyMax" outlined dense required hint="半角英数字で入力"/>
        </v-card-text>
        <v-card-actions>
          <v-btn text class="font-weight-bold" @click="resetDialog('monthmax'); showEditMonthMaxDialog = false">CANCEL</v-btn>
          <v-btn color="#135389" text class="font-weight-bold" @click="handleSaveMonthlyMax">SAVE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showResetDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title class="d-flex align-center">
          <v-icon color="red" class="dialog-icon">mdi-restore</v-icon>
          <span class="font-weight-bold">RESET</span>
        </v-card-title>
        <v-card-text>
          支出管理設定を初期設定に<br />戻しますか？
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text class="font-weight-bold" @click="showResetDialog = false">Cancel</v-btn>
          <v-btn color="red" text class="font-weight-bold" @click="handleReset">OK</v-btn>
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
        const userId = JSON.parse(localStorage.getItem("user"));

        const userName = ref("");
        const userEmail = ref("");
        const userCreatedAt = ref("");
        const currentDayMaxValue = ref("");
        const currentMonthMaxValue = ref("");

        const newUserName = ref("");
        const newUserEmail = ref("");
        const currentPassword = ref("");
        const newPassword = ref("");
        const confirmNewPassword = ref("");
        const newDailyMax = ref("");
        const newMonthlyMax = ref("");

        const showCurrentPassword = ref(false);
        const showNewPassword = ref(false);
        const showConfirmPassword = ref(false);

        const showEditNameDialog = ref(false);
        const showEditEmailDialog = ref(false);
        const showEditPasswordDialog = ref(false);
        const showEditDayMaxDialog = ref(false);
        const showEditMonthMaxDialog = ref(false);
        const showResetDialog = ref(false);
        const showLogoutDialog = ref(false);
        const showDeleteDialog = ref(false);
        const showSecondDeleteDialog = ref(false);

        const errors = ref({
            username: '',
            email: '',
            currentPassword: '',
            newPassword: '',
            confirmNewPassword: '',
        });

        const deleteClickCount = ref(0);

        const fetchUserSettings = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/api/setting/${userId}`);
                if (response.status === 200) {
                    const data = response.data;

                    userName.value = data.username;
                    userEmail.value = data.email;
                    userCreatedAt.value = data.created_at;
                    currentDayMaxValue.value = data.daily_spending_limit;
                    currentMonthMaxValue.value = data.monthly_spending_limit;
                }
            } catch (error) {
                console.error("設定取得エラー：", error);
            }
        };

        const validateUserName = () => {
            errors.value.username = '';
            if (!newUserName.value.trim()) {
                errors.value.username = 'ユーザ名を入力してください。';
                return false;
            }
            if (!/^[a-zA-Z0-9]{6,15}$/.test(newUserName.value)) {
                errors.value.username = '6〜15文字の半角英数字のみ使用可能です。';
                return false;
            }
            return true;
        };

        const validateEmail = () => {
            errors.value.email = '';
            if (!newUserEmail.value.trim()) {
                errors.value.email = 'メールアドレスを入力してください。';
                console.log(errors.value.email);
                return false;
            } else if (!newUserEmail.value.includes('@')) {
                errors.value.email = '有効なメールアドレスを入力してください。';
                console.log(errors.value.email);
                return false;
            }
            return true;
        };

        const validatePassword = () => {
            let isValid = true;
            errors.value.currentPassword = '';
            errors.value.newPassword = '';
            errors.value.confirmNewPassword = '';

            if (!currentPassword.value.trim()) {
                errors.value.currentPassword = '現在のパスワードを入力してください。';
                isValid = false;
            }

            if (!newPassword.value.trim()) {
                errors.value.newPassword = '新しいパスワードを入力してください。';
                isValid = false;
            }
            if (!/^[a-zA-Z0-9\-.]{8,}$/.test(newPassword.value)) {
                errors.value.newPassword = '8文字以上の半角英数字,(- .)のみ使用可能です。';
                isValid = false;
            }

            if (!confirmNewPassword.value.trim()) {
                errors.value.confirmNewPassword = '新しいパスワードを再入力してください。';
                isValid = false;
            }else if (newPassword.value !== confirmNewPassword.value) {
                errors.value.confirmNewPassword = 'パスワードが一致しません。';
                isValid = false;
            }

            return isValid;
        };

        const clearError = (field) => {
            if (errors.value[field]) {
                errors.value[field] = '';
            }
        };

        const resetDialog = (dialogName) => {
            switch (dialogName) {
                case 'password':
                    currentPassword.value = '';
                    newPassword.value = '';
                    confirmNewPassword.value = '';
                    errors.value.currentPassword = '';
                    errors.value.newPassword = '';
                    errors.value.confirmNewPassword = '';
                    break;
                case 'email':
                    newUserEmail.value = '';
                    errors.value.email = '';
                    break;
                case 'username':
                    newUserName.value = '';
                    errors.value.username = '';
                    break;
                case 'daymax':
                    newDailyMax.value = '';
                    break;
                case 'monthmax':
                    newMonthlyMax.value = '';
                    break;
            }
        };

        const handleSaveUserName = async () => {
            if (!validateUserName()) {
                return;
            }
            try {
                const response = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'username',
                    value: newUserName.value,
                });
                if (response.status === 200) {
                    userName.value = newUserName.value;
                    showEditNameDialog.value = false;
                    alert('ユーザー名を変更しました！');
                    resetDialog('username');
                }
            } catch (error) {
                if (error.response) {
                    console.log('エラーレスポンス:', error.response);

                    const responseErrors = error.response.data.errors || {};
                    if (responseErrors.username) {
                        errors.value.username = responseErrors.username;
                    }
                }
            }
        };

        const handleSaveUserEmail = async () => {
            if (!validateEmail()) {
                return;
            }
            try {
                const response = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'email',
                    value: newUserEmail.value,
                });
                if (response.status === 200){
                    userEmail.value = newUserEmail.value;
                    showEditEmailDialog.value = false;
                    alert('メールアドレスを変更しました！');
                    resetDialog('email');
                }
            } catch (error) {
                if (error.response) {
                    console.log('エラーレスポンス:', error.response);

                    const responseErrors = error.response.data.errors || {};
                    if (responseErrors.email) {
                        errors.value.email = responseErrors.email;
                    }
                }
            }
        };

        const handleSavePassword = async () => {
            if (!validatePassword()) {
                return;
            }
            try {
                const response = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'password',
                    value: newPassword.value,
                    current_password: currentPassword.value,
                });
                if (response.status === 200){
                    showEditPasswordDialog.value = false;
                    alert('パスワードを変更しました');
                    resetDialog('password');
                }
            } catch (error) {
                if (error.response) {
                    console.log('エラーレスポンス:', error.response);

                    const responseErrors = error.response.data.errors || {};
                    if (responseErrors.password) {
                        errors.value.currentPassword = responseErrors.password;
                    }
                }
            }
        };

        const handleSaveDaylyMax = async () => {
            try {
                const response = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'daymax',
                    value: newDailyMax.value,
                });
                if (response.status === 200){
                    currentDayMaxValue.value = newDailyMax.value;
                    showEditDayMaxDialog.value = false;
                    alert('1日の支出上限を変更しました');
                    resetDialog('daymax');
                }
            } catch (error) {
                if (error.response) {
                    console.log('エラーレスポンス:', error.response);
                }
            }
        };

        const handleSaveMonthlyMax = async () => {
            try {
                const response = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'monthmax',
                    value: newMonthlyMax.value,
                });
                if (response.status === 200){
                    currentMonthMaxValue.value = newMonthlyMax.value;
                    showEditMonthMaxDialog.value = false;
                    alert('1ヵ月の支出上限を変更しました');
                    resetDialog('monthmax');
                }
            } catch (error) {
                if (error.response) {
                    console.log('エラーレスポンス:', error.response);
                }
            } finally {
                showResetDialog.value = false;
            }
        };
        
        const handleReset = async () => {
            try {
                const dayResponse = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'daymax',
                    value: 1000,
                });
                const monthResponse = await axios.put(`${API_BASE_URL}/api/setting`,{
                    user_id: userId,
                    field: 'monthmax',
                    value: 30000,
                });
                if (dayResponse.status === 200 && monthResponse.status === 200) {
                    fetchUserSettings();
                    showResetDialog.value = false;
                    alert('規定値にリセットしました');
                }
            } catch (error) {
                if (error.response) {
                    console.log('エラーレスポンス:', error.response);
                }
            }
        };

        const toggleCurrentPasswordVisibility = () => {
            showCurrentPassword.value = !showCurrentPassword.value;
        };

        const toggleNewPasswordVisibility = () => {
            showNewPassword.value = !showNewPassword.value;
        };

        const toggleConfirmPasswordVisibility = () => {
            showConfirmPassword.value = !showConfirmPassword.value;
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
            // ユーザ設定情報
            userName,
            userEmail,
            userCreatedAt,
            currentDayMaxValue,
            currentMonthMaxValue,
            
            // 設定変更用変数
            newUserName,
            newUserEmail,
            newPassword,
            confirmNewPassword,
            currentPassword,
            newDailyMax,
            newMonthlyMax,

            // パスワード表示
            showCurrentPassword,
            showNewPassword,
            showConfirmPassword,
            toggleCurrentPasswordVisibility,
            toggleNewPasswordVisibility,
            toggleConfirmPasswordVisibility,

            // ダイアログ表示フラグ
            showEditNameDialog,
            showEditEmailDialog,
            showEditPasswordDialog,
            showEditDayMaxDialog,
            showEditMonthMaxDialog,
            showResetDialog,
            showLogoutDialog,
            showDeleteDialog,
            showSecondDeleteDialog,

            // ハンドル関数
            handleSaveUserName,
            handleSaveUserEmail,
            handleSavePassword,
            handleSaveDaylyMax,
            handleSaveMonthlyMax,
            handleReset,
            handleLogout,
            deleteAccount,
            handleDeleteClick,

            // エラー対応
            errors,
            clearError,

            // その他
            deleteClickCount,
            resetDialog,
        };
    },
}
</script>

<style scoped>
h1 {
  text-align: center;
  margin-top: 10px;
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
  margin-bottom: 4px;
  margin-right: 5px;
  font-size: 1.5rem;
}

.dialog-icon {
  margin-bottom: 4px;
  padding-right: 12px;
}
</style>
<template>
  <div class="user-register">
    <h1>Register</h1>
    <v-form @submit.prevent="registerUser">
      <v-text-field
        v-model="username"
        label="Username"
        variant="outlined"
        prepend-icon="mdi-account"
        hint="6〜30文字の半角英数字のみ使用可能"
        :error-messages="errors.username"
        @input="clearError('username')"
      ></v-text-field>

      <v-text-field
        v-model="email"
        label="Email"
        variant="outlined"
        prepend-icon="mdi-email"
        :error-messages="errors.email"
        @input="clearError('email')"
      ></v-text-field>

      <v-text-field
        v-model="password"
        label="Password"
        variant="outlined"
        :type="showPassword ? 'text' : 'password'"
        prepend-icon="mdi-lock"
        hint="8文字以上の半角英数字及び記号(- .)のみ使用可能"
        :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="togglePasswordVisibility"
        :error-messages="errors.password"
        @input="clearError('password')"
      ></v-text-field>

      <v-text-field
        v-model="confirmPassword"
        label="Retype Password"
        variant="outlined"
        :type="showConfirmPassword ? 'text' : 'password'"
        prepend-icon="mdi-lock-check"
        :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="toggleConfirmPasswordVisibility"
        :error-messages="errors.confirmPassword"
        @input="clearError('confirmPassword')"
      ></v-text-field>

      <v-btn color="#135389" type="submit" block class="mt-4">Register</v-btn>
    </v-form>

    <p class="login-link">
      アカウントをお持ちの方は
      <a href="/login">こちら</a>
    </p>

    <transition name="popup">
      <div v-if="showPopup" class="popup-overlay">
        <div class="popup-card">
          <h2> 登録成功 </h2>
          <p>アカウントが作成されました。</p>
          <p>ログインページへ移動します。</p>
          <v-btn color="primary" @click="redirectToLogin">OK</v-btn>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'UserRegister',
  setup() {
    const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const errors = ref({});
    const success = ref(false);
    const showPopup = ref(false);
    const router = useRouter();
    const showPassword = ref(false);
    const showConfirmPassword = ref(false);

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    const toggleConfirmPasswordVisibility = () => {
      showConfirmPassword.value = !showConfirmPassword.value;
    };

    const validateFields = () => {
      errors.value = {};
      if (!username.value.trim()) {
        errors.value.username = 'ユーザ名を入力してください。';
      } else if (!/^[a-zA-Z0-9]{6,15}$/.test(username.value)) {
        errors.value.username =
          '6~15文字の半角英数字のみ使用可能です。';
      }

      if (!email.value.trim()) {
        errors.value.email = 'メールアドレスを入力してください。';
      } else if (!email.value.includes('@')) {
        errors.value.email = '有効なメールアドレスを入力してください。';
      }

      if (!password.value.trim()) {
        errors.value.password = 'パスワードを入力してください。';
      } else if (password.value.length < 8) {
        errors.value.password = 'パスワードは8文字以上である必要があります。';
      } else if (!/^[a-zA-Z0-9\-.]{8,}$/.test(password.value)) {
        errors.value.password = '半角英数字と記号(-.)のみ使用可能です。';
      }


      if (!confirmPassword.value.trim()) {
        errors.value.confirmPassword = 'パスワードを再入力してください。';
      } else if (password.value !== confirmPassword.value) {
        errors.value.confirmPassword = 'パスワードが一致しません。';
      }

      return Object.keys(errors.value).length === 0;
    };

    const clearError = (field) => {
      if (errors.value[field]) {
        errors.value[field] = '';
      }
    };

    const registerUser = async () => {
      if (!validateFields()) {
        return;
      }
      try {
        const response = await axios.post(`${API_BASE_URL}/api/register`, {
          username: username.value,
          email: email.value,
          password: password.value,
        });
        if (response.status === 201) {
          success.value = true;
          username.value = '';
          email.value = '';
          password.value = '';
          confirmPassword.value = '';
          errors.value = {};

          showPopup.value = true;
        }
      } catch (err) {
        if (err.response) {
            console.log('エラーレスポンス:', err.response);

          if (err.response.status === 409) {
            if (err.response.data.errors.username) {
              errors.value.username = 'このユーザ名は既に使用されています。';
            }
            if (err.response.data.errors.email) {
              errors.value.email = 'このメールアドレスは既に使用されています。';
            }
          } else {
            errors.value.form = '登録に失敗しました。もう一度お試しください。';
          }
        } else {
          errors.value.form = 'サーバーエラーが発生しました。';
        }
      }
    };

    const redirectToLogin = () => {
      showPopup.value = false;
      router.push('/login');
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      errors,
      success,
      showPopup,
      showPassword,
      showConfirmPassword,
      togglePasswordVisibility,
      toggleConfirmPasswordVisibility,
      registerUser,
      clearError,
      redirectToLogin,
    };
  },
};
</script>


<style scoped>
.user-register {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-sizing: border-box;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.v-text-field {
  margin-bottom: 12px;
}


.error-text {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

.login-link {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

.login-link a {
  color: #135389;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.login-link a:hover {
  color: #1d7ed1;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 透明感のある背景 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup-card {
  background-color: white; /* モーダルの背景色 */
  padding: 30px 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  max-width: 350px;
  width: 90%;
  animation: slide-down 0.3s ease-out; /* アニメーション */
}

.popup-card h2 {
  color: #135389; /* 成功を表す明るい緑 */
  margin-bottom: 10px;
}

.popup-card p {
  color: #333;
  margin-bottom: 20px;
}

.popup-card button {
  background-color: #135389;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.popup-card button:hover {
  background-color: #1d7ed1;
}

/* スライドインアニメーション */
@keyframes slide-down {
  from {
    transform: translateY(-20%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.popup-enter-active,
.popup-leave-active {
  transition: opacity 0.5s;
}

.popup-enter-from,
.popup-leave-to {
  opacity: 0;
}
</style>

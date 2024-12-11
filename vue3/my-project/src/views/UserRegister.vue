<template>
  <div class="user-register">
    <h1>Register</h1>
    <form @submit.prevent="registerUser">
      <div class="form-group" :class="{ 'error-group': errors.username }">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          @input="clearError('username')"
          placeholder="ユーザ名を入力"
        />
        <p v-if="errors.username" class="error-text">{{ errors.username }}</p>
      </div>
      <div class="form-group" :class="{ 'error-group': errors.email }">
        <label for="email">Email</label>
        <input
          type="text"
          id="email"
          v-model="email"
          @input="clearError('email')"
          placeholder="メールアドレスを入力"
        />
        <p v-if="errors.email" class="error-text">{{ errors.email }}</p>
      </div>
      <div class="form-group" :class="{ 'error-group': errors.password }">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          @input="clearError('password')"
          placeholder="パスワードを入力"
        />
        <p v-if="errors.password" class="error-text">{{ errors.password }}</p>
      </div>
      <div class="form-group" :class="{ 'error-group': errors.confirmPassword }">
        <label for="confirm-password">Retype Password</label>
        <input
            type="password"
            id="confirm-password"
            v-model="confirmPassword"
            @input="clearError('confirmPassword')"
            placeholder="パスワードを再入力"
        />
        <p v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</p>
      </div>
      <button type="submit" class="submit-button">Register</button>
    </form>

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
          <button @click="redirectToLogin">OK</button>
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
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const errors = ref({});
    const success = ref(false);
    const showPopup = ref(false);
    const router = useRouter();

    const validateFields = () => {
      errors.value = {};
        // ユーザ名の検証
        if (!username.value.trim()) {
            errors.value.username = 'ユーザ名を入力してください。';
        } else if (!/^[a-zA-Z0-9]{6,30}$/.test(username.value)) {
            errors.value.username =
            'ユーザ名は6〜30文字の半角英数字のみ使用可能です。';
        }

        // メールアドレスの検証
        if (!email.value.trim()) {
            errors.value.email = 'メールアドレスを入力してください。';
        } else if (!email.value.includes('@')) {
            errors.value.email = '有効なメールアドレスを入力してください。';
        }

        // パスワードの検証
        if (!password.value.trim()) {
            errors.value.password = 'パスワードを入力してください。';
        } else if (password.value.length < 8) {
            errors.value.password = 'パスワードは8文字以上である必要があります。';
        }

        // パスワード再入力の検証
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
        const response = await axios.post('http://localhost:5000/api/register', {
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
        // サーバからのエラーを処理
        if (err.response.status === 409) {
            if (err.response.data.message.includes('ユーザ名')) {
            errors.value.username = 'このユーザ名は既に使用されています。';
            } else if (err.response.data.message.includes('メールアドレス')) {
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
      showPopup.value = false;  // ポップアップを非表示にする
      router.push('/login');     // ログインページへリダイレクト
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      errors,
      success,
      showPopup,
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

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
  color: #333;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus {
  border-color: #449deb;
  outline: none;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

.error-group input {
  border-color: #e74c3c;
}

.error-text {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

/* ボタン */
.submit-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #135389;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #1d7ed1;
}

.error-message,
.success-message {
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
  font-size: 14px;
}

.error-message {
  color: #e74c3c;
}

.success-message {
  color: #27ae60;
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

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  font-size: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.popup button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

.popup button:hover {
  background-color: #45a049;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
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

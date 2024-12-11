<template>
  <div class="login-form">
    <h1>Log In</h1>
    <form @submit.prevent="handleLogin">
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
      <div class="form-group">
        <button type="submit">Log In</button>
      </div>
    </form>

    <p class="signup-link">
      新規登録は 
      <a href="/userregister">こちら</a>
    </p>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'UserLogin',
  setup() {
    const username = ref('');
    const password = ref('');
    const errors = ref({});
    const error = ref('');
    const success = ref(false);
    const router = useRouter();

    const validateFields = () => {
      errors.value = {};
      if (!username.value.trim()) {
        errors.value.username = 'ユーザ名を入力してください。';
      }
      if (!password.value.trim()) {
        errors.value.password = 'パスワードを入力してください。';
      }
      return Object.keys(errors.value).length === 0;
    };

    const clearError = (field) => {
      if (errors.value[field]) {
        errors.value[field] = '';
      }
    };

    const handleLogin = async () => {
      if (!validateFields()) {
        return;
      }
      try {
        const response = await axios.post('http://localhost:5000/api/login', {
          username: username.value,
          password: password.value,
        });

        if (response.status === 200) {
          const { token, user } = response.data;
          const expiry = Date.now() + 3600000;
          localStorage.setItem('token', token);
          localStorage.setItem('tokenExpiry', expiry);
          localStorage.setItem('user', JSON.stringify(user));
          window.location.href = '/userhome';
        }
      } catch (err) {
        error.value = 'ログインに失敗しました。ユーザー名またはパスワードが正しくありません。';
        success.value = false;
      }
    };

    onMounted(() => {
      if (localStorage.getItem('token')) {
        router.push('/userhome');
      }
    });

    return {
      username,
      password,
      errors,
      error,
      success,
      handleLogin,
      clearError,
    };
  },
};
</script>

<style scoped>
.login-form {
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

button {
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

button:hover {
  background-color: #1d7ed1;
}

.error {
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
  font-size: 14px;
  color: #e74c3c;
}

.success {
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
  font-size: 14px;
  color: #27ae60;
}

.signup-link {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

.signup-link a {
  color: #135389;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.signup-link a:hover {
  color: #1d7ed1;
}
</style>

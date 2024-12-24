<template>
  <div class="login-form">
    <h1>Log In</h1>
    <v-form @submit.prevent="handleLogin">
      <v-text-field
        v-model="username"
        label="Username"
        variant="outlined"
        prepend-icon="mdi-account"
        :error-messages="errors.username"
        @input="clearError('username')"
      ></v-text-field>

      <v-text-field
        v-model="password"
        label="Password"
        variant="outlined"
        type="password"
        prepend-icon="mdi-lock"
        :error-messages="errors.password"
        @input="clearError('password')"
      ></v-text-field>

      <v-btn color="#135389" type="submit" block class="mt-4">Log In</v-btn>
    </v-form>

    <p class="signup-link">
      新規登録は 
      <a href="/signup">こちら</a>
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
      if (!validateFields()) return;

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
          window.location.reload();
        }
      } catch (err) {
        error.value = 'ログインに失敗しました。ユーザー名またはパスワードが正しくありません。';
      }
    };

    onMounted(() => {
      if (localStorage.getItem('token')) {
        router.push('/mypage');
      }
    });

    return {
      username,
      password,
      errors,
      error,
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

.error {
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
  font-size: 14px;
  color: #e74c3c;
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

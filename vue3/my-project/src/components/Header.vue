<template>
  <header class="header">
    <div class="header-content">
      <div class="logo">
        <img src="@/assets/logo.png" alt="App Logo" />
        <h1 class="title">QR Shop Log Demo</h1>
      </div>
      <nav class="nav-links">
        <router-link to="/" class="nav-link">HOME</router-link>
        <router-link v-if="!isLoggedIn" to="/login" class="nav-link">LOG IN</router-link>
        <router-link v-if="!isLoggedIn" to="/userregister" class="nav-link">REGISTER</router-link>
        <router-link v-if="isLoggedIn" to="/userhome" class="nav-link">MY PAGE</router-link>
        <router-link v-if="isLoggedIn" to="/login" class="nav-link" @click.prevent="handleLogout">LOG OUT</router-link>
      </nav>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: "Header-main",
  setup() {
    const router = useRouter();
    const isLoggedIn = ref(!!localStorage.getItem("token")); // ログイン状態を判定

    const handleLogout = () => {
      localStorage.removeItem("token");
      isLoggedIn.value = false;
      router.push("/login");
    };

    return {
      isLoggedIn,
      handleLogout,
    };
  },
};
</script>

<style scoped>
.header {
  width: 100%;
  max-width: 100vw;
  padding: 15px 30px;
  background: linear-gradient(90deg, #0b3a63, #135389, #0b3a63);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: #cce7ff;
}
</style>

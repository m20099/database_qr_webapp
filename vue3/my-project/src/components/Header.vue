<template>
  <v-app-bar app :style="{ background: 'linear-gradient(90deg, #0b3a63, #135389, #0b3a63)' }" dark elevation="0">
    <v-container>
      <v-row align="center" justify="space-between" no-gutters>
        <v-col cols="auto" class="d-flex align-center">
            <v-icon color="#ffffff" class="logo-img">mdi-qrcode</v-icon>
          <h1 class="title">QR Shop Log Demo</h1>
        </v-col>

        <v-col cols="auto" v-show="!isMobile" class="d-none d-md-flex">
          <v-btn to="/" text class="nav-link d-flex flex-column align-center">
            <v-icon size="24">mdi-home</v-icon>
            <span class="nav-label">HOME</span>
          </v-btn>
          <template v-if="!isLoggedIn">
            <v-btn to="/login" text class="nav-link d-flex flex-column align-center">
              <v-icon size="24">mdi-login</v-icon>
              <span class="nav-label">LOG IN</span>
            </v-btn>
            <v-btn to="/signup" text class="nav-link d-flex flex-column align-center">
              <v-icon size="24">mdi-account-plus</v-icon>
              <span class="nav-label">REGISTER</span>
            </v-btn>
          </template>
          <template v-else>
            <v-btn to="/mypage" text class="nav-link d-flex flex-column align-center">
              <v-icon size="24">mdi-account</v-icon>
              <span class="nav-label">MY PAGE</span>
            </v-btn>
            <v-btn text class="nav-link d-flex flex-column align-center" @click="showLogoutDialog = true">
              <v-icon size="24">mdi-logout</v-icon>
              <span class="nav-label">LOG OUT</span>
            </v-btn>
          </template>
        </v-col>
      </v-row>
    </v-container>

    <v-dialog v-model="showLogoutDialog" max-width="400">
      <v-card class="pa-3">
        <v-card-title class="d-flex align-center">
          <v-icon color="red" style="margin-bottom: 4px; padding-right: 12px;">mdi-logout</v-icon>
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
  </v-app-bar>
</template>
<script>
import { computed, ref, onMounted, onUnmounted } from "vue";

export default {
  name: "Header-main",
  setup() {
    const isLoggedIn = computed(() => !!localStorage.getItem("token"));
    const isMobile = ref(window.innerWidth <= 960);
    const showLogoutDialog = ref(false);

    const handleLogout = () => {
      localStorage.removeItem("token");
      localStorage.removeItem("tokenExpiry");
      localStorage.removeItem("user");
      showLogoutDialog.value = false;
      window.location.reload();
    };

    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 600;
    };

    onMounted(() => {
      window.addEventListener('resize', checkMobile);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile);
    });

    return {
      isLoggedIn,
      isMobile,
      showLogoutDialog,
      handleLogout,
    };
  },
};
</script>

<style scoped>
.logo-img {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.nav-link {
  color: white;
  font-size: 12px;
  font-weight: 500;
  text-transform: none;
}

.v-app-bar {
  position: fixed;
  top: 0;
  width: 100%;
}

.v-list-item-title {
  font-size: 16px;
}

.nav-label {
  font-size: 12px; 
  margin-left: 2px;
  color: white;
  text-transform: none;
}
</style>

<template>
  <v-bottom-navigation v-model="activeItem" :background-color="'#135389'" app grow v-if="isMobile" color="#135389">
    <v-btn value="home" @click="$router.push('/')">
      <v-icon>mdi-home</v-icon>
      <span>Home</span>
    </v-btn>

    <template v-if="isLoggedIn">
      <v-btn value="mypage" @click="$router.push('/mypage')">
        <v-icon>mdi-account</v-icon>
        <span>Mypage</span>
      </v-btn>

      <v-btn value="camera" @click="$router.push('/mypage/qr_reader')">
        <v-icon>mdi-qrcode-scan</v-icon>
        <span>Reader</span>
      </v-btn>

      <v-btn value="logout" @click="showLogoutDialog = true">
        <v-icon>mdi-logout</v-icon>
        <span>Logout</span>
      </v-btn>
    </template>

    <template v-else>
      <v-btn value="login" @click="$router.push('/login')">
        <v-icon>mdi-login</v-icon>
        <span>Login</span>
      </v-btn>

      <v-btn value="signup" @click="$router.push('/signup')">
        <v-icon>mdi-account-plus</v-icon>
        <span>Register</span>
      </v-btn>
    </template>

        <v-dialog v-model="showLogoutDialog" max-width="400">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon color="red" style="padding-right:12px">mdi-logout</v-icon>
          <span>LOG OUT</span>
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
  </v-bottom-navigation>
</template>

<script>
export default {
  data() {
    return {
      activeItem: 'home',
      isMobile: false,
      isLoggedIn: false,
      showLogoutDialog: false,
    };
  },
  mounted() {
    this.checkMobile();
    this.checkLoginStatus();
    window.addEventListener('resize', this.checkMobile);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth <= 960;
    },
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem("token");
    },
    handleLogout() {
      localStorage.removeItem("token");
      localStorage.removeItem("tokenExpiry");
      localStorage.removeItem("user");
      this.isLoggedIn = false;
      window.location.reload();
    },
  },
};
</script>

<style scoped>
.v-btn {
  text-transform: none;
}
</style>

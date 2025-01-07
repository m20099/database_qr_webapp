<template>
  <v-bottom-navigation v-model="activeItem" :background-color="'#135389'" app grow v-if="isMobile" color="#135389">
    <template v-if="isLoggedIn">
      <v-btn value="mypage" @click="$router.push('/mypage')">
        <v-icon>mdi-account</v-icon>
        <span><b>Mypage</b></span>
      </v-btn>

      <v-btn value="receipt" @click="$router.push('/mypage/receipt_list')">
        <v-icon>mdi-cart</v-icon>
        <span><b>Receipt</b></span>
      </v-btn>      

      <v-btn value="camera" @click="$router.push('/mypage/qr_reader')">
        <v-icon>mdi-qrcode-scan</v-icon>
        <span><b>Reader</b></span>
      </v-btn>

      <v-btn value="setting" @click="$router.push('/mypage/settings')">
        <v-icon>mdi-cog</v-icon>
        <span><b>Setting</b></span>
      </v-btn>
    </template>

    <template v-else>
      <v-btn value="home" @click="$router.push('/')">
        <v-icon>mdi-home</v-icon>
        <span><b>Home</b></span>
      </v-btn>

      <v-btn value="login" @click="$router.push('/login')">
        <v-icon>mdi-login</v-icon>
        <span><b>Login</b></span>
      </v-btn>

      <v-btn value="signup" @click="$router.push('/signup')">
        <v-icon>mdi-account-plus</v-icon>
        <span><b>Register</b></span>
      </v-btn>
    </template>
  </v-bottom-navigation>
</template>

<script>
export default {
  data() {
    return {
      activeItem: 'home',
      isMobile: false,
      isLoggedIn: false,
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
  },
};
</script>

<style scoped>
.v-btn {
  text-transform: none;
}
</style>

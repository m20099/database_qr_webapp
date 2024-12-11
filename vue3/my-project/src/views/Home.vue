<template>
  <div class="home-container">
    <!-- 青背景部分 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>QRコードを利用した<br>買い物履歴管理システム(仮)</h1>
        <p>レシート情報が埋め込まれたQRコードを読み取るだけで簡単に支出を記録</p>
        <div class="hero-actions">
          <router-link to="/login" class="btn">Log In</router-link>
          <router-link to="/userregister" class="btn">Register</router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="@/assets/karigazo.png" alt="仮の画像">
      </div>
    </div>

    <!-- 白背景部分 -->
    <div class="info-section">
      <h2>How to Use</h2>
      <p>未定</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
/* 全体レイアウト */
.home-container {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

/* 青背景セクション */
.hero-section {
  display: flex;
  justify-content: center; /* 要素全体を中央寄せ */
  align-items: center;
  background: linear-gradient(90deg, #0b3a63, #135389, #0b3a63);
  width: 100%; /* 横幅を100%に維持 */
  padding: 40px 10%; /* 左右の余白を縮小 */
  box-sizing: border-box; /* パディング込みで幅を計算 */
  gap: 20px; /* 要素間のスペース */
  color: white;
}

.hero-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  flex: 0.45; /* 幅を45%に制限して寄せる */
}

.hero-content h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}


.hero-actions .btn {
  background-color: white;
  color: #0078d4;
  padding: 10px 20px;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  font-size: 1em;
  transition: background-color 0.3s;
  flex: 1; /* ボタンの幅を均等に */
  max-width: 150px;
}

.hero-actions .btn:hover {
  background-color: #e6f4ff;
}


.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 0.45; /* 幅を45%に制限して寄せる */
}

.hero-image img {
  width: 100%;
  max-width: 300px; /* 最大幅を縮小してバランスを取る */
  height: auto;
  border-radius: 10px;
}

/* 白背景セクション */
.info-section {
  background-color: white;
  padding: 40px;
  text-align: center;
}

.info-section h2 {
  font-size: 1.5em; /* サイズ調整 */
  margin-bottom: 20px;
}

.info-section p {
  font-size: 1em;
  color: #555;
}

/* レスポンシブ対応 */
@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    gap: 10px; /* 縦方向の間隔を縮小 */
  }

  .hero-content {
    margin: 0; /* マージンをリセット */
  }

  .hero-image {
    margin: 20px 0; /* 上下余白追加 */
  }

  .hero-content h1 {
    font-size: 1.8em; /* フォントサイズ縮小 */
  }

  .hero-actions {
    gap: 10px; /* ボタン間の間隔縮小 */
  }

  .info-section h2 {
    font-size: 1.2em; /* サイズ調整 */
  }
}
</style>

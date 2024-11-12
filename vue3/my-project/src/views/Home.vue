<template>
  <div class="home-container">
    <!-- タイトル -->
    <h1 class="title">QR Code Web App Demo</h1>
    
    <!-- ボックスのコンテナ -->
    <div class="boxes-container">
      <!-- ボックス1 -->
      <div class="box">
        <h3>店側</h3>
        <button class="box-button" @click="$router.push('/storehome')">PUSH</button>
      </div>

      <!-- ボックス2 -->
      <div class="box">
        <h3>ユーザ側</h3>
        <button class="box-button" @click="$router.push('/userhome')">PUSH</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home-Page'
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #30343A;
}

.title {
  font-size: 2.5em;
  font-weight: bold;
  color: #30343A;
  margin-bottom: 40px;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
}

.boxes-container {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.box {
  background-color: #ffffff;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  width: 220px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}

.box:hover {
  transform: translateY(-5px);
}

.box h3 {
  margin-bottom: 15px;
  color: #333;
  font-size: 1.2em;
}

.box-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  color: white;
  background-color: #135389;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.box-button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

@media (max-width: 600px) {
  .boxes-container {
    flex-direction: column;
  }
}
</style>

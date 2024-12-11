<template>
  <div class="user-home">
    <div class="chart-container">
      <button class="nav-button left" @click="goToPreviousWeek">＜</button>
      <canvas id="expenseChart"></canvas>
      <button class="nav-button right" @click="goToNextWeek" :disabled="isNextButtonDisabled">＞</button>
    </div>
    <div class="totals-row">
      <div class="total-container">
        <p class="total-label">合計支出（{{ computedDateRange }}）</p>
        <p class="total-expenses">¥{{ totalExpense.toLocaleString() }}</p>
      </div>
      <div class="total-container">
        <p class="total-label">1か月の合計支出</p>
        <p class="total-expenses">¥{{ monthlyTotalExpense.toLocaleString() }}</p>
      </div>
    </div>
    <div class="qr-button-container">
      <router-link to="/userhome/qr_reader" class="qr-button">QRコードを読み取る</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import Chart from "chart.js/auto";

export default {
  name: "UserHome",
  setup() {
    const startDate = ref(new Date());
    const weeklyData = ref([]);
    const today = new Date();
    const monthlyData = ref([]);
    let chartInstance = null;

    // サンプルデータ生成
    const generateDataWithDates = (startDate, days) => {
      const result = { data: [], labels: [] };
      for (let i = 0; i < days; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        const formatted = `${date.getMonth() + 1}/${date.getDate()}`;
        result.labels.push(formatted);
        result.data.push(date > today ? 0 : Math.floor(Math.random() * 3000));
      }
      return result;
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            callbacks: {
                label: (tooltipItem) => `¥${tooltipItem.raw.toLocaleString()}`,
            },
            },
        },
        scales: {
            x: {
            grid: { display: false },
            ticks: {
                font: { size: 12 },
                color: "#555",
            },
            },
            y: {
            grid: { color: "rgba(0, 0, 0, 0.1)" },
            ticks: {
                font: { size: 12 },
                color: "#555",
                stepSize: 2000,
                callback: (value) => `¥${value.toLocaleString()}`,
            },
            beginAtZero: true,
            },
        },
        };

        const updateChart = () => {
        const sundayStart = getSundayStart(startDate.value);
        const { data: newWeeklyData, labels } = generateDataWithDates(sundayStart, 7);
        weeklyData.value = newWeeklyData;

        const ctx = document.getElementById("expenseChart").getContext("2d");
        const chartData = {
            labels: labels,
            datasets: [
            {
                data: newWeeklyData,
                backgroundColor: "rgba(33, 150, 243, 0.6)",
                borderColor: "rgba(33, 150, 243, 1)",
                borderWidth: 1,
                hoverBackgroundColor: "rgba(33, 150, 243, 0.8)",
            },
            ],
        };

        if (chartInstance) {
            chartInstance.destroy();
        }
        chartInstance = new Chart(ctx, { type: "bar", data: chartData, options: chartOptions });
        };

    const isNextButtonDisabled = computed(() => {
      const nextWeekStartDate = new Date(startDate.value);
      nextWeekStartDate.setDate(nextWeekStartDate.getDate() + 7);
      return nextWeekStartDate > today; // 次の週の開始日が今日より未来なら無効
    });

    const totalExpense = computed(() => {
      return weeklyData.value.reduce((sum, expense) => sum + expense, 0);
    });

    const monthlyTotalExpense = computed(() => {
      return monthlyData.value.reduce((sum, expense) => sum + expense, 0);
    });

    const computedDateRange = computed(() => {
      const start = new Date(startDate.value);
      const end = new Date(startDate.value);
      end.setDate(end.getDate() + 6);
      return `${start.getMonth() + 1}/${start.getDate()} ～ ${end.getMonth() + 1}/${end.getDate()}`;
    });

    const getSundayStart = (date) => {
      const currentDate = new Date(date);
      const day = currentDate.getDay();
      currentDate.setDate(currentDate.getDate() - day);
      return currentDate;
    };

    const goToPreviousWeek = () => {
      const newDate = new Date(startDate.value);
      newDate.setDate(newDate.getDate() - 7);
      startDate.value = getSundayStart(newDate);
      updateChart();
    };

    const goToNextWeek = () => {
      const currentDate = new Date(startDate.value);
      currentDate.setDate(currentDate.getDate() + 7);
      startDate.value = currentDate;
      updateChart();
    };

    const generateMonthlyData = () => {
        const startOfMonth = new Date(today);
        startOfMonth.setDate(1); // 今月の初日
        const endOfMonth = new Date(today);
        endOfMonth.setMonth(startOfMonth.getMonth() + 1);
        endOfMonth.setDate(0); // 今月の末日

        const result = [];
        for (
            let date = new Date(startOfMonth);
            date <= endOfMonth;
            date.setDate(date.getDate() + 1)
        ) {
            const value = date > today ? 0 : Math.floor(Math.random() * 3000); // 未来は0
            result.push(value);
        }

        monthlyData.value = result;
    };


    onMounted(() => {
      updateChart();
      generateMonthlyData();
    });

    return {
      goToPreviousWeek,
      goToNextWeek,
      totalExpense,
      monthlyTotalExpense,
      isNextButtonDisabled,
      computedDateRange,
    };
  },
};
</script>


<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap");

.user-home {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: "Poppins", Arial, sans-serif;
  color: #4a4a4a;
}

.chart-container {
  width: 100%;
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 16px;
  background: #ffffff;
  position: relative;
  border: 2px solid #dcdcdc; /* 追加: 枠線 */
}

.chart-container canvas {
  width: 100%;
  height: 300px;
}

.nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #6c5ce7, #341f97);
  border: none;
  border-radius: 50%;
  padding: 10px;
  width: 45px;
  height: 45px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-button:hover {
  background: linear-gradient(135deg, #8e44ad, #341f97);
}

.nav-button.left {
  left: -60px;
}

.nav-button.right {
  right: -60px;
}

.nav-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.totals-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 740px;
  margin: 20px auto;
  gap: 20px;
  color: #333;
}

.total-container {
  flex: 1;
  padding: 20px;
  border-radius: 12px;
  background-color: #ffffff;
  text-align: center;
  border: 2px solid #dcdcdc;
}

.total-label {
  font-size: 16px;
  font-weight: 500;
  color: #7f8c8d;
  margin-bottom: 10px;
}

.total-expenses {
  font-size: 32px;
  font-weight: 700;
  color: #2980b9;
  margin: 0;
}

.qr-button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.qr-button {
  background: linear-gradient(135deg, #f9f9f9, #a7d4f2);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s ease;
}

.qr-button:hover {
  background: linear-gradient(135deg, #f9f8fa, #828282);
}
</style>


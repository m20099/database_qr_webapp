<template>
  <v-container class="user-home">
    <v-row justify="center">
      <v-col cols="12" md="10" sm="12">
        <v-card outlined>
          <v-card-title class="d-flex justify-space-between">
            <v-btn icon @click="goToPreviousWeek">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            {{ computedDateRange }}
            <v-btn icon @click="goToNextWeek" :disabled="isNextButtonDisabled">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <canvas id="expenseChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="totals-row" dense>
      <v-col cols="12" md="5" sm="12">
        <v-card outlined class="pa-2 mb-6">
          <v-tabs v-model="activeTab" align-tabs="center" class="tab-btn-group">
            <v-tab :value="1">
              <v-icon color="blue" class="mr-1">mdi-calendar-today</v-icon>Today
            </v-tab>
            <v-tab :value="2">
              <v-icon color="green" class="mr-1">mdi-calendar-week</v-icon>Week
            </v-tab>
            <v-tab :value="3">
              <v-icon color="orange" class="mr-1">mdi-calendar-month</v-icon>Month
            </v-tab>
          </v-tabs>
          <v-tabs-window v-model="activeTab" :transition="tabTransition">
            <v-tabs-window-item :value="1">
              <v-card-text class="text-center">
                <div class="text-subtitle-1">今日</div>
                <div class="text-h5 font-weight-bold mt-2">
                  ¥{{ todayExpense.toLocaleString() }}
                </div>
              </v-card-text>
            </v-tabs-window-item>

            <v-tabs-window-item :value="2" :transition="tabTransition">
              <v-card-text class="text-center">
                <div class="text-subtitle-1"> {{ computedDateRange }}</div>
                <div class="text-h5 font-weight-bold mt-2">
                  ¥{{ totalExpense.toLocaleString() }}
                </div>
              </v-card-text>
            </v-tabs-window-item>

            <v-tabs-window-item :value="3" :transition="tabTransition">
              <v-card-text class="text-center">
                <div class="text-subtitle-1">今月</div>
                <div class="text-h5 font-weight-bold mt-2">
                  ¥{{ monthlyExpense.toLocaleString() }}
                </div>
              </v-card-text>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted, computed, nextTick } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "UserHome",
  setup() {
    const startDate = ref(new Date());
    const weeklyData = ref([]);
    const today = new Date();
    const purchaseRecords = ref([]);
    let chartInstance = null;
    const activeTab = ref(1);

    const fetchPurchaseData = async () => {
      try {
        const userId = JSON.parse(localStorage.getItem("user"));
        
        const response = await axios.get("http://localhost:5000/api/purchases", {
            params: { user_id: userId },
        });

        purchaseRecords.value = response.data.purchase_records;

        const groupedData = {};
        purchaseRecords.value.forEach(record => {
            const date = new Date(record.purchase_date);
            const formattedDate = `${date.getMonth() + 1}/${date.getDate()}`;
            groupedData[formattedDate] = (groupedData[formattedDate] || 0) + record.total_amount;
        });


        const labels = [];
        const data = [];
        const sundayStart = getSundayStart(startDate.value);
        for (let i = 0; i < 7; i++) {
          const date = new Date(sundayStart);
          date.setDate(date.getDate() + i);
          const formatted = `${date.getMonth() + 1}/${date.getDate()}`;
          labels.push(formatted);
          data.push(groupedData[formatted] || 0);
        }

        weeklyData.value = data;
        updateChart(labels, data);
        } catch (error) {
        console.error("購入データ取得エラー:", error.response ? error.response.data : error.message);
        }
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

    const updateChart = (labels, data) => {
      const ctx = document.getElementById("expenseChart").getContext("2d");
      const chartData = {
        labels: labels,
        datasets: [
          {
            data: data,
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
      return nextWeekStartDate > today;
    });

    const totalExpense = computed(() => {
      return weeklyData.value.reduce((sum, expense) => sum + expense, 0);
    });

    const todayExpense = computed(() => {
        const formattedToday = `${today.getMonth() + 1}/${today.getDate()}`;
        return weeklyData.value.reduce((sum, amount, index) => {
            const label = chartInstance?.data.labels[index];
            return label === formattedToday ? sum + amount : sum;
        }, 0);
    });

    const monthlyExpense = computed(() => {
        const currentMonth = today.getMonth() + 1;
        const currentYear = today.getFullYear();

        return purchaseRecords.value.reduce((sum, record) => {
            const date = new Date(record.purchase_date);
            if (date.getFullYear() === currentYear && date.getMonth() + 1 === currentMonth) {
            sum += record.total_amount;
            }
            return sum;
        }, 0);
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
      fetchPurchaseData();
    };

    const goToNextWeek = () => {
      const currentDate = new Date(startDate.value);
      currentDate.setDate(currentDate.getDate() + 7);
      startDate.value = currentDate;
      fetchPurchaseData();
    };

    onMounted(async () => {
        await nextTick();
        fetchPurchaseData();
    });

    return {
      activeTab,
      goToPreviousWeek,
      goToNextWeek,
      totalExpense,
      todayExpense,
      monthlyExpense,
      isNextButtonDisabled,
      computedDateRange,
    };
  },
};
</script>

<style scoped>
.user-home {
  margin-top: 20px;
}

.v-card {
  box-shadow: none !important;
  border: 1px solid #a4a4a4;
  border-radius: 16px; 
}
</style>


import { ref, onMounted, computed, nextTick } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "UserHome",
  setup() {
    const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
    const weeklyData = ref([]);
    const today = new Date();
    const purchaseRecords = ref([]);
    let chartInstance = null;
    const activeTab = ref(1);
    const userMaxValue = ref(null);
    const userName = ref('');
    const userId = JSON.parse(localStorage.getItem("user"));

    const fetchUserData = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/username/${userId}`);
            if (response.status === 200) {
                userName.value = response.data.user_name;
                console.log("User Name:", userName);
            } else {
                console.error("Failed to fetch user data:", response.status);
            }
        } catch (error) {
            console.error("Error fetching user data:", error);
        }
    };

    const fetchUserSettings = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/setting/${userId}`);
            if (response.status === 200) {
                userMaxValue.value = response.data.budget_limit || null; // デフォルトはnull
            } else {
                console.error("設定データ取得失敗:", response.status);
            }
        } catch (error) {
            console.error("設定データ取得エラー:", error);
        }
    };
    

    const fetchPurchaseData = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/purchases`, {
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

        const weekdays = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

        for (let i = 0; i < 7; i++) {
          const date = new Date(sundayStart);
          date.setDate(date.getDate() + i);

        const weekday = weekdays[date.getDay()];
        const formattedDate = `${date.getMonth() + 1}/${date.getDate()}`;
        labels.push([weekday, formattedDate]);

          const formattedDateKey = `${date.getMonth() + 1}/${date.getDate()}`;
          data.push(groupedData[formattedDateKey] || 0);
        }

        weeklyData.value = data;
        updateChart(labels, data);
        } catch (error) {
        console.error("購入データ取得エラー:", error.response ? error.response.data : error.message);
        }
    };

    const updateChart = (labels, data) => {
        const maxDataValue = Math.max(...data);

        const getRoundedMax = (value) => {
            const base = 1000;
            const roundedValue = Math.ceil(value / base) * base;
            return Math.max(roundedValue, 10000);
        };

        const autoRoundedMax = getRoundedMax(maxDataValue * 1.2);
        const chartMax = userMaxValue.value || autoRoundedMax;

        const getStepSize = (maxValue) => {
            const magnitude = Math.pow(10, Math.floor(Math.log10(maxValue)));
            const stepSize = Math.ceil(maxValue / 10 / magnitude) * magnitude;
            return stepSize;
          };

        const stepSize = getStepSize(chartMax);

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

        chartInstance = new Chart(ctx, {
            type: "bar",
            data: chartData,
            options: {
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
                    font: { size: window.innerWidth < 600 ? 10 : 12 },
                    color: "#555",
                    autoSkip: false,
                },
                },
                y: {
                grid: { color: "rgba(0, 0, 0, 0.1)" },
                ticks: {
                    // display: false,
                    font: { size: window.innerWidth < 600 ? 10 : 12 },
                    color: "#555",
                    autoSkip: false,
                    stepSize: stepSize,
                    callback: (value) => `¥${value.toLocaleString()}`,
                },
                beginAtZero: true,
                max: chartMax,
                },
            },
            },
        });
    };

    const setUserMaxValue = (value) => {
        userMaxValue.value = value;
        fetchPurchaseData();
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
        const formattedToday = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
        return purchaseRecords.value.reduce((sum, record) => {
            if (record.purchase_date.startsWith(formattedToday)) {
                sum += record.total_amount;
            }
            return sum;
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
        const d = new Date(date);
        d.setDate(d.getDate() - d.getDay());
        return d;
    };

    const startDate = ref(getSundayStart(new Date()));

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
        await fetchUserSettings();
        fetchUserData();
        fetchPurchaseData();
    });

    return {
      userName,
      activeTab,
      goToPreviousWeek,
      goToNextWeek,
      totalExpense,
      todayExpense,
      monthlyExpense,
      isNextButtonDisabled,
      computedDateRange,
      setUserMaxValue,
      userMaxValue
    };
  },
};
<template>
  <v-container class="user-home">
    <v-row justify="center">
      <v-col cols="8" md="8" sm="6">
        <v-card outlined class="pa-2 d-flex align-center">
          <v-icon class="mr-1">mdi-account</v-icon>
          <span>{{ userName || 'Loading...' }}</span>
        </v-card>
      </v-col>
      <v-col cols="2" md="1" sm="2">
        <v-card outlined class="pa-0">
        <router-link to="/mypage/qr_reader" class="d-flex align-center justify-center text-decoration-none">
            <v-btn block class="pa-2" color="primary">
                <v-icon>mdi-camera</v-icon>
            </v-btn>
        </router-link>
        </v-card>
      </v-col>
      <v-col cols="2" md="1" sm="2">
        <v-card outlined class="pa-0">
        <router-link to="/mypage/settings" class="d-flex align-center justify-center text-decoration-none">
            <v-btn block class="pa-2" color="primary">
                <v-icon>mdi-cog</v-icon>
            </v-btn>
        </router-link>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="10" sm="10">
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
      <v-col cols="12" md="5" sm="10">
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
          <v-tabs-window v-model="activeTab">
            <v-tabs-window-item :value="1">
              <v-card-text class="text-center">
                <div class="text-subtitle-1">今日</div>
                <div class="text-h5 font-weight-bold mt-2">
                  ¥{{ todayExpense.toLocaleString() }}
                </div>
              </v-card-text>
            </v-tabs-window-item>

            <v-tabs-window-item :value="2">
              <v-card-text class="text-center">
                <div class="text-subtitle-1"> {{ computedDateRange }}</div>
                <div class="text-h5 font-weight-bold mt-2">
                  ¥{{ totalExpense.toLocaleString() }}
                </div>
              </v-card-text>
            </v-tabs-window-item>

            <v-tabs-window-item :value="3">
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

<script src="@/scripts/UserHomeScript.js"></script>

<style scoped>
.user-home {
  margin-top: 20px;
  max-width: 1000px;
}

.v-card {
  box-shadow: none !important;
  border: 1px solid #a4a4a4;
  border-radius: 16px; 
}
</style>


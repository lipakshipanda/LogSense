<script setup lang="ts">
import { ref } from 'vue'
import Dashboard from './pages/Dashboard.vue'
import LogsPage from './pages/LogsPage.vue'
import AnomaliesPage from './pages/AnomaliesPage.vue'
import RCAPage from './pages/RCAPage.vue'

const NAV = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'logs', label: 'Live Logs' },
  { id: 'anomalies', label: 'Anomalies' },
  { id: 'rca', label: 'RCA Reports' },
]
const page = ref('dashboard')
</script>

<template>
  <div class="app">
    <nav class="navbar">
      <span class="logo">🛡 LogSense</span>
      <div class="nav-links">
        <button
          v-for="n in NAV" :key="n.id"
          :class="['nav-btn', { active: page === n.id }]"
          @click="page = n.id"
        >{{ n.label }}</button>
      </div>
    </nav>
    <main class="main">
      <Dashboard v-if="page === 'dashboard'" />
      <LogsPage v-else-if="page === 'logs'" />
      <AnomaliesPage v-else-if="page === 'anomalies'" />
      <RCAPage v-else-if="page === 'rca'" />
    </main>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { api } from '../utils/api'
import type { DashboardStats } from '../types'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

const stats = ref<DashboardStats | null>(null)
const loading = ref(true)
const healthValues = ref<number[]>([])
const typeValues = ref<number[]>([])
const barData = ref({ labels: [] as string[], datasets: [{ label: 'Anomalies', backgroundColor: '#4f5cff', data: [] as number[], borderRadius: 4 }] })
const pieData = ref({ labels: [] as string[], datasets: [{ backgroundColor: ['#f87171', '#fbbf24', '#a78bfa', '#60a5fa'], data: [] as number[] }] })
const chartOptions = { responsive: true, plugins: { legend: { labels: { color: '#94a3b8' } } }, scales: { x: { ticks: { color: '#64748b' } }, y: { ticks: { color: '#64748b' } } } }

async function load() {
  loading.value = true
  try {
    const [s, t, h] = await Promise.all([api.getStats(), api.getAnomalyTypes(), api.getServiceHealth()])
    stats.value = s.data
    typeValues.value = Object.values(t.data.breakdown)
    healthValues.value = Object.values(h.data.service_health)
    barData.value = { labels: Object.keys(h.data.service_health).map(n => n.replace('-service', '')), datasets: [{ label: 'Anomalies', backgroundColor: '#4f5cff', data: healthValues.value, borderRadius: 4 }] }
    pieData.value = { labels: Object.keys(t.data.breakdown), datasets: [{ backgroundColor: ['#f87171', '#fbbf24', '#a78bfa', '#60a5fa'], data: typeValues.value }] }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function generateAndRefresh() {
  await api.generateLogs(80, 0.15)
  load()
}

onMounted(load)
</script>

<template>
  <div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
      <h1 class="page-title" style="margin-bottom:0">SOC Dashboard</h1>
      <button class="btn btn-primary" @click="generateAndRefresh">⚡ Generate Logs</button>
    </div>
    <p v-if="loading" class="loading">Loading dashboard…</p>
    <template v-else>
      <div class="stat-grid">
        <div class="stat-card"><div class="stat-label">Total Logs</div><div class="stat-value">{{ stats?.total_logs ?? 0 }}</div></div>
        <div class="stat-card"><div class="stat-label">Anomalies</div><div class="stat-value danger">{{ stats?.total_anomalies ?? 0 }}</div></div>
        <div class="stat-card"><div class="stat-label">Anomaly Rate</div><div class="stat-value warn">{{ stats?.anomaly_rate ?? 0 }}%</div></div>
        <div class="stat-card"><div class="stat-label">Services Hit</div><div class="stat-value">{{ stats?.services_affected ?? 0 }}</div></div>
        <div class="stat-card"><div class="stat-label">Critical Events</div><div class="stat-value danger">{{ stats?.critical_count ?? 0 }}</div></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
        <div class="card">
          <div class="card-title">Anomalies per Service</div>
          <Bar v-if="healthValues.length" :data="barData" :options="chartOptions" />
          <p v-else class="loading">No data — click Generate Logs</p>
        </div>
        <div class="card">
          <div class="card-title">Anomaly Type Breakdown</div>
          <Pie v-if="typeValues.length" :data="pieData" :options="chartOptions" />
          <p v-else class="loading">No data — click Generate Logs</p>
        </div>
      </div>
    </template>
  </div>
</template>
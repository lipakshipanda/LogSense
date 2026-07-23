<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../utils/api'
import type { Anomaly } from '../types'

const TYPE_CLASS: Record<string, string> = {
  latency_spike: 'badge-latency', cascade_failure: 'badge-cascade',
  error_burst: 'badge-error_b', unknown_anomaly: 'badge-WARN',
}
const anomalies = ref<Anomaly[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const res = await api.getAnomalies(100)
    anomalies.value = [...res.data.anomalies].reverse()
  } catch { anomalies.value = [] } finally { loading.value = false }
}
onMounted(load)
</script>

<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem">
      <h1 class="page-title" style="margin-bottom:0">Detected Anomalies</h1>
      <button class="btn btn-primary" @click="load">↻ Refresh</button>
    </div>
    <p v-if="loading" class="loading">Loading…</p>
    <div class="card" style="padding:0">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Time</th><th>Service</th><th>Type</th><th>Score</th><th>Severity</th></tr></thead>
          <tbody>
            <tr v-for="a in anomalies" :key="a.log_id">
              <td>{{ new Date(a.timestamp).toLocaleTimeString() }}</td>
              <td>{{ a.service }}</td>
              <td><span :class="`badge ${TYPE_CLASS[a.anomaly_type] ?? 'badge-WARN'}`">{{ a.anomaly_type?.replace(/_/g, ' ') }}</span></td>
              <td>
                <div style="display:flex;align-items:center;gap:8px">
                  <div style="flex:1;background:#2d3148;border-radius:4px;height:6px">
                    <div :style="{ width: `${a.anomaly_score * 100}%`, background: a.anomaly_score > 0.7 ? '#f87171' : '#fbbf24', height: '100%', borderRadius: '4px' }"></div>
                  </div>
                  <span>{{ (a.anomaly_score * 100).toFixed(0) }}%</span>
                </div>
              </td>
              <td :style="{ color: a.anomaly_score > 0.7 ? '#f87171' : '#fbbf24' }">{{ a.anomaly_score > 0.7 ? 'HIGH' : 'MEDIUM' }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="!anomalies.length && !loading" class="loading">No anomalies — generate logs from Dashboard first</p>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { api } from '../utils/api'
import type { LogEntry } from '../types'

const logs = ref<LogEntry[]>([])
const loading = ref(false)
const filter = ref('ALL')
const filters = ['ALL', 'INFO', 'WARN', 'ERROR', 'CRITICAL']

async function load() {
  loading.value = true
  try {
    const res = await api.getLogs(200)
    logs.value = [...res.data.logs].reverse()
  } catch { logs.value = [] } finally { loading.value = false }
}
async function generate() { await api.generateLogs(50, 0.12); load() }

const visible = computed(() =>
  (filter.value === 'ALL' ? logs.value : logs.value.filter(l => l.level === filter.value)).slice(0, 100)
)
function statusColor(code: number) { return code >= 500 ? '#f87171' : code >= 400 ? '#fbbf24' : '#34d399' }

onMounted(load)
</script>

<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem">
      <h1 class="page-title" style="margin-bottom:0">Live Logs</h1>
      <div style="display:flex;gap:8px">
        <button v-for="f in filters" :key="f" class="btn" :class="filter === f ? 'btn-primary' : ''"
          :style="filter !== f ? 'background:#2d3148;color:#94a3b8;padding:5px 12px;font-size:0.8rem' : 'padding:5px 12px;font-size:0.8rem'"
          @click="filter = f">{{ f }}</button>
        <button class="btn btn-primary" @click="generate">+ Generate</button>
      </div>
    </div>
    <p v-if="loading" class="loading">Loading…</p>
    <div class="card" style="padding:0">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Time</th><th>Service</th><th>Level</th><th>Message</th><th>Latency</th><th>Status</th></tr></thead>
          <tbody>
            <tr v-for="log in visible" :key="log.id">
              <td style="white-space:nowrap">{{ new Date(log.timestamp).toLocaleTimeString() }}</td>
              <td>{{ log.service }}</td>
              <td><span :class="`badge badge-${log.level}`">{{ log.level }}</span></td>
              <td>{{ log.message }}</td>
              <td>{{ log.latency_ms }} ms</td>
              <td :style="{ color: statusColor(log.status_code) }">{{ log.status_code }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="!visible.length && !loading" class="loading">No logs — click Generate</p>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../utils/api'
import type { RCAReport } from '../types'

const reports = ref<RCAReport[]>([])
const genLoad = ref(false)
const message = ref('')
const searchQuery = ref('')
const searchResults = ref<{ score: number; root_cause: string }[]>([])

async function loadHistory() {
  try { reports.value = (await api.getRCAHistory()).data.reports } catch { reports.value = [] }
}

async function generateRCA() {
  genLoad.value = true
  message.value = ''
  try {
    const res = await api.generateRCA()
    message.value = res.data.message + (res.data.report?.jira_ticket ? ` — Jira ticket ${res.data.report.jira_ticket} created` : '')
    loadHistory()
  } catch {
    message.value = 'Error: Make sure backend is running and logs have been generated.'
  } finally {
    genLoad.value = false
  }
}

async function searchSimilar() {
  if (!searchQuery.value.trim()) return
  searchResults.value = (await api.searchSimilar(searchQuery.value)).data.results
}

onMounted(loadHistory)
</script>

<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem">
      <h1 class="page-title" style="margin-bottom:0">RCA Reports</h1>
      <button class="btn btn-danger" :disabled="genLoad" @click="generateRCA">
        {{ genLoad ? 'Generating…' : '🤖 Generate RCA with Groq' }}
      </button>
    </div>

    <div v-if="message" style="margin-bottom:1rem;padding:10px 16px;background:#1a3a2a;border-radius:8px;color:#34d399;font-size:0.875rem">
      {{ message }}
    </div>

    <div class="card">
      <div class="card-title">Find Similar Past Incidents</div>
      <div style="display:flex;gap:8px">
        <input v-model="searchQuery" placeholder="e.g. database connection timeout"
          style="flex:1;background:#12151f;border:1px solid #2d3148;border-radius:8px;padding:8px 12px;color:#e2e8f0"
          @keyup.enter="searchSimilar" />
        <button class="btn btn-primary" @click="searchSimilar">Search</button>
      </div>
      <div v-if="searchResults.length" style="margin-top:12px;display:flex;flex-direction:column;gap:8px">
        <div v-for="(r, i) in searchResults" :key="i" style="background:#12151f;border-radius:8px;padding:10px 14px">
          <div style="font-size:0.75rem;color:#64748b">Match score: {{ r.score.toFixed(3) }}</div>
          <div style="font-size:0.875rem;color:#e2e8f0">{{ r.root_cause }}</div>
        </div>
      </div>
    </div>

    <div v-if="!reports.length" class="card">
      <p style="color:#64748b;text-align:center">No reports yet. Go to Dashboard → Generate Logs, then come back and click Generate RCA.</p>
    </div>

    <div v-for="r in reports" :key="r.incident_id" class="card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
        <div>
          <div style="font-size:0.75rem;color:#64748b;margin-bottom:4px">Incident #{{ r.incident_id }}</div>
          <div :class="`sev-${r.severity}`" style="font-size:1rem;font-weight:700">{{ r.severity }} SEVERITY</div>
        </div>
        <div style="font-size:0.75rem;color:#64748b">{{ new Date(r.generated_at).toLocaleString() }}</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
        <div style="background:#12151f;border-radius:8px;padding:10px 14px">
          <div style="font-size:0.7rem;color:#64748b;margin-bottom:6px;text-transform:uppercase">Root Cause</div>
          <div style="font-size:0.875rem;color:#e2e8f0">{{ r.root_cause }}</div>
        </div>
        <div style="background:#12151f;border-radius:8px;padding:10px 14px">
          <div style="font-size:0.7rem;color:#64748b;margin-bottom:6px;text-transform:uppercase">Impact</div>
          <div style="font-size:0.875rem;color:#e2e8f0">{{ r.impact_summary }}</div>
        </div>
      </div>
      <div style="background:#12151f;border-radius:8px;padding:10px 14px;margin-bottom:12px">
        <div style="font-size:0.7rem;color:#64748b;margin-bottom:6px;text-transform:uppercase">Suggested Fix</div>
        <div style="font-size:0.875rem;color:#34d399">{{ r.suggested_fix }}</div>
      </div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
        <span style="font-size:0.7rem;color:#64748b">Affected:</span>
        <span v-for="s in r.affected_services" :key="s" style="font-size:0.75rem;background:#1e2235;padding:2px 8px;border-radius:4px;color:#94a3b8">{{ s }}</span>
        <span v-if="r.jira_ticket" style="font-size:0.75rem;background:#0052cc;padding:2px 8px;border-radius:4px;color:#fff;margin-left:auto">🎫 {{ r.jira_ticket }}</span>
      </div>
    </div>
  </div>
</template>
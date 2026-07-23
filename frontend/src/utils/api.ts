import axios from 'axios'
import type { LogEntry, Anomaly, RCAReport, DashboardStats } from '../types'

const BASE = 'http://localhost:8000/api'

export const api = {
  generateLogs: (n = 50, ratio = 0.1) =>
    axios.get(`${BASE}/logs/generate`, { params: { n, anomaly_ratio: ratio } }),
  getLogs: (limit = 100) =>
    axios.get<{ logs: LogEntry[]; count: number }>(`${BASE}/logs/`, { params: { limit } }),
  getAnomalies: (limit = 50) =>
    axios.get<{ anomalies: Anomaly[]; count: number }>(`${BASE}/anomalies/`, { params: { limit } }),
  generateRCA: () =>
    axios.post<{ message: string; report: RCAReport | null }>(`${BASE}/rca/generate`),
  getRCAHistory: () =>
    axios.get<{ reports: RCAReport[]; count: number }>(`${BASE}/rca/history`),
  searchSimilar: (query: string, top_k = 5) =>
    axios.get<{ results: { score: number; root_cause: string }[] }>(`${BASE}/rca/similar`, { params: { query, top_k } }),
  getStats: () => axios.get<DashboardStats>(`${BASE}/stats/`),
  getAnomalyTypes: () => axios.get<{ breakdown: Record<string, number> }>(`${BASE}/stats/anomaly-types`),
  getServiceHealth: () => axios.get<{ service_health: Record<string, number> }>(`${BASE}/stats/service-health`),
}
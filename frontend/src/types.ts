export interface LogEntry {
  id: string
  timestamp: string
  service: string
  level: 'INFO' | 'WARN' | 'ERROR' | 'CRITICAL'
  message: string
  latency_ms: number
  status_code: number
}

export interface Anomaly {
  log_id: string
  service: string
  timestamp: string
  anomaly_score: number
  is_anomaly: boolean
  anomaly_type: 'latency_spike' | 'cascade_failure' | 'error_burst' | 'unknown_anomaly'
}

export interface RCAReport {
  incident_id: string
  affected_services: string[]
  root_cause: string
  impact_summary: string
  suggested_fix: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  generated_at: string
  jira_ticket?: string | null
}

export interface DashboardStats {
  total_logs: number
  total_anomalies: number
  anomaly_rate: number
  services_affected: number
  critical_count: number
}
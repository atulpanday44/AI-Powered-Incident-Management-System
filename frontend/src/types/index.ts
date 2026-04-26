/**
 * Type definitions for the Incident Management System
 */

export enum LogLevel {
  DEBUG = "DEBUG",
  INFO = "INFO",
  WARNING = "WARNING",
  ERROR = "ERROR",
  CRITICAL = "CRITICAL",
}

export enum SeverityLevel {
  LOW = "LOW",
  MEDIUM = "MEDIUM",
  HIGH = "HIGH",
  CRITICAL = "CRITICAL",
}

export enum IncidentStatus {
  OPEN = "OPEN",
  IN_PROGRESS = "IN_PROGRESS",
  RESOLVED = "RESOLVED",
  CLOSED = "CLOSED",
}

export interface Log {
  id: string;
  service: string;
  level: string;
  message: string;
  timestamp: string;
  created_at: string;
}

export interface Incident {
  id: string;
  title: string;
  service: string;
  severity: string;
  status: string;
  cluster_id: string | null;
  anomaly_score: number | null;
  log_count: number;
  created_at: string;
  updated_at: string;
}

export interface CreateLogRequest {
  service: string;
  level: LogLevel;
  message: string;
  timestamp?: string;
}

export interface CreateIncidentRequest {
  title: string;
  service: string;
  severity: SeverityLevel;
  cluster_id?: string;
  anomaly_score?: number;
}

export interface UpdateIncidentRequest {
  status?: IncidentStatus;
  severity?: SeverityLevel;
}

export interface Statistics {
  total_incidents: number;
  open_incidents: number;
  critical_incidents: number;
  high_incidents: number;
  timestamp: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

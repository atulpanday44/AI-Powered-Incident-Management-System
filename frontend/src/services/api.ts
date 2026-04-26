/**
 * API client service for backend communication
 */

import {
  Log,
  Incident,
  CreateLogRequest,
  CreateIncidentRequest,
  UpdateIncidentRequest,
  Statistics,
} from "../types";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Logs API
  async ingestLog(log: CreateLogRequest): Promise<Log> {
    return this.request<Log>("/logs", {
      method: "POST",
      body: JSON.stringify({
        ...log,
        timestamp: log.timestamp || new Date().toISOString(),
      }),
    });
  }

  async getLogs(
    service?: string,
    level?: string,
    limit: number = 100
  ): Promise<Log[]> {
    const params = new URLSearchParams();
    if (service) params.append("service", service);
    if (level) params.append("level", level);
    params.append("limit", limit.toString());

    return this.request<Log[]>(`/logs?${params.toString()}`);
  }

  async getLog(logId: string): Promise<Log> {
    return this.request<Log>(`/logs/${logId}`);
  }

  // Incidents API
  async createIncident(incident: CreateIncidentRequest): Promise<Incident> {
    return this.request<Incident>("/incidents", {
      method: "POST",
      body: JSON.stringify(incident),
    });
  }

  async getIncidents(
    service?: string,
    status?: string,
    severity?: string,
    limit: number = 100
  ): Promise<Incident[]> {
    const params = new URLSearchParams();
    if (service) params.append("service", service);
    if (status) params.append("status_filter", status);
    if (severity) params.append("severity", severity);
    params.append("limit", limit.toString());

    return this.request<Incident[]>(`/incidents?${params.toString()}`);
  }

  async getIncident(incidentId: string): Promise<Incident> {
    return this.request<Incident>(`/incidents/${incidentId}`);
  }

  async updateIncident(
    incidentId: string,
    update: UpdateIncidentRequest
  ): Promise<Incident> {
    return this.request<Incident>(`/incidents/${incidentId}`, {
      method: "PATCH",
      body: JSON.stringify(update),
    });
  }

  async getStatistics(): Promise<Statistics> {
    return this.request<Statistics>("/incidents-summary");
  }

  async getOpenIncidents(): Promise<Incident[]> {
    return this.getIncidents(undefined, "OPEN");
  }

  async getCriticalIncidents(): Promise<Incident[]> {
    return this.getIncidents(undefined, undefined, "CRITICAL");
  }
}

export default new ApiClient();

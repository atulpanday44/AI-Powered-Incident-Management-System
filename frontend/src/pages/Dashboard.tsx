/**
 * Dashboard page
 */

import React, { useEffect, useState } from "react";
import { StatCard } from "../components/StatCard";
import { Table } from "../components/Table";
import { Badge } from "../components/Badge";
import api from "../services/api";
import { Incident, Statistics } from "../types";
import { useApi } from "../hooks/useApi";

export const Dashboard: React.FC = () => {
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [openIncidents, setOpenIncidents] = useState<Incident[]>([]);

  const statsApi = useApi(() => api.getStatistics(), { immediate: true });
  const incidentsApi = useApi(() => api.getOpenIncidents(), { immediate: true });

  useEffect(() => {
    if (statsApi.data) setStatistics(statsApi.data);
  }, [statsApi.data]);

  useEffect(() => {
    if (incidentsApi.data) setOpenIncidents(incidentsApi.data);
  }, [incidentsApi.data]);

  const handleRefresh = () => {
    statsApi.refetch();
    incidentsApi.refetch();
  };

  // Show error if API is not available
  if ((statsApi.error || incidentsApi.error) && !statsApi.loading && !incidentsApi.loading) {
    return (
      <div className="card" style={{ textAlign: "center", padding: "var(--spacing-2xl)" }}>
        <h2>❌ Connection Error</h2>
        <p>Unable to connect to the backend API at {process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1"}</p>
        <p style={{ color: "var(--text-light)", marginTop: "var(--spacing-md)" }}>
          Make sure the backend is running. Use Docker Compose:
        </p>
        <code style={{ display: "block", backgroundColor: "var(--bg-secondary)", padding: "var(--spacing-lg)", borderRadius: "var(--border-radius)", marginTop: "var(--spacing-lg)" }}>
          docker-compose up -d
        </code>
        <button className="btn-primary mt-lg" onClick={handleRefresh}>
          🔄 Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: "var(--spacing-2xl)" }}>
        <button className="btn-primary" onClick={handleRefresh}>
          🔄 Refresh
        </button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-3" style={{ marginBottom: "var(--spacing-2xl)" }}>
        <StatCard
          title="Total Incidents"
          value={statistics?.total_incidents || 0}
          icon="📊"
          color="primary"
        />
        <StatCard
          title="Open Incidents"
          value={statistics?.open_incidents || 0}
          icon="🔴"
          color="warning"
          trend={statistics?.open_incidents ? 5 : 0}
        />
        <StatCard
          title="Critical Issues"
          value={statistics?.critical_incidents || 0}
          icon="🚨"
          color="critical"
        />
        <StatCard
          title="High Priority"
          value={statistics?.high_incidents || 0}
          icon="⚠️"
          color="danger"
        />
      </div>

      {/* Recent Open Incidents */}
      <div className="card">
        <h2 style={{ marginBottom: "var(--spacing-lg)" }}>Recent Open Incidents</h2>
        <Table<Incident>
          columns={[
            { header: "Title", accessor: "title", width: "300px" },
            { header: "Service", accessor: "service", width: "150px" },
            {
              header: "Severity",
              accessor: "severity",
              render: (value) => <Badge text={value} type={value.toLowerCase() as any} />,
            },
            {
              header: "Status",
              accessor: "status",
              render: (value) => {
                const statusType = value.toLowerCase().replace("_", "-") as any;
                return <Badge text={value} type={statusType} />;
              },
            },
            {
              header: "Logs",
              accessor: "log_count",
            },
            {
              header: "Created",
              accessor: "created_at",
              render: (value) => new Date(value).toLocaleDateString(),
            },
          ]}
          data={openIncidents.slice(0, 10)}
          loading={incidentsApi.loading}
          emptyMessage="No open incidents"
        />
      </div>
    </div>
  );
};

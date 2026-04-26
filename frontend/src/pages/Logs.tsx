/**
 * Logs viewing page
 */

import React, { useState, useEffect } from "react";
import { Table } from "../components/Table";
import { Badge } from "../components/Badge";
import api from "../services/api";
import { Log } from "../types";
import { useApi } from "../hooks/useApi";

export const Logs: React.FC = () => {
  const [logs, setLogs] = useState<Log[]>([]);
  const [filters, setFilters] = useState({
    service: "",
    level: "",
  });

  const logsApi = useApi(
    () =>
      api.getLogs(
        filters.service || undefined,
        filters.level || undefined,
        200
      ),
    { immediate: true }
  );

  useEffect(() => {
    if (logsApi.data) setLogs(logsApi.data);
  }, [logsApi.data]);

  const getServiceOptions = () => {
    const services = new Set(logs.map((log) => log.service));
    return Array.from(services).sort();
  };

  return (
    <div>
      {/* Filters */}
      <div
        className="card"
        style={{
          marginBottom: "var(--spacing-lg)",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "var(--spacing-md)",
        }}
      >
        <div>
          <label style={{ fontSize: "var(--font-size-sm)", fontWeight: 500 }}>
            Service
          </label>
          <select
            value={filters.service}
            onChange={(e) => setFilters({ ...filters, service: e.target.value })}
            style={{ width: "100%", marginTop: "var(--spacing-sm)" }}
          >
            <option value="">All Services</option>
            {getServiceOptions().map((service) => (
              <option key={service} value={service}>
                {service}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ fontSize: "var(--font-size-sm)", fontWeight: 500 }}>
            Level
          </label>
          <select
            value={filters.level}
            onChange={(e) => setFilters({ ...filters, level: e.target.value })}
            style={{ width: "100%", marginTop: "var(--spacing-sm)" }}
          >
            <option value="">All Levels</option>
            <option value="DEBUG">Debug</option>
            <option value="INFO">Info</option>
            <option value="WARNING">Warning</option>
            <option value="ERROR">Error</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>

        <div style={{ display: "flex", alignItems: "flex-end" }}>
          <button
            className="btn-secondary"
            onClick={() => logsApi.refetch()}
            style={{ width: "100%" }}
          >
            🔍 Search
          </button>
        </div>
      </div>

      {/* Logs Table */}
      <div className="card">
        <Table<Log>
          columns={[
            { header: "Service", accessor: "service", width: "150px" },
            {
              header: "Level",
              accessor: "level",
              render: (value) => {
                const levelMap: Record<string, "low" | "medium" | "high" | "critical"> = {
                  DEBUG: "low",
                  INFO: "low",
                  WARNING: "medium",
                  ERROR: "high",
                  CRITICAL: "critical",
                };
                return <Badge text={value} type={levelMap[value] || "low"} />;
              },
            },
            { header: "Message", accessor: "message", width: "400px" },
            {
              header: "Timestamp",
              accessor: "timestamp",
              render: (value) => new Date(value).toLocaleString(),
            },
          ]}
          data={logs}
          loading={logsApi.loading}
          emptyMessage="No logs found"
        />
      </div>
    </div>
  );
};

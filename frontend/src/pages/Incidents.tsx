/**
 * Incidents management page
 */

import React, { useState, useEffect } from "react";
import { Table } from "../components/Table";
import { Badge } from "../components/Badge";
import { Modal } from "../components/Modal";
import api from "../services/api";
import { Incident, IncidentStatus, SeverityLevel } from "../types";
import { useApi } from "../hooks/useApi";

export const Incidents: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [filters, setFilters] = useState({
    service: "",
    status: "",
    severity: "",
  });

  const incidentsApi = useApi(
    () =>
      api.getIncidents(
        filters.service || undefined,
        filters.status || undefined,
        filters.severity || undefined,
        100
      ),
    { immediate: true }
  );

  useEffect(() => {
    if (incidentsApi.data) setIncidents(incidentsApi.data);
  }, [incidentsApi.data]);

  const handleOpenModal = (incident: Incident) => {
    setSelectedIncident(incident);
    setIsModalOpen(true);
  };

  const handleUpdateIncident = async (
    status: IncidentStatus,
    severity: SeverityLevel
  ) => {
    if (!selectedIncident) return;

    try {
      const updated = await api.updateIncident(selectedIncident.id, {
        status,
        severity,
      });
      setIncidents((prev) =>
        prev.map((inc) => (inc.id === updated.id ? updated : inc))
      );
      setIsModalOpen(false);
      alert("Incident updated successfully!");
    } catch (error) {
      alert("Failed to update incident");
    }
  };

  const getServiceOptions = () => {
    const services = new Set(incidents.map((i) => i.service));
    return Array.from(services);
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
            Status
          </label>
          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            style={{ width: "100%", marginTop: "var(--spacing-sm)" }}
          >
            <option value="">All Status</option>
            <option value="OPEN">Open</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: "var(--font-size-sm)", fontWeight: 500 }}>
            Severity
          </label>
          <select
            value={filters.severity}
            onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
            style={{ width: "100%", marginTop: "var(--spacing-sm)" }}
          >
            <option value="">All Severity</option>
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>

        <div style={{ display: "flex", alignItems: "flex-end" }}>
          <button
            className="btn-secondary"
            onClick={() => incidentsApi.refetch()}
            style={{ width: "100%" }}
          >
            🔍 Search
          </button>
        </div>
      </div>

      {/* Incidents Table */}
      <div className="card">
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
            { header: "Logs", accessor: "log_count" },
            {
              header: "Anomaly Score",
              accessor: "anomaly_score",
              render: (value) => (value ? value.toFixed(2) : "—"),
            },
            {
              header: "Created",
              accessor: "created_at",
              render: (value) => new Date(value).toLocaleDateString(),
            },
          ]}
          data={incidents}
          loading={incidentsApi.loading}
          emptyMessage="No incidents found"
          onRowClick={handleOpenModal}
        />
      </div>

      {/* Modal for editing incident */}
      <Modal
        isOpen={isModalOpen}
        title={selectedIncident?.title || "Incident Details"}
        onClose={() => setIsModalOpen(false)}
      >
        {selectedIncident && (
          <div className="gap-lg" style={{ display: "flex", flexDirection: "column" }}>
            <div>
              <strong>Service:</strong> {selectedIncident.service}
            </div>
            <div>
              <strong>Status:</strong>{" "}
              <Badge
                text={selectedIncident.status}
                type={selectedIncident.status.toLowerCase().replace("_", "-") as any}
              />
            </div>
            <div>
              <strong>Severity:</strong>{" "}
              <Badge
                text={selectedIncident.severity}
                type={selectedIncident.severity.toLowerCase() as any}
              />
            </div>
            <div>
              <strong>Log Count:</strong> {selectedIncident.log_count}
            </div>
            {selectedIncident.anomaly_score && (
              <div>
                <strong>Anomaly Score:</strong> {selectedIncident.anomaly_score.toFixed(2)}
              </div>
            )}
            <div>
              <strong>Created:</strong>{" "}
              {new Date(selectedIncident.created_at).toLocaleString()}
            </div>

            <div style={{ borderTop: "1px solid var(--border-color)", paddingTop: "var(--spacing-lg)" }}>
              <label style={{ fontSize: "var(--font-size-sm)", fontWeight: 500, marginBottom: "var(--spacing-sm)", display: "block" }}>
                Update Status
              </label>
              <select style={{ width: "100%", marginBottom: "var(--spacing-lg)" }}>
                <option value={selectedIncident.status}>{selectedIncident.status}</option>
                {Object.values(IncidentStatus).map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>

              <label style={{ fontSize: "var(--font-size-sm)", fontWeight: 500, marginBottom: "var(--spacing-sm)", display: "block" }}>
                Update Severity
              </label>
              <select style={{ width: "100%", marginBottom: "var(--spacing-lg)" }}>
                <option value={selectedIncident.severity}>{selectedIncident.severity}</option>
                {Object.values(SeverityLevel).map((severity) => (
                  <option key={severity} value={severity}>
                    {severity}
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}
        <div
          style={{
            display: "flex",
            gap: "var(--spacing-md)",
            justifyContent: "flex-end",
          }}
        >
          <button className="btn-secondary" onClick={() => setIsModalOpen(false)}>
            Cancel
          </button>
          <button className="btn-primary" onClick={() => setIsModalOpen(false)}>
            Save Changes
          </button>
        </div>
      </Modal>
    </div>
  );
};

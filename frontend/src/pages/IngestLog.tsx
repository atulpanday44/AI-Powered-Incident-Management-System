/**
 * Log ingestion form page
 */

import React, { useState } from "react";
import api from "../services/api";
import { LogLevel } from "../types";

export const IngestLog: React.FC = () => {
  const [formData, setFormData] = useState({
    service: "",
    level: LogLevel.INFO,
    message: "",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      await api.ingestLog({
        service: formData.service,
        level: formData.level as LogLevel,
        message: formData.message,
        timestamp: new Date().toISOString(),
      });

      setMessage({
        type: "success",
        text: "Log ingested successfully! It will be processed by the system.",
      });
      setFormData({ service: "", level: LogLevel.INFO, message: "" });
    } catch (error) {
      setMessage({
        type: "error",
        text: `Failed to ingest log: ${error instanceof Error ? error.message : "Unknown error"}`,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card" style={{ maxWidth: "600px" }}>
        <h2 style={{ marginBottom: "var(--spacing-lg)" }}>Ingest New Log</h2>

        {message && (
          <div
            className={`alert alert-${message.type}`}
            style={{ marginBottom: "var(--spacing-lg)" }}
          >
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "var(--spacing-lg)" }}>
            <label style={{ display: "block", marginBottom: "var(--spacing-sm)", fontWeight: 500 }}>
              Service Name *
            </label>
            <input
              type="text"
              name="service"
              value={formData.service}
              onChange={handleInputChange}
              placeholder="e.g., auth-service"
              required
              style={{ width: "100%" }}
            />
          </div>

          <div style={{ marginBottom: "var(--spacing-lg)" }}>
            <label style={{ display: "block", marginBottom: "var(--spacing-sm)", fontWeight: 500 }}>
              Log Level *
            </label>
            <select
              name="level"
              value={formData.level}
              onChange={handleInputChange}
              style={{ width: "100%" }}
            >
              {Object.values(LogLevel).map((level) => (
                <option key={level} value={level}>
                  {level}
                </option>
              ))}
            </select>
          </div>

          <div style={{ marginBottom: "var(--spacing-lg)" }}>
            <label style={{ display: "block", marginBottom: "var(--spacing-sm)", fontWeight: 500 }}>
              Message *
            </label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleInputChange}
              placeholder="Enter log message..."
              required
              rows={6}
              style={{ width: "100%" }}
            />
          </div>

          <div style={{ display: "flex", gap: "var(--spacing-md)" }}>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Sending..." : "Send Log"}
            </button>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => setFormData({ service: "", level: LogLevel.INFO, message: "" })}
            >
              Clear
            </button>
          </div>
        </form>

        {/* Example */}
        <div
          style={{
            marginTop: "var(--spacing-2xl)",
            padding: "var(--spacing-lg)",
            backgroundColor: "var(--bg-secondary)",
            borderRadius: "var(--border-radius)",
            borderLeft: "4px solid var(--primary-color)",
          }}
        >
          <h4 style={{ marginBottom: "var(--spacing-md)" }}>Example Log</h4>
          <pre
            style={{
              margin: 0,
              fontSize: "var(--font-size-sm)",
              overflow: "auto",
              color: "var(--text-secondary)",
            }}
          >
            {JSON.stringify(
              {
                service: "payment-service",
                level: "ERROR",
                message: "Database connection timeout after 30s",
              },
              null,
              2
            )}
          </pre>
        </div>
      </div>
    </div>
  );
};

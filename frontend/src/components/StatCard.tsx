/**
 * Statistics card component
 */

import React from "react";

interface StatCardProps {
  title: string;
  value: number | string;
  icon: string;
  color?: "primary" | "success" | "warning" | "danger" | "critical";
  trend?: number;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  color = "primary",
  trend,
}) => {
  const colorMap = {
    primary: "#2563eb",
    success: "#16a34a",
    warning: "#ea580c",
    danger: "#dc2626",
    critical: "#991b1b",
  };

  const bgColorMap = {
    primary: "#dbeafe",
    success: "#dcfce7",
    warning: "#fed7aa",
    danger: "#fee2e2",
    critical: "#fee2e2",
  };

  return (
    <div className="card" style={{ borderLeft: `4px solid ${colorMap[color]}` }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div className="text-small text-muted" style={{ marginBottom: "var(--spacing-sm)" }}>
            {title}
          </div>
          <h2 style={{ fontSize: "var(--font-size-2xl)", margin: 0 }}>{value}</h2>
          {trend !== undefined && (
            <div
              className="text-small mt-sm"
              style={{
                color: trend > 0 ? "#dc2626" : "#16a34a",
              }}
            >
              {trend > 0 ? "▲" : "▼"} {Math.abs(trend)}%
            </div>
          )}
        </div>
        <div
          style={{
            fontSize: "2.5rem",
            opacity: 0.8,
          }}
        >
          {icon}
        </div>
      </div>
    </div>
  );
};

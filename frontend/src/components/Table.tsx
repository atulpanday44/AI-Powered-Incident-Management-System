/**
 * Generic table component
 */

import React from "react";

interface Column<T> {
  header: string;
  accessor: keyof T | ((row: T) => React.ReactNode);
  width?: string;
  render?: (value: any, row: T) => React.ReactNode;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
}

export function Table<T extends object>({
  columns,
  data,
  loading = false,
  emptyMessage = "No data available",
  onRowClick,
}: TableProps<T>): JSX.Element {
  if (loading) {
    return (
      <div className="card text-center" style={{ padding: "var(--spacing-2xl)" }}>
        <div className="spinner" style={{ margin: "0 auto" }}></div>
        <p className="text-muted mt-lg">Loading...</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="card text-center" style={{ padding: "var(--spacing-2xl)" }}>
        <p className="text-muted">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div style={{ overflowX: "auto" }}>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          backgroundColor: "white",
          borderRadius: "var(--border-radius-lg)",
        }}
      >
        <thead>
          <tr style={{ borderBottom: "2px solid var(--border-color)" }}>
            {columns.map((col, idx) => (
              <th
                key={idx}
                style={{
                  padding: "var(--spacing-lg)",
                  textAlign: "left",
                  fontWeight: 600,
                  fontSize: "var(--font-size-sm)",
                  textTransform: "uppercase",
                  color: "var(--text-secondary)",
                  width: col.width,
                }}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIdx) => (
            <tr
              key={rowIdx}
              onClick={() => onRowClick?.(row)}
              style={{
                borderBottom: "1px solid var(--border-color)",
                cursor: onRowClick ? "pointer" : "default",
                transition: "background-color 0.2s ease",
              }}
              onMouseEnter={(e) => {
                if (onRowClick) {
                  (e.currentTarget as HTMLTableRowElement).style.backgroundColor =
                    "var(--bg-secondary)";
                }
              }}
              onMouseLeave={(e) => {
                if (onRowClick) {
                  (e.currentTarget as HTMLTableRowElement).style.backgroundColor =
                    "transparent";
                }
              }}
            >
              {columns.map((col, colIdx) => (
                <td
                  key={colIdx}
                  style={{
                    padding: "var(--spacing-lg)",
                    fontSize: "var(--font-size-sm)",
                  }}
                >
                  {col.render
                    ? col.render(
                        typeof col.accessor === "function"
                          ? col.accessor(row)
                          : row[col.accessor],
                        row
                      )
                    : typeof col.accessor === "function"
                    ? col.accessor(row)
                    : (row[col.accessor] as React.ReactNode)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

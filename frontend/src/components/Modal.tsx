/**
 * Modal dialog component
 */

import React from "react";

interface ModalProps {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  actions?: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  title,
  onClose,
  children,
  actions,
}) => {
  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: "rgba(0, 0, 0, 0.5)",
          zIndex: 999,
        }}
      />

      {/* Modal */}
      <div
        style={{
          position: "fixed",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: "white",
          borderRadius: "var(--border-radius-lg)",
          boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
          maxWidth: "500px",
          width: "90%",
          zIndex: 1000,
          maxHeight: "90vh",
          overflowY: "auto",
        }}
      >
        <div style={{ padding: "var(--spacing-2xl)", borderBottom: "1px solid var(--border-color)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2 style={{ margin: 0 }}>{title}</h2>
            <button
              onClick={onClose}
              style={{
                background: "none",
                border: "none",
                fontSize: "1.5rem",
                cursor: "pointer",
                padding: 0,
                color: "var(--text-light)",
              }}
            >
              ×
            </button>
          </div>
        </div>

        <div style={{ padding: "var(--spacing-2xl)" }}>{children}</div>

        {actions && (
          <div
            style={{
              padding: "var(--spacing-2xl)",
              borderTop: "1px solid var(--border-color)",
              display: "flex",
              gap: "var(--spacing-md)",
              justifyContent: "flex-end",
            }}
          >
            {actions}
          </div>
        )}
      </div>
    </>
  );
};

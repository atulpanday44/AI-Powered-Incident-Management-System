/**
 * Sidebar navigation component
 */

import React from "react";
import styles from "../styles/Layout.module.css";

interface SidebarProps {
  activePage: string;
  onNavigate: (page: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activePage, onNavigate }) => {
  const menuItems = [
    { id: "dashboard", label: "Dashboard", icon: "📊" },
    { id: "incidents", label: "Incidents", icon: "🚨" },
    { id: "logs", label: "Logs", icon: "📋" },
    { id: "ingest", label: "Ingest Log", icon: "➕" },
    { id: "diagnostics", label: "Diagnostics", icon: "🔧" },
  ];

  return (
    <aside className={styles.sidebar}>
      <div className={styles.sidebarHeader}>
        <span>⚡</span>
        <span>Incident Manager</span>
      </div>
      <nav className={styles.sidebarMenu}>
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`${styles.sidebarLink} ${
              activePage === item.id ? styles.active : ""
            }`}
            onClick={() => onNavigate(item.id)}
          >
            <span className={styles.sidebarIcon}>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
};

/**
 * Header component
 */

import React from "react";
import styles from "../styles/Layout.module.css";

interface HeaderProps {
  title: string;
  actions?: React.ReactNode;
}

export const Header: React.FC<HeaderProps> = ({ title, actions }) => {
  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        <h1 className={styles.headerTitle}>{title}</h1>
        {actions && <div className={styles.headerActions}>{actions}</div>}
      </div>
    </header>
  );
};

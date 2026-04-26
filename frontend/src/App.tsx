/**
 * Main application component
 */

import React, { useState } from "react";
import "./styles/App.css";
import styles from "./styles/Layout.module.css";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { Dashboard } from "./pages/Dashboard";
import { Incidents } from "./pages/Incidents";
import { Logs } from "./pages/Logs";
import { IngestLog } from "./pages/IngestLog";

type PageType = "dashboard" | "incidents" | "logs" | "ingest";

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>("dashboard");

  const getPageTitle = (page: PageType): string => {
    const titles: Record<PageType, string> = {
      dashboard: "Dashboard",
      incidents: "Incidents",
      logs: "Logs",
      ingest: "Ingest Log",
    };
    return titles[page];
  };

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <Dashboard />;
      case "incidents":
        return <Incidents />;
      case "logs":
        return <Logs />;
      case "ingest":
        return <IngestLog />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className={styles.layout}>
      <Sidebar activePage={currentPage} onNavigate={(page) => setCurrentPage(page as PageType)} />

      <div className={styles.main}>
        <Header title={getPageTitle(currentPage)} />
        <main className={styles.content}>
          <div className={styles.contentInner}>{renderPage()}</div>
        </main>
      </div>
    </div>
  );
}

export default App;

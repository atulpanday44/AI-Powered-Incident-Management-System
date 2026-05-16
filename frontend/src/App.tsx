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
import { Diagnostics } from "./pages/Diagnostics";

type PageType = "dashboard" | "incidents" | "logs" | "ingest" | "diagnostics";

class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean }> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error) {
    console.error("Error caught by boundary:", error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: "2rem", textAlign: "center" }}>
          <h2>⚠️ Application Error</h2>
          <p>Something went wrong. Please check the console for details.</p>
          <button
            onClick={() => window.location.reload()}
            className="btn-primary"
          >
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>("dashboard");

  const getPageTitle = (page: PageType): string => {
    const titles: Record<PageType, string> = {
      dashboard: "Dashboard",
      incidents: "Incidents",
      logs: "Logs",
      ingest: "Ingest Log",
      diagnostics: "Diagnostics",
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
      case "diagnostics":
        return <Diagnostics />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <ErrorBoundary>
      <div className={styles.layout}>
        <Sidebar activePage={currentPage} onNavigate={(page) => setCurrentPage(page as PageType)} />

        <div className={styles.main}>
          <Header title={getPageTitle(currentPage)} />
          <main className={styles.content}>
            <div className={styles.contentInner}>{renderPage()}</div>
          </main>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;

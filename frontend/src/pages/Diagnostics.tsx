/**
 * Diagnostics page for testing API connectivity
 */

import React, { useState, useEffect } from "react";

export const Diagnostics: React.FC = () => {
  const [results, setResults] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const runDiagnostics = async () => {
      const testResults: Record<string, string> = {};

      // Test 1: Check environment variables
      const apiUrl = process.env.REACT_APP_API_URL;
      testResults["env_REACT_APP_API_URL"] = apiUrl || "NOT SET";

      // Test 2: Try to fetch health endpoint
      try {
        const healthUrl = `${apiUrl || "http://localhost:8000/api/v1"}/health`;
        testResults["health_url"] = healthUrl;
        
        const response = await fetch(healthUrl);
        testResults["health_status"] = `${response.status} ${response.statusText}`;
        
        if (response.ok) {
          const data = await response.json();
          testResults["health_data"] = JSON.stringify(data);
        }
      } catch (error) {
        testResults["health_error"] = String(error);
      }

      // Test 3: Try to fetch incidents
      try {
        const incidentsUrl = `${apiUrl || "http://localhost:8000/api/v1"}/incidents`;
        testResults["incidents_url"] = incidentsUrl;
        
        const response = await fetch(incidentsUrl);
        testResults["incidents_status"] = `${response.status} ${response.statusText}`;
        
        if (response.ok) {
          const data = await response.json();
          testResults["incidents_data"] = JSON.stringify(data);
        }
      } catch (error) {
        testResults["incidents_error"] = String(error);
      }

      // Test 4: Try to fetch incidents-summary
      try {
        const summaryUrl = `${apiUrl || "http://localhost:8000/api/v1"}/incidents-summary`;
        testResults["summary_url"] = summaryUrl;
        
        const response = await fetch(summaryUrl);
        testResults["summary_status"] = `${response.status} ${response.statusText}`;
        
        if (response.ok) {
          const data = await response.json();
          testResults["summary_data"] = JSON.stringify(data);
        }
      } catch (error) {
        testResults["summary_error"] = String(error);
      }

      setResults(testResults);
      setLoading(false);
    };

    runDiagnostics();
  }, []);

  if (loading) {
    return <div>Running diagnostics...</div>;
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>API Diagnostics</h1>
      <pre style={{ backgroundColor: "#f0f0f0", padding: "1rem", borderRadius: "8px", overflow: "auto" }}>
        {JSON.stringify(results, null, 2)}
      </pre>
    </div>
  );
};

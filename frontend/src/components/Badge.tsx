/**
 * Badge component for status/severity display
 */

import React from "react";

interface BadgeProps {
  text: string;
  type: "low" | "medium" | "high" | "critical" | "open" | "in-progress" | "resolved" | "closed";
}

export const Badge: React.FC<BadgeProps> = ({ text, type }) => {
  return <span className={`badge badge-${type}`}>{text}</span>;
};

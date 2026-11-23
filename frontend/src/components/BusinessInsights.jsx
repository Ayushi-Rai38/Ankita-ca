import React from "react";

function BusinessInsights({ insights }) {
  if (!insights || insights.length === 0) return null;

  return (
    <div className="section insights-section">
      <h2>💡 Business Insights</h2>
      <div className="insights-list">
        {insights.map((text, idx) => (
          <div className="insight-item" key={idx}>
            <span className="insight-text">{text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BusinessInsights;

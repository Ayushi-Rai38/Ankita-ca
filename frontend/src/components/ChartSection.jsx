import React from "react";
import { chartUrl } from "../api";

function ChartSection({ filters }) {
  // Append a cache-buster so the browser re-fetches when filters change
  const ts = JSON.stringify(filters);

  return (
    <div className="charts-section">
      {/* Monthly Trends - full width */}
      <div className="chart-card full-width">
        <h2>Monthly Order Trends</h2>
        <img src={chartUrl("monthly-trends", filters)} alt="Monthly Trends" key={"mt" + ts} />
      </div>

      {/* Two-column row */}
      <div className="charts-row">
        <div className="chart-card">
          <h2>Country-wise Product Quantity</h2>
          <img src={chartUrl("country-product-quantity", filters)} alt="Country Product Qty" key={"cpq" + ts} />
        </div>
        <div className="chart-card">
          <h2>Country-wise Customer Count</h2>
          <img src={chartUrl("country-customer-count", filters)} alt="Country Customers" key={"ccc" + ts} />
        </div>
      </div>

      {/* Two-column row */}
      <div className="charts-row">
        <div className="chart-card">
          <h2>Top 10 Customers by Quantity</h2>
          <img src={chartUrl("top-customers", filters)} alt="Top Customers" key={"tc" + ts} />
        </div>
        <div className="chart-card">
          <h2>Top 10 Products by Quantity</h2>
          <img src={chartUrl("top-products", filters)} alt="Top Products" key={"tp" + ts} />
        </div>
      </div>

      {/* Scatter - full width */}
      <div className="chart-card full-width">
        <h2>Customer Orders vs Quantity</h2>
        <img src={chartUrl("orders-vs-quantity", filters)} alt="Orders vs Qty Scatter" key={"ovq" + ts} />
      </div>
    </div>
  );
}

export default ChartSection;

import React from "react";

function Highlights({ maxOrders, maxCustomers, avgQuantity }) {
  return (
    <div className="highlights">
      <div className="highlight-card">
        <div className="highlight-icon"></div>
        <div className="highlight-info">
          <h3>Highest Product Orders</h3>
          <div className="highlight-value">
            {maxOrders?.Country || "—"}
          </div>
          <div className="highlight-sub">
            {maxOrders ? `${maxOrders.total_quantity.toLocaleString()} units` : ""}
          </div>
        </div>
      </div>

      <div className="highlight-card">
        <div className="highlight-icon"></div>
        <div className="highlight-info">
          <h3>Most Customers</h3>
          <div className="highlight-value">
            {maxCustomers?.Country || "—"}
          </div>
          <div className="highlight-sub">
            {maxCustomers ? `${maxCustomers.customer_count.toLocaleString()} customers` : ""}
          </div>
        </div>
      </div>

      <div className="highlight-card">
        <div className="highlight-icon"></div>
        <div className="highlight-info">
          <h3>Avg Quantity / Customer</h3>
          <div className="highlight-value">
            {avgQuantity !== null ? avgQuantity.toLocaleString() : "—"}
          </div>
          <div className="highlight-sub">across all customers</div>
        </div>
      </div>
    </div>
  );
}

export default Highlights;

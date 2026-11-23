import React, { useState } from "react";

const PAGE_SIZE = 15;

function CustomerTable({ customers }) {
  const [page, setPage] = useState(0);

  const totalPages = Math.ceil(customers.length / PAGE_SIZE);
  const pageData = customers.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  // Reset page if customers data changes and page is out of bounds
  if (page > 0 && page >= totalPages) {
    setPage(0);
  }

  return (
    <div className="section">
      <h2>📋 Customer-wise Order Analysis ({customers.length} customers)</h2>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Customer ID</th>
              <th>Orders</th>
              <th>Total Quantity</th>
              <th>Avg Qty / Order</th>
              <th>Revenue (£)</th>
            </tr>
          </thead>
          <tbody>
            {pageData.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: "center", padding: "20px" }}>
                  No customers found for selected filters.
                </td>
              </tr>
            ) : (
              pageData.map((row, idx) => (
                <tr key={row.CustomerID}>
                  <td>{page * PAGE_SIZE + idx + 1}</td>
                  <td>{row.CustomerID}</td>
                  <td>{row.num_orders.toLocaleString()}</td>
                  <td>{row.total_quantity.toLocaleString()}</td>
                  <td>{row.avg_quantity.toLocaleString()}</td>
                  <td>{row.total_revenue?.toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button disabled={page === 0} onClick={() => setPage(page - 1)}>
            ← Previous
          </button>
          <span>
            Page {page + 1} of {totalPages}
          </span>
          <button disabled={page >= totalPages - 1} onClick={() => setPage(page + 1)}>
            Next →
          </button>
        </div>
      )}
    </div>
  );
}

export default CustomerTable;

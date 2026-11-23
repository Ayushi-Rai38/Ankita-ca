import React from "react";

function Filters({
  filters,
  setFilters,
  countries,
  products,
  dateRange,
}) {
  const update = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const clearAll = () => {
    setFilters({ country: "", customer_id: "", start_date: "", end_date: "", product: "" });
  };

  const hasFilters = Object.values(filters).some((v) => v);

  return (
    <div className="filters-section">
      <div className="filters-header">
        <h2>🔍 Filters</h2>
        {hasFilters && (
          <button className="clear-btn" onClick={clearAll}>
            Clear All
          </button>
        )}
      </div>
      <div className="filters-row">
        <div className="filter-item">
          <label>Country</label>
          <select
            value={filters.country}
            onChange={(e) => update("country", e.target.value)}
          >
            <option value="">All Countries</option>
            {countries.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        <div className="filter-item">
          <label>Customer ID</label>
          <input
            type="text"
            placeholder="Search ID..."
            value={filters.customer_id}
            onChange={(e) => update("customer_id", e.target.value)}
          />
        </div>

        <div className="filter-item">
          <label>Start Date</label>
          <input
            type="date"
            value={filters.start_date}
            min={dateRange.min_date}
            max={dateRange.max_date}
            onChange={(e) => update("start_date", e.target.value)}
          />
        </div>

        <div className="filter-item">
          <label>End Date</label>
          <input
            type="date"
            value={filters.end_date}
            min={dateRange.min_date}
            max={dateRange.max_date}
            onChange={(e) => update("end_date", e.target.value)}
          />
        </div>

        <div className="filter-item">
          <label>Product</label>
          <select
            value={filters.product}
            onChange={(e) => update("product", e.target.value)}
          >
            <option value="">All Products</option>
            {products.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}

export default Filters;

import React, { useEffect, useState, useCallback } from "react";
import "./App.css";

import KPICards from "./components/KPICards.jsx";
import Highlights from "./components/Highlights.jsx";
import Filters from "./components/Filters.jsx";
import ChartSection from "./components/ChartSection.jsx";
import CustomerTable from "./components/CustomerTable.jsx";
import BusinessInsights from "./components/BusinessInsights.jsx";

import {
  fetchKPIs,
  fetchCustomerOrders,
  fetchAvgQuantity,
  fetchMaxOrdersCountry,
  fetchMaxCustomersCountry,
  fetchInsights,
  fetchCountryList,
  fetchProductList,
  fetchDateRange,
} from "./api";

function App() {
  // Filter state
  const [filters, setFilters] = useState({
    country: "",
    customer_id: "",
    start_date: "",
    end_date: "",
    product: "",
  });

  // Dropdown options (loaded once)
  const [countries, setCountries] = useState([]);
  const [products, setProducts] = useState([]);
  const [dateRange, setDateRange] = useState({ min_date: "", max_date: "" });

  // Dashboard data (updated on filter change)
  const [kpis, setKpis] = useState(null);
  const [customers, setCustomers] = useState([]);
  const [maxOrders, setMaxOrders] = useState(null);
  const [maxCustomers, setMaxCustomers] = useState(null);
  const [avgQuantity, setAvgQuantity] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load dropdown options once
  useEffect(() => {
    Promise.all([fetchCountryList(), fetchProductList(), fetchDateRange()])
      .then(([c, p, d]) => {
        setCountries(c);
        setProducts(p);
        setDateRange(d);
      })
      .catch((err) => console.error("Error loading options:", err));
  }, []);

  // Reload all data when filters change
  const loadData = useCallback(async () => {
    try {
      const [kpiData, avgData, maxOrd, maxCust, custData, insightData] =
        await Promise.all([
          fetchKPIs(filters),
          fetchAvgQuantity(filters),
          fetchMaxOrdersCountry(filters),
          fetchMaxCustomersCountry(filters),
          fetchCustomerOrders(filters),
          fetchInsights(filters),
        ]);

      setKpis(kpiData);
      setAvgQuantity(avgData.avg_quantity_per_customer);
      setMaxOrders(maxOrd);
      setMaxCustomers(maxCust);
      setCustomers(custData);
      setInsights(insightData);
    } catch (err) {
      console.error("Error loading data:", err);
    }
    setLoading(false);
  }, [filters]);

  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(loadData, 400);
    return () => clearTimeout(timer);
  }, [loadData]);

  if (loading && !kpis) {
    return (
      <div className="app">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>E-commerce Data Analytics Dashboard</h1>
        <p>Online Retail Dataset — Insights & Analysis powered by Python</p>
      </header>

      {/* Filters */}
      <Filters
        filters={filters}
        setFilters={setFilters}
        countries={countries}
        products={products}
        dateRange={dateRange}
      />

      {/* KPI Cards */}
      <KPICards kpis={kpis} />

      {/* Key Highlights */}
      <Highlights
        maxOrders={maxOrders}
        maxCustomers={maxCustomers}
        avgQuantity={avgQuantity}
      />

      {/* Charts */}
      <ChartSection filters={filters} />

      {/* Business Insights */}
      <BusinessInsights insights={insights} />

      {/* Customer Table */}
      <CustomerTable customers={customers} />

      {/* Footer */}
      <footer className="footer">
        Built with React.js, FastAPI, Pandas, NumPy, Matplotlib & Seaborn
      </footer>
    </div>
  );
}

export default App;

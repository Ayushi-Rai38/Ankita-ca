const BASE_URL = "http://localhost:8000";

// ── Build query string from filter object ──
function buildQuery(filters = {}) {
  const params = [];
  if (filters.country) params.push(`country=${encodeURIComponent(filters.country)}`);
  if (filters.customer_id) params.push(`customer_id=${encodeURIComponent(filters.customer_id)}`);
  if (filters.start_date) params.push(`start_date=${encodeURIComponent(filters.start_date)}`);
  if (filters.end_date) params.push(`end_date=${encodeURIComponent(filters.end_date)}`);
  if (filters.product) params.push(`product=${encodeURIComponent(filters.product)}`);
  return params.length ? `?${params.join("&")}` : "";
}

// ── JSON data fetchers ──
export async function fetchKPIs(filters) {
  const res = await fetch(`${BASE_URL}/api/kpis${buildQuery(filters)}`);
  return res.json();
}

export async function fetchCustomerOrders(filters) {
  const res = await fetch(`${BASE_URL}/api/customers/orders${buildQuery(filters)}`);
  return res.json();
}

export async function fetchAvgQuantity(filters) {
  const res = await fetch(`${BASE_URL}/api/customers/avg-quantity${buildQuery(filters)}`);
  return res.json();
}

export async function fetchMaxOrdersCountry(filters) {
  const res = await fetch(`${BASE_URL}/api/countries/max-orders${buildQuery(filters)}`);
  return res.json();
}

export async function fetchMaxCustomersCountry(filters) {
  const res = await fetch(`${BASE_URL}/api/countries/max-customers${buildQuery(filters)}`);
  return res.json();
}

export async function fetchInsights(filters) {
  const res = await fetch(`${BASE_URL}/api/insights${buildQuery(filters)}`);
  return res.json();
}

export async function fetchCountryList() {
  const res = await fetch(`${BASE_URL}/api/countries`);
  return res.json();
}

export async function fetchProductList() {
  const res = await fetch(`${BASE_URL}/api/products`);
  return res.json();
}

export async function fetchDateRange() {
  const res = await fetch(`${BASE_URL}/api/date-range`);
  return res.json();
}

// ── Chart image URL builder ──
export function chartUrl(chartName, filters) {
  return `${BASE_URL}/api/charts/${chartName}${buildQuery(filters)}`;
}

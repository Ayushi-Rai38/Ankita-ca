
const BASE_URL = "https://ecommerce-backend-jqq4.onrender.com";

// Build query string from filter object
function buildQuery(filters = {}) {
  const params = new URLSearchParams();

  if (filters.country) params.set("country", filters.country);
  if (filters.customer_id) params.set("customer_id", filters.customer_id);
  if (filters.start_date) params.set("start_date", filters.start_date);
  if (filters.end_date) params.set("end_date", filters.end_date);
  if (filters.product) params.set("product", filters.product);

  const query = params.toString();
  return query ? `?${query}` : "";
}

// Common request handler
async function apiFetch(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `API error ${response.status}: ${errorText || response.statusText}`
    );
  }

  return response.json();
}

// JSON data fetchers
export async function fetchKPIs(filters) {
  return apiFetch(`/api/kpis${buildQuery(filters)}`);
}

export async function fetchCustomerOrders(filters) {
  return apiFetch(`/api/customers/orders${buildQuery(filters)}`);
}

export async function fetchAvgQuantity(filters) {
  return apiFetch(`/api/customers/avg-quantity${buildQuery(filters)}`);
}

export async function fetchMaxOrdersCountry(filters) {
  return apiFetch(`/api/countries/max-orders${buildQuery(filters)}`);
}

export async function fetchMaxCustomersCountry(filters) {
  return apiFetch(`/api/countries/max-customers${buildQuery(filters)}`);
}

export async function fetchInsights(filters) {
  return apiFetch(`/api/insights${buildQuery(filters)}`);
}

export async function fetchCountryList() {
  return apiFetch("/api/countries");
}

export async function fetchProductList() {
  return apiFetch("/api/products");
}

export async function fetchDateRange() {
  return apiFetch("/api/date-range");
}

// Chart image URL builder
export function chartUrl(chartName, filters) {
  return `${BASE_URL}/api/charts/${chartName}${buildQuery(filters)}`;
}

"""
data_processing.py
-------------------
Loads the Online Retail CSV dataset, cleans it, and provides
helper functions used by the FastAPI routes.
All filtering is centralised in filter_dataframe().
"""

import os
import pandas as pd
import numpy as np

# --------------- Load & Clean ---------------

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.csv")


def load_and_clean_data() -> pd.DataFrame:
    """Read the CSV and perform basic cleaning."""
    df = pd.read_csv(
        DATA_PATH,
        encoding="ISO-8859-1",
        dtype={"CustomerID": str, "InvoiceNo": str},
    )

    # 1. Drop rows where CustomerID is missing
    df = df.dropna(subset=["CustomerID"])

    # 2. Remove cancelled orders (InvoiceNo starts with 'C')
    df = df[~df["InvoiceNo"].str.startswith("C")]

    # 3. Keep only rows with positive Quantity and UnitPrice
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # 4. Strip extra whitespace from text columns
    df["Description"] = df["Description"].fillna("").str.strip()
    df["Country"] = df["Country"].str.strip()

    # 5. Convert CustomerID to clean integer-string (remove ".0")
    df["CustomerID"] = df["CustomerID"].str.replace(r"\.0$", "", regex=True)

    # 6. Parse InvoiceDate
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="mixed", dayfirst=False)

    # 7. Add Revenue column
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    df = df.reset_index(drop=True)
    return df


# Cache the cleaned dataframe so it's loaded only once
_df: pd.DataFrame = load_and_clean_data()


def get_dataframe() -> pd.DataFrame:
    """Return the cached cleaned dataframe."""
    return _df


# --------------- Central Filter Helper ---------------

def filter_dataframe(
    country: str | None = None,
    customer_id: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    product: str | None = None,
) -> pd.DataFrame:
    """Apply all slicer filters to the dataframe and return the filtered copy."""
    df = get_dataframe()

    if country:
        df = df[df["Country"].str.lower() == country.lower()]
    if customer_id:
        df = df[df["CustomerID"].str.contains(customer_id, case=False, na=False)]
    if start_date:
        df = df[df["InvoiceDate"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["InvoiceDate"] <= pd.to_datetime(end_date)]
    if product:
        df = df[df["Description"].str.contains(product, case=False, na=False)]

    return df


# --------------- Dropdown option lists ---------------

def get_country_list() -> list[str]:
    return sorted(get_dataframe()["Country"].unique().tolist())


def get_product_list() -> list[str]:
    """Return top 200 products by frequency for the dropdown."""
    df = get_dataframe()
    top = df["Description"].value_counts().head(200).index.tolist()
    return sorted([p for p in top if p])


def get_date_range() -> dict:
    df = get_dataframe()
    return {
        "min_date": str(df["InvoiceDate"].min().date()),
        "max_date": str(df["InvoiceDate"].max().date()),
    }


# --------------- KPI helpers ---------------

def get_kpis(df: pd.DataFrame | None = None) -> dict:
    if df is None:
        df = get_dataframe()
    return {
        "total_orders": int(df["InvoiceNo"].nunique()),
        "total_customers": int(df["CustomerID"].nunique()),
        "total_quantity": int(df["Quantity"].sum()),
        "total_countries": int(df["Country"].nunique()),
        "total_revenue": round(float(df["Revenue"].sum()), 2),
        "total_products": int(df["Description"].nunique()),
    }


# --------------- Customer-wise Order Analysis ---------------

def customer_order_analysis(df: pd.DataFrame | None = None) -> list[dict]:
    if df is None:
        df = get_dataframe()

    if df.empty:
        return []

    grouped = df.groupby("CustomerID").agg(
        num_orders=("InvoiceNo", "nunique"),
        total_quantity=("Quantity", "sum"),
        total_revenue=("Revenue", "sum"),
    ).reset_index()

    grouped["avg_quantity"] = (grouped["total_quantity"] / grouped["num_orders"]).round(2)
    grouped["total_revenue"] = grouped["total_revenue"].round(2)
    grouped = grouped.sort_values("total_quantity", ascending=False)

    return grouped.to_dict(orient="records")


# --------------- Country-wise Product Analysis ---------------

def country_product_analysis(df: pd.DataFrame | None = None) -> list[dict]:
    if df is None:
        df = get_dataframe()

    if df.empty:
        return []

    grouped = df.groupby("Country").agg(
        total_quantity=("Quantity", "sum"),
    ).reset_index()

    grouped = grouped.sort_values("total_quantity", ascending=False)
    return grouped.to_dict(orient="records")


def country_with_max_orders(df: pd.DataFrame | None = None) -> dict:
    data = country_product_analysis(df)
    return data[0] if data else {}


# --------------- Average Quantity per Customer ---------------

def avg_quantity_per_customer(df: pd.DataFrame | None = None) -> float:
    if df is None:
        df = get_dataframe()
    if df.empty:
        return 0.0
    per_customer = df.groupby("CustomerID")["Quantity"].sum()
    return round(float(per_customer.mean()), 2)


# --------------- Country-wise Customer Analysis ---------------

def country_customer_analysis(df: pd.DataFrame | None = None) -> list[dict]:
    if df is None:
        df = get_dataframe()

    if df.empty:
        return []

    grouped = df.groupby("Country").agg(
        customer_count=("CustomerID", "nunique"),
    ).reset_index()

    grouped = grouped.sort_values("customer_count", ascending=False)
    return grouped.to_dict(orient="records")


def country_with_max_customers(df: pd.DataFrame | None = None) -> dict:
    data = country_customer_analysis(df)
    return data[0] if data else {}


# --------------- Monthly Order Trends ---------------

def monthly_order_trends(df: pd.DataFrame | None = None) -> list[dict]:
    if df is None:
        df = get_dataframe()
    if df.empty:
        return []

    df = df.copy()
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    grouped = df.groupby("YearMonth").agg(
        order_count=("InvoiceNo", "nunique"),
        total_quantity=("Quantity", "sum"),
        total_revenue=("Revenue", "sum"),
    ).reset_index().sort_values("YearMonth")

    grouped["total_revenue"] = grouped["total_revenue"].round(2)
    return grouped.to_dict(orient="records")


# --------------- Top Products ---------------

def top_products(df: pd.DataFrame | None = None, n: int = 10) -> list[dict]:
    if df is None:
        df = get_dataframe()
    if df.empty:
        return []

    grouped = df.groupby("Description").agg(
        total_quantity=("Quantity", "sum"),
    ).reset_index()

    grouped = grouped.sort_values("total_quantity", ascending=False).head(n)
    return grouped.to_dict(orient="records")


# --------------- Business Insights (auto-generated) ---------------

def generate_insights(df: pd.DataFrame | None = None) -> list[str]:
    """Generate a list of key findings from the filtered data."""
    if df is None:
        df = get_dataframe()
    if df.empty:
        return ["No data available for the selected filters."]

    insights = []

    # 1. Top country
    country_data = country_product_analysis(df)
    if country_data:
        top_c = country_data[0]
        insights.append(
            f" {top_c['Country']} leads with {top_c['total_quantity']:,} units ordered, "
            f"accounting for {top_c['total_quantity'] / df['Quantity'].sum() * 100:.1f}% of total quantity."
        )

    # 2. Top customer
    cust_data = customer_order_analysis(df)
    if cust_data:
        top_cust = cust_data[0]
        insights.append(
            f"Customer {top_cust['CustomerID']} is the top buyer with "
            f"{top_cust['total_quantity']:,} units across {top_cust['num_orders']} orders."
        )

    # 3. Average order size
    avg_qty = avg_quantity_per_customer(df)
    insights.append(f" On average, each customer ordered {avg_qty:,.2f} units in total.")

    # 4. Revenue insight
    total_rev = df["Revenue"].sum()
    avg_rev_per_order = total_rev / df["InvoiceNo"].nunique() if df["InvoiceNo"].nunique() > 0 else 0
    insights.append(f" Total revenue is £{total_rev:,.2f} with an average of £{avg_rev_per_order:,.2f} per order.")

    # 5. Product variety
    n_products = df["Description"].nunique()
    top_prod = df.groupby("Description")["Quantity"].sum().idxmax()
    insights.append(f" {n_products:,} unique products sold. Most popular: \"{top_prod}\".")

    # 6. Busiest month
    monthly = monthly_order_trends(df)
    if monthly:
        busiest = max(monthly, key=lambda x: x["order_count"])
        insights.append(
            f" Busiest month: {busiest['YearMonth']} with {busiest['order_count']:,} orders "
            f"and {busiest['total_quantity']:,} units."
        )

    # 7. Customer concentration
    if len(cust_data) >= 10:
        top10_qty = sum(c["total_quantity"] for c in cust_data[:10])
        total_qty = df["Quantity"].sum()
        insights.append(
            f" Top 10 customers account for {top10_qty / total_qty * 100:.1f}% of all quantity ordered."
        )

    return insights

"""
main.py
--------
FastAPI application exposing analytics APIs and chart images.
All endpoints accept optional filter query params that are applied
consistently via data_processing.filter_dataframe().
"""
from chart_generator import CHART_LOCK
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

import data_processing as dp
import chart_generator as cg

app = FastAPI(title="E-commerce Data Analytics API")



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ecommerce-analyticss-dashboard.netlify.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ── Helper: extract common filter params ──
def _get_filtered_df(
    country: str | None = None,
    customer_id: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    product: str | None = None,
):
    return dp.filter_dataframe(country, customer_id, start_date, end_date, product)


# ══════════════════════════════════════════════
#  DROPDOWN OPTIONS
# ══════════════════════════════════════════════

@app.get("/api/countries")
def country_list():
    return dp.get_country_list()

@app.get("/api/products")
def product_list():
    return dp.get_product_list()

@app.get("/api/date-range")
def date_range():
    return dp.get_date_range()


# ══════════════════════════════════════════════
#  JSON DATA ENDPOINTS (all filterable)
# ══════════════════════════════════════════════

@app.get("/api/kpis")
def kpis(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.get_kpis(df)


@app.get("/api/customers/orders")
def customer_orders(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.customer_order_analysis(df)


@app.get("/api/customers/avg-quantity")
def avg_quantity(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return {"avg_quantity_per_customer": dp.avg_quantity_per_customer(df)}


@app.get("/api/countries/products")
def country_products(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.country_product_analysis(df)


@app.get("/api/countries/max-orders")
def max_orders_country(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.country_with_max_orders(df)


@app.get("/api/countries/customers")
def country_customers(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.country_customer_analysis(df)


@app.get("/api/countries/max-customers")
def max_customers_country(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.country_with_max_customers(df)


@app.get("/api/insights")
def insights(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return dp.generate_insights(df)


# ══════════════════════════════════════════════
#  CHART IMAGE ENDPOINTS (all filterable)
# ══════════════════════════════════════════════

@app.get("/api/charts/country-product-quantity")
def chart_country_product_quantity(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return Response(content=cg.country_product_quantity_chart(df), media_type="image/png")


@app.get("/api/charts/country-customer-count")
def chart_country_customer_count(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return Response(content=cg.country_customer_count_chart(df), media_type="image/png")


@app.get("/api/charts/top-customers")
def chart_top_customers(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return Response(content=cg.top_customers_chart(df), media_type="image/png")


@app.get("/api/charts/orders-vs-quantity")
def chart_orders_vs_quantity(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return Response(content=cg.orders_vs_quantity_scatter(df), media_type="image/png")


@app.get("/api/charts/monthly-trends")
def chart_monthly_trends(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return Response(content=cg.monthly_trends_chart(df), media_type="image/png")


@app.get("/api/charts/top-products")
def chart_top_products(
    country: str = Query(default=None),
    customer_id: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    product: str = Query(default=None),
):
    df = _get_filtered_df(country, customer_id, start_date, end_date, product)
    return Response(content=cg.top_products_chart(df), media_type="image/png")

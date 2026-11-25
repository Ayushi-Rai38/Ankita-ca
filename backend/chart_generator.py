"""
chart_generator.py
-------------------
Generates chart images using Matplotlib and Seaborn.
All charts accept a filtered DataFrame so they respond to dashboard slicers.
"""

import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import threading
import data_processing as dp
CHART_LOCK = threading.Lock()

# ── Global style ──
sns.set_theme(style="whitegrid", font_scale=1.1)
PALETTE_BLUE = ["#4e79a7", "#59a14f", "#9c755f", "#f28e2b", "#e15759",
                "#76b7b2", "#ff9da7", "#edc948", "#b07aa1", "#bab0ac",
                "#af7aa1", "#aec7e8", "#ffbb78", "#98df8a", "#c5b0d5"]
PALETTE_WARM = sns.color_palette("YlOrRd_r", 15)
BG_COLOR = "#fafafa"


def _fig_to_bytes(fig) -> bytes:
    """Convert a Matplotlib figure to PNG bytes and close it."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def _style_ax(ax, title, xlabel="", ylabel=""):
    """Apply consistent styling to an axis."""
    ax.set_title(title, fontsize=15, fontweight="bold", pad=12, color="#333")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color="#555")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color="#555")
    ax.tick_params(colors="#555", labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ══════════════════════════════════════════════
#  1. Country-wise Product Quantity
# ══════════════════════════════════════════════
def country_product_quantity_chart(df: pd.DataFrame | None = None) -> bytes:
    data = dp.country_product_analysis(df)
    chart_df = pd.DataFrame(data).head(15)

    if chart_df.empty:
        return _empty_chart("No country data for selected filters")

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars = ax.barh(chart_df["Country"], chart_df["total_quantity"],
                   color=PALETTE_BLUE[:len(chart_df)], edgecolor="white", height=0.65)
    ax.invert_yaxis()
    _style_ax(ax, "Country-wise Product Quantity (Top 15)", "Total Quantity Ordered")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K" if x >= 1000 else f"{x:.0f}"))

    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(chart_df["total_quantity"]) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{int(w):,}", va="center", fontsize=9, color="#444")

    fig.tight_layout()
    return _fig_to_bytes(fig)


# ══════════════════════════════════════════════
#  2. Country-wise Customer Count
# ══════════════════════════════════════════════
def country_customer_count_chart(df: pd.DataFrame | None = None) -> bytes:
    data = dp.country_customer_analysis(df)
    chart_df = pd.DataFrame(data).head(15)

    if chart_df.empty:
        return _empty_chart("No customer data for selected filters")

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars = ax.barh(chart_df["Country"], chart_df["customer_count"],
                   color=PALETTE_WARM[:len(chart_df)], edgecolor="white", height=0.65)
    ax.invert_yaxis()
    _style_ax(ax, "Country-wise Customer Count (Top 15)", "Number of Distinct Customers")

    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(chart_df["customer_count"]) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{int(w):,}", va="center", fontsize=9, color="#444")

    fig.tight_layout()
    return _fig_to_bytes(fig)


# ══════════════════════════════════════════════
#  3. Top 10 Customers by Total Quantity
# ══════════════════════════════════════════════
def top_customers_chart(df: pd.DataFrame | None = None) -> bytes:
    data = dp.customer_order_analysis(df)
    chart_df = pd.DataFrame(data).head(10)

    if chart_df.empty:
        return _empty_chart("No customer data for selected filters")

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    colors = sns.color_palette("coolwarm", len(chart_df))
    bars = ax.bar(chart_df["CustomerID"].astype(str), chart_df["total_quantity"],
                  color=colors, edgecolor="white", width=0.6)
    _style_ax(ax, "Top 10 Customers by Total Quantity", "Customer ID", "Total Quantity")
    plt.xticks(rotation=40, ha="right")

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + max(chart_df["total_quantity"]) * 0.01,
                f"{int(h):,}", ha="center", va="bottom", fontsize=9, color="#444")

    fig.tight_layout()
    return _fig_to_bytes(fig)


# ══════════════════════════════════════════════
#  4. Customer Orders vs Quantity (Scatter)
# ══════════════════════════════════════════════
def orders_vs_quantity_scatter(df: pd.DataFrame | None = None) -> bytes:
    data = dp.customer_order_analysis(df)
    chart_df = pd.DataFrame(data)

    if chart_df.empty:
        return _empty_chart("No data for selected filters")

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.scatter(chart_df["num_orders"], chart_df["total_quantity"],
               alpha=0.55, s=40, c="#4e79a7", edgecolors="white", linewidths=0.4)
    _style_ax(ax, "Customer Orders vs Quantity (Scatter)", "Number of Orders", "Total Quantity Ordered")

    fig.tight_layout()
    return _fig_to_bytes(fig)


# ══════════════════════════════════════════════
#  5. Monthly Order Trends (Line Chart) — NEW
# ══════════════════════════════════════════════
def monthly_trends_chart(df: pd.DataFrame | None = None) -> bytes:
    data = dp.monthly_order_trends(df)
    chart_df = pd.DataFrame(data)

    if chart_df.empty:
        return _empty_chart("No monthly data for selected filters")

    fig, ax1 = plt.subplots(figsize=(14, 6))
    fig.set_facecolor(BG_COLOR)
    ax1.set_facecolor(BG_COLOR)

    # Bar for quantity
    ax1.bar(chart_df["YearMonth"], chart_df["total_quantity"],
            color="#4e79a7", alpha=0.6, label="Quantity", width=0.5)
    ax1.set_ylabel("Total Quantity", fontsize=11, color="#4e79a7")
    ax1.tick_params(axis="y", labelcolor="#4e79a7")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))

    # Line for order count on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(chart_df["YearMonth"], chart_df["order_count"],
             color="#e15759", marker="o", linewidth=2.5, markersize=6, label="Orders")
    ax2.set_ylabel("Number of Orders", fontsize=11, color="#e15759")
    ax2.tick_params(axis="y", labelcolor="#e15759")
    ax2.spines["top"].set_visible(False)

    _style_ax(ax1, "Monthly Order Trends")
    plt.xticks(rotation=45, ha="right", fontsize=9)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10)

    fig.tight_layout()
    return _fig_to_bytes(fig)


# ══════════════════════════════════════════════
#  6. Top 10 Products (Bar Chart) — NEW
# ══════════════════════════════════════════════
def top_products_chart(df: pd.DataFrame | None = None) -> bytes:
    data = dp.top_products(df, n=10)
    chart_df = pd.DataFrame(data)

    if chart_df.empty:
        return _empty_chart("No product data for selected filters")

    # Truncate long product names
    chart_df["short_name"] = chart_df["Description"].str[:35]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars = ax.barh(chart_df["short_name"], chart_df["total_quantity"],
                   color=sns.color_palette("viridis", len(chart_df)), edgecolor="white", height=0.65)
    ax.invert_yaxis()
    _style_ax(ax, "Top 10 Products by Quantity Sold", "Total Quantity")

    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(chart_df["total_quantity"]) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{int(w):,}", va="center", fontsize=9, color="#444")

    fig.tight_layout()
    return _fig_to_bytes(fig)


# ══════════════════════════════════════════════
#  Empty chart placeholder
# ══════════════════════════════════════════════
def _empty_chart(message: str) -> bytes:
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.text(0.5, 0.5, message, ha="center", va="center",
            fontsize=14, color="#999", transform=ax.transAxes)
    ax.axis("off")
    return _fig_to_bytes(fig)

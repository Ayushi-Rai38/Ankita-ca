# E-commerce Data Analytics Dashboard

A full-stack analytics project built with **React.js** (frontend) and **FastAPI + Python** (backend) that analyzes the [Online Retail Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset) from Kaggle.

All data analysis, calculations, and chart generation are performed in **Python** using Pandas, NumPy, Matplotlib, and Seaborn. The React frontend only displays the results and chart images received from the backend.

---

## Project Structure

```
Traffic_ankita/
├── backend/
│   ├── main.py                # FastAPI application (API routes)
│   ├── data_processing.py     # Data loading, cleaning & analytics (Pandas, NumPy)
│   ├── chart_generator.py     # Chart generation (Matplotlib, Seaborn)
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Python virtual environment
├── frontend/
│   ├── index.html             # HTML entry point
│   ├── vite.config.js         # Vite configuration
│   ├── package.json           # Node dependencies
│   ├── .npmrc                 # npm config
│   └── src/
│       ├── components/
│       │   ├── KPICards.jsx        # KPI metric cards
│       │   ├── Highlights.jsx      # Key insight cards
│       │   ├── ChartSection.jsx    # Displays Python-generated charts
│       │   └── CustomerTable.jsx   # Customer order analysis table
│       ├── api.js              # API helper functions
│       ├── App.jsx             # Main dashboard component
│       ├── App.css             # Styles
│       └── index.jsx           # React entry point
├── data/
│   └── data.csv                # Kaggle Online Retail Dataset
└── README.md
```

---

## Tech Stack

| Layer            | Technology                     |
| ---------------- | ------------------------------ |
| Frontend         | React.js, JavaScript, HTML/CSS |
| Bundler          | Vite                           |
| Backend          | Python, FastAPI                |
| Data Analysis    | Pandas, NumPy                  |
| Visualization    | Matplotlib, Seaborn            |

---

## Features

### Dashboard
- **KPI Cards** – Total Orders, Total Customers, Total Quantity, Total Countries
- **Key Highlights** – Country with max orders, country with most customers, average quantity per customer

### Charts (Generated in Python)
All charts are created using **Matplotlib** and **Seaborn** in the backend and served as PNG images:
1. Country-wise Product Quantity (Top 15) – Horizontal Bar Chart
2. Country-wise Customer Count (Top 15) – Horizontal Bar Chart
3. Top 10 Customers by Quantity – Vertical Bar Chart
4. Customer Orders vs Quantity – Scatter Plot

### Customer Analysis Table
- Paginated table showing CustomerID, number of orders, total quantity, and average quantity per order
- **Search** by Customer ID
- **Filter** by Country

---

## Analytics Performed

1. **Customer-wise Order Analysis** – Number of orders and total quantity per customer
2. **Country-wise Product Analysis** – Total product quantity by country; identifies the country with maximum orders
3. **Average Quantity Analysis** – Average quantity ordered per customer
4. **Country-wise Customer Analysis** – Distinct customer count per country; identifies the country with the highest customer count

---

## Setup & Running Instructions

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** and **npm** installed

### Step 1: Start the Backend

```bash
# Open a terminal and navigate to the backend folder
cd backend

# Create virtual environment (only needed the first time)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install Python dependencies (only needed the first time)
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**.  
You can explore the API docs at **http://localhost:8000/docs**.

### Step 2: Start the Frontend

```bash
# Open another terminal and navigate to the frontend folder
cd frontend

# Install Node dependencies (only needed the first time)
npm install

# Start the Vite development server
npm run dev
```

The dashboard will open at **http://localhost:3000**.

---

## API Endpoints

| Endpoint                              | Method | Description                              |
| ------------------------------------- | ------ | ---------------------------------------- |
| `/api/kpis`                           | GET    | High-level KPI numbers                   |
| `/api/customers/orders`               | GET    | Customer-wise order analysis (`?search=` and `?country=`) |
| `/api/customers/avg-quantity`          | GET    | Average quantity per customer             |
| `/api/countries/products`             | GET    | Country-wise product quantity             |
| `/api/countries/customers`            | GET    | Country-wise customer count               |
| `/api/countries/max-orders`           | GET    | Country with maximum product orders       |
| `/api/countries/max-customers`        | GET    | Country with highest customer count       |
| `/api/countries`                      | GET    | List of all countries                     |
| `/api/charts/country-product-quantity` | GET   | PNG chart – country product quantity      |
| `/api/charts/country-customer-count`  | GET    | PNG chart – country customer count        |
| `/api/charts/top-customers`           | GET    | PNG chart – top 10 customers              |
| `/api/charts/orders-vs-quantity`      | GET    | PNG chart – orders vs quantity scatter    |

---

## Data Cleaning Steps

1. Removed rows with missing `CustomerID`
2. Removed cancelled orders (InvoiceNo starting with 'C')
3. Kept only rows with positive `Quantity` and `UnitPrice`
4. Stripped whitespace from text columns
5. Parsed `InvoiceDate` to datetime format

---

## Author

Built as a college project for B.Tech CSE – Data Analytics.

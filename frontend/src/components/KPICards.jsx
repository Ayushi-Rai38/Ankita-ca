import React from "react";

function KPICards({ kpis }) {
  if (!kpis) return null;

  const cards = [
    { label: "Total Orders",    value: kpis.total_orders,     },
    { label: "Total Customers", value: kpis.total_customers,  },
    { label: "Total Quantity",  value: kpis.total_quantity,   },
    { label: "Total Revenue",   value: `£${kpis.total_revenue?.toLocaleString()}`,  },
    { label: "Products",        value: kpis.total_products,  },
    { label: "Countries",       value: kpis.total_countries,  },
  ];

  return (
    <div className="kpi-container">
      {cards.map((card) => (
        <div className="kpi-card" key={card.label}>
          <div className="kpi-icon">{card.icon}</div>
          <div>
            <h3>{card.label}</h3>
            <div className="kpi-value">
              {typeof card.value === "number"
                ? card.value.toLocaleString()
                : card.value}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default KPICards;

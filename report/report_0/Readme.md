Superstore Analysis — Modular Version

An end-to-end data analysis of the Superstore retail dataset (2015–2018) 
using a **modular Python architecture**.

---

 Project Objective

Answer 5 core business questions:
1. Sales trend & seasonality
2. Category & sub-category performance
3. Regional performance (multi-metric: sales, profit, margin)
4. Discount impact on profitability
5. Customer segment contribution

Plus 6 bonus exercises on shipping, loss orders, top products, 
segments, quarters, and correlations.

---
Project Architecture

The project follows a **modular design** where each module has a 
single responsibility:

---

 Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `data_loader` | Read Excel, convert dates |
| `data_cleaning` | Remove duplicates, filter invalid values |
| `feature_engineering` | Year, Month, Quarter, Shipping Days |
| `eda` | Monthly/Category/Region/Segment summaries |
| `visualization` | 5 charts + consolidated dashboard |
| `practice` | 6 bonus exercises |

The **notebooks only orchestrate** these modules — no business logic 
inside them.

---

 Key Findings

1. **Seasonality** — Sales peak annually in Q4 (Shahrivar–Azar)
2. **Technology** leads in profit; **Furniture** has very low margin
3. **West & East** together drive over 60% of revenue
4. **Discounts above 20%** destroy profitability (optimal ~10%)
5. **Consumer** segment = ~50% of sales, but creates concentration risk

---

Bonus Exercises

1. **Average Shipping Time** — computed and visualized
2. **Loss-Making Orders** — analyzed by category & region
3. **Top 5 Sub-Categories** — ranked by sales
4. **Segment Share** — pie chart with percentages
5. **Quarterly Analysis** — Q1–Q4 comparison
6. **Correlation Matrix** — heatmap of numeric variables

---

## 🛠 Tools & Libraries

| Tool | Purpose |
|------|---------|
| Python 3.13 | Programming language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Base plotting |
| Seaborn | Statistical charts |
| Jupyter | Interactive environment |

---

 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt

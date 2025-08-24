
##
Analyze customer sales data from an SQLite3 database and provide two solutions:
1. **Pure SQL Query**
2. **Python (Pandas)**

The objective is to find **total quantities of each item purchased by customers aged 18–35**, while:
- Treating `NULL` quantities as `0`
- Excluding items with total quantity = `0`
- Ensuring results are integers (no decimals)

---

## Files in this Repository
- `solution_assignment.py` → Main script (runs both SQL and Pandas solutions, outputs CSVs).
- `output_sql.csv` → Result generated using SQL query.
- `output_pandas.csv` → Result generated using Pandas.
- `README.md` → Instructions and documentation.

---

## How to Run
Make sure you have **Python 3.x** and the required packages:
```bash
pip install pandas

import sys
import sqlite3
import pandas as pd

def solve_sql(db_path: str) -> pd.DataFrame:
    query = """
    SELECT
      c.customer_id AS Customer,
      c.age AS Age,
      i.item_name AS Item,
      CAST(SUM(COALESCE(o.quantity, 0)) AS INTEGER) AS Quantity
    FROM customers c
    JOIN sales s ON c.customer_id = s.customer_id
    JOIN orders o ON s.sales_id = o.sales_id
    JOIN items i ON o.item_id = i.item_id
    WHERE c.age BETWEEN 18 AND 35
    GROUP BY c.customer_id, c.age, i.item_name
    HAVING Quantity > 0
    ORDER BY Customer, Item;
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(query, conn)

def solve_pandas(db_path: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        customers = pd.read_sql("SELECT * FROM customers;", conn)
        items = pd.read_sql("SELECT * FROM items;", conn)
        sales = pd.read_sql("SELECT * FROM sales;", conn)
        orders = pd.read_sql("SELECT * FROM orders;", conn)

   
    cust = customers[(customers["age"] >= 18) & (customers["age"] <= 35)]


    merged = (sales.merge(orders, on="sales_id")
                   .merge(cust, on="customer_id")
                   .merge(items, on="item_id"))


    merged["quantity"] = merged["quantity"].fillna(0)


    grouped = (merged.groupby(["customer_id", "age", "item_name"])["quantity"]
                     .sum()
                     .astype(int)
                     .reset_index())


    filtered = grouped[grouped["quantity"] > 0]


    return (filtered.rename(columns={
        "customer_id": "Customer",
        "age": "Age",
        "item_name": "Item",
        "quantity": "Quantity"
    }).sort_values(["Customer", "Item"]))

def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else "Data Engineer_ETL Assignment.db"
    out_sql = sys.argv[2] if len(sys.argv) > 2 else "output_sql.csv"
    out_pd = sys.argv[3] if len(sys.argv) > 3 else "output_pandas.csv"


    df_sql = solve_sql(db_path)
    df_sql.to_csv(out_sql, index=False, sep=';')


    df_pd = solve_pandas(db_path)
    df_pd.to_csv(out_pd, index=False, sep=';')

    print(f"Wrote SQL output to: {out_sql}")
    print(f"Wrote Pandas output to: {out_pd}")

if __name__ == "__main__":
    main()

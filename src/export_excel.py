import pandas as pd
import sqlite3
import os

# Rutas de directorios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'ecommerce.db')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Asegurar que existe el directorio de reportes
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_excel_report():
    print("Conectando a la base de datos...")
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Consulta SQL: Ventas por País
    query_country = """
    SELECT 
        c.country, 
        COUNT(DISTINCT s.transaction_id) as total_orders,
        SUM(s.quantity) as total_items_sold,
        SUM(s.revenue) as total_revenue
    FROM fact_sales s
    JOIN dim_customers c ON s.customer_id = c.customer_id
    GROUP BY c.country
    ORDER BY total_revenue DESC;
    """
    df_country = pd.read_sql_query(query_country, conn)
    
    # 2. Consulta SQL: Ventas por Categoría de Producto
    query_category = """
    SELECT 
        p.category, 
        SUM(s.quantity) as total_items_sold,
        SUM(s.revenue) as total_revenue
    FROM fact_sales s
    JOIN dim_products p ON s.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC;
    """
    df_category = pd.read_sql_query(query_category, conn)
    
    # 3. Consulta SQL: Top 10 Clientes
    query_top_customers = """
    SELECT 
        c.name,
        c.email,
        SUM(s.revenue) as total_spent
    FROM fact_sales s
    JOIN dim_customers c ON s.customer_id = c.customer_id
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 10;
    """
    df_top_customers = pd.read_sql_query(query_top_customers, conn)
    
    conn.close()
    
    # Escribir en Excel con múltiples hojas
    report_path = os.path.join(REPORTS_DIR, 'Executive_Report.xlsx')
    print(f"Generando reporte Excel en {report_path}...")
    
    # Usando el motor openpyxl (instalado en requirements)
    with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
        df_country.to_excel(writer, sheet_name='Sales by Country', index=False)
        df_category.to_excel(writer, sheet_name='Sales by Category', index=False)
        df_top_customers.to_excel(writer, sheet_name='Top 10 Customers', index=False)
        
    print("¡Reporte generado exitosamente!")

if __name__ == "__main__":
    generate_excel_report()

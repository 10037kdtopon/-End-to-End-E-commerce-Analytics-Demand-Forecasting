import pandas as pd
import sqlite3
import os

# Rutas de directorios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DB_DIR = os.path.join(BASE_DIR, 'database')

# Asegurar que existan los directorios
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, 'ecommerce.db')

def extract():
    """Extrae datos de los archivos CSV"""
    print("Iniciando extracción (ETL - Extract)...")
    customers = pd.read_csv(os.path.join(RAW_DATA_DIR, 'customers.csv'))
    products = pd.read_csv(os.path.join(RAW_DATA_DIR, 'products.csv'))
    sales = pd.read_csv(os.path.join(RAW_DATA_DIR, 'sales.csv'))
    return customers, products, sales

def transform(customers, products, sales):
    """Limpia y transforma los datos"""
    print("Iniciando transformación (ETL - Transform)...")
    
    # Asegurar tipos de datos correctos
    customers['signup_date'] = pd.to_datetime(customers['signup_date'])
    sales['transaction_date'] = pd.to_datetime(sales['transaction_date'])
    
    # Validar nulos y eliminarlos si existen (en nuestro dataset sintético no hay, pero es buena práctica)
    customers = customers.dropna()
    products = products.dropna()
    sales = sales.dropna()
    
    # Calcular Revenue Total por venta (Precio * Cantidad * (1 - Descuento))
    # Para ello, necesitamos hacer un merge temporal
    sales_merged = sales.merge(products[['product_id', 'price']], on='product_id', how='left')
    sales['revenue'] = sales_merged['price'] * sales_merged['quantity'] * (1 - sales_merged['discount_applied'])
    
    # Guardar datos transformados como parquet o csv limpio (opcional, pero útil)
    customers.to_csv(os.path.join(PROCESSED_DATA_DIR, 'clean_customers.csv'), index=False)
    products.to_csv(os.path.join(PROCESSED_DATA_DIR, 'clean_products.csv'), index=False)
    sales.to_csv(os.path.join(PROCESSED_DATA_DIR, 'clean_sales.csv'), index=False)
    
    return customers, products, sales

def load(customers, products, sales):
    """Carga los datos en la base de datos SQLite"""
    print("Iniciando carga a BD (ETL - Load)...")
    conn = sqlite3.connect(DB_PATH)
    
    # Guardar en SQLite
    customers.to_sql('dim_customers', conn, if_exists='replace', index=False)
    products.to_sql('dim_products', conn, if_exists='replace', index=False)
    sales.to_sql('fact_sales', conn, if_exists='replace', index=False)
    
    print(f"Datos cargados exitosamente en la base de datos: {DB_PATH}")
    
    # Ejemplo de prueba: Imprimir cuántas filas tiene la tabla de ventas
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fact_sales")
    count = cursor.fetchone()[0]
    print(f"Total de registros en fact_sales: {count}")
    
    conn.close()

if __name__ == "__main__":
    # Ejecutar Pipeline ETL
    df_customers, df_products, df_sales = extract()
    df_customers_clean, df_products_clean, df_sales_clean = transform(df_customers, df_products, df_sales)
    load(df_customers_clean, df_products_clean, df_sales_clean)
    print("¡Proceso ETL finalizado con éxito!")

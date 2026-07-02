import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

# Definir la ruta donde se guardarán los datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# Asegurar que la carpeta existe
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Parámetros de generación
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 50
NUM_TRANSACTIONS = 5000

# Semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generate_customers():
    print("Generando clientes...")
    countries = ['USA', 'Canada', 'Mexico', 'Spain', 'Colombia', 'Argentina', 'Chile']
    
    customers = pd.DataFrame({
        'customer_id': range(1, NUM_CUSTOMERS + 1),
        'name': [f"Customer_{i}" for i in range(1, NUM_CUSTOMERS + 1)],
        'email': [f"customer{i}@example.com" for i in range(1, NUM_CUSTOMERS + 1)],
        'country': np.random.choice(countries, NUM_CUSTOMERS, p=[0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
        'signup_date': [datetime(2022, 1, 1) + timedelta(days=np.random.randint(0, 365*2)) for _ in range(NUM_CUSTOMERS)],
        'is_premium': np.random.choice([True, False], NUM_CUSTOMERS, p=[0.2, 0.8])
    })
    
    # Formatear la fecha
    customers['signup_date'] = customers['signup_date'].dt.strftime('%Y-%m-%d')
    customers.to_csv(os.path.join(RAW_DATA_DIR, 'customers.csv'), index=False)
    print("customers.csv generado exitosamente.")
    return customers

def generate_products():
    print("Generando productos...")
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
    
    products = pd.DataFrame({
        'product_id': range(1, NUM_PRODUCTS + 1),
        'product_name': [f"Product_{i}" for i in range(1, NUM_PRODUCTS + 1)],
        'category': np.random.choice(categories, NUM_PRODUCTS),
        'price': np.round(np.random.uniform(10.0, 500.0, NUM_PRODUCTS), 2)
    })
    
    # Añadir un costo (margen de beneficio aleatorio)
    products['cost'] = np.round(products['price'] * np.random.uniform(0.4, 0.8, NUM_PRODUCTS), 2)
    
    products.to_csv(os.path.join(RAW_DATA_DIR, 'products.csv'), index=False)
    print("products.csv generado exitosamente.")
    return products

def generate_transactions(customers_df, products_df):
    print("Generando transacciones de ventas...")
    
    # Rango de fechas para las ventas (últimos 2 años)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    transactions = pd.DataFrame({
        'transaction_id': range(10001, 10001 + NUM_TRANSACTIONS),
        'customer_id': np.random.choice(customers_df['customer_id'], NUM_TRANSACTIONS),
        'product_id': np.random.choice(products_df['product_id'], NUM_TRANSACTIONS),
        'quantity': np.random.randint(1, 6, NUM_TRANSACTIONS),
        # Generar fechas aleatorias con una ligera tendencia de aumento los fines de semana (opcional, aquí mantenemos simple)
        'transaction_date': [start_date + timedelta(days=np.random.randint(0, 730), hours=np.random.randint(0, 24)) for _ in range(NUM_TRANSACTIONS)],
        # Algunos descuentos aleatorios
        'discount_applied': np.random.choice([0.0, 0.10, 0.20, 0.30], NUM_TRANSACTIONS, p=[0.7, 0.15, 0.1, 0.05])
    })
    
    # Ordenar por fecha
    transactions = transactions.sort_values(by='transaction_date')
    transactions['transaction_date'] = transactions['transaction_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    transactions.to_csv(os.path.join(RAW_DATA_DIR, 'sales.csv'), index=False)
    print("sales.csv generado exitosamente.")

if __name__ == "__main__":
    print(f"Iniciando generación de datos en: {RAW_DATA_DIR}")
    c_df = generate_customers()
    p_df = generate_products()
    generate_transactions(c_df, p_df)
    print("¡Generación de datos completada exitosamente!")

import pandas as pd
import sqlite3
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'ecommerce.db')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(MODELS_DIR, exist_ok=True)

def train_segmentation_model():
    print("Conectando a BD para Análisis RFM...")
    conn = sqlite3.connect(DB_PATH)
    
    # Extraer datos para calcular RFM (Recency, Frequency, Monetary)
    query = """
    SELECT 
        c.customer_id,
        MAX(s.transaction_date) as last_purchase_date,
        COUNT(s.transaction_id) as frequency,
        SUM(s.revenue) as monetary
    FROM dim_customers c
    JOIN fact_sales s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id
    """
    
    df_rfm = pd.read_sql_query(query, conn)
    
    # Calcular Recency (días desde la última compra hasta hoy)
    # Convertir a datetime
    df_rfm['last_purchase_date'] = pd.to_datetime(df_rfm['last_purchase_date'])
    max_date = df_rfm['last_purchase_date'].max()
    df_rfm['recency'] = (max_date - df_rfm['last_purchase_date']).dt.days
    
    # Preparar datos para Machine Learning
    X = df_rfm[['recency', 'frequency', 'monetary']]
    
    # Escalar datos (importante para K-Means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("Entrenando modelo de Machine Learning (K-Means)...")
    # Agrupar en 4 clusters
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_rfm['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Asignar nombres a los clusters basados en su valor promedio
    # Esto es una simplificación, generalmente se analiza cada cluster para ponerle nombre
    cluster_means = df_rfm.groupby('cluster')['monetary'].mean().sort_values()
    
    # Mapeo simple: 0: Low Value, 1: Mid Value, 2: High Value, 3: VIP
    # Como los índices de cluster_means están ordenados por gasto promedio, podemos mapearlos
    labels = ['Lost/Low Value', 'At Risk', 'Loyal', 'VIP/Champions']
    cluster_mapping = {cluster_id: label for cluster_id, label in zip(cluster_means.index, labels)}
    df_rfm['segment'] = df_rfm['cluster'].map(cluster_mapping)
    
    # Guardar resultados en la base de datos
    df_rfm[['customer_id', 'recency', 'frequency', 'monetary', 'segment']].to_sql('customer_segments', conn, if_exists='replace', index=False)
    
    conn.close()
    
    # Guardar el modelo y el scaler
    model_path = os.path.join(MODELS_DIR, 'kmeans_rfm.pkl')
    scaler_path = os.path.join(MODELS_DIR, 'scaler_rfm.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(kmeans, f)
        
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"Modelo guardado en: {model_path}")
    print("Segmentación de clientes completada y guardada en la base de datos.")

if __name__ == "__main__":
    train_segmentation_model()

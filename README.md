# 🚀 End-to-End E-commerce Analytics & Demand Forecasting

Este es un proyecto completo de Ciencia de Datos y Business Intelligence diseñado para simular el ciclo de vida de los datos en una empresa de e-commerce. Abarca desde la generación sintética de datos hasta el despliegue de un Dashboard interactivo, incluyendo ETL, Machine Learning y reportería.

## 🌟 Características Destacadas
- **Procesamiento ETL (Extract, Transform, Load)**: Extracción de datos de CSVs, limpieza y transformación usando `Pandas`, y carga en una base de datos relacional `SQLite`.
- **Análisis SQL**: Consultas optimizadas para extraer KPIs (Key Performance Indicators) de negocio.
- **Automatización de Excel**: Generación de reportes ejecutivos multi-hoja utilizando `openpyxl`.
- **Machine Learning**: Modelo no supervisado (K-Means Clustering) implementado con `scikit-learn` para Segmentación de Clientes basado en análisis RFM (Recency, Frequency, Monetary value).
- **Business Intelligence**: Dashboard interactivo y atractivo construido con `Streamlit` y `Plotly` para presentar los datos a los stakeholders.

## 📁 Estructura del Proyecto

```text
Ecommerce_Analytics_Portfolio/
│
├── app/
│   └── dashboard.py         # Dashboard interactivo en Streamlit
├── data/
│   ├── raw/                 # Datos originales (generados por script)
│   └── processed/           # Datos limpios y transformados
├── database/
│   └── ecommerce.db         # Base de datos SQLite
├── models/
│   └── ...                  # Modelos de Machine Learning guardados (.pkl)
├── reports/
│   └── Executive_Report.xlsx # Reporte generado automáticamente
├── src/
│   ├── generate_data.py     # Script para generar datos sintéticos
│   ├── etl.py               # Pipeline ETL
│   ├── ml_model.py          # Entrenamiento del modelo de ML
│   └── export_excel.py      # Generador de reportes Excel
└── requirements.txt         # Dependencias del proyecto
```

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.10+
- **Librerías de Datos:** Pandas, NumPy
- **Base de Datos:** SQLite3
- **Machine Learning:** Scikit-Learn
- **Visualización y BI:** Streamlit, Plotly
- **Exportación:** Openpyxl

## 🚀 Cómo Ejecutar el Proyecto Localmente

1. **Clonar el repositorio y configurar el entorno:**
   ```bash
   git clone <tu-repo-url>
   cd Ecommerce_Analytics_Portfolio
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Generar los datos iniciales:**
   ```bash
   python src/generate_data.py
   ```

3. **Ejecutar el Pipeline ETL:**
   ```bash
   python src/etl.py
   ```

4. **Entrenar el modelo de Segmentación de Clientes (ML):**
   ```bash
   python src/ml_model.py
   ```

5. **Generar el Reporte de Excel Ejecutivo:**
   ```bash
   python src/export_excel.py
   ```

6. **Levantar el Dashboard de Business Intelligence:**
   ```bash
   streamlit run app/dashboard.py
   ```

## 📊 Muestra de Resultados


<img width="1913" height="897" alt="image" src="https://github.com/user-attachments/assets/5f34ed84-51ce-4ff2-a4ec-ca5403bb4de9" />

📈 Resultados (Basados en los gráficos)

Análisis de Categorías: Se identificó que la categoría de Electrónica (o la categoría más alta en tu gráfico) representa el mayor porcentaje de los ingresos totales, demostrando ser el pilar financiero del negocio.
Tendencias Mensuales: El gráfico de línea evidenció picos de ventas en ciertos meses (como a final de año), lo que permite al equipo de inventario prepararse mejor para la alta demanda estacional.
Segmentación de Usuarios (IA): El modelo logró clasificar exitosamente la base de datos en 4 grupos clave, logrando separar con precisión a los clientes de alto valor (VIP) de aquellos que llevan meses sin comprar (At Risk).


<img width="1918" height="941" alt="image" src="https://github.com/user-attachments/assets/acaf6cc2-a925-4077-b601-67cd272b0ce4" />


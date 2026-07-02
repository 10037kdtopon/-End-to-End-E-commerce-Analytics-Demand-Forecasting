import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="E-Commerce Analytics", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'ecommerce.db')

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    sales_query = """
    SELECT 
        s.transaction_date, 
        s.revenue, 
        p.category, 
        c.country 
    FROM fact_sales s
    JOIN dim_products p ON s.product_id = p.product_id
    JOIN dim_customers c ON s.customer_id = c.customer_id
    """
    df_sales = pd.read_sql_query(sales_query, conn)
    df_sales['transaction_date'] = pd.to_datetime(df_sales['transaction_date'])
    
    try:
        segments_query = "SELECT * FROM customer_segments"
        df_segments = pd.read_sql_query(segments_query, conn)
    except Exception:
        df_segments = pd.DataFrame() 
        
    conn.close()
    return df_sales, df_segments

def apply_custom_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;900&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Ocultar elementos de Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Fondo animado oscuro premium */
    .stApp {
        background: linear-gradient(-45deg, #09090b, #1c1917, #172554, #09090b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism extremo para métricas */
    div[data-testid="metric-container"] {
        background: rgba(25, 30, 40, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(56, 189, 248, 0.2) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        background: rgba(25, 30, 40, 0.6) !important;
    }

    /* Texto principal métricas */
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="metric-container"] div {
        color: #f8fafc !important;
    }
    
    /* Título principal neón */
    h1.neon-title {
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8, #38bdf8);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 0rem !important;
        padding-bottom: 0rem !important;
        animation: shine 3s linear infinite;
        background-size: 200% auto;
    }
    
    @keyframes shine {
      to { background-position: 200% center; }
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Headers de secciones */
    h2, h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def style_plotly_fig(fig):
    """Elimina el fondo blanco y aplica colores premium a los gráficos"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente externo
        plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente interno
        font=dict(color='#ffffff', family='Outfit, sans-serif'),    # Texto blanco y fuente moderna
        hoverlabel=dict(bgcolor="rgba(15, 23, 42, 0.9)", font_size=14, bordercolor="rgba(255,255,255,0.2)"),
        margin=dict(t=50, l=10, r=20, b=80)  # Aumenté el margen inferior (b=80) para que no se corten las letras
    )
    # Grillas sutiles para no distraer
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    return fig

def main():
    apply_custom_theme()

    st.markdown("<h1 class='neon-title'>🚀 AI-Powered E-Commerce Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Real-time Business Intelligence & Customer Segmentation</p>", unsafe_allow_html=True)

    df_sales, df_segments = load_data()

    if df_sales.empty:
        st.warning("No hay datos disponibles. Ejecuta el pipeline ETL primero.")
        return

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    total_revenue = df_sales['revenue'].sum()
    total_orders = len(df_sales)
    
    col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("📦 Total Orders", f"{total_orders:,}")
    col3.metric("🎯 Avg Order Value", f"${total_revenue/total_orders if total_orders else 0:,.2f}")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- Gráficos de Ventas ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        category_revenue = df_sales.groupby('category')['revenue'].sum().reset_index()
        # Paleta de colores neón brillante
        color_discrete_sequence = ['#38bdf8', '#818cf8', '#c084fc', '#fb7185', '#2dd4bf']
        
        fig_cat = px.bar(category_revenue, x='category', y='revenue', color='category', 
                         title="Revenue by Product Category", 
                         color_discrete_sequence=color_discrete_sequence)
        fig_cat = style_plotly_fig(fig_cat)
        st.plotly_chart(fig_cat, use_container_width=True, theme=None)

    with col_chart2:
        df_sales_monthly = df_sales.set_index('transaction_date').resample('M')['revenue'].sum().reset_index()
        fig_time = px.line(df_sales_monthly, x='transaction_date', y='revenue', 
                           title="Monthly Revenue Trend", markers=True)
        # Darle estilo neón a la línea
        fig_time.update_traces(line_color='#38bdf8', line_width=4, marker=dict(size=8, color='#c084fc'))
        fig_time = style_plotly_fig(fig_time)
        st.plotly_chart(fig_time, use_container_width=True, theme=None)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Segmentación de Clientes (ML) ---
    st.markdown("### 🧠 Machine Learning: Customer Segmentation (RFM)")
    if not df_segments.empty:
        col_seg1, col_seg2 = st.columns(2)
        
        # Paleta de colores para segmentos
        segment_colors = {'VIP/Champions': '#2dd4bf', 'Loyal': '#38bdf8', 'At Risk': '#fb7185', 'Lost/Low Value': '#94a3b8'}
        
        with col_seg1:
            segment_counts = df_segments['segment'].value_counts().reset_index()
            segment_counts.columns = ['segment', 'count']
            fig_pie = px.pie(segment_counts, names='segment', values='count', 
                             title="Customer Distribution by Segment", hole=0.6,
                             color='segment', color_discrete_map=segment_colors)
            fig_pie = style_plotly_fig(fig_pie)
            # Quitar grillas del pie chart por seguridad aunque plotly lo hace solo
            fig_pie.update_layout(showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True, theme=None)
            
        with col_seg2:
            fig_scatter = px.scatter(df_segments, x='recency', y='monetary', color='segment', 
                                     title="Recency vs Monetary Value",
                                     labels={'recency': 'Recency (Days)', 'monetary': 'Monetary Value ($)'},
                                     color_discrete_map=segment_colors)
            
            # Hacer los puntos un poco más grandes y semi transparentes
            fig_scatter.update_traces(marker=dict(size=10, opacity=0.8, line=dict(width=1, color='white')))
            fig_scatter = style_plotly_fig(fig_scatter)
            st.plotly_chart(fig_scatter, use_container_width=True, theme=None)
    else:
        st.info("Ejecuta el script de Machine Learning (ml_model.py) para ver la segmentación de clientes.")

if __name__ == "__main__":
    main()

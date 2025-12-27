import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="EraPhone Intelligence Suite",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CSS - BACKGROUND PUTIH, TEXT GELAP ====================
st.markdown("""
<style>
    /* BACKGROUND PUTIH untuk semua */
    .main {
        background-color: white !important;
    }
    
    .stApp {
        background-color: white !important;
    }
    
    .block-container {
        background-color: white !important;
        padding-top: 1rem !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header dengan background merah */
    .header-container {
        background: linear-gradient(135deg, #E30613 0%, #B71C1C 100%);
        color: white;
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(227, 6, 19, 0.2);
    }
    
    /* Section headers - TEXT GELAP */
    .section-header {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: #111111 !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 3px solid #E30613 !important;
    }
    
    /* Modern header styling */
    .modern-header {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #111111 !important;
        margin: 2.5rem 0 1.2rem 0 !important;
        padding-bottom: 0.8rem !important;
        border-bottom: 2px solid #E30613 !important;
        position: relative !important;
    }
    
    .modern-header:after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #E30613, #FF6B6B);
    }
    
    /* Elegant card shadows */
    .elegant-card {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid rgba(227, 6, 19, 0.1) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    .elegant-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.12) !important;
    }
    
    /* Card styling - BACKGROUND PUTIH, TEXT GELAP */
    .metric-card {
        background: white !important;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
        margin-bottom: 0.8rem;
        color: #111111 !important;
    }
    
    /* Styling untuk semua teks di dashboard */
    .stMarkdown, .stMetric, .stDataFrame, .stText {
        color: #111111 !important;
    }
    
    /* Table styling - BACKGROUND PUTIH, TEXT GELAP */
    .dataframe {
        background: white !important;
        color: #111111 !important;
    }
    
    .dataframe th {
        background: #f8f9fa !important;
        color: #111111 !important;
        font-weight: 600;
    }
    
    .dataframe td {
        background: white !important;
        color: #222222 !important;
        border-bottom: 1px solid #e0e0e0 !important;
    }
    
    /* Metric value styling */
    [data-testid="stMetricValue"] {
        color: #111111 !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #444444 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa !important;
        border-radius: 10px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        color: #333333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #E30613 !important;
        color: white !important;
        border-color: #E30613 !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #E30613 !important;
        color: white !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white !important;
        color: #111111 !important;
        border: 1px solid #dee2e6 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNGSI UTILITAS ====================
def format_currency(value):
    """Format nilai mata uang dengan satuan yang sesuai"""
    if pd.isna(value):
        return "Rp 0"
    
    value = float(value)
    if value >= 1_000_000_000:
        return f"Rp {value/1_000_000_000:,.2f} M"
    elif value >= 1_000_000:
        return f"Rp {value/1_000_000:,.1f} Jt"
    elif value >= 1_000:
        return f"Rp {value/1_000:,.0f} K"
    else:
        return f"Rp {value:,.0f}"

def create_product_bar_chart(products_df, title, color):
    """Membuat bar chart untuk produk"""
    if products_df.empty or len(products_df) == 0:
        return None
    
    # Ambil top 10 produk
    top_products = products_df.head(10).copy()
    
    # Buat nama pendek untuk label
    top_products['short_name'] = top_products['nama_barang'].apply(
        lambda x: (x[:20] + "...") if len(x) > 20 else x
    )
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top_products['short_name'],
        y=top_products['total_value'],
        name='Revenue',
        marker_color=color,
        text=top_products['total_value'].apply(lambda x: format_currency(x)),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Revenue: Rp %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'🏆 {title} - Top 10 Products',
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111111', size=12),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(color='#333333'),
            title_font=dict(color='#333333')
        ),
        yaxis=dict(
            title="Revenue (Rp)",
            tickformat=',.0f',
            tickfont=dict(color='#333333'),
            title_font=dict(color='#333333'),
            gridcolor='rgba(0,0,0,0.05)'
        ),
        margin=dict(t=50, b=100, l=80, r=40)
    )
    
    return fig

def create_revenue_pie_chart(products_df, title):
    """Membuat pie chart yang lebih compact untuk dashboard"""
    if products_df.empty or len(products_df) == 0:
        return None
    
    # Ambil maksimal 5 item untuk readability
    if len(products_df) > 5:
        display_df = products_df.head(4).copy()
        other_revenue = products_df.iloc[4:]['total_value'].sum()
        other_row = pd.DataFrame({
            'nama_barang': ['Other'],
            'total_value': [other_revenue],
            'revenue_pct': [100 - display_df['revenue_pct'].sum() if 'revenue_pct' in display_df.columns else 0]
        })
        display_df = pd.concat([display_df, other_row], ignore_index=True)
    else:
        display_df = products_df.copy()
    
    # Buat label sangat pendek
    display_df['short_name'] = display_df['nama_barang'].apply(
        lambda x: x[:10] + "..." if len(x) > 10 else x
    )
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=display_df['short_name'],
        values=display_df['total_value'],
        textinfo='percent',  # HANYA PERSENTASE di chart
        textposition='inside',
        textfont=dict(color='white', size=9, family='Arial'),
        hovertemplate='<b>%{full_label}</b><br>Revenue: Rp %{value:,.0f}<br>Share: %{percent}<extra></extra>',
        marker=dict(colors=['#E30613', '#FF6B6B', '#FF9800', '#4CAF50', '#2196F3'][:len(display_df)]),
        hole=0.5,  # DONUT CHART - lebih hemat space
        rotation=90
    ))
    
    # Custom data untuk hover
    full_labels = display_df['nama_barang'].tolist()
    for i, trace in enumerate(fig.data):
        trace.customdata = [[full_labels[i]] for i in range(len(full_labels))]
        trace.hovertemplate = '<b>%{customdata[0]}</b><br>Revenue: Rp %{value:,.0f}<br>Share: %{percent}<extra></extra>'
    
    fig.update_layout(
        title={
            'text': f'{title} Revenue',
            'font': {'size': 14, 'color': '#111111', 'family': 'Arial'},
            'y': 0.95
        },
        height=350,  # LEBIH PENDEK! (dari 500)
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111111', size=9, family='Arial'),
        margin=dict(t=40, b=10, l=10, r=10),  # MARGIN SANGAT KECIL
        showlegend=True,
        legend=dict(
            font=dict(color='#333333', size=8),
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,  # LEGEND DI LUAR
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#CCCCCC',
            borderwidth=1
        ),
        uniformtext=dict(
            minsize=8,
            mode='hide'
        )
    )
    
    return fig

def create_forecast_chart(history_df, forecast_df):
    """Membuat chart forecasting yang sudah DIPERBAIKI"""
    
    fig = go.Figure()
    
    # ===== 1. PLOT HISTORY DATA =====
    if not history_df.empty and 'revenue' in history_df.columns:
        try:
            # Cari kolom tanggal yang benar
            date_col_history = None
            for col in ['date', 'tanggal_order', 'tanggal', 'ds']:
                if col in history_df.columns:
                    date_col_history = col
                    break
            
            if date_col_history:
                # Konversi tanggal
                history_df[date_col_history] = pd.to_datetime(history_df[date_col_history])
                history_df = history_df.sort_values(date_col_history)
                
                # Plot garis history
                fig.add_trace(go.Scatter(
                    x=history_df[date_col_history],
                    y=history_df['revenue'],
                    name='Actual Revenue',
                    mode='lines+markers',
                    line=dict(color='#E30613', width=4),
                    marker=dict(size=8, color='#E30613'),
                    hovertemplate='<b>%{x|%b %Y}</b><br>Actual: Rp %{y:,.0f}<extra></extra>'
                ))
                
                # Plot moving average jika ada
                if 'ma_3' in history_df.columns:
                    ma_data = history_df[~history_df['ma_3'].isna()]
                    if not ma_data.empty:
                        fig.add_trace(go.Scatter(
                            x=ma_data[date_col_history],
                            y=ma_data['ma_3'],
                            name='3-Month MA',
                            mode='lines',
                            line=dict(color='#FF6B6B', width=2.5, dash='dot'),
                            opacity=0.8
                        ))
                        
        except Exception as e:
            st.sidebar.warning(f"History plot error: {str(e)[:50]}")
    
    # ===== 2. PLOT FORECAST DATA =====
    if not forecast_df.empty and 'forecast_revenue' in forecast_df.columns:
        try:
            # Cari kolom tanggal yang benar
            date_col_forecast = None
            for col in ['date', 'tanggal', 'ds']:
                if col in forecast_df.columns:
                    date_col_forecast = col
                    break
            
            if date_col_forecast:
                # Konversi tanggal
                forecast_df[date_col_forecast] = pd.to_datetime(forecast_df[date_col_forecast])
                forecast_df = forecast_df.sort_values(date_col_forecast)
                
                # Plot confidence interval jika ada
                if 'lower_ci' in forecast_df.columns and 'upper_ci' in forecast_df.columns:
                    # Buat area confidence interval
                    x_ci = pd.concat([forecast_df[date_col_forecast], forecast_df[date_col_forecast][::-1]])
                    y_ci = pd.concat([forecast_df['upper_ci'], forecast_df['lower_ci'][::-1]])
                    
                    fig.add_trace(go.Scatter(
                        x=x_ci,
                        y=y_ci,
                        fill='toself',
                        fillcolor='rgba(78, 205, 196, 0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='95% Confidence Interval',
                        hoverinfo='skip',
                        showlegend=True
                    ))
                
                # Plot garis forecast
                fig.add_trace(go.Scatter(
                    x=forecast_df[date_col_forecast],
                    y=forecast_df['forecast_revenue'],
                    name='Revenue Forecast',
                    mode='lines+markers',
                    line=dict(color='#4ECDC4', width=4, dash='dash'),
                    marker=dict(
                        size=10, 
                        color='#4ECDC4', 
                        symbol='diamond',
                        line=dict(width=1, color='white')
                    ),
                    hovertemplate='<b>%{x|%b %Y}</b><br>Forecast: Rp %{y:,.0f}<extra></extra>'
                ))
                
        except Exception as e:
            st.sidebar.warning(f"Forecast plot error: {str(e)[:50]}")
    
    # ===== 3. KONFIGURASI GRAFIK =====
    fig.update_layout(
        title={
            'text': '📈 Revenue Trend Analysis & Forecast',
            'font': {'size': 24, 'color': '#111111', 'family': 'Arial, sans-serif'},
            'y': 0.95
        },
        height=550,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#333333', size=12, family='Segoe UI, Arial'),
        xaxis=dict(
            title='',
            tickfont=dict(color='#555555', size=11),
            gridcolor='rgba(0,0,0,0.07)',
            showgrid=True,
            tickformat='%b %Y',
            tickangle=0
        ),
        yaxis=dict(
            title='Revenue (Rupiah)',
            tickformat=',.0f',
            tickfont=dict(color='#555555', size=11),
            title_font=dict(color='#555555', size=13),
            gridcolor='rgba(0,0,0,0.07)',
            zerolinecolor='rgba(0,0,0,0.1)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#333333', size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        hovermode='x unified',
        margin=dict(t=80, b=80, l=80, r=40)
    )
    
    return fig

# ==================== LOAD DATA - VERSI DIPERBAIKI ====================
@st.cache_data
def load_data():
    """Load dan proses data - VERSI SIMPLIFIED"""
    try:
        data = {}
        
        # ===== 1. LOAD SEMUA FILE DENGAN TRY-EXCEPT =====
        file_mapping = {
            'transactions': 'df_analysis.csv',
            'top_products': 'produk_kelas_A.csv',
            'mid_products': 'produk_kelas_B.csv', 
            'low_products': 'produk_kelas_C.csv',
            'bundles': 'decision_bundling.csv',
            'cross_sell': 'decision_cross_selling.csv',
            'priority_actions': 'decision_priority_action.csv',  # ✅ TAMBAH INI
            'sales_history': 'time_series_revenue_actual.csv',
            'sales_forecast': 'time_series_revenue_forecast.csv'
        }
        
        for key, filename in file_mapping.items():
            try:
                df = pd.read_csv(filename)
                data[key] = df
                print(f"✓ Success: {filename} ({len(df)} rows)")
            except Exception as e:
                print(f"✗ Failed: {filename} - {str(e)[:50]}")
                data[key] = pd.DataFrame()  # DataFrame kosong
        
        return data
        
    except Exception as e:
        st.error(f"Fatal error loading data: {str(e)[:100]}")
        return {key: pd.DataFrame() for key in file_mapping.keys()}

# ==================== HEADER & BRANDING ERAPHONE ====================
# ==================== HEADER & BRANDING ERAPHONE ====================
st.markdown("""
<div class="header-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
        <div>
            <h1 style="margin:0; font-size:2.8rem; font-weight:800; color: white; letter-spacing: -0.5px;">EraPhone Intelligence</h1>
            <p style="margin:0.5rem 0 0 0; font-size:1.3rem; color: rgba(255,255,255,0.95); font-weight:300;">
                Advanced Business Intelligence Dashboard
            </p>
            <div style="display: flex; gap: 1rem; margin-top: 1.2rem;">
                <div style="background: rgba(255,255,255,0.15); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                    📅 Last Updated: Real-time
                </div>
                <div style="background: rgba(255,255,255,0.15); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                    📊 Data Driven Decisions
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="background: white; padding: 0.8rem; border-radius: 12px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <span style="font-size: 2rem; color: #E30613; font-weight: bold;">EP</span>
            </div>
            <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 600;">EraPhone BI Suite v6.0</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



# ==================== LOAD DATA ====================
data = load_data()

# ==================== DEBUG INFO ====================
with st.sidebar.expander("🔍 Data Status", expanded=False):
    st.write("**Forecast Data:**")
    if not data['sales_forecast'].empty:
        st.success(f"✓ Loaded: {len(data['sales_forecast'])} rows")
        st.write(f"Columns: {data['sales_forecast'].columns.tolist()}")
        st.write("First 3 rows:", data['sales_forecast'].head(3))
    else:
        st.error("✗ No forecast data loaded")
    
    st.write("---")
    
    st.write("**History Data:**")
    if not data['sales_history'].empty:
        st.success(f"✓ Loaded: {len(data['sales_history'])} rows")
    else:
        st.error("✗ No history data loaded")

# ==================== EXECUTIVE SUMMARY ====================
st.markdown('<h2 class="modern-header">📊 Executive Summary</h2>', unsafe_allow_html=True)

transactions_df = data.get('transactions', pd.DataFrame())
top_products = data.get('top_products', pd.DataFrame())
mid_products = data.get('mid_products', pd.DataFrame())
low_products = data.get('low_products', pd.DataFrame())

# ===== HITUNG DATA TAMBAHAN =====
# Hitung top brand
top_brand_name = "N/A"
top_brand_revenue = 0
if not transactions_df.empty and 'brand' in transactions_df.columns:
    brand_revenue = transactions_df.groupby('brand')['total_value'].sum().reset_index()
    if not brand_revenue.empty:
        top_brand = brand_revenue.sort_values('total_value', ascending=False).iloc[0]
        top_brand_name = top_brand['brand']
        top_brand_revenue = top_brand['total_value']
        if len(top_brand_name) > 15:
            top_brand_name = top_brand_name[:15] + "..."

# Hitung total brands
total_brands = transactions_df['brand'].nunique() if not transactions_df.empty and 'brand' in transactions_df.columns else 0

# Hitung average revenue per transaction
total_revenue = transactions_df['total_value'].sum() if not transactions_df.empty else 0
total_transactions = len(transactions_df) if not transactions_df.empty else 0
avg_revenue_per_tx = total_revenue / total_transactions if total_transactions > 0 else 0

# Top product info
top_product_name = "N/A"
top_product_revenue = 0
if not top_products.empty and 'nama_barang' in top_products.columns:
    top_product_name = top_products.iloc[0]['nama_barang']
    top_product_revenue = top_products.iloc[0]['total_value'] if 'total_value' in top_products.columns else 0
    if len(top_product_name) > 18:
        top_product_name = top_product_name[:18] + "..."



# Metrics Row 1 - VERSI DENGAN "TOTAL PRODUCTS"

# Metrics Row 1 - VERSI DIPERBAIKI
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = transactions_df['total_value'].sum() if not transactions_df.empty else 0
    st.metric("💰 Total Revenue", format_currency(total_revenue))

with col2:
    total_transactions = len(transactions_df) if not transactions_df.empty else 0
    st.metric("🧾 Total Transactions", f"{total_transactions:,}")

with col3:
    # AMBIL LANGSUNG DARI df_analysis.csv
    transactions_data = data.get('transactions', pd.DataFrame())
    
    # HITUNG nama_barang unik
    total_produk = transactions_data['nama_barang'].nunique() if not transactions_data.empty and 'nama_barang' in transactions_data.columns else 0
    
    # TAMPILKAN
    st.metric("📦 Total Products", f"{total_produk:,}")

with col4:
    # AVERAGE REVENUE PER TRANSACTION
    avg_revenue_per_tx = total_revenue / total_transactions if total_transactions > 0 else 0
    st.metric("📈 Avg. per Transaction", format_currency(avg_revenue_per_tx))

with col5:
    total_brands = transactions_df['brand'].nunique() if not transactions_df.empty and 'brand' in transactions_df.columns else 0
    st.metric("🏷️ Total Brands", f"{total_brands:,}")

# Metrics Row 2 - INFORMASI BARU
col6, col7, col8, col9 = st.columns(4)

with col6:
    # TOP PRODUCT
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #E30613; box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
        <div style="font-size: 0.85rem; color: #666666; margin-bottom: 0.4rem;">🏆 TOP PRODUCT</div>
        <div style="font-size: 1rem; font-weight: 600; color: #111111; line-height: 1.2; margin-bottom: 0.5rem;">{top_product_name}</div>
        <div style="font-size: 0.95rem; color: #E30613; font-weight: 700;">{format_currency(top_product_revenue)}</div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    # TOP BRAND  
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #4CAF50; box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
        <div style="font-size: 0.85rem; color: #666666; margin-bottom: 0.4rem;">👑 TOP BRAND</div>
        <div style="font-size: 1rem; font-weight: 600; color: #111111; line-height: 1.2; margin-bottom: 0.5rem;">{top_brand_name}</div>
        <div style="font-size: 0.95rem; color: #4CAF50; font-weight: 700;">{format_currency(top_brand_revenue)}</div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    # CLASS A REVENUE
    class_a_revenue = top_products['total_value'].sum() if not top_products.empty else 0
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #FF9800; box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
        <div style="font-size: 0.85rem; color: #666666; margin-bottom: 0.4rem;">⭐ CLASS A REVENUE</div>
        <div style="font-size: 1.1rem; color: #111111; font-weight: 700; margin-bottom: 0.2rem;">{format_currency(class_a_revenue)}</div>
        <div style="font-size: 0.8rem; color: #666666;">
            {len(top_products)} products
        </div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    # CLASS B+C REVENUE
    class_b_revenue = mid_products['total_value'].sum() if not mid_products.empty else 0
    class_c_revenue = low_products['total_value'].sum() if not low_products.empty else 0
    total_bc_revenue = class_b_revenue + class_c_revenue
    total_bc_products = len(mid_products) + len(low_products)
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #2196F3; box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
        <div style="font-size: 0.85rem; color: #666666; margin-bottom: 0.4rem;">📊 CLASS B + C REVENUE</div>
        <div style="font-size: 1.1rem; color: #111111; font-weight: 700; margin-bottom: 0.2rem;">{format_currency(total_bc_revenue)}</div>
        <div style="font-size: 0.8rem; color: #666666;">
            {total_bc_products} products
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    

# ==================== TOP PERFORMERS ANALYSIS ====================
st.markdown('<h2 class="modern-header">🏆 Top Performers Analysis</h2>', unsafe_allow_html=True)

# Buat 3 tab untuk Top Brands, Top Products, Top Categories
top_tab1, top_tab2, top_tab3 = st.tabs(["🏷️ Top Brands", "📦 Top Products", "📊 Top Categories"])

with top_tab1:
    if not transactions_df.empty and 'brand' in transactions_df.columns:
        # Hitung metrics brand
        brand_analysis = transactions_df.groupby('brand').agg({
            'total_value': 'sum',
            'quantity': 'sum',
            'nama_barang': 'nunique'
        }).reset_index()
        brand_analysis = brand_analysis.sort_values('total_value', ascending=False)
        brand_analysis.columns = ['Brand', 'Total Revenue', 'Total Quantity', 'Unique Products']
        
        # Format currency
        brand_analysis['Revenue Formatted'] = brand_analysis['Total Revenue'].apply(format_currency)
        brand_analysis['Revenue %'] = (brand_analysis['Total Revenue'] / brand_analysis['Total Revenue'].sum() * 100).round(2)
        
        # Tampilkan metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            top_brand = brand_analysis.iloc[0]['Brand'] if len(brand_analysis) > 0 else "N/A"
            top_brand_rev = brand_analysis.iloc[0]['Total Revenue'] if len(brand_analysis) > 0 else 0
            st.metric("👑 Top Brand", top_brand, format_currency(top_brand_rev))
        
        with col2:
            avg_rev_per_brand = brand_analysis['Total Revenue'].mean()
            st.metric("📊 Avg/Brand", format_currency(avg_rev_per_brand))
        
        with col3:
            top_3_share = brand_analysis.head(3)['Total Revenue'].sum() / brand_analysis['Total Revenue'].sum() * 100
            st.metric("🎯 Top 3 Share", f"{top_3_share:.1f}%")
        
        # Visualisasi
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Bar chart top 10 brands
            top_10_brands = brand_analysis.head(10)
            fig_brands = px.bar(
                top_10_brands,
                x='Brand',
                y='Total Revenue',
                title='Top 10 Brands by Revenue',
                color='Total Revenue',
                color_continuous_scale='reds',
                text='Revenue Formatted'
            )
            fig_brands.update_layout(
                height=400,
                xaxis_tickangle=-45,
                yaxis_title="Revenue",
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_brands, use_container_width=True)
        
        with col_viz2:
            # Pie chart brand distribution
            fig_pie = px.pie(
                brand_analysis.head(8),
                values='Total Revenue',
                names='Brand',
                title='Brand Revenue Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Reds
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Data table
        st.markdown("### 📋 Brand Performance Details")
        display_brand_df = brand_analysis[['Brand', 'Revenue Formatted', 'Revenue %', 'Total Quantity', 'Unique Products']]
        st.dataframe(display_brand_df, use_container_width=True, height=300)
    else:
        st.info("No brand data available")

with top_tab2:
    if not transactions_df.empty:
        # Hitung metrics produk
        product_analysis = transactions_df.groupby('nama_barang').agg({
            'total_value': 'sum',
            'quantity': 'sum',
            'brand': 'first',
            'cat_norm': 'first'
        }).reset_index()
        product_analysis = product_analysis.sort_values('total_value', ascending=False)
        
        # Tambahkan metrics tambahan
        product_analysis['Revenue Formatted'] = product_analysis['total_value'].apply(format_currency)
        product_analysis['Avg Price'] = (product_analysis['total_value'] / product_analysis['quantity']).round(0)
        
        # Tampilkan metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            top_product = product_analysis.iloc[0]['nama_barang'][:20] + "..." if len(product_analysis.iloc[0]['nama_barang']) > 20 else product_analysis.iloc[0]['nama_barang']
            top_product_rev = product_analysis.iloc[0]['total_value']
            st.metric("🥇 Top Product", top_product, format_currency(top_product_rev))
        
        with col2:
            total_unique_products = len(product_analysis)
            st.metric("📦 Unique Products", f"{total_unique_products:,}")
        
        with col3:
            avg_rev_per_product = product_analysis['total_value'].mean()
            st.metric("💰 Avg/Product", format_currency(avg_rev_per_product))
        
        # Filter interaktif
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            selected_brand = st.selectbox(
                "Filter by Brand",
                options=["All"] + sorted(product_analysis['brand'].dropna().unique().tolist()),
                key="product_brand_filter"
            )
        
        with col_filter2:
            min_revenue = st.number_input(
                "Minimum Revenue (Rp)",
                min_value=0,
                value=1000000,
                step=1000000,
                format="%d"
            )
        
        # Apply filters
        filtered_products = product_analysis.copy()
        if selected_brand != "All":
            filtered_products = filtered_products[filtered_products['brand'] == selected_brand]
        filtered_products = filtered_products[filtered_products['total_value'] >= min_revenue]
        
        # Visualisasi
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Top products bar chart
            top_20_products = filtered_products.head(20).copy()
            top_20_products['Short Name'] = top_20_products['nama_barang'].apply(
                lambda x: (x[:15] + "...") if len(x) > 15 else x
            )
            
            fig_products = px.bar(
                top_20_products,
                x='Short Name',
                y='total_value',
                title=f'Top Products by Revenue ({selected_brand if selected_brand != "All" else "All Brands"})',
                hover_data=['brand', 'quantity', 'Avg Price'],
                color='total_value',
                color_continuous_scale='reds'
            )
            fig_products.update_layout(
                height=500,
                xaxis_tickangle=-45,
                yaxis_title="Revenue",
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_products, use_container_width=True)
        
        with col_viz2:
            # Scatter plot: Quantity vs Revenue
            fig_scatter = px.scatter(
                filtered_products.head(50),
                x='quantity',
                y='total_value',
                size='total_value',
                color='brand',
                hover_name='nama_barang',
                title='Quantity vs Revenue Analysis',
                labels={'quantity': 'Quantity Sold', 'total_value': 'Total Revenue'},
                size_max=30
            )
            fig_scatter.update_layout(height=500, plot_bgcolor='white')
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Data table dengan pagination
        st.markdown(f"### 📋 Product Details ({len(filtered_products)} products)")
        
        # Pagination
        items_per_page = 20
        total_pages = max(1, len(filtered_products) // items_per_page + (1 if len(filtered_products) % items_per_page > 0 else 0))
        page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page_number - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(filtered_products))
        
        display_product_df = filtered_products.iloc[start_idx:end_idx].copy()
        display_product_df = display_product_df[[
            'nama_barang', 'brand', 'cat_norm', 'Revenue Formatted', 
            'quantity', 'Avg Price'
        ]]
        display_product_df.columns = ['Product', 'Brand', 'Category', 'Revenue', 'Quantity', 'Avg Price']
        
        st.dataframe(display_product_df, use_container_width=True, height=400)
        
        # Pagination info
        st.caption(f"Showing products {start_idx+1}-{end_idx} of {len(filtered_products)}")
        
    else:
        st.info("No product data available")

with top_tab3:
    if not transactions_df.empty and 'cat_norm' in transactions_df.columns:
        # Hitung metrics kategori
        category_analysis = transactions_df.groupby('cat_norm').agg({
            'total_value': 'sum',
            'quantity': 'sum',
            'nama_barang': 'nunique',
            'brand': 'nunique'
        }).reset_index()
        category_analysis = category_analysis.sort_values('total_value', ascending=False)
        category_analysis.columns = ['Category', 'Total Revenue', 'Total Quantity', 'Unique Products', 'Unique Brands']
        
        # Format dan hitung persentase
        category_analysis['Revenue Formatted'] = category_analysis['Total Revenue'].apply(format_currency)
        category_analysis['Revenue %'] = (category_analysis['Total Revenue'] / category_analysis['Total Revenue'].sum() * 100).round(2)
        category_analysis['Avg Price'] = (category_analysis['Total Revenue'] / category_analysis['Total Quantity']).round(0)
        
        # Tampilkan metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            top_category = category_analysis.iloc[0]['Category']
            top_cat_rev = category_analysis.iloc[0]['Total Revenue']
            st.metric("🏆 Top Category", top_category, format_currency(top_cat_rev))
        
        with col2:
            category_count = len(category_analysis)
            st.metric("📂 Total Categories", f"{category_count}")
        
        with col3:
            top_3_cat_share = category_analysis.head(3)['Total Revenue'].sum() / category_analysis['Total Revenue'].sum() * 100
            st.metric("🎯 Top 3 Categories Share", f"{top_3_cat_share:.1f}%")
        
        # Visualisasi
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Bar chart kategori
            fig_cat_bar = px.bar(
                category_analysis,
                x='Category',
                y='Total Revenue',
                title='Category Revenue Distribution',
                color='Total Revenue',
                color_continuous_scale='reds',
                text='Revenue %'
            )
            fig_cat_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_cat_bar.update_layout(
                height=400,
                xaxis_tickangle=-45,
                yaxis_title="Revenue",
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_cat_bar, use_container_width=True)
        
        with col_viz2:
            # Treemap kategori
            fig_treemap = px.treemap(
                category_analysis,
                path=['Category'],
                values='Total Revenue',
                title='Category Revenue Treemap',
                color='Total Revenue',
                color_continuous_scale='Reds',
                hover_data=['Revenue %', 'Unique Products']
            )
            fig_treemap.update_layout(height=400)
            fig_treemap.update_traces(textinfo="label+value+percent entry")
            st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Detail table
        st.markdown("### 📋 Category Performance Details")
        
        # Sort options
        sort_by = st.selectbox(
            "Sort by",
            options=['Total Revenue', 'Total Quantity', 'Unique Products', 'Avg Price'],
            key="category_sort"
        )
        
        sorted_categories = category_analysis.sort_values(sort_by, ascending=False)
        display_cat_df = sorted_categories[[
            'Category', 'Revenue Formatted', 'Revenue %', 
            'Total Quantity', 'Unique Products', 'Unique Brands', 'Avg Price'
        ]]
        display_cat_df.columns = [
            'Category', 'Revenue', 'Revenue %', 'Quantity', 
            'Unique Products', 'Unique Brands', 'Avg Price'
        ]
        
        st.dataframe(display_cat_df, use_container_width=True, height=300)
        
        # Kategori vs Brand analysis
        st.markdown("#### 🔍 Category vs Brand Analysis")
        if not transactions_df.empty:
            cat_brand_analysis = transactions_df.groupby(['cat_norm', 'brand']).agg({
                'total_value': 'sum'
            }).reset_index()
            
            # Pivot table
            pivot_table = cat_brand_analysis.pivot_table(
                index='brand',
                columns='cat_norm',
                values='total_value',
                aggfunc='sum',
                fill_value=0
            )
            
            # Heatmap
            fig_heatmap = px.imshow(
                pivot_table,
                title='Brand Performance Across Categories (Heatmap)',
                color_continuous_scale='reds',
                aspect="auto"
            )
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("No category data available")

# ==================== FORECASTING SECTION ====================
st.markdown('<h2 class="modern-header">📈 Revenue Forecasting & Trends</h2>', unsafe_allow_html=True)

sales_history = data.get('sales_history', pd.DataFrame())
sales_forecast = data.get('sales_forecast', pd.DataFrame())

# Forecast Summary Metrics
if not sales_forecast.empty:
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        avg_forecast = sales_forecast['forecast_revenue'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #666666; margin-bottom: 0.5rem;">📅 Avg Monthly Forecast</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #111111;">{format_currency(avg_forecast)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f2:
        forecast_months = len(sales_forecast)
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #666666; margin-bottom: 0.5rem;">🗓️ Forecast Period</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #111111;">{forecast_months} Months</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f3:
        if not sales_history.empty and 'revenue' in sales_history.columns:
            last_actual = sales_history['revenue'].iloc[-1] if len(sales_history) > 0 else 0
            first_forecast = sales_forecast['forecast_revenue'].iloc[0]
            growth_pct = ((first_forecast - last_actual) / last_actual * 100) if last_actual > 0 else 0
            trend = "▲" if growth_pct > 0 else "▼"
            color = "#4CAF50" if growth_pct > 0 else "#E30613"
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #666666; margin-bottom: 0.5rem;">📊 Projected Growth</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {color};">{trend} {growth_pct:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

# Plot Forecast Chart
forecast_chart = create_forecast_chart(sales_history, sales_forecast)
if forecast_chart:
    st.plotly_chart(forecast_chart, width='stretch')
else:
    st.warning("Forecast chart could not be generated. Check data in sidebar.")
    
# ===== TIME SERIES DRILL-DOWN ANALYSIS =====
st.markdown("---")
st.markdown("#### 🔍 Time Series Drill-Down")

if not transactions_df.empty and 'tanggal_order' in transactions_df.columns:
    # Konversi tanggal
    transactions_df['tanggal_order'] = pd.to_datetime(transactions_df['tanggal_order'])
    
    # Pilih granularity
    time_granularity = st.radio(
        "Time Granularity",
        options=["Daily", "Weekly", "Monthly"],
        horizontal=True
    )
    
    # Resample berdasarkan granularity
    if time_granularity == "Daily":
        transactions_df['time_period'] = transactions_df['tanggal_order'].dt.date
        freq_label = "Day"
    elif time_granularity == "Weekly":
        transactions_df['time_period'] = transactions_df['tanggal_order'].dt.to_period('W').apply(lambda r: r.start_time)
        freq_label = "Week"
    else:  # Monthly
        transactions_df['time_period'] = transactions_df['tanggal_order'].dt.to_period('M').apply(lambda r: r.start_time)
        freq_label = "Month"
    
    # Agregasi data
    time_series = transactions_df.groupby('time_period').agg({
        'total_value': 'sum',
        'quantity': 'sum',
        'nama_barang': 'nunique'
    }).reset_index()
    time_series.columns = ['Period', 'Revenue', 'Quantity', 'Unique Products']
    time_series = time_series.sort_values('Period')
    
    # Moving average
    time_series['MA_7'] = time_series['Revenue'].rolling(window=min(7, len(time_series)), min_periods=1).mean()
    
    # Plot time series dengan dual axis
    fig_detailed = go.Figure()
    
    # Revenue line
    fig_detailed.add_trace(go.Scatter(
        x=time_series['Period'],
        y=time_series['Revenue'],
        name='Revenue',
        mode='lines+markers',
        line=dict(color='#E30613', width=3),
        yaxis='y'
    ))
    
    # Moving average
    fig_detailed.add_trace(go.Scatter(
        x=time_series['Period'],
        y=time_series['MA_7'],
        name='7-Period MA',
        mode='lines',
        line=dict(color='#FF6B6B', width=2, dash='dash'),
        yaxis='y'
    ))
    
    # Quantity (secondary axis)
    fig_detailed.add_trace(go.Bar(
        x=time_series['Period'],
        y=time_series['Quantity'],
        name='Quantity',
        marker_color='rgba(78, 205, 196, 0.6)',
        yaxis='y2'
    ))
    
    fig_detailed.update_layout(
        title=f'{freq_label}ly Revenue & Quantity Trend',
        height=450,
        plot_bgcolor='white',
        xaxis=dict(title=f'{freq_label}'),
        yaxis=dict(
            title="Revenue (Rp)",
            tickformat=',.0f',
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis2=dict(
            title="Quantity",
            overlaying='y',
            side='right',
            gridcolor='rgba(0,0,0,0)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_detailed, use_container_width=True)
    
    # Metrics cards untuk time series
    col_ts1, col_ts2, col_ts3, col_ts4 = st.columns(4)
    
    with col_ts1:
        peak_revenue = time_series['Revenue'].max()
        peak_date = time_series.loc[time_series['Revenue'].idxmax(), 'Period']
        st.metric(
            "📈 Peak Revenue", 
            format_currency(peak_revenue),
            delta=f"On {peak_date.strftime('%d %b')}" if hasattr(peak_date, 'strftime') else ""
        )
    
    with col_ts2:
        avg_daily_rev = time_series['Revenue'].mean()
        st.metric(
            f"💰 Avg/{freq_label}", 
            format_currency(avg_daily_rev)
        )
    
    with col_ts3:
        growth_rate = ((time_series['Revenue'].iloc[-1] - time_series['Revenue'].iloc[0]) / 
                      time_series['Revenue'].iloc[0] * 100) if len(time_series) > 1 and time_series['Revenue'].iloc[0] > 0 else 0
        st.metric(
            "📊 Total Growth", 
            f"{growth_rate:.1f}%"
        )
    
    with col_ts4:
        avg_quantity = time_series['Quantity'].mean()
        st.metric(
            "📦 Avg Quantity", 
            f"{avg_quantity:.0f}"
        )

# ==================== PRODUCT PORTFOLIO ANALYSIS ====================
st.markdown('<h2 class="modern-header">📦 Product Portfolio Analysis</h2>', unsafe_allow_html=True)

# Tabs untuk product classes
# Tabs untuk product classes - VERSI LEBIH PENDEK
tab1, tab2, tab3 = st.tabs(["⭐ Class A", "📈 Class B", "🌱 Class C"])

# CLASS A TAB
with tab1:
    if not top_products.empty:
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            bar_chart_a = create_product_bar_chart(top_products, "Class A", "#C62828")
            if bar_chart_a:
                st.plotly_chart(bar_chart_a, width='stretch')
        
        with col_a2:
            pie_chart_a = create_revenue_pie_chart(top_products, "Class A")
            if pie_chart_a:
                st.plotly_chart(pie_chart_a, width='stretch')
        
        # Product Table
        st.markdown("### 📋 Class A Product Details")
        display_df_a = top_products.copy()
        
        # Format columns
        if 'nama_barang' in display_df_a.columns:
            display_df_a['Product Name'] = display_df_a['nama_barang']
        if 'total_value' in display_df_a.columns:
            display_df_a['Revenue'] = display_df_a['total_value'].apply(format_currency)
        if 'revenue_pct' in display_df_a.columns:
            display_df_a['Revenue %'] = display_df_a['revenue_pct'].apply(lambda x: f"{x:.3f}%")
        
        display_columns = ['Product Name', 'Revenue', 'Revenue %']
        if 'ABC_class' in display_df_a.columns:
            display_columns.append('ABC_class')
        
        st.dataframe(display_df_a[display_columns], width='stretch', height=400)
    else:
        st.warning("No Class A products data available")

# CLASS B TAB
with tab2:
    if not mid_products.empty:
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            bar_chart_b = create_product_bar_chart(mid_products, "Class B", "#FF9800")
            if bar_chart_b:
                st.plotly_chart(bar_chart_b, width='stretch')
        
        with col_b2:
            pie_chart_b = create_revenue_pie_chart(mid_products, "Class B")
            if pie_chart_b:
                st.plotly_chart(pie_chart_b, width='stretch')
        
        st.markdown("### 📋 Class B Product Details")
        display_df_b = mid_products.copy()
        
        if 'nama_barang' in display_df_b.columns:
            display_df_b['Product Name'] = display_df_b['nama_barang']
        if 'total_value' in display_df_b.columns:
            display_df_b['Revenue'] = display_df_b['total_value'].apply(format_currency)
        if 'revenue_pct' in display_df_b.columns:
            display_df_b['Revenue %'] = display_df_b['revenue_pct'].apply(lambda x: f"{x:.3f}%")
        
        display_columns = ['Product Name', 'Revenue', 'Revenue %']
        if 'ABC_class' in display_df_b.columns:
            display_columns.append('ABC_class')
        
        st.dataframe(display_df_b[display_columns], width='stretch', height=400)
    else:
        st.warning("No Class B products data available")

# CLASS C TAB
with tab3:
    if not low_products.empty:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            bar_chart_c = create_product_bar_chart(low_products, "Class C", "#2E7D32")
            if bar_chart_c:
                st.plotly_chart(bar_chart_c, width='stretch')
        
        with col_c2:
            pie_chart_c = create_revenue_pie_chart(low_products, "Class C")
            if pie_chart_c:
                st.plotly_chart(pie_chart_c, width='stretch')
        
        st.markdown("### 📋 Class C Product Details")
        display_df_c = low_products.copy()
        
        if 'nama_barang' in display_df_c.columns:
            display_df_c['Product Name'] = display_df_c['nama_barang']
        if 'total_value' in display_df_c.columns:
            display_df_c['Revenue'] = display_df_c['total_value'].apply(format_currency)
        if 'revenue_pct' in display_df_c.columns:
            display_df_c['Revenue %'] = display_df_c['revenue_pct'].apply(lambda x: f"{x:.3f}%")
        
        display_columns = ['Product Name', 'Revenue', 'Revenue %']
        if 'ABC_class' in display_df_c.columns:
            display_columns.append('ABC_class')
        
        st.dataframe(display_df_c[display_columns], width='stretch', height=400)
    else:
        st.warning("No Class C products data available")
        
        
# ==================== PRODUCT INVENTORY BY BRAND ====================
st.markdown('<h2 class="modern-header">📋 Product Inventory by Brand</h2>', unsafe_allow_html=True)

if not transactions_df.empty and 'brand' in transactions_df.columns:
    # Pilih brand untuk analisis detail
    all_brands = sorted(transactions_df['brand'].dropna().unique())
    selected_brands = st.multiselect(
        "Select Brands to Analyze",
        options=all_brands,
        default=all_brands[:3] if len(all_brands) >= 3 else all_brands,
        help="Select brands to view their product portfolio"
    )
    
    if selected_brands:
        # Filter data untuk brand yang dipilih
        filtered_by_brand = transactions_df[transactions_df['brand'].isin(selected_brands)]
        
        # Ringkasan metrics - WARNA FONT HITAM SEMUA
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        
        with col_sum1:
            total_products = filtered_by_brand['nama_barang'].nunique()
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #E30613; 
                        box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
                <div style="font-size: 0.85rem; color: #111111; margin-bottom: 0.4rem; font-weight: 600;">📦 TOTAL PRODUCTS</div>
                <div style="font-size: 1.4rem; color: #111111; font-weight: 800;">{total_products:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_sum2:
            total_revenue = filtered_by_brand['total_value'].sum()
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #E30613; 
                        box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
                <div style="font-size: 0.85rem; color: #111111; margin-bottom: 0.4rem; font-weight: 600;">💰 TOTAL REVENUE</div>
                <div style="font-size: 1.4rem; color: #111111; font-weight: 800;">{format_currency(total_revenue)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_sum3:
            avg_price = (filtered_by_brand['total_value'].sum() / filtered_by_brand['quantity'].sum()) if filtered_by_brand['quantity'].sum() > 0 else 0
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #E30613; 
                        box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
                <div style="font-size: 0.85rem; color: #111111; margin-bottom: 0.4rem; font-weight: 600;">🏷️ AVG PRICE</div>
                <div style="font-size: 1.4rem; color: #111111; font-weight: 800;">{format_currency(avg_price)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_sum4:
            transactions_count = len(filtered_by_brand)
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #E30613; 
                        box-shadow: 0 2px 6px rgba(0,0,0,0.05); height: 100%;">
                <div style="font-size: 0.85rem; color: #111111; margin-bottom: 0.4rem; font-weight: 600;">🧾 TRANSACTIONS</div>
                <div style="font-size: 1.4rem; color: #111111; font-weight: 800;">{transactions_count:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detail produk per brand
        for brand in selected_brands:
            brand_data = filtered_by_brand[filtered_by_brand['brand'] == brand]
            
            with st.expander(f"📱 **{brand}** - Product Portfolio ({len(brand_data)} transactions)", expanded=(brand == selected_brands[0])):
                # Brand summary
                brand_summary = brand_data.groupby('nama_barang').agg({
                    'total_value': 'sum',
                    'quantity': 'sum',
                    'cat_norm': 'first'
                }).reset_index()
                brand_summary = brand_summary.sort_values('total_value', ascending=False)
                
                col_b1, col_b2 = st.columns(2)
                
                with col_b1:
                    # Top products chart - WARNA FONT HITAM
                    top_products_brand = brand_summary.head(10).copy()
                    top_products_brand['Short Name'] = top_products_brand['nama_barang'].apply(
                        lambda x: (x[:20] + "...") if len(x) > 20 else x
                    )
                    
                    fig_brand = px.bar(
                        top_products_brand,
                        x='Short Name',
                        y='total_value',
                        title=f'Top Products - {brand}',
                        color='total_value',
                        color_continuous_scale='reds',
                        text='quantity'
                    )
                    fig_brand.update_layout(
                        height=350,
                        xaxis_tickangle=-45,
                        yaxis_title="Revenue",
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(color='#111111', size=12),
                        title_font=dict(color='#111111', size=16),
                        xaxis=dict(
                            tickfont=dict(color='#111111'),
                            title_font=dict(color='#111111')
                        ),
                        yaxis=dict(
                            tickfont=dict(color='#111111'),
                            title_font=dict(color='#111111'),
                            gridcolor='rgba(0,0,0,0.05)'
                        )
                    )
                    st.plotly_chart(fig_brand, use_container_width=True)
                
                with col_b2:
                    # Kategori distribution - WARNA FONT HITAM
                    if 'cat_norm' in brand_data.columns:
                        cat_dist = brand_data.groupby('cat_norm').agg({
                            'total_value': 'sum',
                            'quantity': 'sum'
                        }).reset_index()
                        
                        fig_cat_pie = px.pie(
                            cat_dist,
                            values='total_value',
                            names='cat_norm',
                            title=f'Category Distribution - {brand}',
                            hole=0.4,
                            color_discrete_sequence=px.colors.sequential.Reds
                        )
                        fig_cat_pie.update_layout(
                            height=350,
                            plot_bgcolor='white',
                            paper_bgcolor='white',
                            font=dict(color='#111111', size=12),
                            title_font=dict(color='#111111', size=16),
                            legend=dict(font=dict(color='#111111'))
                        )
                        fig_cat_pie.update_traces(
                            textfont=dict(color='#111111', size=10),
                            textposition='inside'
                        )
                        st.plotly_chart(fig_cat_pie, use_container_width=True)
                
                # Product details table - WARNA FONT HITAM
                st.markdown(f"#### Product Details - {brand}")
                
                # Format table
                display_brand_df = brand_summary.copy()
                display_brand_df['Revenue'] = display_brand_df['total_value'].apply(format_currency)
                display_brand_df['Avg Price'] = (display_brand_df['total_value'] / display_brand_df['quantity']).round(0)
                display_brand_df['Avg Price Formatted'] = display_brand_df['Avg Price'].apply(format_currency)
                
                display_brand_df = display_brand_df[[
                    'nama_barang', 'cat_norm', 'quantity', 
                    'Revenue', 'Avg Price Formatted'
                ]]
                display_brand_df.columns = ['Product', 'Category', 'Quantity', 'Revenue', 'Avg Price']
                
                # CSS untuk table dengan font hitam
                st.markdown("""
                <style>
                    .inventory-table th {
                        color: #111111 !important;
                        font-weight: 700 !important;
                    }
                    .inventory-table td {
                        color: #111111 !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_brand_df, 
                    use_container_width=True, 
                    height=250
                )
else:
    st.info("No brand data available for inventory analysis")
        
# ==================== BUSINESS INTELLIGENCE - ELEGANT DESIGN ====================
st.markdown('<h2 class="modern-header">🎯 Business Intelligence Dashboard</h2>', unsafe_allow_html=True)

# Custom CSS untuk estetika
st.markdown("""
<style>
    .era-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(227, 6, 19, 0.15);
        box-shadow: 0 3px 10px rgba(227, 6, 19, 0.05);
        transition: all 0.2s ease;
    }
    .era-card:hover {
        box-shadow: 0 5px 15px rgba(227, 6, 19, 0.1);
        transform: translateY(-1px);
    }
    .era-pill {
        background: linear-gradient(135deg, #E30613, #B71C1C);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .era-badge {
        background: rgba(227, 6, 19, 0.1);
        color: #E30613;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

bundles = data.get('bundles', pd.DataFrame())
cross_sell = data.get('cross_sell', pd.DataFrame())

if not bundles.empty or not cross_sell.empty:
    # ELEGANT HEADER
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not bundles.empty:
            high_conf = len(bundles[bundles['confidence'] > 0.7])
            st.metric(
                label="🔥 Premium Bundles",
                value=high_conf,
                delta=f"{(high_conf/len(bundles)*100):.0f}%" if len(bundles) > 0 else None
            )
    
    with col2:
        if not cross_sell.empty:
            avg_conf = cross_sell['confidence'].mean() * 100
            st.metric(
                label="📈 Avg Confidence",
                value=f"{avg_conf:.1f}%"
            )
    
    with col3:
        if not bundles.empty:
            top_lift = bundles['lift'].max() if 'lift' in bundles.columns else 0
            st.metric(
                label="🚀 Max Lift",
                value=f"{top_lift:.1f}x"
            )
    
    # ELEGANT TABS
    tab1, tab2 = st.tabs(["✨ **Premium Bundling Strategies**", "🔄 **Cross-Selling Opportunities**"])
    
    # ===== BUNDLING TAB =====
    with tab1:
        if not bundles.empty:
            for idx, row in bundles.head(10).iterrows():
                # Card container
                st.markdown('<div class="era-card">', unsafe_allow_html=True)
                
                # Header row
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**Strategy #{idx+1}**")
                with col_b:
                    conf = float(row.get('confidence', 0)) * 100
                    lift = float(row.get('lift', 0))
                    st.markdown(f'<span class="era-pill">{conf:.0f}% • {lift:.1f}x</span>', unsafe_allow_html=True)
                
                # Product pair - elegant layout
                st.markdown("---")
                col_left, col_plus, col_right = st.columns([5, 1, 5])
                
                with col_left:
                    st.markdown("**Customer Buys**")
                    antecedents = str(row.get('antecedents', ''))
                    st.code(antecedents[:40] + ("..." if len(antecedents) > 40 else ""), language="")
                
                with col_plus:
                    st.markdown("<br><h3 style='color:#E30613; text-align:center;'>+</h3>", unsafe_allow_html=True)
                
                with col_right:
                    st.markdown("**Recommend Add**")
                    consequents = str(row.get('consequents', ''))
                    st.code(consequents[:40] + ("..." if len(consequents) > 40 else ""), language="")
                
                # Footer info
                st.markdown("---")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    strategy = row.get('business_strategy', '')
                    st.markdown(f"**Strategy:** `{strategy}`")
                with col_f2:
                    priority = row.get('execution_priority', '')
                    st.markdown(f"**Priority:** `{priority}`")
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📋 No bundling data available")
    
    # ===== CROSS-SELL TAB =====
    with tab2:
        if not cross_sell.empty:
            for idx, row in cross_sell.head(10).iterrows():
                # Card container
                st.markdown('<div class="era-card">', unsafe_allow_html=True)
                
                # Header with confidence meter
                conf = float(row.get('confidence', 0)) * 100
                score = float(row.get('business_score', 0)) * 100
                
                col_h1, col_h2 = st.columns([3, 1])
                with col_h1:
                    st.markdown(f"**Opportunity #{idx+1}**")
                    # Confidence progress bar
                    st.progress(conf/100)
                    st.caption(f"Confidence: {conf:.0f}%")
                
                with col_h2:
                    st.metric("Score", f"{score:.0f}", delta=None, label_visibility="collapsed")
                
                # Purchase flow
                st.markdown("---")
                st.markdown("**Purchase Flow**")
                
                flow_col1, flow_arrow, flow_col2 = st.columns([5, 1, 5])
                
                with flow_col1:
                    antecedents = str(row.get('antecedents', ''))
                    st.markdown(f"*When buying:*\n`{antecedents[:45]}{'...' if len(antecedents) > 45 else ''}`")
                
                with flow_arrow:
                    st.markdown("<h3 style='color:#E30613; text-align:center;'>→</h3>", unsafe_allow_html=True)
                
                with flow_col2:
                    consequents = str(row.get('consequents', ''))
                    st.markdown(f"*Recommend:*\n`{consequents[:45]}{'...' if len(consequents) > 45 else ''}`")
                
                # Metrics footer
                st.markdown("---")
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    lift = float(row.get('lift', 0))
                    st.metric("Lift", f"{lift:.1f}x")
                
                with col_m2:
                    support = float(row.get('support', 0))
                    st.metric("Support", f"{support:.3f}")
                
                with col_m3:
                    strategy = row.get('business_strategy', '')
                    st.markdown(f'<span class="era-badge">{strategy}</span>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📋 No cross-selling data available")

else:
    # Elegant empty state
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%); 
                border-radius: 16px; border: 2px solid #fecaca; margin: 2rem 0;">
        <div style="font-size: 3rem; color: #E30613; margin-bottom: 1rem;">📊</div>
        <h3 style="color: #7f1d1d; margin-bottom: 0.5rem;">Business Intelligence Dashboard</h3>
        <p style="color: #991b1b;">No association rules data available for analysis.</p>
    </div>
    """, unsafe_allow_html=True)

st.caption("Showing top 10 recommendations by confidence score • EraPhone BI")


st.markdown("""
<div style="text-align: center;">
<h4 style="color: #E30613; margin-bottom: 10px;">🚀 EraPhone Intelligence Dashboard</h4>
<p style="color: #444; font-weight: 600; margin-bottom: 5px;">👥 Kelompok 7 - Data Science</p>
<p style="color: #555; margin-bottom: 5px;"><strong>Anggota:</strong> Ayu Lutfiah • Jeni Fajarwati • Valerrinna Azzahra</p>
<p style="color: #666; font-size: 14px; margin-bottom: 10px;">Informatika - FT UHO • 2025</p>
<p style="color: #888; font-size: 13px; margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px;">© 2025 EraPhone BI Suite</p>
</div>
""", unsafe_allow_html=True)
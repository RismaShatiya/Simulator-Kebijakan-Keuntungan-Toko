import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Simulator Kebijakan Keuntungan",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background-color: #0F172A;
}

.main .block-container {
    padding: 1.5rem 2rem 2rem 2rem;
    max-width: 1280px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1E293B;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Header */
.header-wrap {
    background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 100%);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.header-wrap::before {
    content: '';
    position: absolute;
    width: 320px;
    height: 320px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
    top: -100px;
    right: -80px;
}

.header-wrap::after {
    content: '';
    position: absolute;
    width: 180px;
    height: 180px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
    bottom: -60px;
    left: 40%;
}

.header-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: white;
    margin: 0 0 8px 0;
    position: relative;
    z-index: 1;
}

.header-sub {
    font-size: 14px;
    color: rgba(255,255,255,0.72);
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
    max-width: 580px;
}

.header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    position: relative;
    z-index: 1;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25) !important;
}

[data-testid="metric-container"] label {
    color: #94A3B8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Section labels */
.section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7C3AED;
    margin-bottom: 6px;
}

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 16px;
}

/* Sidebar styling */
.sidebar-heading {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid #334155;
}

.sidebar-info {
    background: #0F172A;
    border: 1px solid #334155;
    border-left: 3px solid #7C3AED;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 8px;
}

.sidebar-info p {
    color: #94A3B8;
    font-size: 13px;
    margin: 0;
    line-height: 1.7;
}

.sidebar-info strong {
    color: #CBD5E1;
}

/* Slider labels */
.slider-label {
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
    margin-bottom: 4px;
    letter-spacing: 0.04em;
}

/* Stacked value label for sliders */
.stSlider label {
    color: #CBD5E1 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Success / info boxes */
.stSuccess {
    background: #064E3B !important;
    border: 1px solid #10B981 !important;
    border-radius: 12px !important;
    color: #A7F3D0 !important;
}

.stInfo {
    background: #1E1B4B !important;
    border: 1px solid #6D28D9 !important;
    border-radius: 12px !important;
    color: #C4B5FD !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid #334155 !important;
}

/* Expander */
details {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

/* Divider */
hr {
    border-color: #334155 !important;
    margin: 20px 0 !important;
}

/* Buttons */
.stButton button {
    background: #7C3AED !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: #6D28D9 !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.3) !important;
}

/* Caption */
.stCaption {
    color: #475569 !important;
    font-size: 12px !important;
}

/* Subheader override */
h3 {
    color: #F1F5F9 !important;
}

/* stat cards */
.stat-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px 22px;
}
.stat-card .stat-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 8px;
}
.stat-card .stat-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #F1F5F9;
}

/* divider line */
.divider {
    height: 1px;
    background: #1E293B;
    border: none;
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA TRAINING
# ==================================================
X_train = np.array([
    [5, 10],
    [10, 20],
    [15, 5],
    [20, 25],
    [25, 15]
])

y_train = np.array([50, 80, 110, 90, 150])

# ==================================================
# MODEL
# ==================================================
model = LinearRegression()
model.fit(X_train, y_train)

# ==================================================
# BASELINE
# ==================================================
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# ==================================================
# FUNCTION
# ==================================================
def run_simulation(iklan, diskon):
    pred = model.predict(np.array([[iklan, diskon]]))[0]
    delta = pred - baseline_pred
    return pred, delta

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="header-wrap">
    <div class="header-badge">📊 Machine Learning · Simulasi Bisnis</div>
    <h1 class="header-title">Simulator Kebijakan Keuntungan Toko</h1>
    <p class="header-sub">
        Analisis dampak perubahan anggaran iklan dan besaran diskon
        terhadap estimasi keuntungan secara real-time menggunakan model Linear Regression.
    </p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown('<div class="sidebar-heading">⚙️ Pengaturan Simulasi</div>', unsafe_allow_html=True)

    iklan_slider = st.slider(
        "💰 Anggaran Iklan (Juta Rp)",
        min_value=0,
        max_value=50,
        value=10,
        help="Geser untuk mengubah anggaran iklan"
    )

    diskon_slider = st.slider(
        "🏷️ Besaran Diskon (%)",
        min_value=0,
        max_value=50,
        value=10,
        help="Geser untuk mengubah persentase diskon"
    )

    st.markdown("""
    <div class="sidebar-info">
        <p><strong>📌 Titik Baseline</strong><br>
        Iklan &nbsp; : <strong>Rp 10 Juta</strong><br>
        Diskon : <strong>10%</strong><br>
        Prediksi baseline dihitung otomatis sebagai pembanding.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Model: Linear Regression · Fitur: 2 variabel")

# ==================================================
# PREDIKSI
# ==================================================
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

# ==================================================
# KPI METRICS
# ==================================================
st.markdown('<div class="section-label">Ringkasan</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Hasil Prediksi Skenario</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🎯 Prediksi Keuntungan",
        value=f"Rp {hasil_pred:.2f} Jt",
        delta=f"{delta:+.2f} Jt vs baseline"
    )

with col2:
    st.metric(
        label="📍 Keuntungan Baseline",
        value=f"Rp {baseline_pred:.2f} Jt"
    )

with col3:
    pct = (delta / baseline_pred * 100) if baseline_pred != 0 else 0
    status = "🟢 Meningkat" if delta > 0 else ("🔴 Menurun" if delta < 0 else "⚪ Tidak Berubah")
    st.metric(
        label="📈 Status",
        value=status,
        delta=f"{pct:+.1f}% dari baseline"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# CHARTS — 2 columns
# ==================================================
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown('<div class="section-label">Visualisasi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Perbandingan Skenario</div>', unsafe_allow_html=True)

    plot_df = pd.DataFrame({
        "Skenario": ["Baseline", "Intervensi"],
        "Keuntungan": [baseline_pred, hasil_pred],
        "Warna": ["#4F46E5", "#7C3AED" if delta >= 0 else "#EF4444"]
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=plot_df["Skenario"],
        y=plot_df["Keuntungan"],
        marker=dict(
            color=["#4F46E5", "#7C3AED" if delta >= 0 else "#EF4444"],
            line=dict(color="rgba(0,0,0,0)", width=0),
            cornerradius=8,
        ),
        text=[f"Rp {v:.2f} Jt" for v in plot_df["Keuntungan"]],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=13, family="Inter"),
        width=0.45
    ))

    fig.update_layout(
        height=340,
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=13, color="#CBD5E1"),
            title=""
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            gridwidth=1,
            tickfont=dict(size=11, color="#64748B"),
            title="Keuntungan (Juta Rp)"
        ),
        margin=dict(t=20, b=10, l=10, r=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.markdown('<div class="section-label">Kontribusi Variabel</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Bobot Fitur Model</div>', unsafe_allow_html=True)

    coef_df = pd.DataFrame({
        "Variabel": ["Anggaran Iklan", "Besaran Diskon"],
        "Koefisien": model.coef_
    })

    fig2 = go.Figure(go.Bar(
        x=coef_df["Koefisien"],
        y=coef_df["Variabel"],
        orientation='h',
        marker=dict(
            color=["#06B6D4", "#8B5CF6"],
            cornerradius=6
        ),
        text=[f"{v:.2f}" for v in coef_df["Koefisien"]],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=12)
    ))

    fig2.update_layout(
        height=340,
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="#334155", title="Koefisien"),
        yaxis=dict(showgrid=False, tickfont=dict(color="#CBD5E1", size=12)),
        margin=dict(t=20, b=10, l=10, r=40),
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# HISTORY TRACKING
# ==================================================
if "history" not in st.session_state:
    st.session_state.history = []

new_data = {
    "Iklan (Juta)": iklan_slider,
    "Diskon (%)": diskon_slider,
    "Prediksi Keuntungan (Juta)": round(hasil_pred, 2),
    "Δ dari Baseline (Juta)": round(delta, 2)
}

if len(st.session_state.history) == 0 or st.session_state.history[-1] != new_data:
    st.session_state.history.append(new_data)

history_df = pd.DataFrame(st.session_state.history)

# ==================================================
# STATISTIK ROW
# ==================================================
st.markdown('<div class="section-label">Statistik</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Ringkasan Semua Simulasi</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🔢 Total Simulasi", len(history_df))

with c2:
    st.metric(
        "🏆 Keuntungan Tertinggi",
        f"Rp {history_df['Prediksi Keuntungan (Juta)'].max():.2f} Jt"
    )

with c3:
    st.metric(
        "📊 Rata-rata Keuntungan",
        f"Rp {history_df['Prediksi Keuntungan (Juta)'].mean():.2f} Jt"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# RANKING TABLE
# ==================================================
ranking_df = history_df.sort_values(
    by="Prediksi Keuntungan (Juta)",
    ascending=False
).reset_index(drop=True)
ranking_df.index = ranking_df.index + 1
ranking_df.index.name = "Rank"

st.markdown('<div class="section-label">Peringkat</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Skenario Terbaik</div>', unsafe_allow_html=True)

# Best scenario callout
if len(ranking_df) > 0:
    best = ranking_df.iloc[0]
    st.success(
        f"🏆 **Skenario terbaik** menghasilkan **Rp {best['Prediksi Keuntungan (Juta)']} Juta** "
        f"— Iklan **Rp {best['Iklan (Juta)']} Jt** · Diskon **{best['Diskon (%)']}%**"
    )

st.dataframe(ranking_df, use_container_width=True, height=260)

# ==================================================
# HISTORY EXPANDER
# ==================================================
with st.expander("📋 Lihat Riwayat Lengkap Simulasi"):
    st.dataframe(history_df, use_container_width=True)

st.divider()

# ==================================================
# RESET + FOOTER
# ==================================================
col_btn, col_cap = st.columns([1, 4])
with col_btn:
    if st.button("🔄 Reset History"):
        st.session_state.history = []
        st.rerun()

with col_cap:
    st.caption("Simulator Kebijakan Keuntungan Toko · Powered by Streamlit & Scikit-learn · Linear Regression Model")

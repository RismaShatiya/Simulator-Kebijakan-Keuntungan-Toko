```python
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression
from PIL import Image

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Simulator Kebijakan Keuntungan",
    page_icon="logo.png",  # ganti dengan logo Anda
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.header-box{
    background: linear-gradient(135deg,#1E3A8A,#2563EB);
    padding:25px;
    border-radius:18px;
    color:white;
    margin-bottom:20px;
}

.metric-card{
    background:white;
    padding:15px;
    border-radius:12px;
    border:1px solid #E5E7EB;
}

[data-testid="metric-container"]{
    background-color:white;
    border:1px solid #E5E7EB;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
}

.stDataFrame{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA TRAINING
# ==================================================
X_train = np.array([
    [5,10],
    [10,20],
    [15,5],
    [20,25],
    [25,15]
])

y_train = np.array([
    50,
    80,
    110,
    90,
    150
])

# ==================================================
# MODEL
# ==================================================
model = LinearRegression()
model.fit(X_train, y_train)

# ==================================================
# BASELINE
# ==================================================
baseline_input = np.array([[10,10]])
baseline_pred = model.predict(baseline_input)[0]

# ==================================================
# FUNCTION
# ==================================================
def run_simulation(iklan, diskon):
    pred = model.predict(np.array([[iklan,diskon]]))[0]
    delta = pred - baseline_pred
    return pred, delta

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="header-box">
    <h1>Simulator Kebijakan Keuntungan Toko</h1>
    <p>
    Analisis dampak perubahan anggaran iklan dan diskon
    terhadap keuntungan menggunakan Machine Learning.
    </p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:

    try:
        logo = Image.open("logo.png")
        st.image(logo, width=180)
    except:
        pass

    st.markdown("## Pengaturan Simulasi")

    iklan_slider = st.slider(
        "Anggaran Iklan (Juta Rupiah)",
        min_value=0,
        max_value=50,
        value=10
    )

    diskon_slider = st.slider(
        "Besaran Diskon (%)",
        min_value=0,
        max_value=50,
        value=10
    )

    st.divider()

    st.info("""
Baseline

• Iklan : 10 Juta

• Diskon : 10%
""")

# ==================================================
# PREDIKSI
# ==================================================
hasil_pred, delta = run_simulation(
    iklan_slider,
    diskon_slider
)

# ==================================================
# KPI
# ==================================================
st.subheader("Ringkasan Hasil")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Prediksi Keuntungan",
        f"Rp {hasil_pred:.2f} Jt",
        f"{delta:.2f} Jt"
    )

with col2:
    st.metric(
        "Keuntungan Baseline",
        f"Rp {baseline_pred:.2f} Jt"
    )

with col3:
    status = "Meningkat" if delta > 0 else "Menurun"
    st.metric(
        "Status",
        status
    )

# ==================================================
# GRAFIK
# ==================================================
st.subheader("Perbandingan Baseline dan Skenario")

plot_df = pd.DataFrame({
    "Skenario":[
        "Baseline",
        "Intervensi"
    ],
    "Keuntungan":[
        baseline_pred,
        hasil_pred
    ]
})

fig = px.bar(
    plot_df,
    x="Skenario",
    y="Keuntungan",
    text_auto=".2f"
)

fig.update_layout(
    height=450,
    xaxis_title="",
    yaxis_title="Keuntungan (Juta Rupiah)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# HISTORY
# ==================================================
if "history" not in st.session_state:
    st.session_state.history = []

new_data = {
    "Iklan (Juta)": iklan_slider,
    "Diskon (%)": diskon_slider,
    "Prediksi Keuntungan (Juta)": round(hasil_pred,2),
    "Perubahan dari Baseline (Juta)": round(delta,2)
}

if (
    len(st.session_state.history)==0
    or st.session_state.history[-1] != new_data
):
    st.session_state.history.append(new_data)

history_df = pd.DataFrame(st.session_state.history)

# ==================================================
# STATISTIK
# ==================================================
st.subheader("Statistik Simulasi")

c1,c2,c3 = st.columns(3)

with c1:
    st.metric(
        "Jumlah Simulasi",
        len(history_df)
    )

with c2:
    st.metric(
        "Keuntungan Tertinggi",
        f"Rp {history_df['Prediksi Keuntungan (Juta)'].max():.2f} Jt"
    )

with c3:
    st.metric(
        "Rata-rata Keuntungan",
        f"Rp {history_df['Prediksi Keuntungan (Juta)'].mean():.2f} Jt"
    )

# ==================================================
# RANKING
# ==================================================
ranking_df = history_df.sort_values(
    by="Prediksi Keuntungan (Juta)",
    ascending=False
).reset_index(drop=True)

ranking_df.index = ranking_df.index + 1

st.subheader("Ranking Skenario")

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==================================================
# SKENARIO TERBAIK
# ==================================================
if len(ranking_df) > 0:

    best = ranking_df.iloc[0]

    st.success(
        f"""
Skenario terbaik menghasilkan keuntungan sebesar
Rp {best['Prediksi Keuntungan (Juta)']} Juta
dengan anggaran iklan {best['Iklan (Juta)']} Juta
dan diskon {best['Diskon (%)']}%.
"""
    )

# ==================================================
# HISTORY
# ==================================================
with st.expander("Lihat Riwayat Simulasi"):

    st.dataframe(
        history_df,
        use_container_width=True
    )

# ==================================================
# RESET
# ==================================================
st.divider()

if st.button("Reset History"):

    st.session_state.history = []

    st.rerun()

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")

st.caption(
    "Simulator Kebijakan Keuntungan Toko | Streamlit Dashboard"
)
```

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Simulator Kebijakan Keuntungan",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title-box {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(90deg, #4F46E5, #7C3AED);
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.10);
}

.stat-card {
    text-align: center;
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.10);
}

div[data-testid="metric-container"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.10);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA TRAINING
# ==========================================
X_train = np.array([
    [5, 10],
    [10, 20],
    [15, 5],
    [20, 25],
    [25, 15]
])

y_train = np.array([
    50,
    80,
    110,
    90,
    150
])

# ==========================================
# TRAIN MODEL
# ==========================================
model = LinearRegression()
model.fit(X_train, y_train)

# ==========================================
# BASELINE
# ==========================================
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# ==========================================
# FUNCTION SIMULASI
# ==========================================
def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])
    prediction = model.predict(intervention_input)[0]
    delta_y = prediction - baseline_pred
    return prediction, delta_y

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="title-box">
    <h1>🚀 Simulator Kebijakan Keuntungan Toko</h1>
</div>
""", unsafe_allow_html=True)

st.write(
    "Gunakan slider pada sidebar untuk mengubah kebijakan iklan dan diskon, "
    "kemudian lihat dampaknya terhadap keuntungan toko."
)

# ==========================================
# SIDEBAR
# ==========================================

iklan_slider = st.sidebar.slider(
    "Anggaran Iklan (Juta)",
    min_value=0,
    max_value=50,
    value=10
)

diskon_slider = st.sidebar.slider(
    "Besaran Diskon (%)",
    min_value=0,
    max_value=50,
    value=10
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Baseline**
    
    Iklan = 10 Juta
    
    Diskon = 10%
    """
)

# ==========================================
# JALANKAN SIMULASI
# ==========================================
hasil_pred, delta = run_simulation(
    iklan_slider,
    diskon_slider
)

# ==========================================
# HASIL PREDIKSI
# ==========================================
st.subheader("Hasil Simulasi")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Prediksi Keuntungan",
        value=f"Rp {hasil_pred:.2f} Juta",
        delta=f"{delta:.2f} Juta"
    )

with col2:
    if delta > 0:
        st.success(
            f"Keuntungan meningkat sebesar Rp {delta:.2f} Juta dibanding baseline."
        )
    elif delta < 0:
        st.error(
            f"Keuntungan menurun sebesar Rp {abs(delta):.2f} Juta dibanding baseline."
        )
    else:
        st.info("Tidak ada perubahan dibanding baseline.")

# ==========================================
# VISUALISASI
# ==========================================
st.subheader("Perbandingan Baseline vs Intervensi")

data_plot = pd.DataFrame({
    "Skenario": ["Baseline", "Intervensi"],
    "Keuntungan": [baseline_pred, hasil_pred]
})

st.bar_chart(
    data_plot.set_index("Skenario")
)

# ==========================================
# HISTORY
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

new_data = {
    "Iklan (Juta)": iklan_slider,
    "Diskon (%)": diskon_slider,
    "Prediksi Keuntungan (Juta)": round(hasil_pred, 2),
    "Perubahan dari Baseline (Juta)": round(delta, 2)
}

if (
    len(st.session_state.history) == 0
    or st.session_state.history[-1] != new_data
):
    st.session_state.history.append(new_data)

history_df = pd.DataFrame(st.session_state.history)

# ==========================================
# RINGKASAN
# ==========================================
st.subheader("Ringkasan Simulasi")

c1, c2, c3 = st.columns(3)

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

# ==========================================
# HISTORY TABLE
# ==========================================
with st.expander("Lihat History Simulasi", expanded=False):
    st.dataframe(
        history_df,
        use_container_width=True
    )

# ==========================================
# RANKING
# ==========================================
ranking_df = history_df.sort_values(
    by="Prediksi Keuntungan (Juta)",
    ascending=False
).reset_index(drop=True)

medals = []

for i in range(len(ranking_df)):
    if i == 0:
        medals.append("🥇")
    elif i == 1:
        medals.append("🥈")
    elif i == 2:
        medals.append("🥉")
    else:
        medals.append(str(i + 1))

ranking_df.insert(0, "Ranking", medals)

st.subheader("Ranking Skenario Terbaik")

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==========================================
# TOP SCENARIO
# ==========================================
if len(ranking_df) > 0:

    best = ranking_df.iloc[0]

    st.success(
        f"""
        Skenario Terbaik Saat Ini
        
        Iklan: {best['Iklan (Juta)']} Juta
        
        Diskon: {best['Diskon (%)']}%
        
        Prediksi Keuntungan: Rp {best['Prediksi Keuntungan (Juta)']} Juta
        """
    )

# ==========================================
# RESET HISTORY
# ==========================================
st.markdown("---")

if st.button("🗑️ Hapus Seluruh History"):
    st.session_state.history = []
    st.rerun()

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption(
    "Dibuat menggunakan Streamlit + Machine Learning (Linear Regression)"
)


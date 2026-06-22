import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
# 1. Menyiapkan data historis sederhana
# Fitur: [Iklan (Juta), Diskon (%)]
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])

# Target: Keuntungan (Juta)
y_train = np.array([50, 80, 110, 90, 150])

# 2. Melatih model (Mesin Replika)
model = LinearRegression().fit(X_train, y_train)

# 3. Menetapkan Skenario Dasar (Baseline)
# Kondisi saat ini: Iklan 10 Juta, Diskon 10%
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]
print(f"Prediksi Keuntungan Baseline: Rp {baseline_pred:.2f} Juta")

def run_simulation(new_iklan, new_diskon):
    # Input baru dari user (Intervensi)
    intervention_input = np.array([[new_iklan, new_diskon]])
    # Prediksi hasil intervensi
    prediction = model.predict(intervention_input)[0]
    # Menghitung Delta (Selisih)
    delta_y = prediction - baseline_pred
    return prediction, delta_y

import streamlit as st
st.markdown(
    "<h1 style='font-size:50px;'>Simulator Kebijakan Keuntungan Toko 🚀</h1>",
    unsafe_allow_html=True
)
st.write("Gunakan slider untuk menguji skenario 'What-If'.")

# --- SIDEBAR: Variabel Kontrol ---
st.sidebar.header("Tuas Kebijakan (Intervensi)")
iklan_slider = st.sidebar.slider("Anggaran Iklan (Juta)", 0, 50, 10)
diskon_slider = st.sidebar.slider("Besaran Diskon (%)", 0, 50, 10)

# --- ENGINE: Jalankan Simulasi ---
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

# --- UI: Tampilkan Hasil ---
col1, col2 = st.columns(2)
col1.metric("Prediksi Keuntungan", f"Rp {hasil_pred:.2f} Jt", f"{delta:.2f} Jt")
col2.write(f"Skenario ini menghasilkan perubahan sebesar {delta:.2f} Juta dibandingkan kondisi baseline.")

# Visualisasi Perbandingan
data_plot = pd.DataFrame({
    'Skenario': ['Baseline', 'Intervensi'],
    'Keuntungan': [baseline_pred, hasil_pred]
    })
st.bar_chart(data=data_plot, x='Skenario', y='Keuntungan')

# HISTORY DAN RANKING 

# Membuat session state untuk menyimpan riwayat
if 'history' not in st.session_state:
    st.session_state.history = []

# Simpan skenario terbaru
st.session_state.history.append({
    "Iklan (Juta)": iklan_slider,
    "Diskon (%)": diskon_slider,
    "Prediksi Keuntungan (Juta)": round(hasil_pred, 2),
    "Perubahan dari Baseline (Juta)": round(delta, 2)
})

# Membuat DataFrame history
history_df = pd.DataFrame(st.session_state.history)

# keuntungan tertinggi ke terendah
ranking_df = history_df.sort_values(
    by="Prediksi Keuntungan (Juta)",
    ascending=False
).reset_index(drop=True)

# ranking
ranking_df.insert(0, "Ranking", range(1, len(ranking_df) + 1))

st.subheader("📊 History Skenario")
st.dataframe(history_df, use_container_width=True)

st.subheader("🏆 Ranking Skenario Terbaik")
st.dataframe(ranking_df, use_container_width=True)

# Tombol hapus history
if st.button("🗑️ Hapus History"):
    st.session_state.history = []
    st.rerun()
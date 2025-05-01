import streamlit as st
import numpy as np
import pandas as pd
import colour
import matplotlib.pyplot as plt

# Cấu hình trang web
st.set_page_config(page_title="Khoa học màu sắc", layout="wide")

# Sidebar menu
menu = st.sidebar.selectbox(
    "📘 Chọn chức năng",
    [
        "🔰 Giới thiệu",
        "🎨 Chuyển đổi sRGB ↔ XYZ",
        "📈 Vẽ sơ đồ màu CIE 1931",
        "📊 Tính XYZ từ phổ phản xạ (CSV)"
    ]
)

# 🧾 Giới thiệu
if menu == "🔰 Giới thiệu":
    st.title("👋 Chào mừng đến với môn Khoa học Màu sắc")
    st.markdown("""
    ---
    🧑‍🎓 **Họ tên:** Nguyễn Gia Khánh  
    🆔 **MSSV:** 21158104  

    🌈 Đây là ứng dụng hỗ trợ học tập môn *Khoa học màu sắc* trong ngành in.  
    Sử dụng thư viện Python `colour-science`, `Streamlit`, và các công cụ xử lý phổ màu để mô phỏng, tính toán và hiển thị các hệ màu thông dụng.
    ---
    """)

# 🎨 Chuyển đổi không gian màu
elif menu == "🎨 Chuyển đổi sRGB ↔ XYZ":
    st.title("🎨 Chuyển đổi giữa không gian màu sRGB và XYZ")
    mode = st.radio("Chọn loại chuyển đổi:", ("sRGB → XYZ", "XYZ → sRGB"))

    col1, _, _ = st.columns(3)
    with col1:
        if mode == "sRGB → XYZ":
            R = st.number_input('Nhập R (0–255):', min_value=0.0, max_value=255.0, value=120.0)
            G = st.number_input('Nhập G (0–255):', min_value=0.0, max_value=255.0, value=200.0)
            B = st.number_input('Nhập B (0–255):', min_value=0.0, max_value=255.0, value=150.0)

            if st.button("Chuyển sang XYZ"):
                rgb = np.array([R/255.0, G/255.0, B/255.0])
                xyz = colour.sRGB_to_XYZ(rgb)
                st.success(f"👉 Kết quả: X = {xyz[0]*100:.2f}, Y = {xyz[1]*100:.2f}, Z = {xyz[2]*100:.2f}")

        else:  # XYZ → sRGB
            X = st.number_input('Nhập X:', value=41.24)
            Y = st.number_input('Nhập Y:', value=21.26)
            Z = st.number_input('Nhập Z:', value=1.93)

            if st.button("Chuyển sang sRGB"):
                xyz = np.array([X/100.0, Y/100.0, Z/100.0])
                rgb = colour.XYZ_to_sRGB(xyz)
                r = np.clip(rgb[0]*255, 0, 255)
                g = np.clip(rgb[1]*255, 0, 255)
                b = np.clip(rgb[2]*255, 0, 255)
                st.success(f"👉 Kết quả: R = {r:.0f}, G = {g:.0f}, B = {b:.0f}")

# 📈 Vẽ sơ đồ màu CIE
elif menu == "📈 Vẽ sơ đồ màu CIE 1931":
    st.title("📈 Sơ đồ màu CIE 1931 Chromaticity Diagram")
    st.write("Sơ đồ này minh họa toàn bộ phổ màu mà mắt người có thể nhìn thấy.")
    fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)
    st.pyplot(fig)

# 📊 Tính XYZ từ phổ phản xạ (CSV)
elif menu == "📊 Tính XYZ từ phổ phản xạ (CSV)":
    st.title("📊 Tính giá trị XYZ từ phổ phản xạ")
    uploaded_file = st.file_uploader("Tải lên file CSV chứa phổ phản xạ", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📄 **Dữ liệu phổ xem trước:**")
        st.dataframe(df.head(10))

        if st.button("Tính XYZ"):
            data = {int(row[0]): row[1] for row in df.values}
            sd = colour.SpectralDistribution(data)
            cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
            illuminant = colour.SDS_ILLUMINANTS['D65']

            xyz = colour.sd_to_XYZ(sd, cmfs, illuminant)
            st.success(f"✅ Kết quả: X = {xyz[0]:.2f}, Y = {xyz[1]:.2f}, Z = {xyz[2]:.2f}")

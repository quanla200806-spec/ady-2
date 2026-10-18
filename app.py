# ==============================================================================
# HỆ THỐNG TRA CỨU HỒ SƠ BỆNH NHÂN TIM MẠCH TỪ SQL SERVER
# Đồ án môn học: ADY201m
# Tác giả: Nhóm sinh viên thực hiện
# Công nghệ: Python, Streamlit, Microsoft SQL Server
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. KHAI BÁO CÁC THƯ VIỆN CẦN THIẾT
# ------------------------------------------------------------------------------
import streamlit as st                      # Thư viện tạo giao diện web ứng dụng
import pandas as pd                         # Thư viện xử lý và hiển thị bảng dữ liệu
import urllib.parse                         # Thư viện mã hóa chuỗi kết nối CSDL an toàn
from sqlalchemy import create_engine, text  # Thư viện tạo động cơ kết nối SQL Server

# Cấu hình giao diện trang web (đặt tiêu đề và mở rộng bố cục trang)
st.set_page_config(
    page_title="Hệ Thống Tra Cứu Hồ Sơ Bệnh Nhân",
    page_icon="🏥",
    layout="wide"
)

# ------------------------------------------------------------------------------
# 2. HÀM KẾT NỐI CƠ SỞ DỮ LIỆU SQL SERVER
# ------------------------------------------------------------------------------
def ket_noi_sql():
    """
    Hàm kết nối tới Microsoft SQL Server bằng Windows Authentication.
    Viết ngắn gọn, dễ hiểu để trả lời vấn đáp với giảng viên.
    """
    chuoi_cau_hinh = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=localhost;"
        "Database=ady;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    chuoi_ma_hoa = urllib.parse.quote_plus(chuoi_cau_hinh)
    dong_co = create_engine(f"mssql+pyodbc:///?odbc_connect={chuoi_ma_hoa}")
    return dong_co

# ------------------------------------------------------------------------------
# 3. THANH BÊN (SIDEBAR): KIỂM TRA KẾT NỐI CƠ SỞ DỮ LIỆU
# ------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=80)
    st.title("Quản Trị Hệ Thống")
    st.write("**Máy chủ (Server):** `localhost`")
    st.write("**Cơ sở dữ liệu:** `ady`")
    st.write("**Bảng dữ liệu:** `dbo.heart_data`")
    st.divider()
    
    # Nút bấm kiểm tra xem đã thông mạch với SQL Server chưa
    st.subheader("Kiểm tra kết nối")
    if st.button("🔌 Kiểm tra kết nối SQL", use_container_width=True):
        try:
            # Tạo kết nối
            dong_co = ket_noi_sql()
            # Thực thi truy vấn đếm tổng số dòng bệnh nhân trong CSDL
            with dong_co.connect() as ket_noi:
                ket_qua = ket_noi.execute(text("SELECT COUNT(*) FROM dbo.heart_data")).fetchone()
                tong_so_benh_nhan = ket_qua[0]
            
            # Thông báo kết quả
            st.success("Kết nối SQL Server thành công!")
            st.info(f"Tổng số bệnh nhân trong CSDL: **{tong_so_benh_nhan:,}**")
        except Exception as loi:
            st.error(f"Lỗi kết nối CSDL: {loi}")
            
    st.divider()
    st.caption("Đồ án môn học ADY201m - FPT University")

# ------------------------------------------------------------------------------
# 4. GIAO DIỆN CHÍNH: TRA CỨU HỒ SƠ BỆNH NHÂN
# ------------------------------------------------------------------------------
st.title("🏥 HỆ THỐNG TRA CỨU HỒ SƠ BỆNH NHÂN TIM MẠCH")
st.write("Tra cứu trực tiếp hồ sơ bệnh án lâm sàng từ cơ sở dữ liệu Microsoft SQL Server.")
st.divider()

# Tạo bố cục gồm 3 cột: Ô nhập ID, Nút tìm kiếm, Nút tải 10 dòng mẫu
cot_nhap, cot_nut_tim, cot_nut_mau = st.columns([3, 2, 2])

with cot_nhap:
    # Ô nhập mã ID bệnh nhân (số nguyên dương)
    ma_id_nhap = st.number_input(
        "Nhập mã ID bệnh nhân cần tra cứu:",
        min_value=1,
        step=1,
        value=1,
        help="Nhập số thứ tự ID bệnh nhân (ví dụ: 1, 2, 3...)"
    )

with cot_nut_tim:
    st.write("") # Dòng trống căn chỉnh độ cao nút bấm
    st.write("")
    nut_tim_benh_nhan = st.button("🔎 Tìm bệnh nhân", use_container_width=True, type="primary")

with cot_nut_mau:
    st.write("") # Dòng trống căn chỉnh độ cao nút bấm
    st.write("")
    nut_tai_mau = st.button("📋 Tải 10 bệnh nhân mẫu", use_container_width=True)

# ------------------------------------------------------------------------------
# 5. XỬ LÝ SỰ KIỆN: KHI BẤM NÚT "TẢI 10 BỆNH NHÂN MẪU"
# ------------------------------------------------------------------------------
if nut_tai_mau:
    try:
        # Lấy động cơ kết nối CSDL
        dong_co = ket_noi_sql()
        
        # Câu lệnh SQL lấy 10 bản ghi đầu tiên
        cau_lenh_sql_mau = "SELECT TOP 10 * FROM dbo.heart_data ORDER BY id ASC"
        
        # Đọc dữ liệu từ SQL Server vào DataFrame
        du_lieu_mau_df = pd.read_sql(cau_lenh_sql_mau, con=dong_co)
        
        if not du_lieu_mau_df.empty:
            st.info("Danh sách 10 bệnh nhân đầu tiên trong cơ sở dữ liệu:")
            st.dataframe(du_lieu_mau_df, use_container_width=True)
        else:
            st.warning("Bảng dbo.heart_data hiện đang rỗng (chưa có dòng dữ liệu nào)!")
    except Exception as loi:
        st.error(f"Lỗi khi tải dữ liệu mẫu: {loi}")

# ------------------------------------------------------------------------------
# 6. XỬ LÝ SỰ KIỆN: KHI BẤM NÚT "TÌM BỆNH NHÂN"
# ------------------------------------------------------------------------------
if nut_tim_benh_nhan:
    try:
        # Lấy động cơ kết nối CSDL
        dong_co = ket_noi_sql()
        
        # Câu lệnh SQL truy vấn có tham số an toàn :ma_id (chống SQL Injection)
        cau_lenh_sql_tim = text("SELECT * FROM dbo.heart_data WHERE id = :ma_id")
        
        # Thực thi truy vấn
        with dong_co.connect() as ket_noi:
            ket_qua_tim_kiem = pd.read_sql(cau_lenh_sql_tim, con=ket_noi, params={"ma_id": ma_id_nhap})
        
        # Kiểm tra kết quả trả về
        if not ket_qua_tim_kiem.empty:
            # Lấy dòng bệnh nhân tìm được
            benh_nhan = ket_qua_tim_kiem.iloc[0]
            
            st.success(f"Đã tìm thấy hồ sơ bệnh nhân mang mã ID = **{ma_id_nhap}**!")
            st.markdown(f"### 📋 HỒ SƠ Y TẾ BỆNH NHÂN #{int(benh_nhan['id'])}")
            
            # --- HIỂN THỊ 4 THẺ THÔNG TIN NỔI BẬT (st.metric) ---
            cot_tuoi, cot_gioi_tinh, cot_huyet_ap, cot_bmi = st.columns(4)
            
            with cot_tuoi:
                # Tuổi theo năm
                st.metric(label="Tuổi", value=f"{int(benh_nhan['age_year'])} tuổi")
                
            with cot_gioi_tinh:
                # 1: Nữ, 2: Nam
                gioi_tinh_chu = "Nữ" if benh_nhan['gender'] == 1 else "Nam"
                st.metric(label="Giới tính", value=gioi_tinh_chu)
                
            with cot_huyet_ap:
                # Huyết áp tâm thu / tâm trương
                huyet_ap_chu = f"{int(benh_nhan['ap_hi'])} / {int(benh_nhan['ap_lo'])}"
                st.metric(label="Huyết áp (mmHg)", value=huyet_ap_chu)
                
            with cot_bmi:
                # Chỉ số BMI
                st.metric(label="Chỉ số BMI", value=f"{float(benh_nhan['BMI']):.2f}")
                
            # --- HIỂN THỊ TOÀN BỘ CÁC CHỈ SỐ CÒN LẠI DƯỚI DẠNG BẢNG (st.dataframe) ---
            st.write("#### Chi tiết các chỉ số lâm sàng & sinh hoạt:")
            
            bang_chi_tiet = pd.DataFrame({
                "Chỉ số lâm sàng": [
                    "Tuổi (theo ngày)",
                    "Chiều cao (cm)",
                    "Cân nặng (kg)",
                    "Chỉ số Cholesterol",
                    "Chỉ số Glucose",
                    "Thói quen hút thuốc",
                    "Uống rượu bia",
                    "Vận động thể lực",
                    "Kết quả bệnh tim mạch"
                ],
                "Giá trị ghi nhận": [
                    f"{int(benh_nhan['age'])} ngày",
                    f"{int(benh_nhan['height'])} cm",
                    f"{float(benh_nhan['weight']):.1f} kg",
                    "Bình thường (1)" if benh_nhan['cholesterol'] == 1 else ("Cao (2)" if benh_nhan['cholesterol'] == 2 else "Rất cao (3)"),
                    "Bình thường (1)" if benh_nhan['gluc'] == 1 else ("Cao (2)" if benh_nhan['gluc'] == 2 else "Rất cao (3)"),
                    "Có hút thuốc (1)" if benh_nhan['smoke'] == 1 else "Không hút thuốc (0)",
                    "Có uống rượu bia (1)" if benh_nhan['alco'] == 1 else "Không uống (0)",
                    "Có vận động (1)" if benh_nhan['active'] == 1 else "Ít vận động (0)",
                    "⚠️ CÓ BỆNH TIM (1)" if benh_nhan['cardio'] == 1 else "✅ KHỎE MẠNH (0)"
                ]
            })
            st.dataframe(bang_chi_tiet, use_container_width=True, hide_index=True)
            
        else:
            st.warning(f"Không tìm thấy bệnh nhân nào có mã ID = **{ma_id_nhap}** trong CSDL.")
            
    except Exception as loi:
        st.error(f"Lỗi khi thực hiện truy vấn CSDL: {loi}")

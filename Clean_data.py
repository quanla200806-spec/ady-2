
import pandas as pd
from pathlib import Path

path = Path(r"abc.csv")

if not path.exists():
    raise FileNotFoundError(f"Không tìm thấy file: {path}")

df = pd.read_csv(path, sep=';')

print('1. Dataset có bao nhiêu dòng, bao nhiêu cột')
print(df.shape)

print('2. Kiểm tra kiểu dữ liệu')
df.info()

print('3. Kiểm tra dữ liệu thiếu')
print(df.isnull().sum())

print('4. Thống kê mô tả')
print(df.describe().to_string())

print('5. Tỷ lệ bệnh tim')
print(df["cardio"].value_counts())

# Khởi tạo thông tin ghi nhận
so_dong_goc = len(df)

# 1. XỬ LÝ BẢN GHI TRÙNG LẶP
so_dong_trung = df.duplicated().sum()
df = df.drop_duplicates()

# 2. XỬ LÝ GIÁ TRỊ THIẾU
so_dong_thieu = df.isnull().any(axis=1).sum()
df = df.dropna()

# 3. CHUẨN HÓA KIỂU DỮ LIỆU VÀ ĐỊNH DẠNG
df["id"] = df["id"].astype(int)

# Quy đổi cột tuổi từ ngày sang năm (làm tròn xuống)
df["age_year"] = (df["age"] / 365).astype(int)

# Tính BMI
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)

# 4. NHẬN DIỆN VÀ XỬ LÝ NGOẠI LỆ BAN ĐẦU
outliers = df[
    (df["ap_hi"] < 70) |
    (df["ap_hi"] > 250) |
    (df["ap_lo"] < 40) |
    (df["ap_lo"] > 200) |
    (df["ap_lo"] > df["ap_hi"]) |
    (df["height"] < 120) |
    (df["gender"] <= 0) |
    (df["gender"] >= 3) |
    (df["cholesterol"] <= 0) |
    (df["cholesterol"] >= 4) |
    (df["gluc"] <= 0) |
    (df["gluc"] >= 4) |
    (df["smoke"] < 0) |
    (df["smoke"] > 1) |
    (df["alco"] < 0) |
    (df["alco"] > 1) |
    (df["active"] < 0) |
    (df["active"] > 1) |
    (df["cardio"] < 0) |
    (df["cardio"] > 1)
]

df_clean = df[
    (df["ap_hi"] >= 70) &
    (df["ap_hi"] <= 250) &
    (df["ap_lo"] >= 40) &
    (df["ap_lo"] <= 200) &
    (df["ap_lo"] <= df["ap_hi"]) &
    (df["height"] >= 120) &
    (df["gender"] > 0) &
    (df["gender"] < 3) &
    (df["cholesterol"] > 0) &
    (df["cholesterol"] < 4) &
    (df["gluc"] > 0) &
    (df["gluc"] < 4) &
    (df["smoke"] >= 0) &
    (df["smoke"] <= 1) &
    (df["alco"] >= 0) &
    (df["alco"] <= 1) &
    (df["active"] >= 0) &
    (df["active"] <= 1) &
    (df["cardio"] >= 0) &
    (df["cardio"] <= 1)
]

# Lưu các dòng lỗi thành 1 file riêng
outliers.to_csv("removed_outliers.csv", index=False)

# Lưu thành file sạch
df_clean.to_csv("heart_cleaned.csv", index=False)

# 8. In kết quả tổng hợp
print("=== KẾT QUẢ XỬ LÝ DỮ LIỆU ===")
print("Số dòng ban đầu:", so_dong_goc)
print("Số dòng trùng lặp đã xóa:", so_dong_trung)
print("Số dòng chứa giá trị thiếu đã xóa:", so_dong_thieu)
print("Số dòng bị loại bỏ do ngoại lệ (outliers):", len(outliers))
print("Số dòng sạch sau cùng:", len(df_clean))

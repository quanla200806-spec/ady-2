
import pandas as pd
from pathlib import Path

path = Path(r"cardio_train.csv")

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
# Bỏ cột 'id' trước vì đây là mã định danh, không dùng để phân tích và tránh làm ảnh hưởng đến việc tìm dòng trùng
if "id" in df.columns:
    df = df.drop(columns=["id"])

# Đếm số dòng trùng lặp và tiến hành xóa các dòng trùng lặp
so_dong_trung = df.duplicated().sum()
df = df.drop_duplicates()

# 2. XỬ LÝ GIÁ TRỊ THIẾU
# Bước 2.1: Bỏ các cột có toàn bộ giá trị bị thiếu (thiếu full 100%)
# axis=1: thao tác trên cột, how='all': tất cả giá trị trong cột đều bị thiếu mới xóa
df = df.dropna(axis=1, how="all")

# Bước 2.2: Bỏ các hàng có ít nhất 1 giá trị bị thiếu
# axis=0: thao tác trên hàng, how='any': chỉ cần có ít nhất 1 giá trị thiếu là xóa
so_dong_thieu = df.isnull().any(axis=1).sum()
df = df.dropna(axis=0, how="any")

# 3. CHUẨN HÓA KIỂU DỮ LIỆU VÀ ĐỊNH DẠNG
# Danh sách các cột cần định dạng về kiểu số nguyên (int)
cac_cot_so_nguyen = [
    "age", "gender", "height", "ap_hi", "ap_lo",
    "cholesterol", "gluc", "smoke", "alco", "active", "cardio"
]

# Chuẩn hóa kiểu int cho các cột số nguyên
for cot in cac_cot_so_nguyen:
    if cot in df.columns:
        df[cot] = df[cot].astype(int)

# Chuẩn hóa kiểu số thực (float) cho cột cân nặng
if "weight" in df.columns:
    df["weight"] = df["weight"].astype(float).round(1)

# Quy đổi cột tuổi từ ngày sang năm (làm tròn xuống thành số nguyên)
df["age_year"] = (df["age"] / 365).astype(int)

# Tính chỉ số BMI và làm tròn 2 chữ số thập phân
df["BMI"] = (df["weight"] / ((df["height"] / 100) ** 2)).round(2)


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
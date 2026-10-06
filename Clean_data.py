#XỬ LÝ BẢN GHI TRÙNG LẶP
#XỬ LÝ GIÁ TRỊ THIẾU
#CHUẨN HÓA KIỂU DỮ LIỆU VÀ ĐỊNH DẠNG
#NHẬN DIỆN VÀ XỬ LÝ NGOẠI LỆ BAN ĐẦU
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

# 2. Tính BMI 
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)
# print(df[df["BMI"]])

# 3. Xác định các dòng lỗi 
outliers = df[
    (df["ap_hi"] < 70) |
    (df["ap_hi"] > 250) |
    (df["ap_lo"] < 40) |
    (df["ap_lo"] > 200) |
    (df["ap_lo"] > df["ap_hi"]) |
    (df["height"] < 120)
]

# 4. Lưu các dòng lỗi
# outliers.to_excel("removed_outliers.xlsx", index=False)

# 5. Các dòng hợp lệ
df_clean = df[
    (df["ap_hi"] >= 70) &
    (df["ap_hi"] <= 250) &
    (df["ap_lo"] >= 40) &
    (df["ap_lo"] <= 200) &
    (df["ap_lo"] <= df["ap_hi"]) &
    (df["height"] >= 120)
]

# 6. Xóa cột BMI nếu không muốn lưu vào dataset chính
# df_clean = df_clean.drop("BMI", axis=1)

# 7. Lưu file sạch
df_clean.to_excel("heart_cleaned.xlsx", index=False)

# 8. In kết quả
print("Số dòng ban đầu:", len(df))
print("Số dòng bị loại:", len(outliers))
print("Số dòng sau khi làm sạch:", len(df_clean))
print("minhngao321-quângy")

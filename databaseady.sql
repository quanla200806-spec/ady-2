-- Chuyển sang làm việc trên database ady
USE ady;
GO

-- 1. Đếm tổng số lượng bệnh nhân có trong bảng
SELECT COUNT(*) AS [Tong_So_Benh_Nhan] 
FROM dbo.cleaned_cardio;
GO

-- 2. Xem 10 bệnh nhân đầu tiên (khớp với nút "Xem 10 bệnh nhân mẫu" trên web)
SELECT TOP 10 * 
FROM dbo.cleaned_cardio 
ORDER BY id ASC;
GO

-- 3. Tra cứu 1 bệnh nhân cụ thể theo ID (khớp với chức năng tìm kiếm trên web)
SELECT * 
FROM dbo.cleaned_cardio 
WHERE id = 0;
GO


-- ============================================================
-- PHẦN 4. LỌC THEO ĐỘ TUỔI
-- ============================================================

-- 4a. Lọc ra những bệnh nhân từ 30 tuổi trở lên
SELECT *
FROM dbo.cleaned_cardio
WHERE age >= 30;
GO

-- 4b. Lọc ra những bệnh nhân từ 40 tuổi trở lên
SELECT *
FROM dbo.cleaned_cardio
WHERE age >= 40;
GO

-- 4c. Lọc ra những bệnh nhân trong độ tuổi từ 30 đến 50
SELECT *
FROM dbo.cleaned_cardio
WHERE age BETWEEN 30 AND 50;
GO


-- ============================================================
-- PHẦN 5. LỌC NGƯỜI CÓ HUYẾT ÁP CAO
-- ============================================================

-- 5a. Lọc người có huyết áp tâm thu (ap_hi) từ 140 mmHg trở lên
--     (Ngưỡng tăng huyết áp độ 1 theo WHO)
SELECT *
FROM dbo.cleaned_cardio
WHERE ap_hi >= 140;
GO

-- 5b. Lọc người có huyết áp tâm thu cao nguy hiểm (140 đến 180 mmHg)
SELECT *
FROM dbo.cleaned_cardio
WHERE ap_hi BETWEEN 140 AND 180;
GO

-- 5c. Lọc người có cả huyết áp tâm thu (ap_hi) VÀ tâm trương (ap_lo) đều cao
--     ap_hi >= 140 và ap_lo >= 90 là dấu hiệu tăng huyết áp độ 1
SELECT *
FROM dbo.cleaned_cardio
WHERE ap_hi >= 140
  AND ap_lo >= 90;
GO


-- ============================================================
-- PHẦN 6. THỐNG KÊ TỔNG HỢP TOÀN BẢNG (SUM, AVG, MIN, MAX)
-- ============================================================

-- 6. Tính tổng, trung bình, min, max cho từng cột số liệu
SELECT
    COUNT(*)        AS [Tong_So_Benh_Nhan],

    AVG(age)        AS [Tuoi_Trung_Binh],
    MIN(age)        AS [Tuoi_Nho_Nhat],
    MAX(age)        AS [Tuoi_Lon_Nhat],

    AVG(height)     AS [ChieuCao_TrungBinh_cm],
    MIN(height)     AS [ChieuCao_NhoNhat_cm],
    MAX(height)     AS [ChieuCao_LonNhat_cm],

    AVG(weight)     AS [CanNang_TrungBinh_kg],
    MIN(weight)     AS [CanNang_NhoNhat_kg],
    MAX(weight)     AS [CanNang_LonNhat_kg],

    AVG(ap_hi)      AS [HuyetAp_TamThu_TrungBinh],
    MIN(ap_hi)      AS [HuyetAp_TamThu_NhoNhat],
    MAX(ap_hi)      AS [HuyetAp_TamThu_LonNhat],

    AVG(ap_lo)      AS [HuyetAp_TamTruong_TrungBinh],
    MIN(ap_lo)      AS [HuyetAp_TamTruong_NhoNhat],
    MAX(ap_lo)      AS [HuyetAp_TamTruong_LonNhat]

FROM dbo.cleaned_cardio;
GO


-- ============================================================
-- PHẦN 7. GROUP BY — THỐNG KÊ THEO NHÓM
-- ============================================================

-- 7a. Thống kê số lượng, huyết áp trung bình theo nhóm có bệnh / không có bệnh (cardio)
SELECT
    cardio                          AS [Nhom_Benh_Tim],
    COUNT(*)                        AS [So_Luong_Nguoi],
    AVG(age)                        AS [Tuoi_Trung_Binh],
    AVG(ap_hi)                      AS [HuyetAp_TamThu_TrungBinh],
    AVG(ap_lo)                      AS [HuyetAp_TamTruong_TrungBinh],
    AVG(weight)                     AS [CanNang_TrungBinh],
    AVG(cholesterol)                AS [Cholesterol_TrungBinh]
FROM dbo.cleaned_cardio
GROUP BY cardio;
GO

-- 7b. Thống kê theo mức Cholesterol: mỗi mức có bao nhiêu người, huyết áp trung bình là bao nhiêu
--     cholesterol: 1 = Bình thường, 2 = Trên chuẩn, 3 = Rất cao
SELECT
    cholesterol                     AS [Muc_Cholesterol],
    COUNT(*)                        AS [So_Luong_Nguoi],
    AVG(ap_hi)                      AS [HuyetAp_TamThu_TrungBinh],
    MIN(ap_hi)                      AS [HuyetAp_TamThu_NhoNhat],
    MAX(ap_hi)                      AS [HuyetAp_TamThu_LonNhat],
    SUM(cardio)                     AS [Tong_So_Nguoi_Co_Benh_Tim]
FROM dbo.cleaned_cardio
GROUP BY cholesterol
ORDER BY cholesterol;
GO

-- 7c. Thống kê theo giới tính (gender): 1 = Nữ, 2 = Nam
SELECT
    gender                          AS [Gioi_Tinh],
    COUNT(*)                        AS [So_Luong_Nguoi],
    AVG(age)                        AS [Tuoi_Trung_Binh],
    AVG(ap_hi)                      AS [HuyetAp_TamThu_TrungBinh],
    SUM(cardio)                     AS [Tong_So_Nguoi_Co_Benh_Tim]
FROM dbo.cleaned_cardio
GROUP BY gender;
GO


-- ============================================================
-- PHẦN 8. HAVING — LỌC NHÓM SAU KHI GROUP BY
-- ============================================================

-- 8a. Tìm các mức tuổi có huyết áp tâm thu TRUNG BÌNH >= 130 mmHg
--     (Chỉ giữ lại những nhóm tuổi đáng lo ngại)
SELECT
    age                             AS [Tuoi],
    COUNT(*)                        AS [So_Luong_Nguoi],
    AVG(ap_hi)                      AS [HuyetAp_TamThu_TrungBinh],
    AVG(ap_lo)                      AS [HuyetAp_TamTruong_TrungBinh]
FROM dbo.cleaned_cardio
GROUP BY age
HAVING AVG(ap_hi) >= 130
ORDER BY AVG(ap_hi) DESC;
GO

-- 8b. Tìm các nhóm Cholesterol có tổng số người bị bệnh tim > 5000 người
SELECT
    cholesterol                     AS [Muc_Cholesterol],
    COUNT(*)                        AS [So_Luong_Nguoi],
    SUM(cardio)                     AS [So_Nguoi_Co_Benh_Tim]
FROM dbo.cleaned_cardio
GROUP BY cholesterol
HAVING SUM(cardio) > 5000
ORDER BY SUM(cardio) DESC;
GO

-- 8c. Nhóm tuổi từ 40 tuổi trở lên, tìm các mức tuổi
--     có huyết áp tâm thu trung bình TRÊN 135 mmHg
SELECT
    age                             AS [Tuoi],
    COUNT(*)                        AS [So_Luong_Nguoi],
    AVG(ap_hi)                      AS [HuyetAp_TamThu_TrungBinh]
FROM dbo.cleaned_cardio
WHERE age >= 40
GROUP BY age
HAVING AVG(ap_hi) > 135
ORDER BY age;
GO

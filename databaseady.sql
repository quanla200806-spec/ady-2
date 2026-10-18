USE [master];
GO

-- 1. TẠO CƠ SỞ DỮ LIỆU MỚI (NẾU CHƯA CÓ)
IF DB_ID(N'ady') IS NULL
BEGIN
    CREATE DATABASE [ady];
END
GO

USE [ady];
GO

-- 2. XÓA BẢNG CŨ (NẾU ĐÃ CÓ) ĐỂ TẠO MỚI TINH
DROP TABLE IF EXISTS dbo.heart_data;
GO

-- 3. TẠO BẢNG MỚI HOÀN TOÀN KHỚP 100% VỚI clean_data.py
CREATE TABLE dbo.heart_data (
    -- Cột ID tự động tăng (1, 2, 3,...) làm khóa chính để tìm kiếm
    id INT IDENTITY(1,1) NOT NULL,
    
    -- Các cột khớp chính xác với file heart_cleaned.csv
    age INT NOT NULL,                  -- Tuổi theo ngày (dữ liệu gốc)
    gender INT NOT NULL,               -- 1: Nữ, 2: Nam
    height INT NOT NULL,               -- Chiều cao (cm)
    weight FLOAT NOT NULL,             -- Cân nặng (kg)
    ap_hi INT NOT NULL,                -- Huyết áp tâm thu
    ap_lo INT NOT NULL,                -- Huyết áp tâm trương
    cholesterol INT NOT NULL,          -- 1: Bình thường, 2: Cao, 3: Rất cao
    gluc INT NOT NULL,                 -- 1: Bình thường, 2: Cao, 3: Rất cao
    smoke INT NOT NULL,                -- 0: Không, 1: Có
    alco INT NOT NULL,                 -- 0: Không, 1: Có
    active INT NOT NULL,               -- 0: Không, 1: Có
    cardio INT NOT NULL,               -- 0: Khỏe mạnh, 1: Bệnh tim
    age_year INT NOT NULL,              -- Tuổi theo NĂM (dùng để tìm kiếm và hiển thị)
    BMI FLOAT NOT NULL,                -- Chỉ số BMI đã làm tròn 2 chữ số
    
    CONSTRAINT PK_heart_data_id PRIMARY KEY (id)
);
GO

-- 4. TẠO CHỈ MỤC (INDEX) TỐI ƯU TỐC ĐỘ TÌM KIẾM
CREATE NONCLUSTERED INDEX IX_heart_search_age_cardio
ON dbo.heart_data (age_year, cardio)
INCLUDE (gender, ap_hi, ap_lo, BMI, cholesterol);
GO

-- 5. TẠO THỦ TỤC TÌM KIẾM BỆNH NHÂN ĐA NĂNG (STORED PROCEDURE)
CREATE OR ALTER PROCEDURE dbo.sp_SearchPatient
    @id INT = NULL,                     -- Tìm chính xác theo ID (VD: 10, 100)
    @gender INT = NULL,                 -- 1: Nữ, 2: Nam (NULL: Tất cả)
    @min_age INT = NULL,                -- Độ tuổi từ (VD: 45)
    @max_age INT = NULL,                -- Độ tuổi đến (VD: 60)
    @cardio INT = NULL,                 -- 1: Nguy cơ bệnh tim, 0: Bình thường
    @is_high_bp BIT = NULL,             -- 1: Huyết áp cao (ap_hi >= 140 hoặc ap_lo >= 90)
    @min_bmi FLOAT = NULL,              -- BMI từ (VD: 25 là thừa cân)
    @top_records INT = 100              -- Giới hạn số dòng hiển thị
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@top_records)
        id AS [Mã BN],
        age_year AS [Tuổi],
        CASE gender WHEN 1 THEN N'Nữ' WHEN 2 THEN N'Nam' ELSE N'Khác' END AS [Giới tính],
        height AS [Chiều cao (cm)],
        weight AS [Cân nặng (kg)],
        ROUND(BMI, 2) AS [Chỉ số BMI],
        CASE 
            WHEN BMI < 18.5 THEN N'Gầy'
            WHEN BMI < 25 THEN N'Bình thường'
            WHEN BMI < 30 THEN N'Thừa cân'
            ELSE N'Béo phì'
        END AS [Thể trạng],
        CONCAT(ap_hi, '/', ap_lo) AS [Huyết áp],
        CASE 
            WHEN ap_hi >= 140 OR ap_lo >= 90 THEN N'Cao'
            WHEN ap_hi < 90 OR ap_lo < 60 THEN N'Thấp'
            ELSE N'Bình thường'
        END AS [Tình trạng huyết áp],
        CASE cholesterol WHEN 1 THEN N'Bình thường' WHEN 2 THEN N'Cao' WHEN 3 THEN N'Rất cao' END AS [Cholesterol],
        CASE smoke WHEN 1 THEN N'Có' ELSE N'Không' END AS [Hút thuốc],
        CASE alco WHEN 1 THEN N'Có' ELSE N'Không' END AS [Uống rượu],
        CASE active WHEN 1 THEN N'Có' ELSE N'Không' END AS [Vận động],
        CASE cardio WHEN 1 THEN N'⚠️ Nguy cơ tim mạch' ELSE N'✅ Khỏe mạnh' END AS [Kết luận]
    FROM dbo.heart_data
    WHERE 
        (@id IS NULL OR id = @id)
        AND (@gender IS NULL OR gender = @gender)
        AND (@min_age IS NULL OR age_year >= @min_age)
        AND (@max_age IS NULL OR age_year <= @max_age)
        AND (@cardio IS NULL OR cardio = @cardio)
        AND (@min_bmi IS NULL OR BMI >= @min_bmi)
        AND (
            @is_high_bp IS NULL 
            OR (@is_high_bp = 1 AND (ap_hi >= 140 OR ap_lo >= 90))
            OR (@is_high_bp = 0 AND (ap_hi < 140 AND ap_lo < 90))
        )
    ORDER BY id ASC;
END;
GO
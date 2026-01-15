-- SQL Queries for Waste Data Analysis

-- 1. Qual é a categoria alimentar que gera o maior desperdício total em toneladas e o maior prejuízo econômico?
-- Total de Desperdício por Categoria
SELECT
    "Food Category",
    SUM("Total Waste (Tons)") AS TotalWaste
FROM
    Waste
GROUP BY
    "Food Category"
ORDER BY
    TotalWaste DESC;

-- Prejuízo Econômico por Categoria
SELECT
    "Food Category",
    SUM("Economic Loss (Million $)") AS TotalLoss
FROM
    Waste
GROUP BY
    "Food Category"
ORDER BY
    TotalLoss DESC;

-- 2. Quais países apresentam os maiores índices de desperdício per capita em relação à população total?
SELECT
    "Country Name",
    "Avg Waste per Capita (Kg)",
    "Population (Million)"
FROM
    Waste
ORDER BY
    "Avg Waste per Capita (Kg)" DESC;

-- 3. Qual a relação entre o percentual de resíduos domésticos e o desperdício total por categoria alimentar?
SELECT
    "Food Category",
    "Household Waste (%)",
    "Total Waste (Tons)"
FROM
    Waste;

-- 4. Países com maior população apresentam maior desperdício absoluto ou proporcional?
-- Desperdício Absoluto
SELECT
    "Country Name",
    "Population (Million)",
    SUM("Total Waste (Tons)") AS TotalWaste
FROM
    Waste
GROUP BY
    "Country Name", "Population (Million)"
ORDER BY
    "Population (Million)" DESC;

-- Desperdício Proporcional (per capita)
SELECT
    "Country Name",
    "Population (Million)",
    "Avg Waste per Capita (Kg)"
FROM
    Waste
ORDER BY
    "Population (Million)" DESC;

-- 5. Qual seria o impacto na perda econômica se o desperdício doméstico fosse reduzido em 10% em cada país?
SELECT
    "Country Name",
    SUM("Economic Loss (Million $)") AS OriginalLoss,
    SUM("Economic Loss (Million $)") * 0.9 AS ReducedLoss
FROM
    Waste
GROUP BY
    "Country Name";

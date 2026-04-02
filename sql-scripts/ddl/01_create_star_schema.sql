-- Star Schema DDL
-- Initial version created 2024-01-10

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'reporting')
BEGIN
    EXEC('CREATE SCHEMA reporting')
END
GO

-- DEPRECATED: Old customer table from previous migration
CREATE TABLE [dbo].[dim_customer_old] (
    [customer_id] NVARCHAR(50),
    [email] NVARCHAR(255),
    [signup_date] DATE
) WITH (DISTRIBUTION = REPLICATE);

CREATE TABLE [reporting].[dim_product] (
    [product_key] INT IDENTITY(1,1),
    [product_id] NVARCHAR(50) NOT NULL,
    [name] NVARCHAR(255),
    [category] NVARCHAR(100),
    [price] DECIMAL(18,2)
) WITH (DISTRIBUTION = REPLICATE, CLUSTERED COLUMNSTORE INDEX);

CREATE TABLE [reporting].[fact_orders] (
    [order_id] NVARCHAR(50) NOT NULL,
    [customer_id] NVARCHAR(50),
    [order_time] DATETIME2,
    [total_amount] DECIMAL(18,2), -- Standardized from 'amount'
    [currency] NVARCHAR(10)
) WITH (
    DISTRIBUTION = HASH([order_id]),
    CLUSTERED COLUMNSTORE INDEX
);

-- FIXME: Add indexes for currency filters once volume increases

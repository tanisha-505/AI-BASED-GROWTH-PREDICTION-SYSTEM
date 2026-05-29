-- setup.sql
-- Run this in MySQL Workbench or MySQL terminal BEFORE starting the server.
-- This creates your database and both tables.

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS growth_prediction_db;
USE growth_prediction_db;

-- Step 2: Historical sales data table
CREATE TABLE IF NOT EXISTS sales_data (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    month            INT          NOT NULL,
    year             INT          NOT NULL,
    sales            FLOAT        NOT NULL,
    marketing_spend  FLOAT        NOT NULL,
    num_employees    INT          NOT NULL,
    region           VARCHAR(50)  NOT NULL,
    product_category VARCHAR(100) NOT NULL,
    created_at       DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Predictions log table
CREATE TABLE IF NOT EXISTS predictions (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    predicted_sales  FLOAT,
    model_used       VARCHAR(100),
    month            INT,
    year             INT,
    marketing_spend  FLOAT,
    num_employees    INT,
    region           VARCHAR(50),
    product_category VARCHAR(100),
    timestamp        VARCHAR(50),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Verify tables were created
SHOW TABLES;
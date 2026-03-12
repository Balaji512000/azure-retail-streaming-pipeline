# Databricks notebook source
# 03_kpi_aggregations

import pyspark.sql.functions as F

# Watermark logic to handle late events before aggregation
df_silver = (spark.readStream
    .table("silver_orders")
    .withWatermark("event_time", "2 hours")
)

# Aggregate hourly revenue using total_amount
df_gold = (df_silver
    .groupBy(F.window("event_time", "1 hour"), "currency")
    .agg(
        F.count("order_id").alias("order_count"),
        F.sum("total_amount").alias("revenue")
    )
    .select(
        F.col("window.start").alias("hour"),
        "currency",
        "order_count",
        "revenue"
    )
)

(df_gold.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/mnt/datalake/checkpoints/gold_hourly_sales/")
    .table("gold_hourly_sales")
)

# TODO: Add Z-ORDER by hour once this table grows past 1GB

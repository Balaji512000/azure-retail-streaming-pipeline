# Databricks notebook source
# 01_raw_to_bronze

# %run ../streaming-utils/config_loader
# conf = load_config()

import pyspark.sql.functions as F

RAW_PATH = "/mnt/datalake/raw/ecommerce_events/" # Fallback
CHECKPOINT = "/mnt/datalake/checkpoints/bronze_ingestion/"

# AutoLoader with directory listing to save cost
df_raw = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"{CHECKPOINT}/schema")
    .load(RAW_PATH)
)

df_bronze = df_raw.select(
    "*",
    F.current_timestamp().alias("_ingestion_time"),
    F.input_file_name().alias("_source_file")
)

# FIXME: Small files problem in Bronze. Auto-optimize helps but doesn't fix everything.
(df_bronze.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT)
    .option("delta.autoOptimize.optimizeWrite", "true")
    .trigger(processingTime='30 seconds') 
    .table("bronze_ecommerce_events")
)

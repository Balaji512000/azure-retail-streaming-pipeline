# Databricks notebook source
# 02_cleansing_orders

import pyspark.sql.functions as F
from pyspark.sql.window import Window

# Settings
BRONZE_TABLE = "bronze_ecommerce_events"
SILVER_TABLE = "silver_orders"
CHECKPOINT = "/mnt/datalake/checkpoints/silver_orders/"

# Explicit schema to ensure total_amount is captured correctly
order_schema = "order_id STRING, customer_id STRING, total_amount DOUBLE, currency STRING, items ARRAY<STRUCT<product_id: STRING, quantity: INT, price: DOUBLE>>"

df = (spark.readStream
    .table(BRONZE_TABLE)
    .filter("event_type = 'ORDER_PLACED'")
    .withColumn("event_time", F.to_timestamp("event_timestamp"))
    .withWatermark("event_time", "24 hours")
)

df_parsed = df.withColumn("p", F.from_json("payload", order_schema)).select("event_id", "event_time", "p.*")

def upsert(batch_df, batch_id):
    # Deterministic dedup: keeping latest event in case payment updates arrive out of order
    window_spec = Window.partitionBy("order_id").orderBy(F.col("event_time").desc())
    deduped = (batch_df
        .withColumn("rn", F.row_number().over(window_spec))
        .filter("rn = 1")
        .drop("rn")
    )
    
    deduped.createOrReplaceTempView("updates")
    spark.sql(f"""
        MERGE INTO {SILVER_TABLE} t
        USING updates s
        ON t.order_id = s.order_id
        WHEN MATCHED AND s.event_time > t.event_time THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)

(df_parsed.writeStream
    .foreachBatch(upsert)
    .option("checkpointLocation", CHECKPOINT)
    .trigger(availableNow=True)
    .start()
)

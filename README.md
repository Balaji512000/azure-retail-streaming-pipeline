# ecommerce-streaming-platform

Streaming data pipeline for e-commerce events (orders, payments, inventory) on Databricks and Delta Lake.

## Architecture
- **Ingestion**: Event Hubs -> Bronze (AutoLoader)
- **Processing**: Bronze -> Silver (Dedup/Watermark) -> Gold (Hourly Aggs)
- **Serving**: Delta tables exposed to Synapse via SQL Analytics

## Setup
1.  **Configs**: Environment settings are in `configs/`. `streaming-utils/config_loader` handles the path injection.
2.  **Schema**: Execute `sql-scripts/ddl/01_create_star_schema.sql` in Synapse to initialize the `reporting` schema.
3.  **Simulator**: Use `streaming-simulator/event-generators/main_generator.py` to push sample JSON to your raw landing zone.

## Operational Status
- **Dedup**: We use a 24h watermark on order IDs. Late payment events landing outside this window go to an orphan table for manual review.
- **Deduplication**: Logic is deterministic using `row_number()` over the event timestamp.
- **Replays**: Manual replay script is in `utilities/manual_replay.py`. Not yet automated in ADF.
- **Holiday Traffic**: During peak windows (BFCM), we disable Auto-Optimize in Bronze to reduce write latency and handle it via a separate maintenance job.

## TODOs
- [ ] Implement automated checkpoint cleanup.
- [ ] Migrate `dim_customer` to a full SCD Type 2 model.
- [ ] Centralize schema registry for JSON parsing.

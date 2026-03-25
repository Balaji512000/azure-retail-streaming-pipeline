# Troubleshooting

## Stream is stuck (No new records)
- **Check Event Hubs**: Is there actually data coming in? Use 'Process Data' in Azure Portal to check.
- **Check Watermark**: If the watermark is too aggressive, late data might be silently dropped.
- **Checkpoint Issues**: Sometimes the checkpoint gets into a weird state. Try restarting the cluster. If that fails, see the Runbook for how to clear the last offset (careful!).

## Duplicate Orders in Synapse
- This happens if the Silver dedup job fails and the batch is re-run without the `MERGE` logic working correctly. 
- Run the reconciliation script to identify the duplicates and use the manual cleanup script in `sql-scripts/reporting/cleanup_dupes.sql`.

## Schema Mismatch in Bronze
- Usually means the Checkout team changed the JSON structure without telling us.
- Check the `_corrupt_record` column in the temporary debug table (if enabled).
- Land the offending files in quarantine and notify the @Checkout-Team.

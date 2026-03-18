# Operational Notes

## Monitoring
- ADF: Check `PL_Main_Streaming_Orchestration`. If it fails, usually it's a transient Databricks cluster startup issue.
- Databricks: Check 'Streaming' tab. Keep an eye on input rate vs. processing rate.

## Recovery
- **Checkpoint Corruption**: If a stream fails with a checkpoint error, do NOT delete the whole folder. Try deleting just the `offsets` and `commits` for the last batch first.
- **Malformed Events**: Land in `/mnt/datalake/quarantine`. Inspect the JSON and check for schema changes from the upstream Checkout service.

## Late Event Handling
- Payments often lag orders by several minutes. Our 24h watermark handles most cases.
- If we get a massive batch of late events (e.g., after an upstream outage), we might need to manually bump the watermark in the Silver notebook temporarily to force a re-scan.

## Peak Load Strategy
- During sales (Black Friday/Cyber Monday), we disable Auto-Optimize in Bronze to reduce write latency. Remember to re-enable after the peak.
- TODO: Automate the scale-out of the job cluster based on Event Hub backlog metrics.

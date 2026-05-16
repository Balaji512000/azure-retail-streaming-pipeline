# How to Run the OpsCenter Dashboard

1.  Navigate to the `showcase-dashboard` directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

The dashboard will open in your default browser at `http://localhost:8501`.

### Key Showcase Points:
- **Overview**: Shows real-time ingestion throughput and system health.
- **Pipeline Monitoring**: Simulates micro-batch execution logs and watermark delays.
- **Medallion Explorer**: Allows reviewers to see the transformation of data from Bronze to Gold.
- **Replay Simulation**: Demonstrates operational awareness of data recovery (Quarantine -> Replay).

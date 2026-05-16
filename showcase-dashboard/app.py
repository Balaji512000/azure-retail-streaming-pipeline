import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="OpsCenter | E-Commerce Streaming Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Engineering Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #31333f;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] {
        color: #a3a8b4 !important;
    }
    .status-up { color: #28a745; font-weight: bold; }
    .status-down { color: #dc3545; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA GENERATORS ---

@st.cache_data
def get_kpi_data():
    return {
        "orders_today": 14250,
        "orders_per_min": 124,
        "failed_payments": 42,
        "late_events": 128,
        "replay_queue": 12,
        "stream_lag_ms": 450,
        "pipeline_health": "99.8%",
        "inventory_alerts": 5
    }

@st.cache_data
def get_stream_metrics():
    times = [datetime.now() - timedelta(minutes=i) for i in range(60, 0, -1)]
    throughput = [random.randint(1000, 1500) for _ in range(60)]
    latency = [random.randint(200, 800) for _ in range(60)]
    return pd.DataFrame({"Time": times, "Throughput (ev/s)": throughput, "Latency (ms)": latency})

@st.cache_data
def get_layer_sample(layer="bronze"):
    if layer == "bronze":
        return pd.DataFrame([
            {"event_id": f"evt-{i}", "event_type": "ORDER_PLACED", "ingestion_ts": datetime.now() - timedelta(seconds=i*10), "status": "RAW"}
            for i in range(10)
        ])
    elif layer == "silver":
        return pd.DataFrame([
            {"order_id": f"ord-{i}", "customer_id": f"cust-{random.randint(100,999)}", "total_amount": round(random.uniform(10,500),2), "event_time": datetime.now() - timedelta(minutes=i), "dedup_status": "CLEAN"}
            for i in range(10)
        ])
    else:
        return pd.DataFrame([
            {"hour": (datetime.now() - timedelta(hours=i)).strftime("%H:00"), "revenue": round(random.uniform(5000,15000),2), "order_count": random.randint(100,300)}
            for i in range(10)
        ])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚡ OpsCenter v2.4")
st.sidebar.markdown("Internal Monitoring Portal")
page = st.sidebar.selectbox("Navigate", [
    "Overview Dashboard", 
    "Pipeline Monitoring", 
    "Medallion Explorer", 
    "Data Quality & Replay", 
    "Architecture & Docs"
])

st.sidebar.divider()
st.sidebar.subheader("System Health")
st.sidebar.write("🟢 Event Hubs: Healthy")
st.sidebar.write("🟢 Databricks: Active")
st.sidebar.write("🟡 Synapse: Sync Delayed (2m)")

# --- PAGE: OVERVIEW DASHBOARD ---
if page == "Overview Dashboard":
    st.title("Platform Overview")
    st.markdown("Real-time operational KPIs and system throughput.")
    
    kpis = get_kpi_data()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Orders Today", f"{kpis['orders_today']:,}", "+12%")
    with col2:
        st.metric("Stream Lag", f"{kpis['stream_lag_ms']}ms", "-50ms", delta_color="normal")
    with col3:
        st.metric("Failed Payments", kpis['failed_payments'], "4.2%", delta_color="inverse")
    with col4:
        st.metric("Replay Queue", kpis['replay_queue'], "Stale")

    st.divider()
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Ingestion Throughput (Last 60 mins)")
        metrics = get_stream_metrics()
        fig = px.line(metrics, x="Time", y="Throughput (ev/s)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("Critical Alerts")
        st.warning("⚠️ High Volume: Black Friday simulation active (Load: 1.5x)")
        st.error("🚨 12 Payment events dropped (Watermark mismatch > 24h)")
        st.info("ℹ️ Scheduled OPTIMIZE running on Gold tables")

# --- PAGE: PIPELINE MONITORING ---
elif page == "Pipeline Monitoring":
    st.title("Streaming Pipeline Health")
    
    st.subheader("Micro-batch Execution Timeline")
    batches = pd.DataFrame([
        {"Batch ID": i, "Status": "SUCCESS" if i != 42 else "FAILED", "Duration (s)": random.uniform(2, 8), "Processed Rows": random.randint(500, 2000)}
        for i in range(35, 45)
    ])
    
    def color_status(val):
        color = 'green' if val == 'SUCCESS' else 'red'
        return f'color: {color}'

    st.table(batches.style.applymap(color_status, subset=['Status']))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Watermark Delay (Silver)")
        st.write("Current Delay: **1h 14m**")
        st.progress(0.85)
        st.caption("Threshold: 24h before eviction")
        
    with col2:
        st.subheader("Checkpoint Health")
        st.write("Last Commit: 14s ago")
        st.write("Storage Account: `stdedatalakecheckpoints`")
        st.write("Size: 142.4 MB")

# --- PAGE: MEDALLION EXPLORER ---
elif page == "Medallion Explorer":
    st.title("Medallion Layer Explorer")
    
    tab1, tab2, tab3 = st.tabs(["Bronze (Raw)", "Silver (Cleansed)", "Gold (Curated)"])
    
    with tab1:
        st.write("Ingesting raw JSON payloads from Checkout Microservice")
        st.dataframe(get_layer_sample("bronze"), use_container_width=True)
        st.caption("Note: `payload` field omitted for visibility. Use Databricks for full JSON inspection.")
        
    with tab2:
        st.write("Deduplicated and Normalized Order records")
        st.dataframe(get_layer_sample("silver"), use_container_width=True)
        
    with tab3:
        st.write("Hourly Sales Aggregates for Finance Dashboards")
        st.dataframe(get_layer_sample("gold"), use_container_width=True)

# --- PAGE: DATA QUALITY & REPLAY ---
elif page == "Data Quality & Replay":
    st.title("Data Quality & Recovery")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reconciliation Summary")
        recon = pd.DataFrame({
            "Layer": ["Bronze", "Silver"],
            "Record Count": [14250, 14245],
            "Variance": [0, -5]
        })
        st.table(recon)
        st.caption("Mismatch (-5) attributed to late events outside 24h watermark.")
        
    with col2:
        st.subheader("Quarantine Registry")
        st.error("12 Malformed Records detected in `mnt/datalake/quarantine/`")
        st.write("Reason: `PAYMENT_ID` field expected String, received Null")
        
    st.divider()
    
    st.subheader("Manual Replay Simulation")
    replay_id = st.text_input("Enter Batch ID or Order ID to Replay", "")
    if st.button("Trigger Replay"):
        if replay_id:
            with st.spinner(f"Moving {replay_id} from Quarantine to Landing Zone..."):
                time.sleep(2)
                st.success(f"Replay initiated for {replay_id}. Check Bronze ingestion in 30s.")
        else:
            st.warning("Please enter a valid ID.")

# --- PAGE: ARCHITECTURE & DOCS ---
elif page == "Architecture & Docs":
    st.title("Architecture & Documentation")
    
    st.image("https://raw.githubusercontent.com/Balaji512000/azure-retail-streaming-pipeline/main/documentation/architecture_diagram.png", caption="System Architecture (Internal Concept)", use_column_width=True)
    
    st.markdown("""
    ### Technical Stack
    - **Ingestion**: Azure Event Hubs (Kafka compatible)
    - **Processing**: Azure Databricks (PySpark Structured Streaming)
    - **Storage**: Delta Lake (Medallion Architecture)
    - **Orchestration**: Azure Data Factory (ADF)
    - **Warehouse**: Azure Synapse Analytics
    - **Observability**: This OpsCenter (Streamlit)
    
    ### Documentation Quick Links
    - [GitHub Repository](https://github.com/Balaji512000/azure-retail-streaming-pipeline)
    - [Operational Runbook](https://github.com/Balaji512000/azure-retail-streaming-pipeline/blob/main/documentation/runbook/operational_runbook.md)
    - [Troubleshooting Guide](https://github.com/Balaji512000/azure-retail-streaming-pipeline/blob/main/documentation/troubleshooting/common_issues.md)
    - [Development History](https://github.com/Balaji512000/azure-retail-streaming-pipeline/blob/main/documentation/dev_history.md)
    """)

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("© 2024 E-Commerce Data Engineering Team")
st.sidebar.caption("Confidential - Internal Use Only")

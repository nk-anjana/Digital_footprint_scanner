import streamlit as st
import pandas as pd
from api import get_scans, get_scan_result

st.set_page_config(page_title="Operations Dashboard - Nexus", page_icon="📊", layout="wide")

if not st.session_state.get("access_token"):
    st.warning("UNAUTHORIZED. Please login via the main platform.")
    st.stop()

st.title("📊 Operations Dashboard")
st.markdown("Monitor and decrypt intelligence payloads from past operations.")

scans = get_scans()

if not scans:
    st.info("No active operations found in the database. Head to 'New Scan' to initiate one.")
else:
    # High-level Metrics
    total_scans = len(scans)
    completed_scans = sum(1 for s in scans if s.get('status') == 'Completed')
    avg_risk = sum(s.get('risk_score', 0) for s in scans) / total_scans if total_scans > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Operations", total_scans)
    col2.metric("Successful Traces", completed_scans)
    col3.metric("Average Threat Risk", f"{int(avg_risk)} / 100")
    
    st.markdown("---")
    
    # Organize data for the interactive table
    df = pd.DataFrame(scans)
    # Reorder and format columns
    df = df[['scan_id', 'status', 'risk_score', 'email', 'username', 'domain', 'created_at']]
    
    st.subheader("Trace History")
    
    # Display the dataframe with Streamlit's new column config for interactivity
    st.dataframe(
        df,
        column_config={
            "scan_id": "Operation ID",
            "status": st.column_config.TextColumn("Status", help="Current state of the trace"),
            "risk_score": st.column_config.NumberColumn("Risk", format="%d - /100"),
            "email": "Target Email",
            "username": "Target User",
            "domain": "Target Domain",
            "created_at": st.column_config.DatetimeColumn("Timestamp", format="D MMM YY, h:mm a"),
        },
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.subheader("Decrypt Specific Payload")
    
    selected_scan = st.selectbox("Select Operation ID to analyze findings:", df['scan_id'])
    
    if st.button("Decrypt Payload Data", type="primary"):
        with st.spinner("Extracting secured data payload..."):
            result = get_scan_result(selected_scan)
            if result:
                findings = result.get("findings", [])
                
                # Display findings clearly
                if findings:
                    st.success("Payload successfully decrypted.")
                    f_df = pd.DataFrame(findings)
                    st.dataframe(f_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Scan completed but yielded no critical footprint data.")
            else:
                st.error("Failed to retrieve payload from the database.")
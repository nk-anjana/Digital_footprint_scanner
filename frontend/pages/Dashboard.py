import streamlit as st
import pandas as pd
from api import get_scans, get_scan_result
from style_manager import apply_custom_page_style, render_theme_toggle, apply_theme_attribute

st.set_page_config(page_title="Operations Dashboard - Nexus", page_icon="📊", layout="wide")

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Check authentication
if not st.session_state.get("access_token"):
    st.warning("🔒 UNAUTHORIZED - Please login first")
    if st.button("Go to Login"):
        st.switch_page("Login.py")
    st.stop()

# Render theme toggle and apply styling
try:
    render_theme_toggle()
    apply_theme_attribute()
except ImportError:
    pass

apply_custom_page_style("Dashboard")

# Sidebar logout button
with st.sidebar:
    st.markdown("---")
    username = st.session_state.get("username", "User")
    st.caption(f"👤 Logged in as: **{username}**")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.access_token = None
        st.session_state.username = None
        st.session_state.clear()
        st.switch_page("Login.py")

st.title("📊 Operations Dashboard")
st.markdown("Monitor and decrypt intelligence payloads from past operations.")

try:
    scans = get_scans()
except Exception as e:
    st.error(f"❌ Backend Authentication Failed: {str(e)}")
    st.info("Make sure you have a valid access token and the API is running.")
    st.stop()

if not scans:
    st.info("ℹ️ No active operations found. Navigate to **New Scan** to initiate one.")
else:
    # High-level Metrics
    total_scans = len(scans)
    completed_scans = sum(1 for s in scans if s.get('status') == 'Completed')
    avg_risk = sum(s.get('risk_score', 0) for s in scans) / total_scans if total_scans > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Operations", total_scans)
    col2.metric("✅ Successful Traces", completed_scans)
    col3.metric("⚠️ Average Threat Risk", f"{int(avg_risk)} / 100")
    
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
                status = result.get("status")
                findings = result.get("findings", [])
                
                if status == "Running":
                    st.info("This scan is still running. Please check back later.")
                elif status == "Failed":
                    st.error("This scan failed. Check the error details below.")
                    f_df = pd.DataFrame(findings)
                    st.dataframe(f_df, use_container_width=True, hide_index=True)
                else:
                    # Display findings clearly for Completed scans
                    if findings:
                        st.success("Payload successfully decrypted.")
                        f_df = pd.DataFrame(findings)
                        st.dataframe(f_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("Scan completed but yielded no critical footprint data.")
            else:
                st.error("Failed to retrieve payload from the database.")
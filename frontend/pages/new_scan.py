import streamlit as st
import time
import pandas as pd
from api import start_scan, get_scan_result

st.set_page_config(page_title="New Scan - Nexus", page_icon="🎯", layout="wide")

if not st.session_state.get("access_token"):
    st.warning("UNAUTHORIZED. Please login via the main platform.")
    st.stop()

st.title("🎯 Intelligence Target Scan")
st.markdown("Initiate a comprehensive digital footprint trace across global databases.")

# Clean form container
with st.container(border=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        target_type = st.radio(
            "Target Classification", 
            ["Email", "Username", "Domain"], 
            help="Select the type of information you want to trace."
        )
    with col2:
        st.write("")
        st.write("")
        target_value = st.text_input(f"Enter target {target_type.lower()}...", placeholder=f"e.g., target.{target_type.lower()}@example.com")

if st.button("Execute Trace Initiative", type="primary", use_container_width=True):
    if not target_value:
        st.error("Target identification parameter is required.")
    else:
        payload = {"email": "", "username": "", "domain": ""}
        payload[target_type.lower()] = target_value
        
        # UI State reset before scan
        res_container = st.empty()
        
        with res_container.container():
            st.info("Initializing communication with scan engines...")
            res = start_scan(payload)
            
            if res.status_code == 202:
                scan_id = res.json().get("scan_id")
                st.success(f"Trace assigned ID: {scan_id}")
                
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Increased polling to 30 iterations (60 seconds)
                    completed = False
                    final_data = None
                    for i in range(30):
                        time.sleep(2)
                        
                        # Update progress based on polling loop (visual only)
                        visual_progress = min(95, (i + 1) * 3)
                        progress_bar.progress(visual_progress)
                        status_text.caption(f"Querying distributed networks... ({visual_progress}%)")
                        
                        check = get_scan_result(scan_id)
                        if check and check.get("status") == "Completed":
                            progress_bar.progress(100)
                            status_text.success("DATA SECURED & ANALYZED.")
                            completed = True
                            final_data = check
                            break
                    else:
                        st.warning("Trace taking longer than expected. It is still running in the background. Check Dashboard later.")
                
                # Show results dynamically
                if completed and final_data:
                    findings = final_data.get("findings", [])
                    st.markdown("---")
                    st.subheader("Intelligence Report")
                    
                    # Risk Metrics
                    risk = final_data.get("risk_score", 0)
                    r_col1, r_col2, r_col3 = st.columns(3)
                    r_col1.metric("Risk Score", f"{risk}/100", delta_color="inverse")
                    r_col2.metric("Total Findings", len(findings))
                    r_col3.metric("Status", final_data.get("status"))
                    
                    if findings:
                        df = pd.DataFrame(findings)
                        st.dataframe(
                            df,
                            column_config={
                                "source": st.column_config.TextColumn("Source Database"),
                                "severity": st.column_config.TextColumn("Severity Level"),
                                "type": st.column_config.TextColumn("Data Type"),
                                "value": st.column_config.TextColumn("Value/Evidence"),
                                "url": st.column_config.LinkColumn("Source URL")
                            },
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("No critical footprint data discovered for this target.")
                        
            else:
                st.error(f"System Error: {res.text}")
import streamlit as st
from api import analyze_image

st.set_page_config(page_title="Forensics - Nexus", page_icon="📷", layout="wide")

if not st.session_state.get("access_token"):
    st.warning("UNAUTHORIZED. Please login via the main platform.")
    st.stop()

st.title("📷 Digital Forensics: EXIF Extractor")
st.markdown("Upload image payloads to strip hidden metadata, device information, and embedded geospatial coordinates.")

with st.container(border=True):
    uploaded_file = st.file_uploader("Drop target image here...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Target Visual")
        st.image(uploaded_file, use_container_width=True, caption=f"File: {uploaded_file.name}")
        
        if st.button("Run Forensic Analysis", type="primary", use_container_width=True):
            st.session_state.analyze_clicked = True
            
    with col2:
        if st.session_state.get("analyze_clicked", False):
            with st.spinner("Executing forensic subroutines..."):
                res = analyze_image(
                    uploaded_file.getvalue(), 
                    uploaded_file.name, 
                    uploaded_file.type
                )
                
            if res.status_code == 200:
                data = res.json()
                st.success("Forensic Analysis Complete. Metadata extracted.")
                
                # Geospatial Data section
                if data.get("location"):
                    st.subheader("📍 Geospatial Evidence Discovered")
                    lat = data["location"]["latitude"]
                    lon = data["location"]["longitude"]
                    
                    st.map(latitude=[lat], longitude=[lon], zoom=12)
                    st.markdown(f"**Maps Link**: [View on Google Maps]({data['location']['google_maps']})")
                else:
                    st.info("No geospatial (GPS) coordinates found in the image.")
                
                # Raw Metadata expander
                with st.expander("View Raw Discovered Metadata", expanded=True):
                    st.json(data.get("metadata", {}))
            else:
                st.error(f"Extraction sequence failed: {res.text}")
import streamlit as st
from api import login, register

st.set_page_config(
    page_title="Nexus OSINT", 
    page_icon="🌍", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Premium Modern CSS
st.markdown("""
<style>
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.5px;
        color: #f0f2f6;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 10px 15px;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 2px rgba(79, 172, 254, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(118, 75, 162, 0.4);
        color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Nexus Intelligence")

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if st.session_state.access_token:
    st.success("Authentication successful. Welcome to the Nexus.")
    st.info("👈 Use the sidebar to navigate the intelligence modules.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="System Status", value="Online", delta="Stable")
    with col2:
        st.metric(label="Secure Modules", value="3 Active", delta="Updated")
else:
    st.markdown("Enter your credentials to access the secure intelligence platform.")
    st.write("")
    
    tab1, tab2 = st.tabs(["Authentication", "New Operative Registration"])
    
    with tab1:
        with st.container(border=True):
            st.subheader("Secure Login")
            l_user = st.text_input("Username", key="l_user")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            st.write("")
            if st.button("Authenticate"):
                with st.spinner("Verifying credentials..."):
                    res = login(l_user, l_pass)
                if res.status_code == 200:
                    st.session_state.access_token = res.json().get("access_token")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid credentials.")
                
    with tab2:
        with st.container(border=True):
            st.subheader("Register Identity")
            r_user = st.text_input("Username", key="r_user")
            r_pass = st.text_input("Password", type="password", key="r_pass")
            st.write("")
            if st.button("Establish Identity"):
                with st.spinner("Registering in the database..."):
                    res = register(r_user, r_pass)
                if res.status_code == 200:
                    st.success("Identity established. Please return to Authentication.")
                else:
                    st.error(res.json().get("detail", "Error registering."))
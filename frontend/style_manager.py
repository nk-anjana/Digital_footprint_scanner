"""
Style Management Module for Nexus OSINT
========================================
Handles loading and applying CSS styling to Streamlit app
"""

import streamlit as st
import os


def load_css(css_file_path: str = "styles.css") -> str:
    """
    Load CSS from file or return CSS as string.
    
    Args:
        css_file_path: Path to the CSS file relative to frontend directory
        
    Returns:
        CSS content as string
    """
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, css_file_path)
        
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            st.warning(f"CSS file not found at {full_path}")
            return ""
    except Exception as e:
        st.error(f"Error loading CSS: {e}")
        return ""


def apply_styles(css_file_path: str = "styles.css") -> None:
    """
    Apply CSS styles to the Streamlit app.
    
    Args:
        css_file_path: Path to the CSS file relative to frontend directory
    """
    css_content = load_css(css_file_path)
    
    if css_content:
        st.markdown(
            f"<style>{css_content}</style>",
            unsafe_allow_html=True
        )

def apply_theme_attribute():
    theme = get_theme()
    st.markdown(
        f"""
        <script>
            document.documentElement.setAttribute("data-theme", "{theme}");
        </script>
        """,
        unsafe_allow_html=True
    )
def apply_inline_styles() -> None:
    """
    Apply inline CSS directly to the Streamlit app for immediate effect.
    This is more effective than loading from file for Streamlit components.
    """
    theme = get_theme()
    
    # Dark theme colors
    if theme == "dark":
        dark_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Root Variables */
            :root {
                --primary-blue: #4facfe;
                --primary-cyan: #00f2fe;
                --primary-purple: #667eea;
                --primary-dark-purple: #764ba2;
                --accent-green: #06d6a0;
                --accent-pink: #ff006e;
                --text-primary: #f0f2f6;
                --text-secondary: #b8bcc4;
                --bg-dark: #0f1419;
            }
            
            /* Global */
            html, body, [data-testid="stAppViewContainer"] {
                font-family: 'Inter', sans-serif;
                background-color: #0f1419 !important;
                color: #f0f2f6 !important;
            }
            
            /* Headers */
            h1, h2, h3 {
                font-weight: 600 !important;
                color: #f0f2f6 !important;
                letter-spacing: -0.5px;
            }
            
            h1 {
                background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 2rem !important;
            }
            
            /* Buttons */
            .stButton > button {
                width: 100%;
                border-radius: 8px !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                border: none !important;
                padding: 0.75rem 1.5rem !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4) !important;
            }
            
            /* Input Fields */
            .stTextInput > div > div > input,
            .stPasswordInput > div > div > input,
            .stNumberInput > div > div > input {
                border-radius: 8px !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                background-color: rgba(15, 20, 25, 0.8) !important;
                color: #f0f2f6 !important;
                padding: 0.75rem 1rem !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stPasswordInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {
                border-color: #4facfe !important;
                box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.2) !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #b8bcc4 !important;
                font-weight: 500;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: #4facfe !important;
                font-weight: 600;
            }
            
            /* Metrics */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(118, 75, 162, 0.1)) !important;
                border: 1px solid rgba(79, 172, 254, 0.2) !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
            }
            
            [data-testid="metric-container"] > div:first-child {
                color: #b8bcc4 !important;
            }
            
            [data-testid="metric-container"] > div:nth-child(2) {
                color: #4facfe !important;
                font-size: 2rem !important;
            }
            
            /* Containers */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 8px !important;
                background: linear-gradient(135deg, rgba(79, 172, 254, 0.05), rgba(118, 75, 162, 0.05)) !important;
                transition: all 0.3s ease;
            }
            
            [data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: #4facfe !important;
                box-shadow: 0 4px 12px rgba(79, 172, 254, 0.2) !important;
            }
            
            /* Dataframe */
            [data-testid="dataFrame"] {
                border-radius: 8px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Alerts */
            .stAlert {
                border-radius: 8px !important;
                border-left: 4px solid !important;
                padding: 1rem 1.5rem !important;
            }
            
            .stAlert > [data-testid="stAlertContainer"] {
                background-color: transparent !important;
            }
            
            /* Selects */
            .stSelectbox > div > div > select {
                background-color: rgba(15, 20, 25, 0.8) !important;
                color: #f0f2f6 !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 8px !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(15, 20, 25, 0.95), rgba(10, 13, 19, 0.95)) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding: 2.5rem 1.8rem !important;
            }
            
            /* Sidebar Navigation Items */
            [data-testid="stSidebar"] > div > div > div > div > button {
                width: 100% !important;
                margin: 0.5rem 0 !important;
                padding: 0.875rem 1.25rem !important;
                border-radius: 8px !important;
                justify-content: flex-start !important;
                text-align: left !important;
                transition: all 0.3s ease !important;
            }
            
            /* Sidebar Navigation Items Hover */
            [data-testid="stSidebar"] > div > div > div > div > button:hover {
                background-color: rgba(79, 172, 254, 0.15) !important;
                transform: translateX(4px) !important;
            }
            
            /* Sidebar Active Navigation Item */
            [data-testid="stSidebar"] > div > div > div > div > button[aria-pressed="true"] {
                background: linear-gradient(135deg, rgba(79, 172, 254, 0.3), rgba(79, 172, 254, 0.15)) !important;
                border-left: 3px solid #4facfe !important;
                padding-left: calc(1.25rem - 3px) !important;
                box-shadow: 0 4px 12px rgba(79, 172, 254, 0.2) !important;
            }
            
            /* Sidebar Text Elements */
            [data-testid="stSidebar"] p {
                margin: 1rem 0 !important;
                padding: 0.5rem 0 !important;
                line-height: 1.6 !important;
            }
            
            /* Sidebar Labels */
            [data-testid="stSidebar"] label {
                margin: 0.75rem 0 !important;
                padding: 0.5rem 0.75rem !important;
                font-weight: 500 !important;
            }
            
            /* Text */
            p, span, label {
                color: #f0f2f6 !important;
            }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)
    
    # Light theme colors
    else:
        light_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Root Variables for Light Theme */
            :root {
                --primary-blue: #0366d6;
                --primary-cyan: #0098d4;
                --primary-purple: #5e4fba;
                --primary-dark-purple: #6f42c1;
                --accent-green: #28a745;
                --accent-pink: #d73a49;
                --text-primary: #24292e;
                --text-secondary: #586069;
                --bg-dark: #ffffff;
            }
            
            /* Global */
            html, body, [data-testid="stAppViewContainer"] {
                font-family: 'Inter', sans-serif;
                background-color: #ffffff !important;
                color: #24292e !important;
            }
            
            /* Headers */
            h1, h2, h3 {
                font-weight: 600 !important;
                color: #24292e !important;
                letter-spacing: -0.5px;
            }
            
            h1 {
                background: linear-gradient(45deg, #0366d6 0%, #0098d4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 2rem !important;
            }
            
            /* Buttons */
            .stButton > button {
                width: 100%;
                border-radius: 8px !important;
                background: linear-gradient(135deg, #7eb3f5 0%, #5ba3ed 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                border: none !important;
                padding: 0.75rem 1.5rem !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(123, 179, 245, 0.3) !important;
            }
            
            /* Input Fields */
            .stTextInput > div > div > input,
            .stPasswordInput > div > div > input,
            .stNumberInput > div > div > input {
                border-radius: 8px !important;
                border: 1px solid rgba(0,0,0,0.15) !important;
                background-color: #fafbfc !important;
                color: #24292e !important;
                padding: 0.75rem 1rem !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stPasswordInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {
                border-color: #0366d6 !important;
                box-shadow: 0 0 0 3px rgba(3, 102, 214, 0.15) !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2rem;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #586069 !important;
                font-weight: 500;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: #0366d6 !important;
                font-weight: 600;
            }
            
            /* Metrics */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, rgba(3, 102, 214, 0.08), rgba(111, 66, 193, 0.08)) !important;
                border: 1px solid rgba(3, 102, 214, 0.2) !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
            }
            
            [data-testid="metric-container"] > div:first-child {
                color: #586069 !important;
            }
            
            [data-testid="metric-container"] > div:nth-child(2) {
                color: #0366d6 !important;
                font-size: 2rem !important;
            }
            
            /* Containers */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                border-radius: 8px !important;
                background: linear-gradient(135deg, rgba(3, 102, 214, 0.05), rgba(111, 66, 193, 0.05)) !important;
                transition: all 0.3s ease;
            }
            
            [data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: #0366d6 !important;
                box-shadow: 0 4px 12px rgba(3, 102, 214, 0.15) !important;
            }
            
            /* Dataframe */
            [data-testid="dataFrame"] {
                border-radius: 8px !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Alerts */
            .stAlert {
                border-radius: 8px !important;
                border-left: 4px solid !important;
                padding: 1rem 1.5rem !important;
            }
            
            .stAlert > [data-testid="stAlertContainer"] {
                background-color: transparent !important;
            }
            
            /* Selects */
            .stSelectbox > div > div > select {
                background-color: #fafbfc !important;
                color: #24292e !important;
                border: 1px solid rgba(0, 0, 0, 0.15) !important;
                border-radius: 8px !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: #f0f0f0 !important;
                border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
                padding: 2.5rem 1.8rem !important;
            }
            
            /* Sidebar Navigation Items */
            [data-testid="stSidebar"] > div > div > div > div > button {
                width: 100% !important;
                margin: 0.5rem 0 !important;
                padding: 0.875rem 1.25rem !important;
                border-radius: 8px !important;
                justify-content: flex-start !important;
                text-align: left !important;
                transition: all 0.3s ease !important;
                color: #24292e !important;
            }
            
            /* Sidebar Navigation Items Hover */
            [data-testid="stSidebar"] > div > div > div > div > button:hover {
                background-color: rgba(3, 102, 214, 0.1) !important;
                transform: translateX(4px) !important;
            }
            
            /* Sidebar Active Navigation Item */
            [data-testid="stSidebar"] > div > div > div > div > button[aria-pressed="true"] {
                background: linear-gradient(135deg, rgba(3, 102, 214, 0.2), rgba(3, 102, 214, 0.1)) !important;
                border-left: 3px solid #0366d6 !important;
                padding-left: calc(1.25rem - 3px) !important;
                box-shadow: 0 4px 12px rgba(3, 102, 214, 0.15) !important;
            }
            
            /* Sidebar Text Elements */
            [data-testid="stSidebar"] p {
                margin: 1rem 0 !important;
                padding: 0.5rem 0 !important;
                line-height: 1.6 !important;
                color: #24292e !important;
            }
            
            /* Sidebar Labels */
            [data-testid="stSidebar"] label {
                margin: 0.75rem 0 !important;
                padding: 0.5rem 0.75rem !important;
                font-weight: 500 !important;
                color: #24292e !important;
            }
            
            /* Text */
            p, span, label {
                color: #24292e !important;
            }
        </style>
        """
        st.markdown(light_css, unsafe_allow_html=True)


def get_theme_colors() -> dict:
    """
    Return theme color constants for use in dynamic styling.
    
    Returns:
        Dictionary of theme colors
    """
    return {
        "primary_blue": "#4facfe",
        "primary_cyan": "#00f2fe",
        "primary_purple": "#667eea",
        "primary_dark_purple": "#764ba2",
        "accent_pink": "#ff006e",
        "accent_green": "#06d6a0",
        "bg_dark": "#0f1419",
        "bg_darker": "#0a0d13",
        "text_primary": "#f0f2f6",
        "text_secondary": "#b8bcc4",
    }


def get_gradient_button_style(color1: str = "#667eea", color2: str = "#764ba2") -> str:
    """
    Create a gradient button style inline.
    
    Args:
        color1: First gradient color
        color2: Second gradient color
        
    Returns:
        CSS style string
    """
    return f"background: linear-gradient(135deg, {color1} 0%, {color2} 100%); color: white;"


def create_metric_card_html(label: str, value: str, delta: str = "", icon: str = "📊") -> str:
    """
    Create an HTML metric card with custom styling.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change indicator
        icon: Optional emoji icon
        
    Returns:
        HTML string for the metric card
    """
    delta_html = f"<div style='color: #06d6a0; font-size: 0.875rem; margin-top: 0.5rem;'>{delta}</div>" if delta else ""
    
    html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.08), rgba(118, 75, 162, 0.08));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: #b8bcc4; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">{label}</div>
        <div style="color: #4facfe; font-size: 2rem; font-weight: 700;">{value}</div>
        {delta_html}
    </div>
    """
    return html


def create_alert_html(message: str, alert_type: str = "info", icon: str = "ℹ️") -> str:
    """
    Create a custom styled alert box.
    
    Args:
        message: Alert message text
        alert_type: Type of alert (info, success, error, warning)
        icon: Emoji icon for the alert
        
    Returns:
        HTML string for the alert
    """
    colors = {
        "info": ("#4facfe", "rgba(79, 172, 254, 0.1)"),
        "success": ("#06d6a0", "rgba(6, 214, 160, 0.1)"),
        "error": ("#ff006e", "rgba(255, 0, 110, 0.1)"),
        "warning": ("#ffc107", "rgba(255, 193, 7, 0.1)"),
    }
    
    color, bg_color = colors.get(alert_type, colors["info"])
    
    html = f"""
    <div style="
        background-color: {bg_color};
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    ">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div style="color: #f0f2f6; font-size: 0.95rem;">{message}</div>
    </div>
    """
    return html


def apply_custom_page_style(page_title: str) -> None:
    """
    Apply custom styling for specific pages.
    
    Args:
        page_title: Title of the page (used to apply specific styles)
    """
    # Apply inline base styles for all pages
    apply_inline_styles()
    
    # Page-specific styling
    if page_title == "Dashboard":
        st.markdown("""
        <style>
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(118, 75, 162, 0.1));
                padding: 2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                border: 1px solid rgba(79, 172, 254, 0.2);
                animation: slideIn 0.5s ease-out;
            }
        </style>
        """, unsafe_allow_html=True)
    
    elif page_title == "Scan":
        st.markdown("""
        <style>
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            .scan-form {
                background: linear-gradient(135deg, rgba(79, 172, 254, 0.05), rgba(118, 75, 162, 0.05));
                border: 1px solid rgba(79, 172, 254, 0.2);
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 2rem;
                animation: slideInLeft 0.5s ease-out;
            }
            
            .scan-results {
                background: linear-gradient(135deg, rgba(6, 214, 160, 0.05), rgba(102, 126, 234, 0.05));
                border: 1px solid rgba(6, 214, 160, 0.2);
                border-radius: 12px;
                padding: 2rem;
                margin-top: 2rem;
                animation: slideInRight 0.5s ease-out;
            }
        </style>
        """, unsafe_allow_html=True)


# Session state helper for theme
def set_theme(theme_name: str = "dark") -> None:
    """
    Set the app theme.
    
    Args:
        theme_name: Name of the theme (dark or light)
    """
    if "theme" not in st.session_state:
        st.session_state.theme = theme_name
    if "theme" in st.session_state and st.session_state.theme != theme_name:
        st.session_state.theme = theme_name


def get_theme() -> str:
    """Get current theme from session state."""
    return st.session_state.get("theme", "dark")


def render_theme_toggle() -> None:
    """
    Render a theme toggle button at the top right corner.
    """
    # Add CSS for button styling - specifically target the theme toggle button
    st.markdown(
        """
        <style>
            /* Target theme toggle button specifically */
            div[data-testid="column"]:last-child button {
                width: 60px !important;
                height: 60px !important;
                padding: 0 !important;
                margin: 0 !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 32px !important;
                line-height: 1 !important;
                vertical-align: middle !important;
                gap: 0 !important;
                border-radius: 8px !important;
            }
            
            /* Ensure the button text/icon is centered */
            div[data-testid="column"]:last-child button > span {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                height: 100% !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create columns to position the button on the right
    col1, col2 = st.columns([19, 1])
    
    with col2:
        if st.button("🌙" if get_theme() == "dark" else "☀️", key="theme_toggle"):
            new_theme = "light" if get_theme() == "dark" else "dark"
            set_theme(new_theme)
            st.rerun()


def create_stat_box(
    label: str,
    value: str,
    change: str = "",
    change_positive: bool = True,
    icon: str = "📊"
) -> str:
    """
    Create a statistics box with change indicator.
    
    Args:
        label: Stat label
        value: Stat value
        change: Change text (e.g., "+5%")
        change_positive: Whether change is positive
        icon: Emoji icon
        
    Returns:
        HTML string
    """
    change_color = "#06d6a0" if change_positive else "#ff006e"
    change_html = f"<div style='color: {change_color}; font-size: 0.875rem; margin-top: 0.5rem;'>{change}</div>" if change else ""
    
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(118, 75, 162, 0.1));
        border: 1px solid rgba(79, 172, 254, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: #b8bcc4; font-size: 0.875rem; font-weight: 500;">{label}</div>
        <div style="color: #4facfe; font-size: 1.75rem; font-weight: 700; margin: 0.5rem 0;">{value}</div>
        {change_html}
    </div>
    """


def apply_animation(element_id: str, animation_type: str = "slide-in") -> str:
    """
    Apply animation to an element.
    
    Args:
        element_id: CSS class or ID to animate
        animation_type: Animation type (slide-in, fade-in, etc.)
        
    Returns:
        CSS class string
    """
    animation_map = {
        "slide-in": "animate-slide-in",
        "fade-in": "animate-fade-in",
        "glow": "animate-glow",
        "pulse": "animate-pulse",
    }
    return animation_map.get(animation_type, "")

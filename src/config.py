import streamlit as st

# Configuration de la page
PAGE_CONFIG = {
    "page_title": "PneumoScan PRO - Intelligence Artificielle Médicale",
    "page_icon": "🫁",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://pneumoscan.ai/support',
        'Report a bug': 'https://pneumoscan.ai/bug-report',
        'About': "PneumoScan PRO - Détection IA de Pneumonie v2.0"
    }
}

# Styles CSS Complets
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-soft: 0 8px 32px rgba(31, 38, 135, 0.37);
        --shadow-strong: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    body, .main, .block-container {
        background-color: #121212 !important;
        color: #e0e0e0 !important;
    }

    .sidebar .sidebar-content {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
    }

    button, input, select, textarea {
        background-color: #333 !important;
        color: #eee !important;
        border-color: #444 !important;
    }

    a, a:hover, a:focus {
        color: #80cbc4 !important;
    }
            
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .main {
        padding-top: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }

    .hero-header {
        background: var(--primary-gradient);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: var(--shadow-strong);
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }

    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(31, 38, 135, 0.5);
    }

    .upload-zone {
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .upload-icon {
        font-size: 4rem;
        color: #667eea;
        margin-bottom: 1rem;
        display: block;
    }

    .result-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: var(--shadow-strong);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }

    .probability-display {
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .status-badge {
        display: inline-block;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }

    .status-low { background: var(--success-gradient); color: white; }
    .status-high { background: var(--danger-gradient); color: white; }

    .custom-progress {
        width: 100%;
        height: 8px;
        border-radius: 4px;
        background: rgba(102, 126, 234, 0.2);
        overflow: hidden;
        margin: 1rem 0;
    }

    .progress-fill {
        height: 100%;
        background: var(--primary-gradient);
        border-radius: 4px;
        transition: width 0.5s ease;
    }
</style>
"""

def setup_page():
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
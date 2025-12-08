import streamlit as st

# ==================== CONSTANTES & STATUTS ====================
THRESHOLD_HIGH = 0.70
THRESHOLD_LOW = 0.30

STATUS_IDLE = "IDLE"
STATUS_PROCESSING_IMAGE = "PROCESSING_IMAGE"
STATUS_MODEL_PREDICTING = "MODEL_PREDICTING"
STATUS_REPORT_GENERATING = "REPORT_GENERATING"
STATUS_COMPLETE = "COMPLETE"

PAGE_CONFIG = {
    "page_title": "PneumoScan PRO - Clinical Interface",
    "page_icon": "🫁",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

# ==================== CSS CLINICAL MODERN ====================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* === RESET STREAMLIT === */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Remove Streamlit default spacing */
    .element-container {margin-bottom: 0 !important;}
    div[data-testid="stVerticalBlock"] > div {gap: 0rem;}

    /* === VARIABLES === */
    :root {
        --primary: #667eea;
        --primary-dark: #764ba2;
        --dark-bg: #2d3561;
        --darker-bg: #1a1f3a;
        --darkest-bg: #0a0e1f;
        --text-main: #2d3748;
        --text-light: #718096;
        --bg-light: #f7fafc;
        --border: #e2e8f0;
        --success: #48bb78;
        --warning: #ed8936;
        --danger: #f56565;
    }

    /* === MAIN CONTAINER === */
    .main-wrapper {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 0 auto;
    }

    /* === HEADER === */
    .clinical-header {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 100%);
        color: white;
        padding: 25px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }
    
    .logo-text h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
    }
    
    .logo-text p {
        margin: 0;
        font-size: 12px;
        opacity: 0.7;
    }
    
    .header-actions {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .header-badge {
        background: rgba(255,255,255,0.1);
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* === GRID LAYOUT === */
    .panel-grid {
        display: grid;
        grid-template-columns: 1fr 1.5fr 1fr;
        gap: 0;
        min-height: calc(100vh - 180px);
        background: white;
    }

    /* === PANELS === */
    .panel {
        padding: 30px;
        border-right: 1px solid var(--border);
        background: white;
    }
    
    .panel:last-child {
        border-right: none;
    }
    
    .panel-center {
        background: var(--darker-bg);
        padding: 30px;
        display: flex;
        flex-direction: column;
    }
    
    .panel-title {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--bg-light);
    }
    
    .panel-title-light {
        color: white;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }

    /* === UPLOAD ZONE === */
    .upload-wrapper {
        margin-bottom: 25px;
    }
    
    .upload-zone {
        border: 3px dashed var(--border);
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        background: var(--bg-light);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: var(--primary);
        background: #edf2f7;
    }
    
    .upload-icon {
        font-size: 48px;
        margin-bottom: 15px;
        opacity: 0.5;
    }
    
    .upload-text {
        font-size: 16px;
        color: var(--text-main);
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .upload-hint {
        font-size: 12px;
        color: var(--text-light);
    }
    
    /* Hide Streamlit's default file uploader styling */
    .stFileUploader > div > div {
        padding: 0 !important;
        border: none !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }

    /* === PATIENT INFO === */
    .patient-info {
        background: var(--bg-light);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .patient-header {
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 15px;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border);
    }
    
    .info-row:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .info-label {
        font-size: 11px;
        color: var(--text-light);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        font-size: 13px;
        color: var(--text-main);
        font-weight: 500;
    }

    /* === IMAGE DISPLAY === */
    .image-container {
        flex: 1;
        background: var(--darkest-bg);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        overflow: hidden;
        position: relative;
        min-height: 500px;
    }
    
    .placeholder-content {
        text-align: center;
        color: rgba(255,255,255,0.3);
    }
    
    .placeholder-icon {
        font-size: 80px;
        margin-bottom: 20px;
    }
    
    .placeholder-text {
        font-size: 18px;
        margin-bottom: 8px;
    }
    
    .placeholder-hint {
        font-size: 14px;
        opacity: 0.7;
    }

    /* === IMAGE CONTROLS === */
    .image-controls {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
    }

    /* === RESULTS === */
    .results-empty {
        text-align: center;
        padding: 60px 20px;
        color: var(--text-light);
    }
    
    .results-empty-icon {
        font-size: 64px;
        margin-bottom: 20px;
        opacity: 0.3;
    }
    
    .results-empty-text {
        font-size: 16px;
        color: var(--text-main);
        margin-bottom: 8px;
    }
    
    .results-empty-hint {
        font-size: 12px;
    }
    
    .result-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .result-label {
        font-size: 12px;
        opacity: 0.9;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .result-value {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        background: rgba(255,255,255,0.2);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 5px;
    }
    
    .confidence-bar {
        background: rgba(255,255,255,0.2);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 15px;
    }
    
    .confidence-fill {
        height: 100%;
        background: white;
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    .model-info {
        font-size: 11px;
        margin-top: 8px;
        opacity: 0.8;
    }

    /* === REPORT SECTIONS === */
    .report-section {
        background: var(--bg-light);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .report-title {
        font-size: 14px;
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .report-text {
        font-size: 13px;
        color: var(--text-main);
        line-height: 1.6;
        max-height: 200px;
        overflow-y: auto;
    }

    /* === BUTTONS === */
    .stButton > button {
        width: 100%;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-size: 14px !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: var(--text-main) !important;
        border: 2px solid var(--border) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--primary) !important;
        color: var(--primary) !important;
    }
    
    .stButton > button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }

    /* === DOWNLOAD BUTTON === */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        width: 100%;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border: none !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* === SPINNER === */
    .stSpinner > div {
        border-color: var(--primary) !important;
    }

    /* === TOGGLE === */
    .stCheckbox {
        margin-top: 10px;
    }
    
    .stCheckbox label {
        color: white !important;
        font-weight: 600 !important;
    }

    /* === PROCESSING STATES === */
    .processing-overlay {
        text-align: center;
        padding: 40px;
        color: rgba(255,255,255,0.8);
    }
    
    .processing-spinner {
        font-size: 48px;
        margin-bottom: 20px;
        animation: spin 2s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .processing-text {
        font-size: 16px;
        margin-bottom: 8px;
    }
    
    .processing-detail {
        font-size: 12px;
        opacity: 0.7;
    }

    /* === RESPONSIVE === */
    @media (max-width: 1200px) {
        .panel-grid {
            grid-template-columns: 1fr;
        }
        
        .panel {
            border-right: none;
            border-bottom: 1px solid var(--border);
        }
        
        .panel:last-child {
            border-bottom: none;
        }
    }
</style>
"""

def setup_page():
    """Configure la page avec le style clinique moderne"""
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
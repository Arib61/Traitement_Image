import streamlit as st
from io import BytesIO

# Imports
from src.config import (
    setup_page, 
    STATUS_IDLE, 
    STATUS_PROCESSING_IMAGE, 
    STATUS_MODEL_PREDICTING, 
    STATUS_REPORT_GENERATING, 
    STATUS_COMPLETE
)
from src.model_logic import PneumoniaModel
from src import image_utils, report_utils, ui_components

# Setup Page Configuration
setup_page()

# ==================== SESSION STATE INITIALIZATION ====================
if "app_status" not in st.session_state:
    st.session_state.app_status = STATUS_IDLE
if "processed_img" not in st.session_state:
    st.session_state.processed_img = None
if "probability" not in st.session_state:
    st.session_state.probability = 0.0
if "report_text" not in st.session_state:
    st.session_state.report_text = ""
if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None
if "heatmap_enabled" not in st.session_state:
    st.session_state.heatmap_enabled = False
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# ==================== HELPER FUNCTIONS ====================
def handle_example(fname):
    """Load example X-ray images"""
    try:
        with open(fname, "rb") as f:
            f_bytes = BytesIO(f.read())
            f_bytes.name = fname
            return f_bytes
    except FileNotFoundError:
        st.error(f"Example file not found: {fname}")
        return None

def reset_analysis():
    """Reset the analysis state"""
    st.session_state.app_status = STATUS_IDLE
    st.session_state.processed_img = None
    st.session_state.probability = 0.0
    st.session_state.report_text = ""
    st.session_state.pdf_data = None
    st.session_state.heatmap_enabled = False
    st.session_state.uploaded_file = None

# ==================== MAIN APPLICATION ====================
def main():
    # Render Header
    ui_components.render_header()
    
    # Initialize Model Handler
    model_handler = PneumoniaModel()
    
    # ==================== MAIN LAYOUT (3-COLUMN GRID) ====================
    # Create three columns for the clinical interface
    col_left, col_center, col_right = st.columns([1, 1.5, 1], gap="small")
    
    # ==================== LEFT PANEL: Upload & Patient Info ====================
    with col_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        
        uploaded_file, btn_sain, btn_malade = ui_components.render_left_panel(
            st.session_state.app_status
        )
        
        # Handle file input sources
        file_to_process = None
        
        if btn_sain:
            file_to_process = handle_example("sain.jpeg")
        elif btn_malade:
            file_to_process = handle_example("malade.jpeg")
        elif uploaded_file:
            file_to_process = uploaded_file
        
        # Trigger processing
        if file_to_process and st.session_state.app_status in [STATUS_IDLE, STATUS_COMPLETE]:
            st.session_state.uploaded_file = file_to_process
            st.session_state.app_status = STATUS_PROCESSING_IMAGE
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== STATE MACHINE: Processing Pipeline ====================
    
    # State 1: Image Processing
    if st.session_state.app_status == STATUS_PROCESSING_IMAGE:
        try:
            if st.session_state.uploaded_file:
                filename = st.session_state.uploaded_file.name.lower()
                
                if "dcm" in filename or filename.endswith(".dcm"):
                    st.session_state.processed_img = image_utils.process_dicom(
                        st.session_state.uploaded_file
                    )
                else:
                    st.session_state.processed_img = image_utils.process_standard(
                        st.session_state.uploaded_file
                    )
                
                st.session_state.app_status = STATUS_MODEL_PREDICTING
                st.rerun()
        except Exception as e:
            st.error(f"Image processing error: {str(e)}")
            reset_analysis()
    
    # State 2: Model Prediction
    elif st.session_state.app_status == STATUS_MODEL_PREDICTING:
        try:
            if st.session_state.processed_img is not None:
                img_np = image_utils.prepare_for_model(st.session_state.processed_img)
                st.session_state.probability = model_handler.predict(img_np)
                st.session_state.app_status = STATUS_REPORT_GENERATING
                st.rerun()
        except Exception as e:
            st.error(f"Model prediction error: {str(e)}")
            reset_analysis()
    
    # State 3: Report Generation
    elif st.session_state.app_status == STATUS_REPORT_GENERATING:
        try:
            # Get Gemini API key from secrets
            api_key = st.secrets.get("GEMINI_API_KEY", "")
            
            # Generate AI report
            st.session_state.report_text = report_utils.get_gemini_response(
                st.session_state.probability, 
                api_key
            )
            
            # Generate PDF
            st.session_state.pdf_data = report_utils.create_pdf(
                st.session_state.probability,
                st.session_state.report_text,
                st.session_state.processed_img
            )
            
            st.session_state.app_status = STATUS_COMPLETE
            st.rerun()
        except Exception as e:
            st.error(f"Report generation error: {str(e)}")
            # Still show results even if report generation fails
            st.session_state.report_text = "Report generation encountered an error. Please check API configuration."
            st.session_state.app_status = STATUS_COMPLETE
            st.rerun()
    
    # ==================== CENTER PANEL: Image Display ====================
    with col_center:
        st.markdown('<div class="panel panel-center">', unsafe_allow_html=True)
        
        # Sync heatmap toggle state
        if "heatmap_toggle" in st.session_state:
            st.session_state.heatmap_enabled = st.session_state.heatmap_toggle
        
        ui_components.render_center_panel(
            st.session_state.app_status,
            st.session_state.processed_img,
            st.session_state.heatmap_enabled
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== RIGHT PANEL: Results & Report ====================
    with col_right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        
        ui_components.render_right_panel(
            st.session_state.app_status,
            st.session_state.probability,
            st.session_state.report_text,
            st.session_state.pdf_data
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== FOOTER: Additional Actions ====================
    # Add a subtle footer with reset option
    if st.session_state.app_status == STATUS_COMPLETE:
        st.markdown("---")
        col_footer1, col_footer2, col_footer3 = st.columns([1, 1, 1])
        
        with col_footer2:
            if st.button("🔄 New Analysis", use_container_width=True, type="secondary"):
                reset_analysis()
                st.rerun()

# ==================== APPLICATION ENTRY POINT ====================
if __name__ == "__main__":
    main()
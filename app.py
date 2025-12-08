import streamlit as st
from io import BytesIO

# Import des modules locaux
from src.config import setup_page
from src.model_logic import PneumoniaModel
from src import image_utils, report_utils, ui_components

# 1. Configuration initiale
setup_page()

def main():
    # 2. Affichage UI
    ui_components.render_hero()
    confidence_threshold = ui_components.render_sidebar()

    # 3. Chargement du modèle
    model_handler = PneumoniaModel()
    if not model_handler.model:
        return

    # 4. Interface principale
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #667eea; text-align: center; margin-bottom: 2rem;">📁 Upload d'Image</h3>
        </div>
        """, unsafe_allow_html=True)
        
        upload_type = st.radio(
            "🔍 Type d'image :",
            ["🏥 DICOM (.dcm)", "📸 Standard (JPG/PNG)"],
            index=1,
            horizontal=True
        )
        
        # Gestion des exemples préchargés
        if "selected_image_path" not in st.session_state:
            st.session_state.selected_image_path = None

        st.markdown("### 📂 Exemples")
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            if st.button("🖼️ Charger Sain"):
                st.session_state.selected_image_path = "sain.jpeg"
        with col_ex2:
            if st.button("🖼️ Charger Malade"):
                st.session_state.selected_image_path = "malade.jpeg"

        # Gestion fichier
        uploaded_file = None
        if st.session_state.selected_image_path:
            try:
                with open(st.session_state.selected_image_path, "rb") as f:
                    uploaded_file = BytesIO(f.read())
                    uploaded_file.name = st.session_state.selected_image_path
                    st.info(f"Image chargée : {st.session_state.selected_image_path}")
            except FileNotFoundError:
                st.error("Image d'exemple introuvable. Veuillez uploader un fichier.")

        if not uploaded_file:
            uploaded_file = st.file_uploader(
                "Glissez-déposez votre fichier ici",
                type=["dcm", "jpg", "jpeg", "png"]
            )
    
    with col2:
        if uploaded_file:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #667eea; text-align: center;">🔬 Analyse en Cours</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # A. Traitement
            with st.spinner("Traitement de l'image..."):
                if "DICOM" in upload_type:
                    processed_img = image_utils.process_dicom(uploaded_file)
                else:
                    processed_img = image_utils.process_standard(uploaded_file)
            
            if processed_img:
                st.image(processed_img, caption="Image Analysée", use_container_width=True)

                # B. Prédiction
                img_np = image_utils.prepare_for_model(processed_img)
                probability = model_handler.predict(img_np)

                if probability is not None:
                    display_results(probability, processed_img)

def display_results(probability, image):
    st.divider()
    
    # Indicateurs Visuels
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: #667eea;">🎯 Probabilité</h3>
            <div class="probability-display">{probability*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.plotly_chart(report_utils.create_chart(probability), use_container_width=True)
    
    with c3:
        status = "RISQUE ÉLEVÉ" if probability > 0.7 else "RISQUE MODÉRÉ" if probability > 0.3 else "RISQUE FAIBLE"
        color = "status-high" if probability > 0.7 else "status-low"
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; display: flex; align-items: center; justify-content: center; height: 100%;">
            <div class="status-badge {color}">{status}</div>
        </div>
        """, unsafe_allow_html=True)

    # Section Rapport IA & PDF
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    if api_key:
        st.markdown("### 📋 Rapport Médical & PDF")
        with st.expander("📝 Lire le rapport généré par l'IA", expanded=True):
            with st.spinner("Génération du rapport et du PDF..."):
                # 1. Générer le texte
                report_text = report_utils.get_gemini_response(probability, api_key)
                st.markdown(report_text)
                
                # 2. Générer le PDF
                pdf_data = report_utils.create_pdf(probability, report_text, image)
                
                if pdf_data:
                    st.download_button(
                        label="📥 Télécharger le Rapport PDF Officiel",
                        data=pdf_data,
                        file_name=f"PneumoScan_Rapport.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error("Erreur génération PDF.")
    else:
        st.warning("⚠️ Clé API Gemini manquante dans .streamlit/secrets.toml")

if __name__ == "__main__":
    main()
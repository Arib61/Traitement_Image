import streamlit as st
import datetime
from src.config import STATUS_IDLE, STATUS_COMPLETE

def render_header():
    """Affiche le Header 'PneumoScan PRO' style dashboard."""
    st.markdown("""
    <div class="clinical-header">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 2rem;">🫁</div>
            <div>
                <h1 style="margin:0; font-size: 1.5rem; font-weight: 700; color: white;">PneumoScan PRO</h1>
                <p style="margin:0; font-size: 0.8rem; opacity: 0.8;">Interface Clinique Assistée par IA</p>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 6px; font-size: 0.8rem;">
                👤 Dr. Smith (Radiologie)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_left_panel(status):
    """Panneau Gauche : Upload & Infos Patient (Statique)."""
    st.markdown('<div class="panel-title">📤 Source & Patient</div>', unsafe_allow_html=True)
    
    # 1. Upload
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Sélectionner un fichier RX", 
        type=["dcm", "jpg", "png", "jpeg"],
        label_visibility="collapsed",
        disabled=(status != STATUS_IDLE and status != STATUS_COMPLETE)
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Boutons exemples
    c1, c2 = st.columns(2)
    with c1:
        load_sain = st.button("🟢 Sain", key="btn_sain", disabled=(status != STATUS_IDLE and status != STATUS_COMPLETE))
    with c2:
        load_malade = st.button("🔴 Malade", key="btn_malade", disabled=(status != STATUS_IDLE and status != STATUS_COMPLETE))

    # 2. Infos Patient (Dummy Data pour le réalisme)
    st.markdown(f"""
    <div class="patient-card">
        <div style="font-weight: 700; color: #2d3561; margin-bottom: 10px;">DOSSIER PATIENT</div>
        <div class="info-row"><span class="info-label">ID</span><span class="info-val">P-{datetime.datetime.now().strftime('%Y-%m')}-042</span></div>
        <div class="info-row"><span class="info-label">NOM</span><span class="info-val">ANONYME</span></div>
        <div class="info-row"><span class="info-label">AGE/GENRE</span><span class="info-val">45 ans / M</span></div>
        <div class="info-row"><span class="info-label">DATE EXAMEN</span><span class="info-val">{datetime.datetime.now().strftime('%d/%m/%Y')}</span></div>
        <div class="info-row"><span class="info-label">INDICATION</span><span class="info-val">Toux, Fièvre, Dyspnée</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    return uploaded_file, load_sain, load_malade

def render_center_panel(status, image, heatmap_enabled):
    """Panneau Central : Affichage sombre de l'image."""
    
    # On utilise st.markdown pour ouvrir le div sombre
    st.markdown('<div class="center-panel-dark">', unsafe_allow_html=True)
    
    if status == STATUS_IDLE:
        st.markdown("""
            <div style="opacity: 0.5;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📷</div>
                <h3>En attente d'image</h3>
                <p>Chargez une radio pour commencer l'analyse</p>
            </div>
        """, unsafe_allow_html=True)
    
    elif image:
        # Titre interne
        st.markdown('<h4 style="color:white; margin-bottom: 1rem;">🖼️ Vue Radiologique</h4>', unsafe_allow_html=True)
        
        # Affichage image
        st.image(image, use_container_width=True)
        
        # Contrôles (Boutons simulés)
        if status == STATUS_COMPLETE:
            st.markdown("---")
            # Le bouton toggle pour la heatmap sera géré hors du HTML pur pour l'interactivité
            
    else:
        # État de chargement
        st.spinner("Chargement de la vue...")
        
    st.markdown('</div>', unsafe_allow_html=True) # Fermeture div

def render_right_panel(status, probability, report_text, pdf_data):
    """Panneau Droit : Résultats."""
    st.markdown('<div class="panel-title">📋 Résultats & Rapport</div>', unsafe_allow_html=True)
    
    if status != STATUS_COMPLETE:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0; opacity: 0.5;">
            <div style="font-size: 3rem;">⏳</div>
            <p>En attente des résultats...</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # 1. Carte de Résultat
    risk_label = "RISQUE ÉLEVÉ" if probability > 0.7 else "RISQUE MODÉRÉ" if probability > 0.3 else "RISQUE FAIBLE"
    
    st.markdown(f"""
    <div class="result-card-gradient">
        <div style="font-size: 0.9rem; opacity: 0.9;">PROBABILITÉ PNEUMONIE</div>
        <div class="big-score">{probability*100:.1f}%</div>
        <div class="risk-badge">{risk_label}</div>
        <div style="margin-top: 15px; font-size: 0.8rem; opacity: 0.8;">
            Modèle DenseNet-121 (Confiance ~94%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Rapport Rapide
    st.markdown("##### 🤖 Analyse Synthétique")
    st.markdown(f"""
    <div style="background: #f8fafc; padding: 15px; border-radius: 8px; font-size: 0.9rem; max-height: 200px; overflow-y: auto; margin-bottom: 1rem;">
        {report_text[:400]}...
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Actions
    if pdf_data:
        st.download_button(
            "📄 Exporter le Rapport PDF",
            data=pdf_data,
            file_name="rapport_clinique.pdf",
            mime="application/pdf"
        )
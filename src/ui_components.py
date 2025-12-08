import streamlit as st

def render_hero():
    """Affiche l'en-tête principal."""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🫁 PNEUMOSCAN PRO</h1>
        <p class="hero-subtitle">Intelligence Artificielle Médicale • Détection Avancée de Pneumonie</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Affiche la barre latérale et retourne les paramètres."""
    with st.sidebar:
        st.markdown("""
        <div class="glass-card">
            <h3 style="text-align: center; color: #667eea; margin-bottom: 1rem;">
                🎛️ Paramètres
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        confidence_threshold = st.slider(
            "Seuil de Confiance (%)", 
            min_value=50, max_value=95, value=75
        )
        
        st.markdown("---")
        st.markdown("""
        <div class="glass-card">
            <h4>ℹ️ Système</h4>
            <p style="font-size: 0.8rem; color: #666;">
                <strong>Version :</strong> 2.0<br>
                <strong>Modèle :</strong> DenseNet-121<br>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return confidence_threshold
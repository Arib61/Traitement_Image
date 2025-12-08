import google.generativeai as gen_ai
import datetime
from fpdf import FPDF
import tempfile
import os
from PIL import Image
import plotly.graph_objects as go
import streamlit as st
import time

def get_gemini_response(probability: float, api_key: str) -> str:
    """
    Génère le texte du rapport via l'API Gemini.
    Si l'API échoue (Erreur 429 ou autre), génère un rapport de secours local.
    """
    try:
        gen_ai.configure(api_key=api_key)
        model = gen_ai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        En tant qu'expert en radiologie, génère un rapport médical professionnel et détaillé en français pour :
        
        **DONNÉES D'ANALYSE :**
        - Probabilité de pneumonie détectée : {probability*100:.2f}%
        - Date d'analyse : {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}
        - Système : PneumoScan PRO v2.0
        
        **STRUCTURE REQUISE :**
        **🔍 ANALYSE RADIOLOGIQUE :** Description des observations et comparaison avec la normale.
        **📊 INTERPRÉTATION CLINIQUE :** Signification de la probabilité, risques.
        **⚕️ RECOMMANDATIONS MÉDICALES :** Conduite à tenir, examens.
        **⚠️ LIMITATIONS :** Limites de l'IA.
        
        Format professionnel, emojis médicaux, ton rigoureux. Max 500 mots.
        """
        
        # Tentative d'appel API
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return _generate_fallback_report(probability)

    except Exception as e:
        # En cas d'erreur (Quota 429, internet coupé, clé invalide)
        # On log l'erreur dans la console pour le développeur
        print(f"⚠️ Erreur API Gemini : {str(e)}")
        print("ℹ️ Passage au rapport de secours (Fallback).")
        
        # On retourne le rapport généré localement sans IA
        return _generate_fallback_report(probability)

def _generate_fallback_report(probability: float) -> str:
    """Génère un rapport standard basé sur des modèles prédéfinis (Sans IA)."""
    
    date_str = datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')
    percentage = f"{probability*100:.1f}%"
    
    if probability > 0.7:
        conclusion = "RISQUE ÉLEVÉ DE PNEUMONIE"
        details = """
        L'analyse des opacités pulmonaires suggère une forte probabilité pathologique.
        Des zones de consolidation sont suspectées.
        """
        recommendation = "Consultation médicale urgente et confirmation radiologique nécessaire."
    elif probability > 0.3:
        conclusion = "RISQUE MODÉRÉ / INCERTAIN"
        details = """
        L'analyse détecte des anomalies mineures ou des artefacts nécessitant une vérification.
        Le tableau clinique n'est pas clairement défini par l'image seule.
        """
        recommendation = "Surveillance clinique et corrélation avec les symptômes du patient."
    else:
        conclusion = "RISQUE FAIBLE / NORMAL"
        details = """
        Les champs pulmonaires apparaissent clairs.
        Absence d'opacités significatives détectées par le modèle.
        """
        recommendation = "Pas de suivi particulier suggéré sur la base de cette image seule."

    return f"""
    RAPPORT GÉNÉRÉ PAR PNEUMOSCAN PRO (MODE HORS-LIGNE)
    Date : {date_str}
    
    🔍 RÉSULTAT DE L'ANALYSE
    -----------------------
    Probabilité calculée : {percentage}
    Conclusion algorithmique : {conclusion}
    
    📊 DÉTAILS TECHNIQUES
    {details}
    
    ⚕️ RECOMMANDATIONS STANDARDS
    {recommendation}
    
    ⚠️ NOTE
    Ce rapport a été généré par le système expert interne suite à une indisponibilité
    temporaire du module d'IA générative avancée. La précision de la détection
    numérique (le pourcentage) reste inchangée et valide.
    """

def create_chart(probability: float):
    """Crée le graphique de jauge."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilité de Pneumonie (%)"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
        }
    ))
    fig.update_layout(
        height=300,
        font={'color': "darkblue", 'family': "Inter"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_pdf(probability: float, report_text: str, image: Image.Image) -> bytes:
    """Crée un PDF professionnel complet."""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # En-tête
        pdf.set_font("helvetica", "B", 20)
        pdf.set_text_color(51, 51, 153)
        pdf.cell(0, 15, 'PNEUMOSCAN PRO - RAPPORT D\'ANALYSE', 0, 1, 'C')
        
        # Ligne
        pdf.set_draw_color(102, 126, 234)
        pdf.set_line_width(0.5)
        pdf.line(20, 35, 190, 35)
        
        # Infos
        pdf.ln(10)
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 8, f'Date : {datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")}', 0, 1)
        pdf.cell(0, 8, f'Système : PneumoScan PRO v2.0', 0, 1)
        
        # Résultat
        pdf.ln(10)
        pdf.set_font("helvetica", "B", 16)
        pdf.set_text_color(102, 126, 234)
        pdf.cell(0, 12, 'RÉSULTAT PRINCIPAL', 0, 1)
        
        pdf.set_fill_color(240, 242, 255)
        pdf.rect(20, pdf.get_y(), 170, 25, 'F')
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(51, 51, 153)
        pdf.cell(0, 12, f'Probabilité de pneumonie : {probability*100:.1f}%', 0, 1, 'C')
        
        # Image
        pdf.ln(20)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            img_resized = image.resize((300, 300), Image.Resampling.LANCZOS)
            img_resized.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        pdf.image(tmp_path, x=55, y=pdf.get_y(), w=100)
        os.unlink(tmp_path)
        
        # Rapport texte
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.set_text_color(102, 126, 234)
        pdf.cell(0, 12, 'RAPPORT DÉTAILLÉ', 0, 1)
        
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        
        # Nettoyage du texte pour FPDF (latin-1 ne supporte pas certains caractères)
        # On remplace les caractères problématiques courants
        safe_text = report_text.replace("’", "'").replace("œ", "oe").replace("€", "EUR")
        clean_text = safe_text.encode('latin-1', 'ignore').decode('latin-1')
        
        pdf.multi_cell(0, 6, clean_text)
        
        # Footer
        pdf.ln(15)
        pdf.set_font("helvetica", "I", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, "AVERTISSEMENT : Ce rapport est une aide au diagnostic générée par IA. Consultez un médecin.")
        
        return pdf.output(dest='S').encode('latin-1')
        
    except Exception as e:
        print(f"Erreur PDF : {e}")
        return None
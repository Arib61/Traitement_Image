import pydicom
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import streamlit as st

def process_dicom(file) -> Image.Image:
    """Traite un fichier DICOM et retourne une image PIL."""
    try:
        dicom = pydicom.dcmread(file)
        img_array = dicom.pixel_array
        
        # Normalisation et conversion
        img_normalized = cv2.convertScaleAbs(img_array, alpha=(255.0 / np.max(img_array)))
        img_pil = Image.fromarray(img_normalized).convert("L")
        
        # Amélioration de l'image
        enhancer = ImageEnhance.Contrast(img_pil)
        img_enhanced = enhancer.enhance(1.2)
        
        return img_enhanced
    except Exception as e:
        st.error(f"Erreur lors du traitement DICOM : {str(e)}")
        return None

def process_standard(file) -> Image.Image:
    """Traite une image standard et retourne une image PIL."""
    try:
        img = Image.open(file).convert("L")
        
        # Amélioration de l'image
        enhancer = ImageEnhance.Contrast(img)
        img_enhanced = enhancer.enhance(1.1)
        
        return img_enhanced
    except Exception as e:
        st.error(f"Erreur lors du traitement de l'image : {str(e)}")
        return None

def prepare_for_model(image: Image.Image) -> np.ndarray:
    """Prépare l'image PIL pour le modèle (resize, numpy conversion float32)."""
    img = image.convert("L").resize((224, 224))
    img_np = np.array(img).astype(np.float32)
    return img_np
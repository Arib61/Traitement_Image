import torch
import torchxrayvision as xrv
import numpy as np
import streamlit as st

class PneumoniaModel:
    def __init__(self):
        self.model = self._load_model()

    @staticmethod
    @st.cache_resource
    def _load_model():
        """Charge le modèle de détection de pneumonie avec mise en cache."""
        try:
            model = xrv.models.DenseNet(weights="densenet121-res224-rsna").eval()
            return model
        except Exception as e:
            st.error(f"Erreur lors du chargement du modèle : {str(e)}")
            return None

    def predict(self, img_np: np.ndarray) -> float:
        """Effectue la prédiction sur une image numpy."""
        if self.model is None:
            return None
        
        try:
            # Normalisation par TorchXRayVision
            img_np_normalized = xrv.datasets.normalize(img_np, maxval=255.0)
            
            # Transformation en Tensor
            img_tensor = torch.from_numpy(img_np_normalized).unsqueeze(0).unsqueeze(0).float()

            # Prédiction
            with torch.no_grad():
                output = self.model(img_tensor)[0]

            if "Pneumonia" not in self.model.pathologies:
                st.error("❌ Label 'Pneumonia' non trouvé dans le modèle.")
                return None

            pneumonia_idx = self.model.pathologies.index("Pneumonia")
            raw_score = output[pneumonia_idx].item()
            probability = torch.sigmoid(torch.tensor(raw_score)).item()

            return probability

        except Exception as e:
            st.error(f"❌ Erreur prédiction : {str(e)}")
            return None
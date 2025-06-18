import cv2
import numpy as np
from tensorflow.keras.models import load_model

# função para verificar se o mamoeiro é anômalo ou não

class ModeloAgrineural:
    
    def __init__(self):
        self.modelo = load_model("MVC/services/model_checkpoint.h5transistor_AE_epoch_48.h5", compile=False)
        self.threshold = 0.003638065652921796  # Definido como constante
        
        
    def setTrashold(self, novo_threshold):
        self.threshold = novo_threshold
    
    def analisarImagem(self, caminhoArquivo):
        img = cv2.imread(caminhoArquivo)
        img = cv2.resize(img, (256, 256))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_norm = img.astype("float32") / 255.0
        entrada = np.expand_dims(img_norm, axis=0)

        reconstruida = self.modelo.predict(entrada)[0]
        erro = np.mean((img_norm - reconstruida) ** 2)
        return  "Anômala" if erro > self.threshold else "Normal"
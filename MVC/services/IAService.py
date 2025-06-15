import cv2
import numpy as np
from tensorflow.keras.models import load_model

modelo_ae = load_model("MVC/services/model_checkpoint.h5transistor_AE_epoch_48.h5", compile=False)
threshold = 0.003638065652921796

# função para verificar se o mamoeiro é anômalo ou não

def analisarImagem(caminhoArquivo):
    img = cv2.imread(caminhoArquivo)
    img = cv2.resize(img, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_norm = img.astype("float32") / 255.0
    entrada = np.expand_dims(img_norm, axis=0)

    reconstruida = modelo_ae.predict(entrada)[0]
    erro = np.mean((img_norm - reconstruida) ** 2)
    return  "Anômala" if erro > threshold else "Normal"
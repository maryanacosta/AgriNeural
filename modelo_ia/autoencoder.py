import cv2
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Carrega o modelo
modelo = load_model("C:\\Users\\ACER\\Downloads\\model_checkpoint.h5transistor_AE_epoch_48.h5", compile=False)

# Lê e pré-processa uma imagem
img_path = "C:\\Users\\ACER\\Downloads\\mamao3.jpg"
img = cv2.imread(img_path)
img = cv2.resize(img, (256, 256))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_norm = img.astype("float32") / 255.0
entrada = np.expand_dims(img_norm, axis=0)

# Reconstrução
reconstruida = modelo.predict(entrada)[0]

# Calcula o erro quadrático médio
erro = np.mean((img_norm - reconstruida) ** 2)

# Define o limiar de erro
threshold = 0.003638065652921796

if erro > threshold:
    print("Folha ANÔMALA!")
else:
    print("Folha NORMAL")


# Visualiza
plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img)
plt.axis("off")
plt.subplot(1,2,2)
plt.title("Reconstruída")
plt.imshow((reconstruida * 255).astype(np.uint8))
plt.axis("off")
plt.tight_layout()
plt.show()

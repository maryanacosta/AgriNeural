from tensorflow.keras.models import load_model
#from tensorflow.keras.utils import plot_model
import visualkeras

# Caminho para o arquivo .h5
caminho = "C:\\Users\\ACER\\Downloads\\model_checkpoint.h5transistor_AE_epoch_48.h5"
# Carregar o modelo
#modelo = load_model("C:\\Users\\ACER\\Downloads\\model_checkpoint.h5transistor_AE_epoch_48.h5")
modelo = load_model(caminho, compile=False)

#plot_model(modelo, to_file="modelo.png", show_shapes=True, show_layer_names=True)
visualkeras.layered_view(modelo, to_file='modelo_lego.png', legend=True)

# Verificar a arquitetura
modelo.summary()


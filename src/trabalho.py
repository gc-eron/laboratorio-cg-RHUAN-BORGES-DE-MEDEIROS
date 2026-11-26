import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Trabalho de Computação Gráfica")

foto = Image.open("imagens/foto-trabalho.png").convert("RGB")
img = np.array(foto)
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
st.image(img, caption="Foto original")

st.header("1. Saturação")
fator_saturacao = st.slider("Fator de saturação", 0.0, 2.0, 1.0)
hsv_saturacao = hsv.copy()
saturacao = hsv[:, :, 1].astype(float) * fator_saturacao
hsv_saturacao[:, :, 1] = np.clip(saturacao, 0, 255).astype(np.uint8)
img_saturacao = cv2.cvtColor(hsv_saturacao, cv2.COLOR_HSV2RGB)
st.image(img_saturacao, caption="Saturação ajustada")

st.header("2. Brilho")
fator_brilho = st.slider("Fator de brilho", 0.0, 2.0, 1.0)
hsv_brilho = hsv.copy()
brilho = hsv[:, :, 2].astype(float) * fator_brilho
hsv_brilho[:, :, 2] = np.clip(brilho, 0, 255).astype(np.uint8)
img_brilho = cv2.cvtColor(hsv_brilho, cv2.COLOR_HSV2RGB)
st.image(img_brilho, caption="Brilho ajustado")

st.header("3. Matiz girada")
giro = st.slider("Giro da matiz (graus)", 0, 360, 120, step=2)
hsv_matiz = hsv.copy()
matiz = (hsv[:, :, 0].astype(int) + giro // 2) % 180
hsv_matiz[:, :, 0] = matiz.astype(np.uint8)
img_matiz = cv2.cvtColor(hsv_matiz, cv2.COLOR_HSV2RGB)
st.image(img_matiz, caption="Matiz girada")

st.header("9. Recorte")
altura, largura = img.shape[:2]
tamanho_maximo = min(altura, largura) - 1
tamanho = st.slider("Lado do quadrado (pixels)", 1, tamanho_maximo, max(1, tamanho_maximo // 3))
limite_x = largura - tamanho
limite_y = altura - tamanho
x = st.slider("Coluna inicial (x)", 0, limite_x, min(largura // 4, limite_x))
y = st.slider("Linha inicial (y)", 0, limite_y, min(altura // 4, limite_y))
recorte = img[y:y + tamanho, x:x + tamanho]
st.image(recorte, caption="Recorte quadrado")

st.header("11. Espelhamento")
horizontal = img[:, ::-1]
vertical = img[::-1, :]
coluna_horizontal, coluna_vertical = st.columns(2)
coluna_horizontal.image(horizontal, caption="Espelhamento horizontal")
coluna_vertical.image(vertical, caption="Espelhamento vertical")

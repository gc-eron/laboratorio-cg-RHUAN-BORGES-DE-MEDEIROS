
import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Atv 5: HSV e recorte")


foto = Image.open("imagens/fox.jpeg").convert("RGB")
img = np.array(foto)


st.header("1. HSV")
col1, col2 = st.columns(2)

hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

col1.image(img, caption="Imagem original")

so_h = hsv.copy()
so_h[:, :, 1] = 255
so_h[:, :, 2] = 255

rgb_h = cv2.cvtColor(so_h, cv2.COLOR_HSV2RGB)
col2.image(rgb_h, caption="H")

# 2. Mudando o HSV
st.header("2. Mudando o HSV")
col1, col2 = st.columns(2)

fator = col1.slider("Saturação", 0.0, 2.0, 1.5)

hsv2 = hsv.copy()
s = hsv[:, :, 1].astype(float) * fator
hsv2[:, :, 1] = np.clip(s, 0, 255).astype(np.uint8)

col1.image(
    cv2.cvtColor(hsv2, cv2.COLOR_HSV2RGB),
    caption="Saturação"
)

fator_brilho = col1.slider("Brilho", 0.0, 2.0, 1.0)

hsv3 = hsv.copy()
v = hsv[:, :, 2].astype(float) * fator_brilho
hsv3[:, :, 2] = np.clip(v, 0, 255).astype(np.uint8)

col1.image(
    cv2.cvtColor(hsv3, cv2.COLOR_HSV2RGB),
    caption="Brilho"
)

giro = col2.slider("Giro (graus)", 0, 360, 120)

hsv_giro = hsv.copy()
hsv_giro[:, :, 0] = (
    (hsv[:, :, 0].astype(int) + giro // 2) % 180
).astype(np.uint8)

col2.image(
    cv2.cvtColor(hsv_giro, cv2.COLOR_HSV2RGB),
    caption="Matiz girada"
)

# 3. Faixa na escala
st.header("3. Faixa na escala")
col1, col2 = st.columns(2)

escala = np.zeros((1, 12, 3), dtype=np.uint8)
escala[0, :, 0] = np.arange(0, 180, 15)
escala[0, :, 1] = 255
escala[0, :, 2] = 255

rgb = cv2.cvtColor(escala, cv2.COLOR_HSV2RGB)

col1.image(
    rgb.repeat(40, axis=0).repeat(40, axis=1),
    caption="Escala"
)

h_min, h_max = col1.slider(
    "Faixa de H na escala",
    0, 179, (90, 130)
)

mascara = cv2.inRange(
    escala,
    (h_min, 0, 0),
    (h_max, 255, 255)
)

mascara_ampliada = mascara.repeat(40, axis=0).repeat(40, axis=1)

col2.image(mascara_ampliada, caption="Máscara")

# 4. Máscara de cor
st.header("4. Máscara de cor")
col1, col2 = st.columns(2)

h_min, h_max = col1.slider(
    "Faixa de H",
    0, 179, (140, 179)
)

mascara = cv2.inRange(
    hsv,
    (h_min, 60, 40),
    (h_max, 255, 255)
)

col1.image(mascara, caption="Máscara")

foto_cor = cv2.bitwise_and(img, img, mask=mascara)

col2.image(foto_cor, caption="Foto com a cor selecionada")

# 5. Recorte
st.header("5. Recorte")
col1, col2 = st.columns(2)

altura, largura = img.shape[:2]

y = col1.slider("y", 0, altura - 1, altura // 4)
x = col1.slider("x", 0, largura - 1, largura // 4)

t = col1.slider(
    "Tamanho",
    1,
    min(altura, largura),
    max(1, min(altura, largura) // 3)
)

recorte = img[
    y:min(y + t, altura),
    x:min(x + t, largura)
]

col1.image(recorte, caption="Recorte")

negativo = img.copy()

negativo[
    y:min(y + t, altura),
    x:min(x + t, largura)
] = 255 - negativo[
    y:min(y + t, altura),
    x:min(x + t, largura)
]

col2.image(negativo, caption="Negativo dentro do recorte")

# 6. Espelhamento
st.header("6. Espelhamento")
col1, col2 = st.columns(2)

horizontal = img[:, ::-1]
vertical = img[::-1, :]

col1.image(horizontal, caption="Espelhada na horizontal")
col2.image(vertical, caption="Espelhada na vertical")

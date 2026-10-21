import streamlit as st
import numpy as np

def ampliar(imagem, k):
    return imagem.repeat(k, axis=0).repeat(k, axis=1)

bandeira = np.zeros((12, 18, 3), dtype=np.uint8)

bandeira[0:4, :] = (0, 0, 0)        
bandeira[4:8, :] = (255, 255, 255)  
bandeira[8:12, :] = (0, 122, 61)    

for y in range(12):
    largura = int(7 * (1 - abs(y - 5.5) / 5.5))
    bandeira[y, :largura + 1] = (206, 17, 38)

st.image(ampliar(bandeira, 20))
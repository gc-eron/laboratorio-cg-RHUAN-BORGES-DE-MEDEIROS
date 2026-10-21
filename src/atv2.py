import numpy as np
import streamlit as st
def ampliar(imagem, k=30):
return imagem.repeat(k, axis=0).repeat(k, axis=1)
st.title("Imagem como matriz")
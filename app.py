import os
import shutil
import subprocess
import hashlib
import streamlit as st
import sys

# Agregar la ruta actual para que importe sin problema tus archivos de ANTLR
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from antlr4 import *
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser
from bazilio import BazilioVisitor  # O tu visitor/listener principal

st.set_page_config(page_title="Compilador Bazilio - ANTLR", page_icon="🎵")

st.title("Compilador Bazilio (ANTLR) en la Nube")
st.write("Escribe tu código en Bazilio y genera tus partituras y audios desde cualquier dispositivo.")

# Texto predeterminado actualizado según tu código funcional
codigo_usuario = st.text_area("Código Bazilio:", "Main\n|:\n  (:){E4 F3}\n:|\n", height=150)

if st.button("Compilar y Generar", type="primary"):
    if not codigo_usuario.strip():
        st.warning("Por favor ingresa código.")
    else:
        try:
            os.makedirs("Practica", exist_ok=True)
            
            # 1. Procesar con ANTLR
            input_stream = InputStream(codigo_usuario)
            lexer = BazilioLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = BazilioParser(stream)
            tree = parser.programa()
            
            # 2. Ejecutar tu Visitor/Listener o lógica que genera el .ly
            base = os.path.join("Practica", f"partitura_{hashlib.md5(codigo_usuario.encode()).hexdigest()[:6]} ")
            
            ruta_bzl = "temp_cloud.bzl"
            with open(ruta_bzl, "w", encoding="utf-8") as f:
                f.write(codigo_usuario)
                
            res = subprocess.run(["python3", "bazilio.py", ruta_bzl, "Main"], capture_output=True, text=True)
            
            if res.returncode != 0:
                st.error(f"Error de sintaxis ANTLR / Ejecución:\n{res.stderr}")
            else:
                st.success("¡Compilación y generación exitosa con ANTLR!")
                
                col1, col2, col3 = st.columns(3)
                st.info("Revisa los archivos generados en la carpeta de salida de tu script.")

        except Exception as e:
            st.error(f"Error: {e}")
import streamlit as st
import streamlit.components.v1 as components

def markmap(html_content: str, height: int = 300):
    # Declara o nome do componente. O segundo parâmetro é o path para o diretório contendo o componente.
    component = components.declare_component("markmap", path="/markmap.py")

    # Chamando o componente e passando o HTML
    component(html=html_content, height=height)

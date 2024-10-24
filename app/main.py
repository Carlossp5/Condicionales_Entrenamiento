import streamlit as st
import modules.Selector_Tareas_v3
import modules.Selector_Tiempos_v0
import modules.Selector_Entrenos_v1

st.set_page_config(page_title="Selector de Entrenos", layout="wide")

# Sidebar for navigation
st.sidebar.title("Selector de Funcionalidad")

# Dictionary to map page names to functions
pages = {
    "Selector de Tareas": modules.Selector_Tareas_v3.show,
    "Selector de Tiempos": modules.Selector_Tiempos_v0.show,
    "CREADOR DE ENTRENOS": modules.Selector_Entrenos_v1.show
}

# Sidebar selection
selection = st.sidebar.radio("Ir a:", list(pages.keys()))

# Call the selected page's function
pages[selection]()

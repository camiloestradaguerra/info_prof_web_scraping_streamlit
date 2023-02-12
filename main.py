
import streamlit as st
import scraper as _scraper

st.title("Búsqueda de datos de profesionales y sus respectivas sanciones")
st.write(""" ## Ingrese el número de cédula
""")
cedula = st.text_input('Cédula', ' ')
st.write('Los datos del profesional son:')

try:
    datos = _scraper._get_data_profesionales(cedula)
    st.write(datos)
except:
    st.write("No existen registros encontrados con el documento ingresado.")
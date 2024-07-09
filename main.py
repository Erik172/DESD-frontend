import streamlit as st
from auth import authenticate
from components import lateral_menu

authenticator = authenticate()

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")
st.image("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png", width=120)

if st.session_state['authentication_status']:
    lateral_menu(authenticator)
    st.subheader("DESD - Detección de Errores en Documentos Escaneados mediante Inteligencia Artificial")

    st.page_link('main.py', label='Home', icon='🏠', disabled=True)
    st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍', disabled=False, help='Pagina auditoria')
    st.page_link('pages/duplicidad.py', label='Duplicidad', icon='2️⃣', disabled=False, help='Pagina donde se encuentra el modulo de Detección de duplicados')
    st.page_link('pages/resultados.py', label='Resultados', icon='📂', help='Pagina donde se encuentra todos los reportes de todos los modelos corridos')

    st.divider()

    st.subheader("Modelos")
    st.write('Modelos disponibles en la pagina auditoria: ')

    models = {
        'nombre': ['RoDe', 'TilDe', 'CuDe'],
        'tarea': ['Deteccion de Rotacion', 'Deteccion de inclinacion en el texto', 'Deteccion de corte de informacion en la pagina'],
        'version': ['2', '2', '1.5'],
    }

    st.table(models)

else:
    st.switch_page('pages/login.py')
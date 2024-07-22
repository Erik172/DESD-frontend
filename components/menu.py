import streamlit as st

def lateral_menu(authenticator, show_logo: bool = True):
    with st.sidebar:
        if show_logo:
            st.image("images/logo.png", width=100)
            # st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png", icon_image='images/logo.png')

        st.caption("Developer Version 2.0")
        st.subheader(f"Hola, {st.session_state['username']} 👋")           
        st.write("Bienvenido a la aplicación DESD.")
        authenticator.logout()

        st.divider()

        st.subheader("Menu")

        st.page_link('main.py', label='Home', icon='🏠', disabled=False)
        st.page_link('pages/auditoria.py', label='Auditoría', icon='🔍', disabled=False, help='Pagina auditoria')
        st.page_link('pages/duplicidad.py', label='Duplicidad', icon='2️⃣', disabled=False, help='Pagina donde se encuentra el modulo de Detección de duplicados')
        st.page_link('pages/folio.py', label='Folio Beta', icon='📄', disabled=False, help='Pagina donde se encuentra el modulo de Detección de folios')
        st.page_link('pages/resultados.py', label='Resultados', icon='📂', help='Pagina donde se encuentra todos los reportes de todos los modelos corridos')
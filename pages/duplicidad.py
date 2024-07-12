from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
from components import lateral_menu, work_status_component
from auth import authenticate
import streamlit as st
import threading
import requests
import time

controller = CookieController(key="dude_controller")
RemoveEmptyElementContainer()

authenticator = authenticate()

if st.session_state['authentication_status']:
    lateral_menu(authenticator) 

    st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

    st.title("DuDe (Duplicate Detection) Detección de duplicados 2️⃣")
    st.caption("V2.0 - Estable, con alta precisión 📊")

    uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)

    def process_uploaded_images(uploaded_file):
        random_id = requests.get(f"{st.secrets['api_address']}/v2/generate_id").json()["random_id"]
        controller.set("dude_result_id", random_id)
        st.success(f"Identificador de resultados: **{random_id}**", icon="📄")
        st.info(f"Procesando **{len(uploaded_file)}** archivos... 🔄")
            
        url = f"{st.secrets['api_address']}/v2/dude"
        files = [('files', (file.name, file, file.type)) for file in uploaded_file]
        threading.Thread(target=requests.post, args=(url,), kwargs={"files": files, "data": {"result_id": str(random_id)}}).start()
        st.caption("Procesando archivos...")
        time.sleep(3)


    if st.button("Buscar Duplicados", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
        if uploaded_file:
            process_uploaded_images(uploaded_file)

    work_status_component(controller, 'dude_result_id')

else:
    st.error("Debes iniciar sesión para acceder a esta página 🚫")
    if st.button("Iniciar sesión", help="Iniciar sesión para acceder a la página de auditoría", use_container_width=True):
        st.switch_page('pages/login.py')
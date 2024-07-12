from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
from components import lateral_menu, work_status_component
from auth import authenticate
import streamlit as st
import requests
import threading
import time 

controller = CookieController(key="auditoria_controller")
RemoveEmptyElementContainer()

authenticator = authenticate()

# st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

if st.session_state['authentication_status']:
    lateral_menu(authenticator)

    st.title("Auditoría 🔍")
    st.caption("V2.0 - 80% mas rapido 🚀")

    models = st.multiselect(
        "Selecciona los modelos a utilizar",
        ["Inclinacion", "Rotacion", "Corte_informacion"],
        ["Rotacion"]
    )

    uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)

    def process_files(upload_files):
        global models

        models = [model.lower() for model in models]

        if len(upload_files) == 0:
            st.warning("Debes subir al menos un archivo", icon="⚠️")
            return
        
        random_id = requests.get(f"{st.secrets['api_address']}/v2/generate_id").json()["random_id"]
        controller.set('desd_result_id', random_id)
        st.success(f"Identificador para guardar los resultados: **{random_id}**")
        st.info(f"Total de archivos a procesar: **{len(upload_files)}**")
        st.info(f"Modelos seleccionados: **{', '.join(models)}**")

        url = f"{st.secrets['api_address']}/v2/desd"
        files = [('files', (file.name, file, file.type)) for file in upload_files]
        threading.Thread(target=requests.post, args=(url,), kwargs={"files": files, "data": {"models": models, "result_id": str(random_id)}}).start()
        st.caption("Procesando archivos...")
        time.sleep(5)

    if st.button("Procesar", help="Procesar las imágenes y archivos PDF subidos", use_container_width=True):
        if uploaded_file:
            with st.sidebar:
                download = st.empty()
            process_files(uploaded_file)

    work_status_component(controller, 'desd_result_id')
else:
    st.error("Debes iniciar sesión para acceder a esta página 🚫")
    if st.button("Iniciar sesión", help="Iniciar sesión para acceder a la página de auditoría", use_container_width=True):
        st.switch_page('pages/login.py')
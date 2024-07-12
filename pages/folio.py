from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
from components import lateral_menu, work_status_component
from auth import authenticate
import streamlit as st
import threading
import requests
import time

controller = CookieController(key="folio_controller")
RemoveEmptyElementContainer()

authenticate = authenticate()
lateral_menu(authenticator=authenticate)

st.title("Folio")
st.caption("V0.1 - En desarrollo 🚧")

uploaded_file = st.file_uploader("Subir Archivos", type=["pdf"], accept_multiple_files=True)

def process_files(upload_files: list) -> None:
    random_id = requests.get(f"{st.secrets['api_address']}/v2/generate_id").json()["random_id"]
    controller.set('folio_result_id', random_id)
    st.success(f"Identificador de resultados: **{random_id}**", icon="📄")

    url = f"{st.secrets['api_address']}/v1/folio"
    files = [('files', (file.name, file, file.type)) for file in upload_files]
    threading.Thread(target=requests.post, args=(url,), kwargs={"files": files, "data": {"result_id": str(random_id)}}).start()
    st.caption("Procesando archivos...")
    time.sleep(5)

if st.button("Procesar", help="Procesar los archivos PDF subidos", use_container_width=True):
    if uploaded_file:
        process_files(uploaded_file)

work_status_component(controller, 'folio_result_id')
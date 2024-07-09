from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
from auth import authenticate
from components import lateral_menu
import streamlit as st
import requests
import threading
import time 

controller = CookieController(key="auditoria_controller")
RemoveEmptyElementContainer()

authenticator = authenticate()

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")


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

    def work_status(result_id):
        url = f"{st.secrets['api_address']}/v2/status/{result_id}"
        response = requests.get(url)
        return response

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

    if controller.get('desd_result_id') != None:
        st.subheader(f"Estado de ({controller.get('desd_result_id')})")
        porcentaje = st.empty()
        files_process = st.empty()
        data = st.empty()
        error_count = 0
        download_partial = st.empty()
        while True:
            status = work_status(controller.get('desd_result_id'))
            if status.status_code == 200:
                status = status.json()
                if status["status"] == "in_progress":
                    porcentaje.progress(float(status["percentage"]) / 100.0, f'{round(status["percentage"], 1)}% - {status["files_processed"]} / {status["total_files"]} completados')
                    files_process.info(f"Procesando archivos...   {status['files_processed']} de {status['total_files']} completados")
                else:
                    download_partial.empty()
                    porcentaje.progress(1.0, "100% completado")
                    files_process.success("Procesamiento completado")
                    break
            elif status.status_code == 404:
                if error_count == 2:
                    files_process.error("Demasiados intentos fallidos... abortando")
                    break
                
                error_count += 1
                files_process.error(f"No se encontraron resultados previos... reintentando en 5 segundos, intento {error_count}")	
                time.sleep(5)

            else:
                files_process.error("Error al obtener los resultados")
                break
            
            # data.write(status)
        try:
            st.info(f'Total de archivos procesados: {status["total_files"]}')

            if st.download_button(
                label="Descargar resultados completos en CSV",
                data=requests.get(f"{st.secrets['api_address']}/v2/export/{controller.get('desd_result_id')}").content,
                file_name=f"{controller.get('desd_result_id')}.csv",
                mime="text/csv",
                help="Descargar los resultados completos en formato CSV",
                use_container_width=True
            ):
                st.toast("Descargando resultados...", icon="📥")
                requests.delete(f"{st.secrets['api_address']}/v2/export/{controller.get('desd_result_id')}")
        except:
            pass

        if st.button("Limpiar", help="Eliminar resultados previos", use_container_width=True):
            controller.remove('desd_result_id')
            st.rerun()

    else:
        st.caption("No hay resultados previos para mostrar")
else:
    st.error("Debes iniciar sesión para acceder a esta página 🚫")
    if st.button("Iniciar sesión", help="Iniciar sesión para acceder a la página de auditoría", use_container_width=True):
        st.switch_page('pages/login.py')
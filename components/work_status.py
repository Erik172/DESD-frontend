from streamlit_cookies_controller import CookieController
import streamlit as st
import requests
import time

def work_status(result_id: str) -> requests.models.Response:
    url = f"{st.secrets['api_address']}/v2/status/{result_id}"
    response = requests.get(url)
    return response

def work_status_component(controller: CookieController, cookie_name: str):
    if controller.get(cookie_name) != None:
        st.subheader(f"Estado de ({controller.get(cookie_name)})")
        porcentaje = st.empty()
        files_process = st.empty()
        error_count = 0
        download_partial = st.empty()
        while True:
            status = work_status(controller.get(cookie_name))
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

                st.write(status["summary"])

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
        try:
            st.info(f'Total de archivos procesados: {status["total_files"]}')

            if st.download_button(
                label="Descargar resultados completos en CSV",
                data=requests.get(f"{st.secrets['api_address']}/v2/export/{controller.get(cookie_name)}").content,
                file_name=f"{controller.get(cookie_name)}.csv",
                mime="text/csv",
                help="Descargar los resultados completos en formato CSV",
                use_container_width=True
            ):
                st.toast("Descargando resultados...", icon="📥")
                requests.delete(f"{st.secrets['api_address']}/v2/export/{controller.get(cookie_name)}")
        except:
            pass

        if st.button("Limpiar", help="Eliminar resultados previos", use_container_width=True):
            controller.remove(cookie_name)
            st.rerun()

    else:
        st.caption("No hay resultados previos para mostrar")
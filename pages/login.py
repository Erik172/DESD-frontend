import streamlit as st
from auth import authenticate

authenticator = authenticate()

# st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")
st.image("images/logo.png", width=140)

# st.info("**Username:** tester    **Password:** tester")
authenticator.login()
if st.session_state["authentication_status"] is False:
    st.error('Username/password es incorrecto')
if st.session_state["authentication_status"]:
    st.toast("Bienvenido")
    st.switch_page('main.py')

create_account, forgot_password = st.columns(2)

if create_account.button("Crear cuenta", use_container_width=True, disabled=False):
    st.switch_page('pages/create_account.py')
if forgot_password.button("Olvidaste tu contraseña", use_container_width=True):
    pass
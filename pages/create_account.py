import requests
import streamlit as st
from auth import authenticate

authenticator = authenticate()

if not st.session_state['authentication_status']:
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user, password = authenticator.register_user(pre_authorization=True)
        if st.button('Iniciar sesión', use_container_width=True):
            st.switch_page('pages/login.py')
        if email_of_registered_user:
            print(f'Email: {email_of_registered_user}')
            print(f'Username: {username_of_registered_user}')
            print(f'Name: {name_of_registered_user}')
            print(f'Password: {password}')
            st.toast('User registered successfully')
            st.switch_page('pages/login.py')
    except Exception as e:
        st.error(e)
else:
    st.error('You are already logged in')
    st.switch_page('main.py')
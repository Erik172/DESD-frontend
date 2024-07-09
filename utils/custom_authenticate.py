from streamlit_authenticator.utilities.exceptions import DeprecationError
from streamlit_authenticator.utilities.validator import Validator
import streamlit_authenticator as stauth
from typing import Optional
import streamlit as st

class Authenticate(stauth.Authenticate):
    def __init__(self, credentials: dict, cookie_name: str, cookie_key: str,
                 cookie_expiry_days: float = 30.0, pre_authorized: Optional[list] = None,
                 validator: Optional[Validator] = None):
        # Llamar al método __init__ de la clase base
        super().__init__(credentials, cookie_name, cookie_key, cookie_expiry_days, pre_authorized, validator)
        
        # Reemplazar el manejador de autenticación con el manejador modificado
        self.authentication_handler = AuthenticationHandler(credentials, pre_authorized, validator)

    def register_user(self, location: str='main', pre_authorization: bool=True,
                  domains: Optional[list]=None, fields: dict=None,
                  clear_on_submit: bool=False) -> tuple:
        if fields is None:
            fields = {'Form name': 'Register user', 'Email': 'Email', 'Username': 'Username',
                    'Password': 'Password', 'Repeat password': 'Repeat password',
                    'Register': 'Register'}
        if pre_authorization:
            if not self.authentication_handler.pre_authorized:
                raise ValueError("pre-authorization argument must not be None")
        if location not in ['main', 'sidebar']:
            raise DeprecationError("""Likely deprecation error, the 'form_name' parameter has
                                been replaced with the 'fields' parameter. For further
                                information please refer to 
                                https://github.com/mkhorasani/Streamlit-Authenticator/tree/main?tab=readme-ov-file#authenticateregister_user""")
        if location == 'main':
            register_user_form = st.form('Register user', clear_on_submit=clear_on_submit)
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        register_user_form.subheader('Register User' if 'Form name' not in fields
                                    else fields['Form name'])
        new_name = register_user_form.text_input('Name' if 'Name' not in fields
                                                else fields['Name'])
        new_email = register_user_form.text_input('Email' if 'Email' not in fields
                                                else fields['Email'])
        new_username = register_user_form.text_input('Username' if 'Username' not in fields
                                                    else fields['Username']).lower()
        new_password = register_user_form.text_input('Password' if 'Password' not in fields
                                                    else fields['Password'], type='password')
        new_password_repeat = register_user_form.text_input('Repeat password'
                                                            if 'Repeat password' not in fields
                                                            else fields['Repeat password'],
                                                            type='password')
        if register_user_form.form_submit_button('Register' if 'Register' not in fields
                                                else fields['Register'],
                                                use_container_width=True):
            # Asegúrate de manejar los cuatro valores retornados por register_user
            email, username, name, password = self.authentication_handler.register_user(new_password, new_password_repeat,
                                                                                        pre_authorization, new_username,
                                                                                        new_name, new_email, domains)
            return email, username, name, password
        return None, None, None, None  # Asegúrate de retornar cuatro valores aquí también


# Asegúrate de tener la definición de AuthenticationHandler previamente
class AuthenticationHandler(stauth.authenticate.AuthenticationHandler):
    def register_user(self, new_password: str, new_password_repeat: str, pre_authorization: bool,
                      new_username: str, new_name: str, new_email: str,
                      domains) -> tuple:
        # Llama al método original de la clase base
        base_result = super().register_user(new_password, new_password_repeat, pre_authorization, new_username, new_name, new_email, domains)

        # Agrega new_password al resultado y devuélvelo
        return base_result + (new_password,)
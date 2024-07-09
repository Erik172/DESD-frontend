import yaml
import streamlit as st
from yaml.loader import SafeLoader
from utils.custom_authenticate import Authenticate

with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

def authenticate():
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    return authenticator
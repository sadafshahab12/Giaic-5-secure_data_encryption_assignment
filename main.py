# Users store data with a unique passkey.
# Users decrypt data by providing the correct passkey.
# Multiple failed attempts result in a forced reauthorization (login page).
# The system operates entirely in memory without external databases.
import streamlit as st
import hashlib
import json
import time
import base64
from cryptography.fernet import Fernet

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0  # it track how may times password enter
if "stored_data" not in st.session_state:
    
# generate a key

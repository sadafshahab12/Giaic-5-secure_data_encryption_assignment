# Users store data with a unique passkey.
# Users decrypt data by providing the correct passkey.
# Multiple failed attempts result in a forced reauthorization (login page).
# The system operates entirely in memory without external databases.
import streamlit as st
import hashlib

from cryptography.fernet import Fernet

# generate a key 
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# in memory data store 
stored_data = {}
failed_attempts = 0

# function to hash pass key 
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

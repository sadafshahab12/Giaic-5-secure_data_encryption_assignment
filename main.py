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

# initialize session state variables if then don't exist
if (
    "failed_attempts" not in st.session_state
):  # “If the value for failed_attempts hasn’t been saved yet in the session, create it and set it to 0.”
    st.session_state.failed_attempts = 0  # it track how may times password enter
if (
    "stored_data" not in st.session_state
):  # If there’s no stored_data saved in the session yet, create it and make it an empty dictionary {}.
    st.session_state.stored_data = {}

if (
    "current_page" not in st.session_state
):  # “If we haven’t saved a page name in the session yet, set it to 'Home' by default.”
    st.session_state.current_page = "Home"
if (
    "last_attempt" not in st.session_state
):  # If there’s no last_attempt saved in the session yet, set it to 0.”
    st.session_state.last_attempt = 0


# function that generate hash pass key
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()


# function generate key from passkey
def generate_key_from_passkey(passkey):
    hashed_key = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed_key[:32])


def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()


def decrypt_data(encrypted_text, passkey, data_id):
    try:
        # check if passkey matches
        hashed_passkey = hash_passkey(passkey)
        if (
            data_id in st.session_state.stored_data
            and st.session_state.stored_data[data_id]["passkey"] == hashed_passkey
        ):
            # if pass key matches decrypt the data
            key = generate_key_from_passkey(passkey)
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_text.encode()).decode()
            st.session_state.failed_attemptps = 0
            return decrypted_data
        else:
            # Increment fail attempt increase
            st.session_state.failed_attempts += 1
            st.session_state.last_attempt = time.time()
            return None
    except Exception as e:
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt = time.time()
        return None


# generate unique id for data
def generate_data_id():
    import uuid

    return str(uuid.uuid4())


# reset failed attempts
def reset_failed_attempts():
    st.session_state.failed_attempts = 0


def change_page(page):
    st.session_state.current_page = page


st.title("Secure Data Encryption System")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox(
    "Navigation", menu, index=menu.index(st.session_state.current_page)
)
# update page based on current selection
st.session_state.current_page = choice

if st.session_state.failed_attempts >= 3:
    st.session_state.current_page = "Login"
    st.warning("Too many failed attempts! Reauthorization required")

# display current page
if st.session_state.current_page == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write(
        "Use this app to **securely store and retrieve data** using unique passkeys."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Store new data", use_container_width=True):
            change_page("Store Data")
    with col2:
        if st.button("Retrieve Data ", use_container_width=True):
            change_page("Retrieve Data")

    st.info(
        f"Currently storing {len(st.session_state.stored_data)} encrypted data entries"
    )

elif st.session_state.current_page == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data: ")
    passkey = st.text_input("Enter passkey: ", type="password")
    confirm_passkey = st.text_input("Enter Confirm passkey: ", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey and confirm_passkey:
            if passkey != confirm_passkey:
                st.error("Passkeys do not match!")
            else:
                # generate a unique id for this data
                data_id = generate_data_id()
                # hash the passkey
                hashed_passkey = hash_passkey(passkey)
                # encrypt the data
                encrypted_text = encrypt_data(user_data, passkey)

                # store
                st.session_state.stored_data[data_id] = {
                    "encrypted_text": encrypted_text,
                    "passkey": hashed_passkey,
                }
                st.success("Data stored securely!")
                # display id for data retrievel
                st.code(data_id, language="text")
                st.info("Save this Data ID! You will need it to retrieve your data.")
        else:
            st.error("All fields are required!")

elif st.session_state.current_page == "Retrieve Data":
    st.subheader("Retrieve Data Securely")

    attempts_remaining = 3 - st.session_state.failed_attempts
    st.info(f"Attempts Remaining: {attempts_remaining}")

    data_id = st.text_input("Enter Data ID:")
    passkey = st.text_input("Enter passkey:", type="password")

    if st.button("Decrypt"):
        if data_id and passkey:
            if data_id in st.session_state.stored_data:
                encrypted_text = st.session_state.stored_data[data_id]["encrypted_text"]
                decrypted_text = decrypt_data(encrypted_text, passkey, data_id)

                if decrypted_text:
                    st.success("Decryption successful!")
                    st.markdown("### Your Decrypted Data:")
                    st.code(decrypted_text, language="text")
                else:
                    st.error(
                        f"Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}"
                    )
            else:
                st.error("Data ID not found!")
            if st.session_state.failed_attempts >= 3:
                st.warning("Too many failed attempts! Redirecting to Login Page.")
                st.session_state.current_page = "Login"
                st.rerun()
    else:
        st.error("Both fields are required!")

elif st.session_state.current_page == "Login":
    st.subheader("Reauthorization Required")
    # timout adding
    if (
        time.time() - st.session_state.last_attempt < 10
        and st.session_state.failed_attempts >= 3
    ):
        remaining_time = int(10 - (time.time() - st.session_state.last_attempt))
        st.warning(f"Please wait! {remaining_time}  seconds before trying!")
    else:
        login_pass = st.text_input("Enter Master Password:", type="password")
        if st.button("Login"):
            if login_pass == "admin123":
                reset_failed_attempts()
                st.success("✅ Reauthorized successfully!")
                st.session_state.current_page = "Home"
                st.rerun()  # experimental_rerun()
            else:
                st.error("Incorrect password!")
st.markdown("-----")
st.markdown("Secure Data Encryption System | Educational Project")

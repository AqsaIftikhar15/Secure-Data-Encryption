import streamlit as st
import hashlib
from cryptography.fernet import Fernet

st.set_page_config(
    page_icon ="🗝️",
    page_title="Secure Data Encryption",
    layout="centered",
)

st.title("🔒 Secure Data Encryption System")

# Session state init
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False

cipher = Fernet(st.session_state.fernet_key)

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()



if st.session_state.failed_attempts >= 3 or st.session_state.locked:
    st.session_state.locked = True
    st.warning("🚫 Too many failed attempts. Please enter master password to unlock (letmein).")
    master_input = st.text_input("Enter Master Password", type="password")

    if st.button("Unlock"):
        if master_input == "letmein": 
            st.success("🔓 Access granted!")
            st.session_state.failed_attempts = 0
            st.session_state.locked = False
        else:
            st.error("❌ Incorrect master password.")
    st.stop()  # 🛑 Stop here, don’t show main app



st.subheader("🔐 Encrypt & Store Data")

data = st.text_area("Enter the data you want to encrypt:")
pass_key = st.text_input("Enter a password", type="password")

if st.button("Store securely"):
    if data and pass_key:
        encrypted = cipher.encrypt(data.encode()).decode()
        hashed = hash_password(pass_key)

        st.session_state.stored_data[encrypted] = {
            "encrypted_data": encrypted,
            "key": hashed
        }
        st.success("✅ Data stored securely!")
        st.write("📦 Encrypted data:", encrypted)
    else:
        st.error("❗ Both fields are required.")

# Retrieve
st.subheader("🔓 Retrieve Data")

retrieve_key = st.text_input("Enter password to retrieve data", type="password")
if st.button("Retrieve Data"):
    if retrieve_key:
        hashed_input = hash_password(retrieve_key)
        found = False

        for encrypted_text, record in st.session_state.stored_data.items():
            if record["key"] == hashed_input:
                decrypted = cipher.decrypt(record["encrypted_data"].encode()).decode()
                st.success(f"✅ Decrypted Data: {decrypted}")
                found = True
                break

        if not found:
            st.session_state.failed_attempts += 1
            st.error("❗ Incorrect password.")
            st.warning(f"❗ Attempts: {st.session_state.failed_attempts}")
    else:
        st.error("❗ Enter a password.")

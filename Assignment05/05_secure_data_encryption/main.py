import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import json
import os
import time
from datetime import datetime, timedelta

# Constants
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 300  # 5 minutes in seconds
DATA_FILE = "encrypted_data.json"
MASTER_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()  # For demo purposes only

# Generate or load encryption key
def get_encryption_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

KEY = get_encryption_key()
cipher = Fernet(KEY)
# After the encryption key setup, add:
USERS_FILE = "users.json"  # File to store user credentials

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}  # Empty dict if no file exists

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

users_db = load_users()  # Load existing users




# Initialize session state
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'locked_out' not in st.session_state:
    st.session_state.locked_out = False
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = None

# Load or initialize stored data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

stored_data = load_data()

# Security functions
def hash_passkey(passkey, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    # Using PBKDF2 for better security
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        passkey.encode(),
        salt.encode(),
        100000  # Number of iterations
    )
    return f"{salt}${hashed.hex()}"

def verify_passkey(passkey, hashed_passkey):
    if not hashed_passkey or '$' not in hashed_passkey:
        return False
    salt, stored_hash = hashed_passkey.split('$')
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        passkey.encode(),
        salt.encode(),
        100000
    ).hex()
    return new_hash == stored_hash

# Data encryption/decryption
def encrypt_data(text, passkey):
    encrypted_text = cipher.encrypt(text.encode()).decode()
    hashed_passkey = hash_passkey(passkey)
    return encrypted_text, hashed_passkey

def decrypt_data(encrypted_text, passkey):
    if st.session_state.locked_out:
        remaining_time = (st.session_state.lockout_time + timedelta(seconds=LOCKOUT_TIME) - datetime.now()).seconds
        st.error(f"🔒 Account locked. Please try again in {remaining_time} seconds.")
        return None

    for key, value in stored_data.items():
        if value["encrypted_text"] == encrypted_text and verify_passkey(passkey, value["passkey"]):
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    
    st.session_state.failed_attempts += 1
    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
        st.session_state.locked_out = True
        st.session_state.lockout_time = datetime.now()
        st.error("🔒 Too many failed attempts! Account locked for 5 minutes.")
    else:
        st.error(f"❌ Incorrect passkey! Attempts remaining: {MAX_ATTEMPTS - st.session_state.failed_attempts}")
    return None





# Streamlit UI
st.set_page_config(page_title="Secure Data Encryption System", page_icon="🔒")

# Navigation
# Change the menu options to:
menu = ["Home", "Register", "Login", "Store Data", "Retrieve Data"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.title("🏠 Secure Data Encryption System")
    st.write("""
    Welcome to the Secure Data Encryption System!
    
    This application allows you to:
    - 🔐 Store sensitive data securely using encryption
    - 🔑 Retrieve your data using a unique passkey
    - 🛡️ Benefit from multiple security layers including PBKDF2 hashing and account lockout
    
    Use the sidebar to navigate to different sections.
    """)
elif choice == "Register":
    st.title("📝 User Registration")
    new_username = st.text_input("Choose a Username:")
    new_password = st.text_input("Choose a Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    if st.button("Register"):
        if not new_username or not new_password:
            st.error("❌ Username and password are required!")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif new_username in users_db:
            st.error("❌ Username already exists!")
        else:
            hashed_password = hash_passkey(new_password)
            users_db[new_username] = {"password": hashed_password}
            save_users(users_db)
            st.success("✅ Registration successful! Please login.")

elif choice == "Login":
    st.title("🔑 Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("❌ Username and password are required!")
        elif username not in users_db:
            st.error("❌ User does not exist!")
        elif not verify_passkey(password, users_db[username]["password"]):
            st.error("❌ Incorrect password!")
        else:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username}!")
            time.sleep(1)
            st.rerun()


elif choice == "Store Data":
    if not st.session_state.get("logged_in"):
        st.warning("⚠️ Please login first!")
        st.stop()
    
    st.title("📂 Store Data Securely")
    st.write(f"Logged in as: {st.session_state.username}")
    
    user_data = st.text_area("Data to Encrypt:", height=150)
    passkey = st.text_input("Create a Passkey:", type="password")
    passkey_confirm = st.text_input("Confirm Passkey:", type="password")
    
    if st.button("Encrypt & Save"):
        if not user_data or not passkey:
            st.error("⚠️ Please enter both data and passkey!")
        elif passkey != passkey_confirm:
            st.error("⚠️ Passkeys do not match!")
        else:
            encrypted_text, hashed_passkey = encrypt_data(user_data, passkey)
            data_id = f"{st.session_state.username}_data_{encrypted_text[:8]}"
            
            # Initialize user's data storage if not exists
            if st.session_state.username not in stored_data:
                stored_data[st.session_state.username] = {}
                
            stored_data[st.session_state.username][data_id] = {
                "encrypted_text": encrypted_text,
                "passkey": hashed_passkey,
                "timestamp": str(datetime.now())
            }
            
            save_data(stored_data)
            st.success("✅ Data stored securely!")
            st.code(f"Data ID: {data_id}\nEncrypted: {encrypted_text[:50]}...")

elif choice == "Retrieve Data":
    if not st.session_state.get("logged_in"):
        st.warning("⚠️ Please login first!")
        st.stop()
    
    st.title("🔍 Retrieve Your Data")
    st.write(f"Logged in as: {st.session_state.username}")
    
    # Check if user has any data
    if st.session_state.username not in stored_data or not stored_data[st.session_state.username]:
        st.warning("You haven't stored any data yet!")
        st.stop()
    
    # Get user's specific data
    user_data = stored_data[st.session_state.username]
    
    # Create list of data items with IDs and timestamps for display
    data_options = [
        f"{data_id} (Created: {user_data[data_id]['timestamp']})" 
        for data_id in user_data
    ]
    
    selected_data = st.selectbox("Select Data to Retrieve", [""] + data_options)
    
    if selected_data:
        # Extract the actual data_id from the displayed string
        data_id = selected_data.split(" (Created:")[0]
        encrypted_text = user_data[data_id]["encrypted_text"]
        
        st.text_area("Encrypted Data", encrypted_text, height=150, disabled=True)
        passkey = st.text_input("Enter Passkey:", type="password")
        
        if st.button("Decrypt"):
            if not passkey:
                st.error("Please enter a passkey!")
            else:
                # Modified decrypt_data call for user-specific data
                decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
                if verify_passkey(passkey, user_data[data_id]["passkey"]):
                    st.session_state.failed_attempts = 0
                    st.success("✅ Decryption successful!")
                    st.text_area("Decrypted Data", decrypted_text, height=200)
                else:
                    st.session_state.failed_attempts += 1
                    remaining_attempts = MAX_ATTEMPTS - st.session_state.failed_attempts
                    st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining_attempts}")
                    
                    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
                        st.session_state.locked_out = True
                        st.session_state.lockout_time = datetime.now()
                        st.error("🔒 Too many failed attempts! Account locked for 5 minutes.")
                        time.sleep(2)
                        st.rerun()
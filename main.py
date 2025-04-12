import streamlit as st
from backend import auth, encryption, emailer
from backend.db import db
import random, string, re
import time

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email)

def is_strong_password(pw):
    return (
        len(pw) >= 8 and
        re.search(r"[A-Z]", pw) and
        re.search(r"[a-z]", pw) and
        re.search(r"[0-9]", pw) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw)
    )

st.set_page_config("SecureBox - Secure Data Encryption System", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

st.markdown("""
<style>
html, body, .stApp {
    background-color: #FFFFFF;
    color: #000000;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    color: #1F6FEB;
}

.main-header {
    font-size: 36px;
    font-weight: bold;
    color: #1F6FEB;
    margin-bottom: 20px;
    text-align: center;
}

   h1 {
        font-size: 48px;
    }

@media screen and (max-width: 768px) {
    .main-header {
        font-size: 28px;
    }
    h1 {
        font-size: 30px;
    }
}

@media screen and (max-width: 480px) {
    .main-header {
        font-size: 20px;
    }
      h1 {
        font-size: 20px;
    }
}

.stTextInput > div > input,
.stTextArea textarea,
.stFileUploader input[type="file"],
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #F0F0F0 !important;
    color: #000000 !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 8px;
    padding: 8px;
}

.stButton > button {
    background-color: #1F6FEB !important;
    color: white !important;
    border-radius: 8px;
    padding: 10px 24px;
    border: none;
}

.stButton > button:hover {
    background-color: #1158C7 !important;
    transform: scale(1.05);
}

.stDownloadButton > button {
    background-color: #2DA44E !important;
    color: white !important;
    border-radius: 6px;
    padding: 8px 20px;
}

.stDownloadButton > button:hover {
    background-color: #218739 !important;
}

section[data-testid="stSidebar"] {
    background-color: #F7F7F7 !important;
    color: #000000 !important;
}

hr {
    border-top: 1px solid #DDDDDD;
}

.stAlert {
    background-color: #FAFAFA !important;
    border-left: 5px solid #1F6FEB !important;
    color: #000000 !important;
}

.markdown-text-container, .stMarkdown {
    color: #000000 !important;
}

a {
    color: #1F6FEB !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title(" SecureBox Menu")
menu = st.sidebar.radio("Navigation", ["Home", "Login", "Signup", "Encrypt", "Decrypt", "Logout"])

# ==== Home ==== 
if menu == "Home":
    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h1 style='color: #0A0A23;'> Welcome to the Secure Data Encryption System</h1>
            <h2 style='color: #1F6FEB; font-size: 38px; margin-top: 20px;'> SecureBox</h2>
            <h3 style='color: #444;'>Protect & Share Your Data with Confidence</h3>
            <p style='color: #666; font-size: 18px; margin-top: 20px;'>
                Use SecureBox to encrypt messages and files, send passkeys, and decrypt safely.<br>
                All your data remains confidential and accessible only by the intended recipient.
            </p>
        </div>
        <hr style='margin: 30px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("""
        ###  What You Can Do:
        -  Securely encrypt and share messages & files  
        -  Send auto-generated passkeys via email  
        -  Decrypt files and messages securely  

        > Use the sidebar to **Login**, **Signup**, or **Start Encrypting** now!
        
        ---

        ###  Where & How Can You Use SecureBox?

        -  **Teachers**: Share exam papers, feedback, or grades privately with students  
        -  **Students**: Submit assignments, research, or important files securely  
        -  **Doctors**: Send encrypted medical reports or prescriptions to patients  
        -  **Lawyers**: Share confidential legal case files with clients  
        -  **Professionals**: Protect business documents, contracts, or reports  
        -  **Families & Friends**: Exchange personal letters, passwords, or memories safely  
        
        ---

        ###  Only Intended Receiver Can Decrypt

        - Encrypted data is locked to the **receiver's email**  
        - The recipient **must login with that same email** to decrypt the message or file  
        - Adds an extra layer of **account-bound security**  
        - A **passkey is sent via email** — without it, even having the file is useless  

        > Your data. Your control. Your security.
    """)

# ==== Signup ==== 
if menu == "Signup":
    st.title("Create a New Account")
    email = st.text_input(" Email Address")
    pw = st.text_input(" Password", type="password")
    if st.button("Create Account"):
        try:
            if not is_valid_email(email):
                st.error(" Invalid email format. Please try again.")
            elif not is_strong_password(pw):
                st.error(" Password is weak. Ensure it has at least 8 characters, uppercase, lowercase, digits, and a symbol.")
            else:
                result = auth.signup(email, pw)
                if result == "signup_success":
                    st.success(" Your account has been created! Please log in.")
                elif result == "email_already_exists":
                    st.error(" This email is already registered.")
                else:
                    st.error(" Something went wrong. Please try again.")
        except Exception as e:
            st.error(f" Error: {str(e)}")

# ==== Login ==== 
if menu == "Login":
    st.title("Login to Your Account")
    email = st.text_input(" Email Address")
    pw = st.text_input(" Password", type="password")
    if st.button("Login"):
        try:
            result = auth.login(email, pw)
            if result == "login_success":
                st.session_state.logged_in = True
                st.session_state.user = email
                st.success(" You have logged in successfully!")
            elif result == "email_not_found":
                st.error(" No account found with this email.")
            elif result == "wrong_password":
                st.error(" Incorrect password. Please try again.")
            else:
                st.error(" Login failed. Please check your credentials.")
        except Exception as e:
            st.error(f" Error: {str(e)}")

# ==== Encrypt ==== 
if menu == "Encrypt" and st.session_state.logged_in:
    st.title("Encrypt & Send Secure Data")
    receiver = st.text_input(" Receiver's Email Address")
    message = st.text_area(" Your Secret Message")
    uploaded = st.file_uploader(" Upload a File")

    if st.button(" Encrypt & Send"):
        try:
            if uploaded and message and receiver:
                passkey = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                file_bytes = uploaded.getvalue()
                enc_file, enc_msg = encryption.encrypt_file_message(file_bytes, message, passkey)

                if not enc_file or not enc_msg:
                    st.error(" Encryption failed. Please try again.")
                else:
                    db.files.insert_one({
                        "from": st.session_state.user,
                        "to": receiver,
                        "file": enc_file,
                        "msg": enc_msg,
                        "passkey": passkey,
                        "attempts": 0,
                        "timestamp": time.time()
                    })
                    emailer.send_email(receiver, passkey)
                    st.success(" The message and file have been encrypted and sent successfully!")
            else:
                st.error(" Please fill all required fields to proceed.")
        except Exception as e:
            st.error(f" Error: {str(e)}")

elif menu == "Encrypt" and not st.session_state.logged_in:
    st.warning(" Please log in to encrypt and send files.")

# ==== Decrypt ==== 
if menu == "Decrypt" and st.session_state.logged_in:
    st.title("Decrypt Your Secure Data")
    passkey = st.text_input(" Enter your passkey")
    if st.button(" Decrypt"):
        try:
            record = db.files.find_one({"to": st.session_state.user, "passkey": passkey})
            if record:
                if record["attempts"] >= 3:
                    st.warning(" Too many failed attempts. Try again later.")
                else:
                    file, msg = encryption.decrypt_file_message(record["file"], record["msg"], passkey)
                    if not file or msg == "invalid_passkey_or_data":
                        db.files.update_one({"_id": record["_id"]}, {"$inc": {"attempts": 1}})
                        st.error(" Incorrect passkey. Please verify your credentials.")
                    elif "decryption_error" in msg:
                        st.error(f" Decryption error: {msg}")
                    else:
                        st.success(f" Message: {msg}")
                        st.download_button(" Download the Decrypted File", file, file_name="secret_file")
            else:
                st.error(" No record found for the given passkey.")
        except Exception as e:
            st.error(f" Error: {str(e)}")

elif menu == "Decrypt" and not st.session_state.logged_in:
    st.warning(" Please log in to decrypt files.")

# ==== Logout ====
if menu == "Logout":
    if st.session_state.logged_in:
        st.title("Logout")
        st.markdown("### Are you sure you want to log out?")
        if st.button("Yes, Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.success("You have been logged out successfully.")
    else:
        st.warning("You are not logged in.")



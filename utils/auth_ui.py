import streamlit as st
import json
import os

USER_FILE = "users.json"

# -----------------------
# LOAD USERS
# -----------------------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

# -----------------------
# SAVE USERS
# -----------------------
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# -----------------------
# AUTH PAGE UI
# -----------------------
def auth_page():

    users = load_users()

    st.markdown("## 👗 GlamTrend Login")

    mode = st.radio("Select", ["Login", "Signup"], horizontal=True)

    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # -----------------------
    # LOGIN
    # -----------------------
    if mode == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:

                st.session_state["logged_in"] = True
                st.session_state["user"] = username

                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

    # -----------------------
    # SIGNUP
    # -----------------------
    else:
        if st.button("Create Account"):
            if username in users:
                st.warning("User already exists")
            else:
                users[username] = password
                save_users(users)
                st.success("Account created successfully 🎉")
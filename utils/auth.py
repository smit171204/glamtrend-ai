# import streamlit as st
# import json
# import os

# USER_FILE = "users.json"

# # -----------------------
# # LOAD / SAVE
# # -----------------------
# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r") as f:
#         return json.load(f)

# def save_users(users):
#     with open(USER_FILE, "w") as f:
#         json.dump(users, f)

# # -----------------------
# # AUTH SYSTEM (FINAL)
# # -----------------------
# def auth_ui():

#     menu = st.sidebar.radio("Account", ["Login", "Signup"])

#     users = load_users()

#     # # ---------------- LOGIN ----------------
#     # if menu == "Login":
#     #     with st.sidebar.form("login_form"):   # ✅ FORM FIX
#     #         st.subheader("🔐 Login")

#     #         username = st.text_input("Username")
#     #         password = st.text_input("Password", type="password")

#     #         submit = st.form_submit_button("Login")

#     #         if submit:
#     #             if username in users and users[username] == password:
#     #                 st.session_state["logged_in"] = True
#     #                 st.sidebar.success("Login successful")
#     #             else:
#     #                 st.sidebar.error("Invalid credentials")

#     # # ---------------- SIGNUP ----------------
#     # else:
#     #     with st.sidebar.form("signup_form"):  # ✅ FORM FIX
#     #         st.subheader("📝 Signup")

#     #         new_user = st.text_input("New Username")
#     #         new_pass = st.text_input("New Password", type="password")

#     #         submit = st.form_submit_button("Create Account")

#     #         if submit:
#     #             if new_user in users:
#     #                 st.sidebar.error("User already exists")
#     #             else:
#     #                 users[new_user] = new_pass
#     #                 save_users(users)
#     #                 st.sidebar.success("Account created! Now login")


#     # -----------------------
# # LOGIN
# # -----------------------
# if mode == "Login":
#     if st.button("Login"):
#         if username in users and users[username] == password:

#             st.session_state["logged_in"] = True
#             st.session_state["user"] = username   # ✅ STORE USER

#             st.success("Login Successful ✅")
#             st.rerun()
#         else:
#             st.error("Invalid credentials ❌")

# # -----------------------
# # SIGNUP
# # -----------------------
# else:
#     if st.button("Create Account"):
#         if username in users:
#             st.warning("User already exists")
#         else:
#             users[username] = password
#             save_users(users)
#             st.success("Account created successfully 🎉")
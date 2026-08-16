import streamlit as st
import random

# Set page configuration
st.set_page_config(page_title="Random Number Generator", page_icon="🎲")

# Check if the installed version even supports native auth
if not hasattr(st, "login") or not hasattr(st, "user"):
    st.error("Your Streamlit version is too old or [auth] secrets are missing!")
    st.info(f"Current Streamlit Version: {st.__version__}")
    st.stop()


# --- 1. Authentication Gatekeeper ---
if not st.user.is_logged_in:
    st.title("🔐 Authentication Required")
    st.write("Please log in with your Google account to access the generator.")
    st.button("Log in with Google", on_click=st.login)
    st.stop()  # Prevents downstream code execution until authenticated


# --- 2. Email Verification Check ---
# Ensure the Google email has been verified
if not getattr(st.user, "email_verified", False):
    st.error("⚠️ Access Denied: Your Google account email address is not verified.")
    st.write("Please log out and log in with a verified Google email address.")
    st.button("Log out and try another account", on_click=st.logout)
    st.stop()  # Stops execution for unverified accounts


# --- 3. Authenticated Application Logic ---
st.title("🎲 Random Number Generator")

# Display user greeting, email, and logout option
st.write(f"Welcome, **{st.user.name}** (`{st.user.email}`)!")
st.button("Log out", on_click=st.logout)
st.divider()
     
# Core generator logic
# Set up the inputs with default values of 0 and 100
min_val = st.number_input("Minimum value", value=0, step=1)
max_val = st.number_input("Maximum value", value=100, step=1)

# Generate the random number when the button is clicked
if st.button("Generate"):
    if min_val > max_val:
        st.error("The minimum value cannot be greater than the maximum value.")
    else:
        # Generate a random whole number inclusive of the endpoints
        random_number = random.randint(min_val, max_val)
        st.success(f"Your random number: **{random_number}**")


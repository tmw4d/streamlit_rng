import streamlit as st
import random

# Check if the installed version even supports native auth
if not hasattr(st, "login") or not hasattr(st, "user"):
    st.error("Your Streamlit version is too old or [auth] secrets are missing!")
    st.info(f"Current Streamlit Version: {st.__version__}")
    st.stop()

# --- 1. Authentication Check ---
if not st.user.is_logged_in:
    st.title("Authentication Required")
    st.write("Please log in with your Google account to access the generator.")
    st.button("Log in with Google", on_click=st.login)
    st.stop() # Stops the script here so the rest of the app doesn't render

# --- 2. Authenticated App Logic ---
st.title("Random Number Generator")

# Display user information and a logout button
st.write(f"Welcome, {st.user.name}!")
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



# OLD CODE
# 1. Check if the user is authenticated
#if not st.user.is_logged_in:
    # Prompt the user to log in if they haven't already
#    st.write("Please log in to access the application.")
#    if st.button("Log in with Google"):
#        st.login("google")
#    st.stop()  # Stop executing the rest of the page for unauthenticated users

# 2. If logged in, display the welcome message using st.user attributes
#st.title(f"Welcome, {st.user.name}!")
#st.write(f"Logged in as: {st.user.email}")

# 3. Provide a logout option
#if st.button("Log out"):
#    st.logout()


# Safe to proceed if attributes exist
#if not st.user.is_logged_in:
#    st.login()

import streamlit as st

import random

st.title("Random Number Generator")

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

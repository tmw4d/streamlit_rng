# Streamlit Random Number Generator with Google OAuth

A simple, secure Streamlit web application that generates a random whole number between two custom bounds (defaulting to 0 and 100), protected by Google OAuth 2.0 authentication.

**Live Application:** [https://tmw4d-rng.streamlit.app/](https://tmw4d-rng.streamlit.app/)

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
   - [Phase 1: Google Cloud Platform Setup](#phase-1-google-cloud-platform-setup)
   - [Phase 2: App Code Development](#phase-2-app-code-development)
   - [Phase 3: Dependencies Configuration](#phase-3-dependencies-configuration)
   - [Phase 4: Streamlit Cloud Deployment & Secrets](#phase-4-streamlit-cloud-deployment--secrets)
5. [Troubleshooting & Key Gotchas](#troubleshooting--key-gotchas)
6. [Local Development](#local-development)

---

## Overview

This project demonstrates how to implement native authentication in Streamlit (v1.42.0+) using Google Cloud Platform as the OpenID Connect (OIDC) identity provider. Users visiting the application are prompted to sign in with their Google account before gaining access to the random number generator logic.

## Features

- **Google OAuth Authentication:** Requires user sign-in via Google before revealing app controls.
- **Session Management:** Uses `st.user` for user session details (displaying user name) and explicit logout functionality via `st.logout()`.
- **Random Number Generator:** Generates an inclusive random integer between custom minimum and maximum bounds (default: 0 to 100).
- **Validation:** Handles invalid input (e.g., minimum greater than maximum) with clean error alerts.

---

## Project Structure

```text
tmw4d-rng/
├── app.py              # Main Streamlit application with auth logic
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
```

---

## Step-by-Step Setup Guide

### Phase 1: Google Cloud Platform Setup

1. **Create/Select a GCP Project:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.

2. **Configure the OAuth Consent Screen:**
   - Navigate to **APIs & Services > OAuth consent screen**.
   - Select **External** user type and click **Create**.
   - Fill in required fields:
     - **App name:** `Streamlit RNG App` (or similar)
     - **User support email:** Your email address
     - **Developer contact information:** Your email address
   - Proceed through **Scopes** and **Test Users** (defaults are sufficient for standard identity authentication).

3. **Create OAuth 2.0 Credentials:**
   - Navigate to **APIs & Services > Credentials**.
   - Click **+ Create Credentials** and select **OAuth client ID**.
   - Set **Application type** to **Web application**.
   - Set **Name** to `Streamlit RNG App`.
   - Under **Authorized redirect URIs**, click **Add URI** and enter:
     ```text
     https://tmw4d-rng.streamlit.app/oauth2callback
     ```
   - Click **Create**.
   - Copy and securely save the generated **Client ID** and **Client Secret**.

---

### Phase 2: App Code Development

Create `app.py` with authentication checks using Streamlit's native `st.user`, `st.login()`, and `st.logout()` methods:

```python
import streamlit as st
import random

# Set page configuration
st.set_page_config(page_title="Random Number Generator", page_icon="🎲")

# --- 1. Authentication Gatekeeper ---
if not st.user.is_logged_in:
    st.title("🔐 Authentication Required")
    st.write("Please log in with your Google account to access the generator.")
    st.button("Log in with Google", on_click=st.login)
    st.stop()  # Prevents downstream code execution until authenticated

# --- 2. Authenticated Application Logic ---
st.title("🎲 Random Number Generator")

# Display user greeting and logout option
st.write(f"Welcome, **{st.user.name}**!")
st.button("Log out", on_click=st.logout)
st.divider()

# Input fields
min_val = st.number_input("Minimum value", value=0, step=1)
max_val = st.number_input("Maximum value", value=100, step=1)

# Generation logic
if st.button("Generate"):
    if min_val > max_val:
        st.error("The minimum value cannot be greater than the maximum value.")
    else:
        random_number = random.randint(min_val, max_val)
        st.success(f"Your random number: **{random_number}**")
```

---

### Phase 3: Dependencies Configuration

Create `requirements.txt` in the root folder. **Note:** `httpx` is explicitly required alongside `Authlib` to prevent runtime 500 errors during authentication calls in Streamlit Community Cloud.

```text
streamlit>=1.42.0
Authlib>=1.3.2
httpx
```

---

### Phase 4: Streamlit Cloud Deployment & Secrets

1. Deploy your repository to [Streamlit Community Cloud](https://share.streamlit.io/).
2. In the Streamlit Cloud dashboard, click the three-dot menu (`...`) next to your app and select **Settings**.
3. Go to the **Secrets** section.
4. Add the `[auth]` section configuration in TOML format:

```toml
[auth]
redirect_uri = "https://tmw4d-rng.streamlit.app/oauth2callback"
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
cookie_secret = "YOUR_CUSTOM_LONG_RANDOM_SECRET_KEY"
```

> **Tip:** Replace `YOUR_CUSTOM_LONG_RANDOM_SECRET_KEY` with a long, random string (e.g., generated via `openssl rand -hex 32`) to encrypt login browser session cookies.

---

## Troubleshooting & Key Gotchas

| Issue / Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| **500 Internal Server Error** on `/~/+/auth/login` | Missing `httpx` package required internally by Authlib. | Add `httpx` to `requirements.txt` and reboot the app on Streamlit Cloud. |
| **`ModuleNotFoundError` in logs** | Dependencies not auto-installed after editing `requirements.txt`. | Manually reboot the app from the Streamlit Cloud dashboard (`...` > **Reboot app**). |
| **Redirect URI Error on Google Sign-in** | Mismatch between GCP Authorized Redirect URI and `secrets.toml`. | Ensure both match exactly: `https://tmw4d-rng.streamlit.app/oauth2callback` without markdown brackets or trailing slashes. |
| **Session keeps logging out** | Missing or changing `cookie_secret`. | Specify a static, secure `cookie_secret` string in your Streamlit Cloud secrets. |

---

## Local Development

To run this app locally for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/tmw4d-rng.git
   cd tmw4d-rng
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.streamlit/secrets.toml` in your project root with your OAuth credentials and a local redirect URI (`http://localhost:8501/oauth2callback`).
4. Run the Streamlit server:
   ```bash
   streamlit run app.py
   ```

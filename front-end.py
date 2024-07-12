import streamlit as st
from PIL import Image
import tempfile
import os
import subprocess
import time
import urllib.request
import threading
import uuid
from img2img_server import load_workflow, prompt_image_to_image,run_server,wait_for_connection
from download_files import download_all_files

st.set_page_config(page_title="PhotoRealify")

# Initialize session state for server
if 'server_started' not in st.session_state:
    st.session_state['server_started'] = False

if not st.session_state['server_started']:
    download_all_files()
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    server_address = "127.0.0.1:8188"
    client_id = str(uuid.uuid4())
    wait_for_connection(server_address)
    st.session_state['server_started'] = True

st.title("PhotoRealify")

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Text input widget
prompt = st.text_input("Enter the prompt")

# Run button
if st.button("Run"):
    if uploaded_file is not None and prompt:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            # Save the uploaded file to the temporary file
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name

        workflow = load_workflow('prompt.json')
        image = prompt_image_to_image(workflow, tmp_file_path,prompt , save_previews=True)

        st.image(image, caption="Uploaded Image.", use_column_width=True)
        os.remove(tmp_file_path)
    else:
        st.warning("Please upload an image and enter some text before clicking the Run button.")

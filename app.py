import streamlit as st
import requests

# Define FastAPI backend URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI PowerPoint Generator", layout="centered")
st.title("AI Based Auto-Generating PowerPoint Slides")
st.write("Upload documents and generate slides automatically.")

uploaded_file = st.file_uploader("Upload a document (TXT, PDF, DOCX, CSV)", type=["txt", "pdf", "docx", "csv"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")

    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    upload_response = requests.post(f"{BASE_URL}/uploadfile/", files=files)

    st.write(f"Upload status code: {upload_response.status_code}")
    st.write(upload_response.text)

    if upload_response.status_code == 200:
        st.success("File uploaded to server successfully!")

        if st.button("Generate Slides"):
            generate_response = requests.get(f"{BASE_URL}/generator/")

            if generate_response.status_code == 200:
                result = generate_response.json()
                download_url = f"{BASE_URL}{result['download_url']}"
                st.success("Slides generated successfully!")
                st.markdown(f"[Download PowerPoint]({download_url})", unsafe_allow_html=True)
            else:
                st.error("Slide generation failed! Check API logs.")
    else:
        st.error("File Upload failed! Please try again.")

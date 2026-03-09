
import streamlit as st
from PIL import Image
import cv2
import numpy as np

st.set_page_config(page_title="AI ID Forgery Detection", layout="centered")

st.title("AI ID Forgery Detection System")
st.write("Upload an ID document image to analyze possible tampering.")

uploaded_file = st.file_uploader("Upload ID Document", type=["jpg","jpeg","png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_container_width=True)

    st.success("Image format validated")

    # Convert to OpenCV format
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection (simple tampering signal)
    edges = cv2.Canny(gray,100,200)

    tamper_score = float(np.mean(edges))

    # Simple rule based fraud scoring
    risk = "LOW"

    if tamper_score > 20:
        risk = "MEDIUM"

    if tamper_score > 40:
        risk = "HIGH"

    st.subheader("Fraud Detection Report")

    st.write("Tampering Score:", round(tamper_score,2))
    st.write("Risk Level:", risk)

    if risk == "HIGH":
        st.error("⚠ Possible document tampering detected")

    elif risk == "MEDIUM":
        st.warning("⚠ Suspicious signals detected. Manual verification recommended")

    else:
        st.success("✓ Document appears likely genuine")

    # Show edges for visual explanation
    st.subheader("Edge Analysis")
    st.image(edges, caption="Edge Detection Output")

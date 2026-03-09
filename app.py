import streamlit as st
from PIL import Image
import cv2
import numpy as np

st.set_page_config(page_title="AI ID Forgery Detection", layout="centered")

st.title("AI ID Forgery Detection System")
st.write("Upload an ID document image to analyze potential tampering.")

uploaded_file = st.file_uploader("Upload ID Document", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    # Load image
    image = Image.open(uploaded_file)

    st.subheader("Uploaded Document")
    st.image(image, use_container_width=True)

    # Convert image to OpenCV format
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 100, 200)

    # Calculate tampering score
    tamper_score = float(np.mean(edges))

    # Risk evaluation
    risk = "LOW"

    if tamper_score > 20:
        risk = "MEDIUM"

    if tamper_score > 40:
        risk = "HIGH"

    # Edge visualization
    st.subheader("Edge Analysis")
    st.image(
        edges,
        caption="Edge Detection Output (used to detect tampering patterns)",
        use_container_width=True
    )

    # Structured fraud report
    st.subheader("Fraud Detection Report")

    report = {
        "tampering_score": round(tamper_score, 2),
        "risk_level": risk,
        "analysis_method": "OpenCV Edge Detection",
        "conclusion": "Possible document tampering detected" if risk != "LOW" else "Document appears genuine"
    }

    st.json(report)

    # User-friendly message
    if risk == "HIGH":
        st.error("⚠ Possible document forgery detected")

    elif risk == "MEDIUM":
        st.warning("⚠ Suspicious signals detected. Manual verification recommended")

    else:
        st.success("✅ Document appears genuine")

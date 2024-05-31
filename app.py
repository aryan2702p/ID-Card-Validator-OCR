# import streamlit as st
# import cv2
# import pytesseract
# import re
# from PIL import Image
# import numpy as np
# import os

# # Function to perform OCR and extract text from image
# def perform_ocr(image_path):
#     # Perform OCR using Tesseract
#     img = cv2.imread(image_path)

# # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Apply Gaussian blur to reduce noise
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)

# # Perform thresholding to binarize the image
#     _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# # Perform dilation to enhance the text
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     dilate = cv2.dilate(thresh, kernel, iterations=1)

# # Perform OCR on the preprocessed image using Tesseract
#     text = pytesseract.image_to_string(Image.fromarray(dilate))

#     print(text)
#     return text

# # Function to extract credentials using regex
# def extract_credentials(ocr_text):
#     # Define regex patterns for name, enrollment number, address, and validity date
#     name_pattern = r"([A-Z]+(?: [A-Z]+)*)\s+prece"
#     enrol_pattern = r"\bEnrol No\s+(\d{10})\b"
#     addr_pattern = r"\bAddress\s+(.+?)\s+(\d{6})"
#     validity_pattern = r"\bValid upto:\s+([A-Za-z]+ \d{4})"

#     # Extract credentials using regex
#     name_match = re.search(name_pattern, ocr_text)
#     name = name_match.group(1) if name_match else None

#     enrol_match = re.search(enrol_pattern, ocr_text)
#     enrol_no = enrol_match.group(1) if enrol_match else None

#     addr_match = re.search(addr_pattern, ocr_text)
#     address = addr_match.group(1) if addr_match else None
#     postal_code = addr_match.group(2) if addr_match else None

#     validity_match = re.search(validity_pattern, ocr_text)
#     validity_date = validity_match.group(1) if validity_match else None

#     return name, enrol_no, address, postal_code, validity_date

# # Streamlit app
# def main():
#     st.title("Credit Card OCR Scanner")

#     # Upload image
#     uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

#     if uploaded_image:
#         # Save the uploaded image to a temporary file
#         with open("temp_image.jpg", "wb") as f:
#             f.write(uploaded_image.getbuffer())

#         # Display uploaded image
#         st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

#         # Perform OCR and extract credentials
#         ocr_text = perform_ocr("temp_image.jpg")
#         name, enrol_no, address, postal_code, validity_date = extract_credentials(ocr_text)

#         # Display extracted credentials
#         st.subheader("Extracted Credentials:")
#         st.write(f"Name: {name}" if name else "Name: Not found")
#         st.write(f"Enrollment Number: {enrol_no}" if enrol_no else "Enrollment Number: Not found")
#         st.write(f"Address: {address}" if address else "Address: Not found")
#         st.write(f"Postal Code: {postal_code}" if postal_code else "Postal Code: Not found")
#         st.write(f"Validity Date: {validity_date}" if validity_date else "Validity Date: Not found")

#         # Clean up by removing the temporary file
#         os.remove("temp_image.jpg")

# # Run the Streamlit app
# if __name__ == "__main__":
#     main()
import streamlit as st
import easyocr
import re
import os
from PIL import Image

# Function to perform OCR and extract text from image
def perform_ocr(image_path):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    # Perform OCR on the image
    result = reader.readtext(image_path)
    
    # Extract the text from the OCR result
    extracted_text = ""
    for (bbox, text, prob) in result:
        extracted_text += text + "\n"
    
    print(extracted_text)
    
    return extracted_text

# Function to extract credentials using regex
def extract_credentials(ocr_text):
    # Define regex patterns for name, enrollment number, address, and validity date
    name_pattern = r"\b([A-Z]+(?:\s[A-Z]+)+)\b"
    enrol_pattern = r"Enroll No[:;\s]+(\d{10})"
    addr_pattern = r"Address\s+(.+?)\s+(\d{6})"
    validity_pattern = r"Valid upto\s*[:=]*\s*([A-Za-z]+\s+\d{4})"
    # Extract credentials using regex
    name_match = re.search(name_pattern, ocr_text)
    name = name_match.group(1) if name_match else None

    enrol_match = re.search(enrol_pattern, ocr_text)
    enrol_no = enrol_match.group(1) if enrol_match else None

    addr_match = re.search(addr_pattern, ocr_text, re.DOTALL)
    address = addr_match.group(1) if addr_match else None
    postal_code = addr_match.group(2) if addr_match else None

    validity_match = re.search(validity_pattern, ocr_text)
    validity_date = validity_match.group(1) if validity_match else None

    return name, enrol_no, address, postal_code, validity_date

# Streamlit app
def main():
    
    st.title("ID Card OCR Scanner ")

    # Upload image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        # Save the uploaded image to a temporary file
        image_path = "temp_image.jpg"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

        # Display uploaded image
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

        # Perform OCR and extract credentials
        ocr_text = perform_ocr(image_path)
        name, enrol_no, address, postal_code, validity_date = extract_credentials(ocr_text)

        # Display extracted credentials
        st.subheader("Extracted Credentials:")
        #st.write(f"Name: {name}" if name else "Name: Not found")
        st.write(f"Enrollment Number: {enrol_no}" if enrol_no else "Enrollment Number: Not found")
        st.write(f"Address: {address}" if address else "Address: Not found")
        st.write(f"Postal Code: {postal_code}" if postal_code else "Postal Code: Not found")
        st.write(f"Validity Date: {validity_date}" if validity_date else "Validity Date: Not found")

        # Clean up by removing the temporary file
        os.remove(image_path)

# Run the Streamlit app
if __name__ == "__main__":
    main()

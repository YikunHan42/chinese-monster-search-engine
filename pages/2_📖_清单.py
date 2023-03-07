import streamlit as st
import base64
# import os

st.markdown("目前收录的妖怪清单如下：")

file_path = './demon.pdf'

with open(file_path,"rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'

st.markdown(pdf_display, unsafe_allow_html=True)


# with open("post1-compressed.pdf", "rb") as pdf_file:
# PDFbyte = pdf_file.read()
# st.download_button(label="Download PDF Tutorial",
# data=PDFbyte,
# file_name="pandas-clean-id-column.pdf",
# mime='application/octet-stream')
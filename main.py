import streamlit as st
import sys
# from ..jobAppAutomater.db.db_main import db_connection
import db_main
from io import StringIO


pdf_path = 'uploads/linkedin_profile.pdf'  # Path to the uploaded resume (adjust path as needed)

ss = st.session_state

st.set_page_config(
    page_title="[Insert our Name]",
    page_icon="👋",
)

st.write("# Welcome to [Insert Our Name]! 👋")


# Initialize the session state to store the list
if 'skills' not in ss:
    ss.skills = []
if 'position' not in ss:
    ss.position = ""
if 'whyResponse' not in ss:
    ss.whyResponse = ""
if "currQ" not in ss:
    ss.currQ = ""
if "currRes" not in ss:
    ss.currRes = ""
if "additionalResponses" not in ss:
    ss.additionalResponses = []
if "addMoreInfo" not in ss:
    ss.addMoreInfo = True
if "pdf" not in ss:
    ss.pdf = ""
if "stringio" not in ss:
    ss.stringio = ""

# ss.pdf = st.file_uploader("Upload Linkedin PDF", type="pdf", accept_multiple_files=False)
# ss.stringio = StringIO(ss.pdf.getvalue().decode("utf-8"))
# st.write(ss.stringio.read())

pdf=st.file_uploader("Upload Linkedin PDF", type="pdf", accept_multiple_files=False)

# Create a text input field
user_input = st.text_input("Enter your skills:", "")

# When the user submits an item, add it to the list
if st.button("Add skill"):
    if user_input:
        ss.skills.append(user_input)
        st.success(f"Added: {user_input}")


ss.position = st.text_input("What position title are you looking for?") 

ss.whyResponse = st.text_area("Give a short description for why you are interested to be a "+ss.position+".")

addInfoBtn = st.subheader("Optional: Answer personalized prompts (this will help us create better personlized resources).", divider="gray")

ss.currQ = st.text_input("Add a Question")
ss.currRes = st.text_area("Give your response")
addResponse = st.button("Add Response")
if addResponse:
    ss.additionalResponses.append((ss.currQ, ss.currRes))

st.write(ss.additionalResponses)

testdb = st.button("Test")
if testdb:
    st.write(db_main.db_connection(pdf, user_input_skills=ss.skills, industries_of_interest="", describe_yourself="", question=""))



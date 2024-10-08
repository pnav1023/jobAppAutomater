import streamlit as st

ss = st.session_state

st.set_page_config(
    page_title="[Insert our Name]",
    page_icon="👋",
)

st.write("# Welcome to [Insert Our Name]! 👋")

st.file_uploader("Upload Linkedin PDF", type="pdf", accept_multiple_files=False)

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





# Display the list
# if ss.skills:
#     st.write("Your list of skills:")
#     for skill in ss.skills:
#         st.write(skill)



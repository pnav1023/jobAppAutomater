import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if st.button("Generate links"):
    topic="python programming"

    messages = [
        {
            "role": "system",
            "content": (
                "Generate links to educational resources based on the topic given."
                "Include links to least one beginner youtube video, one advanced youtube video, a wikipedia article and an official source."
            ),
        },
        {
            "role": "user",
            "content": topic,
        },
    ]

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    st.write(response.choices[0].message.content)
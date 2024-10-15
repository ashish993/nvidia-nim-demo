##### Importing libraries
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

# Streamlit app title
st.title("NVidia NIM Platform")

# Get user input
user_prompt = st.text_area("Enter your prompt:", value="What is GPU computing in 50 words.")

#List of available models models
models = ["meta/llama-3.1-405b-instruct",
        "meta/1lama-3.1-8b-instruct",
        "nvidia/nemotron-4-340b-instruct",
        "nv-mistralai/mistral-nemo-12b-instruct",
        "mistralai/mathstral-7b-ve.1", 
        "google/gemma-2-2b-it",
        "writer/palmyra-fin-70b-32k"]

selected_models = st.multiselect("Select models:", models)

#Initialize OpenAI client
client=OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)
    
# Generate when the user clicks the button
if st.button("Generate Responses"):
    for model in selected_models:
        completion =  client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        # Display the result 
        limerick = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                limerick += chunk.choices[0].delta.content

        st.write(f"Response from {model}:")
        st.write(limerick)
        st.write("---")

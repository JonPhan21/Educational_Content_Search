"""
Educational Content Search Engine
Main application entry point
"""

#Import modules
import streamlit as st
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Ou_Search")
st.title("Ou_Search")

@st.cache_resource
def setup_bedrock():
    return boto3.client(
        'bedrock-agent-runtime'
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

bedrock = setup_bedrock()
kb_id = os.getenv('KNOWLEDGE_BASE_ID')

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.write(messages['content'])

if prompt := st.chat_input("Ask me for anything related to your documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                engineer_prompt = f"You are an AI assistant for an educational content search engine. Use the knowledge base to provide accurate and concise answers to user queries. You are free to give the user downloadable docx files from the knowledge base. This is the prompt {prompt}"

                response = bedrock.retrieve_and_generate(
                    input={
                        'text': (engineer_prompt)
                    }, 
                    retrieveAndGenerateConfiguration={
                        'type': 'KNOWLEDGE_BASE',
                        'knowledgeBaseConfiguration': {
                            'knowledgeBaseId': kb_id,
                            'modelArn': "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"}
                        }
                )

                answer = response['output']['text']
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                st.error(f"Error: {e}")

                           




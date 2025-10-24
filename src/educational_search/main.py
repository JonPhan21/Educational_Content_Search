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
                engineer_prompt = f"""
                Situation
                You are working with a collection of documents that need to be organized and presented in a structured format for easy reference and access.

                Task
                You are an expert data analyst and information organizer. Create a comprehensive table with exactly 3 columns that organizes the provided documents. The assistant should format the output as a clean, well-structured table where each row represents one document.

                Objective
                To provide a clear, organized overview of multiple documents that allows for quick scanning of content and easy access to source materials.

                Knowledge
                The table must contain exactly these 3 columns:

                Document Title - The official or descriptive title of each document
                AI Summary - A concise, informative summary that captures the key points, main topics, and essential information from each document
                Website Link - The complete URL where the document can be accessed online
                The assistant should ensure summaries are comprehensive enough to understand the document's purpose and content without being overly lengthy. All links should be properly formatted and functional. If any information is missing for a particular document, clearly indicate this in the appropriate cell rather than leaving it blank.

                When multiple documents are provided, the assistant should organize them in a logical order (alphabetical by title, chronological, or by relevance) and ensure consistent formatting throughout the table.

                This is the prompt {prompt}
                """




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

                           




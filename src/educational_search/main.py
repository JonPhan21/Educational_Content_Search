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

# Enhanced page configuration
st.set_page_config(
    page_title="Ou Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling and readable text
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .search-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .stChatMessage {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        line-height: 1.6;
        font-size: 16px;
    }
    .stChatMessage p {
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    .stChatMessage table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 14px;
    }
    .stChatMessage th {
        background: #667eea;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: 600;
    }
    .stChatMessage td {
        padding: 12px;
        border-bottom: 1px solid #e9ecef;
        vertical-align: top;
        color: #2c3e50;
    }
    .stChatMessage tr:nth-child(even) {
        background: #f8f9fa;
    }
    .stChatMessage a {
        color: #667eea;
        text-decoration: none;
    }
    .stChatMessage a:hover {
        text-decoration: underline;
    }
    .readable-content {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.7;
        color: #2c3e50;
        max-width: none;
    }
    .stSpinner {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Beautiful header
st.markdown("""
<div class="main-header">
    <h1>🔍 Ou Search</h1>
    <p>Your Intelligent Asian American Educational Content Search Engine</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def setup_bedrock():
    try:
        # Handle both permanent and temporary credentials
        client_kwargs = {
            'service_name': 'bedrock-agent-runtime',
            'region_name': os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
        }
        
        # Add credentials if provided
        if os.getenv('AWS_ACCESS_KEY_ID'):
            client_kwargs['aws_access_key_id'] = os.getenv('AWS_ACCESS_KEY_ID')
            client_kwargs['aws_secret_access_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')
            
            # Add session token if using temporary credentials
            if os.getenv('AWS_SESSION_TOKEN'):
                client_kwargs['aws_session_token'] = os.getenv('AWS_SESSION_TOKEN')
        
        return boto3.client(**client_kwargs)
    except Exception as e:
        st.error(f"Failed to setup AWS Bedrock client: {e}")
        return None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Configuration validation
required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'KNOWLEDGE_BASE_ID']
missing_vars = [var for var in required_vars if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}_here"]

if missing_vars:
    st.error(f"❌ **Missing Configuration:** {', '.join(missing_vars)}")
    st.info("💡 **Setup Required:** Please configure your .env file with valid AWS credentials and Knowledge Base ID")
    st.stop()

bedrock = setup_bedrock()
kb_id = os.getenv('KNOWLEDGE_BASE_ID')

if not bedrock:
    st.error("❌ **AWS Connection Failed:** Unable to connect to Bedrock")
    st.stop()

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.write(messages['content'])

# Search interface with better styling
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown("### 💬 Ask Your Question")
st.markdown("*Search through educational documents and get organized, comprehensive answers*")
st.markdown('</div>', unsafe_allow_html=True)

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

                           




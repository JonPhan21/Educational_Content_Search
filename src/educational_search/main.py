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
        'bedrock_agent_runtime',
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name = os.getenv('AWS_DEFAULT_REGION')
    )






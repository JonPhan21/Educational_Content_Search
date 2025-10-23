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
        'bedrock-agent-runtime',
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name = os.getenv('AWS_DEFAULT_REGION')
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
                response = bedrock.retrieve_and_generate(
                    input={
                        'text': (
                            f"""<|im_start|>system
You are a historian and educator specializing in Asian American and Pacific Islander (AAPI) history, culture, and pedagogy. Your expertise aligns with the educational resources and principles found at asianamericanedu.org.

ROLE AND RESPONSIBILITIES:
- Analyze teacher curriculum requests and materials
- Search through available AAPI educational resources 
- Identify relevant course plans, lessons, and thematic units
- Recommend curriculum improvements with cultural sensitivity

OUTPUT STRUCTURE:
1. Teacher Request Summary: Briefly restate what the educator is asking for
2. Recommended Focus: Identify the most relevant course plans/modules from available resources
3. Suggested Revisions: Provide specific, actionable improvements including:
   - Missing perspectives (Pacific Islander voices, immigrant labor histories, women's narratives)
   - Cultural balance and representation improvements
   - Connections between historical events and current community issues
4. Supporting Examples: Include relevant stories, case studies, or historical figures when they directly enhance curriculum goals
5. Source Citations: Reference specific documents from the knowledge base

GUIDING PRINCIPLES:
- Prioritize historical accuracy, cultural sensitivity, and pedagogical usefulness
- Be concise yet insightful
- Show both WHY and HOW suggested changes improve curriculum
- Maintain academic yet accessible tone for educators
- ESSENTIAL: Directly reference and cite the retrieved documents in your feedback
<|im_end|>

TEACHER REQUEST:
{prompt}

Please analyze this request and provide curriculum recommendations following the structure outlined in your role description. Make sure to directly reference specific documents from the available resources in your recommendations.
<|im_end|>

<|im_start|>assistant""")
                    }, 
                    retrieveAndGenerateConfiguration={
                        'type': 'KNOWLEDGE_BASE',
                        'knowledgeBaseConfiguration': {
                            'knowledgeBaseId': kb_id,
                            'modelArn': f'arn:aws:bedrock:us-west-2::foundation-model/{os.getenv("BEDROCK_MODEL_ID")}'
                        }
                    }
                )

                answer = response['output']['text']
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                st.error(f"Error: {e}")

                           




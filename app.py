import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="API Chat Interface",
    page_icon="💬",
    layout="wide"
)

# Title and description
st.title("💬 Chat API Interface")
st.markdown("Connect to your local API endpoint and chat!")

# API Configuration in sidebar
st.sidebar.header("⚙️ API Configuration")
api_url = st.sidebar.text_input(
    "API URL", 
    value="http://localhost:7860/api/v1/run/1effbd4f-0774-486b-971c-6431bf605188",
    help="Enter your API endpoint URL"
)

api_key = st.sidebar.text_input(
    "API Key", 
    value="sk-KoHDHZh68T9juZavQoTOgjDGx1Nn68TeWqe6AfEACvg",
    type="password",
    help="Enter your API key"
)

stream_enabled = st.sidebar.checkbox("Enable Streaming", value=False)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to make API call
def call_api(user_input, api_url, api_key, stream=False):
    """Make API call to the specified endpoint"""
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    
    # Construct URL with stream parameter
    url = f"{api_url}?stream={'true' if stream else 'false'}"
    
    data = {
        "input_value": user_input,
        "output_type": "chat",
        "input_type": "chat"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
    except json.JSONDecodeError as e:
        return None, f"JSON decode error: {str(e)}"

# Chat input
if prompt := st.chat_input("What would you like to say?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Make API call
            response_data, error = call_api(
                prompt, 
                api_url, 
                api_key, 
                stream=stream_enabled
            )
            
            if error:
                error_message = f"❌ Error: {error}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message
                })
            else:
                # Extract response content
                if isinstance(response_data, dict):
                    response_content = (
                        response_data.get('output_value') or 
                        response_data.get('response') or 
                        response_data.get('message') or 
                        response_data.get('content') or 
                        str(response_data)
                    )
                else:
                    response_content = str(response_data)
                
                st.markdown(response_content)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_content
                })

# Sidebar additional options
st.sidebar.markdown("---")
st.sidebar.header("🔧 Options")

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Display API response structure
if st.sidebar.checkbox("Show Debug Info"):
    st.sidebar.markdown("### Latest API Response")
    if st.session_state.messages:
        st.sidebar.json({"last_response": "Check browser console for full response"})

# Connection test
st.sidebar.markdown("---")
if st.sidebar.button("Test Connection"):
    with st.spinner("Testing connection..."):
        test_response, test_error = call_api(
            "test", 
            api_url, 
            api_key, 
            stream=stream_enabled
        )
        
        if test_error:
            st.sidebar.error(f"❌ Connection failed: {test_error}")
        else:
            st.sidebar.success("✅ Connection successful!")
            st.sidebar.json(test_response)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | API Chat Interface", unsafe_allow_html=True)
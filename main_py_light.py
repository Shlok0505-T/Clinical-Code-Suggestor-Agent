import streamlit as st
import requests
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MedSimplify AI - Medical Text Simplification",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for light modern theme
st.markdown("""
<style>
    /* Global light theme */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header {
        background: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .section-header h3 {
        margin: 0;
        color: #1e293b;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .chat-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .user-message {
        background: #f1f5f9;
        color: #1e293b;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .assistant-message {
        background: #fefefe;
        color: #1e293b;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #764ba2;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .error-message {
        background: #fef2f2;
        color: #dc2626;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #ef4444;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.1);
        border: 1px solid #fecaca;
    }
    
    .input-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
    }
    
    .sidebar-content {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .metric-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    .timestamp {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        font-style: italic;
    }
    
    .message-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .doctor-badge {
        background: #667eea;
        color: white;
    }
    
    .ai-badge {
        background: #764ba2;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    .stExpander {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    .stExpander > div:first-child {
        background-color: #ffffff;
        color: #1e293b;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #f0fdf4 !important;
        color: #16a34a !important;
        border-left: 4px solid #22c55e !important;
        border: 1px solid #bbf7d0 !important;
    }
    
    .stError {
        background-color: #fef2f2 !important;
        color: #dc2626 !important;
        border-left: 4px solid #ef4444 !important;
        border: 1px solid #fecaca !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 2px solid #cbd5e1 !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #1e293b !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🩺 MedSimplify AI</h1>
    <p style="font-size: 1.2rem; margin: 0.5rem 0 0 0; opacity: 0.9;">Medical Text Simplification Assistant</p>
</div>
""", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("""
    <div class="section-header">
        <h3>⚙️ Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # API Configuration
    with st.expander("🔧 API Settings", expanded=False):
        api_url = st.text_input(
            "API Endpoint", 
            value="http://localhost:7860/api/v1/run/1effbd4f-0774-486b-971c-6431bf605188",
            help="Your medical simplification API endpoint"
        )
        
        api_key = st.text_input(
            "API Key", 
            value=os.getenv("API_KEY", "sk-KoHDHZh68T9juZavQoTOgjDGx1Nn68TeWqe6AfEACvg"),
            type="password",
            help="Secure API authentication key"
        )
        
        stream_enabled = st.checkbox("🔄 Real-time Processing", value=False)
    
    # Quick Actions
    st.markdown("""
    <div class="section-header">
        <h3>🚀 Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_test, col_clear = st.columns(2)
    
    with col_test:
        if st.button("🔍 Test", use_container_width=True):
            with st.spinner("Testing..."):
                try:
                    headers = {'Content-Type': 'application/json', 'x-api-key': api_key}
                    url = f"{api_url}?stream=false"
                    data = {"input_value": "test connection", "output_type": "chat", "input_type": "chat"}
                    response = requests.post(url, headers=headers, json=data, timeout=10)
                    if response.status_code == 200:
                        st.success("✅ Connected!")
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection failed")
    
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Usage Statistics
    st.markdown("""
    <div class="section-header">
        <h3>📊 Session Stats</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" in st.session_state:
        total_messages = len(st.session_state.messages)
        doctor_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        simplified_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_messages}</div>
            <div class="metric-label">Total Messages</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{doctor_messages}</div>
            <div class="metric-label">Texts Processed</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{simplified_messages}</div>
            <div class="metric-label">Simplifications</div>
        </div>
        """, unsafe_allow_html=True)

with col1:
    st.markdown("""
    <div class="section-header">
        <h3>💬 Medical Text Simplification</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm here to help you simplify complex medical language for better patient communication. Please share the medical text you'd like me to simplify.",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    # Display chat history in container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <span class="message-badge doctor-badge">👨‍⚕️ MEDICAL TEXT</span>
                <div>{message["content"]}</div>
                <div class="timestamp">{message.get("timestamp", "")}</div>
            </div>
            """, unsafe_allow_html=True)
        elif "Error" in message["content"]:
            st.markdown(f"""
            <div class="error-message">
                <span class="message-badge" style="background: #ef4444;">❌ ERROR</span>
                <div>{message["content"]}</div>
                <div class="timestamp">{message.get("timestamp", "")}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <span class="message-badge ai-badge">🤖 SIMPLIFIED VERSION</span>
                <div>{message["content"]}</div>
                <div class="timestamp">{message.get("timestamp", "")}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Function to make API call
    def call_api(user_input, api_url, api_key, stream=False):
        headers = {'Content-Type': 'application/json', 'x-api-key': api_key}
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
    
    # Input area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Create input area
    input_col1, input_col2 = st.columns([4, 1])
    
    with input_col1:
        user_input = st.text_area(
            "",
            placeholder="Enter complex medical text to simplify (e.g., 'The patient presents with acute myocardial infarction'):",
            height=100,
            key="medical_input",
            label_visibility="collapsed"
        )
    
    with input_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("🔄 Simplify", use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process input
    if send_button and user_input.strip():
        # Add user message
        current_time = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": current_time
        })
        
        # Show processing
        with st.spinner("🔄 Processing medical text..."):
            response_data, error = call_api(user_input, api_url, api_key, stream=stream_enabled)
            
            if error:
                error_message = f"Failed to fetch simplification: {error}"
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message,
                    "timestamp": current_time
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
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_content,
                    "timestamp": current_time
                })
        
        # Clear input and rerun
        st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem; margin-top: 2rem; border-top: 1px solid #e2e8f0;">
    <p><strong>MedSimplify AI</strong> - Medical Communication Assistant</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">⚠️ This tool is for communication assistance only. Always verify medical accuracy.</p>
</div>
""", unsafe_allow_html=True)
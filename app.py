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

# Custom CSS for dark modern theme
st.markdown("""
<style>
    /* Global dark theme */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .section-header {
        background: #2d2d2d;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .section-header h3 {
        margin: 0;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .chat-container {
        background: #2d2d2d;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid #404040;
    }
    
    .user-message {
        background: #404040;
        color: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .assistant-message {
        background: #333333;
        color: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #764ba2;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .error-message {
        background: #4a1f1f;
        color: #ff6b6b;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 4px solid #ff6b6b;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .input-container {
        background: #2d2d2d;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid #404040;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 2px solid #555555 !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 2px solid #555555 !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .sidebar-content {
        background: #2d2d2d;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #404040;
    }
    
    .metric-card {
        background: #333333;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #cccccc;
        margin-top: 0.5rem;
    }
    
    .timestamp {
        font-size: 0.8rem;
        color: #888888;
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
        background-color: #1a1a1a;
    }
    
    .stExpander {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 12px;
    }
    
    .stExpander > div:first-child {
        background-color: #2d2d2d;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #1a4a3a !important;
        color: #4ade80 !important;
        border-left: 4px solid #4ade80 !important;
    }
    
    .stError {
        background-color: #4a1f1f !important;
        color: #ff6b6b !important;
        border-left: 4px solid #ff6b6b !important;
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
                <span class="message-badge" style="background: #ff6b6b;">❌ ERROR</span>
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
            placeholder="Input Your Doctor's Note (e.g., 'Pt. c/o CP. Has HTN. ECG done. Rx: Nitroglycerin'):",
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
                error_message = f"Failed to fetch insight: {error}"
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
<div style="text-align: center; color: #666666; padding: 2rem; margin-top: 2rem; border-top: 1px solid #404040;">
    <p><strong>MedSimplify AI</strong> - Medical Communication Assistant</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">⚠️ This tool is for communication assistance only. Always verify medical accuracy.</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import time
from model_handler import ModelHandler
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AI Chatbot Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .chat-container {
        background: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize model handler
@st.cache_resource
def initialize_model():
    return ModelHandler()

model_handler = initialize_model()

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot Control Panel")
    
    # Model status
    model_info = model_handler.get_model_info()
    
    if model_info["status"] == "Model loaded successfully":
        st.success("✅ Model Status: Active")
        
        # Model information
        st.subheader("📊 Model Information")
        st.info(f"**Input Shape:** {model_info['input_shape']}")
        st.info(f"**Output Shape:** {model_info['output_shape']}")
        st.info(f"**Layers:** {model_info['layers']}")
        st.info(f"**Parameters:** {model_info['parameters']:,}")
        
        # Performance metrics (dummy data for demo)
        st.subheader("📈 Performance Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Response Time", "0.23s", "-0.05s")
        with col2:
            st.metric("Accuracy", "94.2%", "+2.1%")
            
        # Model confidence chart
        st.subheader("🎯 Recent Predictions")
        if "prediction_history" not in st.session_state:
            st.session_state.prediction_history = []
        
        if st.session_state.prediction_history:
            df = pd.DataFrame(st.session_state.prediction_history)
            fig = px.line(df, x='timestamp', y='confidence', 
                         title='Model Confidence Over Time',
                         labels={'confidence': 'Confidence Score', 'timestamp': 'Time'})
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Model Status: Error")
        st.error(model_info["status"])
    
    # Settings
    st.subheader("⚙️ Settings")
    show_confidence = st.checkbox("Show Confidence Scores", value=True)
    response_style = st.selectbox("Response Style", 
                                 ["Professional", "Casual", "Technical"])
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.prediction_history = []
        st.rerun()

# Main content
st.markdown('<h1 class="main-header">🤖 AI Chatbot Demo</h1>', unsafe_allow_html=True)

# Status overview
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Model Status", "Active" if model_info["status"] == "Model loaded successfully" else "Error")
with col2:
    st.metric("Total Messages", len(st.session_state.get("messages", [])))
with col3:
    st.metric("Session Time", f"{int(time.time()) % 3600}s")
with col4:
    avg_confidence = sum([p['confidence'] for p in st.session_state.get("prediction_history", [])]) / max(len(st.session_state.get("prediction_history", [])), 1)
    st.metric("Avg Confidence", f"{avg_confidence:.2f}")

# Chat interface
st.markdown("### 💬 Chat Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm your AI assistant powered by a TensorFlow model. How can I help you today?"
    })

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            # Get response from model
            response = model_handler.generate_response(prompt)
            
            # Add prediction to history for charts
            prediction_result = model_handler.predict(prompt)
            if prediction_result.get("success", False):
                confidence = prediction_result["prediction"][0][0]
                st.session_state.prediction_history.append({
                    "timestamp": len(st.session_state.prediction_history),
                    "confidence": confidence,
                    "message": prompt[:30] + "..." if len(prompt) > 30 else prompt
                })
            
            # Display response
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 <strong>AI Chatbot Demo</strong> | Powered by TensorFlow & Streamlit</p>
    <p>Built to showcase model integration and professional UI design</p>
</div>
""", unsafe_allow_html=True)

# Real-time model monitoring (optional)
if st.sidebar.button("🔄 Refresh Model Stats"):
    st.rerun()


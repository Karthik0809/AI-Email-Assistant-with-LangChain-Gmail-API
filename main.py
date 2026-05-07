import streamlit as st
import sys
import os
from urllib.parse import quote

# Ensure the utils directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.reply_generator import ReplyGenerator
from config import Config

st.set_page_config(page_title="Email Reply Helper", layout="centered")

st.title("📧 Email Reply Helper")
st.write("Paste an email, generate a reply using AI, and open it in Gmail with one click.")

# Initialize the reply generator
@st.cache_resource
def get_reply_generator():
    return ReplyGenerator()

reply_generator = get_reply_generator()

# --- Session State Initialization ---
if 'generated_reply' not in st.session_state:
    st.session_state.generated_reply = ""
if 'generation_mode' not in st.session_state:
    st.session_state.generation_mode = ""

# --- Sidebar Configuration ---
st.sidebar.header("⚙️ Configuration")

# Show AI status
ai_status = reply_generator.get_ai_status()
if "✅" in ai_status:
    st.sidebar.success(ai_status)
else:
    st.sidebar.error(ai_status)
    st.sidebar.warning("AI is not available. Please check your configuration.")

# Model selection for OpenRouter
selected_model = Config.OPENROUTER_MODEL
if Config.USE_OPENROUTER:
    st.sidebar.subheader("🤖 AI Model Selection")
    available_models = Config.get_available_models()
    selected_model = st.sidebar.selectbox(
        "Choose Model:",
        available_models,
        index=available_models.index(Config.OPENROUTER_MODEL) if Config.OPENROUTER_MODEL in available_models else 0,
        help="Select the AI model to use for generating replies."
    )

# Tone selection
st.sidebar.subheader("🎭 Tone Selection")
selected_tone = st.sidebar.selectbox(
    "Choose Tone:",
    ["Professional", "Friendly", "Concise", "Detailed", "Enthusiastic", "Apologetic"],
    index=0
)

# --- UI Components ---

# 1. Input for the original email
st.header("1. Paste the Email You Received")
email_content = st.text_area(
    "Incoming Email Content:",
    height=150,
    placeholder="Hi, I was wondering if we could schedule a meeting for next week..."
)

# 2. Inputs for reply details
st.header("2. Prepare Your Reply")
col1, col2 = st.columns(2)
with col1:
    recipient = st.text_input("Recipient's Email:", placeholder="original_sender@example.com")
with col2:
    subject = st.text_input("Subject:", value="Re: Your Email")

# 3. Generate the reply
if st.button("🤖 Generate AI Reply", type="primary"):
    if email_content.strip():
        with st.spinner("Generating AI reply..."):
            reply, mode = reply_generator.generate_reply(
                email_content,
                model_name=selected_model,
                tone=selected_tone
            )
            st.session_state.generated_reply = reply
            st.session_state.generation_mode = mode
    else:
        st.warning("Please paste the email content above.")

# 4. Display the generated reply and provide the send link
if st.session_state.generated_reply:
    st.header("3. Your Generated Reply")
    
    # Show which mode was used
    if st.session_state.generation_mode == "ai":
        st.success("✅ Reply generated using AI (LangChain)")
    else:
        st.error("❌ Error generating reply")
    
    edited_reply = st.text_area(
        "You can edit the reply here:",
        value=st.session_state.generated_reply,
        height=200
    )

    if recipient:
        # URL-encode the body and subject for the mailto link
        encoded_subject = quote(subject)
        encoded_body = quote(edited_reply)
        
        # Create the mailto link
        mailto_link = f"mailto:{recipient}?subject={encoded_subject}&body={encoded_body}"
        
        # Display the button as a link
        st.markdown(
            f'<a href="{mailto_link}" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px;">🚀 Send via Gmail</a>',
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter the recipient's email to create the 'Send' link.")

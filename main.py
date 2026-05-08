import streamlit as st
import sys
import os
from urllib.parse import quote

# Ensure the utils directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.reply_generator import ReplyGenerator
from utils.gmail_manager import GmailManager
from config import Config

st.set_page_config(page_title="Email Reply Helper", layout="wide")

st.title("📧 Email Reply Helper")
st.write("Paste an email, generate a reply using AI, and open it in Gmail with one click.")

# Initialize the reply generator
@st.cache_resource
def get_reply_generator():
    return ReplyGenerator()

reply_generator = get_reply_generator()

# --- Session State Initialization ---
if 'gmail_manager' not in st.session_state:
    st.session_state.gmail_manager = GmailManager()

gmail_manager = st.session_state.gmail_manager

if 'generated_reply' not in st.session_state:
    st.session_state.generated_reply = ""
if 'generation_mode' not in st.session_state:
    st.session_state.generation_mode = ""
if 'gmail_authenticated' not in st.session_state:
    st.session_state.gmail_authenticated = False
if 'recent_emails' not in st.session_state:
    st.session_state.recent_emails = []

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

# Gmail Integration in Sidebar
st.sidebar.subheader("📧 Gmail Integration")
if not st.session_state.gmail_authenticated:
    if st.sidebar.button("Connect to Gmail"):
        service, message = gmail_manager.authenticate()
        if service:
            st.session_state.gmail_authenticated = True
            st.sidebar.success(message)
        else:
            st.sidebar.error(message)
else:
    st.sidebar.success("✅ Gmail Connected")
    if st.sidebar.button("Fetch Recent Emails"):
        with st.spinner("Fetching emails..."):
            st.session_state.recent_emails = gmail_manager.get_recent_emails()
            if not st.session_state.recent_emails:
                st.sidebar.warning("No emails found.")

# --- UI Components ---

# 1. Input for the original email
col_email_list, col_email_input = st.columns([1, 2])

with col_email_list:
    st.header("📬 Inbox")
    if st.session_state.recent_emails:
        for idx, email in enumerate(st.session_state.recent_emails):
            if st.button(f"{email['from'][:25]}...\n{email['subject'][:30]}...", key=f"email_{idx}"):
                st.session_state.selected_email = email
    else:
        st.write("Connect Gmail and fetch emails to see them here.")

with col_email_input:
    st.header("1. Email Content")

    # If an email is selected from the list, use its content
    default_content = ""
    default_recipient = ""
    default_subject = "Re: Your Email"

    if 'selected_email' in st.session_state:
        default_content = st.session_state.selected_email['body']
        default_recipient = st.session_state.selected_email['from']
        # Extract email between brackets if present
        import re
        email_match = re.search(r'<(.*?)>', default_recipient)
        if email_match:
            default_recipient = email_match.group(1)
        default_subject = f"Re: {st.session_state.selected_email['subject']}"

    email_content = st.text_area(
        "Incoming Email Content:",
        value=default_content,
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
        c1, c2 = st.columns(2)
        with c1:
            # URL-encode the body and subject for the mailto link
            encoded_subject = quote(subject)
            encoded_body = quote(edited_reply)

            # Create the mailto link
            mailto_link = f"mailto:{recipient}?subject={encoded_subject}&body={encoded_body}"

            # Display the button as a link
            st.markdown(
                f'<a href="{mailto_link}" target="_blank" style="display: inline-block; padding: 12px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; width: 100%;">🚀 Open in Desktop Client</a>',
                unsafe_allow_html=True
            )
        
        with c2:
            if st.session_state.gmail_authenticated:
                if st.button("📤 Send via Gmail API", type="primary", use_container_width=True):
                    thread_id = st.session_state.selected_email['threadId'] if 'selected_email' in st.session_state else None
                    success, message = gmail_manager.send_reply(recipient, subject, edited_reply, thread_id)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            else:
                st.info("Connect Gmail to send directly via API.")
    else:
        st.warning("Please enter the recipient's email to create the 'Send' link.")

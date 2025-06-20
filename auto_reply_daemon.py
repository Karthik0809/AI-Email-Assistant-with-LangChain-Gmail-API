
import time
from utils.gmail_api import authenticate_gmail, fetch_recent_email
from agent.reply_agent import generate_reply
from utils.smtp_sender import send_email

CHECK_INTERVAL = 60  # seconds

def main():
    service = authenticate_gmail()
    print("🤖 Auto-reply daemon started...")

    while True:
        try:
            email_text = fetch_recent_email(service)
            if email_text:
                print("📬 New email received. Generating reply...")
                reply = generate_reply(email_text)
                send_email(reply, to_email="someone@example.com")  # Replace with parsed email
                print("✅ Reply sent.")
            else:
                print("📭 No new email.")

            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("❌ Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()

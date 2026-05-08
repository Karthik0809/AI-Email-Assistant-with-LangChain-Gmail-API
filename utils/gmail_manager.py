import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

class GmailManager:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None

    def authenticate(self):
        """Authenticates the user and returns the Gmail service object."""
        # Note: In a production environment like Render, you should use a web-based
        # OAuth flow with redirect URIs. This implementation uses the local server flow
        # which is suitable for local development. For hosting, you'd need to adapt
        # this to handle session-based storage of tokens and redirect handling.
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            try:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_path):
                        return None, "credentials.json not found. Please follow the instructions in README to set it up."

                    # This part will only work locally
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    self.creds = flow.run_local_server(port=0)

                # Save the credentials
                with open(self.token_path, 'w') as token:
                    token.write(self.creds.to_json())
            except Exception as e:
                return None, f"Authentication failed: {str(e)}"

        self.service = build('gmail', 'v1', credentials=self.creds)
        return self.service, "Authenticated successfully"

    def get_recent_emails(self, max_results=10):
        """Fetches recent emails from the inbox."""
        if not self.service:
            return []

        try:
            results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
            messages = results.get('messages', [])

            email_list = []
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()

                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')

                # Get snippet
                snippet = msg.get('snippet', '')

                # Get body (simplified for now)
                body = ""
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body'].get('data')
                            if data:
                                body = base64.urlsafe_b64decode(data).decode()
                                break
                else:
                    data = msg['payload']['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode()

                email_list.append({
                    'id': message['id'],
                    'threadId': msg['threadId'],
                    'subject': subject,
                    'from': sender,
                    'snippet': snippet,
                    'body': body or snippet
                })

            return email_list
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def send_reply(self, to, subject, body, thread_id=None):
        """Sends an email reply."""
        if not self.service:
            return False, "Not authenticated"

        try:
            message = EmailMessage()
            message.set_content(body)
            message['To'] = to
            message['Subject'] = subject

            if thread_id:
                # To reply in a thread, we need to set the threadId and usually In-Reply-To/References
                # For simplicity, we'll just use threadId in the send call
                pass

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                'raw': encoded_message
            }
            if thread_id:
                create_message['threadId'] = thread_id

            send_message = self.service.users().messages().send(userId="me", body=create_message).execute()
            return True, f"Message sent! ID: {send_message['id']}"
        except HttpError as error:
            return False, f'An error occurred: {error}'

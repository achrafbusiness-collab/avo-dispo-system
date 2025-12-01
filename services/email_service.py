# app/services/email_service.py

import imaplib
import email
import json
import traceback
import os

from app.database import SessionLocal
from app.models import ImportedOrder
from app.services.ai_service import extract_with_ai  # <-- richtig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAP_CONFIG_FILE = os.path.join(BASE_DIR, "imap_config.json")


def load_imap_config():
    if not os.path.exists(IMAP_CONFIG_FILE):
        return {}
    try:
        with open(IMAP_CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def extract_plain_text_from_email(msg):
    try:
        if msg.is_multipart():
            parts = []
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        parts.append(part.get_payload(decode=True).decode(errors="ignore"))
                    except:
                        pass
            return "\n".join(parts).strip()
        else:
            return msg.get_payload(decode=True).decode(errors="ignore")
    except:
        return ""


def imap_login(mail_obj, user, password):
    try:
        mail_obj.login(user, password)
        return True
    except:
        return False


def test_imap_connection():
    config = load_imap_config()
    try:
        mail = imaplib.IMAP4_SSL(config["imap_host"], int(config["imap_port"]))
        ok = imap_login(mail, config["imap_user"], config["imap_pass"])
        mail.logout()

        if ok:
            return {"status": "success"}
        return {"status": "error", "message": "Login fehlgeschlagen"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def fetch_imports():
    config = load_imap_config()

    host = config.get("imap_host")
    user = config.get("imap_user")
    password = config.get("imap_pass")
    port = int(config.get("imap_port", 993))

    created = []

    try:
        mail = imaplib.IMAP4_SSL(host, port)
        if not imap_login(mail, user, password):
            return []

        mail.select("INBOX")
        status, data = mail.search(None, "UNSEEN")

        if status != "OK":
            return []

        db = SessionLocal()

        for num in data[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")

            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get("subject", "")
            sender = msg.get("from", "")
            date_ = msg.get("date", "")
            body = extract_plain_text_from_email(msg)

            parsed = extract_with_ai(body)  # <-- richtig

            new_imp = ImportedOrder(
                source_msg_id=num.decode(),
                subject=subject,
                sender=sender,
                received_at=date_,
                raw_text=body,
                **parsed
            )

            db.add(new_imp)
            db.commit()
            db.refresh(new_imp)

            created.append(new_imp.id)

        db.close()
        mail.logout()

        return created

    except Exception as e:
        traceback.print_exc()
        return []

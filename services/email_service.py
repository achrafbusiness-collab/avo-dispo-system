# app/services/email_service.py

import imaplib
import email
import json
import traceback
import os

from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.models import ImportedOrder
from app.services.ai_service import extract_order_data

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAP_CONFIG_FILE = os.path.join(BASE_DIR, "imap_config.json")


# ============================================================
# IMAP KONFIG LADEN
# ============================================================
def load_imap_config():
    if not os.path.exists(IMAP_CONFIG_FILE):
        return {}

    try:
        with open(IMAP_CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# ============================================================
# EMAIL → PLAIN TEXT EXTRAKTION
# ============================================================
def extract_plain_text_from_email(msg):
    """
    Holt den Text-Inhalt aus der E-Mail.
    Unterstützt multipart + encoding-fixes.
    """

    try:
        if msg.is_multipart():
            parts = []
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        txt = part.get_payload(decode=True).decode(errors="ignore")
                        parts.append(txt)
                    except:
                        pass
            return "\n".join(parts).strip()

        else:
            return msg.get_payload(decode=True).decode(errors="ignore")

    except:
        return ""


# ============================================================
# HAUPTFUNKTION: EMAILS ABRUFEN UND SPEICHERN
# ============================================================
def fetch_and_import_emails():
    """
    Holt alle ungelesenen Emails vom IMAP-Server,
    extrahiert die Daten und speichert sie als ImportedOrder.
    """

    config = load_imap_config()
    if not config:
        print("⚠️ Keine IMAP Konfiguration gefunden.")
        return

    host = config.get("host")
    username = config.get("username")
    password = config.get("password")
    mailbox = config.get("mailbox", "INBOX")

    if not host or not username or not password:
        print("⚠️ IMAP Zugangsdaten unvollständig.")
        return

    try:
        mail = imaplib.IMAP4_SSL(host)
        mail.login(username, password)
        mail.select(mailbox)
    except:
        print("❌ IMAP-Verbindung fehlgeschlagen.")
        traceback.print_exc()
        return

    try:
        result, data = mail.search(None, "UNSEEN")

        if result != "OK":
            print("⚠️ Keine ungelesenen Nachrichten gefunden.")
            return

        email_ids = data[0].split()

        for eid in email_ids:
            _, msg_data = mail.fetch(eid, "(RFC822)")

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg.get("Subject", "")
            sender = msg.get("From", "")
            text = extract_plain_text_from_email(msg)

            # KI / Regex Datenextraktion
            extracted = extract_order_data(text)

            # Datenbank speichern
            db = SessionLocal()

            imported = ImportedOrder(
                subject=subject,
                sender=sender,
                raw_text=text,
                mv_nr=extracted.get("mv_nr"),
                kennzeichen=extracted.get("kennzeichen"),
                modell=extracted.get("modell"),
                fin=extracted.get("fin"),
                abhol_stadt=extracted.get("abhol_stadt"),
                abhol_strasse=extracted.get("abhol_strasse"),
                abhol_plz=extracted.get("abhol_plz"),
                abhol_datum=extracted.get("abhol_datum"),
                anliefer_stadt=extracted.get("anliefer_stadt"),
                anliefer_strasse=extracted.get("anliefer_strasse"),
                anliefer_plz=extracted.get("anliefer_plz"),
                anliefer_datum=extracted.get("anliefer_datum"),
                infofeld=extracted.get("infofeld"),
            )

            db.add(imported)
            db.commit()
            db.close()

    except:
        print("❌ Fehler beim Abrufen der Emails.")
        traceback.print_exc()

    finally:
        try:
            mail.close()
            mail.logout()
        except:
            pass

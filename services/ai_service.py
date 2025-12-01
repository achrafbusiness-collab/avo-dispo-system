# app/services/ai_service.py

import json
import traceback
import os

try:
    import openai
except:
    openai = None

from app.config import OPENAI_API_KEY

if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


# ===============================
# KI-Feldextraktion
# ===============================

def extract_with_ai(email_text: str):
    """
    Nutzt OpenAI wenn verfügbar, sonst heuristische Extraktion.
    """

    template = {
        "mv_nr": None, "kennzeichen": None, "modell": None, "fin": None, "auftraggeber": None,
        "infofeld": None,
        "abhol_stadt": None, "abhol_strasse": None, "abhol_str_nr": None, "abhol_plz": None,
        "kontakt_abholung": None, "ap_abholung": None, "abholdatum": None, "abhol_von": None, "abhol_bis": None,
        "anliefer_stadt": None, "anliefer_strasse": None, "anliefer_str_nr": None, "anliefer_plz": None,
        "kontakt_anlieferung": None, "ap_anlieferung": None, "anlieferdatum": None, "anliefer_von": None, "anliefer_bis": None,
        "kilometer": None, "preis": None, "preis_selbstst": None,
        "fahrer_id": None
    }

    # ==========================
    # OpenAI Parsing
    # ==========================
    if OPENAI_API_KEY and openai:
        try:
            prompt = f"""
Extrahiere alle Auftragsdaten aus dieser E-Mail und gib sie als sauberes JSON zurück:

\"\"\"{email_text}\"\"\"
"""

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700
            )

            parsed = json.loads(response["choices"][0]["message"]["content"])

            for key in template.keys():
                template[key] = parsed.get(key)

            return template

        except Exception as e:
            traceback.print_exc()
            print("❌ AI Parsing fehlgeschlagen – nutze Heuristik")

    # ==========================
    # Heuristische Notfalllösung
    # ==========================
    lower = email_text.lower()

    if "kennzeichen" in lower:
        template["kennzeichen"] = email_text.split("Kennzeichen")[-1].split("\n")[0].strip()

    template["infofeld"] = "Automatisch extrahiert (Heuristik). Bitte prüfen."

    return template

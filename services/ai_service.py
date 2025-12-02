# app/services/ai_service.py

"""
AI-gestützte Extraktion von Auftragsdaten aus E-Mails.
Struktur:
1. Regelbasierte Vorverarbeitung
2. Mustererkennung (Regex)
3. KI-Fallback (optional / später aktivieren)
4. Heuristische Notlösung
"""

import re


# ============================================================
# Hauptfunktion: Extract aus Rohtext
# ============================================================
def extract_order_data(email_text: str) -> dict:
    """
    Extrahiert relevante Felder aus einem E-Mail-Text.
    Gibt ein strukturiertes Dictionary zurück.
    """

    template = {
        "mv_nr": None,
        "kennzeichen": None,
        "modell": None,
        "fin": None,

        "abhol_stadt": None,
        "abhol_strasse": None,
        "abhol_plz": None,
        "abhol_datum": None,

        "anliefer_stadt": None,
        "anliefer_strasse": None,
        "anliefer_plz": None,
        "anliefer_datum": None,

        "infofeld": "",
    }

    text = email_text.replace("\r", "").strip()


    # ========================================================
    # 1) MV / Auftrag / Referenznummer
    # ========================================================
    mv_match = re.search(r"(MV|Mv|mv)[-:\s]*([A-Za-z0-9]+)", text)
    if mv_match:
        template["mv_nr"] = mv_match.group(2).strip()


    # ========================================================
    # 2) Kennzeichen
    # ========================================================
    kenn_match = re.search(r"Kennzeichen[:\s]*([A-Z]{1,3}\s*[A-Z0-9]{1,4})", text)
    if kenn_match:
        template["kennzeichen"] = kenn_match.group(1).strip()


    # ========================================================
    # 3) FIN
    # ========================================================
    fin_match = re.search(r"(FIN|Vin|Fahrgestellnummer)[:\s]*([A-HJ-NPR-Z0-9]{11,17})", text)
    if fin_match:
        template["fin"] = fin_match.group(2).strip()


    # ========================================================
    # 4) Modell / Fahrzeugtyp
    # ========================================================
    model_match = re.search(r"Modell[:\s]*(.+)", text)
    if model_match:
        template["modell"] = model_match.group(1).split("\n")[0].strip()


    # ========================================================
    # 5) Adressen (extrem vereinfacht – später KI)
    # ========================================================
    city_match = re.search(r"(\d{5})\s+([A-Za-zäöüÄÖÜß\s]+)", text)
    if city_match:
        template["abhol_plz"] = city_match.group(1)
        template["abhol_stadt"] = city_match.group(2).strip()


    # ========================================================
    # 6) Datumsangaben
    # ========================================================
    date_match = re.search(r"(\d{1,2}\.\d{1,2}\.\d{2,4})", text)
    if date_match:
        template["abhol_datum"] = date_match.group(1)


    # ========================================================
    # 7) KI-Fallback – vorbereitet, aber noch nicht aktiv
    # ========================================================
    # TODO: später aktivieren
    # ai_result = call_ai_model(email_text)
    # template = merge_ai_result(template, ai_result)


    # ========================================================
    # 8) Heuristische Notlösung
    # ========================================================
    lower = text.lower()

    if not template["kennzeichen"] and "kennzeichen" in lower:
        try:
            template["kennzeichen"] = text.split("Kennzeichen")[-1].split("\n")[0].strip()
        except:
            pass

    template["infofeld"] = "Automatisch extrahiert. Bitte prüfen."

    return template

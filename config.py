# app/config.py

import os

# OpenAI API Key aus Umgebungsvariablen lesen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

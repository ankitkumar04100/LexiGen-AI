# backend/models/legal_simplifier.py
"""
Mock AI helpers for LexiGen AI prototype.
Replace the implementations with real Google Cloud / PaLM / Vertex integrations.
"""

import os
from gtts import gTTS  # pip install gTTS

def summarize_document(text: str) -> str:
    """
    Mock summarizer. Replace with LLM call to PaLM/Gemini for production.
    """
    if not text:
        return "No text available to summarize."
    # Very simple heuristic summary for demo:
    lines = text.strip().splitlines()
    short = " ".join(lines[:3])  # demo
    return f"Summary: {short} ... (This is a demo summary — replace with real LLM.)"

def extract_clauses(text: str):
    """
    Very naive clause splitter for demo. Replace with structured parsing / Document AI.
    """
    if not text:
        return []
    # Split on periods (demo)
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    clauses = []
    for i, s in enumerate(sentences[:10]):
        clauses.append({
            "clause_id": i+1,
            "original": s[:800],
            "simplified": f"(Demo) {s[:120]}... simplified explanation.",
            "risk": "⚠️" if "penal" in s.lower() or "fine" in s.lower() else "✅"
        })
    return clauses

def answer_question(text: str, query: str) -> str:
    """
    Mock QA. Replace with an LLM QA chain on the document.
    """
    # Demo responses based on keywords
    q = query.lower()
    if "evict" in q or "eviction" in q:
        return "⚠️ Usually the landlord needs to provide notice before eviction. (Demo answer)"
    if "deposit" in q:
        return "✅ Deposit rules vary. Check the deposit clause in the contract. (Demo answer)"
    return f"(Demo) I searched the document for: '{query}'. Replace this with an LLM answer."

def translate_text(text: str, language_code: str) -> str:
    """
    Mock translation. Replace with real translation API or LLM call.
    """
    return f"(Demo translation to {language_code}) {text[:200]}..."

def synthesize_speech(text: str, doc_id: str) -> str:
    """
    Create an mp3 file using gTTS for demo. In production, use a cloud TTS (higher quality).
    Returns path to file.
    """
    if not text:
        text = "No text to speak."
    audio_dir = os.path.join(os.path.dirname(__file__), "..", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    filename = os.path.join(audio_dir, f"{doc_id}.mp3")
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

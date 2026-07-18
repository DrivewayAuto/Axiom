"""Axiom web app - phone-friendly chat interface.

Run locally:   python web.py          (then open http://localhost:5000)
Run hosted:    gunicorn web:app       (what Render/Railway use)
"""
import os
from flask import Flask, request, jsonify, render_template
from axiom.brain import Brain
from axiom.memory import Memory

app = Flask(__name__, template_folder="templates")
brain = Brain()
memory = Memory()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    text = (request.json or {}).get("message", "").strip()
    if not text:
        return jsonify({"reply": "Say something and I'll get to work."})
    try:
        reply = brain.think(text, memory)
        memory.log_turn("user", text)
        memory.log_turn("assistant", reply)
    except Exception as e:
        reply = f"Hit a snag: {e}"
    return jsonify({"reply": reply})


@app.route("/health")
def health():
    return jsonify({"ok": True, "full_brain": brain.client is not None})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)

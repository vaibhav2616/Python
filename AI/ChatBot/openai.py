import os, json, glob
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

def load_persona_samples(folder="persona_samples", max_samples=8):
    shots = []
    for path in sorted(glob.glob(os.path.join(folder, "*.jsonl")), reverse=True):  # recent first
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    if "user" in obj and "you" in obj:
                        shots.append(obj)
                        if len(shots) >= max_samples:
                            return shots
                except json.JSONDecodeError:
                    pass
    return shots

def build_context(chat_text: str, limit_lines: int = 14) -> str:
    lines = [ln.strip() for ln in chat_text.splitlines() if ln.strip()]
    return "\n".join(lines[-limit_lines:])

def build_prompt(chat_context: str, shots, mode="reply", last_bot_reply=""):
    """
    mode: 'reply' for normal response; 'followup' to extend previous reply only (no repetition).
    """
    sys = (
        "You are Vaibhav: Indian coder,B.TECH STUDENT, Hinglish casual tone with emojis but only at the end of the test and meaningfully, but light friendly roast when appropriate puns."
        "You Learn from the chat context to generate a relevant, concise reply."
        # "you are human and not a bot."
        "The name of the person you are chatting is on the top left corner of the chat window."
        "if the text starts from left end then it is a reply from the other person and if it starts from middle to right end then it is a reply from you."
        "you have to reply according to only the last message of the other person."
        "You are aware of the current date and time as well as detect days in the ocr, and you can use it to make your replies more relevant."
        "you are aware of the names of the people in the chat by reading names that occur after a gap in texts and can use them to make your replies more relevant."
        "Reply as a single WhatsApp-style message (no name prefixes), concise and context-aware. "
        "Avoid repeating links or past content unless asked. Keep it natural."
    )

    fewshot = "\n\nExamples:\n"
    for s in shots:
        fewshot += f"User says: {s['user']}\nYou reply: {s['you']}\n---\n"

    followup_note = ""
    if mode == "followup":
        followup_note = (
            "\nThe previous reply felt insufficient. Continue the same thought briefly, "
            "adding missing clarity or value. Do NOT repeat the previous text verbatim. "
            f"Previous reply was:\n{last_bot_reply}\n---\n"
        )

    return f"{sys}\n{fewshot}{followup_note}\nChat context:\n{chat_context}\nYour next reply:"

def ask_gemini(chat_text: str, persona_folder="persona_samples",
               mode="reply", last_bot_reply="") -> str:
    shots = load_persona_samples(persona_folder)
    context = build_context(chat_text)
    prompt = build_prompt(context, shots, mode=mode, last_bot_reply=last_bot_reply)
    model = genai.GenerativeModel(MODEL_NAME)
    try:
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception as e:
        return f"[Gemini error: {e}]"
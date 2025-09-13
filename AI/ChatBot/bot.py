import os, time, hashlib
import json
import pyautogui, pyperclip, keyboard
import pytesseract, cv2, numpy as np
from dotenv import load_dotenv
from get_cursor import load_region
from openai import ask_gemini

load_dotenv()

# ===== Hotkeys =====
TRIGGER_NEW = "ctrl+alt+space"           # Generate a new reply suggestion
TRIGGER_SUPP = "ctrl+alt+shift+space"     # Generate a follow-up (supplement) to last reply
ACCEPT_HK    = "ctrl+alt+r"               # Accept suggestion (type it)
EDIT_HK      = "ctrl+alt+e"               # Edit before sending
REJECT_HK    = "ctrl+alt+n"               # Reject suggestion

# ===== Your name to avoid self-replies if needed (heuristic only) =====
YOU_NAME = "Vaibhav"

# ===== Optional: Tesseract path (Windows) =====
# Put path in .env as TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
tesseract_path = os.getenv("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

# ===== State =====
last_suggestion = None
awaiting_decision = False
current_mode = "new"  # or "supplement"

def preprocess_for_ocr(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 7, 50, 50)
    thr = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 9)
    return thr

def grab_chat_text(region):
    x, y, w, h = region
    shot = pyautogui.screenshot(region=(x, y, w, h))
    bgr = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
    thr = preprocess_for_ocr(bgr)
    text = pytesseract.image_to_string(thr, lang="eng", config="--psm 6")
    # light cleanup
    return "\n".join([ln.rstrip() for ln in text.splitlines() if ln.strip()])

def stable_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()

def show_toast_in_console(s, prefix="[SUGGESTION] "):
    # Console toast + short beep so you don't need to leave the chat app
    try:
        import winsound
        winsound.Beep(900, 120)
    except Exception:
        pass
    print(f"\n{prefix}{s}\n")
    print(f"Press  {ACCEPT_HK} to Accept,  {EDIT_HK} to Edit,  {REJECT_HK} to Reject.")

def paste_and_optionally_send(input_box, text, auto_send):
    pyperclip.copy(text)
    if input_box:
        pyautogui.click(input_box["x"], input_box["y"])
        time.sleep(0.15)
    pyautogui.hotkey("ctrl", "v")
    if auto_send:
        time.sleep(0.1)
        pyautogui.press("enter")

def trigger_generation(mode="new"):
    global last_suggestion, awaiting_decision, current_mode
    region, input_box, auto_send, _screen = load_region()
    current_mode = mode

    print(f"[INFO] Triggered ({mode}). OCR-ing region {region}...")
    chat_text = grab_chat_text(region)
    if not chat_text:
        show_toast_in_console("⚠️ No text detected in region. Recheck region.json.", prefix="[WARN] ")
        return

    print("[INFO] Asking Gemini for suggestion...")
    try:
        suggestion = ask_gemini(chat_text, mode=mode)
    except Exception as e:
        show_toast_in_console(f"API error: {e}", prefix="[ERROR] ")
        return

    if not suggestion:
        show_toast_in_console("No suggestion generated.", prefix="[INFO] ")
        return

    last_suggestion = suggestion.strip()
    awaiting_decision = True
    show_toast_in_console(last_suggestion)

def on_accept():
    global last_suggestion, awaiting_decision
    if not awaiting_decision or not last_suggestion:
        print("[INFO] No pending suggestion.")
        return
    region, input_box, auto_send, _ = load_region()
    paste_and_optionally_send(input_box, last_suggestion, auto_send)
    print("[INFO] Accepted. (Pasted" + (" + sent)" if auto_send else ".)"))
    awaiting_decision = False

def on_edit():
    global last_suggestion, awaiting_decision
    if not awaiting_decision or not last_suggestion:
        print("[INFO] No pending suggestion.")
        return
    try:
        # Simple console edit: you stay in chat app; press EDIT_HK, then alt+tab to console if needed.
        # If you prefer a GUI prompt, replace with tkinter.simpledialog.askstring
        print("\n[EDIT] Current suggestion:\n", last_suggestion)
        new_text = input("\nType your edited message (leave blank to cancel): ").strip()
        if not new_text:
            print("[INFO] Edit cancelled.")
            return
        region, input_box, auto_send, _ = load_region()
        paste_and_optionally_send(input_box, new_text, auto_send)
        print("[INFO] Edited message pasted" + (" and sent." if auto_send else "."))
        awaiting_decision = False
    except KeyboardInterrupt:
        print("\n[INFO] Edit cancelled.")

def on_reject():
    global last_suggestion, awaiting_decision
    if not awaiting_decision:
        print("[INFO] Nothing to reject.")
        return
    print("[INFO] Suggestion rejected.")
    awaiting_decision = False
    last_suggestion = None

def main():
    print(f"[READY] Press {TRIGGER_NEW} to suggest reply. Press {TRIGGER_SUPP} to add a follow-up.")
    print(f"[READY] Then use: {ACCEPT_HK}=Accept  {EDIT_HK}=Edit  {REJECT_HK}=Reject")
    print("[NOTE] No typing will happen until you accept. Uses region.json for chat area & input box.\n")

    keyboard.add_hotkey(TRIGGER_NEW, lambda: trigger_generation("new"))
    keyboard.add_hotkey(TRIGGER_SUPP, lambda: trigger_generation("supplement"))
    keyboard.add_hotkey(ACCEPT_HK, on_accept)
    keyboard.add_hotkey(EDIT_HK, on_edit)
    keyboard.add_hotkey(REJECT_HK, on_reject)

    try:
        while True:
            time.sleep(0.1)  # idle; no heavy loop
    except KeyboardInterrupt:
        print("\n[EXIT] Stopped.")

if __name__ == "__main__":
    main()
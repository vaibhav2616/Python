# get_cursor.py
import json
import time
import pyautogui
import keyboard
import os
import sys

CONFIG_FILE = "region.json"

def capture_point(hotkey, description):
    """Wait for the user to press the given hotkey and capture mouse position."""
    print(f"➡ Hover over {description} and press {hotkey} to capture...")
    while True:
        try:
            if keyboard.is_pressed(hotkey.lower()):
                time.sleep(0.25)  # debounce
                x, y = pyautogui.position()
                print(f"✅ Captured {description}: ({x}, {y})")
                return x, y
        except Exception:
            print("⚠ Keyboard hook failed. Try running as Administrator.")
            sys.exit(1)
        time.sleep(0.05)

def load_region():
    """Load region configuration from file."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Region config '{CONFIG_FILE}' not found. Run get_cursor.py first.")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    
    region_dict = cfg.get("region", {})
    x1, y1, x2, y2 = region_dict["x1"], region_dict["y1"], region_dict["x2"], region_dict["y2"]
    region_tuple = (x1, y1, x2 - x1, y2 - y1)  # convert to (x, y, width, height)
    
    input_box = cfg.get("input_box", None)
    auto_send = cfg.get("auto_send", False)
    screen = cfg.get("screen", {})
    
    return region_tuple, input_box, auto_send, screen

def main():
    print("=== Region Selector ===")
    print("[F8]  Top-left of chat area")
    print("[F9]  Bottom-right of chat area")
    print("[F10] (Optional) Input box position")
    print("[Esc] Save & Exit\n")

    tl = capture_point('F8', 'TOP-LEFT of chat area')
    br = capture_point('F9', 'BOTTOM-RIGHT of chat area')

    if br[0] <= tl[0] or br[1] <= tl[1]:
        print("❌ Invalid rectangle. Bottom-right must be greater than top-left.")
        return

    input_box = None
    print("Press [F10] to capture input box position, or [Esc] to skip.")
    while True:
        if keyboard.is_pressed('f10'):
            time.sleep(0.25)
            input_box = pyautogui.position()
            print(f"✅ Captured input box: {input_box}")
            break
        if keyboard.is_pressed('esc'):
            print("ℹ Skipping input box capture.")
            time.sleep(0.25)
            break
        time.sleep(0.05)

    screen_w, screen_h = pyautogui.size()
    config = {
        "region": {"x1": tl[0], "y1": tl[1], "x2": br[0], "y2": br[1]},
        "screen": {"width": screen_w, "height": screen_h},
        "input_box": {"x": input_box[0], "y": input_box[1]} if input_box else None,
        "auto_send": False
    }

    print("\n📄 Preview config:")
    print(json.dumps(config, indent=2))

    confirm = input("💾 Save this config to region.json? (y/N): ").strip().lower()
    if confirm == 'y':
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print(f"✅ Saved {CONFIG_FILE}")
    else:
        print("❎ Not saved.")

if __name__ == "__main__":
    os.system('')  # enable ANSI on Windows terminal
    main()
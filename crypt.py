import engine
import sys
import os
import string
import datetime
from typing import List, Dict, Callable, NamedTuple, Optional, Any

# Constants
ALPHABET_LATIN = list(string.ascii_uppercase)
ALPHABET_SPANISH = list(string.ascii_uppercase + "Ñ")
ALPHABET_FRENCH = list(string.ascii_uppercase + "ÀÂÆÇÉÈÊËÎÏÔŒÙÛÜŸ")

# Command Pattern Structure
class MenuAction(NamedTuple):
    label: str
    handler: Callable[[], None]

# State variables
current_data = {
    "name": "Unnamed Project",
    "entries": [],
    "alphabet": ALPHABET_LATIN, 
    "shift": 1
}

def get_active_msg() -> str:
    if current_data["entries"]:
        return current_data["entries"][-1].get("result", "")
    return ""

def get_active_status() -> str:
    if current_data["entries"]:
        return current_data["entries"][-1].get("status", "RAW")
    return "RAW"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("[Press Enter]")

def add_history_entry(msg: str, result: str, status: str, keys: List[str] = None, mapping: List[Dict] = None):
    entry = {
        "msg": msg,
        "result": result,
        "keys": keys or [],
        "mapping": mapping or [],
        "status": status,
        "timestamp": datetime.datetime.now().isoformat()
    }
    current_data["entries"].append(entry)

def print_box(lines: List[str], title: str = "MENU"):
    """Draws an ASCII box around a list of text lines."""
    width = 60
    print("+" + "=" * width + "+")
    if title:
        padding_total = width - len(title) - 2
        padding_left = padding_total // 2
        print("|" + " " * padding_left + f"{title}" + " " * (padding_total - padding_left) + "|")
        print("+" + "-" * width + "+")
    
    for line in lines:
        print(f"| {line:<{width-2}} |")
    
    print("+" + "=" * width + "+")

def set_message():
    print("\n[ EDIT MESSAGE ]")
    print("Type a message or 'import' to load text file.")
    
    # Auto-detect msg.txt
    if os.path.exists("msg.txt"):
        print(">> Found standard file 'msg.txt'.")
        choice = input(">> Import content from 'msg.txt'? (y/n): ").strip().lower()
        if choice == 'y':
            try:
                with open("msg.txt", 'r', encoding='utf-8') as f:
                    msg = f.read().strip()
                add_history_entry(msg, msg, "RAW")
                print(f">> Imported {len(msg)} chars.")
                pause()
                return
            except Exception as e:
                print(f"!! Error importing msg.txt: {e}")
    
    msg = input("Enter message: ").strip()
    
    if msg.lower() == 'import':
        filename = input("Enter filename (e.g. msg.txt): ").strip()
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    msg = f.read().strip()
                print(f">> Imported {len(msg)} chars from {filename}")
            except Exception as e:
                print(f"!! Error: {e}")
                pause()
                return
        else:
            print(f"!! File not found: {filename}")
            pause()
            return

    add_history_entry(msg, msg, "RAW")
    print(f">> Added new entry to Project.")
    pause()

def save_project():
    print("\n[ SAVE PROJECT ]")
    filename = input("Enter project name (e.g. secret_ops.json): ").strip()
    if not filename: return
    
    if engine.save_session_json(current_data, filename):
        print(f">> Project saved to vault/{filename}")
    pause()

def load_project():
    print("\n[ OPEN PROJECT ]")
    vault_dir = os.path.join(os.path.dirname(__file__), 'vault')
    if os.path.exists(vault_dir):
        files = [f for f in os.listdir(vault_dir) if f.endswith('.json')]
        if files:
            print("Available Projects:")
            for f in files:
                print(f" - {f}")
        else:
            print("(No projects found in vault)")
    
    filename = input("Enter project name (e.g. secret_ops.json): ").strip()
    if not filename: return
    
    data = engine.load_session_json(filename)
    if data:
        current_data.update(data)
        print(f">> Project loaded from vault/{filename}")
    pause()

def run_encryption():
    active_msg = get_active_msg()
    if not active_msg:
        print("!! Error: No active message in project history. Create one first.")
        pause()
        return
    
    print("\n[ ENCRYPTION ]")
    print(f"Encrypting: {active_msg[:30]}...")
    
    encrypted_text, used_keys, mapping = engine.encrypt_sentence_otp(
        active_msg, 
        current_data["alphabet"], 
        current_data["shift"]
    )
    
    add_history_entry(active_msg, encrypted_text, "ENCODED", used_keys, mapping)
    
    print(f">> Result: {encrypted_text}")
    print("\n>> Entry added to Project history.")
    
    # Prompt to save standard files
    save_std = input("Save to standard files (cipher.txt, keys.txt)? (y/n): ").strip().lower()
    if save_std == 'y':
        engine.save_text(encrypted_text, "cipher.txt")
        engine.save_keys(used_keys, "keys.txt")
        print(">> Saved to cipher.txt and keys.txt")

    save = input("Save Project (JSON) now? (y/n): ").strip().lower()
    if save == 'y':
        save_project()
    else:
        pause()

def run_decryption():
    active_entry = current_data["entries"][-1] if current_data["entries"] else None
    
    if not active_entry:
        # If project is empty, look for files
        for std_file in ["cipher.txt", "msg.txt"]:
            if os.path.exists(std_file):
                print(f">> Found standard file '{std_file}'.")
                choice = input(f">> Import as active entry? (y/n): ").strip().lower()
                if choice == 'y':
                    try:
                        with open(std_file, 'r', encoding='utf-8') as f:
                            add_history_entry("", f.read().strip(), "RAW")
                        print(f">> Imported from {std_file}.")
                        active_entry = current_data["entries"][-1]
                        break
                    except Exception as e:
                        print(f"!! Error: {e}")

    if not active_entry or not active_entry["result"]:
         print("!! Error: No active ciphertext (result) in project.")
         pause()
         return

    ciphertext = active_entry["result"]
    print("\n[ DECRYPTION ]")
    
    # Check for internal keys in the active entry
    keys = active_entry["keys"]
    if keys:
        print(f">> Found {len(keys)} keys associated with this entry.")
    else:
        print("!! No keys associated with this entry.")
        
        # Auto-detect keys.txt
        if os.path.exists("keys.txt"):
             print(">> Found standard file 'keys.txt'.")
             choice = input(">> Import keys from 'keys.txt'? (y/n): ").strip().lower()
             if choice == 'y':
                 keys = engine.load_keys("keys.txt")
                 if keys:
                    print(f">> Imported {len(keys)} keys.")
                 else:
                    print("!! Failed to load keys.")
        
        if not keys:
            choice = input("Import keys from external file manually? (y/n): ").strip().lower()
            if choice == 'y':
                filename = input("Filename (e.g. keys.txt): ").strip()
                if os.path.exists(filename):
                    keys = engine.load_keys(filename)
                    print(f">> Imported {len(keys)} keys.")
                else:
                    print("!! File not found.")
                    pause()
                    return
            else:
                pause()
                return

    try:
        decrypted_text, mapping = engine.decrypt_sentence(
            ciphertext, 
            keys, 
            current_data["alphabet"], 
            current_data["shift"]
        )
        
        add_history_entry(ciphertext, decrypted_text, "DECODED", keys, mapping)
        
        print(f">> Result: {decrypted_text}")
        print("\n>> Entry added to Project history.")
        
        # Prompt to save standard file
        save_std = input("Save result to msg.txt? (y/n): ").strip().lower()
        if save_std == 'y':
            engine.save_text(decrypted_text, "msg.txt")
            print(">> Saved to msg.txt")

        save = input("Save Project (JSON) now? (y/n): ").strip().lower()
        if save == 'y':
            save_project()
        else:
            pause()
                    
    except Exception as e:
        print(f"!! Decryption failed: {e}")
        pause()

# OPTIONS MENU FUNCTIONS
def set_language():
    while True:
        clear_screen()
        print_box([
            "1. Latin (A-Z)",
            "2. Spanish (A-Z + Ñ)",
            "3. French (A-Z + Accents)",
            "4. Custom",
            "0. Back"
        ], "SET LANGUAGE")
        
        current_str = "".join(current_data["alphabet"])
        current_disp = current_str if len(current_str) < 40 else current_str[:37] + "..."
        print(f"Current: {current_disp}")
        
        choice = input("\nSelect > ").strip()
        
        if choice == '1':
            current_data["alphabet"] = ALPHABET_LATIN
            print(">> Set to Latin.")
            pause()
            break
        elif choice == '2':
            current_data["alphabet"] = ALPHABET_SPANISH
            print(">> Set to Spanish.")
            pause()
            break
        elif choice == '3':
            current_data["alphabet"] = ALPHABET_FRENCH
            print(">> Set to French.")
            pause()
            break
        elif choice == '4':
            new_alpha = input("Enter new alphabet string (e.g. ABC): ").strip()
            if not new_alpha:
                print("!! Invalid input.")
                pause()
                continue
            
            # Duplicate check
            if len(set(new_alpha)) != len(new_alpha):
                print("!! Error: Alphabet contains duplicate characters.")
                pause()
                continue
                
            current_data["alphabet"] = list(new_alpha)
            print(">> Custom Alphabet updated.")
            pause()
            break
        elif choice == '0':
            break
        else:
            print("Invalid choice.")
            pause()

def set_shift():
    print("\n[ SET SHIFT ]")
    print(f"Current: {current_data['shift']}")
    try:
        val_str = input("Enter integer shift: ").strip()
        if not val_str: return
        val = int(val_str)
        current_data["shift"] = val
        print(">> Shift updated.")
    except ValueError:
        print("!! Invalid integer.")
    input("[Press Enter]")

def reset_defaults():
    current_data["alphabet"] = ALPHABET_LATIN
    current_data["shift"] = 1
    print(">> Defaults restored (Latin, Shift 1).")
    input("[Press Enter]")

def menu_options():
    while True:
        clear_screen()
        lines = [
            "1. Set Language / Alphabet",
            "2. Set Table Shift",
            "3. Reset to Defaults",
            "0. Back"
        ]
        print_box(lines, "SETTINGS")
        # Show Current Settings
        alpha_str = "".join(current_data["alphabet"])
        alpha_disp = alpha_str if len(alpha_str) < 20 else alpha_str[:17] + "..."
        print(f"  Shift: {current_data['shift']}")
        print(f"  Alphabet: {alpha_disp}")
        
        choice = input("\nSelect > ").strip()
        if choice == '1': set_language()
        elif choice == '2': set_shift()
        elif choice == '3': reset_defaults()
        elif choice == '0': break
        else: 
            print("Invalid choice.")
            pause()

def view_state():
    clear_screen()
    print_box([f"Project: {current_data['name']}"], "PROJECT INFO")
    
    if not current_data["entries"]:
        print("  (No history entries found)")
    else:
        history_lines = []
        for i, entry in enumerate(current_data["entries"]):
            ts = entry.get("timestamp", "N/A")[:19].replace("T", " ")
            stat = entry.get("status", "RAW")
            res = entry.get("result", "")
            if len(res) > 30: res = res[:27] + "..."
            history_lines.append(f"[{i:02}] {ts} | {stat:<7} | {res}")
        
        print("\n--- Entry History ---")
        for line in history_lines:
            print(f"  {line}")
        
        # Show details of the most recent entry if requested
        print("\nOptions: [Index] View Mapping, [Enter] Back")
        idx_str = input("Select > ").strip()
        if idx_str.isdigit():
            idx = int(idx_str)
            if 0 <= idx < len(current_data["entries"]):
                entry = current_data["entries"][idx]
                clear_screen()
                mapping = entry.get("mapping", [])
                map_lines = []
                for m in mapping:
                    orig = m.get("original", "")
                    res = m.get("result", "")
                    key = m.get("key", "None") or "None"
                    m_type = m.get("type", "SEP")
                    map_lines.append(f"{m_type:<4} | {orig:<8} -> {res:<8} | Key: {key}")
                
                print_box(map_lines, f"ENTRY {idx} MAPPING")
                pause()
    
    pause()

def shutdown():
    print("Shutting Down...")
    sys.exit()

# Main Menu Dispatch Table
# Map key -> MenuAction
MAIN_MENU: Dict[str, MenuAction] = {
    "1": MenuAction("Edit Message", set_message),
    "2": MenuAction("Open Project (JSON)", load_project),
    "3": MenuAction("Save Project (JSON)", save_project),
    "4": MenuAction("Encrypt", run_encryption),
    "5": MenuAction("Decrypt", run_decryption),
    "6": MenuAction("Settings", menu_options),
    "7": MenuAction("View Project Details", view_state),
    "0": MenuAction("Exit", shutdown)
}

def main():
    while True:
        clear_screen()
        active_msg = get_active_msg()
        active_status = get_active_status()
        
        # Generate Menu Lines dynamically
        menu_items = []
        # Sort keys to ensure order 1..7, 0
        sorted_keys = sorted([k for k in MAIN_MENU.keys() if k != '0']) + ['0']
        
        for key in sorted_keys:
            action = MAIN_MENU[key]
            menu_items.append(f"{key}. {action.label}")
        
        # Draw Menu
        print_box(menu_items, "CRYPT MENU")
        
        preview = active_msg
        if len(preview) > 30: 
            preview = preview[:27] + "..."
        elif not preview:
            preview = "(none)"

        print(f"\n  Project Status: {active_status}")
        print(f"  Active Result: {preview}")
        
        choice = input("\nSelect > ").strip()
        
        if choice in MAIN_MENU:
            handler = MAIN_MENU[choice].handler
            handler()
        else:
            print("Invalid choice.")
            pause()

if __name__ == "__main__":
    main()

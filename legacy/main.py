TRACE = False

def trace(msg):
    if TRACE:
        print(f"[TRACE] {msg}")

def build_table():
    """
    Builds the Vigenère table (26x26).
    """
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] # lines the top and left columns of table
    array = alphabet[::] # copy from the table header
    table = []
    for i in range(26):
        table.append(array[::]) # add a copy of the current array each iteration
        popped = array.pop(0) # remove the first letter in the array
        array.append(popped) # then add first letter to the end
    return table

def encrypt(msg, key, table):
    """
    Encrypts a message using a key and the Vigenère table.
    """
    result = "" # start with an empty string
    cords = []
    for idx in range(len(msg)): # we use range to iterate per letter in msg
        key_i = idx % len(key) # map the msg index to the key index, starting over at len(key)
        row = ord(key[key_i]) - ord('A') # we subtract the unicode value of the letter to retrieve the table position
        col = ord(msg[idx]) - ord('A')
        result += table[row][col] # we add the letter from the table to our result 
        cords.append(f"key Unicode: {ord(key[key_i]), key[key_i]} at X: {row}")
        cords.append(f"msg Unicode: {ord(msg[idx]), msg[idx]} at Y: {col}")
    return result, cords

def decrypt(msg, key, table):
    """
    Decrypts a message using a key and the Vigenère table.
    """
    result = ""
    cords = []
    for idx in range(len(msg)):
        key_i = idx % len(key) # get key index for table row 
        row = ord(key[key_i]) - ord("A") 
        col = table[row].index(msg[idx]) # find the letter inside the table with the key[] cycle and msg[]
        cipher = chr(col + ord('A')) # chr is the opposite of ord, gives the letter of unicode
        cords.append(f"key Unicode: {ord(key[key_i]), key[key_i]} at X: {row}")
        cords.append(f"msg Unicode: {ord(msg[idx]), msg[idx]} at Y: {col}")
        result += cipher
    return result, cords

# State variables
current_data = {
    "msg": "",
    "key": "",
    "encrypted": "",
    "decrypted": "",
    "table": build_table()
}

def set_message():
    """Input the message to process."""
    msg = input("Enter message: ").strip().upper()
    current_data["msg"] = msg
    trace(f"Message set to: {msg}")
    print(f"Message updated to: {msg}")

def set_key():
    """Input the encryption key."""
    key = input("Enter key: ").strip().upper()
    current_data["key"] = key
    trace(f"Key set to: {key}")
    print(f"Key updated to: {key}")

def run_encryption():
    """Run encryption on current msg and key."""
    if not current_data["msg"] or not current_data["key"]:
        print("Error: Both message and key must be set.")
        return
    res, _ = encrypt(current_data["msg"], current_data["key"], current_data["table"])
    current_data["encrypted"] = res
    print(f"Encryption Result: {res}")

def run_decryption():
    """Run decryption on current message (as ciphertext) and key."""
    if not current_data["msg"] or not current_data["key"]:
        print("Error: Both message and key must be set.")
        return
    res, _ = decrypt(current_data["msg"], current_data["key"], current_data["table"])
    current_data["decrypted"] = res
    print(f"Decryption Result: {res}")

def view_state():
    """Display the current state of variables."""
    print("\n=== Current State ===")
    print(f"Message:   {current_data['msg']}")
    print(f"Key:       {current_data['key']}")
    print(f"Encrypted: {current_data['encrypted']}")
    print(f"Decrypted: {current_data['decrypted']}")

def toggle_trace():
    """Toggle debug trace messages."""
    global TRACE
    TRACE = not TRACE
    state = "ON" if TRACE else "OFF"
    print(f"Trace mode is now {state}.")

def shutdown():
    """Exit the program."""
    print("Shutting Down...")
    return False

def print_menu():
    """Display the menu options."""
    print("\n=== Crypt Menu ===")
    for key, label, _ in menu:
        print(f"[{key}] {label}")
    print("=== Select an action ===")

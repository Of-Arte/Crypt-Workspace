import random
import string
from collections import deque
import re
import os
import json
from typing import List, Optional, Tuple, Dict, Any

def build_table(alphabet: Optional[List[str]] = None, shift: int = 1) -> List[List[str]]:
    """
    Makes a Vigenère “table”: rows match alphabet length, shifted left 'shift' times each row.
    """
    if alphabet is None:
        alphabet = list(string.ascii_uppercase)
    
    array = list(alphabet)[:]
    table = []
    # Table height matches alphabet length
    for i in range(len(alphabet)):
        table.append(array[:])
        # Shift the array 'shift' times
        for _ in range(shift):
            array.append(array.pop(0))
    return table

def random_key(length: int, alphabet: Optional[str] = None) -> str:
    """
    Generates a random key from the given alphabet with the specified length.
    """
    if alphabet is None:
        alphabet = string.ascii_uppercase
    return ''.join(random.choices(alphabet, k=length))

def pad_key(key: str, length: int, alphabet: Optional[str] = None) -> str:
    """
    Makes the key as long as the word, filling with random letters if needed.
    This prevents a short key from being a repeat/weakness.
    """
    if alphabet is None:
        alphabet = string.ascii_uppercase
    # Pads key with random letters from alphabet to reach 'length'
    if len(key) >= length:
        return key
    extra = ''.join(random.choices(alphabet, k=length - len(key)))
    return key + extra

def encrypt_word(word: str, key: str, table: List[List[str]], alphabet: List[str]) -> Tuple[str, str]:
    """
    Encrypts each letter using the Vigenère table while preserving the original casing.
    """
    result = ""
    # Store original cases
    cases = [c.isupper() for c in word]
    
    # Work with upper version for table lookup
    word_u = word.upper()
    key_u = pad_key(key, len(word), alphabet).upper()

    for i in range(len(word)):
        if word_u[i] not in alphabet or key_u[i] not in alphabet:
            result += word[i]
            continue
            
        row = alphabet.index(key_u[i])
        col = alphabet.index(word_u[i])
        res_char = table[row][col]
        
        # Map back to original case
        result += res_char if cases[i] else res_char.lower()
        
    return result, key_u

def decrypt_word(coded: str, key: str, table: List[List[str]], alphabet: List[str]) -> str:
    """
    Decrypts while preserving the original casing of the ciphertext.
    """
    result = ""
    cases = [c.isupper() for c in coded]
    coded_u = coded.upper()
    key_u = pad_key(key, len(coded), alphabet).upper()

    for i in range(len(coded)):
        if coded_u[i] not in alphabet or key_u[i] not in alphabet:
            result += coded[i]
            continue
            
        row = alphabet.index(key_u[i])
        if coded_u[i] in table[row]:
            col = table[row].index(coded_u[i])
            res_char = alphabet[col]
            result += res_char if cases[i] else res_char.lower()
        else:
            result += coded[i]
    return result

def split_chunks(text: str, alphabet: Optional[List[str]] = None) -> List[str]:
    """
    Uses regex to split the sentence:
    words go one chunk, punctuation/space another

    Example: "Hi, Bob!" → ['Hi', ',', ' ', 'Bob', '!']
    """
    if alphabet is None:
        alphabet = list(string.ascii_uppercase)
        
    # Manual splitting based on alphabet membership
    chunks = []
    if not text:
        return chunks
        
    current_chunk = ""
    # Check first char membership
    current_chunk = ""
    # Check first char membership
    is_word = text[0].upper() in alphabet
    
    for char in text:
        char_is_in_alpha = char.upper() in alphabet
        
        if char_is_in_alpha == is_word:
            current_chunk += char
        else:
            chunks.append(current_chunk)
            current_chunk = char
            is_word = char_is_in_alpha
            
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def join_chunks(chunks: List[str]) -> str:
    """
    Directly joins chunks as split_chunks preserves all delimiters.
    """
    return "".join(chunks)

def encrypt_sentence_otp(sentence: str, alphabet: Optional[List[str]] = None, shift: int = 1) -> Tuple[str, List[str], List[Dict[str, Any]]]:
    """
    Encrypts a sentence using One-Time Pad (OTP).
    Returns (encrypted_sentence, keys_used, mapping).
    Mapping is a list of dicts: {"text": str, "type": "WORD|SEP", "key": str|None}
    """
    if alphabet is None:
        alphabet = list(string.ascii_uppercase)
        
    table = build_table(alphabet, shift)
    chunks = split_chunks(sentence, alphabet)
    encrypted_chunks = []
    keys_used = []
    mapping = []

    for chunk in chunks:
        is_word = chunk and chunk[0].upper() in alphabet
        if is_word:
            word_key = random_key(len(chunk), alphabet)
            encrypted, used_key = encrypt_word(chunk, word_key, table, alphabet)
            encrypted_chunks.append(encrypted)
            keys_used.append(used_key)
            mapping.append({
                "original": chunk,
                "result": encrypted,
                "type": "WORD",
                "key": used_key
            })
        else:
            encrypted_chunks.append(chunk)
            mapping.append({
                "original": chunk,
                "result": chunk,
                "type": "SEP",
                "key": None
            })
    return join_chunks(encrypted_chunks), keys_used, mapping

def decrypt_sentence(ciphertext: str, keys_used: List[str], alphabet: Optional[List[str]] = None, shift: int = 1) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Decrypts a sentence and returns (decrypted_text, mapping).
    """
    if alphabet is None:
        alphabet = list(string.ascii_uppercase)
        
    table = build_table(alphabet, shift)
    chunks = split_chunks(ciphertext, alphabet)
    decrypted_chunks = []
    mapping = []
    key_idx = 0

    for chunk in chunks:
        is_word = chunk and chunk[0].upper() in alphabet
        if is_word:
             # Legacy Fallback: If only one key provided for multi-word message
             current_key = keys_used[0] if len(keys_used) == 1 else (keys_used[key_idx] if key_idx < len(keys_used) else None)
             
             if current_key:
                decrypted = decrypt_word(chunk, current_key, table, alphabet)
                decrypted_chunks.append(decrypted)
                mapping.append({
                    "original": chunk,
                    "result": decrypted,
                    "type": "WORD",
                    "key": current_key
                })
                key_idx += 1
             else:
                decrypted_chunks.append(chunk)
                mapping.append({
                    "original": chunk,
                    "result": chunk,
                    "type": "WORD",
                    "key": None
                })
        else:
            decrypted_chunks.append(chunk)
            mapping.append({
                "original": chunk,
                "result": chunk,
                "type": "SEP",
                "key": None
            })
    return join_chunks(decrypted_chunks), mapping

def save_keys(keys: List[str], filename: str) -> bool:
    try:
        with open(filename, 'w') as f:
            for key in keys:
                f.write(key + '\n')
        print(f"Keys saved to {filename}")
        return True
    except IOError as e:
        print(f"Error saving keys: {e}")
        return False

def save_text(text: str, filename: str) -> bool:
    """
    Saves text to a file with basic path security checks.
    """
    # Security: Prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        # Simple jail: valid filenames only, no paths.
        print(f"Error: Invalid filename '{filename}'. Use simple filenames only.")
        return False
        
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except IOError as e:
        print(f"Error saving file: {e}")
        return False

def save_session_json(data: Dict[str, Any], filename: str) -> bool:
    """
    Saves the entire session state to a JSON file in the 'vault' directory.
    Enforces security checks on the filename.
    """
    # Ensure vault directory exists
    vault_dir = os.path.join(os.path.dirname(__file__), 'vault')
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir)

    # Security: Prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        print(f"Error: Invalid filename '{filename}'. Use simple filenames only.")
        return False
        
    filepath = os.path.join(vault_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        print(f"Error saving session: {e}")
        return False

def load_session_json(filename: str) -> Optional[Dict[str, Any]]:
    """
    Loads a session state from a JSON file in the 'vault' directory.
    """
    vault_dir = os.path.join(os.path.dirname(__file__), 'vault')
    filepath = os.path.join(vault_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Error: File '{filename}' not found in vault.")
        return None
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading session: {e}")
        return None

def load_keys(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as f:
            keys = [line.strip() for line in f.readlines()]
        return keys
    except IOError as e:
        print(f"Error loading keys: {e}")
        return []
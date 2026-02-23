# User Guide

Welcome to the Crypt Workspace! This guide will help you master the professional features of this Vigenère Cipher tool.

## 🏁 Workflow: Your First Encryption

1. **Start the App**: `python crypt.py`
2. **Set Input**: Press `1` and type your secret message (e.g., "Attack at Dawn").
3. **Run Encryption**: Press `4`.
    - The system generates a random key for "Attack" and "Dawn".
    - The status changes to `ENCODED`.
4. **Save**: Press `3` and name your project `ops_omega.json`.

## 📁 The Workspace History
Unlike simple scripts, this tool stores every step as an **Entry**.

- **View History**: Press `7` to see the `Project History`.
- **View Mapping**: In the history list, type an index (e.g., `0`) to see the **Detailed Mapping**.
    - You will see exactly which key character was used for each letter in your message.
- **Active Chaining**: If you have an `ENCODED` entry and you select `Decrypt`, the system automatically uses that entry as the input.

## 🕵️ Auto-Detection Features
The system is designed to handle common files without manual typing:

| File | Auto-Detection Trigger |
|------|------------------------|
| `msg.txt` | Prompted when setting a message if the file exists. |
| `cipher.txt` | Prompted during Decryption if the current project is empty. |
| `keys.txt` | Prompted if you try to Decrypt an entry that has no stored keys. |

## ⚙️ Customizing the Cipher
Navigate to `6. Settings` to change the mathematical foundation of your encryption.

- **Custom Alphabet**: You can define a subset of letters (e.g., just `ABCD`) for specialized ciphers.
- **Table Shift**: Changes the Caesar shift of the Vigenère rows. 
    - *Tip*: A shift of `0` results in a standard Vigenère square.

> ⚠️ **IMPORTANT**: If you encrypt a message with a custom alphabet or shift, you **MUST** use those same settings to decrypt it. These settings are automatically saved in your `.json` workspace file.

## 💾 JSON Workspace vs. Text Files
- **Projects (JSON)**: Store history, mappings, alphabets, and shifts. Use these for long-term work.
- **Standard Exports**: After encrypting/decrypting, you are prompted to save to `cipher.txt` or `msg.txt`. These are for external use or sharing.

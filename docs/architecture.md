# Architecture Documentation - Deep Dive

## 🏛️ System Overview
The Crypt Workspace is built on a decoupled architecture that separates **Logic** (Stateless Engine) from **State** (Command Pattern CLI & JSON Workspace).

## 🧩 Component Breakdown

### 1. Stateless Engine (`engine.py`)
The engine is a purely functional layer designed to perform deterministic cryptographic operations.
- **Vigenère Core**: Generates a shifted alphabetic matrix. Row index depends on the Key character, Column index depends on the Plaintext character.
- **Word-Level Chunking**: Uses `split_chunks` to separate alphabetic tokens from punctuation/whitespace. This allows the system to encrypt selectively while maintaining sentence structure.
- **Random OTP Generation**: During encryption, a random key is generated for *each* word chunk, maximizing entropy for multi-word sentences.

### 2. Workspace Orchestrator (`crypt.py`)
Managed via a **Command Pattern Dispatcher**.
- **Mutable State**: Holds `current_data` which tracks the active workspace name, global alphabet/shift settings, and the history `entries`.
- **History (Entries) Model**: Each entry is a snapshot.
    - `RAW`: Newly set message.
    - `ENCODED`: Result of `encrypt_sentence_otp`.
    - `DECODED`: Result of `decrypt_sentence`.
- **Active Result Resolution**: Functions like `run_encryption` automatically pull the "Active Result" (the most recent entry) as their input, enabling chaining (e.g., Set -> Encrypt -> Decrypt).


## 📂 Data Storage (Workspace JSON)
The JSON schema is designed for auditing and state recovery.

| Field | Description |
|-------|-------------|
| `name` | Human-readable name of the project. |
| `alphabet` | The character set used for this workspace. |
| `shift`| The Caesar shift applied to the Vigenère rows. |
| `entries` | A chronological list of all actions performed. |

### Entry Schema
```json
{
    "msg": "Input for this step",
    "result": "Output of this step",
    "keys": ["KEY_1", "KEY_2"],
    "mapping": [
        {
            "original": "Hello", 
            "result": "Xyzz", 
            "type": "WORD", 
            "key": "KEY_1"
        }
    ],
    "status": "ENCODED",
    "timestamp": "2026-02-10T09:00:00"
}
```

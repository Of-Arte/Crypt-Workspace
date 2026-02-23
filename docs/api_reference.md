# API Reference

Detailed technical documentation for the URL Tracker / Crypt Workspace.

## 🚀 Engine Layer (`engine.py`)

The engine provides pure logic for Vigenère transformations.

### `build_table(alphabet, shift) -> List[List[str]]`
Generates the Vigenère square.
- **alphabet**: List of characters.
- **shift**: Caesar-style starting offset for the matrix rows.

### `encrypt_word(word, key, table, alphabet) -> Tuple[str, str]`
Encrypts a single word with case preservation.
- **alphabet**: Required for validating char indices.
- **Returns**: `(ciphertext, formatted_key)`

### `encrypt_sentence_otp(sentence, alphabet, shift) -> Tuple[str, List[str], List[Dict]]`
Higher-level orchestrator for One-Time Pad encryption.
- **Process**: Chunks message -> Generates random keys -> Encrypts words.
- **Returns**:
    - `str`: The full encrypted sentence.
    - `List[str]`: All keys generated for word chunks.
    - `List[Dict]`: Detailed mapping for each chunk.

### `decrypt_sentence(ciphertext, keys_used, alphabet, shift) -> Tuple[str, List[Dict]]`
Orchestrator for Decryption.
- **Adaptive Key Matching**: If only one key is provided, it repeats it (Legacy Fallback). Otherwise, it applies keys sequentially to word chunks.

### `split_chunks(text, alphabet) -> List[str]`
Splits a string into a list where alphabetic sequences are separate from whitespace/punctuation.
- **Example**: `"Hi, User!"` -> `["Hi", ", ", "User", "!"]`

---

## 🛠️ CLI Layer (`crypt.py`)

Helpers for state management.

### `get_active_msg() -> str`
Resolves the "current" message in the workspace history. Returns the `result` of the most recent entry in `current_data['entries']`.

### `get_active_status() -> str`
Returns the status tag (`RAW`, `ENCODED`, `DECODED`) of the active result.

### `set_message(msg: str)`
Creates a new `RAW` entry in history. Discards temporary state but preserves historical entries.

### `save_project()` / `load_project()`
Serializes/Deserializes the `current_data` dictionary to the `vault/` directory using `engine.save_session_json`.

---

## 📄 Data Structures

### `MappingChunk` (Dictionary)
| Key | Type | Description |
|-----|------|-------------|
| `original` | `str` | Text before processing. |
| `result` | `str` | Text after processing. |
| `type` | `str` | `WORD` or `SEP`. |
| `key` | `str|None` | Key used for this chunk. |

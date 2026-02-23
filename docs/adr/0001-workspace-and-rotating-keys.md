# ADR-0001: Workspace Model and Rotating Keys (OTP)

## Status

Accepted

## Context

The project originally started as a simple Vigenère cipher implementation. During the conversational development process, we identified several security weaknesses in the standard repeating-key Vigenère model:
1. **Kasiski Examination**: Patterns in the ciphertext reveal the key length.
2. **Frequency Analysis**: Once the key length is known, individual columns can be cracked.

The user suggested an evolution towards using a queue to rotate through a sequence of keys for each word, inspired by the "One-Time Pad" (OTP) model.

## Decision

We decided to move away from a static repeating key and implement a **Workspace Management System** that:
1. Splits incoming text into individual word chunks.
2. Generates a unique, random, and padded key for *each* word chunk.
3. Stores these keys as part of a persistent "History Entry" in a JSON workspace (vault).
4. Enables "Active Result" chaining, where the output of one operation is the default input for the next.

## Decision Drivers

* **Security**: Eliminate patterns found in traditional Vigenère repetitions.
* **Usability**: Preserve punctuation, whitespace, and original casing.
* **Auditability**: Track exactly which key was used for which part of the message.
* **Persistence**: Move beyond ephemeral text files to managed project states (vaults).

## Consequences

### Positive
- **Indistinguishability**: Without the specific key mapping, the ciphertext is resistant to classic cryptanalysis.
- **Natural Rendering**: Messages retain their structure (punctuation/casing).
- **Project Context**: The `vault/` system allows users to manage multiple "secret ops" independently.

### Negative
- **Key Management Overhead**: Decryption requires the original mapping list, not just a single keyword.
- **Vault Complexity**: The system now relies on JSON file integrity in the `vault/` directory.

## Implementation Notes

- **Split Logic**: Implemented in `engine.split_chunks`.
- **OTP Logic**: Implemented in `engine.encrypt_sentence_otp`.
- **Mapping**: Each entry in the history tracks `original`, `result`, `key`, and `type`.

## References

- [Conversation Transcript](Project Spark Conversation)
- [Vigenère Cipher - Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- [One-Time Pad - Wikipedia](https://en.wikipedia.org/wiki/One-time_pad)

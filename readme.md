# Crypt Workspace (Artè Cipher) 🔐

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A secure, command-line workspace for symmetric encryption, built as a capstone project for my dev portfolio.**

---

## 🌟 The Spark

This project was born from a conversation. It started with a simple curiosity about how the **Vigenère cipher** hides text and quickly evolved into a deep dive into algorithmic thinking, data structures, and real world security.

What began as "building a 26x26 table in Python" became a lesson in the fragility of repeating keys and the power of rotating randomness. From pseudocode and ASCII flowcharts to a robust, menu driven workspace system.

You can read the original [Developer Diary on my learning journey here](./legacy/README.md), which documents my design-first approach, early mistakes, and first-year "lightbulb" moments.

---

## 🎓 What I Built & Learned

Through building this capstone project, I mastered several core engineering and cryptographic concepts:

- **Algorithmic Design**: Designing solutions using step-by-step pseudocode and ASCII flowcharts before writing a single line of Python.
- **Data Structures**: Using **Stacks (Lists)** to rotate the alphabet and build the cipher table row by row, and **Queues** to rotate through multiple keys.
- **Character Encoding**: Mastering `ord()` and `chr()` to bridge the gap between human letters and computer-readable Unicode spots (A=0, Z=25).
- **Cryptanalysis**: Learning why simple Vigenère repeats are vulnerable to frequency analysis and Kasiski examination.
- **Secure Architecture**: Implementing a "One-Time Pad" approach where keys are as long as the content, random, and never reused.
- **User Experience (UX)**: Building a menu-driven CLI that maintains project state (Vaults) and preserves natural text elements like casing and punctuation.

---

## ✨ Features

- **OTP Engine**: Generates unique, random, and padded keys for every word chunk.
- **Workspace (Vault) System**: Persistent storage of "Secret Ops" in JSON format, tracking full history and mapping.
- **Linguistic Versatility**: Support for Latin (A-Z), Spanish (A-Z + Ñ), and French (A-Z + Accents) alphabets.
- **Bi-Directional Tracing**: Audit exactly which key shift was applied to which character.
- **Smart Formatting**: Maintains original spaces, punctuation, and casing through the encryption cycle.

---

## 🚀 Quick Start

```bash
# Start the Crypt Workshop
python crypt.py
```

### Typical Workflow:
1. **[1] Set Message**: Import from `msg.txt` or type your secret.
2. **[4] Encrypt**: The engine generates random keys and encrypts your chunks.
3. **[3] Save Project**: Persistent storage in the `vault/`.
4. **[5] Decrypt**: Automatically uses the associated keys from the workspace history.

---

## 📂 Documentation

- [Architecture Guide](./docs/architecture.md) - Deep dive into the engine and mapping logic.
- [User Guide](./docs/user_guide.md) - How to use the CLI and manage vaults.
- [API Reference](./docs/api_reference.md) - Function-level documentation for developers.
- [Architecture Decisions](./docs/adr/0001-workspace-and-rotating-keys.md) - Why we moved to the OTP model.

---

## 🏛️ Flow Overview

```text
       Start [Input Sentence]
             |
      Split sentence into chunks (Words vs. Punctuation)
             ↓
    For each Word chunk:
  ┌───────────────────────────────────┐
  | Generate/Get Next Random Key      |
  | Pad Key to match Word length      |
  | Lookup Vigenère(Key_i, Word_i)    |
  | Save Pair to Mapping History      |
  └─────────────┬─────────────────────┘
                |
        Reassemble Chunks (Keeping Punctuation)
                |
       End [Encrypted Result]
```

---

## 📄 License

Distributed under the MIT License.

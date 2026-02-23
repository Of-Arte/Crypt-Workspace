# Vigenère Cipher Project: A First-Year Developer's Journey

**Author:** De Arte  
**Context:** Self-directed learning project during AI Software Engineering pathway  
**Tech Stack:** Python 3.x  
**Time Investment:** Single intensive coding session  
**Approach:** Design-first (pseudocode → flowchart → implementation)

## What I Built

A command-line Vigenère cipher tool featuring:

- **Programmatic cipher table generation** using list rotation.
- **Encrypt and decrypt functions** with versatile key wrapping.
- **Interactive menu system** for robust state management.
- **Debug trace toggle** to visualize and learn the algorithm mechanics.

## My Learning Journey

### Phase 1: Understanding the Concept
**Challenge:** "How does the Vigenère cipher actually work?"

**Breakthrough:** "The Vigenère cipher uses a message and keyword to map a letter to a value within a 26×26 table."

The mental model clicked when I realized we're doing coordinate lookups, not mysterious encryption magic.

```python
table[key_letter_position][message_letter_position] = encrypted_letter
```

### Phase 2: Designing the Table Builder
**Goal:** Generate the 26×26 cipher table programmatically.

**My Pseudocode:**
1. Initialize alphabet list (A-Z)
2. Copy alphabet to stack
3. Create empty table
4. For each shift from 0 to 25:
   a. Append copy of current stack to table
   b. Pop first letter from stack, append to end
5. Return completed table

**What I Learned:** Visualizing the stack rotation before coding prevented major logic errors later.

### Phase 3: First Major Bug (Reference vs. Copy)
**What Happened:** My initial code appended the same list object 26 times, so all rows changed together when I rotated.

**Bad Code:**
```python
table.append(array)  # All rows point to same object
```

**Fixed Code:**
```python
table.append(array.copy())  # Each row is independent snapshot
```

**Lesson:** Python lists pass by reference. When you need independence, explicitly copy.

### Phase 4: Learning ord() and chr()
**Confusion Point:** "How do I convert letters to numbers and back?"

**What I Learned:**
- Every character has a Unicode number (A=65, B=66, ..., Z=90).
- To get alphabet position: `ord(letter) - ord('A')` gives 0-25.
- To convert back: `chr(index + ord('A'))` gives the letter.

**Mental Model:** Think of the alphabet as numbered boxes:
```text
A B C D E ... Z
0 1 2 3 4 ... 25
```

### Phase 5: Building the Encrypt Function
**Struggle:** "How do I match each message letter with its key letter?"

**Solution:** Key wrapping with modulo.

```python
for idx in range(len(msg)):
    key_i = idx % len(key)  # Repeats key: "CAT" → C-A-T-C-A-T...
    row = ord(key[key_i]) - ord('A')
    col = ord(msg[idx]) - ord('A')
    result += table[row][col]
```

**What I Learned:** The `%` operator makes short keys repeat across long messages automatically.

### Phase 6: Building the Decrypt Function
**Challenge:** Reverse the encryption lookup.

**Mental Model Shift:**
- **Encrypt:** `table[row][col]` gives encrypted letter.
- **Decrypt:** Find which `col` in `table[row]` matches the encrypted letter.

**Solution:**
```python
row = ord(key[key_i]) - ord('A')
col = table[row].index(msg[idx])  # Find position in row
plaintext_letter = chr(col + ord('A'))
```

**What I Learned:** `.index()` searches a list and returns the matching position—the inverse of direct indexing.

### Phase 7: Building the Menu System
**Goal:** Make the tool interactive and testable.

**What I Added:**
- State management dictionary to track message/key/results.
- Menu dispatch system using dictionary lookup.
- Functions for each action (set message, encrypt, decrypt, view state).
- Toggle for debug trace messages.

**What I Learned:** Separating UI (menu) from logic (encrypt/decrypt) makes testing and debugging easier.

## Final Working Code

```python
def build_table():
    """Builds the Vigenère table (26x26)."""
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
                "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    array = alphabet[::]  # Copy for rotation
    table = []
    for i in range(26):
        table.append(array[::])  # Save snapshot
        popped = array.pop(0)     # Rotate
        array.append(popped)
    return table

def encrypt(msg, key, table):
    """Encrypts a message using a key and the Vigenère table."""
    result = ""
    for idx in range(len(msg)):
        key_i = idx % len(key)
        row = ord(key[key_i]) - ord('A')
        col = ord(msg[idx]) - ord('A')
        result += table[row][col]
    return result

def decrypt(msg, key, table):
    """Decrypts a message using a key and the Vigenère table."""
    result = ""
    for idx in range(len(msg)):
        key_i = idx % len(key)
        row = ord(key[key_i]) - ord('A')
        col = table[row].index(msg[idx])  # Reverse lookup
        result += chr(col + ord('A'))
    return result
```

**Test Case:**
```python
table = build_table()
encrypted = encrypt("ATTACKATDAWN", "LEMON", table)  # → "LXFOPVEFRNHR"
decrypted = decrypt("LXFOPVEFRNHR", "LEMON", table)  # → "ATTACKATDAWN"
```

## Key Concepts I Now Understand

1.  **Data Structures Drive Algorithms**: Using a stack (list with pop/append) made table rotation straightforward.
2.  **Design Before Code**: Pseudocode and flowcharts prevented false starts. 
3.  **Indexing vs. Iteration**: Using `range(len(msg))` is crucial when you need both position and value.
4.  **Reference Semantics Matter**: Appending a list appends a reference, not a copy. Modifications affect all "copies" unless you explicitly `.copy()`.
5.  **Mathematical Operations as Table Lookups**: Replaced modular arithmetic with visual table lookups for better debuggability.

## Debugging Stories

1.  **Bug 1: Alphabet Typo**
    - *Problem:* Built table with missing 'U' and duplicate 'Y'.
    - *Fix:* Carefully spell out all 26 letters.
2.  **Bug 2: Lowercase Input**
    - *Problem:* Used `.lower()` on input but table contains uppercase.
    - *Fix:* Always `.upper()` inputs before processing.
3.  **Bug 3: Calling ord() Directly on Index**
    - *Problem:* `table[ord(msg_i)][ord(key_i)]` used Unicode values (65-90) instead of 0-25.
    - *Fix:* Subtract `ord('A')` to get alphabet position.

## Skills I Practiced

- **Algorithm design**: Breaking problems into pseudocode steps
- **Data structures**: Using lists as stacks for rotation
- **Loop logic**: Index-based iteration with wrapping (modulo)
- **String manipulation**: Building results character-by-character
- **Debugging**: Reading error messages, tracing execution
- **Code organization**: Functions, state management, menu dispatch
- **Type conversions**: Characters ↔ integers ↔ alphabet positions

## Future Enhancements

- [ ] Add support for spaces and punctuation (encrypt words only, preserve formatting)
- [ ] Random key generation for one-time pad security
- [ ] File encryption (read plaintext, write ciphertext + key)
- [ ] GUI with visual table highlighting during encryption
- [ ] Frequency analysis tool to crack weak keys

## How to Run

```bash
python main.py
```

### Menu Options:
- `[1]` Set Message
- `[2]` Set Key
- `[3]` Encrypt
- `[4]` Decrypt
- `[5]` View State
- `[6]` Show Menu
- `[7]` Toggle Trace
- `[0]` Shut down

### Example Session:
```text
> 1
Enter message: HELLO
Message updated to: HELLO

> 2
Enter key: KEY
Key updated to: KEY

> 3
Encryption Result: RIJVS

> 5
=== Current State ===
Message:   HELLO
Key:       KEY
Encrypted: RIJVS
Decrypted: 
```

## Why This Project Mattered
Before: Vigenère was an abstract cryptography concept.  
After: I understand table-based substitution, key management, and how classical ciphers work at the character level.

This documentation captures my authentic learning journey—mistakes included—so future me (and other first-year developers) can learn from both the successes and the debugging.

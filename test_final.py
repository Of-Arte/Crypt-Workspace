import engine
import os

def test_final_polish():
    print("--- Final Polish Verification ---")
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    # 1. Smart Case Preservation
    print("\n1. Testing Smart Case...")
    text = "Hello World"
    # Encrypt
    enc, keys, _ = engine.encrypt_sentence_otp(text, alphabet)
    print(f"  Plain: {text}")
    print(f"  Cipher: {enc}")
    
    # Check case preservation (simplified check)
    assert enc[0].isupper(), "First char should be upper"
    assert enc[1].islower(), "Second char should be lower"
    assert " " in enc, "Space should be preserved"
    
    # Decrypt
    dec, _ = engine.decrypt_sentence(enc, keys, alphabet)
    print(f"  Decrypted: {dec}")
    assert dec == text, f"Decryption mismatch: {dec} != {text}"
    print("  >> Smart Case PASSED")
    
    # 2. Legacy Key Fallback
    print("\n2. Testing Legacy Key Fallback...")
    # Single key 'LEMON' for 'HELLO WORLD'
    legacy_keys = ["LEMON"] 
    # Use standard Vigenere expectation:
    # HELLO + LEMON -> QOFZR
    # WORLD + LEMON -> HSRDP
    # Total: QOFZR HSRDP
    
    # Note: engine uses random padding for encryption, but decryption with single key should repeat it.
    # To test this, we need a known ciphertext or just verify it doesn't crash and uses the key.
    # Actually, legacy.py used repeating keys. Our decrypt_sentence will repeat keys[0] if len == 1.
    
    # Encrypt manually with LEMON repeated to get target
    # (Using engine logic)
    res_h, _ = engine.encrypt_word("HELLO", "LEMON", engine.build_table(alphabet), alphabet)
    res_w, _ = engine.encrypt_word("WORLD", "LEMON", engine.build_table(alphabet), alphabet)
    target_cipher = f"{res_h} {res_w}"
    
    # Decrypt with single key
    dec_legacy, _ = engine.decrypt_sentence(target_cipher, legacy_keys, alphabet)
    print(f"  Target Cipher: {target_cipher}")
    print(f"  Decrypted (Single Key): {dec_legacy}")
    assert dec_legacy == "HELLO WORLD", f"Legacy fallback failed: {dec_legacy}"
    print("  >> Legacy Key Fallback PASSED")

    print("\n--- ALL FINAL TESTS PASSED ---")

if __name__ == "__main__":
    test_final_polish()

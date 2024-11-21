# utils.py
def caesar_encrypt(text, shift=3):
    """Encrypt text using a Caesar cipher."""
    encrypted = ''.join(chr((ord(char) + shift - 32) % 95 + 32) if 32 <= ord(char) <= 126 else char for char in text)
    return encrypted

def caesar_decrypt(text, shift=3):
    """Decrypt text using a Caesar cipher."""
    decrypted = ''.join(chr((ord(char) - shift - 32) % 95 + 32) if 32 <= ord(char) <= 126 else char for char in text)
    return decrypted

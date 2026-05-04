import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
import base64
import hashlib

# Caesar Cipher Functions
def encrypt_caesar(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift_amount = shift % 26
            shifted = ord(char) + shift_amount
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                ciphertext += chr(shifted)
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                ciphertext += chr(shifted)
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext, shift):
    return encrypt_caesar(ciphertext, -shift)

# AES Functions with key normalization
def normalize_key(key):
    return hashlib.sha256(key.encode('utf-8')).digest()  # 32 bytes (AES-256)

def encrypt_aes(plaintext, key):
    key = normalize_key(key)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_aes(ciphertext, key):
    key = normalize_key(key)
    data = base64.b64decode(ciphertext)
    nonce = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    return plaintext

# Encrypt Button Function
def encrypt():
    plaintext = text_input.get("1.0", tk.END).strip()
    shift = int(shift_input.get() or 0)
    key = key_input.get()

    if algorithm.get() == "Caesar Cipher":
        result = encrypt_caesar(plaintext, shift)
    elif algorithm.get() == "AES":
        result = encrypt_aes(plaintext, key)
    else:
        result = "Invalid Algorithm"

    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, result)

# Decrypt Button Function
def decrypt():
    ciphertext = text_input.get("1.0", tk.END).strip()
    shift = int(shift_input.get() or 0)
    key = key_input.get()

    if algorithm.get() == "Caesar Cipher":
        result = decrypt_caesar(ciphertext, shift)
    elif algorithm.get() == "AES":
        try:
            result = decrypt_aes(ciphertext, key)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))
            return
    else:
        result = "Invalid Algorithm"

    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, result)

# GUI Setup
app = tk.Tk()
app.title("Simple Encryption and Decryption Tool")

tk.Label(app, text="Text:").pack()
text_input = tk.Text(app, height=5, width=50)
text_input.pack()

tk.Label(app, text="Shift (for Caesar Cipher):").pack()
shift_input = tk.Entry(app)
shift_input.pack()

tk.Label(app, text="Key (for AES):").pack()
key_input = tk.Entry(app)
key_input.pack()

tk.Label(app, text="Algorithm:").pack()
algorithm = tk.StringVar(app)
algorithm.set("Caesar Cipher")
tk.OptionMenu(app, algorithm, "Caesar Cipher", "AES").pack()

tk.Button(app, text="Encrypt", command=encrypt).pack()
tk.Button(app, text="Decrypt", command=decrypt).pack()

tk.Label(app, text="Result:").pack()
result_output = tk.Text(app, height=5, width=50)
result_output.pack()

app.mainloop()

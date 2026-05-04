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

# AES Functions
def normalize_key(key):
    return hashlib.sha256(key.encode('utf-8')).digest()

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

# Encrypt Function
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

# Decrypt Function
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

# NEW: Clear Function
def clear_fields():
    text_input.delete("1.0", tk.END)
    result_output.delete("1.0", tk.END)
    shift_input.delete(0, tk.END)
    key_input.delete(0, tk.END)

# NEW: Copy Function
def copy_result():
    result = result_output.get("1.0", tk.END).strip()
    app.clipboard_clear()
    app.clipboard_append(result)
    messagebox.showinfo("Copied", "Result copied to clipboard!")

# GUI
app = tk.Tk()
app.title("Encryption and Decryption Tool")
app.configure(bg="#1e1e2f")  # dark background

# Labels
tk.Label(app, text="Text:", bg="#1e1e2f", fg="white").pack()
text_input = tk.Text(app, height=5, width=50, bg="#2b2b3c", fg="white")
text_input.pack()

tk.Label(app, text="Shift (Caesar):", bg="#1e1e2f", fg="white").pack()
shift_input = tk.Entry(app, bg="#2b2b3c", fg="white")
shift_input.pack()

tk.Label(app, text="Key (AES):", bg="#1e1e2f", fg="white").pack()
key_input = tk.Entry(app, bg="#2b2b3c", fg="white")
key_input.pack()

tk.Label(app, text="Algorithm:", bg="#1e1e2f", fg="white").pack()
algorithm = tk.StringVar(app)
algorithm.set("Caesar Cipher")
tk.OptionMenu(app, algorithm, "Caesar Cipher", "AES").pack()

# Buttons
tk.Button(app, text="Encrypt", bg="#4CAF50", fg="white", command=encrypt).pack()
tk.Button(app, text="Decrypt", bg="#2196F3", fg="white", command=decrypt).pack()
tk.Button(app, text="Clear", bg="#f44336", fg="white", command=clear_fields).pack()
tk.Button(app, text="Copy Result", bg="#9C27B0", fg="white", command=copy_result).pack()

tk.Label(app, text="Result:", bg="#1e1e2f", fg="white").pack()
result_output = tk.Text(app, height=5, width=50, bg="#2b2b3c", fg="white")
result_output.pack()

app.mainloop()

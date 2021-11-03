from tkinter import *

import algorithms

machine = algorithms.ECCElGamalMachine()

root = Tk()
root.geometry("1000x800")
root.title("Encryption")

key_size_option = [10, 11, 12]
  
def generate_key():
    pub_key, pri_key = machine.create_key_full(int(key_size.get()))

    key_1.delete('1.0', END)
    key_1.insert(END, str(pub_key))

    key_2.delete('1.0', END)
    key_2.insert(END, str(pri_key))

def encrypt():
    pub_key = key_1.get("1.0", "end-1c")
    
    plaintext_value = plaintext.get("1.0", "end-1c")
    plaintext.delete('1.0', END)
    encrypted = machine.encrypt_full(plaintext_value, pub_key)

    ciphertext.delete('1.0', END)
    ciphertext.insert(END, encrypted)

def decrypt():
    pri_key = key_2.get("1.0", "end-1c")

    ciphertext_value = ciphertext.get("1.0", "end-1c")
    ciphertext.delete('1.0', END)
    decrypted = machine.decrypt_full(ciphertext_value, pri_key)

    plaintext.delete('1.0', END)
    plaintext.insert(END, decrypted)
      
main_title = Label(text = "ECC ElGamal Encryption")

key_size = StringVar(root); key_size.set(key_size_option[2]);
key_size_dropdown = OptionMenu(root, key_size, *key_size_option)

generate_key_button = Button(root, height = 2, width = 60, text ="Generate Key", command = lambda: generate_key())

key_1 = Text(root, height = 5, width = 60)
key_2 = Text(root, height = 5, width = 60)

plaintext = Text(root, height = 5, width = 60)
encrypt_button = Button(root, height = 2, width = 60, text ="Encrypt!", command = lambda: encrypt())

ciphertext = Text(root, height = 5, width = 60)
decrypt_button = Button(root, height = 2, width = 60, text ="Decrypt!", command = lambda: decrypt())

  
  
main_title.pack()

key_size_dropdown.pack()
generate_key_button.pack()

key_1.pack()
key_2.pack()
  
plaintext.pack()
encrypt_button.pack()

ciphertext.pack()
decrypt_button.pack()

mainloop()














# p, curve_a, curve_b, B, k = machine.create_agreement(bit=12)

# p, curve_a, curve_b, B, k = machine.create_agreement(12)

# print()

# print("GENERATE RANDOM AGREEMENT")
# print("p\t: " + str(p))
# print("crv_a\t: " + str(curve_a))
# print("crv_b\t: " + str(curve_b))
# print("B\t: " + str(B))
# print("k\t: " + str(k))

# print()

# alice_public_key, alice_private_key = machine.create_key(p, curve_a, curve_b, B)
# print("GENERATE ALICE KEYS")
# print("public_key\t: " + str(alice_public_key))
# print("private_key\t: " + str(alice_private_key))

# print()

# bob_public_key, bob_private_key = machine.create_key(p, curve_a, curve_b, B)
# print("GENERATE BOB KEYS")
# print("public_key\t: " + str(bob_public_key))
# print("private_key\t: " + str(bob_private_key))

# print()

# print("ENCRYPTED")
# encrypted = machine.encrypt("AUFA Fadhlurohman", bob_public_key, p, curve_a, curve_b, B, k)
# print(encrypted)

# print()

# print("DECRYPTED")
# decrypted = machine.decrypt(encrypted, bob_private_key, p, curve_a, curve_b, k)
# print(decrypted)

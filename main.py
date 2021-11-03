from tkinter import *

import random
import math
import codecs
import base64  

class Utils:
    def __init__(self):
        '''if not used then delete'''
    
    def hex_to_dec(hex):
        deci = int(hex, 16)
        return deci

    def dec_to_hex(dec):
        hexa = hex(dec)
        return hexa

    def hex_to_b64(hex):
        hex = hex[2:] if(len(hex[2:]) % 2 == 0) else '0' + hex[2:]
        b64 = codecs.encode(codecs.decode(hex, 'hex'), 'base64').decode()
        return b64
       
    def b64_to_hex(b64):
        hexa = base64.b64decode(b64).hex()
        return hexa
    
    def dec_to_b64(dec):
        b64 = Utils.hex_to_b64(Utils.dec_to_hex(dec))
        return b64

    def b64_to_dec(b64):
        deci = Utils.hex_to_dec(Utils.b64_to_hex(b64))
        return deci

    def is_square(i):
        return i == math.isqrt(i) ** 2

    def mod_sqrt(n, p):

        points = []
        n = n % p
        for x in range (1, p):
            if ((x ** 2) % p == n) :
                points.append(x)
        return points

class ElGamal:
    def __init__(self):
        pass

    def create_key(self, p, g, x):
        y = pow(g, x, p)
        public_key = { 'y': y, 'g': g, 'p': p }
        private_key = { 'x': x, 'p': p }
        return public_key, private_key

    def encrypt(self, message, key, public_key):
        a = pow(public_key['g'], key, public_key['p'])
        b = (pow(public_key['y'], key, public_key['p']) * (message % public_key['p'])) % public_key['p']
        return { 'a': a, 'b': b }

    def decrypt(self, message, private_key):
        return ((message['b'] % private_key['p']) * pow(message['a'], (private_key['p'] - 1 - private_key['x']), private_key['p'])) % private_key['p']

class ElGamalMachine:
    def __init__(self):
        self.elgamal = ElGamal()
    
    def is_prime(self, num, test_count=1000):
        if(num == 1):
            return False
        if(test_count >= num):
            test_count = num - 1
        for _ in range(test_count):
            val = random.randint(1, num - 1)
            if(pow(val, num-1, num) != 1):
                return False
        return True
    def create_random_prime(self, bit):
        found = False
        while not found:
            p = random.randint(2**(bit-1)+1, 2**bit-1)
            if self.is_prime(p):
                return p
    
    def create_key(self, bit):
        p = self.create_random_prime(bit)
        g = random.randint(1, p - 1)
        x = random.randint(1, p -2)

        public_key, private_key = self.elgamal.create_key(p, g, x)

        public_key['y'] = Utils.dec_to_b64(public_key['y'])
        public_key['g'] = Utils.dec_to_b64(public_key['g'])
        public_key['p'] = Utils.dec_to_b64(public_key['p'])

        private_key['x'] = Utils.dec_to_b64(private_key['x'])
        private_key['p'] = Utils.dec_to_b64(private_key['p'])

        pub_key = public_key['y'] + public_key['g'] + public_key['p']
        pri_key = private_key['x'] + private_key['p']

        return pub_key, pri_key

    def encrypt(self, message, public_key):
        y = Utils.b64_to_dec(public_key['y'])
        g = Utils.b64_to_dec(public_key['g'])
        p = Utils.b64_to_dec(public_key['p'])

        p_key = { 'y': y, 'g': g, 'p': p }

        encrypted = ''
        for m in message:
            k = random.randint(1, p-2)
            res = self.elgamal.encrypt(ord(m), k, p_key)
            a = Utils.dec_to_b64(res['a'])
            b = Utils.dec_to_b64(res['b'])
            encrypted += a + b
        return encrypted

    def decrypt(self, encrypted, private_key):
        x = Utils.b64_to_dec(private_key['x'])
        p = Utils.b64_to_dec(private_key['p'])

        p_key = { 'x': x, 'p': p }
        
        encrypted = encrypted.split('=\n')[:-1]
        encrypted_paired = []
        for i in range(0, len(encrypted), 2):
            a = Utils.b64_to_dec(encrypted[i] + '=\n')
            b = Utils.b64_to_dec(encrypted[i+1] + '=\n')
            encrypted_paired.append({ 'a': a, 'b': b })

        message = ''
        for m in encrypted_paired:
            message += chr(self.elgamal.decrypt(m, p_key))
        return message


machine = ElGamalMachine()

root = Tk()
root.geometry("1000x800")
root.title("Encryption")

key_size_option = [64, 128, 256, 512, 1024]
  
def generate_key():
    pub_key, pri_key = machine.create_key(int(key_size.get()))

    key_1.delete('1.0', END)
    key_1.insert(END, str(pub_key))

    key_2.delete('1.0', END)
    key_2.insert(END, str(pri_key))

def encrypt():
    pub_key = key_1.get("1.0", "end-1c")
    public_key = pub_key.split("=\n")[:-1]
    public_key = { 'y': public_key[0] + "=\n", 'g': public_key[1] + "=\n", 'p': public_key[2] + "=\n" }
    
    plaintext_value = plaintext.get("1.0", "end-1c")
    plaintext.delete('1.0', END)
    encrypted = machine.encrypt(plaintext_value, public_key)

    ciphertext.delete('1.0', END)
    ciphertext.insert(END, encrypted)

def decrypt():
    pri_key = key_2.get("1.0", "end-1c")
    private_key = pri_key.split("=\n")[:-1]
    private_key = { 'x': private_key[0] + "=\n", 'p': private_key[1] + "=\n" }

    ciphertext_value = ciphertext.get("1.0", "end-1c")
    ciphertext.delete('1.0', END)
    decrypted = machine.decrypt(ciphertext_value, private_key)

    plaintext.delete('1.0', END)
    plaintext.insert(END, decrypted)
      
main_title = Label(text = "ElGamal Encryption")

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
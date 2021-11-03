import algorithms

machine = algorithms.ECCElGamalMachine()

p, curve_a, curve_b, B, k = machine.create_agreement(bit=12)


p, curve_a, curve_b, B, k = machine.create_agreement(12)

print()

print("GENERATE RANDOM AGREEMENT")
print("p\t: " + str(p))
print("crv_a\t: " + str(curve_a))
print("crv_b\t: " + str(curve_b))
print("B\t: " + str(B))
print("k\t: " + str(k))

print()

alice_public_key, alice_private_key = machine.create_key(p, curve_a, curve_b, B)
print("GENERATE ALICE KEYS")
print("public_key\t: " + str(alice_public_key))
print("private_key\t: " + str(alice_private_key))

print()

bob_public_key, bob_private_key = machine.create_key(p, curve_a, curve_b, B)
print("GENERATE BOB KEYS")
print("public_key\t: " + str(bob_public_key))
print("private_key\t: " + str(bob_private_key))

print()

print("ENCRYPTED")
encrypted = machine.encrypt("AUFA Fadhlurohman", bob_public_key, p, curve_a, curve_b, B, k)
print(encrypted)

print()

print("DECRYPTED")
decrypted = machine.decrypt(encrypted, bob_private_key, p, curve_a, curve_b, k)
print(decrypted)

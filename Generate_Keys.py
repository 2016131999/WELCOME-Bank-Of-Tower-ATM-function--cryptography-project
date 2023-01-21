from RSA_General import generate_keys
u, v, w, x = generate_keys()
n = u*v
public_key = (w, n)
private_key = (x, n)
print("Public Key:   ", public_key)
print("Private Key:  ", private_key)
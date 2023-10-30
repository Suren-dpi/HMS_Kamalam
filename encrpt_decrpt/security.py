from cryptography.fernet import Fernet
'uON5CaIX2ybN-y4at5HyHefXXPIw8Rlb4fMayBRAQhU='
def enc(key, data):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode('utf-8'))
    print("After encryption : ", encrypted_data)

def dec(key,data):
    f = Fernet(key)
    decrypted_data = f.decrypt(data.encode('utf-8'))
    print("After decryption : ", decrypted_data.decode())


enc('2024-11-06')
dec('gAAAAABlSMwxUplLEwcEeIdmp_UhWVqULjuiO7bpQqS9Kdv4jTtsNNDi2ug0mvZToFGa7Ct1O5xvb9BcckB5rCgwzmF5Oc62UA==')
# Python 3 code to print MAC
# in formatted way.

import uuid
import secrets
import string

def get_mac():
    mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                         for ele in range(0, 8 * 6, 8)][::-1])
    return mac_addr




print(generate_password())
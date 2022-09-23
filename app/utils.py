import secrets
import string


def gen_secure_key(length: int = 64) -> str:

    """ Generates secure random key
     of default size 512 bits
     (64 * 8 = 512 bits) """

    scr = []
    for i in range(length):
        scr += secrets.choice(string.printable)
    return "".join(scr)

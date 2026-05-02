from sha256 import sha256
from string import digits, ascii_letters, punctuation
import itertools

original_message = "give my friend 2 bitcoins for a pizza"

for padding in itertools.product(digits + ascii_letters + punctuation, repeat=20):
    sha = sha256(''.join(padding)+original_message)
    if sha.startswith("00000000"):
        print("Prefix found:")
        print(''.join(padding))
        break
else:
    print("Unluck")
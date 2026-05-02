from sha256 import sha256
import re

GIVEN_HASH = "36:A7:60:17:49:FB:AD:99:5A:97:79:E2:C8:A2:B6:89:1D:03:98:70:FF:40:E3:4B:E2:0D:A3:A4:BF:CC:EB:E0"

with open('certificate.der', 'rb') as f:
    data = f.read()

extracted_hash = ":".join(re.findall("..", sha256(data))).upper()
print(extracted_hash)
print(('Fingerprint is wrong', 'Fingerprint is correct')[extracted_hash == GIVEN_HASH])
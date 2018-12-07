################################################################################
# 1) hash
import hashlib
import struct

# we have 2 levels of indentation because this is precisely how Golang would
# extract it into the json.RawMessage field
msg = """{
        "type": "issueTx",
        "userId": 1,
        "transaction": {
            "amount": 10123.50
        }
    }"""

h = hashlib.sha256()
# the .encode("utf-8") is to convert from a Python string to raw bytes
h.update(msg.encode("utf-8"))

# print out the hexadecimal version of the digest
print(h.hexdigest())
# should print:
# 47b17caac45041a19dc8b03921389c55756d9719ad091125ef8f139b99becb96

# print out the binary version of the digest (this is what we really want)
print(h.digest())
# should print:
# b'G\xb1|\xaa\xc4PA\xa1\x9d\xc8\xb09!8\x9cUum\x97\x19\xad\t\x11%\xef\x8f\x13\x9b\x99\xbe\xcb\x96'

################################################################################
# 2) ecdsa
import ecdsa

# load the private/signing key from the key we generated earlier using OpenSSL
sk = ecdsa.SigningKey.from_pem(open("user1.key").read())
# use the hash from earlier to compute the signature
msg_sha256_hash = b'G\xb1|\xaa\xc4PA\xa1\x9d\xc8\xb09!8\x9cUum\x97\x19\xad\t\x11%\xef\x8f\x13\x9b\x99\xbe\xcb\x96'
# compute the signature! (and convert to DER format)
sig = sk.sign_digest(
    msg_sha256_hash,
    sigencode=ecdsa.util.sigencode_der,
)
print(sig)

# on my machine, with my key:
# b'0E\x02 \x19(\xa3\x11\xb6\xb8V^HG\x9a\x7f\x95\xe1\xe6\x15\x8b\xc5\xc2\x863\x10\x99\xcd\xf9\xcf\xb2\x13\xa1\xdbl\xb6\x02!\x00\xc1R\xc0hh\\qK\xfcR\x18\x02\xdb\xddj5kq\xacf\xb0_jO\xb0\x8e\xd4P\x0f\xfb@\xb3'

with open("signature.der", "wb") as f:
    f.write(sig)
################################################################################
# 3) sinature internal
from asn1crypto.core import Sequence

# our ECDSA signature from earlier
sig = b'0E\x02 \x19(\xa3\x11\xb6\xb8V^HG\x9a\x7f\x95\xe1\xe6\x15\x8b\xc5\xc2\x863\x10\x99\xcd\xf9\xcf\xb2\x13\xa1\xdbl\xb6\x02!\x00\xc1R\xc0hh\\qK\xfcR\x18\x02\xdb\xddj5kq\xacf\xb0_jO\xb0\x8e\xd4P\x0f\xfb@\xb3'
# parse the ASN.1 sequence from this signature
seq = Sequence.load(sig)
# print the native (Pythonic) representation of this ASN.1 object
print(seq.native)
# on my machine, prints:
# OrderedDict([('0', 11379620559389084367780510252548132663400275028223528508518721806165041966262), ('1', 87442589186005784642307971049779867575540489022841522355105800395127625826483)])

# print out the key/value pairs embedded in the sequence in hexadecimal
for k, v in seq.native.items():
    print("%s => %X" % (k, v))
# on my machine, prints:
# 0 => 1928A311B6B8565E48479A7F95E1E6158BC5C286331099CDF9CFB213A1DB6CB6
# 1 => C152C068685C714BFC521802DBDD6A356B71AC66B05F6A4FB08ED4500FFB40B3


################################################################################
# 4) openssl
import os
os.system("openssl asn1parse -inform DER -in signature.der")

################################################################################
# base64
import base64

# now base64-encode the signature
b64sig = base64.b64encode(sig)
print(b64sig)
# on my machine, prints:
# b'MEUCIBkooxG2uFZeSEeaf5Xh5hWLxcKGMxCZzfnPshOh22y2AiEAwVLAaGhccUv8UhgC291qNWtxrGawX2pPsI7UUA/7QLM='

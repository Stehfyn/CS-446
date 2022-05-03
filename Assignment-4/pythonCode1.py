# @auth: Stephen Foster May '22 CS-446
# @repo: github.com/Stehfyn/CS-446/Assignment-4/
# @file: pythonCode1.py
# @vers: 1.0

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random

from os import system
from socket import gethostname
from OpenSSL import crypto

def output_to_file(_out_file: str, _data :str, _mode :str = 'a') -> None:
	fout = open(_out_file, _mode)
	fout.write(_data)
	fout.close()

blackblankimage = random.randint(0, 255) * np.ones(shape=[512, 512, 3], dtype=np.uint8)
cv.putText(blackblankimage, "You did it!", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255))
cv.rectangle(blackblankimage, pt1=(200,200), pt2=(300, 300), color=(0,0,255), thickness=-1)
plt.axis('off')
plt.imshow(blackblankimage)
plt.savefig("./pythonCode1Image.png")

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

certificate = crypto.X509()
certificate.get_subject().C = "US"
certificate.get_subject().ST = "NV"
certificate.get_subject().L = "Reno"
certificate.get_subject().O = "University of Nevada, Reno"
certificate.get_subject().OU = "CSE"
certificate.get_subject().CN = gethostname()

FIVEYEARS = 60*60*24*365*5
certificate.gmtime_adj_notBefore(0)
certificate.gmtime_adj_notAfter(FIVEYEARS)

SN = 42
certificate.set_serial_number(SN)
certificate.set_issuer(certificate.get_subject())
certificate.set_pubkey(key)

certificate.sign(key, "sha512")

output_to_file("stephenfoster_privateKey.PEM", 
                crypto.dump_privatekey(crypto.FILETYPE_PEM, key),
                "wb")
output_to_file("stephenfoster_selfSignedCertificate.crt",
                crypto.dump_certificate(crypto.FILETYPE_PEM, certificate),
                "wb")

system("openssl rsa -in stephenfoster_privateKey.PEM -pubout -out stephenfoster_publicKey.PEM")
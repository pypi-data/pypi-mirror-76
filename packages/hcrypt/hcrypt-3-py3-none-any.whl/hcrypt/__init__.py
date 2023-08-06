from os import stat
from os import path
from os import remove
from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
version = "1"
bufferSize = 64 * 1024
maxPassLen = 32
AESBlockSize = 16

def stretch(passw, iv1):
    digest = iv1 + (16 * b"\x00")
    for i in range(8192):
        passHash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        passHash.update(digest)
        passHash.update(bytes(passw, "utf_16_le"))
        digest = passHash.finalize()
    return digest

def encryptFile(infile, outfile, passw, bufferSize):
    try:
        with open(infile, "rb") as fIn:
            if path.isfile(outfile):
                if path.samefile(infile, outfile):
                    raise ValueError("Both Files are Same !")
            try:
                with open(outfile, "wb") as fOut:
                    encryptStream(fIn, fOut, passw, bufferSize)
            except IOError:
                raise IOError("Can't Write output File !")
    except IOError:
        raise IOError("Source File '" + infile + "' not found.")

def encryptStream(fIn, fOut, passw, bufferSize):
    if bufferSize % AESBlockSize != 0:
        raise ValueError("Size must be a multiple AES block size !")
    if len(passw) > maxPassLen:
        raise ValueError("Password too long !")
    iv1 = urandom(AESBlockSize)
    key = stretch(passw, iv1)
    iv0 = urandom(AESBlockSize)
    intKey = urandom(32)
    cipher0 = Cipher(algorithms.AES(intKey), modes.CBC(iv0),
                     backend=default_backend())
    encryptor0 = cipher0.encryptor()
    hmac0 = hmac.HMAC(intKey, hashes.SHA256(),
                      backend=default_backend())
    cipher1 = Cipher(algorithms.AES(key), modes.CBC(iv1),
                     backend=default_backend())
    encryptor1 = cipher1.encryptor()
    c_iv_key = encryptor1.update(iv0 + intKey) + encryptor1.finalize()
    hmac1 = hmac.HMAC(key, hashes.SHA256(),
                      backend=default_backend())
    hmac1.update(c_iv_key)
    fOut.write(bytes("AES", "utf8"))
    fOut.write(b"\x02")
    fOut.write(b"\x00")
    cby = "HCRYPT 2.0 \n\n CREATED BY TAHMID RAYAT | HTR-TECH \n Github : https://github.com/htr-tech \n Instagram : https://instagr.am/tahmid.rayat\n\n  "
    fOut.write(b"\x00" + bytes([1+len("ENCODED BY"+cby)]))
    fOut.write(bytes("ENCODED BY", "utf8") + b"\x00" +
               bytes(cby, "utf8"))
    fOut.write(b"\x00\x80")
    for i in range(128):
        fOut.write(b"\x00")
    fOut.write(b"\x00\x00")
    fOut.write(iv1)
    fOut.write(c_iv_key)
    fOut.write(hmac1.finalize())
    while True:
        fdata = fIn.read(bufferSize)
        bytesRead = len(fdata)
        if bytesRead < bufferSize:
            fs16 = bytes([bytesRead % AESBlockSize])
            if bytesRead % AESBlockSize == 0:
                padLen = 0
            else:
                padLen = 16 - bytesRead % AESBlockSize
            fdata += bytes([padLen])*padLen
            cText = encryptor0.update(fdata) \
                    + encryptor0.finalize()
            hmac0.update(cText)
            fOut.write(cText)
            break
        else:
            cText = encryptor0.update(fdata)                                
            hmac0.update(cText)
            fOut.write(cText)
    fOut.write(fs16)
    fOut.write(hmac0.finalize())

def decryptFile(infile, outfile, passw, bufferSize):
    try:
        with open(infile, "rb") as fIn:
            if path.isfile(outfile):
                if path.samefile(infile, outfile):
                    raise ValueError("Both Files are Same !")
            try:
                with open(outfile, "wb") as fOut:
                    inputFileSize = stat(infile).st_size
                    try:
                        decryptStream(fIn, fOut, passw, bufferSize,
                                      inputFileSize)
                    except ValueError as exd:
                        raise ValueError(str(exd))
            except IOError:
                raise IOError("Can't Write output File !")
            except ValueError as exd:
                remove(outfile)
                raise ValueError(str(exd))
    except IOError:
        raise IOError("Source File '" + infile + "' not found.")

def decryptStream(fIn, fOut, passw, bufferSize, inputLength):
    if bufferSize % AESBlockSize != 0:
        raise ValueError("Size must be a multiple AES block size !")
    if len(passw) > maxPassLen:
        raise ValueError("Password is too long !")
    fdata = fIn.read(3)
    if (fdata != bytes("AES", "utf8") or inputLength < 136):
            raise ValueError("File Corrupted or not AES Crypted !!")
    fdata = fIn.read(1)
    if len(fdata) != 1:
        raise ValueError("File is corrupted !!")
    if fdata != b"\x02":
        raise ValueError("Invalid AES Crypt Format.")
    fIn.read(1)
    while True:
        fdata = fIn.read(2)
        if len(fdata) != 2:
            raise ValueError("File is corrupted !!")
        if fdata == b"\x00\x00":
            break
        fIn.read(int.from_bytes(fdata, byteorder="big"))
    iv1 = fIn.read(16)
    if len(iv1) != 16:
        raise ValueError("File is corrupted !!")
    key = stretch(passw, iv1)
    c_iv_key = fIn.read(48)
    if len(c_iv_key) != 48:
        raise ValueError("File is corrupted !!")
    hmac1 = fIn.read(32)
    if len(hmac1) != 32:
        raise ValueError("File is corrupted !!")
    hmac1Act = hmac.HMAC(key, hashes.SHA256(),
                         backend=default_backend())
    hmac1Act.update(c_iv_key)
    if hmac1 != hmac1Act.finalize():
        raise ValueError("Invalid Password or File Corrupted !!")
    cipher1 = Cipher(algorithms.AES(key), modes.CBC(iv1),
                     backend=default_backend())
    decryptor1 = cipher1.decryptor()
    iv_key = decryptor1.update(c_iv_key) + decryptor1.finalize()
    iv0 = iv_key[:16]
    intKey = iv_key[16:]
    cipher0 = Cipher(algorithms.AES(intKey), modes.CBC(iv0),
                     backend=default_backend())
    decryptor0 = cipher0.decryptor()
    hmac0Act = hmac.HMAC(intKey, hashes.SHA256(),
                         backend=default_backend())
    while fIn.tell() < inputLength - 32 - 1 - bufferSize:
        cText = fIn.read(bufferSize)
        hmac0Act.update(cText)
        fOut.write(decryptor0.update(cText))
    while fIn.tell() < inputLength - 32 - 1 - AESBlockSize:
        cText = fIn.read(AESBlockSize)
        hmac0Act.update(cText)
        fOut.write(decryptor0.update(cText))
    if fIn.tell() != inputLength - 32 - 1:
        cText = fIn.read(AESBlockSize)
        if len(cText) < AESBlockSize:
            raise ValueError("File is corrupted !!")
    else:
        cText = bytes()
    hmac0Act.update(cText)
    fs16 = fIn.read(1)
    if len(fs16) != 1:
        raise ValueError("File is corrupted !!")
    pText = decryptor0.update(cText) + decryptor0.finalize()
    toremove = ((16 - fs16[0]) % 16)
    if toremove != 0:
        pText = pText[:-toremove]
    fOut.write(pText)
    hmac0 = fIn.read(32)
    if len(hmac0) != 32:
        raise ValueError("File is corrupted !!")
    if hmac0 != hmac0Act.finalize():
        raise ValueError("File is corrupted !!")   

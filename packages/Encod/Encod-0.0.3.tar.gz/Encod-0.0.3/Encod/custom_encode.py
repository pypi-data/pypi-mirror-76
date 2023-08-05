import base64
import random

RANDCHAR = random.randint(66, 124)


def encrypter(fileToEncrypt):
    global RANDCHAR


    encrypted = fileToEncrypt.encode("utf-8")

    encryptIn64 = base64.b64encode(encrypted)

    encryptIn85 = base64.a85encode(encryptIn64)

    final = encryptIn85.decode()

    

    asciiDictRev = {chr(i): i for i in reversed(range(128))}

    returnSentence = ""

    for letter in final:
        for key, value in asciiDictRev.items():
            if letter == key:
                returnSentence = "".join([returnSentence, chr(RANDCHAR) + str(value)])

    return returnSentence

   


def decrypter(fileToDecrypt):
    global RANDCHAR

    asciiDict = {i: chr(i) for i in range(128)}

    toDecryptList = fileToDecrypt.split(chr(RANDCHAR))

    returnSentence = ""

    for section in toDecryptList:
        for key, value in asciiDict.items():
            if str(key) == section:
                returnSentence = "".join([returnSentence, value])


    bcc = returnSentence.encode("utf-8")

    bcc2 = base64.a85decode(bcc)

    bcc3 = base64.b64decode(bcc2)


    return bcc3.decode()

import base64


def encrypter(fileToEncrypt):
    


    encrypted = fileToEncrypt.encode("utf-8")

    encryptIn64 = base64.b64encode(encrypted)

    encryptIn85 = base64.a85encode(encryptIn64)

    final = encryptIn85.decode()


    asciiDictRev = {chr(i): i for i in reversed(range(128))}

    returner = "".join("#" + str(value) for letter in final for key, value in asciiDictRev.items() if letter == key)

    return returner

   


def decrypter(fileToDecrypt):

    asciiDict = {i: chr(i) for i in range(128)}

    toDecryptList = fileToDecrypt.split("#")


    returner = "".join(value for section in toDecryptList for key, value in asciiDict.items() if str(key) == section)


    bcc = returner.encode("utf-8")

    bcc2 = base64.a85decode(bcc)

    bcc3 = base64.b64decode(bcc2)


    return bcc3.decode()

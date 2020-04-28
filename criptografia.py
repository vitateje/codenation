# CRIPTOGRAFIA DE JULIO CESAR
# CODENATION

import requests
from flask import Flask, jsonify, request
from requests import api
import json
import hashlib
import pyperclip

from pprint import pprint

# URL - JSON

entrada_criptografia = f"https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=6c9fa857b2c3374fc411908ccdad48d4e74025ba"

retorno = api.get(entrada_criptografia).json() # consumo a API e transformo ela em JSON

# INFOS

numero_casas = json.dumps(retorno['numero_casas'])
token = json.dumps(retorno['token'])
cifrado = json.dumps(retorno['cifrado'])
decifrado = json.dumps(retorno['decifrado'])
#decifrado = "vitor"
resumo_criptografico = json.dumps(retorno['resumo_criptografico'])

dic_com_entrada = json.dumps(retorno['decifrado']) # transforma dicionário em string


print(cifrado)
if '"' in cifrado:
    for i in range(0,len(cifrado)):
        cifrado_tratado = cifrado.replace(cifrado[0],"")
    print(cifrado_tratado)

# DECIFRA + REGRAS:

# Caesar Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import pyperclip

# the string to be encrypted/decrypted
message = cifrado_tratado

# the encryption/decryption key
key = 3

# tells the program to encrypt or decrypt
mode = 'decrypt' # set to 'encrypt' or 'decrypt'

# every possible symbol that can be encrypted
LETTERS = 'abcdefghijklmnopqrstuvwxyz' # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# stores the encrypted/decrypted form of the message
translated = ''

# !capitalize the string in message
message = message.lower()

# run the encryption/decryption code on each symbol in the message string
for symbol in message:
    if symbol in LETTERS:
        # get the encrypted (or decrypted) number for this symbol
        num = LETTERS.find(symbol) # get the number of the symbol
        if mode == 'encrypt':
            num = num + key
        elif mode == 'decrypt':
            num = num - key

        # handle the wrap-around if num is larger than the length of
        # LETTERS or less than 0
        if num >= len(LETTERS):
            num = num - len(LETTERS)
        elif num < 0:
            num = num + len(LETTERS)

        # add encrypted/decrypted number's symbol at the end of translated
        translated = translated + LETTERS[num]

    else:
        # just add the symbol without encrypting/decrypting
        translated = translated + symbol

# print the encrypted/decrypted string to the screen
print(translated)

# copy the encrypted/decrypted string to the clipboard
pyperclip.copy(translated)

# HASHING:

criptografico = hashlib.sha1(b'{decifrado}').hexdigest()

# ATUALIZA JSON

def atualiza_json(retorno, cifrado_tratado, translated,criptografico):
    
    numero_casas = retorno ["numero_casas"]
    token = retorno ["token"]
    cifrado = cifrado_tratado
    decifrado = translated
    resumo_criptografico = criptografico
    dic = {"numero_casas":numero_casas, "token": token, "cifrado":cifrado, "decifrado":decifrado, "resumo_criptografico":resumo_criptografico}
    return dic
    #pass

teste_atualiza = atualiza_json(retorno,cifrado_tratado,translated,criptografico)


# FILE:

arquivo = open("answer.json", "w")

teste_atualiza_to = json.dumps(teste_atualiza) # stringfy

arquivo.write(teste_atualiza_to)

arquivo.close()


# ENVIA:

url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=6c9fa857b2c3374fc411908ccdad48d4e74025ba'

#answer = {'answer': (open("answer.json", "rb")}
answer = {'answer': open('answer.json', 'rb')}

response = requests.post(url, files=answer)

print(response.text) # CHECK ENVIO 
print(response.headers) # CHECK ENVIO

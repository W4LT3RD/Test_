"""
Cifrado Hill
Notación importante:
K = Matriz llave
P = Vector del texto (en números)
C = Vector de texto cifrado (en números)
C = E (K, P) = K * P (módulo X) - X es la longitud del alfabeto utilizado
P = D (K, C) = inv (K) * C (módulo X) - X es la longitud del alfabeto utilizado
"""
import numpy as np
from egcd import egcd # pip install librerías

alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_to_index = dict(zip(alphabet, range(len(alphabet)))) # Establece el rango de letras a números
index_to_letter = dict(zip(range(len(alphabet)), alphabet)) # Establece el rando de número a letras


def matrix_mod_inv(matrix, modulus):
    """Encontramos el módulo de matriz inversa por medio de los siguientes pasos:
    Paso 1) Encuentra determinante
    Paso 2) Encuentre el valor determinante en un módulo específico (generalmente la longitud del alfabeto)
    Paso 3) Tome ese det_inv multiplicado por la matriz invertida det * (esta será la adjunta) en el módulo
    """

    det = int(np.round(np.linalg.det(matrix)))  # Paso 1)
    det_inv = egcd(det, modulus)[1] % modulus  # Paso 2)
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )  # Paso 3)

    return matrix_modulus_inv


def encrypt(message, K):
    encrypted = ""
    message_in_numbers = []

    for letter in message:
        message_in_numbers.append(letter_to_index[letter]) #Proceso para transformar el mensaje en números

    split_P = [
        message_in_numbers[i : i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0])) 
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[" "])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]  # longitud del mensaje cifrado (en números)

        # Se regresa texto encriptado:
        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted


def decrypt(cipher, Kinv):
    decrypted = ""
    cipher_in_numbers = []

    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    split_C = [
        cipher_in_numbers[i : i + int(Kinv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted

def main():
    print("")
    message2 = input("Ingrese el texto a cifrar: ")
    message2 = message2.lower().strip().replace(" ", "")
    print(message2)
    message=message2

   
    print("")
    print(f"Ahora ingrese los valores de la matriz llave")

    a1 = int(input("Ingrese el valor [0,0]: "))
    a2 = int(input("Ingrese el valor [0,1]: "))
    b1 = int(input("Ingrese el valor [1,0]: "))
    b2 = int(input("Ingrese el valor [1,1]: "))

    K = np.matrix([[a1, a2], [b1, b2]])
    Kinv = matrix_mod_inv(K, len(alphabet))

    encrypted_message = encrypt(message, K)
    decrypted_message = decrypt(encrypted_message, Kinv)


    print("")
    print("¿Qué desa hacer con el texto escrito?")
    print("")
    print("1) Ver mensaje original")
    print("2) Ver mensaje encriptado")
    print("3) Ver mensaje desencriptado")
    print("4) Hacer todos los procesos")
    print("")


    num = int(input("Introduzca el número del proceso que desea hacer: "))
    print("_____________________________________________________")
    print("")
    if 0<num<5:
        if(num==1):
            print(f"Mensaje original: " + message)
        if(num==2):
            print(f"Mensaje encriptado: " + encrypted_message)
        if(num==3):
           print(f"Mensaje desencriptado: " + decrypted_message)
        if(num==4): 
            print(f"Mensaje original: " + message)
            print("")
            print(f"Mensaje encriptado: " + encrypted_message)
            print("")
            print(f"Mensaje desencriptado: " + decrypted_message)
    else:
        print(f"Número incorrecto")
    print("_____________________________________________________")
main()
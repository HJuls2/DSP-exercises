import numpy as np
import random as rand


### -------------- MODULAR ALGEBRA AND MATRICES SUPPORT FUNCTIONS------------------- ###
        

def is_modular_invertible(matrix,modulus=26):
    return True if np.gcd(int(round(np.linalg.det(matrix))),modulus) == 1 else False

def random_invertible_matrix(dimension, modulus = 26):
    ''' Build a matrix that is modular invertible '''
    matrix = np.random.randint(low = 0, high = modulus, dtype = int , size = (dimension,dimension))
    while not is_modular_invertible(matrix) and inverse_element(int(round(np.linalg.det(matrix)))) is None:
        matrix = np.random.randint(low = 0, high = modulus, dtype = int, size = (dimension,dimension))
    return matrix

def inverse_element(element, modulus=26):
    inverse = [i for i in range(0,25) if (element*i)%modulus == 1]
    return inverse[0] if len(inverse) != 0 else None

def cofactor_matrix(matrix):
    return np.linalg.inv(matrix).T * np.linalg.det(matrix)

def compute_modular_inverse_matrix(matrix, modulus = 26):
    ''' Compute the modular (mod modulus) inverse matrix of a given matrix'''
    determinant = int(round(np.linalg.det(matrix)))
    if(np.gcd(determinant, modulus) == 1):
        inverse_determinant = inverse_element(determinant)
        cof_matrix = cofactor_matrix(matrix)
        inverse_matrix = np.dot(inverse_determinant,cof_matrix.transpose())
        for i in range(0, inverse_matrix.shape[0]):
            for j in range(0, inverse_matrix.shape[1]):
                inverse_matrix[i][j] = round(inverse_matrix[i][j])%modulus
    return inverse_matrix


### --------------------  CIPHER/DECIPHER/ATTACK FUNCTIONS --------------------------------- ###

def build_blocks(text,block_length):
    return [text[i:i+block_length].upper() for i in range(0,len(text),block_length)]


def cipher_decipher_block(block_text,matrix,alphabet):
    block_array = np.array([alphabet.index(letter) for letter in block_text.upper()]).transpose()
    return "".join([alphabet[int(number)%26] for number in np.dot(matrix,block_array)])


def cipher_text(plaintext,block_length,key_matrix, alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    plaintext_blocks = build_blocks(plaintext,block_length)
    ciphertext_blocks = [cipher_decipher_block(block,key_matrix,alphabet) for block in plaintext_blocks]
    return "".join(ciphertext_blocks), plaintext_blocks, ciphertext_blocks

def decipher_text(ciphertext, inverse_key_matrix, alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    blocks = build_blocks(ciphertext,len(inverse_key_matrix[0]))
    return "".join([cipher_decipher_block(block,inverse_key_matrix, alphabet) for block in blocks])


def known_ciphertext_attack(plaintext_blocks, ciphertext_blocks,block_length, alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    indexes = None
    matrix_P = np.zeros(shape=(block_length, block_length), dtype= int)
    while(not is_modular_invertible(matrix_P)):
        indexes = [ rand.randint(0,len(plaintext_blocks)-1) for i in range(block_length)]
        p_candidates = [plaintext_blocks[i] for i in indexes]
        for block in p_candidates:
            matrix_P[p_candidates.index(block)] = np.array([ alphabet.index(letter) for letter in block], dtype=int)
        matrix_P = matrix_P.transpose()

    inverse_matrix_P = compute_modular_inverse_matrix(matrix_P)

    matrix_C = np.zeros(shape=(block_length, block_length), dtype= int)
    c_candidates = [ciphertext_blocks[i] for i in indexes]
    for block in c_candidates:
        matrix_C[c_candidates.index(block)] = np.array([ alphabet.index(letter) for letter in block],dtype=int)
    matrix_C = matrix_C.transpose()

    key_matrix = np.dot(matrix_C,inverse_matrix_P)

    for i in range(key_matrix.shape[0]):
        for j in range(key_matrix.shape[1]):
            key_matrix[i][j] = int(round(key_matrix[i][j]))%26
    
    return key_matrix
    


### -------------------------------------------------------------------------------------------- ###
def main():
    # Lunghezza testo da cifrare: 216 caratteri in italiano
    print("### ORIGINAL TEXT ###")
    clean_text = "NELLAGELIDAARIANOTTURNALASUAFERITAFUMAVASPETTROSUSSUROLASOFFERENZALOINONDOCOLPISCICONLAPARTEAPPUNTITAQUANDOILTERZOPUGNALEPENETROTRALESUESCAPOLEJONSNOWGRUGNIECADDEDIFACCIANELLANEVENONSENTIMAILAQUARTALAMASOLTANTOILGELO"
    print(clean_text)
    print()
    # Lunghezza blocco 
    m=4
    key_matrix = random_invertible_matrix(m) 
    print( "### KEY MATRIX ###")
    print(key_matrix)
    print()
    
    inverse_matrix = compute_modular_inverse_matrix(key_matrix)
    
    ciphered_text, plaintext_block, ciphertetx_blocks = cipher_text(plaintext = clean_text, block_length = m, key_matrix = key_matrix)
    print( "### ENCRIPTED TEXT ###")
    print(ciphered_text)
    print()
    
    deciphered_text = decipher_text(ciphertext = ciphered_text,inverse_key_matrix = inverse_matrix)
    print( "### PLAINTEXT OBTAINED DECIPHERING CIPHERTEXT ###")
    print(deciphered_text)
    print()

    attacked_key_matrix = known_ciphertext_attack(plaintext_block,ciphertetx_blocks,m)
    print('### KEY MATRIX OBTAINED AFTER ATTACK ###')
    print(key_matrix)

    
if __name__ == "__main__":
    main()
import numpy as np

def build_blocks(text,block_length):
    return [text[i:i+block_length].upper() for i in range(0,len(text),block_length)]

def random_invertible_matrix(dimension, modulus = 26):
    ''' Build a matrix that is invertible and modular invertible '''
    matrix = np.random.randint(low = 0, high = modulus, dtype = int , size = (dimension,dimension))
    while np.gcd(int(round(np.linalg.det(matrix))),modulus) != 1 and np.linalg.det(matrix) != 0.0:
        matrix = np.random.randint(low = 0, high = modulus, dtype = int, size = (dimension,dimension))
    return matrix

def inverse_element(element, modulus=26):
    inverse = [i for i in range(0,25) if (element*i)%modulus == 1]
    return inverse[0]

def cofactor_matrix(matrix):
    return np.linalg.inv(matrix).T * np.linalg.det(matrix)

def compute_modular_inverse_matrix(matrix, modulus = 26):
    ''' Compute the modular (mod modulus) inverse matrix of a given matrix'''
    determinant = int(round(np.linalg.det(matrix)))
    print( "### KEY MATRIX DETERMINANT ###")
    print(determinant)
    if(np.gcd(determinant, modulus) == 1):
        inverse_determinant = inverse_element(determinant)
        cof_matrix = cofactor_matrix(matrix)
        print('### COFACTOR MATRIX ###')
        print(cof_matrix)
        inverse_matrix = np.dot(inverse_determinant,cof_matrix.transpose())
        for i in range(0, inverse_matrix.shape[0]):
            for j in range(0, inverse_matrix.shape[1]):
                inverse_matrix[i][j] = round(inverse_matrix[i][j])%modulus
    return inverse_matrix

### ------------------------------------------------------------------------------------------- ###

def cipher_block(alphabet,block_text,key_matrix):
    block_array = np.array([alphabet.index(letter) for letter in block_text.upper()]).transpose()
    ciphered_block = np.dot(key_matrix,block_array)
    return "".join([alphabet[int(number)%26] for number in ciphered_block])

def decipher_block(alphabet, block_text,inverse_key_matrix):
    block_array = np.array([alphabet.index(letter) for letter in block_text.upper()]).transpose()
    block = np.dot(inverse_key_matrix,block_array)
    return "".join([alphabet[int(number)%26] for number in block])



### -------------------------------------------------------------------------------------------- ###

def cipher_text(alphabet,text,block_length,key_matrix):
    blocks = build_blocks(text,block_length)
    return "".join([cipher_block(alphabet, block,key_matrix) for block in blocks])

def decipher_text(alphabet,ciphered_text, inverse_key_matrix):
    blocks = build_blocks(ciphered_text,len(inverse_key_matrix[0]))
    return "".join([decipher_block(alphabet,block,inverse_key_matrix) for block in blocks])


### -------------------------------------------------------------------------------------------- ###

def main():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Lunghezza testo da cifrare: 216 caratteri in italiano
    print("### ORIGINAL TEXT ###")
    clean_text = "NELLAGELIDAARIANOTTURNALASUAFERITAFUMAVASPETTROSUSSUROLASOFFERENZALOINONDOCOLPISCICONLAPARTEAPPUNTITAQUANDOILTERZOPUGNALEPENETROTRALESUESCAPOLEJONSNOWGRUGNIECADDEDIFACCIANELLANEVENONSENTIMAILAQUARTALAMASOLTANTOILGELO"
    print(clean_text)
    # Lunghezza blocco 
    m=8
    key_matrix = random_invertible_matrix(m) 
    print( "### KEY MATRIX ###")
    print(key_matrix)
    
    inverse_matrix = compute_modular_inverse_matrix(key_matrix)
    print(" ### INVERSE KEY MATRIX ###")
    print(inverse_matrix)

    ciphered_text = cipher_text(alphabet = alphabet, text = clean_text, block_length = m, key_matrix = key_matrix)
    print( "### ENCRIPTED TEXT ###")
    print(ciphered_text)
    
    deciphered_text = decipher_text(alphabet = alphabet, ciphered_text = ciphered_text,inverse_key_matrix = inverse_matrix)
    print( "### DECIPHERED TEXT ###")
    print(deciphered_text)

    
   



if __name__ == "__main__":
    main()
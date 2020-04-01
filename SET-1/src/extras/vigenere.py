import numpy as np

def vigenere_table(text,alphabet,key_length):
    alphabet='0'+alphabet

    if( len(text)%key_length != 0):
        num_placeholder_to_append = key_length - len(text)%key_length
        string_to_append = "".join(['0' for i in range(0,num_placeholder_to_append)])
        text = text + string_to_append

    letters = [alphabet.index(letter) for letter in text]
    columns = [np.array(letters[i:i+key_length]) for i in range(0,len(letters),key_length)]
    table = np.matrix(columns).transpose()
    #print(table)
    return table

def compute_coincidence_index(np_vector):
    vector = np_vector.tolist()[0]
    n = len(vector)
    occurrences = [vector.count(i) for i in range(1,27)]
    print(sum([(occur*(occur-1))/(n*(n-1)) for occur in occurrences]))


def compute_Mg(np_vector, letters_probabilities, g):
    vector = np_vector.tolist()[0]
    #print(vector)
    #print(letters_probabilities)
    occurrences = {i-1:vector.count(i) for i in range(1,27)}
    #print(occurrences)

    print(sum([ letters_probabilities[j]*(occurrences[(j+g)%26]/len(vector)) for j in range(0,26)]))


if __name__ == "__main__":
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = 'PNHEUAAMRMSLYZPSKWAUGAICLLMEDMDEGAEYAEZOWSEIGBWZUTJTYYFWRLEHFWFWRJWIAZLPYMMYPMGRFXPQHVOWVIZOJMLPZMLRVCHIYMMXLALNUUQWRKIXPVOFLJAFGAIHHGEHVEAOQVMEPHPNCCBEYEIEPMCWRQETENGVKWHNRLPDVXHJLAZFTMGRFXRZABSAKRTEEXAZBTOBVKGCURSFJWFLUBAUAEIDZGZUNCDEZBROLLEOJRQPUXVZPKLLCWUNGAIHHGSEJYUDUHTPMCWLPUQMVZLEJIECYQAMRUSOFBSEJMXDVXVDHQOAEYESNLWTUEPRVYXWNRWZUBSECMAKBNXQVZEHVQQCBGWAPZLTFPEYBNOYVEUUJRMSPBXTGMYRFZQSCBICYMEECJEUFGSHOMSEJGFAGXHEBZYEURAHVLGZSTPAXSQTERMYNBZRVKQMOXVHOIEHVUMSFNTAVAPDKMEALHLJLANAEUQOSYICFWFAECECBKXNPBTZVLPECNXJAWLPCYOEBYKCLIEEIQMFRMCEOMRRRTQCNFMWSMDAZBFHRZVLCM'
    letters_probabilities = dict([
        (0,0.08167), (1,0.01492), (2,0.02782), (3,0.04253), (4,0.12702), (5,0.02228), (6,0.02015), (7,0.06094), (8,0.06966), (9,0.00153), (10,0.00772),
        (11, 0.04025), (12,0.02406), (13,0.06749), (14,0.07507), (15,0.01929), (16,0.00095), (17,0.05987), (18,0.06327), (19,0.09056), (20,0.02758),
        (21, 0.00978), (22,0.02360), (23,0.00150), (24,0.01974), (25,0.00074)])
    key= [alphabet.index(letter)+1 for letter in 'HILARYMANTEL']

    print(key)
    
    #print("LUNGHEZZA CIPHERTEXT:" + str(len(text)))
    table = vigenere_table(text=text, alphabet=alphabet,key_length= 12)
    for i in range(0,table.shape[0]):
        #compute_coincidence_index(table[i,:])
        compute_Mg(table[i,:],letters_probabilities, key[i])

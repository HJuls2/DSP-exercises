import operator

def create_huffman_code(alphabet, distribution):
    alphabet = alphabet.lower()
    dictionary = { alphabet[i]:distribution[i] for i in range(len(alphabet))}

    sequence = [dictionary]

    while len(dictionary) > 2:
        dictionary = manage_dictionary(dictionary)
        sequence.insert(0,dictionary)

    #print(sequence)
    
    step = sorted(sequence.pop(0).items(),reverse=True,key=lambda item: item[1])
    children_entries = tuple(symbol for symbol,_ in step)
    coding = {'0':children_entries[0], '1': children_entries[1]}

    while len(sequence) > 0:
        #print(step)
        step = sorted(sequence.pop(0).items(),reverse=True,key=lambda item: item[1])
        children_entries = tuple((symbol,probability) for symbol,probability in step if symbol not in coding.values())
        if children_entries[0][1] == children_entries [1][1]:
            children_entries = sorted(children_entries,reverse=True, key= lambda item: len(item[0]))
        #print(children_entries)
        parent_entry_code = next(iter([code for code,key in coding.items() if children_entries[0][0] in tuple(key)]))
        
        if children_entries[0][1] == children_entries[1][1]:
            coding[parent_entry_code+'0'] = children_entries[0][0] if len(children_entries[0][0])<len(children_entries[1][0]) else children_entries[1][0]
            coding[parent_entry_code+'1'] = children_entries[1][0] if len(children_entries[0][0])<len(children_entries[1][0]) else children_entries[0][0]
        else:
            coding[parent_entry_code+'0'] = children_entries[0][0]
            coding[parent_entry_code+'1'] = children_entries[1][0]
    

    return {symbol:code for code,symbol in coding.items() if len(symbol) == 1}
    

def manage_dictionary(dictionary):
    dictionary = { k:v for k,v in sorted(dictionary.items(),key=lambda item: item[1])}
    pair = [item for item in dictionary.items()]
    first,second = pair[0], pair[1]
    del(dictionary[first[0]])
    del(dictionary[second[0]])
    key, value = (first[0], second[0]),first[1]+second[1]
    dictionary[key] = value
    return dictionary


def encode (text, code_dictionary):
    text = ''.join([char.lower() for char in text if char not in ".,;:-_?!\"\'£$%&/*-+()=^|—[]\{\}<>`’0123456789"]).replace(' ','')
    print(f'Cleaned original text: {text}')
    return ''.join([code_dictionary[letter] for letter in text])

def decode(encoded_text, code_dictionary):
    dictionary = {v:k for k,v in code_dictionary.items()}
    min_codeword_length = min([len(codeword) for codeword in dictionary])

    decoded_text = ''
    start, end = 0, min_codeword_length 
    while end <= len(encoded_text):
        if encoded_text[start:end] in dictionary.keys():
            decoded_text += dictionary[encoded_text[start:end]]
            start = end
            end = start + min_codeword_length
        else:
            end += 1

    return decoded_text 


def main():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    distribution = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772,0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
    #alphabet = 'ABCDEFGH'
    #distribution = [0.025,0.025,0.05,0.1,0.13,0.17,0.25,0.25]
    code = create_huffman_code(alphabet, distribution)
    print(code)

    print('Please insert a string with no accent in it')
    text = input()

    encoded_text = encode(text, code)
    print(f'Encoded text: {encoded_text}')

    decoded_text = decode(encoded_text, code)
    print(f'Decoded text: {decoded_text}')


    

if __name__ == "__main__":
    main()

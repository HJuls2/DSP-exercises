import operator

def huffman_encode(alphabet, distribution):
    alphabet = alphabet.lower()
    dictionary = { alphabet[i]:distribution[i] for i in range(len(alphabet))}

    sequence = [dictionary]

    while len(dictionary) > 2:
        dictionary = manage_dictionary(dictionary)
        sequence.insert(0,dictionary)

    print(sequence)
    
    step = list({k:v for k,v in sorted(sequence.pop(0).items(),reverse=True,key=lambda item: item[1])}.keys())
    coding = {'0':step[0], '1': step[1]}

    while len(sequence) > 0:
        children_entries = list({k:v for k,v in sorted(sequence.pop(0).items(),reverse=True,key=lambda item: item[1]) if k not in coding.values()})
        print(children_entries)
        #children_entries = [ key for key in step.keys() if key not in coding.values()]
        parent_entry_code = next(iter([code for code,key in coding.items() if children_entries[0] in key]))
        '''
        if children_entries[0][1] == children_entries[1][1]:
            coding[parent_entry_code+'0'] = children_entries[0][0] if len(children_entries[0][0])<len(children_entries[1][0]) else children_entries[1][0]
            coding[parent_entry_code+'1'] = children_entries[0][1] if len(children_entries[0][0])<len(children_entries[1][0]) else children_entries[1][0]
        else:
        '''
        coding[parent_entry_code+'0'] = children_entries[0]
        coding[parent_entry_code+'1'] = children_entries[1]
            
    return coding
    

def manage_dictionary(dictionary):
    dictionary = { k:v for k,v in sorted(dictionary.items(),key=lambda item: item[1])}
    pair = [item for item in dictionary.items()]
    first,second = pair[0], pair[1]
    del(dictionary[first[0]])
    del(dictionary[second[0]])
    key, value = (first[0], second[0]),first[1]+second[1]
    dictionary[key] = value
    return dictionary

def main():
    #alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #distibution = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772,0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
    alphabet = 'ABCDEFGH'
    distribution = [0.025,0.025,0.05,0.1,0.13,0.17,0.25,0.25]
    a = huffman_encode(alphabet, distribution)
    print(a)
    

if __name__ == "__main__":
    main()

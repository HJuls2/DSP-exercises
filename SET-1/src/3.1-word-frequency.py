import os

import matplotlib.pyplot as plt
import math
import numpy as np

# SUPPORT FUNCTIONS

def open_file(filename):
    file = open(filename,"r")
    text = file.read()
    file.close()
    return text  

def get_clean_text(filename):
    text = open_file(filename).replace("\n","").replace(" ","")
    letters = [char.lower() for char in text if char not in ".,;:-_?!\"\'£$%&/*-+()=^|—[]\{\}<>`’"]
    text = ""
    for letter in letters:
        text += letter
    return text

def calc_m_grams(text,m):
     m_grams = [ text[i:i+m] for i in range(0,len(text)-(m-1))]
     m_grams_set = set(m_grams)
     return m_grams, m_grams_set

def histogram(letter_frequencies, alphabet):
    plt.bar(x = [num for num in range(0,26)], height = letter_frequencies)
    plt.xticks(ticks = np.arange(0,26,step=1), labels=alphabet)
    plt.xlabel('Letter')
    plt.ylabel('Frequency')
    plt.title('Word Frequency Histogram')
    plt.ion()
    plt.show()
    plt.pause(2)


# Function for point 1
def letter_frequency(text, alphabet):
    letters = [char for char in text]
    frequencies = [letters.count(letter)/len(letters) for letter in alphabet]
    return frequencies

# Function for point 2
def m_gram_distribution(text, m):
    m_grams, m_grams_set = calc_m_grams(text,m)
    distribution = {m_gram:m_grams.count(m_gram)/len(m_grams_set) for m_gram in m_grams_set}
    #m_gram_histogram(distribution, [m_gram.upper() for m_gram in m_grams_set])
    return distribution

# Function for point 3a
def coincidence_index(text, alphabet):
    denominator = len(text)*(len(text)-1)
    index_of_coincidence = 0
    for letter in alphabet:
        occurrences = text.count(letter)
        index_of_coincidence += (occurrences*(occurrences-1))/denominator
    return index_of_coincidence


def shannon_entropy(m_gram_distribution):
    return -sum([ p*math.log(p,2) for p in m_gram_distribution.values()])



# Function main to run all the functions sequentially
def main():
    filepath = os.getcwd() + '/SET-1/resources/moby-dick-chapter-1.txt'
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # Load file
    text = get_clean_text(filepath)

    # Build and view letter frequency 
    letter_frequencies = letter_frequency(text, alphabet)
    print(letter_frequencies)
    histogram(letter_frequencies, [letter for letter in alphabet.upper()])

    print("Insert lenght m for the m-grams")
    m = input() # FIXME : check correct input
    distribution = m_gram_distribution(text,int(m))
    print("### EMPIRIC M-GRAMS DISTRIBUTION ###")
    print(distribution)

    index_of_coincidence = coincidence_index(text,alphabet)
    print("### INDEX OF COINCIDENCE ###")
    print(index_of_coincidence)


    entropy = shannon_entropy(distribution)
    print('### SHANNON ENTROPY')
    print(entropy)


if __name__ == "__main__":
    main()
import math

def shannon_entropy():
    letters_probabilities = [0.12702,0.09056,0.08167,0.07507,0.06966,0.06749,0.06327,0.06094, 0.05987, 0.04253, 0.04025,0.02782,0.02758, 
        0.02406, 0.02360, 0.02228, 0.02015, 0.01974, 0.01929, 0.01492, 0.00978,0.00772, 0.00153, 0.00150, 0.00095,0.00074]
    print( -sum([ p*math.log(p,2) for p in letters_probabilities]))


if __name__ == "__main__":
    shannon_entropy()
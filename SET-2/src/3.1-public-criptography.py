import random
import time

# 3.1.1) Algoritmo euclideo esteso
def extended_euclidean_alghorithm(a, b):
    x0, x1 = 0, 1
    y0, y1 = 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    
    return x0, y0, b

# 3.1.2) Algoritmo di esponenziazione modulare veloce
def fast_exponentiation_modular_algh(a,n, modulus):
    nbase2 = bin(n)
    d=1

    for digit in nbase2:
        d = (d**2)%modulus
        if digit == '1':
            d = (d*a)%modulus

    return d

# 3.1.3) Test di Miller-Rabin
def test_rabin(n, x=2):
    _,_,gcd = extended_euclidean_alghorithm(n,x)
    if gcd != 1:
        return False
    
    nm1 = n -1
    support_var = nm1
    r = 0
    while support_var%2 == 0:
        r+=1
        support_var = support_var // 2
    
    m = 1
    support_var = r
    while support_var != 0:
        # Check if 2**r | n-1
        if nm1 % 2**support_var != 0:
            support_var-=1
        else:
            m =  nm1//2**r
            # Check if m is odd
            if m%2 != 0:
                break

    sequence = [1 for i in range(r+1)]
    sequence[0] = fast_exponentiation_modular_algh(x,m,n)
    if sequence[0] == 1 or sequence[0] == nm1:
        return False

    for i in range(1,len(sequence)):
        sequence[i] = fast_exponentiation_modular_algh(sequence[i-1],2,n)
        if sequence[i] == nm1:
            return False

    return True

# 3.1.4) Algoritmo di generazione di numeri primi    
def prime_generator(order):
    #returns a prime number (first value) with probability in second return value
    number = random_number_generator(order)
    witnesses = set(random.randint(2,number-1) for i in range(10))
    results = [test_rabin(number,x) for x in witnesses]
    
    while True in results:
        number = random_number_generator(order)
        witnesses = set(random.randint(2,number-1) for i in range(10))
        results = [test_rabin(number,x) for x in witnesses]
    
    return number, 1-(1/(4**len(witnesses)))

def random_number_generator(order, flags=(False,True)):
    bits = [ flags[random.getrandbits(1)] for i in range(order)]
    bits[0], bits[-1] = True, True
    bin_number = ''
    for b in bits:
        bin_number+= '1' if b is True else '0'
    
    return int(bin_number, 2)


# 3.1.5) Schema RSA con e senza CRT
def define_RSA_scheme(p = None, q = None, useCrt = False):
    if not p and not q:
        p,q = prime_generator(100)[0], prime_generator(100)[0]
    if p < q:
        p,q = q,p
    n, phi_n = p*q, (p-1)*(q-1)

    d = random.randint(0,n-1)
    _,y,gcd = extended_euclidean_alghorithm(phi_n,d)

    while gcd != 1:
        d = random.randint(0,n-1)
        _,y,gcd = extended_euclidean_alghorithm(phi_n,d)

    e =  y%n

    if useCrt:
        return p,q,n,d,e, compute_CRT_params(d,p,q)
    
    return p,q,n,d,e


def compute_CRT_params(d,p,q):
    # p > q
    # return dp,dq, inverse of q modulus p
    _,y,_ = extended_euclidean_alghorithm(p,q)
    return d%(p-1),d%(q-1), y%p

def RSA_encryption(message,e,n):
    return fast_exponentiation_modular_algh(message,e,n)


def RSA_decryption(ciphertext,d,n):
    return fast_exponentiation_modular_algh(ciphertext,d,n)
    
def RSA_CRT_decryption(ciphertext,p,dp,q,dq,qinv):
    m1 = fast_exponentiation_modular_algh(ciphertext,dp,p)
    m2 = fast_exponentiation_modular_algh(ciphertext,dq,q)
    h = qinv * (m1-m2)%p
    return m2 + h*q


def RSA_test():
    p,q,n,d,e = define_RSA_scheme()

    print(f'\np :{p},q: {q}, n: {n}, d: {d}, e: {e}')

    plaintexts = [random.randint(0,n) for i in range(100)]
    print(f'\n### PLAINTEXTS ###\n{plaintexts}')
   
    ciphertexts = [ RSA_encryption(m,e,n) for m in plaintexts]
    print(f'\n### CIPHERTEXTS ###\n{ciphertexts}')
    
    start_time = time.time()
    deciphered_messages = [ RSA_decryption(c,d,n) for c in ciphertexts]
    end_time = time.time()
    print(f'\n### DECIPHERED MESSAGES ###\n{deciphered_messages}')
    
    dp,dq, qinv = compute_CRT_params(d,p,q)
    crt_start_time = time.time()
    deciphered_messages_with_crt = [RSA_CRT_decryption(c,p,dp,q,dq,qinv) for c in ciphertexts]
    crt_end_time = time.time()
    print(f'\n### DECIPHERED MESSAGES WITH CRT ###\n{deciphered_messages_with_crt}')
    

    print("\nDecryption time: %s seconds" %(end_time-start_time))
    print("Decryption time using CRT: %s seconds" %(crt_end_time-crt_start_time))

def RSA_performance():
    p,q,n,d,e = define_RSA_scheme()
    plaintexts = [random.randint(0,n) for i in range(100)]
    ciphertexts = [ RSA_encryption(m,e,n) for m in plaintexts]

    # Time without CRT
    start_time = time.time()
    deciphered_messages = [ RSA_decryption(c,d,n) for c in ciphertexts]
    exec_time = time.time() - start_time

    # Time with CRT
    dp,dq, qinv = compute_CRT_params(d,p,q)
    start_time = time.time()
    deciphered_messages_with_crt = [RSA_CRT_decryption(c,p,dp,q,dq,qinv) for c in ciphertexts]
    crt_exec_time = time.time() -start_time

    return exec_time,crt_exec_time

def compute_es_2_4():
    n = 1200867589138402836833011627922648843865398758356119243237528992192661195883356632897345588719304934438534205354787918897834861577085344762327143956220911721261528444200091612203799709834594997775067917847690315178675148605331912292785817786238119642200812571328900475396454557843711810878201457471117182510681991129539167165552073440243913144926216242708247975357913354302233984628116835035339887667027876020733894592318754941490852771134623356130705203596572659
    c1 =  13740701343175031613859506260680271
    c2 = 442020648620790478265510268903148188611479520134128911

    x,y,gcd = extended_euclidean_alghorithm(n,c1)
    print(f'x:{x}, y: {y}, gcd: {gcd}')
    
    c1_inv = y % n
    a,b = -3,2
    result = (fast_exponentiation_modular_algh(c1_inv,a,n) * fast_exponentiation_modular_algh(c2,b,n)) % n
    print(result)




def main():
    # 3.1.1) Extended euclidean algorithm test
    a,_ = prime_generator(100)
    b,_ = prime_generator(100)
    x,y, gcd = extended_euclidean_alghorithm(a,b)
    print(f'x: {x}, y : {y%60}, GCD(x,y): {gcd}')
    
    # 3.1.2) Fast modular exponentiation algorithm test
    base,exponent,modulus = 7**100,10**100,random.randint(0,10**100)
    d = fast_exponentiation_modular_algh(base,exponent,modulus)
    print(f'\n{d} is the {exponent}-th power of {base} modulus {modulus}')

    # 3.1.3) Miller-Rabin test in action

    # Test with a prime number with different witnesses
    result = test_rabin(167)

    witnesses = [3,5,7,11]
    witnesses_iterator = iter(witnesses)
    witness = next(witnesses_iterator)
    while not result:
        result = test_rabin(167,witness)
        try:
            witness = next(witnesses_iterator)
        except StopIteration:
            break


    print(f'167 returns {result} with 2,3,5,7,11 as witnesses')

    # Test with a composite number
    result = test_rabin(87545265415412418975674774894174892)
    print(f'\n87545265415412418975674774894174892 (a even number --> a composite number) returns {result}')

    # 3.1.4) Prime generation test
    number, probability = prime_generator(order=100)
    print(f'\n{number} is a prime (with probability {probability}) generated using Miller Rabin test')

    #3.1.5) RSA testing
    RSA_test()

    #3.1.6) RSA performance: compute the mean execution time of RSA and RSA optimized with CRT (over 1000 executions)
    times = [RSA_performance() for i in range(1000)]
    mean_exec_time, mean_crt_exec_time = sum([t[0] for t in times])/1000, sum([t[1] for t in times])/1000
    print(f'\nMean execution time of RSA decryption: {mean_exec_time} seconds\nMean execution time of RSA decryption with CRT optimization: {mean_crt_exec_time} seconds')
    print(f'CRT-optimized RSA is {100-(100*mean_crt_exec_time)/mean_exec_time}% faster than the basic RSA')


if __name__ == "__main__":
    main()
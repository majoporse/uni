

def prime_generator(number):
    primes = [x for x in range(1, number)]
    for i in range (2,len(primes)):#vyber cisla
        if i not in primes:
            continue
        for j in range (i, len(primes)):#vyber setkych nasobkov
            if i*j not in primes:
                continue
            primes.remove(i*j)
            
        
        
    
    return primes

print(prime_generator(250))
class Sieve
    def sieve_prime(n):
        prime = [True]*(n+1)
        p = 2
        while(p*p <= n):
            if prime[p] == True:
                for i in range(p*p,n+1,p):
                    prime[i] = False
            p += 1
        return prime

class Sieve:
    def sieve(n):
        prime = [True]*(n+1)
        p = 2
        while(p*p <= n):
            if prime[p] == True:
                for i in range(p*p,n+1,p):
                    prime[i] = False
            p += 1
        return prime

class Sievepy:
	def primes_till_n(n):
	        result = []
	        prime = Sieve.sieve(n)
	        result = [p for p in range(2,n+1) if prime[p]]
	        return result

	def isprime(n):
	        prime = Sieve.sieve(n)
	        if prime[-1] == True:
	            return "Prime"
	        return "Not a Prime"

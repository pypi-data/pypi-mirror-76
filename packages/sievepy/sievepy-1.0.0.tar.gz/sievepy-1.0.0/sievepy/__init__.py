class sieve:
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

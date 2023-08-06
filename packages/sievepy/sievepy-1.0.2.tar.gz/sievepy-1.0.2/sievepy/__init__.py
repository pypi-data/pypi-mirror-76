import Sieve
class sieve:
	def primes_till_n(n):
	        result = []
	        prime = Sieve.sieve_prime(n)
	        result = [p for p in range(2,n+1) if prime[p]]
	        return result

	def isprime(n):
	        prime = Sieve.sieve_prime(n)
	        if prime[-1] == True:
	            return "Prime"
	        return "Not a Prime"

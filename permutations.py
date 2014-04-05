"""This file loop through the possible reasons and generates all possible keys"""

from itertools import permutations
from itertools import product

def per():
	l = ["e", "f", "g", "o", "t"]

	n_l = []
	for x in range(6):
		for p in permutations(l, x):
			n_l.append(tuple(sorted(p)))
			#print n_l

	return n_l
	
def tuples(li):
	tu = {}
	for l in range(len(li)):
		if len(li[l]) > 0:
			if tu.get(li[l]):
				tu[li[l]] += 1
   			else:
   				tu[li[l]] = 1

   	return sorted(tu.keys())


if __name__ == "__main__":
	perm = per()
	tup = tuples(perm)


# []
# ['e']
# ['f']
# ['g']
# ['o']
# ['t']
# ['e', 'f']
# ['e', 'g']
# ['e', 'o']
# ['e', 't']
# ['e', 'f']
# ['f', 'g']
# ['f', 'o']
# ['f', 't']
# ['e', 'g']
# ['f', 'g']
# ['g', 'o']
# ['g', 't']
# ['e', 'o']
# ['f', 'o']
# ['g', 'o']
# ['o', 't']
# ['e', 't']
# ['f', 't']
# ['g', 't']
# ['o', 't']
# ['e', 'f', 'g']
# ['e', 'f', 'o']
# ['e', 'f', 't']
# ['e', 'f', 'g']
# ['e', 'g', 'o']
# ['e', 'g', 't']
# ['e', 'f', 'o']
# ['e', 'g', 'o']
# ['e', 'o', 't']
# ['e', 'f', 't']
# ['e', 'g', 't']
# ['e', 'o', 't']
# ['e', 'f', 'g']
# ['e', 'f', 'o']
# ['e', 'f', 't']
# ['e', 'f', 'g']
# ['f', 'g', 'o']
# ['f', 'g', 't']
# ['e', 'f', 'o']
# ['f', 'g', 'o']
# ['f', 'o', 't']
# ['e', 'f', 't']
# ['f', 'g', 't']
# ['f', 'o', 't']
# ['e', 'f', 'g']
# ['e', 'g', 'o']
# ['e', 'g', 't']
# ['e', 'f', 'g']
# ['f', 'g', 'o']
# ['f', 'g', 't']
# ['e', 'g', 'o']
# ['f', 'g', 'o']
# ['g', 'o', 't']
# ['e', 'g', 't']
# ['f', 'g', 't']
# ['g', 'o', 't']
# ['e', 'f', 'o']
# ['e', 'g', 'o']
# ['e', 'o', 't']
# ['e', 'f', 'o']
# ['f', 'g', 'o']
# ['f', 'o', 't']
# ['e', 'g', 'o']
# ['f', 'g', 'o']
# ['g', 'o', 't']
# ['e', 'o', 't']
# ['f', 'o', 't']
# ['g', 'o', 't']
# ['e', 'f', 't']
# ['e', 'g', 't']
# ['e', 'o', 't']
# ['e', 'f', 't']
# ['f', 'g', 't']
# ['f', 'o', 't']
# ['e', 'g', 't']
# ['f', 'g', 't']
# ['g', 'o', 't']
# ['e', 'o', 't']
# ['f', 'o', 't']
# ['g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'g', 'o']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'g', 'o']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['f', 'g', 'o', 't']
# ['e', 'g', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['f', 'g', 'o', 't']
# ['e', 'g', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 'o']
# ['f', 'g', 'o', 't']
# ['e', 'g', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'g', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'f', 'o', 't']
# ['e', 'f', 'g', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'g', 't']
# ['f', 'g', 'o', 't']
# ['e', 'g', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['e', 'g', 'o', 't']
# ['e', 'f', 'o', 't']
# ['f', 'g', 'o', 't']
# ['e', 'g', 'o', 't']
# ['f', 'g', 'o', 't']


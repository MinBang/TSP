from random import randrange
from random import uniform

roadCost = [[0, 170, 300, 380, 800, 480],
			[170, 0, 1000, 150, 500, 320],
			[300, 1000, 0, 600, 700, 50],
			[380, 150, 600, 0, 100, 1000],
			[800, 500, 700, 100, 0, 700],
            [480, 320, 50, 1000, 700, 0]]
 
class TSP:
	def __init__(self, chromoSize, pSize):
		self.population = []
		self.fitnesses = []
		self.chromoSize = chromoSize
		self.pSize = pSize

		self.mutant = 5
		self.eliteRate = 2
		self.threshold = 2200
		
		self.bestFit = 0
		self.bestChromo = ""

	def evolve(self, studyCount = 1):
		self.initPopulation()
		
		for i in range(studyCount):
			nPopulation = []
			self.fitnesses = []

			self.fitness()
			if self.checkClear():
				self.printScore(i)
				print("")
				print("---------------------------------------")
				print(" C L E A R ! ! ")
				break

			self.elite(nPopulation)

			for j in range(self.pSize - self.eliteRate):
				choiced = []
				self.selection(choiced)
				nChromo = self.crossover(nPopulation, choiced)
				nPopulation.append(nChromo)

			self.population = nPopulation
			self.printScore(i)
		
		print("---------------------------------------")
		print("bestFit : " + str(self.bestFit) + "   bestChromo : " + str(self.bestChromo))
		print("")
	
	## generic method ##
	def fitness(self):
		for i in range(self.pSize):
			sum = 0
			for j in range(0, self.chromoSize-1):
				sum += roadCost[self.population[i][j]][self.population[i][j + 1]]
				
			self.fitnesses.append(3000 - sum)
			
		self.renewBest()	 			             

	def selection(self, choiced):
		choiceRate = []
		sum = 0

		for i in self.fitnesses:
			sum += i

		for i in self.fitnesses:
			choiceRate.append((float(i) / sum) * 100)

		sum = 0.0

		for i in range(2):
			for j in range(len(choiceRate)):
				sum+=choiceRate[j]
				if uniform(0, 100) < sum:
					choiced.append(j)
					break

	def crossover(self, nPopulation, choiced):
		div = randrange(2, self.chromoSize-1)
		
		str1 = self.population[choiced[0]]
		str2 = self.population[choiced[1]]

		re = str1[0:div]
		t = []

		for i in str2:
			if False == self.checkDuplication(re, i):
				t.append(i)

		re += t
		self.mutation(re)

		return re

	def mutation(self, tStr):
		if uniform(0, 100) <= self.mutant:
			idx1 = randrange(self.chromoSize)
			idx2 = randrange(self.chromoSize)

			while idx1 == idx2:
				idx2 = randrange(self.chromoSize)

			self.swapAlphaBat(tStr, idx1, idx2)

	# get two best in generation
	def honors(self):
		re = [0, 0]

		for i in range(self.eliteRate):
			for j in range(self.pSize):
				if i != 0:
					if self.population[re[0]] == self.population[j]:
						continue
				if self.fitnesses[re[i]] < self.fitnesses[j]:
					re[i] = j

		return re

	# set two best in nPopulation
	def elite(self, nPopulation):
		t = self.honors()

		for i in t:
			nPopulation.append(self.population[i])

	# now state
	def printScore(self, i):
		best = 0

		for j in self.fitnesses:
			if best < j:
				best = j

		print("[" + str(i) + "] " + "[" + str(best) + "]")

	# renew the best in world
	def renewBest(self):
		for i in range(self.pSize):
			if self.bestFit < self.fitnesses[i]:
				self.bestFit = self.fitnesses[i];
				self.bestChromo = self.population[i];
	
	# for test
	def printPopulation(self, data):
		for i in data:
			print(i) 

	# check duplication
	def checkDuplication(self, data, t):
		for i in data:
			if t == i:
				return True
		
		return False

	# first population init
	def initPopulation(self):
		while len(self.population) < self.pSize:
			tChromo = []
			
			while len(tChromo) < self.chromoSize:
				t = randrange(self.chromoSize)
				flag = self.checkDuplication(tChromo, t) 
				
				if flag == True:
					continue
					
				tChromo.append(t)

			self.population.append(tChromo)

	def swapAlphaBat(self, data, idx1, idx2):
		t = data[idx1]
		data[idx1] = data[idx2]
		data[idx2] = t

	def checkClear(self):
		for i in self.fitnesses:
			if self.threshold <= i:
				return True

		return False

def run():
	t = TSP(len(roadCost[0]), 10)

	t.evolve(100000)

if __name__ == "__main__":
	run()
    

import math
import random


def euclid(p, q):
    x = p[0] - q[0]
    y = p[1] - q[1]
    return math.sqrt(x * x + y * y)


# Helper function to check the number of non-empty lines in a file
def number_of_lines(givenFilename):
    file = open(givenFilename, "r")
    counted_lines = len(file.readlines())
    file.close()
    return counted_lines


class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.

    def __init__(self, n, filename):
        if n == -1:
            self.n = number_of_lines(filename)

            distances_table = [[0 for i in range(self.n)] for j in range(self.n)]
            cities_indexed = []
            file = open(filename, "r")
            lines = file.readlines()
            for line in lines:
                coordinates = line.split()
                coordinates[0] = int(coordinates[0])
                coordinates[1] = int(coordinates[1])
                cities_indexed.append(coordinates)
            file.close()

            for i in range(self.n):
                for j in range(self.n):
                    distances_table[i][j] = euclid(cities_indexed[i], cities_indexed[j])


        else:
            self.n = n

            distances_table = [[0 for i in range(self.n)] for j in range(self.n)]

            file = open(filename, "r")
            lines = file.readlines()
            for line in lines:
                lineComponents = line.split()
                i = int(lineComponents[0])
                j = int(lineComponents[1])
                dist = int(lineComponents[2])
                distances_table[i][j] = dist
                distances_table[j][i] = dist
            file.close()

        self.dists = distances_table

        self.perm = [i for i in range(self.n)]

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        total_cost = 0

        for i in range(len(self.perm)):
            j = (i + 1) % self.n
            distance = self.dists[self.perm[i]][self.perm[j]]
            total_cost += distance

        return total_cost

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self, i):
        original_permutation = self.perm[:]
        original_distance = self.tourValue()
        permutation_i = self.perm[i]
        self.perm[i] = self.perm[(i + 1) % self.n]
        self.perm[(i + 1) % self.n] = permutation_i

        if self.tourValue() < original_distance:
            return True
        else:
            self.perm = original_permutation
            return False

    # Consider the effect of reversing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self, i, j):
        original_permutation = self.perm[:]
        original_distance = self.tourValue()
        self.perm[i:(j + 1) % self.n] = self.perm[i:(j + 1) % self.n][::-1]

        if self.tourValue() < original_distance:
            return True
        else:
            self.perm = original_permutation
            return False

    def swapHeuristic(self, k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self, k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for j in range(self.n - 1):
                for i in range(j):
                    if self.tryReverse(i, j):
                        better = True

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        used_nodes = [0 for r in range(self.n)]
        count = 0
        current_i = 0
        next_i = 0
        while count < self.n - 1:
            used_nodes[current_i] = 1

            # Finds any distance in order to later be able to find a minimum distance in the next for loop by comparison
            for j in range(self.n):
                if (self.dists[current_i][j] > 0) and (used_nodes[j] != 1):
                    minimum_distance = self.dists[current_i][j]
                    next_i = j
                    break

            for j in range(self.n):
                if (self.dists[current_i][j] < minimum_distance) and (used_nodes[j] != 1):
                    minimum_distance = self.dists[current_i][j]
                    next_i = j

            current_i = next_i
            used_nodes[current_i] = 1
            self.perm[count + 1] = current_i
            count += 1

    # My own algorithm

    def NearestInsertion(self):
        permutations = [0]

        minimum_distances = [(self.dists[0][j], j) for j in range(self.n) if j != 0]
        current_tuple = min(minimum_distances)
        current_i = current_tuple[1]
        minimum_distances.remove(current_tuple)

        permutations.append(current_i)

        while minimum_distances:
            for i in range(len(minimum_distances)):
                minimum_distances[i] = (
                    min(minimum_distances[i][0], self.dists[current_i][minimum_distances[i][1]]),
                    minimum_distances[i][1])

            current_tuple = min(minimum_distances)
            current_i = current_tuple[1]
            minimum_distances.remove(current_tuple)

            # Creates a list of tuples that will store how much distance is added to the tour when inserted at position i+1
            permutations_tuple = []
            for i in range(len(permutations) - 1):
                permutations_tuple.append(
                    (self.dists[permutations[i]][current_i] + self.dists[permutations[i + 1]][current_i]
                     - self.dists[permutations[i]][permutations[i + 1]], i + 1))
            permutations_tuple.append(
                (self.dists[permutations[len(permutations) - 1]][current_i] + self.dists[permutations[0]][current_i]
                 - self.dists[permutations[len(permutations) - 1]][permutations[0]], len(permutations)))

            minimum_permutation = min(permutations_tuple)[1]

            # Inserts current i in the best position
            permutations.insert(minimum_permutation, current_i)

        self.perm = permutations




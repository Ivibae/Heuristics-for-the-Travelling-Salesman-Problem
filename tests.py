import math
import graph
import random
import os
import time
from matplotlib import pyplot as plt


def createEuclidean(no_of_cities, map_size):
    nodes = [(random.randint(0, map_size), random.randint(0, map_size)) for j in range(no_of_cities)]

    file = open(os.path.join(os.getcwd(), "Cities" + str(no_of_cities)), "a")

    for node in nodes:
        file.write(str(node[0]) + " " + str(node[1]) + "\n")
    file.write(str(node[0]) + " " + str(node[1]) + "\n")

    file.close()


def createGeneral(no_of_cities, max_distance):
    edges = []

    for i in range(no_of_cities):
        for j in range(i + 1, no_of_cities):
            edges.append((i, j, random.randint(1, max_distance)))

    file = open(os.path.join(os.getcwd(), str(no_of_cities) + "Nodes"), "a")

    for edge in edges[:-1]:
        file.write(str(edge[0]) + " " + str(edge[1]) + " " + str(edge[2]) + "\n")

    file.write(str(edges[-1][0]) + " " + str(edges[-1][1]) + " " + str(edges[-1][2]))

    file.close()





number_of_cities = 50

x_values = [x for x in range(number_of_cities)]

original_tourvalues = [0 for t in range(number_of_cities)]

swap_2_opt_tourvalues = [0 for t in range(number_of_cities)]
swap_2_opt_time = [0 for t in range(number_of_cities)]

greedy_tourvalues = [0 for t in range(number_of_cities)]
greedy_time = [0 for t in range(number_of_cities)]

nearest_insertion_tourvalues = [0 for t in range(number_of_cities)]
nearest_insertion_time = [0 for t in range(number_of_cities)]


for i in range(2, number_of_cities):
    createEuclidean(i, 150)

    g = graph.Graph(-1, "Cities" + str(i))
    original_tourvalues[i] = g.tourValue()

    start = time.time()
    g.swapHeuristic(i)
    g.TwoOptHeuristic(i)
    end = time.time()
    swap_2_opt_tourvalues[i] = g.tourValue()
    swap_2_opt_time[i] = end - start

    g.perm = [n for n in range(g.n)]
    start = time.time()
    g.Greedy()
    end = time.time()
    greedy_tourvalues[i] = g.tourValue()
    greedy_time[i] = end - start

    g.perm = [n for n in range(g.n)]
    start = time.time()
    g.NearestInsertion()
    end = time.time()
    nearest_insertion_tourvalues[i] = g.tourValue()
    nearest_insertion_time[i] = end - start

    os.remove("Cities" + str(i))


# Plot the tour value vs number of nodes
plt.plot(x_values, swap_2_opt_tourvalues, label = 'Swap + 2-opt')
plt.plot(x_values, greedy_tourvalues, label = 'Greedy')
plt.plot(x_values, nearest_insertion_tourvalues, label = 'Nearest Insertion')
plt.legend()

plt.title('Generated tour value for different number of nodes')
plt.xlabel('Number of nodes')
plt.ylabel('Tour value')

plt.xlim(2, number_of_cities)
plt.show()



# Plot the running time
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.plot(x_values, swap_2_opt_time, label = 'Swap + 2-opt')
ax1.plot(x_values, greedy_time, label = 'Greedy')
ax1.plot(x_values, nearest_insertion_time, label = 'Nearest Insertion')
ax1.legend()
ax1.set_title('Running time for different number of nodes')
#ax1.set_xlabel('Number of nodes')
ax1.set_ylabel('Running time (seconds)')

ax2.plot(x_values, greedy_time, label = 'Greedy')
ax2.plot(x_values, nearest_insertion_time, label = 'Nearest Insertion')
ax2.legend()
#ax2.set_title('Generated tour value for different number of nodes')
ax2.set_xlabel('Number of nodes')
ax2.set_ylabel('Running time (seconds)')

plt.xlim(2, number_of_cities)
plt.show()



minimum_tourvalues = [0 for m in range(number_of_cities)]
minimum_times = [0 for m in range(number_of_cities)]

for i in range(number_of_cities):
    minimum_tourvalues[i] = min((nearest_insertion_tourvalues[i], 2), (greedy_tourvalues[i], 1), (swap_2_opt_tourvalues[i], 0))
    minimum_tourvalues[i] = minimum_tourvalues[i][1]
    minimum_times[i] = min((nearest_insertion_time[i], 2), (greedy_time[i], 1), (swap_2_opt_time[i], 0))
    minimum_times[i] = minimum_times[i][1]


print('Percentage of times Swap + 2-opt gets the shortest tour value: ' + str(minimum_tourvalues.count(0)*100/number_of_cities) + '%')
print('Percentage of times the greedy algorithm gets the shortest tour value: ' + str(minimum_tourvalues.count(1)*100/number_of_cities) + '%')
print('Percentage of times the nearest insertion algorithm gets the shortest tour value: ' + str(minimum_tourvalues.count(2)*100/number_of_cities) + '%')

print('Percentage of times Swap + 2-opt is the quickest: ' + str(minimum_times.count(0)*100/number_of_cities) + '%')
print('Percentage of times the greedy algorithm is the quickest: ' + str(minimum_times.count(1)*100/number_of_cities) + '%')
print('Percentage of times the nearest insertion algorithm is the quickest: ' + str(minimum_times.count(2)*100/number_of_cities) + '%')



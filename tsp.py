import itertools
import matplotlib.pyplot as plt
import numpy as np

def tsp_brute_force(distances, cities):
    """
    Solves the TSP problem using the brute-force method.

    Parameters:
        distances (list of list of float): A square matrix representing the distances between each pair of cities.
        cities (list of tuple of float): A list of tuples representing the (x, y) coordinates of each city.

    Returns:
        A tuple containing the minimum distance and the optimal path.
    """
    n = len(distances)
    cities_indices = range(n)
    shortest_distance = float('inf')
    optimal_path = None

    for path in itertools.permutations(cities_indices):
        distance = 0
        for i in range(n - 1):
            distance += distances[path[i]][path[i + 1]]
        distance += distances[path[-1]][path[0]]

        if distance < shortest_distance:
            shortest_distance = distance
            optimal_path = path

    return shortest_distance, optimal_path

def tsp_greedy(distances, cities):
    """
    Solves the TSP problem using the greedy method.

    Parameters:
        distances (list of list of float): A square matrix representing the distances between each pair of cities.
        cities (list of tuple of float): A list of tuples representing the (x, y) coordinates of each city.

    Returns:
        A tuple containing the minimum distance and the optimal path.
    """
    n = len(distances)
    cities_indices = range(n)
    visited_cities = [0]
    unvisited_cities = list(cities_indices[1:])

    while unvisited_cities:
        current_city = visited_cities[-1]
        nearest_city = min(unvisited_cities, key=lambda city: distances[current_city][city])
        visited_cities.append(nearest_city)
        unvisited_cities.remove(nearest_city)

    optimal_path = tuple(visited_cities)
    shortest_distance = sum(distances[optimal_path[i]][optimal_path[i + 1]] for i in range(n - 1))
    shortest_distance += distances[optimal_path[-1]][optimal_path[0]]

    return shortest_distance, optimal_path

def visualize_tsp(distances, cities, path):
    """
    Visualizes the TSP problem and the optimal path.

    Parameters:
        distances (list of list of float): A square matrix representing the distances between each pair of cities.
        cities (list of tuple of float): A list of tuples representing the (x, y) coordinates of each city.
        path (tuple of int): The optimal path as a tuple of city indices.
    """
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_title(f'Traveling Salesman Problem (distance = {distances[path[0]][path[-1]]:.2f})')

    for i, city in enumerate(cities):
        ax.annotate(str(i), (city[0] + 0.1, city[1] + 0.1))

    for i in range(len(path) - 1):
        city1 = cities[path[i]]
        city2 = cities[path[i + 1]]
        ax.plot([city1[0], city2[0]], [city1[1], city2[1]], 'k-')

    city1 = cities[path[-1]]
    city2 = cities[path[0]]
    ax.plot([city1[0], city2[0]], [city1[1], city2[1]],'k-')
    plt.show()

cities = [(10, 0), (1, 0), (8, 1), (5, 19), (5, 6)]
distances = [[np.linalg.norm(np.array(cities[i]) - np.array(cities[j])) for j in range(len(cities))] for i in range(len(cities))]

while True:
    print('Choose method:')
    print('1. Brute-force')
    print('2. Greedy')
    choice = input('Enter choice (1 or 2): ')

    if choice == '1':
        distance, path = tsp_brute_force(distances, cities)
        print(f'Minimum distance: {distance:.2f}')
        print(f'Optimal path: {path}')
        visualize_tsp(distances, cities, path)
        break

    elif choice == '2':
        distance, path = tsp_greedy(distances, cities)
        print(f'Minimum distance: {distance:.2f}')
        print(f'Optimal path: {path}')
        visualize_tsp(distances, cities, path)
        break

    else:
        print('Invalid choice. Please try again.')
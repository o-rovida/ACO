import random
import numpy as np
import pandas as pd

def euclidean_distance(a, b):
    distance = 0
    if len(a) != len(b):
        raise Exception("The vectors must have the same size")
    
    for i in range(len(a)):
        distance += (a[i] - b[i])**2

    return distance**(1/2)

class DataObject:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def equals(self, data_object):
        if isinstance(data_object, DataObject):
            if self.id == data_object.id and self.data == data_object.data:
                return True
        else:
            return False
        
    def in_list(self, data_object_list):
        
        for object in data_object_list:
            if self.equals(object):
                return True
            
        return False

class ACOCGraph:
    def __init__(self, data_object_list, number_of_clusters=3, initial_pheromone=0.1):
        self.data_object_list = data_object_list
        self.number_of_clusters = number_of_clusters
        self.initial_pheromone = initial_pheromone
        self.matrix = {}

        for object in self.data_object_list:
            
            self.matrix[object] = {}
            
            for i in range(self.number_of_clusters):
                self.matrix[object][i] = self.initial_pheromone
    
    def update_pheromone_matrix(self, ant_rank, evaporation_constant=0.01):
        # para cada formiga na lista de elite
        for ant in ant_rank['ant']:
            # para cada cluster
            for i in range(self.number_of_clusters):
                # para cada objeto do cluster
                for object in ant.clusters[i].data_object_list:
                    # atualiza a matriz de feromonio
                    self.matrix[object][i] = self.matrix[object][i]*(1-evaporation_constant) + 1/ant.evaluate_solution()

class Cluster:
    def __init__(self, id, data_object_list):
        self.id = id
        self.data_object_list = data_object_list
        self.cluster_center = [self.calculate_cluster_center()]

    def calculate_cluster_center(self):
        center = []
        if not self.data_object_list:
            return center
        
        else:
            for i in range(len(self.data_object_list[0].data)):
                center.append(np.mean([object.data[i] for object in self.data_object_list]))
            return center

    def append_object(self, data_object):
        if not data_object.in_list(self.data_object_list):
            self.data_object_list.append(data_object)
            self.cluster_center = self.calculate_cluster_center()
        else:
            raise Exception("The object is already in the cluster")
        
class Ant():
    def __init__ (self, graph, distance_expoent, pheromone_expoent):
        self.graph = graph

        self.memory_list = []
        self.object_list = self.graph.data_object_list.copy()

        self.clusters = {}

        # inicializa a formiga com um objeto aleatorio em cada cluster, para ser o centro do cluster
        for i in range(self.graph.number_of_clusters):
            
            cluster = Cluster(i, [])
            self.clusters[i] = cluster

            possible_centers = []

            for obj in self.object_list:
                if not obj.in_list(self.memory_list):
                    possible_centers.append(obj)

            obj = random.choices(possible_centers)[0]

            self.memory_list.append(obj)
            self.clusters[i].append_object(obj)

        self.distance_expoent = distance_expoent
        self.pheromone_expoent = pheromone_expoent

    def move(self, strategy='random'): #strategy = 'greedy' or 'random'
        
        possible_destinations = []

        for obj in self.object_list:
            if not obj.in_list(self.memory_list):
                possible_destinations.append(obj)

        if len(possible_destinations) > 0:
            
            next_object = random.choices(possible_destinations)[0]

            probability_list = []

            for i in range(self.graph.number_of_clusters):

                pheromone = self.graph.matrix[next_object][i]
                distance = euclidean_distance(next_object.data, self.clusters[i].calculate_cluster_center())

                probability = pheromone**self.pheromone_expoent * (1/distance)**self.distance_expoent
                probability_list.append(probability)

            probability_list = [p/sum(probability_list) for p in probability_list]
 
            if strategy == 'greedy':
                cluster = probability_list.index(max(probability_list))
                self.clusters[cluster].append_object(next_object)
                
            elif strategy == 'random':
                cluster = random.choices(range(self.graph.number_of_clusters), weights=probability_list)[0]
                self.clusters[cluster].append_object(next_object)

            self.memory_list.append(next_object)

            # se a formiga se moveu retorna True
            return True

        else:

            # se a formiga não se moveu retorna False
            return False
        
    def evaluate_solution(self):
        cost = 0
        for cluster in self.clusters.values():
            cost_cluster = 0
            for obj in cluster.data_object_list:
                cost += euclidean_distance(obj.data, cluster.cluster_center)
            cost += cost_cluster/len(cluster.data_object_list)
        return cost
        
if __name__ == "__main__":

    number_of_epochs = 50
    number_of_clusters = 3
    number_of_ant = 10
    distance_expoent = 1
    pheromone_expoent = 1.5
    better_solution = None
    number_of_elite = 2
    evaporation_constant = 0.01

    
    data = pd.read_csv('dataset/wine.csv', sep=',', header=None)
    data = data.drop([0], axis=1)

    data_list = data.values.tolist()

    data_object_list = []

    for i in range(100): #range(len(data_list)):
        data_object_list.append(DataObject(i, data_list[i]))

    graph = ACOCGraph(data_object_list, number_of_clusters=3, initial_pheromone=0.1)
    
    for i in range(number_of_epochs):
        
        print('Epoch: ', i)

        ant_list = []

        for _ in range(number_of_ant):
            ant_list.append(Ant(graph, distance_expoent=distance_expoent, pheromone_expoent=pheromone_expoent))

        for ant in ant_list:
            keep_moving = True
            while keep_moving:
                keep_moving = ant.move(strategy='greedy')
       
        ant_rank = pd.DataFrame(data=[[ant, ant.evaluate_solution()] for ant in ant_list], columns=['ant', 'cost'])
        ant_rank = ant_rank.sort_values(by='cost', ascending=True, ignore_index=True)
        ant_rank = ant_rank.head(number_of_elite)

        if better_solution is None:
            better_solution = ant_rank['ant'][0]
        elif ant_rank['cost'][0] < better_solution.evaluate_solution():
            better_solution = ant_rank['ant'][0]

        graph.update_pheromone_matrix(ant_rank, evaporation_constant=evaporation_constant)

        print(ant_rank.head(1))
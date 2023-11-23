import random
import numpy as np
import pandas as pd

random.seed(42)

def euclidean_distance(a, b):
    distance = 0
    if len(a) != len(b):
        raise Exception("The vectors must have the same size")
    
    for i in range(len(a)):
        distance += (a[i] - b[i])**2

    return distance**(1/2)

class DataObject:
    def __init__(self, 
                 id: int, 
                 data: np.ndarray,
                 target:int):
        
        self.id = id
        if isinstance(data, np.ndarray):
            self.data = data
        else:
            try:
                self.data = np.array(data)
            except:
                raise Exception("The data must be a list or a numpy array")
        self.target = target

    def equals(self, data_object):

        if isinstance(data_object, DataObject):
            if (self.id == data_object.id) and (self.data.all() == data_object.data.all()):
                return True
            
        else:
            return False
        
    def in_list(self, data_object_list):
    
        for obj in data_object_list:
            if self.equals(obj):
                return True
            
        return False

class ACOCGraph:
    def __init__(self, 
                 data_object_list:list, 
                 number_of_clusters:int=3, 
                 initial_pheromone:float=0.1):
        
        self.data_object_list = data_object_list
        self.number_of_clusters = number_of_clusters
        self.initial_pheromone = initial_pheromone
        self.matrix = {}

        for obj in self.data_object_list:
            
            self.matrix[obj] = {}
            
            for i in range(self.number_of_clusters):
                self.matrix[obj][i] = self.initial_pheromone
    
    def update_pheromone_matrix(self, ant_rank, evaporation_constant=0.01):
        # para cada formiga na lista de elite
        for ant in ant_rank:
            # para cada cluster
            for i in range(self.number_of_clusters):
                # para cada objeto do cluster
                for obj in ant.clusters[i].data_object_list:
                    # atualiza a matriz de feromonio
                    self.matrix[obj][i] = self.matrix[obj][i]*(1-evaporation_constant) + 1/ant.evaluate_solution()

class Cluster:
    def __init__(self, 
                 id: int, 
                 data_object_list: list):
        self.id = id
        self.data_object_list = data_object_list
        self.cluster_center = self.calculate_cluster_center()

    def calculate_cluster_center(self):
        center = []

        if not self.data_object_list:
            return center
        
        else:
            for i in range(len(self.data_object_list[0].data)):
                center.append(np.mean([obj.data[i] for obj in self.data_object_list]))
            return center

    def append_object(self, data_object):
        if not data_object.in_list(self.data_object_list):
            self.data_object_list.append(data_object)
            self.cluster_center = self.calculate_cluster_center()
        else:
            raise Exception("The object is already in the cluster")
        
class Ant():
    def __init__ (self, 
                  graph: ACOCGraph, 
                  distance_expoent: float, 
                  pheromone_expoent: float):
        
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
 
            if strategy == 'greedy': # escolhe o cluster com maior probabilidade
                cluster = probability_list.index(max(probability_list))
                self.clusters[cluster].append_object(next_object)
                
            elif strategy == 'random': # escolhe o cluster aleatoriamente, com probabilidade proporcional a avaliação de cada cluster
                cluster = random.choices(range(self.graph.number_of_clusters), weights=probability_list)[0]
                self.clusters[cluster].append_object(next_object)

            self.memory_list.append(next_object)

            # se a formiga se moveu retorna True
            return True

        else:

            # se a formiga não se moveu retorna False
            return False
        
    def evaluate_solution(self):
        # calcula o custo da solução
        cost = 0
        for cluster in self.clusters.values():
            cost_cluster = 0
            for obj in cluster.data_object_list:
                cost_cluster += euclidean_distance(obj.data, cluster.cluster_center)
            # divide o custo do cluster pelo numero de objetos no cluster
            cost += cost_cluster/len(cluster.data_object_list)
        # custo é a soma da media dos custos de cada cluster
        return cost
        
class ACOC():
    def __init__ (self, 
                  graph: ACOCGraph, 
                  number_of_epochs: int,
                  number_of_clusters: int, 
                  number_of_ant: int, 
                  distance_expoent: float, 
                  pheromone_expoent: float, 
                  number_of_elite: int, 
                  evaporation_constant: float, 
                  strategy:str='greedy'):
        
        self.graph = graph
        self.number_of_epochs = number_of_epochs
        self.number_of_clusters = number_of_clusters
        self.number_of_ant = number_of_ant
        self.distance_expoent = distance_expoent
        self.pheromone_expoent = pheromone_expoent
        self.number_of_elite = number_of_elite
        self.evaporation_constant = evaporation_constant
        self.better_solution = None
        self.strategy = strategy
        self.last_generation = []
        self.epochs_dict = {}

        self.run()

    def run(self):
        
        for i in range(self.number_of_epochs):

            ant_list = []

            for _ in range(self.number_of_ant):

                ant_list.append(Ant(self.graph, self.distance_expoent, self.pheromone_expoent))

            for ant in ant_list:
                keep_moving = True
                while keep_moving:
                    keep_moving = ant.move(strategy=self.strategy)
            
            ant_rank = pd.DataFrame(data=[[ant, ant.evaluate_solution()] for ant in ant_list], columns=['ant', 'cost'])
            ant_rank = ant_rank.sort_values(by='cost', ascending=True, ignore_index=True)

            ant_rank = ant_rank.head(self.number_of_elite)

            if self.better_solution is None:
                self.better_solution = ant_rank['ant'][0]
            
            elif ant_rank['cost'][0] < self.better_solution.evaluate_solution():
                self.better_solution = ant_rank['ant'][0]

            self.graph.update_pheromone_matrix(ant_rank['ant'], evaporation_constant=self.evaporation_constant)

            self.last_generation = ant_rank['ant']
            self.epochs_dict[i] = ant_rank

if __name__ == "__main__":

    dataset = pd.read_csv('dataset/wine.csv', sep=',', header=None)
    target = dataset[0]
    data = dataset.drop([0], axis=1)
    # normalizando os dados, dividindo pelo maior valor de cada coluna
    for col in data.columns:
        scaled_values = [value/max(data[col]) for value in data[col]]
        data[col] = scaled_values
    data_list = data.values.tolist()
    data_object_list = []
    
    for i in range(len(data_list)):
        data_object_list.append(DataObject(id=i, data=data_list[i], target=target[i]))

    graph = ACOCGraph(data_object_list, number_of_clusters=3, initial_pheromone=0.1)

    NUMBER_OF_ANT = int(round(len(data_object_list)*0.05,0))
    NUMBER_OF_ELITE = int(round(NUMBER_OF_ANT*0.2))

    print("numero de formigas: {}".format(NUMBER_OF_ANT))
    print("numero de formigas de elite: {}".format(NUMBER_OF_ELITE))

    acoc = ACOC(graph,
                number_of_epochs=10, 
                number_of_clusters=3, 
                number_of_ant=NUMBER_OF_ANT, 
                distance_expoent=1, 
                pheromone_expoent=1, 
                number_of_elite=NUMBER_OF_ELITE, 
                evaporation_constant=0.01)

    print("melhor avaliação: {}".format(acoc.better_solution.evaluate_solution()))
    print("\n")

    for epoch in acoc.epochs_dict.values():
        print("média da avaliação da geração: {}".format(np.mean([ant.evaluate_solution() for ant in epoch['ant']])))
        print('-----------------')

    print("\n")
    print("melho avaliação: ")
    
    i = 0
    
    for cluster in acoc.better_solution.clusters.values():
        
        i += 1

        print("cluster: {}".format(i))
        
        print("centro do cluster: ")
        print(cluster.cluster_center)
        print("total de objetos no cluster: ")
        print(len(cluster.data_object_list))
        
        class_1 = []
        class_2 = []
        class_3 = []

        class_mapping = {
            1: class_1,
            2: class_2,
            3: class_3
        }

        for obj in cluster.data_object_list:
            class_mapping[obj.target].append(obj)

        print("class 1: {}".format(len(class_1)))
        print("class 2: {}".format(len(class_2)))
        print("class 3: {}".format(len(class_3)))

        print('-----------------')
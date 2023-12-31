import random
import numpy as np
import matplotlib.pyplot as plt

# Define a seed for the random number generator, para reproduzir os resultados
random.seed(42)
# classe que representa uma aresta do grafo, ou seja, o caminho entre dois pontos.
class Arris():
    def __init__(self, 
    origin:str, 
    destination:str, 
    distance:float, 
    pheromone:float):
        
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.pheromone = pheromone

    # calcula a avaliação da aresta.
    # quanto maior a avaliação, maior a probabilidade de ser escolhida.

    def evaluate_arris(self, distance_expoent, pheromone_expoent):
        # é usado o inverso da distancia, ou seja, é inversamente proporcional a distancia
        distance_inverse = (1/self.distance)
        return (distance_inverse**distance_expoent)*(self.pheromone**pheromone_expoent)
    
    def update_pheromone(self, generation, update_constant, evaporation_constant):
        # Variável para armazenar a adição total de feromônio para esta aresta
        pheromone_addition = 0

        # Itera sobre todas as formigas na geração
        for ant in generation:
            # Calcula o feromônio a ser depositado por esta formiga nesta aresta
            pheromone = update_constant / ant.calculate_distance()

            # Itera sobre os vértices visitados pela formiga
            for i in range(len(ant.visited_vertex)):
                # Obtém o vértice atual e o próximo vértice no caminho da formiga,
                # Garantindo que o próximo vértice seja o primeiro se o atual for o último
                vertex = ant.visited_vertex[i]

                # Obtém o próximo vértice no caminho da formiga, o mod é usado para garantir que o índice não seja maior que o tamanho da lista
                next_vertex_index = (i + 1) % len(ant.visited_vertex)
                next_vertex = ant.visited_vertex[next_vertex_index]

                # Verifica se formiga passou por esta aresta, idependente da direção
                if (vertex == self.origin and next_vertex == self.destination) or (vertex == self.destination and next_vertex == self.origin):
                    # Adiciona o feromônio depositado por esta formiga nesta aresta
                    pheromone_addition += pheromone

        # Atualiza o feromônio da aresta considerando a evaporação e a adição de feromônio
        self.pheromone = (1 - evaporation_constant) * self.pheromone + pheromone_addition

class Roulette():
    def __init__(self, 
                 items:list, 
                 distance_expoent:float, 
                 pheromone_expoent:float):
        
        self.items = items
        self.distance_expoent = distance_expoent
        self.pheromone_expoent = pheromone_expoent
        self.total = sum([item.evaluate_arris(self.distance_expoent, self.pheromone_expoent) for item in items])
        self.probabilities = [item.evaluate_arris(self.distance_expoent, self.pheromone_expoent)/self.total for item in items]
        
    def spin(self):
        #Retorna um item aleatorio, com probabilidade proporcional a sua avaliação
        return random.choices(self.items, weights=self.probabilities)[0]

class Tourney():
    def __init__(self, 
                 items:list, 
                 distance_expoent:float, 
                 pheromone_expoent:float):
        
        self.items = items
        self.distance_expoent = distance_expoent
        self.pheromone_expoent = pheromone_expoent

    def compete(self):
        competitor_1 = random.choice(self.items)
        competitor_2 = random.choice(self.items)
        
        #Compara os competidores e retorna o vencedor
        if competitor_1.evaluate_arris(self.distance_expoent, self.pheromone_expoent) > competitor_2.evaluate_arris(self.distance_expoent, self.pheromone_expoent):
            return competitor_1
        elif competitor_1.evaluate_arris(self.distance_expoent, self.pheromone_expoent) < competitor_2.evaluate_arris(self.distance_expoent, self.pheromone_expoent):
            return competitor_2
        # se os competidores tiverem a mesma avaliação, retorna um deles aleatoriamente
        elif competitor_1.evaluate_arris(self.distance_expoent, self.pheromone_expoent) == competitor_2.evaluate_arris(self.distance_expoent, self.pheromone_expoent):
            return random.choice([competitor_1, competitor_2])
        else:
            raise Exception("Error: Invalid evaluation")

class CompleteGraph():
    def __init__(self, 
                 vertex_list:list, 
                 distance_dict:dict, 
                 initial_pheromone:float=0.1):
        self.vertex_list = vertex_list
        self.distance_dict = distance_dict
        self.initial_pheromone = initial_pheromone

        arris_list = []

        #considerando um grafo completo, ou seja, todos os vertices são interligados
        #cria-se uma lista de instancias da classe Arris, que representa as arestas do grafo
        #o feromonio inicial de cada aresta é o mesmo, por padrão 0.1

        for origin in vertex_list:
            for destination in vertex_list:
                if origin != destination:
                    arris_list.append(Arris(origin=origin, destination=destination, distance=distance_dict[origin][destination], pheromone=self.initial_pheromone))

        self.arris_list = arris_list

    def update_pheromone(self, 
                         generation:list, 
                         update_constant:float, 
                         evaporation_constant:float):
        
        for arris in self.arris_list:
            arris.update_pheromone(generation, update_constant, evaporation_constant)

class Ant():
    def __init__ (self, 
                  current_vertex:str, 
                  graph:CompleteGraph, 
                  method_of_selection:str, 
                  distance_expoent:float, 
                  pheromone_expoent:float):
        
        self.current_vertex = current_vertex
        self.visited_vertex = []
        self.visited_vertex.append(current_vertex)
        self.graph = graph
        self.method_of_selection = method_of_selection
        self.distance_expoent = distance_expoent
        self.pheromone_expoent = pheromone_expoent

    def move(self):
        current_vertex = self.current_vertex
        possible_destinations = []
        for arris in self.graph.arris_list:
            if arris.origin == current_vertex and arris.destination not in self.visited_vertex:
                possible_destinations.append(arris)

        if len(possible_destinations) > 0:
            
            if self.method_of_selection == 'roulette':
                next_vertex = Roulette(possible_destinations, self.distance_expoent, self.pheromone_expoent).spin().destination
            elif self.method_of_selection == 'tourney':
                next_vertex = Tourney(possible_destinations, self.distance_expoent, self.pheromone_expoent).compete().destination
            self.visited_vertex.append(next_vertex)
            self.current_vertex = next_vertex

            # se a formiga se moveu retorna True
            return True

        else:

            # se a formiga não se moveu retorna False
            return False
        
    def calculate_distance(self):

        path = []      
        # cria uma lista com o caminho percorrido pela formiga
        path = self.visited_vertex.copy()

            # adiciona o primeiro vertice no final da lista, para que o caminho seja fechado
            # o caxeiro viajante deve voltar para o ponto de partida
        path.append(self.visited_vertex[0])

        distance = 0
        # calcula a distancia total percorrida pela formiga
        for i in range(len(path)-1):
            #print(path[i], path[i+1])
            distance += self.graph.distance_dict[path[i]][path[i+1]]
        
        return distance
    
class ACO():
    def __init__(self, 
                 vertex_list:list, 
                 distance_dict:dict, 
                 initial_pheromone:float=0.1, 
                 evaporation_constant:float=0.01, 
                 update_constant:float=2, 
                 number_of_epochs:int=1000, 
                 method_of_selection:str='roulette', 
                 distance_expoent:float=1.0, 
                 pheromone_expoent:float=1.0):
        
        self.initial_pheromone = initial_pheromone
        self.graph = CompleteGraph(vertex_list, distance_dict, self.initial_pheromone)
        self.evaporation_constant = evaporation_constant
        self.update_constant = update_constant
        self.number_of_epochs = number_of_epochs
        self.method_of_selection = method_of_selection
        self.distance_expoent = distance_expoent
        self.pheromone_expoent = pheromone_expoent
        self.last_generation = []
        self.epochs_dict = {}

        self.run()

    def run(self):
        for i in range(self.number_of_epochs):
        
            self.last_generation = []

            for vertex in self.graph.vertex_list:
                self.last_generation.append(Ant(vertex, self.graph, self.method_of_selection, self.distance_expoent, self.pheromone_expoent))

            for ant in self.last_generation:
                
                keep_moving = True
            
                while keep_moving:
                    keep_moving = ant.move()

            self.graph.update_pheromone(self.last_generation, self.update_constant, self.evaporation_constant)

            self.epochs_dict[i+1] = {"individuals":self.last_generation,
                "evaluation":np.mean([ant.calculate_distance() for ant in self.last_generation])}

if __name__ == "__main__":
    #lista dos vertices do grafo, ou seja os pontos que serao visitados
    #não foi criada uma classe para representar os vertices, pois não há necessidade de armazenar mais informações sobre eles.
    vertex_list = ['A','B','C','D','E']

    #lista das distancias entre os vertices do grafo
    distance_dict = {
        'A': {'B':6,'C':7,'D':6,'E':8},
        'B': {'A':6,'C':3,'D':8,'E':9},
        'C': {'A':7,'B':3,'D':6,'E':5},
        'D': {'A':6,'B':8,'C':6,'E':3},
        'E': {'A':8,'B':9,'C':5,'D':3}
    }

    #instancia o algoritmo ACO
    aco = ACO(vertex_list, 
              distance_dict, 
              initial_pheromone=0.1, 
              evaporation_constant=0.01, 
              update_constant=2, 
              number_of_epochs=50,
              method_of_selection='roulette',
              distance_expoent=1,
              pheromone_expoent=2)

    for epoch in aco.epochs_dict:
        print(f'Epoch {epoch}: {aco.epochs_dict[epoch]["evaluation"]}')

    #imprime o caminho percorrido por cada formiga na ultima geração
    for ant in aco.last_generation:
        print(ant.visited_vertex)
        print(ant.calculate_distance())

    #imprime o feromonio de cada aresta do grafo ao final da execução do algoritmo
    for arris in aco.graph.arris_list:
        print(f'{arris.origin} -> {arris.destination} : {arris.pheromone}')
    
    #plota um grafico com a evolução da avaliação média da população a cada geração
    plt.plot(list(aco.epochs_dict.keys()), [aco.epochs_dict[epoch]["evaluation"] for epoch in aco.epochs_dict.keys()], color='green')
    plt.xlabel('Epoch')
    plt.ylabel('Evaluation')
    plt.show()
import random
import numpy as np

# classe que representa uma aresta do grafo, ou seja, o caminho entre dois pontos
class Arris():
    def __init__(self, origin, destination, distance, pheromone):
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.pheromone = pheromone

    # calcula a avaliação da aresta, que é o produto da distancia sobre 1 e feromonio
    # quanto maior a avaliação, maior a probabilidade de ser escolhida
    def evaluate_arris(self):
        n = (1/self.distance)
        return n*self.pheromone
    
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
                # garantindo que o próximo vértice seja o primeiro se o atual for o último
                vertex = ant.visited_vertex[i]

                # obtém o próximo vértice no caminho da formiga, o mod é usado para garantir que o índice não seja maior que o tamanho da lista
                next_vertex_index = (i + 1) % len(ant.visited_vertex)
                next_vertex = ant.visited_vertex[next_vertex_index]

                # verifica se formiga passou por esta aresta, idependente da direção
                if (vertex == self.origin and next_vertex == self.destination) or (vertex == self.destination and next_vertex == self.origin):
                    # Adiciona o feromônio depositado por esta formiga nesta aresta
                    pheromone_addition += pheromone

        # Atualiza o feromônio da aresta considerando a evaporação e a adição de feromônio
        self.pheromone = (1 - evaporation_constant) * self.pheromone + pheromone_addition

    
#metodo de roleta
class Roulette():
    def __init__(self, itens):
        self.itens = itens
        self.total = sum([item.evaluate_arris() for item in itens])
        self.probablities = [item.evaluate_arris()/self.total for item in itens]

    def spin(self):
        #retorna um item aleatorio, com probabilidade proporcional a sua avaliação
        return random.choices(self.itens, weights=self.probablities)[0]

#metodo de torneio
class Tourney():
    def __init__(self, itens):
        self.itens = itens

    def compete(self):
        #seleciona dois competidores aleatoriamente
        competitor_1 = random.choices(self.itens)[0]
        competitor_2 = random.choices(self.itens)[0]

        #compara os competidores e retorna o vencedor
        if competitor_1.evaluate_arris() > competitor_2.evaluate_arris():
            return competitor_1
        elif competitor_1.evaluate_arris() < competitor_2.evaluate_arris():
            return competitor_2
        #se os competidores tiverem a mesma avaliação, retorna um deles aleatoriamente
        else:
            return random.choices([competitor_1, competitor_2])[0]

class CompleteGraph():
    def __init__(self, vertex_list, distance_dict, initial_pheromone=0.1):
        self.vertex_list = vertex_list
        self.distance_dict = distance_dict
        self.initial_pheromone = initial_pheromone

        arris_list = []

        #considerando um grafo completo, ou seja, todos os vertices são interligados
        #cria-se uma lista de instancias da classe Arris, que representa as arestas do grafo
        #o feromonio inicial de cada aresta é o mesmo, nesse caso 0.1
        for origin in vertex_list:
            for destination in vertex_list:
                if origin != destination:
                    arris_list.append(Arris(origin=origin, destination=destination, distance=distance_dict[origin][destination], pheromone=self.initial_pheromone))

        self.arris_list = arris_list

    def update_pheromone(self, generation, update_constant, evaporation_constant):
        
        for arris in self.arris_list:
            arris.update_pheromone(generation, update_constant, evaporation_constant)

class Ant():
    def __init__ (self, current_vertex, graph, method_of_selection):
        self.current_vertex = current_vertex
        self.visited_vertex = []
        self.visited_vertex.append(current_vertex)
        self.graph = graph
        self.method_of_selection = method_of_selection

    def move(self):
        current_vertex = self.current_vertex
        possible_destinations = []
        for arris in self.graph.arris_list:
            if arris.origin == current_vertex and arris.destination not in self.visited_vertex:
                possible_destinations.append(arris)

        if len(possible_destinations) > 0:
            
            if self.method_of_selection == 'roulette':
                next_vertex = Roulette(possible_destinations).spin().destination
            elif self.method_of_selection == 'tourney':
                next_vertex = Tourney(possible_destinations).compete().destination
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
    def __init__(self, vertex_list, distance_dict, initial_pheromone=0.1, evaporation_constant=0.01, update_constant=2, number_of_epochs=1000, method_of_selection='roulette'):
        self.initial_pheromone = initial_pheromone
        self.graph = CompleteGraph(vertex_list, distance_dict, self.initial_pheromone)
        self.evaporation_constant = evaporation_constant
        self.update_constant = update_constant
        self.number_of_epochs = number_of_epochs
        self.method_of_selection = method_of_selection
        self.last_generation = []
        self.epochs_dict = {}

    def run(self):
        for i in range(self.number_of_epochs):
        
            self.last_generation = []

            for vertex in self.graph.vertex_list:
                self.last_generation.append(Ant(vertex, self.graph, self.method_of_selection))

            for ant in self.last_generation:
                
                keep_moving = True
            
                while keep_moving:
                    keep_moving = ant.move()

            self.graph.update_pheromone(self.last_generation, self.update_constant, self.evaporation_constant)

            self.epochs_dict[i+1] = {"individuals":self.last_generation,
                "evaluation":np.mean([ant.calculate_distance() for ant in self.last_generation])}

if __name__ == "__main__":
    #lista dos vertices do grafo, ou seja os pontos que serao visitados
    #não foi criada uma classe para representar os vertices, pois não há necessidade de armazenar mais informações sobre eles, além do id ou nome
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
              number_of_epochs=1000,
              method_of_selection='roulette')

    #executa o algoritmo
    aco.run()

    for epoch in aco.epochs_dict:
        print(f'Epoch {epoch}: {aco.epochs_dict[epoch]["evaluation"]}')

    #for ant in aco.last_generation:
        #print(ant.visited_vertex)
        #print(ant.calculate_distance())

    #for arris in aco.graph.arris_list:
        #print(f'{arris.origin} -> {arris.destination} : {arris.pheromone}')
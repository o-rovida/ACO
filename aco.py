import random

# classe que representa uma aresta do grafo, ou seja, o caminho entre dois pontos
class Arris():
    def __init__(self, origin, destination, distance, pheromone):
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.pheromone = pheromone

    # calcula a avaliação da aresta, que é o produto da distancia sobre 1 e feromonio
    # quanto maior a avaliação, maior a probabilidade de ser escolhida
    def evaliate_arris(self):
        n = (1/self.distance)
        return n*self.pheromone

#metodo de roleta
class Roulette():
    def __init__(self, itens):
        self.itens = itens
        self.total = sum([item.evaliate_arris() for item in itens])
        self.probablities = [item.evaliate_arris()/self.total for item in itens]

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
        if competitor_1.evaliate_arris() > competitor_2.evaliate_arris():
            return competitor_1
        elif competitor_1.evaliate_arris() < competitor_2.evaliate_arris():
            return competitor_2
        #se os competidores tiverem a mesma avaliação, retorna um deles aleatoriamente
        else:
            return random.choices([competitor_1, competitor_2])[0]

class CompleteGraph():
    def __init__(self, vertex_list, distance_dict):
        self.vertex_list = vertex_list
        self.distance_dict = distance_dict

        arris_list = []

        #considerando um grafo completo, ou seja, todos os vertices são interligados
        #cria-se uma lista de instancias da classe Arris, que representa as arestas do grafo
        #o feromonio inicial de cada aresta é o mesmo, nesse caso 0.1
        for origin in vertex_list:
            for destination in vertex_list:
                if origin != destination:
                    arris_list.append(Arris(origin=origin, destination=destination, distance=distance_dict[origin][destination], pheromone=initial_pheromone))

        self.arris_list = arris_list


class Ant():
    def __init__ (self, current_vertex, graph):
        self.current_vertex = current_vertex
        self.visited_vertex = []
        self.visited_vertex.append(current_vertex)
        self.graph = graph

    def move(self):
        current_vertex = self.current_vertex
        possible_destinations = []
        for arris in self.graph.arris_list:
            if arris.origin == current_vertex and arris.destination not in self.visited_vertex:
                possible_destinations.append(arris)

        if len(possible_destinations) > 0:
            
            next_vertex = Roulette(possible_destinations).spin().destination
            self.visited_vertex.append(next_vertex)
            self.current_vertex = next_vertex

            # se a formiga se moveu retorna True
            return True

        else:

            # se a formiga não se moveu retorna False
            return False
        
    def calculate_distance(self):
        # cria uma lista com o caminho percorrido pela formiga
        path = self.visited_vertex
        # adiciona o primeiro vertice no final da lista, para que o caminho seja fechado
        # o caxeiro viajante deve voltar para o ponto de partida
        path.append(self.visited_vertex[0])

        distance = 0
        # calcula a distancia total percorrida pela formiga
        for i in range(len(path)-1):
            distance += self.graph.distance_dict[self.visited_vertex[i]][self.visited_vertex[i+1]]
        return distance

if __name__ == "__main__":
    #feromonio inicial de todas as arestas
    initial_pheromone = 0.1

    #lista dos vertices do grafo, ou seja os pontos que serao visitados
    #não foi criada uma classe para representar os vertices, pois não há necessidade de armazenar mais informações sobre eles, além do id ou nome
    vertex_list = ['A','B','C','D','E']

    #lista das distancias entre os vertices do grafo
    distance_dict = {
        'A': {'B':6,'C':7,'D':9,'E':8},
        'B': {'A':6,'C':3,'D':8,'E':9},
        'C': {'A':7,'B':3,'D':6,'E':5},
        'D': {'A':9,'B':8,'C':6,'E':3},
        'E': {'A':8,'B':9,'C':5,'D':3}
    }

    grafo = CompleteGraph(vertex_list, distance_dict)

    generation_1 = []

    for vertex in vertex_list:
        generation_1.append(Ant(vertex, grafo))

    for ant in generation_1:
        keep_moving = True
        
        while keep_moving:
            keep_moving = ant.move()

        print(ant.visited_vertex)
        print(ant.calculate_distance(distance_dict))
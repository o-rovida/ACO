# ACO (Otimização por Colônia de Formigas) para o Problema do Caixeiro Viajante
Este script em Python implementa o algoritmo de Otimização por Colônia de Formigas para resolver o Problema do Caixeiro Viajante (PCV). O PCV envolve encontrar a rota mais curta que visita um conjunto dado de cidades e retorna à cidade de origem. O algoritmo ACO simula o comportamento de forrageamento das formigas para encontrar uma solução ótima ou quase ótima para o PCV.

## Implementação
O script inclui as seguintes classes:

### Classe Arris
Representa uma aresta no grafo, armazenando informações sobre origem, destino, distância e nível de feromônio. Também inclui métodos para avaliar a aresta e atualizar o nível de feromônio.

### Classe Roulette
Implementa o método de seleção de roleta, permitindo que o algoritmo escolha arestas probabilisticamente com base em seus valores de avaliação.

### Classe Tourney
Implementa um método de seleção de torneio, onde duas arestas competem, e a escolhida é aquela com um valor de avaliação mais alto. Se as avaliações forem iguais, é feita uma escolha aleatória.

### Classe CompleteGraph
Representa um grafo completo no qual todos os vértices estão interconectados. Inicializa uma lista de arestas (**'Arris'** instâncias) com níveis iniciais de feromônio.

### Classe Ant
Representa uma formiga no algoritmo ACO. Move-se entre vértices com base no método selecionado (roleta ou torneio) e calcula a distância total percorrida.

### Classe ACO
Implementa o algoritmo de Otimização por Colônia de Formigas. Inicializa um grafo completo e formigas, executa o algoritmo por um número especificado de épocas e atualiza os níveis de feromônio.

## Uso

<pre>
<code>
    # Define os vértices do grafo e as distâncias
    vertex_list = ['A', 'B', 'C', 'D', 'E']
    distance_dict = {
        'A': {'B': 6, 'C': 7, 'D': 6, 'E': 8},
        'B': {'A': 6, 'C': 3, 'D': 8, 'E': 9},
        'C': {'A': 7, 'B': 3, 'D': 6, 'E': 5},
        'D': {'A': 6, 'B': 8, 'C': 6, 'E': 3},
        'E': {'A': 8, 'B': 9, 'C': 5, 'D': 3}
    }

    # Instancia o algoritmo ACO
    aco = ACO(
        vertex_list,
        distance_dict,
        initial_pheromone=0.1,
        evaporation_constant=0.01,
        update_constant=2,
        number_of_epochs=1000,
        method_of_selection='roulette'
    )

    # Executa o algoritmo
    aco.run()

    # Imprime a avaliação para cada época
    for epoch in aco.epochs_dict:
        print(f'Época {epoch}: {aco.epochs_dict[epoch]["evaluation"]}')

    # Imprime os caminhos e distâncias das formigas na última geração
    for ant in aco.last_generation:
        print(ant.visited_vertex)
        print(ant.calculate_distance())

    # Imprime os níveis de feromônio de cada aresta no grafo
    for arris in aco.graph.arris_list:
        print(f'{arris.origin} -> {arris.destination} : {arris.pheromone}')

    # Plota um gráfico mostrando a evolução da avaliação média ao longo das épocas
    import matplotlib.pyplot as plt

    plt.plot(
        list(aco.epochs_dict.keys()),
        [aco.epochs_dict[epoch]["evaluation"] for epoch in aco.epochs_dict.keys()],
        color='green'
    )
    plt.xlabel('Época')
    plt.ylabel('Avaliação')
    plt.show()
</code>
</pre>

Este script demonstra o algoritmo ACO aplicado ao PCV usando um grafo de exemplo. Modifique as variáveis **'vertex_list'** e **'distance_dict'** para testar o algoritmo com diferentes grafos.
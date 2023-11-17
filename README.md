Ant Colony Optimization (ACO) Algorithm
Este é um algoritmo de Otimização por Colônia de Formigas (ACO) implementado em Python. O ACO é um método de otimização inspirado no comportamento das formigas ao procurarem caminhos mais curtos entre a colônia e fontes de alimentos. Este código utiliza o ACO para resolver o problema do Caixeiro Viajante em um grafo completo.

Componentes Principais

Classe Arris
Representa uma aresta do grafo, definindo a origem, destino, distância e feromônio. A avaliação da aresta é calculada como o produto da distância pela inversa dela e do feromônio.

Classe Roulette
Implementa o método de roleta, onde itens são selecionados aleatoriamente com probabilidades proporcionais às suas avaliações.

Classe Tourney
Implementa o método de torneio, onde dois competidores são escolhidos aleatoriamente e o vencedor é determinado com base em suas avaliações.

Classe CompleteGraph
Representa um grafo completo, onde todos os vértices estão interligados. Inicializa as arestas do grafo e possui um método para atualizar o feromônio nas arestas.

Classe Ant
Modela uma formiga que percorre o grafo. Move-se de um vértice para outro com base nas avaliações das arestas, utilizando o método de roleta. Calcula a distância total percorrida.

Classe ACO
Implementa o algoritmo ACO para resolver o problema do Caixeiro Viajante. Executa várias gerações de formigas, atualiza o feromônio nas arestas e registra os resultados.

Utilização
Para utilizar o código, crie uma instância da classe ACO, fornecendo a lista de vértices e um dicionário de distâncias entre eles. Em seguida, execute o método run() para iniciar o algoritmo.
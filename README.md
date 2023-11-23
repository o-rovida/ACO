# Ant Colony Optimization (ACO)
Este é um exemplo de implementação do Algoritmo de Otimização por Colônia de Formigas (ACO) em Python. O ACO é uma técnica inspirada no comportamento de formigas reais para encontrar soluções aproximadas para problemas de otimização combinatória, como o Problema do Caixeiro Viajante.

## Estrutura do Código
### Classes Principais
**Arris:**
Representa uma aresta do grafo, definindo o caminho entre dois pontos. Calcula a avaliação da aresta, que é usada para determinar a probabilidade de escolha dessa aresta.

**Roulette:**
Implementa a seleção de itens com base em uma roleta, onde a probabilidade de seleção é proporcional à avaliação dos itens.

**Tourney:**
Realiza uma competição entre dois competidores escolhidos aleatoriamente, garantindo que eles tenham avaliações diferentes.

**CompleteGraph:**
Representa um grafo completo, onde todos os vértices estão interligados. Mantém uma lista de instâncias da classe Arris que representa as arestas do grafo.

**Ant:**
Modela o comportamento de uma formiga, incluindo movimento e cálculo da distância percorrida.

**ACO:**
A classe principal que orquestra a execução do algoritmo ACO. Inclui métodos para inicialização, execução do algoritmo e atualização de feromônio.

### Execução
O código demonstra a execução do ACO em um exemplo específico, resolvendo o Problema do Caixeiro Viajante para um conjunto de vértices e distâncias definidas.

# Ant Colony Optimization for Clustering (ACOC)
/*
=============================================================================
EXERCÍCIO ÁRVORE RUBRO-NEGRA
=============================================================================

1. INSERÇÃO PASSO A PASSO
Elementos a inserir: 30, 15, 60, 7, 22, 45, 75, 17

Passo 1: Inserir 30
- 30 é inserido como raiz com cor Vermelha.
- Regra: A raiz deve ser Negra.
- Ação: Recolorir 30 para Negro. Nenhuma rotação.
- Árvore resultante:
      30(N)

Passo 2: Inserir 15
- 15 é menor que 30, inserido à esquerda como Vermelho.
- Sem violações (pai é Negro).
- Árvore resultante:
      30(N)
     /
   15(V)

Passo 3: Inserir 60
- 60 é maior que 30, inserido à direita como Vermelho.
- Sem violações (pai é Negro).
- Árvore resultante:
      30(N)
     /     \
  15(V)   60(V)

Passo 4: Inserir 7
- 7 < 30 e 7 < 15, inserido à esquerda de 15 como Vermelho.
- Violação: 7(V) e 15(V) são dois nós vermelhos seguidos.
- Análise: O Pai (15) é Vermelho e o Tio (60) também é Vermelho.
- Ação: Recolorir pai (15) e tio (60) para Negro. Recolorir avô (30) para Vermelho. 
  Como 30 é a raiz da árvore, ele volta a ser Negro. Nenhuma rotação.
- Árvore resultante:
      30(N)
     /     \
  15(N)   60(N)
  /
 7(V)

Passo 5: Inserir 22
- 22 < 30, 22 > 15, inserido à direita de 15 como Vermelho.
- Sem violações (pai 15 é Negro).
- Árvore resultante:
      30(N)
     /     \
  15(N)   60(N)
  /   \
 7(V) 22(V)

Passo 6: Inserir 45
- 45 > 30, 45 < 60, inserido à esquerda de 60 como Vermelho.
- Sem violações (pai 60 é Negro).
- Árvore resultante:
        30(N)
      /       \
   15(N)      60(N)
   /   \      /
 7(V) 22(V) 45(V)

Passo 7: Inserir 75
- 75 > 30, 75 > 60, inserido à direita de 60 como Vermelho.
- Sem violações (pai 60 é Negro).
- Árvore resultante:
        30(N)
      /       \
   15(N)      60(N)
   /   \      /   \
 7(V) 22(V) 45(V) 75(V)

Passo 8: Inserir 17
- 17 < 30, 17 > 15, 17 < 22, inserido à esquerda de 22 como Vermelho.
- Violação: 17(V) e 22(V) são nós vermelhos consecutivos.
- Análise: O Pai (22) é Vermelho e o Tio (7) também é Vermelho (filhos de 15).
- Ação: Recolorir pai (22) e tio (7) para Negro. Recolorir avô (15) para Vermelho. 
  Em seguida, verificamos o pai de 15, que é 30 (Negro), logo não há novas violações. Nenhuma rotação.
- Árvore resultante final das inserções:
          30(N)
       /         \
    15(V)        60(N)
    /   \        /   \
  7(N)  22(N)  45(V) 75(V)
        /
      17(V)


2. REMOÇÃO PASSO A PASSO
Elementos a remover: 15, 60
(Utilizaremos a estratégia padrão de substituir pelo sucessor in-order)

Passo 1: Remover 15
- O nó 15 tem dois filhos. Seu sucessor in-order é o 17 (menor valor da subárvore direita).
- Ação: Copiamos o valor 17 para o nó onde está o 15 e removemos fisicamente o nó original do 17.
- O nó 17 original é uma folha e sua cor é Vermelha.
- Operações de balanceamento: Nenhuma. Remover um nó Vermelho folha não altera a quantidade de 
  nós negros nos caminhos, preservando todas as propriedades da Árvore Rubro-Negra.
- Árvore resultante após remoção de 15:
          30(N)
       /         \
    17(V)        60(N)
    /   \        /   \
  7(N)  22(N)  45(V) 75(V)

Passo 2: Remover 60
- O nó 60 tem dois filhos. Seu sucessor in-order é o 75 (menor valor da subárvore direita).
- Ação: Copiamos o valor 75 para a posição do nó 60. O nó que agora armazena 75 mantém a cor Negra original do nó 60.
- Agora precisamos remover fisicamente o nó original do 75. 
- O nó 75 original é uma folha de cor Vermelha.
- Operações de balanceamento: Nenhuma. Assim como no passo anterior, remover uma folha Vermelha 
  não gera duplo negro nem altera a altura negra.
- Árvore resultante após remoção de 60:
          30(N)
       /         \
    17(V)        75(N)
    /   \        /   
  7(N)  22(N)  45(V) 


3. VERIFICAÇÃO DA CONTAGEM DE NÓS NEGROS
=============================================================================
*/

#include <stdio.h>
#include <stdlib.h>

typedef enum { RED, BLACK } Color;

typedef struct Node {
    int data;
    Color color;
    struct Node *left, *right;
} Node;

// Função auxiliar para criar um novo nó
Node* criar_no(int data, Color color) {
    Node* novo = (Node*)malloc(sizeof(Node));
    novo->data = data;
    novo->color = color;
    novo->left = NULL;
    novo->right = NULL;
    return novo;
}

/*
 * Função para contabilizar os nós negros de cada percurso raiz até folha (NULL).
 * Retorna a quantidade de nós negros se todos os caminhos tiverem a mesma quantidade.
 * Retorna -1 se houver divergência entre as subárvores.
 */
int verificar_nos_negros(Node* raiz) {
    // Caso base: chegamos a uma folha nula (NIL). 
    // Em uma Árvore Rubro-Negra, folhas nulas (NIL) são sempre consideradas Negras.
    if (raiz == NULL) {
        return 1;
    }
    
    // Verifica recursivamente as subárvores esquerda e direita
    int contagem_esq = verificar_nos_negros(raiz->left);
    int contagem_dir = verificar_nos_negros(raiz->right);
    
    // Se alguma das subárvores encontrou uma inconsistência, propaga o erro (-1)
    if (contagem_esq == -1 || contagem_dir == -1) {
        return -1;
    }
    
    // Se a quantidade de nós negros for diferente nos caminhos da esquerda e direita, a árvore está inválida
    if (contagem_esq != contagem_dir) {
        return -1; 
    }
    
    // Conta +1 se o nó atual for Negro
    int soma_atual = (raiz->color == BLACK) ? 1 : 0;
    
    return contagem_esq + soma_atual;
}

// Função para exibir o resultado da verificação na tela
void validar_arvore_rubro_negra(Node* raiz) {
    int altura_negra = verificar_nos_negros(raiz);
    if (altura_negra != -1) {
        printf("A arvore eh valida em relacao a contagem de nos negros. Altura negra: %d\n", altura_negra);
    } else {
        printf("A arvore eh invalida! Existem caminhos com quantidades diferentes de nos negros.\n");
    }
}

// Função main simulando a árvore do final do exercício para validar nossa função
int main() {
    /*
     * Montando a árvore resultante do final do exercício para testar a função:
     * 
     *           30(N)
     *        /         \
     *     17(V)        75(N)
     *     /   \        /   
     *   7(N)  22(N)  45(V)
     *
     */
     
    // Criação manual dos nós correspondentes ao estado final da árvore após todas operações
    Node* raiz = criar_no(30, BLACK);
    
    raiz->left = criar_no(17, RED);
    raiz->right = criar_no(75, BLACK);
    
    raiz->left->left = criar_no(7, BLACK);
    raiz->left->right = criar_no(22, BLACK);
    
    raiz->right->left = criar_no(45, RED);
    // raiz->right->right implicitamente NULL
    
    printf("Verificando a arvore apos todas as insercoes e remocoes...\n");
    validar_arvore_rubro_negra(raiz);
    
    // Liberação de memória
    free(raiz->left->left);
    free(raiz->left->right);
    free(raiz->left);
    free(raiz->right->left);
    free(raiz->right);
    free(raiz);
    
    return 0;
}

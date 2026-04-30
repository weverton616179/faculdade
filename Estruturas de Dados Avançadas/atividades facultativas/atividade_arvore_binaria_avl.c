#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Estrutura do Produto
typedef struct {
    int id;
    char nome[100];
    float preco;
    int quantidade;
} Produto;

// Estrutura do Nó da Árvore AVL
typedef struct Node {
    Produto produto;
    struct Node *esquerda;
    struct Node *direita;
    int altura;
} Node;

// Função para obter a altura do nó
int getAltura(Node *N) {
    if (N == NULL)
        return 0;
    return N->altura;
}

// Função utilitária para obter o máximo de dois inteiros
int max(int a, int b) {
    return (a > b) ? a : b;
}

// Função auxiliar para criar um novo nó
Node* novoNo(Produto produto) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->produto = produto;
    node->esquerda = NULL;
    node->direita = NULL;
    node->altura = 1; // Novo nó é inicialmente adicionado na folha
    return node;
}

// Rotação à direita
Node *rotacaoDireita(Node *y) {
    Node *x = y->esquerda;
    Node *T2 = x->direita;

    // Realiza a rotação
    x->direita = y;
    y->esquerda = T2;

    // Atualiza as alturas
    y->altura = max(getAltura(y->esquerda), getAltura(y->direita)) + 1;
    x->altura = max(getAltura(x->esquerda), getAltura(x->direita)) + 1;

    // Retorna a nova raiz
    return x;
}

// Rotação à esquerda
Node *rotacaoEsquerda(Node *x) {
    Node *y = x->direita;
    Node *T2 = y->esquerda;

    // Realiza a rotação
    y->esquerda = x;
    x->direita = T2;

    // Atualiza as alturas
    x->altura = max(getAltura(x->esquerda), getAltura(x->direita)) + 1;
    y->altura = max(getAltura(y->esquerda), getAltura(y->direita)) + 1;

    // Retorna a nova raiz
    return y;
}

// Obtém o fator de balanceamento do nó N
int getBalanceamento(Node *N) {
    if (N == NULL)
        return 0;
    return getAltura(N->esquerda) - getAltura(N->direita);
}

// Função para inserir um produto
Node* inserir(Node* node, Produto produto) {
    // 1. Inserção normal de BST
    if (node == NULL)
        return novoNo(produto);

    if (produto.id < node->produto.id)
        node->esquerda = inserir(node->esquerda, produto);
    else if (produto.id > node->produto.id)
        node->direita = inserir(node->direita, produto);
    else {
        // IDs iguais, compara pelo nome
        int cmp = strcmp(produto.nome, node->produto.nome);
        if (cmp < 0)
            node->esquerda = inserir(node->esquerda, produto);
        else if (cmp > 0)
            node->direita = inserir(node->direita, produto);
        else // IDs e nomes iguais, não permite duplicatas exatas
            return node;
    }

    // 2. Atualiza a altura deste nó ancestral
    node->altura = 1 + max(getAltura(node->esquerda), getAltura(node->direita));

    // 3. Obtém o fator de balanceamento deste nó ancestral
    int balanceamento = getBalanceamento(node);

    // Se o nó se desbalanceou, então existem 4 casos

    // Caso Esquerda-Esquerda
    if (balanceamento > 1 && (produto.id < node->esquerda->produto.id || 
       (produto.id == node->esquerda->produto.id && strcmp(produto.nome, node->esquerda->produto.nome) < 0)))
        return rotacaoDireita(node);

    // Caso Direita-Direita
    if (balanceamento < -1 && (produto.id > node->direita->produto.id || 
       (produto.id == node->direita->produto.id && strcmp(produto.nome, node->direita->produto.nome) > 0)))
        return rotacaoEsquerda(node);

    // Caso Esquerda-Direita
    if (balanceamento > 1 && (produto.id > node->esquerda->produto.id || 
       (produto.id == node->esquerda->produto.id && strcmp(produto.nome, node->esquerda->produto.nome) > 0))) {
        node->esquerda = rotacaoEsquerda(node->esquerda);
        return rotacaoDireita(node);
    }

    // Caso Direita-Esquerda
    if (balanceamento < -1 && (produto.id < node->direita->produto.id || 
       (produto.id == node->direita->produto.id && strcmp(produto.nome, node->direita->produto.nome) < 0))) {
        node->direita = rotacaoDireita(node->direita);
        return rotacaoEsquerda(node);
    }

    // Retorna o nó inalterado
    return node;
}

// Função para buscar um produto pelo ID
Node* buscar(Node* root, int id) {
    if (root == NULL)
        return NULL;
    
    if (id < root->produto.id)
        return buscar(root->esquerda, id);
    else if (id > root->produto.id)
        return buscar(root->direita, id);
    
    return root; // Encontrou
}

// Nó com o menor valor (usado na remoção)
Node* noMenorValor(Node* node) {
    Node* atual = node;
    while (atual->esquerda != NULL)
        atual = atual->esquerda;
    return atual;
}

// Função para remover um produto
Node* remover(Node* root, int id) {
    // PASSO 1: REMOÇÃO PADRÃO BST
    if (root == NULL)
        return root;

    if (id < root->produto.id)
        root->esquerda = remover(root->esquerda, id);
    else if (id > root->produto.id)
        root->direita = remover(root->direita, id);
    else {
        // Encontrou o nó a ser removido

        // Nó com apenas um filho ou nenhum filho
        if ((root->esquerda == NULL) || (root->direita == NULL)) {
            Node *temp = root->esquerda ? root->esquerda : root->direita;

            // Sem filhos
            if (temp == NULL) {
                temp = root;
                root = NULL;
            } else // Um filho
                *root = *temp; // Copia o conteúdo do filho não nulo

            free(temp);
        } else {
            // Nó com dois filhos: obtém o sucessor in-order (menor na subárvore direita)
            Node* temp = noMenorValor(root->direita);

            // Copia os dados do sucessor in-order para este nó
            root->produto = temp->produto;

            // Remove o sucessor in-order
            root->direita = remover(root->direita, temp->produto.id);
        }
    }

    // Se a árvore tinha apenas um nó, retorna
    if (root == NULL)
        return root;

    // PASSO 2: ATUALIZA A ALTURA DO NÓ ATUAL
    root->altura = 1 + max(getAltura(root->esquerda), getAltura(root->direita));

    // PASSO 3: OBTÉM O FATOR DE BALANCEAMENTO
    int balanceamento = getBalanceamento(root);

    // Se o nó ficou desbalanceado, então existem 4 casos

    // Caso Esquerda-Esquerda
    if (balanceamento > 1 && getBalanceamento(root->esquerda) >= 0)
        return rotacaoDireita(root);

    // Caso Esquerda-Direita
    if (balanceamento > 1 && getBalanceamento(root->esquerda) < 0) {
        root->esquerda = rotacaoEsquerda(root->esquerda);
        return rotacaoDireita(root);
    }

    // Caso Direita-Direita
    if (balanceamento < -1 && getBalanceamento(root->direita) <= 0)
        return rotacaoEsquerda(root);

    // Caso Direita-Esquerda
    if (balanceamento < -1 && getBalanceamento(root->direita) > 0) {
        root->direita = rotacaoDireita(root->direita);
        return rotacaoEsquerda(root);
    }

    return root;
}

// Função para exibir a árvore em ordem (in-order)
void exibirEmOrdem(Node *root) {
    if (root != NULL) {
        exibirEmOrdem(root->esquerda);
        printf("ID: %d | Nome: %s | Preco: %.2f | Quantidade: %d\n",
               root->produto.id, root->produto.nome, root->produto.preco, root->produto.quantidade);
        exibirEmOrdem(root->direita);
    }
}

// Função para liberar a memória da árvore
void liberarArvore(Node* root) {
    if (root != NULL) {
        liberarArvore(root->esquerda);
        liberarArvore(root->direita);
        free(root);
    }
}

int main() {
    Node *raiz = NULL;
    Produto p;
    int opcao, idBusca;
    Node *resultado = NULL;

    do {
        printf("\n--- Sistema de Gerenciamento de Estoque (AVL) ---\n");
        printf("1. Inserir Produto\n");
        printf("2. Buscar Produto\n");
        printf("3. Remover Produto\n");
        printf("4. Exibir Produtos (Em Ordem)\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Digite o ID: ");
                scanf("%d", &p.id);
                getchar(); // Consumir o \n
                printf("Digite o Nome: ");
                fgets(p.nome, 100, stdin);
                p.nome[strcspn(p.nome, "\n")] = 0; // Remove \n
                printf("Digite o Preco: ");
                scanf("%f", &p.preco);
                printf("Digite a Quantidade: ");
                scanf("%d", &p.quantidade);
                raiz = inserir(raiz, p);
                printf("Produto inserido com sucesso!\n");
                break;
            case 2:
                printf("Digite o ID para busca: ");
                scanf("%d", &idBusca);
                resultado = buscar(raiz, idBusca);
                if (resultado != NULL) {
                    printf("\nProduto Encontrado:\n");
                    printf("ID: %d\nNome: %s\nPreco: %.2f\nQuantidade: %d\n",
                           resultado->produto.id, resultado->produto.nome,
                           resultado->produto.preco, resultado->produto.quantidade);
                } else {
                    printf("\nProduto com ID %d nao existe no estoque.\n", idBusca);
                }
                break;
            case 3:
                printf("Digite o ID para remover: ");
                scanf("%d", &idBusca);
                resultado = buscar(raiz, idBusca);
                if (resultado != NULL) {
                    raiz = remover(raiz, idBusca);
                    printf("Produto removido com sucesso!\n");
                } else {
                    printf("\nProduto com ID %d nao existe no estoque.\n", idBusca);
                }
                break;
            case 4:
                printf("\n--- Produtos em Estoque ---\n");
                if (raiz == NULL) {
                    printf("Estoque vazio.\n");
                } else {
                    exibirEmOrdem(raiz);
                }
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);

    liberarArvore(raiz);
    return 0;
}

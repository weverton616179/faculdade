#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

// Definicoes e Estruturas
typedef enum {
    ACIDENTE,
    SEMAFORO,
    ENERGIA,
    ALAGAMENTO,
    INCENDIO
} TipoEvento;

typedef enum {
    ATIVO,
    RESOLVIDO
} StatusEvento;

typedef struct {
    int dia, mes, ano;
    int hora, minuto;
} DataHora;

typedef struct {
    int id;
    TipoEvento tipo;
    int severidade; // 1 a 5
    DataHora dataHora;
    char regiao[50];
    StatusEvento status;
} Evento;

typedef struct Node {
    Evento evento;
    struct Node *esquerda;
    struct Node *direita;
    int altura;
} Node;

// Variavel global para metricas
int total_rotacoes = 0;

// Funcoes Utilitarias AVL
int getAltura(Node *N) {
    if (N == NULL)
        return 0;
    return N->altura;
}


Node* novoNo(Evento evento) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->evento = evento;
    node->esquerda = NULL;
    node->direita = NULL;
    node->altura = 1;
    return node;
}

Node *rotacaoDireita(Node *y) {
    total_rotacoes++;
    Node *x = y->esquerda;
    Node *T2 = x->direita;

    x->direita = y;
    y->esquerda = T2;

    y->altura = max(getAltura(y->esquerda), getAltura(y->direita)) + 1;
    x->altura = max(getAltura(x->esquerda), getAltura(x->direita)) + 1;

    return x;
}

Node *rotacaoEsquerda(Node *x) {
    total_rotacoes++;
    Node *y = x->direita;
    Node *T2 = y->esquerda;

    y->esquerda = x;
    x->direita = T2;

    x->altura = max(getAltura(x->esquerda), getAltura(x->direita)) + 1;
    y->altura = max(getAltura(y->esquerda), getAltura(y->direita)) + 1;

    return y;
}

int getBalanceamento(Node *N) {
    if (N == NULL)
        return 0;
    return getAltura(N->esquerda) - getAltura(N->direita);
}

// Insercao na arvore AVL
Node* inserir(Node* node, Evento evento) {
    if (node == NULL)
        return novoNo(evento);

    if (evento.id < node->evento.id)
        node->esquerda = inserir(node->esquerda, evento);
    else if (evento.id > node->evento.id)
        node->direita = inserir(node->direita, evento);
    else
        return node;

    node->altura = 1 + max(getAltura(node->esquerda), getAltura(node->direita));

    int balanceamento = getBalanceamento(node);

    if (balanceamento > 1 && evento.id < node->esquerda->evento.id)
        return rotacaoDireita(node);

    if (balanceamento < -1 && evento.id > node->direita->evento.id)
        return rotacaoEsquerda(node);

    if (balanceamento > 1 && evento.id > node->esquerda->evento.id) {
        node->esquerda = rotacaoEsquerda(node->esquerda);
        return rotacaoDireita(node);
    }

    if (balanceamento < -1 && evento.id < node->direita->evento.id) {
        node->direita = rotacaoDireita(node->direita);
        return rotacaoEsquerda(node);
    }

    return node;
}

// Busca por ID
Node* buscar(Node* root, int id) {
    if (root == NULL)
        return NULL;
    
    if (id < root->evento.id)
        return buscar(root->esquerda, id);
    else if (id > root->evento.id)
        return buscar(root->direita, id);
    
    return root;
}

// Utilitario para remocao
Node* noMenorValor(Node* node) {
    Node* atual = node;
    while (atual->esquerda != NULL)
        atual = atual->esquerda;
    return atual;
}

// Remocao na arvore AVL
Node* remover(Node* root, int id) {
    if (root == NULL)
        return root;

    if (id < root->evento.id)
        root->esquerda = remover(root->esquerda, id);
    else if (id > root->evento.id)
        root->direita = remover(root->direita, id);
    else {
        if ((root->esquerda == NULL) || (root->direita == NULL)) {
            Node *temp = root->esquerda ? root->esquerda : root->direita;

            if (temp == NULL) {
                temp = root;
                root = NULL;
            } else
                *root = *temp;

            free(temp);
        } else {
            Node* temp = noMenorValor(root->direita);
            root->evento = temp->evento;
            root->direita = remover(root->direita, temp->evento.id);
        }
    }

    if (root == NULL)
        return root;

    root->altura = 1 + max(getAltura(root->esquerda), getAltura(root->direita));
    int balanceamento = getBalanceamento(root);

    if (balanceamento > 1 && getBalanceamento(root->esquerda) >= 0)
        return rotacaoDireita(root);

    if (balanceamento > 1 && getBalanceamento(root->esquerda) < 0) {
        root->esquerda = rotacaoEsquerda(root->esquerda);
        return rotacaoDireita(root);
    }

    if (balanceamento < -1 && getBalanceamento(root->direita) <= 0)
        return rotacaoEsquerda(root);

    if (balanceamento < -1 && getBalanceamento(root->direita) > 0) {
        root->direita = rotacaoDireita(root->direita);
        return rotacaoEsquerda(root);
    }

    return root;
}

// Exibicao de um evento
void imprimirEvento(Evento e) {
    const char* tipos[] = {"Acidente", "Semaforo", "Energia", "Alagamento", "Incendio"};
    const char* statuses[] = {"Ativo", "Resolvido"};
    printf("ID: %d | Tipo: %s | Sev: %d | Regiao: %s | Status: %s | Data: %02d/%02d/%04d %02d:%02d\n",
           e.id, tipos[e.tipo], e.severidade, e.regiao, statuses[e.status],
           e.dataHora.dia, e.dataHora.mes, e.dataHora.ano, e.dataHora.hora, e.dataHora.minuto);
}

// Consultas Avancadas
void listarAtivosPorSeveridade(Node* root, int min, int max) {
    if (root != NULL) {
        listarAtivosPorSeveridade(root->esquerda, min, max);
        if (root->evento.status == ATIVO && root->evento.severidade >= min && root->evento.severidade <= max) {
            imprimirEvento(root->evento);
        }
        listarAtivosPorSeveridade(root->direita, min, max);
    }
}

void listarAtivosPorRegiao(Node* root, const char* regiao) {
    if (root != NULL) {
        listarAtivosPorRegiao(root->esquerda, regiao);
        if (root->evento.status == ATIVO && strcmp(root->evento.regiao, regiao) == 0) {
            imprimirEvento(root->evento);
        }
        listarAtivosPorRegiao(root->direita, regiao);
    }
}

void listarPorIntervaloID(Node* root, int minID, int maxID) {
    if (root != NULL) {
        if (minID < root->evento.id) 
            listarPorIntervaloID(root->esquerda, minID, maxID);
        
        if (root->evento.id >= minID && root->evento.id <= maxID) 
            imprimirEvento(root->evento);
            
        if (maxID > root->evento.id) 
            listarPorIntervaloID(root->direita, minID, maxID);
    }
}

// Metricas
int contarNos(Node* root) {
    if (root == NULL) return 0;
    return 1 + contarNos(root->esquerda) + contarNos(root->direita);
}

int contarAtivos(Node* root) {
    if (root == NULL) return 0;
    int count = (root->evento.status == ATIVO) ? 1 : 0;
    return count + contarAtivos(root->esquerda) + contarAtivos(root->direita);
}

int somarBalanceamentos(Node* root) {
    if (root == NULL) return 0;
    return getBalanceamento(root) + somarBalanceamentos(root->esquerda) + somarBalanceamentos(root->direita);
}

float fatorBalanceamentoMedio(Node* root) {
    int totalNos = contarNos(root);
    if (totalNos == 0) return 0.0;
    return (float)somarBalanceamentos(root) / totalNos;
}

// Liberar memoria
void liberarArvore(Node* root) {
    if (root != NULL) {
        liberarArvore(root->esquerda);
        liberarArvore(root->direita);
        free(root);
    }
}

// Menu principal
void exibirMenu() {
    printf("\n--- Sistema de Gerenciamento de Eventos Criticos ---\n");
    printf("1. Cadastrar Evento\n");
    printf("2. Remover Evento (Somente Resolvidos)\n");
    printf("3. Alterar Status (Ativo -> Resolvido)\n");
    printf("4. Atualizar Severidade\n");
    printf("5. Buscar Evento por ID\n");
    printf("6. Listar Ativos por Severidade\n");
    printf("7. Listar Ativos por Regiao\n");
    printf("8. Buscar por Intervalo de ID\n");
    printf("9. Exibir Metricas da Arvore\n");
    printf("0. Sair\n");
    printf("Escolha uma opcao: ");
}

int main() {
    Node* raiz = NULL;
    int opcao, id, min, max, tipo_int;
    char regiao[50];
    Evento e;
    Node* res;

    do {
        exibirMenu();
        if (scanf("%d", &opcao) != 1) {
            while (getchar() != '\n'); // limpa buffer
            continue;
        }

        switch (opcao) {
            case 1:
                printf("ID do Evento: ");
                scanf("%d", &e.id);
                printf("Tipo (0-Acidente, 1-Semaforo, 2-Energia, 3-Alagamento, 4-Incendio): ");
                scanf("%d", &tipo_int);
                e.tipo = (TipoEvento)tipo_int;
                printf("Severidade (1 a 5): ");
                scanf("%d", &e.severidade);
                printf("Data (DD MM AAAA): ");
                scanf("%d %d %d", &e.dataHora.dia, &e.dataHora.mes, &e.dataHora.ano);
                printf("Hora (HH MM): ");
                scanf("%d %d", &e.dataHora.hora, &e.dataHora.minuto);
                printf("Regiao: ");
                scanf(" %49[^\n]", e.regiao);
                e.status = ATIVO;
                raiz = inserir(raiz, e);
                printf("Evento cadastrado com sucesso!\n");
                break;

            case 2:
                printf("ID do Evento para remover: ");
                scanf("%d", &id);
                res = buscar(raiz, id);
                if (res != NULL) {
                    if (res->evento.status == RESOLVIDO) {
                        raiz = remover(raiz, id);
                        printf("Evento removido com sucesso!\n");
                    } else {
                        printf("Erro: Apenas eventos resolvidos podem ser removidos.\n");
                    }
                } else {
                    printf("Evento nao encontrado.\n");
                }
                break;

            case 3:
                printf("ID do Evento para resolver: ");
                scanf("%d", &id);
                res = buscar(raiz, id);
                if (res != NULL) {
                    if (res->evento.status == ATIVO) {
                        res->evento.status = RESOLVIDO;
                        printf("Status atualizado para Resolvido!\n");
                    } else {
                        printf("O evento ja esta resolvido.\n");
                    }
                } else {
                    printf("Evento nao encontrado.\n");
                }
                break;

            case 4:
                printf("ID do Evento para atualizar severidade: ");
                scanf("%d", &id);
                res = buscar(raiz, id);
                if (res != NULL) {
                    if (res->evento.status == ATIVO) {
                        printf("Nova severidade (1 a 5): ");
                        scanf("%d", &e.severidade);
                        res->evento.severidade = e.severidade;
                        printf("Severidade atualizada!\n");
                    } else {
                        printf("Apenas eventos ativos podem ter a severidade alterada.\n");
                    }
                } else {
                    printf("Evento nao encontrado.\n");
                }
                break;

            case 5:
                printf("ID do Evento: ");
                scanf("%d", &id);
                res = buscar(raiz, id);
                if (res != NULL) {
                    imprimirEvento(res->evento);
                } else {
                    printf("Evento nao encontrado.\n");
                }
                break;

            case 6:
                printf("Severidade minima e maxima (ex: 3 5): ");
                scanf("%d %d", &min, &max);
                printf("\n--- Eventos Ativos com Severidade entre %d e %d ---\n", min, max);
                listarAtivosPorSeveridade(raiz, min, max);
                break;

            case 7:
                printf("Regiao: ");
                scanf(" %49[^\n]", regiao);
                printf("\n--- Eventos Ativos na Regiao: %s ---\n", regiao);
                listarAtivosPorRegiao(raiz, regiao);
                break;

            case 8:
                printf("ID minimo e maximo (ex: 10 50): ");
                scanf("%d %d", &min, &max);
                printf("\n--- Eventos com ID entre %d e %d ---\n", min, max);
                listarPorIntervaloID(raiz, min, max);
                break;

            case 9:
                printf("\n--- Metricas da Arvore ---\n");
                printf("Altura total da arvore: %d\n", getAltura(raiz));
                printf("Numero total de nos: %d\n", contarNos(raiz));
                printf("Numero de eventos ativos: %d\n", contarAtivos(raiz));
                printf("Fator de balanceamento medio: %.2f\n", fatorBalanceamentoMedio(raiz));
                printf("Quantidade total de rotacoes realizadas: %d\n", total_rotacoes);
                break;

            case 0:
                printf("Encerrando o sistema e liberando memoria...\n");
                break;

            default:
                printf("Opcao invalida. Tente novamente.\n");
        }
    } while (opcao != 0);

    liberarArvore(raiz);
    return 0;
}

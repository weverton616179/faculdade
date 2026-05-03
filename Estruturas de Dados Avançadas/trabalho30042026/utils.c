#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

int total_rotacoes = 0;

// Funcao utilitaria para retornar o maior valor entre dois inteiros
int max(int a, int b) {
    return (a > b) ? a : b;
}

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

Node* buscar(Node* root, int id) {
    if (root == NULL)
        return NULL;
    
    if (id < root->evento.id)
        return buscar(root->esquerda, id);
    else if (id > root->evento.id)
        return buscar(root->direita, id);
    
    return root;
}

Node* noMenorValor(Node* node) {
    Node* atual = node;
    while (atual->esquerda != NULL)
        atual = atual->esquerda;
    return atual;
}

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

void imprimirEvento(Evento e) {
    const char* tipos[] = {"Acidente", "Semaforo", "Energia", "Alagamento", "Incendio"};
    const char* statuses[] = {"Ativo", "Resolvido"};
    printf("ID: %d | Tipo: %s | Sev: %d | Regiao: %s | Status: %s | Data: %02d/%02d/%04d %02d:%02d\n",
           e.id, tipos[e.tipo], e.severidade, e.regiao, statuses[e.status],
           e.dataHora.dia, e.dataHora.mes, e.dataHora.ano, e.dataHora.hora, e.dataHora.minuto);
}

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

void liberarArvore(Node* root) {
    if (root != NULL) {
        liberarArvore(root->esquerda);
        liberarArvore(root->direita);
        free(root);
    }
}
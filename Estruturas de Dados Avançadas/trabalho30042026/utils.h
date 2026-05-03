#ifndef UTILS_H
#define UTILS_H

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

extern int total_rotacoes;

// Funcao utilitaria para retornar o maior valor entre dois inteiros
int max(int a, int b);

int getAltura(Node *N);
Node* novoNo(Evento evento);
Node *rotacaoDireita(Node *y);
Node *rotacaoEsquerda(Node *x);
int getBalanceamento(Node *N);
Node* inserir(Node* node, Evento evento);
Node* buscar(Node* root, int id);
Node* noMenorValor(Node* node);
Node* remover(Node* root, int id);
void imprimirEvento(Evento e);
void listarAtivosPorSeveridade(Node* root, int min, int max);
void listarAtivosPorRegiao(Node* root, const char* regiao);
void listarPorIntervaloID(Node* root, int minID, int maxID);
int contarNos(Node* root);
int contarAtivos(Node* root);
int somarBalanceamentos(Node* root);
float fatorBalanceamentoMedio(Node* root);
void liberarArvore(Node* root);

#endif

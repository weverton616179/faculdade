#ifndef UTILS_H
#define UTILS_H

// ============================================================================
// Definicoes e Estruturas
// ============================================================================

// Enumeração para representar os tipos de eventos críticos urbanos
typedef enum {
    ACIDENTE,
    SEMAFORO,
    ENERGIA,
    ALAGAMENTO,
    INCENDIO
} TipoEvento;

// Enumeração para o status atual do evento
typedef enum {
    ATIVO,
    RESOLVIDO
} StatusEvento;

// Estrutura para armazenar a data e hora do registro do evento
typedef struct {
    int dia, mes, ano;
    int hora, minuto;
} DataHora;

// Estrutura principal que representa um evento crítico
typedef struct {
    int id;               // Chave primária do evento
    TipoEvento tipo;      // Tipo do evento (enum)
    int severidade;       // Nível de severidade (1 a 5)
    DataHora dataHora;    // Data e hora em que o evento foi registrado
    char regiao[50];      // Região da cidade afetada
    StatusEvento status;  // Status atual (Ativo ou Resolvido)
} Evento;

// Estrutura do Nó da Árvore AVL
typedef struct Node {
    Evento evento;        // Dados do evento armazenado no nó
    struct Node *esquerda;  // Ponteiro para a subárvore esquerda
    struct Node *direita;   // Ponteiro para a subárvore direita
    int altura;           // Altura do nó para cálculo do fator de balanceamento
} Node;

// Variável global para contabilizar as rotações realizadas na árvore
extern int total_rotacoes;

// ============================================================================
// Funções Utilitárias e Operações da Árvore AVL
// ============================================================================

// Retorna o maior valor entre dois inteiros
int max(int a, int b);

// Retorna a altura de um nó (0 se nulo)
int getAltura(Node *N);

// Cria um novo nó da árvore AVL com o evento fornecido
Node* novoNo(Evento evento);

// Realiza a rotação simples à direita para manter o balanceamento da AVL
Node *rotacaoDireita(Node *y);

// Realiza a rotação simples à esquerda para manter o balanceamento da AVL
Node *rotacaoEsquerda(Node *x);

// Calcula o fator de balanceamento de um nó (altura(esq) - altura(dir))
int getBalanceamento(Node *N);

// Insere um novo evento na árvore AVL e rebalanceia se necessário
Node* inserir(Node* node, Evento evento);

// Busca um evento na árvore AVL pelo seu ID (O(log n))
Node* buscar(Node* root, int id);

// Encontra o nó com o menor valor na árvore (usado na remoção)
Node* noMenorValor(Node* node);

// Remove um evento da árvore AVL pelo ID e rebalanceia a árvore
Node* remover(Node* root, int id);

// Imprime os dados de um evento formatados na tela
void imprimirEvento(Evento e);

// Lista todos os eventos ativos cuja severidade esteja no intervalo [min, max]
void listarAtivosPorSeveridade(Node* root, int min, int max);

// Lista todos os eventos ativos ocorrendo em uma região específica (percurso em-ordem)
void listarAtivosPorRegiao(Node* root, const char* regiao);

// Lista os eventos cujo ID esteja dentro do intervalo [minID, maxID] de forma eficiente
void listarPorIntervaloID(Node* root, int minID, int maxID);

// Retorna o número total de nós cadastrados na árvore
int contarNos(Node* root);

// Retorna a quantidade de eventos com o status ATIVO na árvore
int contarAtivos(Node* root);

// Calcula a soma de todos os fatores de balanceamento dos nós (auxiliar)
int somarBalanceamentos(Node* root);

// Retorna o fator de balanceamento médio da árvore AVL
float fatorBalanceamentoMedio(Node* root);

// Libera toda a memória alocada para a árvore (uso ao encerrar o programa)
void liberarArvore(Node* root);

#endif


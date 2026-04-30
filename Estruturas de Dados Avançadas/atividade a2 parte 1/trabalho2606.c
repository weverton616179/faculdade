#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// estrutura do nó da árvore
typedef struct Funcionario {
    int matricula;              
    char nome[100];             
    char cargo[50];
    float salario;  
    struct Funcionario *left;
    struct Funcionario *right;
} Funcionario;


// função para limpar o buffer do teclado e evita bugs ao ler strings após ler números
void limparTeclado() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// função para criar um novo nó (funcionário) dinamicamente na memória
Funcionario* criarFuncionario(int matricula, const char* nome, const char* cargo, float salario) {
    Funcionario* novo = (Funcionario*)malloc(sizeof(Funcionario));
    novo->matricula = matricula;
    strcpy(novo->nome, nome);
    strcpy(novo->cargo, cargo);
    novo->salario = salario;
    novo->left = NULL;
    novo->right = NULL;
    return novo;
}

// insere um novo funcionário na árvore binária de pesquisa usando recursão.
Funcionario* inserirFuncionario(Funcionario* raiz, int matricula, const char* nome, const char* cargo, float salario) {
    // se a árvore/subárvore estiver vazia, cria o nó aqui
    if (raiz == NULL) {
        printf("Funcionario inserido com sucesso!\n");
        return criarFuncionario(matricula, nome, cargo, salario);
    }

    // se a matrícula for menor que a do nó atual, insere na subárvore ESQUERDA
    if (matricula < raiz->matricula) {
        raiz->left = inserirFuncionario(raiz->left, matricula, nome, cargo, salario);
    }
    // se a matrícula for maior, insere na subárvore DIREITA
    else if (matricula > raiz->matricula) {
        raiz->right = inserirFuncionario(raiz->right, matricula, nome, cargo, salario);
    }
    // se a matrícula já existir, não permite duplicatas
    else {
        printf("Erro: Matricula %d ja cadastrada no sistema!\n", matricula);
    }

    return raiz;
}

// busca um funcionário pela matrícula. Retorna o ponteiro para o nó se encontrar, ou NULL.
Funcionario* buscarFuncionario(Funcionario* raiz, int matricula) {
    // caso chegue em um nó nulo ou encontrou a matrícula
    if (raiz == NULL || raiz->matricula == matricula) {
        return raiz;
    }

    // se a matrícula buscada for menor, continua a busca na subárvore ESQUERDA
    if (matricula < raiz->matricula) {
        return buscarFuncionario(raiz->left, matricula);
    }

    // se a matrícula buscada for maior, continua a busca na subárvore DIREITA
    return buscarFuncionario(raiz->right, matricula);
}

// busca o funcionário e, se encontrado, permite atualizar nome, cargo e salário.
void atualizarFuncionario(Funcionario* raiz, int matricula) {
    Funcionario* funcionario = buscarFuncionario(raiz, matricula);
    
    if (funcionario != NULL) {
        printf("\n--- Funcionario Encontrado ---\n");
        printf("Matricula: %d | Nome atual: %s\n", funcionario->matricula, funcionario->nome);
        
        printf("Novo Nome: ");
        scanf("%99[^\n]", funcionario->nome);
        limparTeclado();
        
        printf("Novo Cargo: ");
        scanf("%49[^\n]", funcionario->cargo);
        limparTeclado();
        
        printf("Novo Salario: ");
        scanf("%f", &funcionario->salario);
        limparTeclado();
        
        printf("Dados atualizados com sucesso!\n");
    } else {
        printf("Erro: Funcionario com matricula %d nao encontrado.\n", matricula);
    }
}


// travessia In-Order visitando Esquerda -> Raiz -> Direita.
// garante que os funcionários sejam impressos em ordem crescente de matrícula.
void listarFuncionarios(Funcionario* raiz) {
    if (raiz != NULL) {
        listarFuncionarios(raiz->left);
        
        printf("Matricula: %-5d | Nome: %-20s | Cargo: %-15s | Salario: R$ %.2f\n", 
               raiz->matricula, raiz->nome, raiz->cargo, raiz->salario);
               
        listarFuncionarios(raiz->right);
    }
}

// libera a memória da árvore ao encerrar o programa
void liberarArvore(Funcionario* raiz) {
    if (raiz != NULL) {
        liberarArvore(raiz->left);
        liberarArvore(raiz->right);
        free(raiz);
    }
}

// menu interativo
int main() {
    Funcionario* raiz = NULL;
    int opcao, matricula;
    char nome[100], cargo[50];
    float salario;

    do {
        printf("\n========================================\n");
        printf(" SISTEMA DE FUNCIONARIOS - ARVORE BINARIA \n");
        printf("========================================\n");
        printf("1. Inserir Funcionario\n");
        printf("2. Atualizar Funcionario\n");
        printf("3. Buscar Funcionario\n");
        printf("4. Listar Todos os Funcionarios\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        limparTeclado();

        switch (opcao) {
            case 1:
                printf("\n--- Inserir Novo Funcionario ---\n");
                printf("Matricula: ");
                scanf("%d", &matricula);
                limparTeclado();
                
                printf("Nome: ");
                scanf("%99[^\n]", nome);
                limparTeclado();
                
                printf("Cargo: ");
                scanf("%49[^\n]", cargo);
                limparTeclado();
                
                printf("Salario: ");
                scanf("%f", &salario);
                limparTeclado();
                
                raiz = inserirFuncionario(raiz, matricula, nome, cargo, salario);
                break;

            case 2:
                printf("\n--- Atualizar Funcionario ---\n");
                printf("Informe a matricula do funcionario: ");
                scanf("%d", &matricula);
                limparTeclado();
                atualizarFuncionario(raiz, matricula);
                break;

            case 3:
                printf("\n--- Buscar Funcionario ---\n");
                printf("Informe a matricula: ");
                scanf("%d", &matricula);
                limparTeclado();
                
                Funcionario* encontrado = buscarFuncionario(raiz, matricula);
                if (encontrado != NULL) {
                    printf("\n*** Funcionario Localizado ***\n");
                    printf("Matricula: %d\nNome: %s\nCargo: %s\nSalario: R$ %.2f\n", 
                           encontrado->matricula, encontrado->nome, encontrado->cargo, encontrado->salario);
                } else {
                    printf("Funcionario nao localizado na base de dados.\n");
                }
                break;

            case 4:
                printf("\n--- Lista de Funcionarios (Ordenados por Matricula) ---\n");
                if (raiz == NULL) {
                    printf("Nenhum funcionario cadastrado.\n");
                } else {
                    listarFuncionarios(raiz);
                }
                break;

            case 0:
                printf("Encerrando o sistema e liberando memoria...\n");
                liberarArvore(raiz);
                break;

            default:
                printf("Opcao invalida! Tente novamente.\n");
        }
    } while (opcao != 0);

    return 0;
}
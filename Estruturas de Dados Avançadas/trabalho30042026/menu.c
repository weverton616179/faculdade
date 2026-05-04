#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include "menu.h"
#include "utils.h"

// Le o ID do evento de forma segura e com validacao
void scan_id_evento(Evento* e){
    double aux;
    int is_valid = 0;
    do {
        printf("ID do Evento: ");
        if (scanf("%lf", &aux) == 1) {
            if (aux <= 0 || aux != (int)aux) {
                printf("ID invalido. Tente novamente.\n");
            } else {
                is_valid = 1;
            }
        } else {
            printf("ID invalido. Tente novamente.\n");
        }
        int c;
        while ((c = getchar()) != '\n' && c != EOF); // limpa o buffer
    } while(!is_valid);
    e->id = (int)aux;
}

// Le um valor inteiro de forma segura e garante que estara entre min e max
int scan_inteiro(const char* prompt, int min, int max) {
    double aux;
    int is_valid = 0;
    do {
        if (prompt) printf("%s", prompt);
        if (scanf("%lf", &aux) == 1) {
            if (aux < min || aux > max || aux != (int)aux) {
                printf("Entrada invalida. Tente novamente.\n");
            } else {
                is_valid = 1;
            }
        } else {
            printf("Entrada invalida. Tente novamente.\n");
        }
        int c;
        while ((c = getchar()) != '\n' && c != EOF); // limpa o buffer
    } while(!is_valid);
    return (int)aux;
}

void scan_data(int *dia, int *mes, int *ano) {
    int is_valid = 0;
    do {
        printf("Data (DD MM AAAA): ");
        if (scanf("%d %d %d", dia, mes, ano) == 3) {
            if (*dia >= 1 && *dia <= 31 && *mes >= 1 && *mes <= 12 && *ano >= 1900 && *ano <= 2100) {
                is_valid = 1;
            } else {
                printf("Data invalida. Tente novamente.\n");
            }
        } else {
            printf("Data invalida. Tente novamente.\n");
        }
        int c;
        while ((c = getchar()) != '\n' && c != EOF); // limpa o buffer
    } while(!is_valid);
}

void scan_hora(int *hora, int *minuto) {
    int is_valid = 0;
    do {
        printf("Hora (HH MM): ");
        if (scanf("%d %d", hora, minuto) == 2) {
            if (*hora >= 0 && *hora <= 23 && *minuto >= 0 && *minuto <= 59) {
                is_valid = 1;
            } else {
                printf("Hora invalida. Tente novamente.\n");
            }
        } else {
            printf("Hora invalida. Tente novamente.\n");
        }
        int c;
        while ((c = getchar()) != '\n' && c != EOF); // limpa o buffer
    } while(!is_valid);
}

void scan_intervalo(const char* prompt, int *min, int *max, int min_val, int max_val) {
    int is_valid = 0;
    do {
        if (prompt) printf("%s", prompt);
        if (scanf("%d %d", min, max) == 2) {
            if (*min >= min_val && *max <= max_val && *min <= *max) {
                is_valid = 1;
            } else {
                printf("Intervalo invalido. Tente novamente.\n");
            }
        } else {
            printf("Intervalo invalido. Tente novamente.\n");
        }
        int c;
        while ((c = getchar()) != '\n' && c != EOF); // limpa o buffer
    } while(!is_valid);
}

void scan_string(const char* prompt, char* str, int size) {
    int is_valid = 0;
    do {
        if (prompt) printf("%s", prompt);
        if (fgets(str, size, stdin) != NULL) {
            size_t len = strlen(str);
            if (len > 0 && str[len-1] == '\n') {
                str[len-1] = '\0';
            } else {
                int c;
                while ((c = getchar()) != '\n' && c != EOF);
            }
            if (strlen(str) > 0) {
                is_valid = 1;
            } else {
                printf("Entrada invalida. Tente novamente.\n");
            }
        }
    } while (!is_valid);
}

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

// Laco principal que exibe o menu e trata a entrada do usuario
void executarMenu() {
    Node* raiz = NULL;
    int opcao, id, min, max, tipo_int;
    char regiao[50];
    Evento e;
    Node* res;

    do {
        exibirMenu();
        opcao = scan_inteiro(NULL, 0, 9);

        switch (opcao) {
            case 1:
                // Leitura do ID com validacao robusta
                scan_id_evento(&e);
                
                // Verifica se o ID ja existe na arvore AVL
                if (buscar(raiz, e.id) != NULL) {
                    printf("Erro: Ja existe um evento cadastrado com o ID %d.\n", e.id);
                    break; // Retorna ao menu
                }
                
                tipo_int = scan_inteiro("Tipo (0-Acidente, 1-Semaforo, 2-Energia, 3-Alagamento, 4-Incendio): ", 0, 4);
                e.tipo = (TipoEvento)tipo_int;
                e.severidade = scan_inteiro("Severidade (1 a 5): ", 1, 5);
                scan_data(&e.dataHora.dia, &e.dataHora.mes, &e.dataHora.ano);
                scan_hora(&e.dataHora.hora, &e.dataHora.minuto);
                scan_string("Regiao: ", e.regiao, sizeof(e.regiao));
                e.status = ATIVO;
                raiz = inserir(raiz, e);
                printf("Evento cadastrado com sucesso!\n");
                break;

            case 2:
                id = scan_inteiro("ID do Evento para remover: ", 1, INT_MAX);
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
                id = scan_inteiro("ID do Evento para resolver: ", 1, INT_MAX);
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
                id = scan_inteiro("ID do Evento para atualizar severidade: ", 1, INT_MAX);
                res = buscar(raiz, id);
                if (res != NULL) {
                    if (res->evento.status == ATIVO) {
                        e.severidade = scan_inteiro("Nova severidade (1 a 5): ", 1, 5);
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
                id = scan_inteiro("ID do Evento: ", 1, INT_MAX);
                res = buscar(raiz, id);
                if (res != NULL) {
                    imprimirEvento(res->evento);
                } else {
                    printf("Evento nao encontrado.\n");
                }
                break;

            case 6:
                scan_intervalo("Severidade minima e maxima (ex: 3 5): ", &min, &max, 1, 5);
                printf("\n--- Eventos Ativos com Severidade entre %d e %d ---\n", min, max);
                listarAtivosPorSeveridade(raiz, min, max);
                break;

            case 7:
                scan_string("Regiao: ", regiao, sizeof(regiao));
                printf("\n--- Eventos Ativos na Regiao: %s ---\n", regiao);
                listarAtivosPorRegiao(raiz, regiao);
                break;

            case 8:
                scan_intervalo("ID minimo e maximo (ex: 10 50): ", &min, &max, 1, INT_MAX);
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
}

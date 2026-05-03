#include <stdio.h>
#include <stdlib.h>
#include "menu.h"
#include "utils.h"

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

void executarMenu() {
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
                // printf("ID do Evento: ");
                // scanf("%d", &e.id);
                scan_id_evento(&e);
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
}

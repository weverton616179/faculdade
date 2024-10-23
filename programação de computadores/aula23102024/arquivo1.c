#include <stdio.h>
#include <stdlib.h>

int main() {
    
    FILE *arquivo = fopen("arquivo.txt", "a+");
    
    if (arquivo == NULL) {
    	printf("erro na abertura do arquivo");
	}
	
	fprintf(arquivo, "abcde\n");
	fflush(arquivo); //limpa u buffer e escreve antes do final da execução
	
	rewind(arquivo); //reposiciona o ponteiro no inicio do arquivo
	fseek(arquivo, 0, SEEK_SET); //define o lugar do ponteiro no aruivo, (arquivo, deslocamento, ponto inicial)
	
	scanf("asd");
	
	char teste;
	fscanf(arquivo, "%c",teste);
    printf("%c", teste);
    return 0;
}
